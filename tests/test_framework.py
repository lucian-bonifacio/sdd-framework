from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sdd_framework.checks import create_remediation, inspect
from sdd_framework.cli import main
from sdd_framework.markdown import metadata, render
from sdd_framework.project import AGENT_BLOCK, END, START, bundle, initialize, update
from sdd_framework.progress import START as PROGRESS_START, update_roadmap
from sdd_framework.storage import SDDError, atomic_apply, json_bytes, project_lock, read_json, safe_path


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sdd-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "project"
        self.root.mkdir()

    def put(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def config(self, **values):
        config = read_json(self.root, ".sdd/config.json")
        config.update(values)
        self.put(".sdd/config.json", json_bytes(config).decode())

    def complete_adoption(self):
        for path in (self.root / ".sdd/adoption/tasks").glob("*.md"):
            text = path.read_text().replace("status: pending", "status: done").replace("status: ready", "status: done")
            text = text.replace("verification: not_verified", "verification: passed").replace("Ainda não executada.", "Gate executado e conteúdo revisado com usuário.")
            path.write_text(text)

    def project_documents(self):
        self.put("README.md", "# Produto\n\n## Objetivo\nOrganizar livros.\n\n## Como começar\nExecutar os comandos do projeto.\n")
        for path, headings in {
            "docs/PRD.md": ["Problema e público", "Objetivos e escopo", "Requisitos", "Restrições e pendências"],
            "docs/ARCHITECTURE.md": ["Contexto técnico", "Componentes e contratos", "Restrições e segurança", "Verificação"],
            "docs/ROADMAP.md": ["Entregas", "Prioridades e dependências"],
        }.items():
            self.put(path, "---\nstatus: accepted\n---\n# Documento\n\n" + "\n\n".join(f"## {heading}\nConteúdo definido para o cenário de teste." for heading in headings) + "\n")
        self.config(interface=False)
        with (self.root / "AGENTS.md").open("a", encoding="utf-8") as output:
            output.write("\n## Contexto do projeto\nCatálogo de livros.\n\n## Comandos e verificações\nUsar os comandos do projeto.\n\n## Convenções e restrições\nPreservar contratos.\n")

    def feature(self, folder="001-livros", status="ready", executor="agent", authorization="approved", dependencies=None):
        base = f"specs/{folder}"
        self.put(base + "/SPEC.md", f"---\nid: {folder}\nstatus: accepted\ndesign: inline\n---\n# Livros\n\n## Objetivo e escopo\nCadastrar livros.\n\n## Requisitos\n- RF-001: O usuário cadastra um livro.\n\n## Critérios de aceitação\n- CA-001: Ao informar título, livro é salvo.\n\n## Design técnico\nUsar repositório de livros existente.\n\n## Pendências\nNenhuma.\n")
        self.put(base + "/TASKS.md", "# Tarefas\n\n## Índice\n- [T-001](tasks/T-001.md)\n\n## Ordem e acompanhamento\nSeguir dependências.\n")
        template = bundle()["templates/TASK.md"].decode()
        text = render(template, task_id="T-001", title="Cadastrar livro")
        text = text.replace("status: pending", "status: " + status).replace("executor: agent", "executor: " + executor).replace("authorization: pending", "authorization: " + authorization)
        text = text.replace("dependencies: []", "dependencies: " + json.dumps(dependencies or []))
        import re
        text = re.sub(r"\[PREENCHER:[^\]]+\]", "Cadastrar livro conforme RF-001 e verificar persistência.", text)
        self.put(base + "/tasks/T-001.md", text)
        return base + "/tasks/T-001.md"

    def errors(self, phase=None, spec=None):
        return [i for i in inspect(self.root, phase, spec)["issues"] if i["severity"] == "error"]

    def test_progressive_init_is_idempotent(self):
        result = initialize(self.root)
        self.assertEqual(result["mode"], "new")
        self.assertFalse((self.root / "docs/PRD.md").exists())
        self.assertFalse((self.root / "CHECKPOINT.md").exists())
        self.assertEqual(len(list((self.root / ".sdd/adoption/tasks").glob("*.md"))), 6)
        self.assertEqual(initialize(self.root)["changed"], [])
        self.assertTrue(inspect(self.root)["structural_pass"])
        self.assertEqual(inspect(self.root)["executable"], [".sdd/adoption/tasks/T-001.md"])

    def test_native_directories_and_neutral_codex_config(self):
        initialize(self.root, agent="both")
        self.assertTrue((self.root / ".claude/skills/sdd/SKILL.md").is_file())
        config = self.root / ".codex/config.toml"
        self.assertTrue(config.is_file())
        self.assertEqual(tomllib.loads(config.read_text()), {})
        self.assertNotIn(".codex/config.toml", read_json(self.root, ".sdd/manifest.json")["files"])

    def test_codex_config_owned_by_consumer_survives_init_and_update(self):
        original = b'# Minha configuracao\r\nmodel = "modelo-do-consumidor"\r\n'
        (self.root / ".codex").mkdir()
        (self.root / ".codex/config.toml").write_bytes(original)
        initialize(self.root, agent="codex")
        update(self.root)
        self.assertEqual((self.root / ".codex/config.toml").read_bytes(), original)
        self.assertFalse((self.root / ".claude").exists())

    def test_claude_only_does_not_create_codex_configuration(self):
        initialize(self.root, agent="claude")
        self.assertTrue((self.root / ".claude/skills/sdd/SKILL.md").is_file())
        self.assertFalse((self.root / ".codex").exists())

    def test_update_prepares_missing_codex_config_in_existing_installation(self):
        initialize(self.root, agent="codex")
        (self.root / ".codex/config.toml").unlink()
        self.assertIn("codex_config_missing", {i["code"] for i in self.errors()})
        self.assertIn(".codex/config.toml", update(self.root)["changed"])
        self.assertEqual(self.errors(), [])

    def test_invalid_codex_toml_is_reported_and_preserved(self):
        initialize(self.root, agent="codex")
        config = self.root / ".codex/config.toml"
        config.write_text("model = [")
        update(self.root)
        self.assertEqual(config.read_text(), "model = [")
        self.assertIn("codex_config_invalid", {i["code"] for i in self.errors()})

    def test_read_only_codex_directory_fails_preflight_before_resources(self):
        protected = self.root / ".codex"
        protected.mkdir()
        real_access = os.access

        def access(path, mode):
            return False if Path(path) == protected else real_access(path, mode)

        with patch("sdd_framework.storage.os.access", side_effect=access):
            with self.assertRaisesRegex(SDDError, r"\.codex/config.toml.*terminal"):
                initialize(self.root, agent="both")
        self.assertFalse((self.root / ".sdd/framework").exists())
        self.assertFalse((self.root / ".sdd/config.json").exists())
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_existing_instructions_preserved_byte_for_byte(self):
        before = "# Projeto\n\nRegra própria: não usar rede.\n"
        self.put("AGENTS.md", before)
        self.put("CLAUDE.md", "Meu conteúdo.\n")
        self.put("docs/PRD.md", "Documento legado sem formatação SDD.\n")
        self.assertEqual(initialize(self.root)["mode"], "existing")
        self.assertTrue((self.root / "AGENTS.md").read_text().startswith(before))
        self.assertEqual((self.root / "docs/PRD.md").read_text(), "Documento legado sem formatação SDD.\n")
        with (self.root / "AGENTS.md").open("a") as output:
            output.write("\nOutra regra fora do bloco.\n")
        text = (self.root / "AGENTS.md").read_bytes()
        update(self.root)
        self.assertEqual(text, (self.root / "AGENTS.md").read_bytes())

    def test_windows_line_endings_outside_block_are_preserved(self):
        before = b"# Instrucoes\r\n\r\nRegra do consumidor.\r\n"
        (self.root / "AGENTS.md").write_bytes(before)
        initialize(self.root, agent="none")
        self.assertTrue((self.root / "AGENTS.md").read_bytes().startswith(before))
        current = (self.root / "AGENTS.md").read_bytes()
        update(self.root)
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), current)

    def test_malformed_marker_aborts_before_resources_written(self):
        self.put("AGENTS.md", START + "\nBloco quebrado")
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertFalse((self.root / ".sdd/config.json").exists())
        self.assertFalse((self.root / ".sdd/framework").exists())

    def test_unowned_skill_is_not_overwritten(self):
        self.put(".agents/skills/sdd/SKILL.md", "Minha skill")
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual((self.root / ".agents/skills/sdd/SKILL.md").read_text(), "Minha skill")
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_symlink_escape_is_rejected(self):
        outside = Path(self.directory.name) / "outside"
        outside.mkdir()
        (self.root / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.root / ".sdd/config.json").exists())

    def test_modified_resource_blocks_update_atomically(self):
        initialize(self.root)
        source = self.root / ".sdd/framework/templates/TASK.md"
        source.write_text("Customização importante")
        agents = (self.root / "AGENTS.md").read_bytes()
        manifest = (self.root / ".sdd/manifest.json").read_bytes()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(source.read_text(), "Customização importante")
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), agents)
        self.assertEqual((self.root / ".sdd/manifest.json").read_bytes(), manifest)

    def test_modified_block_is_not_overwritten(self):
        initialize(self.root)
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text().replace("Fluxo SDD", "Meu Fluxo SDD"))
        with self.assertRaises(SDDError):
            update(self.root)

    def test_local_release_update_preserves_product_docs(self):
        initialize(self.root)
        source = Path(self.directory.name) / "release"
        for path, content in bundle().items():
            target = source / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (source / "bundle.json").write_text(json.dumps({"version": "0.1.1", "schema_version": 1}))
        (source / "skill/SKILL.md").write_text((source / "skill/SKILL.md").read_text() + "\nAjuste da nova versão.\n")
        self.put("docs/PRD.md", "Requisitos aprovados pelo usuário.")
        result = update(self.root, source=source)
        self.assertEqual(result["version"], "0.1.1")
        self.assertEqual((self.root / "docs/PRD.md").read_text(), "Requisitos aprovados pelo usuário.")
        self.assertIn("Ajuste da nova versão", (self.root / ".agents/skills/sdd/SKILL.md").read_text())

    def test_incompatible_bundle_is_rejected(self):
        initialize(self.root)
        source = Path(self.directory.name) / "release"
        source.mkdir()
        (source / "bundle.json").write_text('{"version":"0.2.0","schema_version":2}')
        (source / "policy.json").write_text('{}')
        with self.assertRaises(SDDError):
            update(self.root, source=source)

    def test_init_does_not_downgrade_newer_installed_resources(self):
        initialize(self.root)
        config = read_json(self.root, ".sdd/config.json")
        config["framework_version"] = "0.1.1"
        self.put(".sdd/config.json", json_bytes(config).decode())
        manifest = read_json(self.root, ".sdd/manifest.json")
        manifest["version"] = "0.1.1"
        self.put(".sdd/manifest.json", json_bytes(manifest).decode())
        self.assertEqual(initialize(self.root)["version"], "0.1.1")
        with self.assertRaises(SDDError):
            update(self.root)

    def test_remote_update_requires_safe_explicit_reference(self):
        initialize(self.root)
        for repository, ref in (("file:///tmp/repo", "main"), ("https://github.com/a/b", None), ("https://user:token@github.com/a/b", "main"), ("https://github.com/a/b", "--upload-pack=bad")):
            with self.subTest(repository=repository, ref=ref), self.assertRaises(SDDError):
                update(self.root, repository=repository, ref=ref)

    def test_failed_remote_update_does_not_mutate_project(self):
        initialize(self.root)
        before = (self.root / ".sdd/manifest.json").read_bytes()
        with patch("sdd_framework.project.subprocess.run", side_effect=subprocess.TimeoutExpired("git", 60)):
            with self.assertRaises(SDDError):
                update(self.root, repository="https://github.com/example/repository", ref="v0.1.1")
        self.assertEqual((self.root / ".sdd/manifest.json").read_bytes(), before)

    def test_remote_update_reads_bundle_and_remembers_explicit_source(self):
        initialize(self.root)

        def checkout(command, **options):
            self.assertEqual(command[:4], ["git", "-c", "core.hooksPath=/dev/null", "clone"])
            self.assertEqual(options["timeout"], 60)
            target = Path(command[-1]) / "src/sdd_framework/assets"
            for name, content in bundle().items():
                file = target / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(content)
            (target / "bundle.json").write_text('{"version":"0.1.1","schema_version":1}')
            return subprocess.CompletedProcess(command, 0)

        with patch("sdd_framework.project.subprocess.run", side_effect=checkout) as clone:
            result = update(self.root, repository="https://github.com/example/sdd", ref="v0.1.1")
            self.assertEqual(result["version"], "0.1.1")
            self.assertEqual(update(self.root)["source"], "https://github.com/example/sdd")
            self.assertEqual(clone.call_count, 2)

    def test_complete_consumer_reaches_delivery_gate(self):
        initialize(self.root)
        self.project_documents()
        self.complete_adoption()
        path = self.feature(status="done")
        file = self.root / path
        file.write_text(file.read_text().replace("verification: not_verified", "verification: passed").replace("Ainda não executada.", "Persistência verificada pelo teste de cadastro."))
        report = inspect(self.root, "delivery")
        self.assertTrue(report["structural_pass"], report["issues"])
        self.assertEqual(report["counts"]["done"], 7)
        self.assertEqual(report["executable"], [])

    def test_missing_docs_gate_next_phase(self):
        initialize(self.root)
        missing = {i["path"] for i in self.errors("architecture") if i["code"] == "missing_document"}
        self.assertEqual(missing, {"README.md", "docs/PRD.md"})

    def test_placeholder_does_not_satisfy_gate(self):
        initialize(self.root)
        self.put("docs/PRD.md", bundle()["templates/PRD.md"].decode())
        codes = {i["code"] for i in self.errors("architecture")}
        self.assertIn("placeholder", codes)
        self.assertIn("unaccepted_document", codes)

    def test_existing_document_mapping(self):
        initialize(self.root)
        self.project_documents()
        (self.root / "docs/PRD.md").rename(self.root / "docs/PRODUCT.md")
        self.config(document_paths={"docs/PRD.md": "docs/PRODUCT.md"})
        self.assertEqual(self.errors("architecture"), [])

    def test_unsafe_mapping_rejected(self):
        initialize(self.root)
        self.config(document_paths={"docs/PRD.md": "../../outside.md"})
        with self.assertRaises(SDDError):
            inspect(self.root)

    def test_ready_task_requires_authorization(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature(authorization="pending")
        report = inspect(self.root, "implementation")
        self.assertIn("authorization", [i["code"] for i in report["issues"]])
        self.assertNotIn(path, report["executable"])

    def test_product_task_does_not_execute_before_implementation_gate(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature()
        self.assertNotIn(path, inspect(self.root)["executable"])
        self.assertIn(path, inspect(self.root, "implementation")["executable"])

    def test_dependency_cycle_and_missing_reference(self):
        initialize(self.root)
        self.project_documents()
        path = "specs/001-livros/tasks/T-001.md"
        self.feature(dependencies=[path, "specs/002-outro/tasks/T-001.md"])
        codes = {i["code"] for i in self.errors("implementation")}
        self.assertIn("dependency_cycle", codes)
        self.assertIn("missing_dependency", codes)

    def test_requirement_coverage(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature()
        ticket = self.root / path
        ticket.write_text(ticket.read_text().replace('["RF-001"]', '["RF-999"]'))
        codes = {i["code"] for i in self.errors("implementation")}
        self.assertIn("unknown_requirement", codes)
        self.assertIn("uncovered_requirement", codes)

    def test_done_requires_verification_result_and_no_human_pending(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature(status="done", executor="joint")
        ticket = self.root / path
        ticket.write_text(ticket.read_text().replace("Nenhuma.", "Usuário precisa conferir visualmente."))
        codes = {i["code"] for i in self.errors("implementation")}
        self.assertTrue({"unverified_completion", "missing_result", "pending_human_action"} <= codes)

    def test_human_wait_does_not_hide_independent_task(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature(status="awaiting_user", executor="joint")
        ticket = self.root / path
        ticket.write_text(ticket.read_text().replace("Nenhuma.", "Usuário: criar conta; devolver identificador público e confirmar acesso. T-002 depende disso."))
        independent = self.feature("002-independente")
        report = inspect(self.root, "implementation")
        self.assertIn(path, report["awaiting_user"])
        self.assertIn(independent, report["executable"])

    def test_checkpoint_references_actual_ticket(self):
        initialize(self.root)
        template = bundle()["templates/CHECKPOINT.md"].decode()
        template = render(template, date="2026-11-06").replace("task: none", "task: inexistente.md")
        self.put("CHECKPOINT.md", template)
        self.assertIn("checkpoint_task", {i["code"] for i in self.errors()})

    def test_invalid_unrelated_spec_does_not_hide_independent_ready_task(self):
        initialize(self.root)
        self.project_documents()
        ready = self.feature()
        self.feature("002-futura", status="pending")
        draft = self.root / "specs/002-futura/SPEC.md"
        draft.write_text(draft.read_text().replace("status: accepted", "status: draft"))
        report = inspect(self.root, "implementation")
        self.assertFalse(report["structural_pass"])
        self.assertIn(ready, report["executable"])

    def test_ready_task_does_not_depend_on_invalid_done_ticket(self):
        initialize(self.root)
        self.project_documents()
        dependency = self.feature(status="done")
        ready = self.feature("002-dependente", dependencies=[dependency])
        report = inspect(self.root, "implementation")
        self.assertNotIn(ready, report["executable"])

    def test_validation_report_identifies_tested_revision(self):
        initialize(self.root)
        self.put("specs/001-livros/validation/relatorio.md", "---\nverification: passed\n---\n# Relatório\n\n## Escopo e revisão\nTicket T-001.\n\n## Verificações\nTestes executados.\n\n## Resultados e limitações\nAmbiente local.\n")
        self.assertIn("validation_metadata", {i["code"] for i in self.errors()})

    def test_pending_inbox_is_visible_but_not_blocking(self):
        initialize(self.root)
        self.put("docs/inbox/ITEM-001.md", "---\nid: ITEM-001\nstatus: pending\ncreated: 2026-11-06\n---\n# Memória\n\n## Informação ou proposta\nAvaliar ferramenta.\n\n## Fontes\nConversa do usuário em 2026-11-06.\n\n## Impacto e discussão\nIntegração opcional.\n\n## Destino ou justificativa\nPendente.\n")
        report = inspect(self.root)
        self.assertTrue(report["structural_pass"])
        self.assertIn("inbox_pending", {i["code"] for i in report["issues"]})

    def test_roadmap_tracks_state_changes_and_preserves_planning(self):
        initialize(self.root)
        self.project_documents()
        ticket = self.feature()
        roadmap = self.root / "docs/ROADMAP.md"
        original = roadmap.read_bytes()
        update_roadmap(self.root, inspect(self.root))
        self.assertTrue(roadmap.read_bytes().startswith(original))
        self.assertIn("Pronta", roadmap.read_text())
        file = self.root / ticket
        file.write_text(file.read_text().replace("status: ready", "status: awaiting_user").replace("Nenhuma.", "Usuário: conferir o formulário e informar o resultado."))
        update_roadmap(self.root, inspect(self.root))
        content = roadmap.read_text()
        self.assertEqual(content.count(PROGRESS_START), 1)
        self.assertIn("Aguardando usuário", content)
        self.assertIn("conferir o formulário", content)
        self.assertIn("../specs/001-livros/tasks/T-001.md", content)

    def test_roadmap_uses_configured_equivalent_path(self):
        initialize(self.root)
        self.project_documents()
        self.feature()
        self.put("planning/maps/PROJECT.md", (self.root / "docs/ROADMAP.md").read_text())
        self.config(document_paths={"docs/ROADMAP.md": "planning/maps/PROJECT.md"})
        self.assertEqual(update_roadmap(self.root, inspect(self.root)), "planning/maps/PROJECT.md")
        self.assertIn("../../specs/001-livros/tasks/T-001.md", (self.root / "planning/maps/PROJECT.md").read_text())
        self.assertNotIn(PROGRESS_START, (self.root / "docs/ROADMAP.md").read_text())

    def test_malformed_progress_markers_preserve_roadmap(self):
        initialize(self.root)
        self.project_documents()
        path = self.root / "docs/ROADMAP.md"
        original = path.read_text() + "\n" + PROGRESS_START
        path.write_text(original)
        with self.assertRaises(SDDError):
            update_roadmap(self.root, inspect(self.root))
        self.assertEqual(path.read_text(), original)

    def test_cli_progress_includes_remediation_created_in_same_run(self):
        initialize(self.root)
        self.project_documents()
        self.put("README.md", "Conteúdo original sem seções.")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["check", str(self.root), "--fix", "--roadmap", "--json"])
        report = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertTrue(report["remediation_created"])
        paths = {task["path"] for task in report["tasks"]}
        self.assertTrue(set(report["remediation_created"]) <= paths)
        self.assertIn("Acompanhamento das tarefas", (self.root / "docs/ROADMAP.md").read_text())

    def test_remediation_is_deduplicated_and_preserves_documents(self):
        initialize(self.root)
        self.put("README.md", "Meu conteúdo original")
        report = inspect(self.root, "architecture")
        created = create_remediation(self.root, report)
        self.assertTrue(created)
        self.assertEqual(create_remediation(self.root, inspect(self.root, "architecture")), [])
        self.assertEqual((self.root / "README.md").read_text(), "Meu conteúdo original")

    def test_manifest_cannot_omit_required_resource(self):
        initialize(self.root)
        manifest = read_json(self.root, ".sdd/manifest.json")
        manifest["files"].pop(".agents/skills/sdd/SKILL.md")
        self.put(".sdd/manifest.json", json_bytes(manifest).decode())
        self.assertIn("untracked_resource", {i["code"] for i in self.errors()})

    def test_validation_gate_detects_unfinished_tasks(self):
        initialize(self.root)
        self.project_documents()
        self.feature()
        self.assertIn("unfinished_task", {i["code"] for i in self.errors("validation")})

    def test_design_system_is_reference_only(self):
        initialize(self.root)
        self.config(interface=True, design_system={"reference": "design/SYSTEM.md", "version": "1"})
        self.assertIn("design_system_reference", {i["code"] for i in self.errors()})
        self.assertFalse((self.root / "design/SYSTEM.md").exists())

    def test_selected_feature_does_not_demand_acceptance_of_other_drafts(self):
        initialize(self.root)
        self.project_documents()
        self.feature()
        self.feature("002-futura", status="pending", authorization="pending")
        draft = self.root / "specs/002-futura/SPEC.md"
        draft.write_text(draft.read_text().replace("status: accepted", "status: draft"))
        self.assertEqual(self.errors("implementation", "001-livros"), [])

    def test_lock_prevents_competing_writers(self):
        with project_lock(self.root):
            with self.assertRaises(SDDError):
                initialize(self.root)
        self.assertFalse((self.root / ".sdd/lock").exists())

    def test_atomic_write_rolls_back_previous_changes(self):
        self.put("first.md", "original")
        real_replace = os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("Falha simulada de escrita")
            return real_replace(source, target)

        with patch("sdd_framework.storage.os.replace", side_effect=fail_second):
            with self.assertRaises(SDDError):
                atomic_apply(self.root, {"first.md": b"changed", "second.md": b"new"})
        self.assertEqual((self.root / "first.md").read_text(), "original")
        self.assertFalse((self.root / "second.md").exists())

    def test_cli_json_and_error_codes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["inicie", str(self.root), "--agent", "none", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["agent"], "none")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["conferencia", str(self.root), "--phase", "implementation", "--json"])
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(output.getvalue())["structural_pass"])
        self.put(".sdd/config.json", "{broken")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["check", str(self.root), "--json"]), 2)

    def test_malformed_metadata_is_reported_without_crash(self):
        initialize(self.root)
        self.project_documents()
        path = self.feature()
        self.put(path, "---\nid: T-001\nstatus: [\n---\n")
        self.assertIn("metadata", {i["code"] for i in self.errors("implementation")})

    def test_consumer_docs_work_without_framework_resources(self):
        initialize(self.root, agent="none")
        self.project_documents()
        self.feature()
        import shutil
        shutil.rmtree(self.root / ".sdd")
        self.assertIn("RF-001", (self.root / "specs/001-livros/SPEC.md").read_text())
        self.assertIn("Cadastrar livro", (self.root / "specs/001-livros/tasks/T-001.md").read_text())
        self.assertIn("ARCHITECTURE", str(self.root / "docs/ARCHITECTURE.md"))

    def test_consumer_script_updates_without_sdd_from_another_directory(self):
        initialize(self.root, agent="none")
        self.project_documents()
        ticket = self.feature(status="awaiting_user", executor="joint")
        file = self.root / ticket
        file.write_text(file.read_text().replace("Nenhuma.", "Usuário: configurar acesso e devolver o resultado."))
        original = (self.root / "docs/ROADMAP.md").read_bytes()
        import shutil
        shutil.rmtree(self.root / ".sdd")
        script = self.root / "scripts/atualizar_roadmap.py"
        result = subprocess.run([sys.executable, "-I", str(script)], cwd=self.directory.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        content = (self.root / "docs/ROADMAP.md").read_bytes()
        self.assertTrue(content.startswith(original))
        self.assertIn("configurar acesso", content.decode())
        self.assertIn("Aguardando usuário", content.decode())
        self.assertFalse((self.root / ".sdd").exists())

    def test_consumer_script_customization_survives_framework_update(self):
        original = "# Ferramenta própria do consumidor\n"
        self.put("scripts/atualizar_roadmap.py", original)
        initialize(self.root, agent="none")
        update(self.root)
        self.assertEqual((self.root / "scripts/atualizar_roadmap.py").read_text(), original)

    def test_consumer_script_preserves_roadmap_when_ticket_is_invalid(self):
        initialize(self.root, agent="none")
        self.project_documents()
        ticket = self.feature()
        self.put(ticket, "---\nid: T-001\nstatus: invalid\n---\n")
        before = (self.root / "docs/ROADMAP.md").read_bytes()
        result = subprocess.run([sys.executable, "-I", str(self.root / "scripts/atualizar_roadmap.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.root / "docs/ROADMAP.md").read_bytes(), before)
        self.assertFalse((self.root / "docs/ROADMAP.md.lock").exists())

    def test_consumer_script_respects_local_roadmap_path(self):
        initialize(self.root, agent="none")
        self.project_documents()
        self.feature()
        self.put("planning/PRODUCT.md", (self.root / "docs/ROADMAP.md").read_text())
        import shutil
        shutil.rmtree(self.root / ".sdd")
        result = subprocess.run([sys.executable, "-I", str(self.root / "scripts/atualizar_roadmap.py"), "--roadmap", "planning/PRODUCT.md"], cwd=self.directory.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(PROGRESS_START, (self.root / "planning/PRODUCT.md").read_text())
        self.assertNotIn(PROGRESS_START, (self.root / "docs/ROADMAP.md").read_text())

    def test_consumer_script_does_not_follow_symlinked_tickets(self):
        initialize(self.root, agent="none")
        self.project_documents()
        ticket = self.feature()
        outside = Path(self.directory.name) / "outside.md"
        outside.write_text((self.root / ticket).read_text())
        (self.root / ticket).unlink()
        (self.root / ticket).symlink_to(outside)
        before = (self.root / "docs/ROADMAP.md").read_bytes()
        result = subprocess.run([sys.executable, "-I", str(self.root / "scripts/atualizar_roadmap.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.root / "docs/ROADMAP.md").read_bytes(), before)


class FormatTests(unittest.TestCase):
    def test_duplicate_and_nested_metadata_rejected(self):
        for text in ("---\nid: T-001\nid: T-002\n---", "---\ncontext:\n  nested: value\n---", "---\ndependencies: [1]\n---"):
            with self.assertRaises(SDDError):
                metadata(text)

    def test_paths_cannot_escape_root(self):
        for relative in ("../out", "/etc/passwd", "a/../../out", "a\\out", "."):
            with self.assertRaises(SDDError):
                safe_path(Path("/tmp"), relative)


class ReleaseTests(unittest.TestCase):
    def test_zipapp_is_self_contained(self):
        with tempfile.TemporaryDirectory(prefix="sdd-release-") as directory:
            app = Path(directory) / "sdd.pyz"
            subprocess.run([sys.executable, str(ROOT / "tools/build_release.py"), "--output", str(app)], check=True, capture_output=True)
            project = Path(directory) / "consumer"
            subprocess.run([sys.executable, str(app), "init", str(project), "--agent", "both"], cwd=directory, check=True, capture_output=True)
            result = subprocess.run([sys.executable, str(app), "check", str(project), "--json"], cwd=directory, check=True, capture_output=True, text=True)
            self.assertTrue(json.loads(result.stdout)["structural_pass"])


if __name__ == "__main__":
    unittest.main()
