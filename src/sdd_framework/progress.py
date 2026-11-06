"""Adaptador opcional da CLI para o atualizador autônomo do consumidor."""
from pathlib import Path

from .consumer_roadmap import EXECUTORS, STATES, START, END, groups, human_tasks, render_progress, replace_block
from .project import load_config
from .storage import SDDError, atomic_apply, project_lock, read


def update_roadmap(root: Path, report: dict) -> str:
    with project_lock(root):
        config = load_config(root)
        path = config.get("document_paths", {}).get("docs/ROADMAP.md", "docs/ROADMAP.md")
        text = read(root, path)
        if text is None:
            raise SDDError("Roadmap ausente; preencha o documento antes de gerar o acompanhamento")
        try:
            text = replace_block(text, render_progress(report, path))
        except ValueError as exc:
            raise SDDError(str(exc)) from exc
        atomic_apply(root, {path: text.encode()})
        return path
