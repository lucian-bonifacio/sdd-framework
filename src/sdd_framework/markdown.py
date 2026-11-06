"""Contrato Markdown com subconjunto explícito de YAML, sem dependências."""
from __future__ import annotations

import json
import re

from .storage import SDDError

PLACEHOLDER = re.compile(r"\[PREENCHER\b|\{\{[^}]+\}\}|\bNEEDS CLARIFICATION\b", re.I)


def metadata(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise SDDError("Frontmatter ausente")
    result = {}
    for line in lines[1:]:
        if line == "---":
            return result
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):\s*(.*)", line)
        if not match:
            raise SDDError(f"Metadado fora do formato suportado: {line}")
        key, raw = match.groups()
        if key in result:
            raise SDDError(f"Metadado duplicado: {key}")
        if raw.startswith(("[", '"')) or raw in ("true", "false", "null"):
            try:
                value = json.loads(raw)
            except ValueError as exc:
                raise SDDError(f"Valor inválido em {key}; listas e aspas devem usar JSON") from exc
        elif raw.startswith("'") and raw.endswith("'"):
            value = raw[1:-1].replace("''", "'")
        elif not raw or raw.startswith(("{", "|", ">", "&", "*")) or " #" in raw:
            raise SDDError(f"Valor inválido em {key}; use escalar ou lista JSON")
        else:
            value = raw
        if not isinstance(value, (str, bool, list)) and value is not None:
            raise SDDError(f"Tipo não suportado em {key}")
        if isinstance(value, list) and any(not isinstance(x, str) for x in value):
            raise SDDError(f"A lista {key} aceita somente strings")
        result[key] = value
    raise SDDError("Frontmatter sem fechamento")


def sections(text: str) -> dict[str, str]:
    result: dict[str, list[str]] = {}
    active = None
    fenced = False
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        if line.startswith("## ") and not fenced:
            active = line[3:].strip()
            result.setdefault(active, [])
        elif active is not None:
            result[active].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def render(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template
