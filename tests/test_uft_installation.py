"""Portable project installation, including the integrated UFT runtime.

No test modifies global Claude/Codex configuration, runs a model, or connects to
GitHub. The review replay checks archived evidence and does not create an audit.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from genius.install import install_project
from uft.skills import SKILL_NAMES, validate_skills

ROOT = Path(__file__).resolve().parents[1]


class PortableUFTInstallationTests(unittest.TestCase):
    def run_command(self, target, *arguments):
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        result = subprocess.run([sys.executable, *arguments], cwd=target, env=environment,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
        return json.loads(result.stdout)

    def test_fresh_install_runs_after_original_checkout_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            source, target = parent / "source", parent / "project"
            install_project(ROOT, source)
            installed = install_project(source, target)
            self.assertTrue(installed["complete"], installed)
            self.assertEqual(installed["runtime"], "uft")
            for relative in ("uft/__main__.py", "data/goals.json", "config/research.json", "tests/test_uft_store.py", ".gitignore",
                             "docs/research_protocol.md", "evidence/scientific-review.json", "Descargas/UFT_guide.pdf"):
                self.assertTrue((target / relative).is_file(), relative)
            source.rename(parent / "source-unavailable")
            self.assertFalse(source.exists())
            self.assertEqual(len(list((target / ".claude/agents").glob("*.md"))), 7)
            self.assertTrue(validate_skills(target)["valid"])
            for name in SKILL_NAMES:
                entry = target / ".claude/skills" / name / "SKILL.md"
                self.assertTrue(entry.is_file(), name)
                self.assertTrue(entry.resolve().is_relative_to(target))
                text = entry.read_text(encoding="utf-8")
                for relative in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" not in relative and not relative.startswith("#"):
                        self.assertTrue((entry.resolve().parent / relative.split("#", 1)[0]).exists(), (name, relative))
            validation = self.run_command(target, "-m", "uft", "validate")
            self.assertTrue(validation["valid"])
            self.assertEqual(validation["skills"]["count"], 27)
            self.assertEqual(validation["registry"]["profile_count"], 5000)
            self.run_command(target, "-m", "uft", "init")
            seed = self.run_command(target, "scripts/seed_research.py", "--apply-reviewed-audits")
            self.assertEqual(seed["physical_goals_completed"], 0)
            self.assertGreaterEqual(len(seed["reviewed_scoped_claims_imported"]), 1)
            cycle = self.run_command(target, "-m", "uft", "cycle", "--output", str(parent / "new-cycle"))
            self.assertTrue(cycle["successful"], cycle)
            self.assertEqual(cycle["scientific_promotions"], 0)
            self.assertEqual(len(cycle["executions"]), 2)

    def test_working_state_and_credential_files_are_not_copied(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "source", Path(directory) / "project"
            files = {
                "config/research.json": '{"fixture":"public configuration"}',
                "config/private.sqlite-wal": "working journal fixture",
                "memory/cache.db-shm": "working shared-memory fixture",
                "automation/local-state.json": '{"active":false}',
                ".claude/settings.local.json": '{"private":"fixture only"}',
                ".codex/auth.json": '{"credential":"test fixture only"}',
                "data/.env": "FIXTURE_SECRET=do-not-copy",
            }
            for relative, content in files.items():
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            result = install_project(source, target)
            self.assertTrue(result["complete"])
            self.assertTrue((target / "config/research.json").is_file())
            for relative in set(files) - {"config/research.json"}:
                self.assertFalse((target / relative).exists(), relative)

    def test_external_source_symlinks_are_rejected_without_copying_their_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            source, target, outside = parent / "source", parent / "project", parent / "outside"
            source.mkdir()
            outside.mkdir()
            (outside / "private.md").write_text("External test fixture only", encoding="utf-8")
            (source / "docs").symlink_to(outside, target_is_directory=True)
            result = install_project(source, target)
            self.assertFalse(result["complete"])
            self.assertEqual(result["unsafe_source_links"], ["docs"])
            self.assertFalse((target / "docs").exists())

    def test_internal_absolute_symlinks_are_rebased_and_installation_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            source, target = parent / "source", parent / "project"
            canonical = source / ".agents/skills/fixture"
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text("Fixture canonical instructions", encoding="utf-8")
            adapter = source / ".claude/skills/fixture"
            adapter.parent.mkdir(parents=True)
            adapter.symlink_to(canonical, target_is_directory=True)
            preview = install_project(source, target, dry_run=True)
            self.assertTrue(preview["complete"])
            self.assertFalse(target.exists())
            first = install_project(source, target)
            self.assertTrue(first["complete"])
            mirrored = target / ".claude/skills/fixture"
            self.assertFalse(os.path.isabs(os.readlink(mirrored)))
            self.assertEqual(mirrored.resolve(), (target / ".agents/skills/fixture").resolve())
            second = install_project(source, target)
            self.assertTrue(second["complete"])
            self.assertEqual(second["copied"], [])
            self.assertEqual(set(second["unchanged"]), set(first["copied"]))

    def test_existing_project_configuration_is_preserved_with_explicit_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            source, target = parent / "source", parent / "project"
            (source / ".claude").mkdir(parents=True)
            (target / ".claude").mkdir(parents=True)
            (source / "CLAUDE.md").write_text("UFT instructions", encoding="utf-8")
            (source / ".claude/settings.json").write_text('{"source":"fixture"}', encoding="utf-8")
            originals = {"CLAUDE.md": "User project instructions", ".claude/settings.json": '{"model":"user-choice"}'}
            for relative, content in originals.items():
                (target / relative).write_text(content, encoding="utf-8")
            before = {name: hashlib.sha256((target / name).read_bytes()).hexdigest() for name in originals}
            result = install_project(source, target)
            self.assertFalse(result["complete"])
            self.assertEqual(set(result["conflicts_preserved"]), set(originals))
            self.assertEqual({name: hashlib.sha256((target / name).read_bytes()).hexdigest() for name in originals}, before)


if __name__ == "__main__":
    unittest.main()
