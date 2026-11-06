"""Instalação de recursos versionados, preservação e atualização explícita."""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from datetime import date
from importlib.resources import files
from pathlib import Path

from .markdown import render
from .storage import SDDError, atomic_apply, digest, json_bytes, project_lock, read, read_json, safe_path

START = "<!-- SDD:START -->"
END = "<!-- SDD:END -->"
AGENT_BLOCK = f"""{START}
## Fluxo SDD
Se `.sdd/framework/` existir, leia `skill/references/WORKFLOW.md` e
`skill/references/ARTIFACTS.md` dentro dele e use seus templates.
Sem esses recursos, continue pelos documentos e tickets do projeto;
instruções essenciais de execução devem estar neste AGENTS.md.
Consulte CHECKPOINT.md (se existir) ao retomar.
Comece pelas tarefas de `.sdd/adoption/TASKS.md`; depois siga docs/ROADMAP.md
e os tickets em specs/*/tasks/. Execute trabalho autorizado e pronto por
dependência, sem repetir pedidos de autorização. Ações humanas pendentes ficam
no ticket; prossiga com tarefas independentes. Propostas não aceitas vão para
docs/inbox/. Ao pedir pausa ou passagem de contexto, atualize CHECKPOINT.md.
## Continuidade independente
A CLI SDD não é requisito para executar tarefas ou manter os documentos. Leia
os tickets, verifique seus requisitos/dependências e execute os testes do próprio
projeto. Critérios de aceitação, testes e revisões aplicáveis atendidos permitem
concluir sem confirmação manual adicional, salvo ação humana exigida no ticket.
Não declare conclusão com checagens pendentes nem mude requisitos para aceitar código.

Depois de criar ou alterar um ticket, atualize diretamente o acompanhamento no
roadmap indicado pelo projeto (padrão: docs/ROADMAP.md). Leia todos os tickets
em specs/*/tasks/ e os de .sdd/adoption/tasks/ quando existirem. Use os estados
dos tickets; não os deduza da posição no roadmap ou de um resumo anterior.
Preserve entregas, prioridades e conteúdo fora do bloco SDD:PROGRESS. Atualize
ou crie esse bloco usando os marcadores HTML SDD:PROGRESS:START/END. Dentro dele:
- Cabeçalho: Acompanhamento das tarefas; data e contagem de concluídas/total.
- Um grupo por entrega e outro para adequação inicial, quando houver.
- Tabela: Tarefa (link relativo ao ticket), Trabalho, Estado, Execução, Verificação.
- Seção Ações pendentes do usuário: ticket, ação concreta e estado; escrever
  Nenhuma quando não houver. Incluir awaiting_user e trabalho humano ainda aberto.
- Manter bloqueios e ação de desbloqueio nos tickets, sem inventar respostas,
  aprovação humana ou resultado de testes. Tickets são a fonte; roadmap é resumo.
Após criar/alterar tickets, o agente executa `python3 scripts/atualizar_roadmap.py`
na raiz do projeto e confere a saída e o diff. Esse script autônomo pertence ao
consumidor e funciona sem pacote SDD ou .sdd/. Para caminho alternativo,
execute com --roadmap caminho/ROADMAP.md. Preserve customizações do script e não
o substitua automaticamente. Em erro, corrija a causa ou mantenha o resumo pelas
ferramentas habituais, sem declarar atualização que não aconteceu.
Use scripts locais para operações mecânicas definidas; análise de requisitos,
decisões e interpretação das evidências continuam com agente e usuário.
Ferramentas SDD são opcionais para manutenção
expressamente solicitada. Documentos e instruções locais sustentam a continuidade.
{END}"""
CLAUDE_BLOCK = f"{START}\nLeia e siga o AGENTS.md da raiz deste projeto, incluindo o fluxo SDD.\n{END}"


def _collect(resource, prefix="") -> dict[str, bytes]:
    result = {}
    for child in resource.iterdir():
        name = prefix + child.name
        if child.is_dir():
            result.update(_collect(child, name + "/"))
        elif child.is_file():
            result[name] = child.read_bytes()
    return result


