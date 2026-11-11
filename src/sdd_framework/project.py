"""Instalar e atualizar instruções. O usuário aciona o governador na IA."""
from __future__ import annotations

import json
import re
from importlib.resources import files
from pathlib import Path

from .changes import compare, log_section, validate
from .execution import EXECUTION, installed_hash, operation, refresh, snapshots, validate_state
from .storage import SDDError, atomic_apply, digest, json_bytes, project_lock, read, read_json, safe_path

START, END = "<!-- SDD:START -->", "<!-- SDD:END -->"
GOVERNOR = "docs/governador.md"
GOVERNOR_TEMPLATE = "governador.md"
LEGACY_GOVERNOR = "governador.md"
GOV_START, GOV_END = "<!-- SDD:GOVERNADOR:START -->", "<!-- SDD:GOVERNADOR:END -->"
OLD_FLOW = "docs/FLUXO.md"
OLD_START, OLD_END = "<!-- SDD:FLOW:START -->", "<!-- SDD:FLOW:END -->"
MANIFEST = ".sdd/manifest.json"
TEMPLATES = ("README", "AGENTS", "PRD", "ARCHITECTURE", "ROADMAP", "SPEC", "DESIGN", "TASK", "ADR", "INBOX", "CHECKPOINT", "VALIDATION")
REQUIRED = {"bundle.json", GOVERNOR_TEMPLATE, "standards/CONTRATOS.md", "skill/SKILL.md", "skill/agents/openai.yaml", "integrations/codex/config.toml"}
REQUIRED.update(f"templates/{name}.md" for name in TEMPLATES)
AGENT_BLOCK = f"""{START}
Execute docs/governador.md somente quando o usuário solicitar expressamente o
governador SDD ou invocar a skill SDD. Ler arquivos, abrir uma sessão e executar
init/update não acionam o governador. Fora dessa execução, trabalhe nas tarefas
autorizadas do projeto e mantenha seus documentos atualizados.
{END}"""
CLAUDE_BLOCK = f"""{START}
Leia AGENTS.md para as instruções deste projeto. Execute docs/governador.md
somente por pedido explícito do usuário ou invocação de /sdd. Não iniciar
organização documental automaticamente ao abrir uma sessão ou receber update.
{END}"""
LEGACY_BLOCK = f"""{OLD_START}
## Procedimento anterior desativado
O procedimento vigente está em docs/governador.md e só é executado por acionamento
explícito do usuário. O conteúdo próprio abaixo foi preservado para migração
pelo agente durante esse acionamento. Não executar o fluxo anterior.
{OLD_END}"""


def _version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise SDDError("Versão inválida; esperado major.minor.patch")
    return tuple(map(int, value.split(".")))


def _collect(resource, prefix="") -> dict[str, bytes]:
    contents = {}
    for child in resource.iterdir():
        name = prefix + child.name
        if getattr(child, "is_symlink", lambda: False)():
            raise SDDError(f"Link simbólico na distribuição: {name}")
        if child.is_dir():
            contents.update(_collect(child, name + "/"))
        elif child.is_file():
            contents[name] = child.read_bytes()
    return contents


def bundle(source: Path | None = None) -> dict[str, bytes]:
    if source is None:
        contents = _collect(files("sdd_framework").joinpath("assets"))
    else:
        source = source.resolve()
        if (source / "src/sdd_framework/assets").is_dir():
            source = source / "src/sdd_framework/assets"
        if not source.is_dir():
            raise SDDError(f"Fonte local inexistente: {source}")
        contents = _collect(source)
    if REQUIRED != contents.keys():
        raise SDDError(f"Distribuição incompatível; ausentes: {sorted(REQUIRED - contents.keys())}; extras: {sorted(contents.keys() - REQUIRED)}")
    try:
        info = json.loads(contents["bundle.json"])
        if not isinstance(info, dict) or info.get("schema_version") != 2:
            raise SDDError("Distribuição exige formato 2")
        _version(info.get("version"))
        for data in contents.values():
            data.decode("utf-8")
        managed_section(contents[GOVERNOR_TEMPLATE].decode(), GOV_START, GOV_END, required=True)
        if log_section(contents[GOVERNOR_TEMPLATE].decode()) is not None:
            raise SDDError("O registro de atualizações é gerado no consumidor, não na fonte")
        validate(managed_section(contents[GOVERNOR_TEMPLATE].decode(), GOV_START, GOV_END, required=True), {name: data.decode() for name, data in _resources(contents).items()})
    except (ValueError, UnicodeError) as exc:
        raise SDDError(f"Distribuição inválida: {exc}") from exc
    return contents


