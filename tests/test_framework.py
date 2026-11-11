from __future__ import annotations

import copy
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sdd_framework.cli import main
from sdd_framework import __version__
from sdd_framework.changes import LOG_START, LOG_END, log_section, sections
from sdd_framework.project import (
    AGENT_BLOCK, CLAUDE_BLOCK, END, GIT_RULES, GOV_END, GOV_START, GOVERNOR, GOVERNOR_TEMPLATE, LEGACY_GOVERNOR,
    LEGACY_BLOCK, MANIFEST, OLD_END, OLD_FLOW, OLD_START, START,
    _resources, bundle, initialize, managed_section, update,
)
from sdd_framework.execution import EXECUTION, installed_hash, operation
from sdd_framework.storage import SDDError, atomic_apply, digest, json_bytes, read_json, safe_path


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="sdd-test-")
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.root = self.base / "projeto"
        self.root.mkdir()

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode())
        return path

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def release(self, version=None, change=True):
        path = self.base / "release"
        shutil.copytree(ROOT / "src/sdd_framework/assets", path)
        info = json.loads((path / "bundle.json").read_text(encoding="utf-8"))
        major, minor, _ = map(int, __version__.split("."))
        info["version"] = version or f"{major}.{minor + 1}.0"
        (path / "bundle.json").write_bytes(json_bytes(info))
        governor = path / GOVERNOR_TEMPLATE
        if change:
            marker = b"<!-- SDD:ITEM:tasks:START -->"
            governor.write_bytes(governor.read_bytes().replace(marker, marker + b"\nInstrucao adicionada na atualizacao.", 1))
        return path

    def legacy(self):
        resources = {
            ".sdd/framework/templates/PRD.md": b"# Modelo antigo\n",
            ".sdd/framework/policy.json": b"{}\n",
            ".agents/skills/sdd/SKILL.md": b"Skill anterior\n",
            ".agents/skills/sdd/references/WORKFLOW.md": b"Fluxo anterior\n",
            ".claude/skills/sdd/SKILL.md": b"Skill anterior\n",
        }
        old_agent = START + "\nSiga docs/FLUXO.md automaticamente.\n" + END
        old_flow = OLD_START + "\n## Procedimento padrao\nFluxo antigo.\n" + OLD_END
        blocks = {"AGENTS.md": old_agent, "CLAUDE.md": old_agent, OLD_FLOW: old_flow}
        for name, data in resources.items():
            self.put(name, data.decode())
        for name, block in blocks.items():
            self.put(name, "Conteudo proprio antes.\r\n\r\n" + block + "\r\n\r\nPlano aprovado e historico preservado.\r\n")
        self.put(".sdd/config.json", '{"mode":"existing","phase":"implementation","custom":true}\n')
        self.put(".sdd/adoption/tasks/T-001.md", "Ticket concluido anteriormente.\n")
        self.put("scripts/atualizar_roadmap.py", "# Script proprio.\n")
        self.put(MANIFEST, json_bytes({
            "schema_version": 1, "version": "0.1.0",
            "files": {n: digest(v) for n, v in resources.items()},
            "blocks": {n: digest(v.encode()) for n, v in blocks.items()},
        }).decode())
        return resources, blocks

    def test_init_prepares_only_instructions_and_configuration(self):
        result = initialize(self.root)
        self.assertFalse(result["governor_executed"])
        self.assertTrue((self.root / GOVERNOR).is_file())
        self.assertFalse((self.root / LEGACY_GOVERNOR).exists())
        procedure = self.root / GOVERNOR
        for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", procedure.read_text(encoding="utf-8")):
            self.assertTrue((procedure.parent / link).is_file(), link)
        self.assertTrue((self.root / "docs/padroes/PRD.md").is_file())
        self.assertTrue((self.root / ".codex/config.toml").is_file())
        for name in ("README.md", "docs/PRD.md", "docs/ROADMAP.md", "docs/FLUXO.md",
                     "specs", "src", "scripts", ".github", ".sdd/adoption", ".sdd/config.json"):
            self.assertFalse((self.root / name).exists(), name)
        self.assertEqual(managed_section((self.root / "AGENTS.md").read_text(encoding="utf-8")), AGENT_BLOCK)
        self.assertEqual(managed_section((self.root / "CLAUDE.md").read_text(encoding="utf-8")), CLAUDE_BLOCK)

    def test_both_native_integrations_are_explicit_only(self):
        initialize(self.root)
        codex = (self.root / ".agents/skills/sdd/agents/openai.yaml").read_text(encoding="utf-8")
        claude = (self.root / ".claude/skills/sdd/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", codex)
        self.assertIn("disable-model-invocation: true", claude.split("---")[1])
        original = bundle()["skill/SKILL.md"].decode().replace("\r\n", "\n")
        self.assertEqual((self.root / ".agents/skills/sdd/SKILL.md").read_text(encoding="utf-8"), original)
        self.assertEqual(claude.replace("disable-model-invocation: true\n", "", 1), original)

    def test_crlf_distribution_keeps_explicit_claude_invocation(self):
        source = self.release(change=False)
        for path in source.rglob("*"):
            if path.is_file():
                path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        contents = bundle(source)
        with patch("sdd_framework.project.bundle", return_value=contents):
            initialize(self.root)
        claude = (self.root / ".claude/skills/sdd/SKILL.md").read_bytes()
        self.assertIn(b"name: sdd\r\ndisable-model-invocation: true\r\n", claude)
        self.assertEqual(claude.replace(b"disable-model-invocation: true\r\n", b"", 1), contents["skill/SKILL.md"])
        self.assertEqual(update(self.root, source)["changed"], [])

    def test_repeated_init_does_not_modify_existing_installation(self):
        initialize(self.root)
        self.put("docs/padroes/PRD.md", "Modelo ajustado localmente.\n")
        before = self.snapshot()
        result = initialize(self.root)
        self.assertTrue(result["already_initialized"])
        self.assertEqual(result["changed"], [])
        self.assertEqual(self.snapshot(), before)

    def test_existing_business_files_and_configuration_are_untouched(self):
        original = {
            "README.md": "# Produto existente\n", "src/app.py": "raise RuntimeError('nao executar')\n",
            "docs/PRD.md": "# Negocio importante\n", ".codex/config.toml": '# Minha configuracao\ncustom = true\n',
        }
        for name, text in original.items():
            self.put(name, text)
        initialize(self.root)
        update(self.root)
        for name, text in original.items():
            self.assertEqual((self.root / name).read_bytes(), text.encode())

    def test_update_replaces_resources_and_preserves_project_bytes(self):
        self.put("AGENTS.md", "# Instrucoes proprias\r\nNao publicar.\r\n")
        initialize(self.root)
        path = self.root / GOVERNOR
        with path.open("ab") as output:
            output.write(b"\r\nPlano proprio: migrar conteudo e aguardar decisao X.\r\n")
        before = path.read_bytes()
        old_block = managed_section(before.decode(), GOV_START, GOV_END).encode()
        old_agent = (self.root / "AGENTS.md").read_bytes()
        result = update(self.root, self.release())
        after = path.read_bytes()
        new_block = managed_section(after.decode(), GOV_START, GOV_END).encode()
        self.assertNotEqual(old_block, new_block)
        self.assertEqual(before.replace(old_block, b"", 1), after.replace(new_block, b"", 1))
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), old_agent)
        self.assertEqual(result["version"], json.loads((self.base / "release/bundle.json").read_text(encoding="utf-8"))["version"])
        self.assertFalse(result["governor_executed"])
        manifest = read_json(self.root, MANIFEST)
        for name, expected in manifest["files"].items():
            self.assertEqual(digest((self.root / name).read_bytes()), expected)

    def test_update_with_same_distribution_is_idempotent(self):
        initialize(self.root)
        before = self.snapshot()
        result = update(self.root)
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["removed"], [])
        self.assertEqual(self.snapshot(), before)

    def test_git_policy_is_managed_but_custom_rules_and_config_are_preserved(self):
        custom = self.put(".codex/rules/pessoal.rules", '# Regra particular\r\n')
        config = self.put(".codex/config.toml", '# Configuracao particular\r\n')
        before = (custom.read_bytes(), config.read_bytes())
        initialize(self.root)
        expected = bundle()["integrations/codex/sdd-git.rules"]
        self.assertEqual((self.root / GIT_RULES).read_bytes(), expected)
        self.assertEqual(read_json(self.root, MANIFEST)["files"][GIT_RULES], digest(expected))
        source = self.release(change=False)
        rule = source / "integrations/codex/sdd-git.rules"
        rule.write_bytes(expected + b"\n# Revisao da politica.\n")
        result = update(self.root, source)
        self.assertFalse(result["governor_executed"])
        self.assertEqual((self.root / GIT_RULES).read_bytes(), rule.read_bytes())
        self.assertEqual({change["id"] for change in result["governor_changes"]}, {"geral"})
        self.assertEqual((custom.read_bytes(), config.read_bytes()), before)
        self.assertEqual(update(self.root, source)["changed"], [])

    def test_update_adds_git_policy_to_installation_without_it(self):
        contents = bundle()
        contents[GOVERNOR_TEMPLATE] = contents[GOVERNOR_TEMPLATE].replace(
            b', ".codex/rules/sdd-git.rules"', b"")
        previous_resources = {name: data for name, data in _resources(contents).items()
                              if name != GIT_RULES}
        with patch("sdd_framework.project.bundle", return_value=contents), \
                patch("sdd_framework.project._resources", return_value=previous_resources):
            initialize(self.root)
        self.assertFalse((self.root / GIT_RULES).exists())
        self.assertNotIn(GIT_RULES, read_json(self.root, MANIFEST)["files"])
        self.put("docs/PRD.md", "Contrato particular.\n")
        result = update(self.root)
        self.assertIn(GIT_RULES, result["changed"])
        self.assertEqual((self.root / GIT_RULES).read_bytes(),
                         contents["integrations/codex/sdd-git.rules"])
        self.assertEqual((self.root / "docs/PRD.md").read_bytes(), b"Contrato particular.\n")
        self.assertEqual(update(self.root)["changed"], [])

    def test_conflicting_git_policy_aborts_before_any_installation_write(self):
        self.put(GIT_RULES, "# Politica particular.\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_missing_managed_git_policy_is_not_recreated(self):
        initialize(self.root)
        (self.root / GIT_RULES).unlink()
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_git_policy_symlink_does_not_write_to_its_target(self):
        outside = self.base / "particular.rules"
        outside.write_bytes(b"# Preservar.\n")
        policy = self.root / GIT_RULES
        policy.parent.mkdir(parents=True)
        try:
            policy.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(str(exc))
        before = self.snapshot()
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertTrue(policy.is_symlink())
        self.assertEqual(outside.read_bytes(), b"# Preservar.\n")

    def test_git_policy_write_failure_rolls_back_update(self):
        initialize(self.root)
        before = self.snapshot()
        source = self.release(change=False)
        rule = source / "integrations/codex/sdd-git.rules"
        rule.write_bytes(rule.read_bytes() + b"\n# Revisao.\n")
        real_replace = os.replace
        failed = False

        def replace(src, dst):
            nonlocal failed
            if Path(dst) == self.root / GIT_RULES and not failed:
                failed = True
                raise OSError("Falha simulada ao atualizar politica Git")
            return real_replace(src, dst)

        with patch("sdd_framework.storage.os.replace", replace), self.assertRaises(SDDError):
            update(self.root, source)
        self.assertTrue(failed)
        self.assertEqual(self.snapshot(), before)

    def root_governor_installation(self):
        contents = bundle()
        with patch("sdd_framework.project.GOVERNOR", LEGACY_GOVERNOR), \
                patch("sdd_framework.project.bundle", return_value=contents), \
                patch("sdd_framework.project.AGENT_BLOCK", AGENT_BLOCK.replace(GOVERNOR, LEGACY_GOVERNOR)), \
                patch("sdd_framework.project.CLAUDE_BLOCK", CLAUDE_BLOCK.replace(GOVERNOR, LEGACY_GOVERNOR)):
            initialize(self.root)

    def test_update_moves_root_governor_without_losing_content_or_application(self):
        self.root_governor_installation()
        path = self.root / LEGACY_GOVERNOR
        original = b"# Contexto proprio\r\n" + path.read_bytes() + b"\r\nDecisao particular preservada.\r\n"
        path.write_bytes(original)
        state = read_json(self.root, EXECUTION)
        record = state["items"]["prd"]
        record.update(completed=True, applied=copy.deepcopy(record["installed"]),
                      evidence=["docs/PRD.md: requisitos aceitos"], remaining=[])
        self.put(EXECUTION, json_bytes(state).decode())
        result = update(self.root)
        migrated = (self.root / GOVERNOR).read_bytes()
        self.assertEqual(original.replace(managed_section(original.decode(), GOV_START, GOV_END).encode(), b"", 1),
                         migrated.replace(managed_section(migrated.decode(), GOV_START, GOV_END).encode(), b"", 1))
        self.assertFalse(path.exists())
        self.assertIn(LEGACY_GOVERNOR, result["removed"])
        manifest = read_json(self.root, MANIFEST)
        self.assertIn(GOVERNOR, manifest["blocks"])
        self.assertNotIn(LEGACY_GOVERNOR, manifest["blocks"])
        actual = read_json(self.root, EXECUTION)
        for key, item in state["items"].items():
            for field in ("completed", "applied", "evidence", "remaining"):
                self.assertEqual(actual["items"][key][field], item[field])
        self.assertIn(GOVERNOR, (self.root / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertFalse(result["governor_executed"])
        before = self.snapshot()
        self.assertEqual(update(self.root)["changed"], [])
        self.assertEqual(self.snapshot(), before)

    def test_governor_move_conflicts_abort_before_writes(self):
        for case in ("modified", "missing", "destination", "symlink"):
            with self.subTest(case=case):
                self.root = self.base / case
                self.root_governor_installation()
                old = self.root / LEGACY_GOVERNOR
                if case == "modified":
                    old.write_bytes(old.read_bytes().replace(b"# Governador SDD", b"# Alterado", 1))
                elif case == "missing":
                    old.unlink()
                elif case == "destination":
                    self.put(GOVERNOR, "Documento local que nao pode ser sobrescrito.\n")
                else:
                    outside = self.base / "outro-governador"
                    outside.write_bytes(old.read_bytes())
                    old.unlink()
                    try:
                        old.symlink_to(outside)
                    except OSError:
                        continue  # Windows pode exigir privilegio para criar symlink.
                before = self.snapshot()
                with self.assertRaises(SDDError):
                    update(self.root)
                self.assertEqual(self.snapshot(), before)
                if case == "symlink":
                    self.assertTrue(old.is_symlink())

    def test_unmanaged_root_governor_is_preserved(self):
        self.put(LEGACY_GOVERNOR, "Arquivo particular anterior.\n")
        initialize(self.root)
        update(self.root)
        self.assertEqual((self.root / LEGACY_GOVERNOR).read_text(encoding="utf-8"), "Arquivo particular anterior.\n")
        self.assertTrue((self.root / GOVERNOR).is_file())

    def test_governor_move_rolls_back_if_old_file_cannot_be_removed(self):
        self.root_governor_installation()
        before = self.snapshot()
        real_unlink = Path.unlink

        def unlink(path, *args, **kwargs):
            if path == self.root / LEGACY_GOVERNOR:
                raise OSError("Falha simulada na remocao do governador antigo")
            return real_unlink(path, *args, **kwargs)

        with patch("pathlib.Path.unlink", unlink), self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_prd_instruction_change_is_identified_without_touching_business_prd(self):
        initialize(self.root)
        self.put("docs/PRD.md", "Contrato do produto aprovado pelo usuario.\n")
        source = self.release(change=False)
        path = source / GOVERNOR_TEMPLATE
        path.write_text(path.read_text(encoding="utf-8").replace("Definir o contrato do produto:", "Definir o contrato do produto revisado:", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([item["id"] for item in result["governor_changes"]], ["prd"])
        detail = result["governor_changes"][0]["details"][0]
        self.assertIn("-Definir o contrato", detail["diff"])
        self.assertIn("+Definir o contrato do produto revisado", detail["diff"])
        self.assertEqual((self.root / "docs/PRD.md").read_text(encoding="utf-8"), "Contrato do produto aprovado pelo usuario.\n")
        self.assertFalse(result["governor_executed"])
        record = read_json(self.root, EXECUTION)["items"]["prd"]["pending"]
        self.assertIsNone(log_section((self.root / GOVERNOR).read_text(encoding="utf-8")))
        self.assertIn(detail["diff"], [d["diff"] for d in record["details"]])
        self.assertEqual(update(self.root, source)["governor_changes"], [])

    def test_template_change_identifies_its_item_even_without_governor_edit(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / "templates/PRD.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nRegra nova do PRD.\n", encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([item["id"] for item in result["governor_changes"]], ["prd"])
        self.assertEqual(result["governor_changes"][0]["details"][0]["resource"], "docs/padroes/PRD.md")

    def test_method_change_identifies_only_the_relevant_fragment(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / "standards/CONTRATOS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("### PRD\n", "### PRD\nRegra adicional do metodo PRD.\n", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([item["id"] for item in result["governor_changes"]], ["prd"])
        self.assertEqual(result["governor_changes"][0]["details"][0]["resource"], "docs/padroes/CONTRATOS.md#prd")

    def test_shared_changes_are_reported_without_invalidating_all_items(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / "standards/CONTRATOS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("## Escrita e fontes\n", "## Escrita e fontes\nNova orientacao comum.\n", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([item["id"] for item in result["governor_changes"]], ["geral"])

    def test_each_document_resource_identifies_only_its_consuming_items(self):
        templates = {
            "SPEC": {"specs", "design"}, "ARCHITECTURE": {"arquitetura"},
            "DESIGN": {"design"}, "TASK": {"tasks"},
            "ROADMAP": {"roadmap"}, "AGENTS": {"agents"},
            "README": {"agents"}, "CHECKPOINT": {"encerramento"},
            "ADR": {"arquitetura", "encerramento"},
            "INBOX": {"encerramento"}, "VALIDATION": {"encerramento"},
        }
        methods = {
            "Testes automatizados": ({"tasks", "agents"}, "##"),
            "Git e permissões": ({"geral", "agents"}, "##"),
            "SPEC": ({"specs"}, "###"),
            "Arquitetura": ({"arquitetura"}, "###"),
            "Design": ({"design"}, "###"),
            "Tasks": ({"tasks"}, "####"),
            "ROADMAP": ({"roadmap"}, "####"),
            "AGENTS e README": ({"agents"}, "###"),
            "Encerramento": ({"encerramento"}, "###"),
        }
        cases = [(f"templates/{name}.md", None, expected)
                 for name, expected in templates.items()]
        cases += [("standards/CONTRATOS.md", f"{depth} {name}\n", expected)
                  for name, (expected, depth) in methods.items()]
        for index, (resource, heading, expected) in enumerate(cases):
            with self.subTest(resource=resource, heading=heading):
                root = self.base / f"consumidor-{index}"
                initialize(root)
                source = self.base / f"fonte-{index}"
                shutil.copytree(ROOT / "src/sdd_framework/assets", source)
                path = source / resource
                text = path.read_text(encoding="utf-8")
                extra = "Instrução alterada somente neste recurso.\n"
                path.write_text(text.replace(heading, heading + extra, 1)
                                if heading else text + "\n" + extra, encoding="utf-8", newline="\n")
                result = update(root, source)
                self.assertEqual({c["id"] for c in result["governor_changes"]}, expected)
                self.assertFalse(result["governor_executed"])
                self.assertEqual(update(root, source)["changed"], [])

    def test_version_change_alone_does_not_request_item_reexecution(self):
        initialize(self.root)
        before_items = read_json(self.root, EXECUTION)["items"]
        result = update(self.root, self.release(change=False))
        self.assertEqual(result["governor_changes"], [])
        self.assertEqual(read_json(self.root, EXECUTION)["items"], before_items)

    def test_splitting_design_preserves_previous_architecture_application(self):
        previous = bundle()
        text = previous[GOVERNOR_TEMPLATE].decode()
        begin = text.index("<!-- SDD:ITEM:design:START -->")
        end = text.index("<!-- SDD:ITEM:design:END -->", begin) + len("<!-- SDD:ITEM:design:END -->")
        text = text[:begin] + text[end:]
        text = text.replace("## 3. Arquitetura\n", "## 3. Arquitetura e design\n", 1)
        text = text.replace("<!-- SDD:ITEM:arquitetura:END -->",
                            "Design anteriormente aplicado junto à arquitetura.\n<!-- SDD:ITEM:arquitetura:END -->", 1)
        previous[GOVERNOR_TEMPLATE] = text.encode()
        with patch("sdd_framework.project.bundle", return_value=previous):
            initialize(self.root)
        self.put("docs/ARCHITECTURE.md", "Contratos particulares e decisões aceitas.\n")
        self.put("specs/001-entrega/SPEC.md", "Design inline existente a preservar.\n")
        state = read_json(self.root, EXECUTION)
        architecture = state["items"]["arquitetura"]
        architecture.update(completed=True, applied=copy.deepcopy(architecture["installed"]),
                            evidence=["docs/ARCHITECTURE.md: contratos e design anteriores"], remaining=[])
        self.put(EXECUTION, json_bytes(state).decode())
        result = update(self.root)
        items = read_json(self.root, EXECUTION)["items"]
        self.assertEqual(list(sections((self.root / GOVERNOR).read_text(encoding="utf-8"))[0]),
                         ["prd", "specs", "arquitetura", "design", "tasks", "roadmap", "agents", "encerramento"])
        for field in ("completed", "applied", "evidence", "remaining"):
            self.assertEqual(items["arquitetura"][field], architecture[field])
        self.assertEqual(operation(items["arquitetura"]), "reexecute")
        self.assertFalse(items["design"]["completed"])
        self.assertIsNone(items["design"]["applied"])
        self.assertEqual(items["design"]["pending"]["kind"], "adicionado")
        self.assertEqual((self.root / "docs/ARCHITECTURE.md").read_text(encoding="utf-8"), "Contratos particulares e decisões aceitas.\n")
        self.assertEqual((self.root / "specs/001-entrega/SPEC.md").read_text(encoding="utf-8"), "Design inline existente a preservar.\n")
        self.assertFalse(result["governor_executed"])
        self.assertEqual(update(self.root)["changed"], [])

    def test_same_version_content_change_is_detected_without_manual_revision(self):
        initialize(self.root)
        result = update(self.root, self.release(__version__))
        self.assertEqual([item["id"] for item in result["governor_changes"]], ["tasks"])
        self.assertIsNotNone(read_json(self.root, EXECUTION)["items"]["tasks"]["pending"])

    def complete(self, key="prd"):
        state = read_json(self.root, EXECUTION)
        item = state["items"][key]
        item.update(completed=True, applied=copy.deepcopy(item["installed"]),
                    baseline=None, pending=None, remaining=[], evidence=["docs/PRD.md: criterios atendidos"])
        self.put(EXECUTION, json_bytes(state).decode())

    def test_multiple_updates_consolidate_against_applied_and_preserve_application(self):
        initialize(self.root)
        self.complete()
        before = read_json(self.root, EXECUTION)["items"]["prd"]["applied"]
        with (self.root / GOVERNOR).open("ab") as output:
            output.write(b"\nResultado anterior preservado.\n")
        source = self.release(change=False)
        path = source / GOVERNOR_TEMPLATE
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("Definir o contrato do produto:", "Definir o contrato intermediario:", 1), encoding="utf-8", newline="\n")
        update(self.root, source)
        path.write_text(original.replace("Definir o contrato do produto:", "Definir o contrato final:", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        item = read_json(self.root, EXECUTION)["items"]["prd"]
        diff = item["pending"]["details"][0]["diff"]
        self.assertIn("-Definir o contrato do produto:", diff)
        self.assertIn("+Definir o contrato final:", diff)
        self.assertNotIn("intermediario", diff)
        self.assertEqual(item["applied"], before)
        self.assertEqual(result["operations"]["prd"], "reexecute")
        self.assertIn("Resultado anterior preservado.", (self.root / GOVERNOR).read_text(encoding="utf-8"))
        self.assertIsNone(log_section((self.root / GOVERNOR).read_text(encoding="utf-8")))
        # Conclusao pela IA elimina o delta, sem novo historico.
        self.complete()
        result = update(self.root, source)
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["operations"]["prd"], "preserve")
        self.assertIsNone(read_json(self.root, EXECUTION)["items"]["prd"]["pending"])

    def test_reverted_change_clears_pending_without_touching_applied(self):
        initialize(self.root)
        self.complete()
        source = self.release(change=False)
        path = source / "templates/PRD.md"
        original = path.read_text(encoding="utf-8")
        path.write_text(original + "\nMudanca temporaria.\n", encoding="utf-8", newline="\n")
        update(self.root, source)
        self.assertIsNotNone(read_json(self.root, EXECUTION)["items"]["prd"]["pending"])
        path.write_text(original, encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual(result["operations"]["prd"], "preserve")
        self.assertIsNone(read_json(self.root, EXECUTION)["items"]["prd"]["pending"])

    def test_incomplete_execution_keeps_remaining_and_applied_on_update(self):
        initialize(self.root)
        self.assertEqual(update(self.root)["operations"]["prd"], "execute")
        self.complete()
        state = read_json(self.root, EXECUTION)
        state["items"]["prd"].update(completed=False, remaining=["Esclarecer requisito RF-001"])
        self.put(EXECUTION, json_bytes(state).decode())
        applied = state["items"]["prd"]["applied"]
        result = update(self.root, self.release())
        self.assertEqual(result["operations"]["prd"], "execute")
        item = read_json(self.root, EXECUTION)["items"]["prd"]
        self.assertEqual(item["remaining"], ["Esclarecer requisito RF-001"])
        self.assertEqual(item["applied"], applied)

    def test_added_removed_and_reordered_items_use_stable_ids(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / GOVERNOR_TEMPLATE
        text = path.read_text(encoding="utf-8")
        start = text.index("<!-- SDD:ITEM:prd:START -->")
        end = text.index("<!-- SDD:ITEM:prd:END -->") + len("<!-- SDD:ITEM:prd:END -->")
        prd = text[start:end]
        # Remover o item nao remove o documento do produto.
        self.put("docs/PRD.md", "Negocio preservado\n")
        path.write_text(text[:start] + text[end:], encoding="utf-8", newline="\n")
        result = update(self.root, source)
        change = next(c for c in result["governor_changes"] if c["id"] == "prd")
        self.assertEqual(change["kind"], "removido")
        self.assertEqual(result["operations"]["prd"], "assess_removal")
        self.assertEqual((self.root / "docs/PRD.md").read_text(encoding="utf-8"), "Negocio preservado\n")
        # Reintroduzir com o mesmo ID continua sendo o mesmo objeto, nao o numero.
        text = path.read_text(encoding="utf-8").replace("<!-- SDD:GOVERNADOR:END -->", prd + "\n<!-- SDD:GOVERNADOR:END -->")
        path.write_text(text, encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual(next(c for c in result["governor_changes"] if c["id"] == "prd")["kind"], "adicionado")
        path.write_text(text.replace(prd, "").replace("<!-- SDD:ITEM:specs:START -->", prd + "\n<!-- SDD:ITEM:specs:START -->", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([c["id"] for c in result["governor_changes"]], ["geral"])
        self.assertTrue(any(d["resource"] == "ordem dos itens" for d in result["governor_changes"][0]["details"]))

    def test_new_item_after_installation_has_added_delta_and_execute_route(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / GOVERNOR_TEMPLATE
        addition = ("<!-- SDD:ITEM:extra:START -->\n## 8. Extra\n"
                    "Objeto adicional.\n<!-- SDD:ITEM:extra:END -->\n")
        path.write_text(path.read_text(encoding="utf-8").replace(GOV_END, addition + GOV_END), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        item = read_json(self.root, EXECUTION)["items"]["extra"]
        self.assertEqual(result["operations"]["extra"], "execute")
        self.assertEqual(item["pending"]["kind"], "adicionado")
        self.assertIsNone(item["applied"])

    def test_invalid_ids_or_dependency_abort_without_changes(self):
        initialize(self.root)
        source = self.release(change=False)
        path = source / GOVERNOR_TEMPLATE
        text = path.read_text(encoding="utf-8")
        before = self.snapshot()
        path.write_text(text.replace('"docs/padroes/PRD.md"', '"docs/padroes/inexistente.md"', 1), encoding="utf-8", newline="\n")
        with self.assertRaises(SDDError):
            update(self.root, source)
        self.assertEqual(self.snapshot(), before)
        path.write_text(text.replace("SDD:ITEM:specs:", "SDD:ITEM:prd:"), encoding="utf-8", newline="\n")
        with self.assertRaises(SDDError):
            update(self.root, source)
        self.assertEqual(self.snapshot(), before)

    def test_missing_or_corrupted_execution_control_is_not_reset(self):
        initialize(self.root)
        path = self.root / EXECUTION
        original = path.read_bytes()
        for content in (b"{}", b"invalid", None):
            with self.subTest(content=content):
                if content is None:
                    path.unlink()
                else:
                    path.write_bytes(content)
                before = self.snapshot()
                with self.assertRaises(SDDError):
                    update(self.root)
                self.assertEqual(self.snapshot(), before)
                path.write_bytes(original)

    def test_installed_reference_is_protected_but_ai_fields_are_editable(self):
        initialize(self.root)
        self.complete()
        self.assertEqual(update(self.root)["changed"], [])
        state = read_json(self.root, EXECUTION)
        state["items"].pop("prd")
        self.put(EXECUTION, json_bytes(state).decode())
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_completion_without_evidence_is_rejected(self):
        initialize(self.root)
        self.complete()
        state = read_json(self.root, EXECUTION)
        state["items"]["prd"]["evidence"] = []
        self.put(EXECUTION, json_bytes(state).decode())
        with self.assertRaises(SDDError):
            update(self.root)

    def old_log(self, newline="\n"):
        # Simula uma instalacao 0.3, antes do controle separado.
        initialize(self.root)
        (self.root / EXECUTION).unlink()
        record = (LOG_START + "\n## Alteracoes recebidas\nDiff anterior pendente\n" + LOG_END).replace("\n", newline)
        with (self.root / GOVERNOR).open("ab") as output:
            output.write((newline * 2 + record + newline).encode("utf-8"))
        manifest = read_json(self.root, MANIFEST)
        manifest.pop("execution_hash")
        manifest["updates_hash"] = digest(record.encode())
        self.put(MANIFEST, json_bytes(manifest).decode())
        return record

    def test_legacy_execution_states_become_binary_without_losing_criteria(self):
        initialize(self.root)
        self.complete()
        state = read_json(self.root, EXECUTION)
        state["schema_version"] = 1
        old_states = ["completed", "pending", "in_progress", "unrecorded", "not_started"]
        for index, item in enumerate(state["items"].values()):
            item["status"] = "completed" if item.pop("completed") else old_states[1 + index % 4]
        state["items"]["tasks"]["remaining"] = ["Criterio de cobertura nao atendido"]
        self.put(EXECUTION, json_bytes(state).decode())
        result = update(self.root)
        actual = read_json(self.root, EXECUTION)
        self.assertEqual(actual["schema_version"], 2)
        self.assertTrue(actual["items"]["prd"]["completed"])
        self.assertEqual(result["operations"]["prd"], "preserve")
        self.assertFalse(actual["items"]["tasks"]["completed"])
        self.assertEqual(actual["items"]["tasks"]["remaining"], state["items"]["tasks"]["remaining"])
        self.assertEqual(actual["items"]["prd"]["evidence"], state["items"]["prd"]["evidence"])
        self.assertTrue(all("status" not in item for item in actual["items"].values()))
        self.assertEqual(update(self.root)["changed"], [])

    def test_old_log_migrates_once_without_fabricating_completion(self):
        record = self.old_log()
        before = (self.root / GOVERNOR).read_text(encoding="utf-8")
        result = update(self.root)
        state = read_json(self.root, EXECUTION)
        self.assertEqual(state["legacy_pending"], record)
        self.assertEqual(result["operations"]["prd"], "execute")
        self.assertIsNone(state["items"]["prd"]["applied"])
        self.assertEqual((self.root / GOVERNOR).read_text(encoding="utf-8"), before.replace(record, "", 1))
        self.assertNotIn("updates_hash", read_json(self.root, MANIFEST))
        self.assertEqual(update(self.root)["changed"], [])

    def test_crlf_legacy_log_preserves_exact_hash_and_content(self):
        record = self.old_log(newline="\r\n")
        before = (self.root / GOVERNOR).read_bytes()
        result = update(self.root)
        self.assertFalse(result["governor_executed"])
        self.assertEqual(read_json(self.root, EXECUTION)["legacy_pending"], record)
        self.assertEqual((self.root / GOVERNOR).read_bytes(), before.replace(record.encode("utf-8"), b"", 1))
        self.assertEqual(update(self.root)["changed"], [])

    def test_modified_old_log_aborts_before_migration(self):
        record = self.old_log()
        path = self.root / GOVERNOR
        path.write_text(path.read_text(encoding="utf-8").replace(record, record + " adulterado"), encoding="utf-8", newline="\n")
        # Modificar o trecho protegido, nao texto proprio depois dele.
        path.write_text(path.read_text(encoding="utf-8").replace("Diff anterior pendente", "Alterado"), encoding="utf-8", newline="\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_existing_v2_without_item_metadata_gets_precise_migration(self):
        initialize(self.root)
        path = self.root / GOVERNOR
        text = path.read_text(encoding="utf-8")
        (self.root / EXECUTION).unlink()
        import re
        text = re.sub(r"^<!-- SDD:(?:ITEM:.*?|USES:.*?) -->\n?", "", text, flags=re.M)
        path.write_text(text, encoding="utf-8", newline="\n")
        manifest = read_json(self.root, MANIFEST)
        manifest.pop("execution_hash")
        manifest["blocks"][GOVERNOR] = digest(managed_section(text, GOV_START, GOV_END).encode())
        self.put(MANIFEST, json_bytes(manifest).decode())
        source = self.release(change=False)
        target = source / GOVERNOR_TEMPLATE
        target.write_text(target.read_text(encoding="utf-8").replace("Definir o contrato do produto:", "Definir o contrato revisado:", 1), encoding="utf-8", newline="\n")
        result = update(self.root, source)
        self.assertEqual([c["id"] for c in result["governor_changes"]], ["prd"])

    def test_conflicting_local_skill_aborts_before_creating_governor(self):
        self.put(".agents/skills/sdd/SKILL.md", "Skill particular\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / GOVERNOR).exists())

    def test_conflicting_standard_or_governor_is_not_overwritten(self):
        for name in ("docs/padroes/PRD.md", GOVERNOR):
            with self.subTest(name=name):
                path = self.put(name, "Documento particular\n")
                before = self.snapshot()
                with self.assertRaises(SDDError):
                    initialize(self.root)
                self.assertEqual(self.snapshot(), before)
                path.unlink()

    def test_modified_managed_resources_abort_entire_update(self):
        initialize(self.root)
        for name in ("docs/padroes/PRD.md", ".claude/skills/sdd/SKILL.md", GIT_RULES):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b"\nPersonalizacao.\n")
                before = self.snapshot()
                with self.assertRaises(SDDError):
                    update(self.root)
                self.assertEqual(self.snapshot(), before)
                path.write_bytes(original)

    def test_modified_instruction_block_is_preserved(self):
        initialize(self.root)
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("Execute docs/governador.md", "Outra regra"), encoding="utf-8", newline="\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_modified_or_missing_governor_does_not_get_recreated(self):
        initialize(self.root)
        path = self.root / GOVERNOR
        original = path.read_bytes()
        path.write_bytes(original.replace(GOV_START.encode(), b"<!-- Alterado -->"))
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertNotEqual(path.read_bytes(), original)
        path.unlink()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertFalse(path.exists())

    def test_missing_managed_standard_aborts_without_restoring_silently(self):
        initialize(self.root)
        path = self.root / "docs/padroes/PRD.md"
        path.unlink()
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_malformed_or_duplicate_markers_abort(self):
        for text in (START, END + START, START + END + START + END):
            with self.subTest(text=text):
                self.put("AGENTS.md", text)
                before = self.snapshot()
                with self.assertRaises(SDDError):
                    initialize(self.root)
                self.assertEqual(self.snapshot(), before)

    def test_downgrade_is_refused_before_mutation(self):
        initialize(self.root)
        before = self.snapshot()
        with self.assertRaisesRegex(SDDError, "Downgrade"):
            update(self.root, self.release("0.1.0"))
        self.assertEqual(self.snapshot(), before)

    def test_invalid_or_executable_distribution_is_rejected(self):
        initialize(self.root)
        source = self.release()
        extra = source / "executar.py"
        extra.write_text("raise RuntimeError('nunca executar')\n", encoding="utf-8", newline="\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root, source)
        self.assertEqual(self.snapshot(), before)
        extra.unlink()
        (source / "templates/PRD.md").unlink()
        with self.assertRaises(SDDError):
            update(self.root, source)
        self.assertEqual(self.snapshot(), before)

    def test_manifest_cannot_claim_a_business_document(self):
        initialize(self.root)
        self.put("README.md", "Documento do usuario\n")
        manifest = read_json(self.root, MANIFEST)
        manifest["files"]["README.md"] = digest(b"Documento do usuario\n")
        self.put(MANIFEST, json_bytes(manifest).decode())
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_manifest_cannot_claim_other_codex_rules(self):
        initialize(self.root)
        self.put(".codex/rules/pessoal.rules", "# Particular\n")
        manifest = read_json(self.root, MANIFEST)
        manifest["files"][".codex/rules/pessoal.rules"] = digest(b"# Particular\n")
        self.put(MANIFEST, json_bytes(manifest).decode())
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_update_requires_an_existing_installation(self):
        with self.assertRaisesRegex(SDDError, "init"):
            update(self.root)
        self.assertFalse((self.root / GOVERNOR).exists())

    def test_lock_blocks_competing_writer(self):
        initialize(self.root)
        path = self.put(".sdd/lock", "Outro processo\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)
        path.unlink()

    def test_permission_preflight_prevents_partial_installation(self):
        with patch("sdd_framework.storage.os.access", return_value=False):
            with self.assertRaises(SDDError):
                initialize(self.root)
        self.assertEqual(self.snapshot(), {})

    def test_legacy_migration_removes_only_managed_resources(self):
        resources, blocks = self.legacy()
        self.put(".sdd/framework/pessoal.md", "Arquivo nao administrado\n")
        self.put("docs/PRD.md", "Conhecimento do negocio\n")
        original_flow = (self.root / OLD_FLOW).read_bytes()
        old_block = blocks[OLD_FLOW].encode()
        before_config = (self.root / ".sdd/config.json").read_bytes()
        result = update(self.root)
        self.assertFalse(result["governor_executed"])
        for name in resources:
            if name not in (".agents/skills/sdd/SKILL.md", ".claude/skills/sdd/SKILL.md"):
                self.assertFalse((self.root / name).exists(), name)
        self.assertEqual((self.root / ".sdd/framework/pessoal.md").read_text(encoding="utf-8"), "Arquivo nao administrado\n")
        self.assertEqual((self.root / "docs/PRD.md").read_text(encoding="utf-8"), "Conhecimento do negocio\n")
        after_flow = (self.root / OLD_FLOW).read_bytes()
        self.assertEqual(original_flow.replace(old_block, b""), after_flow.replace(LEGACY_BLOCK.encode(), b""))
        self.assertEqual((self.root / ".sdd/config.json").read_bytes(), before_config)
        self.assertEqual((self.root / ".sdd/adoption/tasks/T-001.md").read_text(encoding="utf-8"), "Ticket concluido anteriormente.\n")
        self.assertIn("Nao executar o fluxo anterior".casefold(), LEGACY_BLOCK.casefold().replace("não", "nao"))
        self.assertEqual(read_json(self.root, MANIFEST)["schema_version"], 2)
        self.assertEqual(update(self.root)["changed"], [])

    def test_legacy_conflict_blocks_migration_and_removals(self):
        self.legacy()
        self.put(".sdd/framework/templates/PRD.md", "Template alterado\n")
        before = self.snapshot()
        with self.assertRaises(SDDError):
            update(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / GOVERNOR).exists())

    def test_legacy_flow_can_be_removed_after_agent_migration(self):
        self.legacy()
        update(self.root)
        (self.root / OLD_FLOW).unlink()
        update(self.root)
        self.assertNotIn(OLD_FLOW, read_json(self.root, MANIFEST)["blocks"])

    def test_symlink_in_target_or_distribution_is_refused(self):
        if not hasattr(os, "symlink"):
            self.skipTest("Symlinks indisponiveis")
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.root / "docs").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(SDDError):
            initialize(self.root)
        self.assertEqual(list(outside.iterdir()), [])
        (self.root / "docs").unlink()
        source = self.release()
        path = source / "templates/PRD.md"
        path.unlink()
        path.symlink_to(ROOT / "README.md")
        with self.assertRaises(SDDError):
            bundle(source)

    def test_cli_outputs_json_and_never_runs_governor(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["init", str(self.root), "--json"]), 0)
        self.assertFalse(json.loads(output.getvalue())["governor_executed"])
        error = io.StringIO()
        empty = self.base / "sem-instalacao"
        empty.mkdir()
        with contextlib.redirect_stdout(error):
            self.assertEqual(main(["update", str(empty), "--json"]), 2)
        self.assertEqual(json.loads(error.getvalue())["exit_code"], 2)

    def test_cli_has_no_phase_gate_or_implicit_start_command(self):
        for args in (["check"], ["inicie"], ["init", "--mode", "new"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as result:
                    main(args)
                self.assertEqual(result.exception.code, 2)


class StorageTests(unittest.TestCase):
    def test_paths_cannot_escape_or_follow_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("../fora", "/fora", "a/../fora", "a\\fora", "."):
                with self.subTest(name=name), self.assertRaises(SDDError):
                    safe_path(root, name)

    def test_write_and_delete_rollback_preserves_originals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "old-a").write_bytes(b"original-a")
            (root / "old-b").write_bytes(b"original-b")
            (root / "old-a").chmod(0o600)
            real_unlink = Path.unlink
            failed = False

            def unlink(path, *args, **kwargs):
                nonlocal failed
                if path == root / "old-b" and not failed:
                    failed = True
                    raise PermissionError("Falha simulada")
                return real_unlink(path, *args, **kwargs)

            with patch.object(Path, "unlink", unlink), self.assertRaises(SDDError):
                atomic_apply(root, {"new": b"novo"}, removals=("old-a", "old-b"))
            self.assertEqual((root / "old-a").read_bytes(), b"original-a")
            self.assertEqual((root / "old-b").read_bytes(), b"original-b")
            self.assertFalse((root / "new").exists())
            if os.name != "nt":
                self.assertEqual((root / "old-a").stat().st_mode & 0o777, 0o600)

    def test_write_failure_rolls_back_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_bytes(b"antigo")
            real_replace = os.replace
            failed = False

            def replace(src, dst):
                nonlocal failed
                if Path(dst) == root / "b" and not failed:
                    failed = True
                    raise OSError("Falha simulada")
                return real_replace(src, dst)

            with patch("sdd_framework.storage.os.replace", replace), self.assertRaises(SDDError):
                atomic_apply(root, {"a": b"novo", "b": b"novo"})
            self.assertEqual((root / "a").read_bytes(), b"antigo")
            self.assertFalse((root / "b").exists())


@unittest.skipUnless(shutil.which("codex"), "Avaliador nativo Codex indisponivel")
class CodexPolicyTests(unittest.TestCase):
    def check(self, command, extra_rules=None):
        # Somente avalia tokens: nunca executa a operacao Git representada.
        args = [shutil.which("codex"), "execpolicy", "check", "--rules",
                str(ROOT / "src/sdd_framework/assets/integrations/codex/sdd-git.rules")]
        if extra_rules:
            args += ["--rules", str(extra_rules)]
        result = subprocess.run(args + ["--", *command], capture_output=True,
                                text=True, encoding="utf-8", check=True)
        return json.loads(result.stdout)

    def test_read_queries_do_not_grant_execution_outside_sandbox(self):
        for command in (["git", "status", "--short"], ["git", "diff", "--check"],
                        ["git", "log", "-5", "--oneline"], ["git", "show", "HEAD"],
                        ["git", "rev-parse", "HEAD"]):
            with self.subTest(command=command):
                result = self.check(command)
                self.assertEqual(result["matchedRules"], [])
                self.assertNotIn("decision", result)

    def test_mutations_and_global_option_variants_require_approval(self):
        commands = [
            ["git", "commit", "-m", "ajuste"], ["git", "push", "--force", "origin", "main"],
            ["git", "pull"], ["git", "merge", "outra"], ["git", "rebase", "main"],
            ["git", "reset", "--hard", "HEAD"], ["git", "restore", "."],
            ["git", "clean", "-fd"], ["git", "branch", "-D", "antiga"],
            ["git", "add", "."], ["git", "switch", "-c", "nova"],
            ["git", "checkout", "--", "."], ["git", "fetch", "origin"],
            ["git", "stash", "pop"], ["git", "config", "alias.publicar", "push"],
            ["git", "-C", "outro", "push"], ["git", "-c", "alias.publicar=push", "publicar"],
            ["git", "--git-dir", "outro/.git", "push"],
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(self.check(command)["decision"], "prompt")

    def test_unmatched_forms_never_receive_an_allow_from_sdd(self):
        # Esses casos dependem do sandbox e da autorizacao instrucional, nao
        # sao prometidos como cobertos por prefixos que nao coincidem.
        for command in (["git", "--git-dir=outro/.git", "push"],
                        ["git", "alias-particular"], ["bash", "-lc", "git status && git push"]):
            with self.subTest(command=command):
                self.assertNotEqual(self.check(command).get("decision"), "allow")

    def test_sdd_prompt_and_more_restrictive_custom_rules_take_precedence(self):
        with tempfile.TemporaryDirectory(prefix="sdd-rules-") as directory:
            extra = Path(directory) / "pessoal.rules"
            extra.write_text('prefix_rule(pattern=["git"], decision="allow")\n', encoding="utf-8")
            self.assertEqual(self.check(["git", "push"], extra)["decision"], "prompt")
            extra.write_text('prefix_rule(pattern=["git", "push"], decision="forbidden")\n', encoding="utf-8")
            self.assertEqual(self.check(["git", "push"], extra)["decision"], "forbidden")


class ReleaseTests(unittest.TestCase):
    def test_zipapp_installs_and_updates_outside_checkout(self):
        with tempfile.TemporaryDirectory(prefix="sdd-release-") as directory:
            app = Path(directory) / "sdd.pyz"
            env = dict(os.environ, PYTHONUTF8="1")
            options = dict(cwd=directory, capture_output=True, text=True, encoding="utf-8", env=env)
            subprocess.run([sys.executable, str(ROOT / "tools/build_release.py"), "--output", str(app)], check=True, **options)
            root = Path(directory) / "projeto com espacos"
            result = subprocess.run([sys.executable, str(app), "init", str(root), "--json"], check=True, **options)
            self.assertFalse(json.loads(result.stdout)["governor_executed"])
            result = subprocess.run([sys.executable, str(app), "update", str(root), "--json"], check=True, **options)
            self.assertEqual(json.loads(result.stdout)["changed"], [])
            self.assertTrue((root / "docs/padroes/PRD.md").is_file())
            self.assertEqual((root / GIT_RULES).read_bytes(),
                             bundle()["integrations/codex/sdd-git.rules"])
            self.assertTrue((root / GOVERNOR).is_file())
            self.assertFalse((root / LEGACY_GOVERNOR).exists())
            self.assertFalse((root / "specs").exists())


if __name__ == "__main__":
    unittest.main()