def bundle(source: Path | None = None) -> dict[str, bytes]:
    if source is None:
        contents = _collect(files("sdd_framework").joinpath("assets"))
        contents["scripts/atualizar_roadmap.py"] = files("sdd_framework").joinpath("consumer_roadmap.py").read_bytes()
    else:
        source = source.resolve()
        if (source / "src/sdd_framework/assets").is_dir():
            source = source / "src/sdd_framework/assets"
        if not source.is_dir():
            raise SDDError(f"Fonte de atualização inexistente: {source}")
        contents = {}
        for path in source.rglob("*"):
            relative = path.relative_to(source).as_posix()
            safe_path(source, relative)
            if path.is_file():
                contents[relative] = path.read_bytes()
        if "scripts/atualizar_roadmap.py" not in contents:
            helper = safe_path(source.parent, "consumer_roadmap.py")
            if helper.is_file():
                contents["scripts/atualizar_roadmap.py"] = helper.read_bytes()
    try:
        info = json.loads(contents["bundle.json"])
        policy = json.loads(contents["policy.json"])
    except (KeyError, ValueError) as exc:
        raise SDDError("Distribuição inválida: bundle.json/policy.json ausente ou inválido") from exc
    if not isinstance(info, dict) or info.get("schema_version") != 1:
        raise SDDError("Distribuição usa schema incompatível")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", str(info.get("version", ""))):
        raise SDDError("Versão de distribuição inválida")
    if policy != json.loads(_collect(files("sdd_framework").joinpath("assets"))["policy.json"]):
        raise SDDError("Política diferente da suportada por esta CLI; atualize a CLI antes dos recursos")
    required = {"skill/SKILL.md", "skill/references/WORKFLOW.md", "skill/references/ARTIFACTS.md", "integrations/codex/config.toml", "scripts/atualizar_roadmap.py"}
    required.update("templates/" + name for name in ["PRD.md", "ARCHITECTURE.md", "ROADMAP.md", *policy["templates"]])
    if required - contents.keys():
        raise SDDError(f"Distribuição incompleta: {sorted(required - contents.keys())}")
    # O bundle distribui somente arquivos conhecidos; não executa seu conteúdo.
    allowed = required | {"bundle.json", "policy.json"}
    if contents.keys() - allowed:
        raise SDDError(f"Arquivos inesperados na distribuição: {sorted(contents.keys() - allowed)}")
    try:
        for content in contents.values():
            content.decode("utf-8")
    except UnicodeError as exc:
        raise SDDError("Distribuição deve conter somente texto UTF-8") from exc
    return contents


def load_config(root: Path) -> dict:
    config = read_json(root, ".sdd/config.json")
    if config.get("schema_version") != 1:
        raise SDDError("Schema de configuração incompatível")
    policy = json.loads(bundle()["policy.json"])
    for key, allowed in (("mode", ["new", "existing"]), ("agent", ["codex", "claude", "both", "none"]), ("phase", policy["phases"])):
        if config.get(key) not in allowed:
            raise SDDError(f"Configuração inválida em {key}")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", str(config.get("framework_version", ""))):
        raise SDDError("framework_version inválida")
    mapping = config.get("document_paths", {})
    if not isinstance(mapping, dict) or any(k not in policy["project"] for k in mapping):
        raise SDDError("document_paths deve mapear somente documentos canônicos do projeto")
    for value in mapping.values():
        safe_path(root, value)
    if len(set(mapping.get(k, k) for k in policy["project"])) != len(policy["project"]):
        raise SDDError("Documentos distintos não podem mapear para o mesmo arquivo")
    if config.get("interface") is not None and type(config["interface"]) is not bool:
        raise SDDError("interface deve ser booleano ou null")
    system = config.get("design_system")
    if system is not None and (not isinstance(system, dict) or any(not isinstance(system.get(k), str) or not system[k].strip() for k in ("reference", "version"))):
        raise SDDError("design_system requer reference e version preenchidos")
    return config


def managed_section(text: str) -> str | None:
    if START not in text and END not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
        raise SDDError("Bloco SDD malformado; corrija os marcadores antes de continuar")
    return text[text.index(START):text.index(END) + len(END)]


def integrate(text: str, block: str, expected: str | None) -> str:
    current = managed_section(text)
    if current is not None:
        if expected is None or digest(current.encode()) != expected:
            raise SDDError("Bloco SDD existente não reconhecido ou editado; preserve-o e reconcilie manualmente")
        return text.replace(current, block, 1)
    if expected is not None:
        raise SDDError("Bloco SDD removido; não será recriado silenciosamente")
    return text + ("\n\n" if text and not text.endswith("\n\n") else "") + block + "\n"


