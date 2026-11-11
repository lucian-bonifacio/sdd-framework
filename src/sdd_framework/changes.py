"""Diferenças verificáveis por item; sem executar ou aprovar trabalho da IA."""
from __future__ import annotations

import difflib
import json
import re
import unicodedata

from .storage import SDDError

LOG_START, LOG_END = "<!-- SDD:UPDATES:START -->", "<!-- SDD:UPDATES:END -->"
ITEM = re.compile(r"^<!-- SDD:ITEM:([a-z][a-z0-9-]*):START -->\n(.*?)^<!-- SDD:ITEM:\1:END -->[ \t]*$", re.M | re.S)
USES = re.compile(r"^<!-- SDD:USES:(.*?) -->[ \t]*$", re.M)
LEGACY_IDS = {"prd": "prd", "specs": "specs", "arquitetura-e-design": "arquitetura", "tasks": "tasks", "roadmap": "roadmap", "agents-e-readme": "agents", "encerramento-e-continuidade": "encerramento"}


def log_section(text: str) -> str | None:
    starts = list(re.finditer(r"^" + re.escape(LOG_START) + r"[ \t]*(?=\r?$)", text, re.M))
    ends = list(re.finditer(r"^" + re.escape(LOG_END) + r"[ \t]*(?=\r?$)", text, re.M))
    if not starts and not ends:
        return None
    if len(starts) != 1 or len(ends) != 1 or ends[0].start() < starts[0].end():
        raise SDDError("Marcadores do registro de atualizações malformados")
    return text[starts[0].start():ends[0].end()]



def slug(value: str) -> str:
    value = "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", value)).strip("-")


