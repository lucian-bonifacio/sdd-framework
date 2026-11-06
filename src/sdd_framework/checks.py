"""Conferência estrutural; não substitui testes do produto ou aceite humano."""
from __future__ import annotations

import json
import os
import re
import tomllib
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .markdown import PLACEHOLDER, metadata, render, sections
from .project import END, START, bundle, load_config, managed_section
from .storage import SDDError, atomic_apply, digest, project_lock, read, read_json, safe_path


def markdown_files(root: Path, directory: str) -> list[str]:
    base = safe_path(root, directory)
    if not base.exists():
        return []
    if not base.is_dir():
        raise SDDError(f"Esperado diretório: {directory}")
    found = []
    for current, directories, filenames in os.walk(base, followlinks=False):
        for name in directories + filenames:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            safe_path(root, relative)
            if path.is_file() and path.suffix == ".md":
                found.append(relative)
    return sorted(found)


def inspect(root: Path, phase: str | None = None, spec: str | None = None) -> dict:
    config = load_config(root)
    policy = json.loads(bundle()["policy.json"])
    target = phase or config["phase"]
    if target not in policy["phases"]:
        raise SDDError(f"Etapa desconhecida: {target}")
    rank = policy["phases"].index(target)
    issues = []
    documents: dict[str, tuple[dict, str]] = {}

    def add(code, path, message, severity="error"):
        issues.append({"code": code, "path": path, "message": message, "severity": severity})

    def document(path, required_sections, frontmatter=True, accepted=False):
        content = read(root, path)
        if content is None:
            add("missing_document", path, "Documento obrigatório ausente")
            return None
        parsed_sections = sections(content)
        for heading in required_sections:
            if not parsed_sections.get(heading, "").strip():
                add("empty_section", path, f"Seção obrigatória ausente/vazia: {heading}")
        if PLACEHOLDER.search(content):
            add("placeholder", path, "Modelo ainda contém campos por preencher")
        meta = {}
        if frontmatter:
            try:
                meta = metadata(content)
            except SDDError as exc:
                add("metadata", path, str(exc))
            if accepted and meta.get("status") != "accepted":
                add("unaccepted_document", path, "Documento deve estar accepted antes de avançar")
        documents[path] = (meta, content)
        return meta, content

    manifest = read_json(root, ".sdd/manifest.json")
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), dict) or not isinstance(manifest.get("blocks"), dict):
        raise SDDError("Manifesto inválido")
    if config.get("framework_version") != manifest.get("version"):
        add("version_mismatch", ".sdd/config.json", "Versão diverge do manifesto")
    installed = read_json(root, ".sdd/framework/bundle.json")
    if installed.get("version") != manifest.get("version"):
        add("version_mismatch", ".sdd/framework/bundle.json", "Versão do bundle diverge do manifesto")
    for relative, expected in manifest["files"].items():
        content = read(root, relative)
        if content is None or digest(content.encode()) != expected:
            add("managed_conflict", relative, "Recurso administrado ausente ou modificado; reconciliar antes de atualizar")
    required_blocks = ["AGENTS.md"] + (["CLAUDE.md"] if config["agent"] in ("claude", "both") else [])
    for relative in required_blocks:
        content = read(root, relative) or ""
        try:
            section = managed_section(content)
            expected = manifest["blocks"].get(relative)
            if section is None or not expected or digest(section.encode()) != expected:
                add("agent_instructions", relative, "Bloco SDD ausente ou alterado")
        except SDDError as exc:
            add("agent_instructions", relative, str(exc))
    if rank >= policy["phases"].index("implementation"):
        document("AGENTS.md", policy["templates"]["AGENTS.md"], False)
    if config["agent"] in ("codex", "both"):
        codex_config = read(root, ".codex/config.toml")
        if codex_config is None:
            add("codex_config_missing", ".codex/config.toml", "Configuração Codex ausente; execute update no terminal para preparar o arquivo padrão")
        else:
            try:
                tomllib.loads(codex_config)
            except tomllib.TOMLDecodeError as exc:
                add("codex_config_invalid", ".codex/config.toml", f"TOML inválido; conteúdo preservado: {exc}")
    # Manifesto é inventário, não autoridade para reduzir o conjunto obrigatório.
    required_resources = [f".sdd/framework/{name}" for name in bundle()]
    for agent, directory in (("codex", ".agents"), ("claude", ".claude")):
        if config["agent"] in (agent, "both"):
            required_resources.extend(f"{directory}/skills/sdd/{name.removeprefix('skill/')}" for name in bundle() if name.startswith("skill/"))
    for relative in required_resources:
        if relative not in manifest["files"]:
            add("untracked_resource", relative, "Recurso obrigatório não consta no manifesto")
    for directory in ("docs/inbox", "docs/decisions", "specs"):
        path = safe_path(root, directory)
        if not path.is_dir():
            add("missing_directory", directory, "Diretório SDD obrigatório ausente")
    document(".sdd/adoption/TASKS.md", policy["templates"]["TASKS.md"], False)
    if read(root, "scripts/atualizar_roadmap.py") is None:
        add("missing_consumer_script", "scripts/atualizar_roadmap.py", "Script autônomo de acompanhamento ausente; preparar a ferramenta local do consumidor")

    for canonical, rule in policy["project"].items():
        path = config.get("document_paths", {}).get(canonical, canonical)
        required = rank >= policy["phases"].index(rule["from"])
        if required or safe_path(root, path).exists():
            result = document(path, rule["sections"], canonical != "README.md", accepted=required and canonical != "README.md")
            if result and canonical != "README.md" and result[0].get("status") not in policy["document_states"]:
                add("document_state", path, "Estado de documento inválido")

    specs = [p for p in markdown_files(root, "specs") if p.endswith("/SPEC.md")]
    if spec is not None and (not re.fullmatch(r"\d{3,}-[a-z0-9]+(?:-[a-z0-9]+)*", spec) or f"specs/{spec}/SPEC.md" not in specs):
        raise SDDError("--spec deve identificar a pasta de uma SPEC existente: NNN-nome")
    if rank >= policy["phases"].index("design") and not specs:
        add("missing_spec", "specs", "A etapa exige pelo menos uma SPEC")
    spec_requirements: dict[str, set[str]] = {}
    spec_info = {}
    for path in specs:
        folder = str(Path(path).parent.as_posix())
        selected = spec is None or Path(folder).name == spec
        result = document(path, policy["templates"]["SPEC.md"], accepted=selected and rank >= policy["phases"].index("design"))
        if not result:
            continue
        meta, content = result
        spec_info[folder] = meta
        if meta.get("id") != Path(folder).name:
            add("spec_id", path, "ID da SPEC deve corresponder ao nome da pasta")
        if meta.get("status") not in policy["document_states"]:
            add("document_state", path, "Estado de SPEC inválido")
        reqs = re.findall(r"^\s*-\s+(?:\*\*)?((?:RF|RNF)-\d+)(?:\*\*)?:", sections(content).get("Requisitos", ""), re.M)
        spec_requirements[folder] = set(reqs)
        if not reqs:
            add("missing_requirements", path, "Definir requisitos identificados RF-NNN ou RNF-NNN")
        if len(reqs) != len(set(reqs)):
            add("duplicate_requirement", path, "IDs de requisitos duplicados na SPEC")
        if not re.search(r"\bCA-\d+\b", sections(content).get("Critérios de aceitação", "")):
            add("acceptance", path, "Definir critérios identificados CA-NNN")
        if meta.get("design") == "separate":
            document(folder + "/DESIGN.md", policy["templates"]["DESIGN.md"], accepted=selected and rank >= policy["phases"].index("tasks"))
        elif meta.get("design") != "inline":
            add("design_mode", path, "design deve ser inline ou separate")
        index = folder + "/TASKS.md"
        if (selected and rank >= policy["phases"].index("implementation")) or safe_path(root, index).exists():
            document(index, policy["templates"]["TASKS.md"], False)

    all_task_paths = markdown_files(root, ".sdd/adoption/tasks") + [p for p in markdown_files(root, "specs") if "/tasks/" in p]
    tasks = {}
    for path in all_task_paths:
        result = document(path, policy["templates"]["TASK.md"])
        if not result:
            continue
        meta, content = result
        tasks[path] = {**meta, "path": path, "title": next((s[2:] for s in content.splitlines() if s.startswith("# ")), path)}
        expected_id = Path(path).stem
        if not re.fullmatch(r"T-\d{3,}", expected_id) or meta.get("id") != expected_id:
            add("task_id", path, "ID T-NNN deve corresponder ao nome do ticket")
        for field, allowed in (("status", policy["task_states"]), ("executor", policy["executors"]), ("authorization", policy["authorizations"]), ("verification", policy["verification_states"])):
            if meta.get(field) not in allowed:
                add("task_metadata", path, f"Valor inválido em {field}")
        for field in ("dependencies", "requirements"):
            if not isinstance(meta.get(field), list):
                add("task_metadata", path, f"{field} deve ser lista JSON de strings")
        if meta.get("status") in ("ready", "in_progress", "done") and meta.get("authorization") != "approved":
            add("authorization", path, "Execução/conclusão exige autorização registrada")
        parts = sections(content)
        tasks[path]["human_action"] = parts.get("Ação humana pendente", "")
        if meta.get("status") in ("awaiting_user", "blocked"):
            action = parts.get("Ação humana pendente", "") if meta["status"] == "awaiting_user" else parts.get("Resultado", "")
            if not action or action.strip().lower() in ("nenhuma.", "nenhuma", "ainda não executada."):
                add("missing_blocker", path, "Registrar causa e ação concreta para desbloqueio")
        if meta.get("status") == "done":
            if meta.get("verification") not in ("passed", "not_applicable"):
                add("unverified_completion", path, "Conclusão exige passed ou not_applicable justificado")
            if parts.get("Resultado", "").strip().lower() in ("", "ainda não executada."):
                add("missing_result", path, "Conclusão exige resultado concreto e evidência")
            if parts.get("Ação humana pendente", "").strip().lower() not in ("nenhuma", "nenhuma.", "não se aplica", "não se aplica."):
                add("pending_human_action", path, "Não concluir com ação humana pendente")
        if meta.get("status") == "cancelled" and parts.get("Resultado", "").strip().lower() in ("", "ainda não executada."):
            add("missing_cancellation_reason", path, "Registrar motivo do cancelamento")
        if path.startswith("specs/"):
            folder = path.split("/tasks/", 1)[0]
            if folder not in spec_requirements:
                add("orphan_task", path, "Ticket sem SPEC correspondente")
            declared = meta.get("requirements")
            if not isinstance(declared, list) or not declared:
                add("task_requirements", path, "Ticket de produto exige requisitos da SPEC")
            elif set(declared) - spec_requirements.get(folder, set()):
                add("unknown_requirement", path, "Ticket referencia requisito inexistente na SPEC")
        index = path.split("/tasks/", 1)[0] + "/TASKS.md"
        index_content = read(root, index)
        if index_content is None or f"tasks/{Path(path).name}" not in index_content:
            add("unindexed_task", path, "Ticket deve estar vinculado no TASKS.md correspondente")

    if not any(p.startswith(".sdd/adoption/tasks/") for p in tasks):
        add("missing_adoption", ".sdd/adoption/tasks", "Plano de adequação sem tickets")
    graph = {}
    for path, task in tasks.items():
        dependencies = task.get("dependencies")
        graph[path] = dependencies if isinstance(dependencies, list) else []
        for dependency in graph[path]:
            safe_path(root, dependency)
            if dependency not in tasks:
                add("missing_dependency", path, f"Dependência inexistente: {dependency}")
            elif task.get("status") in ("ready", "in_progress", "done") and tasks[dependency].get("status") != "done":
                add("unmet_dependency", path, f"Dependência não concluída: {dependency}")
    visited, active = set(), set()

    def visit(path):
        if path in active:
            add("dependency_cycle", path, "Ciclo nas dependências")
            return
        if path in visited:
            return
        active.add(path)
        for dependency in graph.get(path, []):
            if dependency in graph:
                visit(dependency)
        active.remove(path)
        visited.add(path)

    for path in graph:
        visit(path)
    if rank >= policy["phases"].index("implementation"):
        for folder, requirements in spec_requirements.items():
            if spec is not None and Path(folder).name != spec:
                continue
            covered = set()
            for path, task in tasks.items():
                if path.startswith(folder + "/tasks/") and task.get("status") != "cancelled" and isinstance(task.get("requirements"), list):
                    covered.update(task["requirements"])
            if requirements - covered:
                add("uncovered_requirement", folder + "/SPEC.md", f"Requisitos sem tarefa: {', '.join(sorted(requirements - covered))}")
    if rank >= policy["phases"].index("validation"):
        for path, task in tasks.items():
            if spec is not None and path.startswith("specs/") and not path.startswith(f"specs/{spec}/tasks/"):
                continue
            if task.get("status") not in ("done", "cancelled"):
                add("unfinished_task", path, "Validação final exige encerrar as tarefas do conjunto")

    for directory, template, prefix, states in (("docs/inbox", "INBOX.md", "ITEM", policy["inbox_states"]), ("docs/decisions", "ADR.md", "ADR", policy["document_states"])):
        for path in markdown_files(root, directory):
            result = document(path, policy["templates"][template])
            if not result:
                continue
            meta, content = result
            if not re.fullmatch(prefix + r"-\d{3,}", Path(path).stem) or meta.get("id") != Path(path).stem:
                add("artifact_id", path, f"Esperado {prefix}-NNN correspondente ao arquivo")
            if meta.get("status") not in states:
                add("artifact_state", path, "Estado inválido")
            if prefix == "ITEM":
                try:
                    date.fromisoformat(meta.get("created", ""))
                except (ValueError, TypeError):
                    add("artifact_date", path, "created deve ser data ISO")
                if meta.get("status") == "pending":
                    add("inbox_pending", path, "Proposta aguardando avaliação; não altera requisitos", "info")
                elif sections(content).get("Destino ou justificativa", "").startswith("Pendente de avaliação"):
                    add("inbox_resolution", path, "Registrar destino ou motivo antes de encerrar item")
    if safe_path(root, "CHECKPOINT.md").exists():
        result = document("CHECKPOINT.md", policy["templates"]["CHECKPOINT.md"])
        if result:
            meta, _ = result
            if meta.get("status") not in policy["checkpoints"]:
                add("checkpoint_state", "CHECKPOINT.md", "Estado active ou closed esperado")
            try:
                date.fromisoformat(meta.get("updated", ""))
            except (ValueError, TypeError):
                add("checkpoint_date", "CHECKPOINT.md", "updated deve ser data ISO")
            if meta.get("task") != "none" and meta.get("task") not in tasks:
                add("checkpoint_task", "CHECKPOINT.md", "Ticket de retomada não encontrado")

    if config.get("interface") is None:
        add("interface_unknown", ".sdd/config.json", "Esclarecer se existe interface", "warning")
    if config.get("interface") is True and config.get("design_system") is None:
        add("design_system_absent", ".sdd/config.json", "Interface sem Design System informado; não criar contrato visual automaticamente", "warning")
    if config.get("design_system"):
        reference = config["design_system"]["reference"]
        if not urlsplit(reference).scheme and not safe_path(root, reference).is_file():
            add("design_system_reference", reference, "Design System local não encontrado")

    reports = [p for p in markdown_files(root, "specs") if "/validation/" in p]
    for path in reports:
        result = document(path, policy["templates"]["VALIDATION.md"])
        if result and (result[0].get("verification") not in policy["verification_states"] or not result[0].get("revision")):
            add("validation_metadata", path, "Relatório exige verification válido e revisão identificada")

    # Validar links locais dos documentos do consumidor; não seguir URLs ou links externos.
    for path, (_, content) in documents.items():
        for raw in re.findall(r"(?<!!)\[[^\]]+\]\(([^\s)]+)\)", content):
            link = unquote(raw.strip("<>"))
            if urlsplit(link).scheme or link.startswith("#"):
                continue
            target_link = link.split("#", 1)[0]
            if not target_link:
                continue
            relative = os.path.normpath(str(Path(path).parent / target_link)).replace(os.sep, "/")
            try:
                linked = safe_path(root, relative)
                if not linked.exists():
                    add("broken_link", path, f"Link local não encontrado: {raw}")
            except SDDError as exc:
                add("unsafe_link", path, str(exc))

    errors = {x["path"] for x in issues if x["severity"] == "error"}
    executable = []
    shared = set(config.get("document_paths", {}).get(k, k) for k in policy["project"]) | {"AGENTS.md", "CLAUDE.md"}
    for path, task in tasks.items():
        if task.get("status") in ("ready", "in_progress") and task.get("authorization") == "approved" and path not in errors and all(tasks.get(d, {}).get("status") == "done" and d not in errors for d in graph[path]):
            # Produto não fica pronto se documentos obrigatórios estão inválidos.
            folder = path.split("/tasks/", 1)[0] + "/"
            relevant_errors = any(x["severity"] == "error" and (x["path"] in shared or x["path"].startswith(".sdd/") or (x["path"].startswith(folder) and x["path"] not in tasks)) for x in issues)
            if path.startswith(".sdd/adoption/") or (rank >= policy["phases"].index("implementation") and (spec is None or path.startswith(f"specs/{spec}/tasks/")) and not relevant_errors):
                executable.append(path)
    counts = {state: sum(task.get("status") == state for task in tasks.values()) for state in policy["task_states"]}
    return {"schema_version": 1, "phase": target, "spec": spec, "structural_pass": not any(x["severity"] == "error" for x in issues), "semantic_review": "required", "issues": issues, "tasks": list(tasks.values()), "counts": counts, "executable": executable, "awaiting_user": [p for p, t in tasks.items() if t.get("status") == "awaiting_user"]}