ADOPTION = [
    ("Inventariar e integrar o projeto", "discovery", "Identificar problema, público, código, testes e documentos existentes. Registrar equivalências e conflitos sem sobrescrever conteúdo útil.", "Inventário descrito no PRD ou nos tickets; modo new/existing confirmado e conflitos identificados."),
    ("Consolidar README e PRD", "requirements", "Preencher README e docs/PRD.md com os templates; levantar requisitos e obter aceite de decisões relevantes.", "README e PRD completos, requisitos claros e revisão semântica registrada."),
    ("Definir arquitetura e instruções do projeto", "architecture", "Preencher docs/ARCHITECTURE.md, comandos reais no AGENTS.md e decisões técnicas. Perguntar sobre interface e Design System existente.", "Tecnologias, restrições, componentes e comandos verificáveis definidos, sem decisão bloqueante em aberto."),
    ("Organizar roadmap", "planning", "Preencher docs/ROADMAP.md com entregas e dependências; alinhar prioridades.", "Prioridades e dependências revisadas; orientação local para acompanhar tarefas sem CLI."),
    ("Especificar a primeira entrega", "specification", "Criar specs/NNN-nome/SPEC.md com requisitos, critérios de aceitação e design inline ou separado, conforme complexidade.", "SPEC aceita, requisitos verificáveis e design coerente com arquitetura e referência de interface disponível."),
    ("Preparar tickets e transferência", "tasks", "Criar TASKS.md e tickets individuais com requisitos, autorização, executor, dependências e verificação; revisar consistência e autonomia do projeto.", "Todo requisito coberto, tickets verificáveis e instruções suficientes para executar e manter documentos sem framework instalado ou contexto da sessão anterior."),
]


def adoption_files(contents: dict[str, bytes], project: str) -> dict[str, bytes]:
    output = {}
    lines = ["# Adequação inicial ao SDD", "", "## Índice", ""]
    template = contents["templates/TASK.md"].decode()
    for i, (title, phase, scope, acceptance) in enumerate(ADOPTION, 1):
        identifier = f"T-{i:03}"
        relative = f".sdd/adoption/tasks/{identifier}.md"
        text = render(template, task_id=identifier, title=title)
        text = text.replace("authorization: pending", "authorization: approved").replace('requirements: ["RF-001"]', "requirements: []")
        if i == 1:
            text = text.replace("status: pending", "status: ready")
        if i > 1:
            text = text.replace("dependencies: []", f'dependencies: [".sdd/adoption/tasks/T-{i-1:03}.md"]')
        replacements = {
            "[PREENCHER: resultado limitado, referenciando a SPEC.]": f"Adequar {project} à etapa {phase} do SDD.",
            "[PREENCHER: trabalho incluído, exclusões e documentos a manter.]": scope + " A autorização inicial cobre organização; decisões relevantes ainda exigem aceite do usuário.",
            "[PREENCHER: resultados verificáveis desta tarefa.]": acceptance,
            "[PREENCHER: testes, revisão, comandos e evidências necessárias; não afirmar sucesso antes de executar.]": "Conferir arquivos e critérios da etapa, registrar evidências e revisar decisões relevantes. A CLI SDD pode auxiliar uma conferência explícita, mas não é pré-requisito para avançar.",
            "[PREENCHER: parte do agente e parte do usuário, se houver.]": "Agente prepara e verifica documentos. Usuário esclarece objetivos e aceita decisões relevantes. Ao depender de resposta, registrar ação e marcar awaiting_user.",
        }
        for before, after in replacements.items():
            text = text.replace(before, after)
        output[relative] = text.encode()
        lines.append(f"- [{identifier} — {title}](tasks/{identifier}.md)")
    lines.extend(["", "## Ordem e acompanhamento", "", "Seguir dependências; estados ficam nos tickets. O agente mantém diretamente no roadmap a visão de tarefas e ações humanas, conforme AGENTS.md, sem depender da CLI.", ""])
    output[".sdd/adoption/TASKS.md"] = "\n".join(lines).encode()
    return output