def managed_section(text: str, start=START, end=END, *, required=False) -> str | None:
    if start not in text and end not in text:
        if required:
            raise SDDError("Trecho administrado ausente")
        return None
    if text.count(start) != 1 or text.count(end) != 1 or text.index(end) < text.index(start):
        raise SDDError("Marcadores SDD malformados ou duplicados")
    return text[text.index(start):text.index(end) + len(end)]


def integrate(current: str | None, block: str, expected: str | None, start=START, end=END) -> str:
    if current is None:
        if expected is not None:
            raise SDDError("Documento administrado ausente; restaurar antes de atualizar")
        return block + "\n"
    previous = managed_section(current, start, end)
    if previous is None:
        if expected is not None:
            raise SDDError("Trecho administrado removido; reconciliar antes de atualizar")
        return current + ("" if current.endswith("\n\n") else "\n" if current.endswith("\n") else "\n\n") + block + "\n"
    if (expected is None and previous != block) or (expected is not None and digest(previous.encode()) != expected):
        raise SDDError("Trecho administrado modificado; conteúdo preservado. Reconciliar nas fontes antes de atualizar")
    return current.replace(previous, block, 1)


def _managed_file(name: str, legacy: bool) -> bool:
    return (name.startswith("docs/padroes/") or
            name.startswith((".agents/skills/sdd/", ".claude/skills/sdd/")) or
            (legacy and name.startswith(".sdd/framework/")))


def _manifest(root: Path) -> dict | None:
    if read(root, MANIFEST) is None:
        return None
    result = read_json(root, MANIFEST)
    if result.get("schema_version") not in (1, 2):
        raise SDDError("Manifesto de instalação incompatível")
    _version(result.get("version"))
    for field in ("updates_hash", "execution_hash"):
        if result.get(field) is not None and not re.fullmatch(r"[0-9a-f]{64}", str(result[field])):
            raise SDDError("Hash do controle de atualizações inválido")
    for field in ("files", "blocks"):
        if not isinstance(result.get(field), dict):
            raise SDDError(f"Manifesto inválido: {field}")
        for name, value in result[field].items():
            safe_path(root, name)
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise SDDError("Hash inválido no manifesto")
            if field == "files" and not _managed_file(name, result["schema_version"] == 1):
                raise SDDError(f"Manifesto não pode administrar documento do projeto: {name}")
            if field == "blocks" and name not in ("AGENTS.md", "CLAUDE.md", GOVERNOR, LEGACY_GOVERNOR, OLD_FLOW):
                raise SDDError(f"Bloco não permitido no manifesto: {name}")
    return result


def _resources(contents: dict[str, bytes]) -> dict[str, bytes]:
    resources = {f"docs/padroes/{name}.md": contents[f"templates/{name}.md"] for name in TEMPLATES}
    resources["docs/padroes/CONTRATOS.md"] = contents["standards/CONTRATOS.md"]
    resources[".agents/skills/sdd/SKILL.md"] = contents["skill/SKILL.md"]
    resources[".agents/skills/sdd/agents/openai.yaml"] = contents["skill/agents/openai.yaml"]
    skill = contents["skill/SKILL.md"]
    newline = b"\r\n" if b"\r\n" in skill else b"\n"
    resources[".claude/skills/sdd/SKILL.md"] = skill.replace(
        b"name: sdd" + newline, b"name: sdd" + newline + b"disable-model-invocation: true" + newline, 1)
    return resources


