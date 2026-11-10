"""Referências limitadas ao padrão atual/aplicado; a IA mantém a execução."""
from __future__ import annotations

import copy
import json

from .changes import _difference, _fragment, _remainder, sections
from .storage import SDDError, digest

EXECUTION = ".sdd/execucao.json"
LEGACY_STATES = {"not_started", "unrecorded", "in_progress", "pending", "completed"}


def fingerprint(value: object) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def snapshots(procedure: str | None, resources: dict[str, str]) -> dict:
    items, common = sections(procedure)
    refs = set(common["uses"])
    refs.update(ref for item in items.values() for ref in item["uses"])
    result = {}
    for identifier, part in [("geral", common), *items.items()]:
        content = {"title": part["title"], "instructions": part["text"],
                   "references": part["uses"],
                   "resources": {ref: _fragment(resources, ref) for ref in part["uses"]}}
        if identifier == "geral":
            content["order"] = list(items)
            content["resources"].update({path: rest for path, text in resources.items()
                                         if (rest := _remainder(text, path, refs))})
        result[identifier] = {"hash": fingerprint(content), "content": content}
    return result


def installed_hash(state: dict) -> str:
    return fingerprint({key: item["installed"] for key, item in state["items"].items()})


def _validate_snapshot(value: object) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or set(value) != {"hash", "content"}:
        raise SDDError("Referência de execução inválida")
    content = value["content"]
    if (not isinstance(content, dict) or not isinstance(content.get("title"), str)
            or not isinstance(content.get("instructions"), str)
            or not isinstance(content.get("references"), list)
            or any(not isinstance(ref, str) for ref in content["references"])
            or not isinstance(content.get("resources"), dict)
            or any(not isinstance(k, str) or not isinstance(v, str) for k, v in content["resources"].items())
            or ("order" in content and (not isinstance(content["order"], list)
                or any(not isinstance(key, str) for key in content["order"])))
            or value["hash"] != fingerprint(content)):
        raise SDDError("Conteúdo/hash da referência de execução inválido")


def validate_state(state: dict, expected: str) -> None:
    if state.get("schema_version") not in (1, 2) or not isinstance(state.get("items"), dict):
        raise SDDError("Controle de execução incompatível")
    for key, item in state["items"].items():
        if not isinstance(key, str) or not isinstance(item, dict):
            raise SDDError("Item de execução inválido")
        valid_completion = (item.get("status") in LEGACY_STATES if state["schema_version"] == 1
                            else type(item.get("completed")) is bool)
        if (not valid_completion
                or not isinstance(item.get("evidence"), list)
                or any(not isinstance(value, str) or not value.strip() for value in item["evidence"])
                or not isinstance(item.get("remaining"), list)
                or any(not isinstance(value, str) or not value.strip() for value in item["remaining"])):
            raise SDDError("Estado/evidências de execução inválidos")
        for field in ("installed", "applied", "baseline"):
            if field not in item:
                raise SDDError(f"Campo de execução ausente: {field}")
            _validate_snapshot(item[field])
        completed = item.get("status") == "completed" if state["schema_version"] == 1 else item["completed"]
        if completed and (item["applied"] is None or not item["evidence"] or item["remaining"]):
            raise SDDError("Conclusão exige referência aplicada, evidência e nenhuma pendência")
    if installed_hash(state) != expected:
        raise SDDError("Referências instaladas modificadas; controle preservado")
    if "legacy_pending" in state and not isinstance(state["legacy_pending"], str):
        raise SDDError("Registro anterior inválido")


def difference(before: dict | None, after: dict | None, identifier: str) -> dict | None:
    if before == after:
        return None
    old = before["content"] if before else {}
    new = after["content"] if after else {}
    details = []
    for label, field in (("instruções", "instructions"), ("título", "title")):
        change = _difference(label, old.get(field, ""), new.get(field, ""))
        if change:
            details.append(change)
    for label, field in (("referências associadas", "references"), ("ordem dos itens", "order")):
        change = _difference(label, "\n".join(old.get(field, [])), "\n".join(new.get(field, [])))
        if change:
            details.append(change)
    old_refs, new_refs = old.get("resources", {}), new.get("resources", {})
    for ref in sorted(old_refs.keys() | new_refs.keys()):
        change = _difference(ref, old_refs.get(ref, ""), new_refs.get(ref, ""))
        if change:
            details.append(change)
    return {"id": identifier, "title": (new or old)["title"],
            "kind": "adicionado" if before is None else "removido" if after is None else "alterado",
            "details": details} if details else None


def operation(item: dict) -> str:
    if item["installed"] is None:
        return "assess_removal"
    if not item["completed"]:
        return "execute"
    return "preserve" if item["applied"]["hash"] == item["installed"]["hash"] else "reexecute"


def refresh(state: dict | None, current: dict, version: str, *, previous: dict | None = None,
            legacy: str | None = None) -> dict:
    result = copy.deepcopy(state) if state else {"schema_version": 2, "items": {}}
    if result["schema_version"] == 1:
        for item in result["items"].values():
            item["completed"] = item.pop("status") == "completed"
        result["schema_version"] = 2
    result["version"] = version
    if legacy:
        result["legacy_pending"] = legacy
    items = result["items"]
    for key in dict.fromkeys([*items, *current]):
        if key not in items:
            items[key] = {"completed": False,
                          "installed": None, "applied": None,
                          "baseline": previous.get(key) if previous is not None else current.get(key),
                          "evidence": [], "remaining": [], "pending": None}
        item = items[key]
        item["installed"] = current.get(key)
        base = item["applied"] if item["applied"] is not None else item["baseline"]
        item["pending"] = difference(base, item["installed"], key)
        # Uma única referência anterior, nunca uma cadeia de versões.
        if item["applied"] is not None:
            item["baseline"] = None
    return result
