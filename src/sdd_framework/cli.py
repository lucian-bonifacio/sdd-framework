"""Instalação e atualização; não executa o governador nem o consumidor."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .project import initialize, update
from .storage import SDDError


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(prog="sdd", description="Instalar e atualizar o governador SDD. A execução é acionada pelo usuário na IA.")
    command.add_argument("--version", action="version", version=__version__)
    operations = command.add_subparsers(dest="operation", required=True)
    init = operations.add_parser("init", help="Instalar governador, padrões e skills; não organizar o projeto")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--json", action="store_true")
    refresh = operations.add_parser("update", help="Atualizar instruções; não acionar o governador")
    refresh.add_argument("path", nargs="?", default=".")
    refresh.add_argument("--source", type=Path, help="Checkout ou diretório assets local da distribuição")
    refresh.add_argument("--json", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.path).expanduser().resolve()
    try:
        result = initialize(root) if args.operation == "init" else update(root, args.source)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"SDD {result['version']} | {len(result['changed'])} arquivos atualizados | {len(result['removed'])} recursos antigos removidos")
            print(result["note"])
            if result.get("governor_changes"):
                print("Itens alterados: " + ", ".join(change["title"] for change in result["governor_changes"]))
        return 0
    except (SDDError, OSError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc), "exit_code": 2}, ensure_ascii=False))
        else:
            print(f"Erro: {exc}", file=sys.stderr)
        return 2
