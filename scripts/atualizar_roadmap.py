"""Atualizar o roadmap a partir de tickets; autônomo, somente biblioteca padrão."""
from __future__ import annotations

import html
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import argparse
import json
import sys
import tempfile

START = "<!-- SDD:PROGRESS:START -->"
END = "<!-- SDD:PROGRESS:END -->"
STATES = {"pending": "Pendente", "ready": "Pronta", "in_progress": "Em andamento", "awaiting_user": "Aguardando usuário", "blocked": "Bloqueada", "done": "Concluída", "cancelled": "Cancelada"}
EXECUTORS = {"agent": "Agente", "user": "Usuário", "joint": "Conjunta"}
EMPTY_ACTIONS = {"", "nenhuma", "nenhuma.", "não se aplica", "não se aplica."}


def groups(report: dict) -> dict[str, list[dict]]:
    result = defaultdict(list)
    for task in sorted(report["tasks"], key=lambda t: t["path"]):
        result[task["path"].split("/tasks/", 1)[0]].append(task)
    return dict(result)


def human_tasks(report: dict) -> list[dict]:
    return [task for task in report["tasks"] if task.get("status") not in ("done", "cancelled") and (task.get("status") == "awaiting_user" or task.get("executor") == "user" or str(task.get("human_action", "")).strip().lower() not in EMPTY_ACTIONS)]


def escape(value: object) -> str:
    text = html.escape(str(value), quote=False).replace("\n", " ").replace("\r", " ")
    return re.sub(r"([\\|\[\]`*_])", r"\\\1", text)


def task_link(task: dict, roadmap: str) -> str:
    relative = os.path.relpath(task["path"], str(Path(roadmap).parent)).replace(os.sep, "/")
    return f"[{escape(task.get('id', Path(task['path']).stem))}]({quote(relative, safe='/._-')})"


def render_progress(report: dict, roadmap: str) -> str:
    total = len(report["tasks"])
    lines = [START, "## Acompanhamento das tarefas", "", "Visão derivada dos tickets, mantida pelo agente conforme AGENTS.md. Edite estados nos tickets e atualize este resumo; atualize com o script local indicado em AGENTS.md.", "", f"Atualizado em: {datetime.now(timezone.utc).isoformat(timespec='seconds')}.", "", f"**{report['counts']['done']}/{total} tarefas concluídas.** Canceladas: {report['counts']['cancelled']}. O resumo não substitui as evidências dos tickets."]
    for group, tasks in groups(report).items():
        label = "Adequação inicial ao SDD" if group == ".sdd/adoption" else group.removeprefix("specs/")
        lines.extend(["", f"### {escape(label)}", "", "| Tarefa | Trabalho | Estado | Execução | Verificação |", "|---|---|---|---|---|"])
        for task in tasks:
            title = re.sub(r"^T-\d+\s*[—-]\s*", "", str(task.get("title", "")))
            lines.append(f"| {task_link(task, roadmap)} | {escape(title)} | {escape(STATES.get(task.get('status'), 'Inválido'))} | {escape(EXECUTORS.get(task.get('executor'), 'Inválida'))} | {escape(task.get('verification', 'not_verified'))} |")
    lines.extend(["", "### Ações pendentes do usuário", ""])
    pending = human_tasks(report)
    if not pending:
        lines.append("Nenhuma ação humana pendente registrada nos tickets.")
    else:
        lines.extend(["| Tarefa | Ação necessária | Estado |", "|---|---|---|"])
        for task in pending:
            action = task.get("human_action", "")
            if str(action).strip().lower() in EMPTY_ACTIONS:
                action = "Consultar responsabilidades e critérios de aceitação no ticket."
            lines.append(f"| {task_link(task, roadmap)} | {escape(action)} | {escape(STATES.get(task.get('status'), 'Inválido'))} |")
    lines.extend(["", END])
    return "\n".join(lines)


def safe_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if not relative or "\\" in relative or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Caminho fora do projeto: {relative}")
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"Link simbólico não permitido: {relative}")
    return current


