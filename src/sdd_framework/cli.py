"""As três entradas públicas: inicie, update e conferência."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .checks import create_remediation, inspect
from .project import initialize, update
from .progress import EXECUTORS, STATES, groups, human_tasks, update_roadmap
from .storage import SDDError


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(prog="sdd", description="Organização e conformidade documental SDD. Não executa código do consumidor.")
    command.add_argument("--version", action="version", version=__version__)
    operations = command.add_subparsers(dest="operation", required=True)
    init = operations.add_parser("init", aliases=["inicie"], help="Preparar projeto e plano progressivo de adequação")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--agent", choices=["codex", "claude", "both", "none"], default="both")
    init.add_argument("--mode", choices=["auto", "new", "existing"], default="auto")
    init.add_argument("--json", action="store_true")
    refresh = operations.add_parser("update", help="Atualizar recursos; preservar documentos do projeto")
    refresh.add_argument("path", nargs="?", default=".")
    source = refresh.add_mutually_exclusive_group()
    source.add_argument("--source", type=Path, help="Checkout local ou diretório assets de uma distribuição compatível")
    source.add_argument("--repository", help="Repositório HTTPS explícito da distribuição")
    refresh.add_argument("--ref", help="Tag/branch Git explícita (não executa scripts do repositório)")
    refresh.add_argument("--json", action="store_true")
    check = operations.add_parser("check", aliases=["conferencia", "conferência"], help="Verificar estrutura, tarefas e pendências humanas")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--phase", choices=["discovery", "requirements", "architecture", "planning", "specification", "design", "tasks", "implementation", "validation", "delivery"])
    check.add_argument("--spec", help="Nome da pasta da entrega a avaliar para avanço; demais entregas mantêm suas etapas")
    check.add_argument("--fix", action="store_true", help="Criar tickets de adequação; não preencher documentos nem aprovar decisões")
    check.add_argument("--roadmap", action="store_true", help="Atualizar no roadmap a visão de todas as tarefas e ações humanas")
    check.add_argument("--json", action="store_true")
    return command


def print_report(report: dict) -> None:
    print(f"Etapa: {report['phase']} | Estrutura: {'conforme' if report['structural_pass'] else 'pendente'}")
    print("Revisão semântica: necessária; este resultado não comprova testes ou aceite.")
    counts = report["counts"]
    print(f"Tarefas: {counts['done']}/{sum(counts.values())} concluídas | {counts['awaiting_user']} aguardando usuário | {counts['blocked']} bloqueadas")
    for group, tasks in groups(report).items():
        print(f"\n{group}:")
        for task in tasks:
            print(f"  {task.get('id', '?')} | {STATES.get(task.get('status'), 'Inválido')} | {EXECUTORS.get(task.get('executor'), '?')} | {task.get('title', task['path'])}")
    for issue in report["issues"]:
        print(f"[{issue['severity']}] {issue['path']} — {issue['message']}")
    if report["executable"]:
        print("Prontas e autorizadas:")
        for path in report["executable"]:
            print(f"  {path}")
    if human_tasks(report):
        print("Ações do usuário:")
        for task in human_tasks(report):
            print(f"  {task['path']} — {task.get('human_action') or 'consultar responsabilidades no ticket'}")
    if report.get("remediation_created"):
        print(f"Tickets de adequação criados: {len(report['remediation_created'])}")
    if report.get("roadmap_updated"):
        print(f"Roadmap atualizado: {report['roadmap_updated']}")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.path).expanduser().resolve()
    try:
        if args.operation in ("init", "inicie"):
            report = initialize(root, args.agent, args.mode)
            code = 0
        elif args.operation == "update":
            if args.ref and not args.repository:
                raise SDDError("--ref exige --repository; para fonte já configurada, use update sem essas opções")
            report = update(root, args.source, args.repository, args.ref)
            code = 0
        else:
            report = inspect(root, args.phase, args.spec)
            if args.fix:
                created = create_remediation(root, report)
                report = inspect(root, args.phase, args.spec)
                report["remediation_created"] = created
            if args.roadmap:
                report["roadmap_updated"] = update_roadmap(root, report)
            code = 0 if report["structural_pass"] else 1
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        elif args.operation in ("check", "conferencia", "conferência"):
            print_report(report)
        else:
            print(f"SDD {report['version']} | {len(report['changed'])} arquivos criados/atualizados")
            if args.operation in ("init", "inicie"):
                print(f"Projeto: {report['mode']} | integração: {report['agent']}")
                print("Leia AGENTS.md e .sdd/adoption/TASKS.md. Planejamento será preenchido pelo agente com o usuário.")
            else:
                print(report["note"])
        return code
    except (SDDError, OSError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc), "exit_code": 2}, ensure_ascii=False))
        else:
            print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