def _part(text: str, title: str) -> dict:
    matches = USES.findall(text)
    if len(matches) > 1:
        raise SDDError(f"Dependências duplicadas no item {title}")
    try:
        uses = json.loads(matches[0]) if matches else []
    except ValueError as exc:
        raise SDDError(f"Dependências inválidas no item {title}") from exc
    if not isinstance(uses, list) or any(not isinstance(ref, str) for ref in uses):
        raise SDDError(f"Dependências devem ser lista de caminhos: {title}")
    body = USES.sub("", text).strip()
    body = re.sub(r"(?m)^## \d+\. ", "## ", body)
    body = re.sub(r"(?m)^Versão do procedimento: \S+\s*", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return {"title": title, "text": body, "uses": uses, "bound": bool(matches)}


def sections(block: str | None) -> tuple[dict, dict]:
    if block is None:
        return {}, _part("", "Orientações comuns")
    text = block.replace("\r\n", "\n")
    text = re.sub(r"^<!-- SDD:GOVERNADOR:(?:START|END) -->\s*$", "", text, flags=re.M)
    matches = list(ITEM.finditer(text))
    items = {}
    if "<!-- SDD:ITEM:" in text:
        if len(re.findall(r"^<!-- SDD:ITEM:.*?:(?:START|END) -->", text, re.M)) != 2 * len(matches):
            raise SDDError("Marcadores de itens malformados ou aninhados")
        common, last = [], 0
        for match in matches:
            identifier, body = match.groups()
            if identifier in items:
                raise SDDError(f"ID de item duplicado: {identifier}")
            heading = re.search(r"^## (?:\d+\. )?(.+)$", body, re.M)
            if not heading:
                raise SDDError(f"Título ausente no item {identifier}")
            items[identifier] = _part(body, heading[1])
            common.append(text[last:match.start()])
            last = match.end()
        common.append(text[last:])
        return items, _part("".join(common), "Orientações comuns")
    # Instalações 0.2 sem IDs: reconhecer títulos conhecidos sem inventar revisões.
    headings = list(re.finditer(r"^## \d+\. (.+)$", text, re.M))
    for index, match in enumerate(headings):
        title = match[1]
        identifier = LEGACY_IDS.get(slug(title), slug(title))
        if identifier in items:
            raise SDDError(f"Item antigo ambíguo: {title}")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        items[identifier] = _part(text[match.start():end], title)
    return items, _part(text[:headings[0].start()] if headings else text, "Orientações comuns")


def _range(text: str, anchor: str) -> tuple[int, int]:
    lines = text.splitlines(keepends=True)
    headings, fence = [], None
    for index, line in enumerate(lines):
        code = re.match(r"\s*(`{3,}|~{3,})", line)
        if code:
            marker = code[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        match = re.match(r"^(#{1,6}) (.+?)\s*$", line)
        if match:
            headings.append((index, len(match[1]), slug(match[2])))
    if not anchor:
        return 0, next((i for i, level, _ in headings if level >= 2), len(lines))
    found = [(i, level) for i, level, name in headings if name == slug(anchor)]
    if len(found) > 1:
        raise SDDError(f"Referência de seção ambígua: {anchor}")
    if not found:
        return 0, 0
    begin, level = found[0]
    return begin, next((i for i, depth, _ in headings if i > begin and depth <= level), len(lines))


def _fragment(resources: dict[str, str], ref: str) -> str:
    path, mark, anchor = ref.partition("#")
    text = resources.get(path, "")
    if not mark:
        return text
    begin, end = _range(text, anchor)
    return "".join(text.splitlines(keepends=True)[begin:end])


def validate(block: str, resources: dict[str, str]) -> None:
    items, common = sections(block)
    if not items:
        raise SDDError("Governador deve conter itens identificáveis")
    for part in [common, *items.values()]:
        for ref in part["uses"]:
            if ref.partition("#")[0] not in resources or not _fragment(resources, ref):
                raise SDDError(f"Dependência desconhecida do governador: {ref}")


def _difference(resource: str, before: str, after: str) -> dict | None:
    if before == after:
        return None
    patch = "\n".join(difflib.unified_diff(before.splitlines(), after.splitlines(), fromfile=f"anterior/{resource}", tofile=f"atual/{resource}", lineterm=""))
    return {"resource": resource, "diff": patch}


def _remainder(text: str, path: str, refs: set[str]) -> str:
    lines = text.splitlines(keepends=True)
    covered = set()
    for ref in refs:
        name, mark, anchor = ref.partition("#")
        if name != path:
            continue
        begin, end = _range(text, anchor) if mark else (0, len(lines))
        covered.update(range(begin, end))
    return "".join(line for index, line in enumerate(lines) if index not in covered)


def compare(before: str | None, after: str, old_resources: dict[str, str], new_resources: dict[str, str]) -> list[dict]:
    old_items, old_common = sections(before)
    new_items, new_common = sections(after)
    changes = []
    pairs = [("geral", old_common, new_common)]
    pairs += [(key, old_items.get(key), new_items.get(key)) for key in dict.fromkeys([*old_items, *new_items])]
    refs = set()
    for identifier, old, new in pairs:
        details = []
        difference = _difference("instruções", old["text"] if old else "", new["text"] if new else "")
        if difference:
            details.append(difference)
        dependencies = set((old or {}).get("uses", [])) | set((new or {}).get("uses", []))
        if old and new and old["bound"] and new["bound"]:
            difference = _difference("referências associadas", json.dumps(old["uses"], ensure_ascii=False), json.dumps(new["uses"], ensure_ascii=False))
            if difference:
                details.append(difference)
        refs.update(dependencies)
        for ref in sorted(dependencies):
            difference = _difference(ref, _fragment(old_resources, ref), _fragment(new_resources, ref))
            if difference:
                details.append(difference)
        if identifier == "geral" and list(old_items) != list(new_items):
            details.append(_difference("ordem dos itens", "\n".join(old_items), "\n".join(new_items)))
        if details:
            changes.append({"id": identifier, "title": (new or old)["title"], "kind": "adicionado" if old is None else "removido" if new is None else "alterado", "details": details})
    # Alteração em conteúdo compartilhado sem associação explícita continua visível.
    for path in sorted(old_resources.keys() | new_resources.keys()):
        difference = _difference(path, _remainder(old_resources.get(path, ""), path, refs), _remainder(new_resources.get(path, ""), path, refs))
        if difference:
            common = next((change for change in changes if change["id"] == "geral"), None)
            if common is None:
                common = {"id": "geral", "title": "Orientações comuns", "kind": "alterado", "details": []}
                changes.insert(0, common)
            common["details"].append(difference)
    return changes