def _install(root: Path, config: dict, contents: dict[str, bytes], initial: bool) -> dict:
    info = json.loads(contents["bundle.json"])
    manifest = {"schema_version": 1, "files": {}, "blocks": {}} if initial else read_json(root, ".sdd/manifest.json")
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), dict) or not isinstance(manifest.get("blocks"), dict):
        raise SDDError("Manifesto inválido ou incompatível")
    if not initial:
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", str(manifest.get("version", ""))):
            raise SDDError("Versão inválida no manifesto")
        current_version = tuple(int(x) for x in str(manifest.get("version", "0.0.0")).split("-", 1)[0].split("+", 1)[0].split("."))
        next_version = tuple(int(x) for x in info["version"].split("-", 1)[0].split("+", 1)[0].split("."))
        if next_version < current_version:
            raise SDDError("Downgrade de recursos recusado; use uma distribuição igual ou mais recente")
    desired = {f".sdd/framework/{name}": content for name, content in contents.items()}
    for agent, directory in (("codex", ".agents"), ("claude", ".claude")):
        if config["agent"] in (agent, "both"):
            for name, content in contents.items():
                if name.startswith("skill/"):
                    desired[f"{directory}/skills/sdd/{name.removeprefix('skill/')}"] = content
    # Verificar todos os arquivos antes de qualquer mutação.
    changes = {}
    hashes = dict(manifest["files"])
    for relative, content in desired.items():
        current = read(root, relative)
        expected = manifest["files"].get(relative)
        if current is not None and (expected is None or digest(current.encode()) != expected):
            raise SDDError(f"Conflito em {relative}; conteúdo local preservado. Reconcilie antes do update.")
        if current is None and expected is not None:
            raise SDDError(f"Recurso administrado removido: {relative}; reconcilie antes do update")
        changes[relative] = content
        hashes[relative] = digest(content)
    blocks = dict(manifest["blocks"])
    targets = {"AGENTS.md": AGENT_BLOCK}
    if config["agent"] in ("claude", "both"):
        targets["CLAUDE.md"] = CLAUDE_BLOCK
    for relative, block in targets.items():
        current = read(root, relative) or ""
        changes[relative] = integrate(current, block, blocks.get(relative)).encode()
        blocks[relative] = digest(block.encode())
    # Configuração nativa pertence ao consumidor: criar somente se ausente,
    # sem registrá-la como recurso que updates possam substituir.
    if config["agent"] in ("codex", "both") and read(root, ".codex/config.toml") is None:
        changes[".codex/config.toml"] = contents["integrations/codex/config.toml"]
    # Ferramenta autônoma pertence ao consumidor; preservar versão/customizações.
    if read(root, "scripts/atualizar_roadmap.py") is None:
        changes["scripts/atualizar_roadmap.py"] = contents["scripts/atualizar_roadmap.py"]
    if initial:
        for relative, content in adoption_files(contents, root.name).items():
            if read(root, relative) is not None:
                raise SDDError(f"Plano de adoção já existe: {relative}")
            changes[relative] = content
    config = dict(config, framework_version=info["version"])
    changes[".sdd/config.json"] = json_bytes(config)
    changes[".sdd/manifest.json"] = json_bytes({"schema_version": 1, "version": info["version"], "files": hashes, "blocks": blocks})
    modified = [name for name, content in changes.items() if read(root, name) != content.decode()]
    atomic_apply(root, changes, ("docs/inbox", "docs/decisions", "specs"))
    return {"version": info["version"], "changed": modified, "mode": config["mode"], "agent": config["agent"]}


def initialize(root: Path, agent: str = "both", mode: str = "auto") -> dict:
    root.mkdir(parents=True, exist_ok=True)
    with project_lock(root):
        if read(root, ".sdd/config.json") is not None:
            config = load_config(root)
            return {"version": config["framework_version"], "changed": [], "mode": config["mode"], "agent": config["agent"], "already_initialized": True}
        if mode == "auto":
            mode = "existing" if any(p.name not in (".git", ".sdd", ".agents", ".claude", ".codex") for p in root.iterdir()) else "new"
        config = {"schema_version": 1, "framework_version": "0.1.0", "mode": mode, "agent": agent, "phase": "discovery", "document_paths": {}, "interface": None, "design_system": None, "update_source": None}
        return _install(root, config, bundle(), True)


def update(root: Path, source: Path | None = None, repository: str | None = None, ref: str | None = None) -> dict:
    with project_lock(root):
        config = load_config(root)
        previous_source = config.get("update_source")
        if source is None and repository is None and previous_source:
            if not isinstance(previous_source, dict):
                raise SDDError("update_source inválido")
            repository, ref = previous_source.get("repository"), previous_source.get("ref")
        if repository is not None:
            if not isinstance(repository, str) or not re.fullmatch(r"https://[A-Za-z0-9][A-Za-z0-9._/-]*", repository) or not isinstance(ref, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", ref):
                raise SDDError("Atualização remota exige repositório HTTPS sem credenciais e --ref explícita")
            with tempfile.TemporaryDirectory(prefix="sdd-update-") as directory:
                checkout = Path(directory) / "source"
                try:
                    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "clone", "--depth", "1", "--branch", ref, "--", repository, str(checkout)], check=True, capture_output=True, text=True, timeout=60)
                except (OSError, subprocess.SubprocessError) as exc:
                    raise SDDError("Falha ao obter distribuição Git; verifique URL, ref e acesso à rede. Nenhum recurso foi atualizado.") from exc
                contents = bundle(checkout)
                config["update_source"] = {"repository": repository, "ref": ref}
                result = _install(root, config, contents, False)
        else:
            result = _install(root, config, bundle(source), False)
        result["source"] = str(source) if source else repository or "installed"
        result["note"] = "Recursos atualizados; documentos do consumidor preservados. Execute conferência. Sem fonte remota configurada, update usa a distribuição local e não consulta novas versões online."
        return result
