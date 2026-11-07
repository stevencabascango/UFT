"""Discovery and isolation checks for the integrated research skill library."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from genius.skills import REQUIRED_SECTIONS, SKILL_NAMES as CORE_SKILL_NAMES
from uft.skills import INTEGRATED_SKILL_NAMES, SKILL_NAMES, discover_skills, load_skill, validate_skills
from uft.store import ResearchStore

ROOT = Path(__file__).resolve().parents[1]


class IntegratedSkillTests(unittest.TestCase):
    def test_shared_library_discovers_twenty_seven_without_mutating_scientific_goals(self):
        before = (ROOT / "data/goals.json").read_bytes()
        skills = discover_skills(ROOT)
        self.assertEqual(len(skills), 27)
        self.assertEqual(len({skill["name"] for skill in skills}), 27)
        self.assertEqual(tuple(skill["name"] for skill in skills[:22]), CORE_SKILL_NAMES)
        self.assertEqual({skill["name"] for skill in skills if skill["library"] == "integrated_uft"}, set(INTEGRATED_SKILL_NAMES))
        self.assertEqual((ROOT / "data/goals.json").read_bytes(), before)
        goals = json.loads(before)
        self.assertFalse(any(goal.get("achieved") for goal in goals["goals"]))
        record = validate_skills(ROOT)
        self.assertTrue(record["valid"], record["errors"])
        self.assertFalse(record["scientific_goals_achieved"])
        self.assertEqual((record["core_count"], record["integrated_count"]), (22, 5))

    def test_claude_and_codex_resolve_to_exactly_the_same_canonical_instruction(self):
        canonical = discover_skills(ROOT, environment="canonical")
        claude = discover_skills(ROOT, environment="claude")
        self.assertEqual([s["path"] for s in canonical], [s["path"] for s in claude])
        for name in INTEGRATED_SKILL_NAMES:
            with self.subTest(skill=name):
                self.assertTrue((ROOT / ".claude/skills" / name).is_symlink())
                self.assertEqual(load_skill(ROOT, name), load_skill(ROOT, name, environment="claude"))
                content = load_skill(ROOT, name)
                for section in REQUIRED_SECTIONS:
                    self.assertIn(f"## {section}\n", content)

    def test_arbitrary_file_paths_and_environments_are_not_loadable(self):
        for name in ("../goals.json", "/etc/passwd", ".", "unknown-skill", "relational-time-lqg/../../../../etc/passwd"):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "Unknown UFT skill"):
                load_skill(ROOT, name)
        with self.assertRaisesRegex(ValueError, "Unknown skill environment"):
            load_skill(ROOT, "scientific-intake", environment="external")

    def test_missing_capability_is_not_silently_discovered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agents/skills").mkdir(parents=True)
            with self.assertRaises(FileNotFoundError):
                discover_skills(root)
            result = validate_skills(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any("scientific-intake" in error for error in result["errors"]))

    def test_canonical_symlink_cannot_read_an_outside_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            folder = root / ".agents/skills/scientific-intake"
            folder.mkdir(parents=True)
            outside = Path(directory) / "private-instructions.md"
            outside.write_text("Private outside file that must not be loaded", encoding="utf-8")
            (folder / "SKILL.md").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "escapes the shared skill library"):
                load_skill(root, "scientific-intake")

    def test_library_root_cannot_be_redirected_outside_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root, outside = Path(directory) / "repo", Path(directory) / "outside"
            (root / ".agents").mkdir(parents=True)
            outside.mkdir()
            (root / ".agents/skills").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "directory escapes"):
                load_skill(root, "scientific-intake")

    def test_equal_text_external_adapter_is_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            canonical = root / ".agents/skills/scientific-intake"
            canonical.mkdir(parents=True)
            content = load_skill(ROOT, "scientific-intake")
            (canonical / "SKILL.md").write_text(content, encoding="utf-8")
            outside = Path(directory) / "outside"
            outside.mkdir()
            (outside / "SKILL.md").write_text(content, encoding="utf-8")
            adapter = root / ".claude/skills/scientific-intake"
            adapter.parent.mkdir(parents=True)
            adapter.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "does not resolve to its canonical skill"):
                load_skill(root, "scientific-intake", environment="claude")

    def test_validator_reports_incomplete_skill_without_modifying_core(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / ".agents", root / ".agents", symlinks=True)
            shutil.copytree(ROOT / ".claude/skills", root / ".claude/skills", symlinks=True)
            (root / "docs").mkdir()
            for name in ("scientific_protocol.md", "research_protocol.md"):
                shutil.copy2(ROOT / "docs" / name, root / "docs" / name)
            core = root / ".agents/skills/rigorous-proof/SKILL.md"
            before = core.read_bytes()
            path = root / ".agents/skills/scientific-intake/SKILL.md"
            path.write_text(path.read_text().replace("## Colaboración\n", ""), encoding="utf-8")
            result = validate_skills(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any("scientific-intake: missing section Colaboración" in error for error in result["errors"]))
            self.assertEqual(core.read_bytes(), before)

    def test_intake_example_workflow_preserves_pending_physics_and_idempotence(self):
        # A realistic input supported by the intake skill: inability to obtain a
        # paper is recorded as an open problem rather than invented evidence.
        with tempfile.TemporaryDirectory() as directory:
            with ResearchStore(Path(directory) / "research.sqlite") as store:
                record = {"id": "SOURCE-UNAVAILABLE", "kind": "document", "objectives": ["googly"],
                          "statement": "The proposed reconstruction argument requires a source not yet obtained",
                          "hypotheses": [], "evidence": [], "dependencies": [], "status": "proposal",
                          "review": {"status": "pending", "reason": "Full text inaccessible"},
                          "sources": [{"id": "LOCAL-REFERENCE-PENDING", "verified": False}]}
                event = {"id": "INTAKE-DEMO", "source": "local-reference-list", "version": "1", "entity": record}
                self.assertEqual(store.ingest(event)["status"], "completed")
                self.assertTrue(store.ingest(event)["idempotent"])
                snapshot = store.snapshot()
                self.assertEqual(snapshot["entities"][0]["status"], "proposal")
                self.assertEqual(snapshot["alerts"], [])
                self.assertEqual(snapshot["assessments"], [])


if __name__ == "__main__":
    unittest.main()