def metadata(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Ticket sem metadados")
    result = {}
    for line in lines[1:]:
        if line == "---":
            return result
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):\s*(.+)", line)
        if not match or match[1] in result:
            raise ValueError(f"Metadado inválido ou duplicado: {line}")
        key, raw = match.groups()
        if raw.startswith(('[', '"')):
            value = json.loads(raw)
        elif raw.startswith("'") and raw.endswith("'"):
            value = raw[1:-1].replace("''", "'")
        else:
            value = raw
        result[key] = value
    raise ValueError("Metadados sem fechamento")


def human_action(text: str) -> str:
    active, fenced, lines = False, False, []
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        if line.startswith("## ") and not fenced:
            active = line[3:].strip() == "Ação humana pendente"
        elif active:
            lines.append(line)
    return "\n".join(lines).strip()


def collect(root: Path) -> dict:
    tasks = []
    for directory in ("specs", ".sdd/adoption/tasks"):
        base = safe_path(root, directory)
        if not base.exists():
            continue
        if not base.is_dir():
            raise ValueError(f"Esperado diretório: {directory}")
        for current, directories, names in os.walk(base, followlinks=False):
            for name in directories + names:
                safe_path(root, (Path(current) / name).relative_to(root).as_posix())
            for name in sorted(names):
                file = Path(current) / name
                relative = file.relative_to(root).as_posix()
                if not name.endswith(".md") or (directory == "specs" and "/tasks/" not in relative):
                    continue
                text = file.read_bytes().decode("utf-8")
                try:
                    meta = metadata(text)
                    if meta.get("id") != file.stem:
                        raise ValueError("ID difere do nome do arquivo")
                    for field, values in (("status", STATES), ("executor", EXECUTORS), ("verification", ("passed", "failed", "not_verified", "not_applicable"))):
                        if meta.get(field) not in values:
                            raise ValueError(f"Campo inválido: {field}")
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"{relative}: {exc}") from exc
                title = next((line[2:] for line in text.splitlines() if line.startswith("# ")), file.stem)
                tasks.append({**meta, "path": relative, "title": title, "human_action": human_action(text)})
    return {"tasks": tasks, "counts": {state: sum(task["status"] == state for task in tasks) for state in STATES}}


def replace_block(text: str, block: str) -> str:
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
            raise ValueError("Marcadores de acompanhamento malformados; roadmap preservado")
        begin, end = text.index(START), text.index(END) + len(END)
        return text[:begin] + block + text[end:]
    return text + ("\n" if text.endswith("\n") else "\n\n") + block + "\n"


def update(root: Path, roadmap: str | None = None) -> str:
    # Configuração SDD é somente dado opcional. Não importa nenhum pacote SDD.
    if roadmap is None:
        config_path = safe_path(root, ".sdd/config.json")
        config = json.loads(config_path.read_bytes()) if config_path.is_file() else {}
        if not isinstance(config, dict):
            raise ValueError("Configuração deve ser um objeto JSON")
        mapping = config.get("document_paths", {})
        if not isinstance(mapping, dict):
            raise ValueError("document_paths deve ser objeto JSON")
        roadmap = mapping.get("docs/ROADMAP.md", "docs/ROADMAP.md")
    if not isinstance(roadmap, str):
        raise ValueError("Caminho do roadmap deve ser texto")
    path = safe_path(root, roadmap)
    if not path.is_file():
        raise ValueError("Roadmap ausente; preencher o documento antes de atualizar o acompanhamento")
    lock = safe_path(root, roadmap + ".lock")
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError as exc:
        raise ValueError("Roadmap em uso ou lock residual; inspecione antes de remover") from exc
    temporary = None
    try:
        with handle:
            handle.write(str(os.getpid()))
        report = collect(root)
        text = path.read_bytes().decode("utf-8")
        updated = replace_block(text, render_progress(report, roadmap))
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".roadmap-", delete=False) as output:
            temporary = Path(output.name)
            output.write(updated.encode("utf-8"))
        temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
        return roadmap
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        lock.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Raiz do consumidor; padrão: pasta acima de scripts/")
    parser.add_argument("--roadmap", help="Caminho relativo à raiz; padrão: docs/ROADMAP.md ou equivalência local")
    args = parser.parse_args(argv)
    try:
        print(f"Roadmap atualizado: {update(args.root.resolve(), args.roadmap)}")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