def create_remediation(root: Path, report: dict) -> list[str]:
    """Gerar tickets deduplicados; não reparar conteúdo ou aprovar requisitos."""
    with project_lock(root):
        template = bundle()["templates/TASK.md"].decode()
        folder = ".sdd/adoption"
        existing_paths = markdown_files(root, folder + "/tasks")
        keys = set()
        highest = 0
        for path in existing_paths:
            content = read(root, path) or ""
            try:
                meta = metadata(content)
                if meta.get("remediation_key") and meta.get("status") not in ("done", "cancelled"):
                    keys.add(meta["remediation_key"])
            except SDDError:
                pass
            match = re.fullmatch(r"T-(\d+)", Path(path).stem)
            if match:
                highest = max(highest, int(match[1]))
        changes, created = {}, []
        index = read(root, folder + "/TASKS.md")
        if index is None:
            index = "# Adequação ao SDD\n\n## Índice\n\n## Ordem e acompanhamento\n\nEstados nos tickets; executar por dependência.\n"
        for issue in report["issues"]:
            if issue["severity"] != "error":
                continue
            key = digest((issue["code"] + ":" + issue["path"]).encode())
            if key in keys:
                continue
            highest += 1
            identifier = f"T-{highest:03}"
            path = f"{folder}/tasks/{identifier}.md"
            text = render(template, task_id=identifier, title=f"Adequar {issue['path']}")
            text = text.replace("authorization: pending", "authorization: approved").replace('requirements: ["RF-001"]', "requirements: []")
            text = text.replace("verification: not_verified", f"verification: not_verified\nremediation_key: {key}")
            replacements = {
                "[PREENCHER: resultado limitado, referenciando a SPEC.]": issue["message"],
                "[PREENCHER: trabalho incluído, exclusões e documentos a manter.]": f"Regularizar {issue['path']} conforme contratos. Preservar conteúdo; não aceitar decisões de produto sem evidência.",
                "[PREENCHER: resultados verificáveis desta tarefa.]": f"Achado {issue['code']} resolvido na conferência da etapa {report['phase']}.",
                "[PREENCHER: testes, revisão, comandos e evidências necessárias; não afirmar sucesso antes de executar.]": f"Executar sdd check --phase {report['phase']} e revisar semanticamente a correção.",
                "[PREENCHER: parte do agente e parte do usuário, se houver.]": "Agente prepara a adequação; usuário resolve decisões relevantes quando necessário.",
            }
            for before, after in replacements.items():
                text = text.replace(before, after)
            changes[path] = text.encode()
            index += f"\n- [{identifier} — {issue['code']}: {issue['path']}](tasks/{identifier}.md)\n"
            created.append(path)
            keys.add(key)
        if created:
            changes[folder + "/TASKS.md"] = index.encode()
            atomic_apply(root, changes)
        return created