def _install(root: Path, contents: dict[str, bytes], previous: dict | None) -> dict:
    info = json.loads(contents["bundle.json"])
    version = info["version"]
    old_files = previous["files"] if previous else {}
    old_blocks = previous["blocks"] if previous else {}
    if previous and _version(version) < _version(previous["version"]):
        raise SDDError("Downgrade de recursos recusado")
    # Conferir todos os conflitos antes de qualquer escrita ou remoção.
    for name, expected in old_files.items():
        content = read(root, name)
        if content is None or digest(content.encode()) != expected:
            raise SDDError(f"Recurso administrado modificado/ausente: {name}; nenhuma alteração aplicada")
    changes, blocks = {}, {}
    resources = _resources(contents)
    for name, data in resources.items():
        current = read(root, name)
        if name not in old_files and current is not None and current.encode() != data:
            raise SDDError(f"Arquivo local conflitante: {name}; conteúdo preservado")
        changes[name] = data
    for name, block in (("AGENTS.md", AGENT_BLOCK), ("CLAUDE.md", CLAUDE_BLOCK)):
        try:
            changes[name] = integrate(read(root, name), block, old_blocks.get(name)).encode()
        except SDDError as exc:
            raise SDDError(f"{name}: {exc}") from exc
        blocks[name] = digest(block.encode())
    template = contents[GOVERNOR_TEMPLATE].decode().replace("{{version}}", version)
    desired = managed_section(template, GOV_START, GOV_END, required=True)
    current = read(root, GOVERNOR)
    migrating_governor = LEGACY_GOVERNOR != GOVERNOR and LEGACY_GOVERNOR in old_blocks
    if migrating_governor:
        if GOVERNOR in old_blocks or current is not None:
            raise SDDError(f"Destino da migração já ocupado: {GOVERNOR}; conteúdo preservado")
        current = read(root, LEGACY_GOVERNOR)
        changes[GOVERNOR] = integrate(current, desired, old_blocks[LEGACY_GOVERNOR], GOV_START, GOV_END).encode()
    elif current is None and GOVERNOR not in old_blocks:
        changes[GOVERNOR] = template.encode()
    else:
        if GOVERNOR not in old_blocks and current != template:
            raise SDDError(f"{GOVERNOR} já existe sem procedência; conteúdo preservado")
        changes[GOVERNOR] = integrate(current, desired, old_blocks.get(GOVERNOR), GOV_START, GOV_END).encode()
    blocks[GOVERNOR] = digest(desired.encode())
    old_resources = {name: read(root, name) or "" for name in old_files if not name.startswith(".sdd/framework/")}
    new_resources = {name: data.decode() for name, data in resources.items()}
    old_procedure = managed_section(current, GOV_START, GOV_END) if current else None
    item_changes = compare(old_procedure, desired, old_resources, new_resources) if previous else []
    legacy = log_section(current) if current else None
    expected_legacy = (previous or {}).get("updates_hash")
    if legacy is not None and (expected_legacy is None or digest(legacy.encode()) != expected_legacy):
        raise SDDError("Registro anterior modificado; conteúdo preservado")
    if legacy is None and expected_legacy is not None:
        raise SDDError("Registro anterior ausente; restaurar antes do update")
    state_text = read(root, EXECUTION)
    expected_state = (previous or {}).get("execution_hash")
    if expected_state is not None:
        if state_text is None:
            raise SDDError("Controle de execução ausente; restaurar antes do update")
        state = read_json(root, EXECUTION)
        validate_state(state, expected_state)
    else:
        if state_text is not None:
            raise SDDError("Controle de execução sem procedência; conteúdo preservado")
        state = None
    state = refresh(state, snapshots(desired, new_resources), version,
                    previous=snapshots(old_procedure, old_resources) if previous else None,
                    legacy=legacy)
    changes[EXECUTION] = json_bytes(state)
    if legacy is not None:
        changes[GOVERNOR] = changes[GOVERNOR].decode().replace(legacy, "", 1).encode()
    # Na migração, desativar só o procedimento antigo; preservar o plano do usuário.
    if OLD_FLOW in old_blocks and read(root, OLD_FLOW) is not None:
        changes[OLD_FLOW] = integrate(read(root, OLD_FLOW), LEGACY_BLOCK, old_blocks[OLD_FLOW], OLD_START, OLD_END).encode()
        blocks[OLD_FLOW] = digest(LEGACY_BLOCK.encode())
    if read(root, ".codex/config.toml") is None:
        changes[".codex/config.toml"] = contents["integrations/codex/config.toml"]
    manifest = {"schema_version": 2, "version": version, "files": {name: digest(data) for name, data in resources.items()}, "blocks": blocks}
    manifest["execution_hash"] = installed_hash(state)
    changes[MANIFEST] = json_bytes(manifest)
    removals = tuple(sorted((set(old_files) - resources.keys()) |
                            ({LEGACY_GOVERNOR} if migrating_governor else set())))
    changed = [name for name, data in changes.items() if read(root, name) != data.decode()]
    atomic_apply(root, changes, removals=removals)
    return {"version": version, "changed": changed, "removed": list(removals), "governor_executed": False,
            "governor_changes": item_changes,
            "operations": {key: operation(item) for key, item in state["items"].items()},
            "note": "Recursos instalados. O governador NÃO foi executado. Referências e pendências por item estão em .sdd/execucao.json. Na próxima invocação explícita, a skill informa as mudanças e trata somente operações afetadas."}


def initialize(root: Path) -> dict:
    contents = bundle()
    root.mkdir(parents=True, exist_ok=True)
    with project_lock(root):
        previous = _manifest(root)
        if previous is not None:
            return {"version": previous["version"], "changed": [], "removed": [], "already_initialized": True,
                    "governor_executed": False, "note": "Instalação já existe. Use update para atualizar recursos; acione docs/governador.md explicitamente na IA."}
        return _install(root, contents, None)


def update(root: Path, source: Path | None = None) -> dict:
    contents = bundle(source)
    if not root.is_dir():
        raise SDDError("Projeto inexistente; execute init primeiro")
    with project_lock(root):
        previous = _manifest(root)
        if previous is None:
            raise SDDError("Instalação ausente; execute init primeiro")
        return _install(root, contents, previous)
