"""I/O restrito à raiz explícita, sem seguir links e sem sobrescrita cega."""
from __future__ import annotations

import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path, PurePosixPath


class SDDError(Exception):
    pass


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise SDDError(f"Caminho inválido: {relative!r}")
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or relative == ".":
        raise SDDError(f"Caminho fora do projeto: {relative}")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise SDDError(f"Link simbólico não permitido em artefato SDD: {relative}")
    return current


def read(root: Path, relative: str) -> str | None:
    path = safe_path(root, relative)
    if not path.exists():
        return None
    if not path.is_file():
        raise SDDError(f"Esperado arquivo: {relative}")
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise SDDError(f"Não foi possível ler {relative}: {exc}") from exc


def read_json(root: Path, relative: str) -> dict:
    content = read(root, relative)
    if content is None:
        raise SDDError(f"Arquivo ausente: {relative}. Execute sdd init primeiro.")
    try:
        value = json.loads(content)
    except ValueError as exc:
        raise SDDError(f"JSON inválido em {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise SDDError(f"Objeto JSON esperado em {relative}")
    return value


def atomic_apply(root: Path, changes: dict[str, bytes], directories: tuple[str, ...] = ()) -> None:
    """Preflight completo e rollback de conteúdo em caso de falha de escrita."""
    previous: dict[str, bytes | None] = {}
    for relative in changes:
        path = safe_path(root, relative)
        if path.exists() and not path.is_file():
            raise SDDError(f"Esperado arquivo: {relative}")
        previous[relative] = path.read_bytes() if path.exists() else None
        if previous[relative] != changes[relative]:
            parent = path.parent
            while not parent.exists():
                parent = parent.parent
            if not parent.is_dir():
                raise SDDError(f"Esperado diretório para criar {relative}: {parent}")
            if not os.access(parent, os.W_OK):
                raise SDDError(f"Sem permissão de escrita para {relative}. Execute init/update no terminal com acesso ao projeto, antes de abrir uma sessão de agente que proteja essas pastas.")
    for relative in directories:
        path = safe_path(root, relative)
        if path.exists() and not path.is_dir():
            raise SDDError(f"Esperado diretório: {relative}")
    written: list[str] = []

    def replace(path: Path, content: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + f".sdd-tmp-{os.getpid()}")
        if temporary.exists() or temporary.is_symlink():
            raise SDDError(f"Arquivo temporário já existe: {temporary}")
        try:
            with temporary.open("xb") as output:
                output.write(content)
            if path.exists():
                temporary.chmod(path.stat().st_mode & 0o777)
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()

    try:
        for relative in directories:
            safe_path(root, relative).mkdir(parents=True, exist_ok=True)
        for relative, content in changes.items():
            if content == previous[relative]:
                continue
            replace(safe_path(root, relative), content)
            written.append(relative)
    except (OSError, SDDError) as exc:
        failures = []
        for relative in reversed(written):
            try:
                path = safe_path(root, relative)
                if previous[relative] is None:
                    path.unlink()
                else:
                    replace(path, previous[relative])
            except OSError as rollback:
                failures.append(str(rollback))
        suffix = f"; rollback incompleto: {failures}" if failures else ""
        raise SDDError(f"Escrita interrompida: {exc}{suffix}") from exc


@contextmanager
def project_lock(root: Path):
    directory = safe_path(root, ".sdd")
    directory.mkdir(parents=True, exist_ok=True)
    lock = safe_path(root, ".sdd/lock")
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError as exc:
        raise SDDError("Há outra operação SDD ou lock residual em .sdd/lock. Inspecione antes de remover.") from exc
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)
