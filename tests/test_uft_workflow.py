"""Acceptance tests for public entry points, source isolation and finite scope."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from uft.inventory import collect_inventory, write_json
from uft.reporting import CRITERIA, REPORT_SECTIONS, dashboard, render_scientific_report
from uft.workflow import bootstrap, run_watch
from uft.store import ResearchStore

ROOT = Path(__file__).resolve().parents[1]


class SourceAndWorkflowTests(unittest.TestCase):
    def fixture(self, root):
        brain = root / "brain"
        brain.mkdir()
        (brain / "META.md").write_text("# Test source\nVersion one\n")
        inventory = collect_inventory(brain, None)
        write_json(root / "data/source_inventory.json", inventory)
        portable = json.loads((ROOT / "data/goals.json").read_text())
        for goal in portable["goals"]:
            goal["milestones"] = []
        write_json(root / "data/goals.json", portable)
        return brain

    def test_inventory_reads_only_explicit_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain = self.fixture(root)
            (brain / "credentials.txt").write_text("TEST_SECRET_NOT_REAL")
            report = collect_inventory(brain, None)
            self.assertEqual(len(report["sources"]), 14)
            self.assertNotIn("credentials.txt", json.dumps(report))
            self.assertNotIn("TEST_SECRET_NOT_REAL", json.dumps(report))

    def test_inventory_rejects_source_symlink_outside_canonical_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain = self.fixture(root)
            outside = root / "outside.md"
            outside.write_text("OUTSIDE_TEST_CONTENT")
            (brain / "META.md").unlink()
            (brain / "META.md").symlink_to(outside)
            row = next(x for x in collect_inventory(brain)["sources"] if x["relative_path"] == "META.md")
            self.assertEqual(row["access"], "unavailable")
            self.assertNotIn("OUTSIDE_TEST_CONTENT", json.dumps(row))

    def test_bootstrap_preserves_user_changes_and_initial_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            with ResearchStore(root / "memory.sqlite") as store:
                bootstrap(root, store)
                old = store.get_entity("GOAL-QG")
                old["statement"] += " User-defined scope."
                store.upsert_entity(old)
                second = bootstrap(root, store)
                self.assertEqual(second["count"], 0)
                self.assertIn("User-defined scope.", store.get_entity("GOAL-QG")["statement"])
                snap = store.snapshot()
                self.assertEqual(len(snap["coverage"]), 108)
                self.assertEqual(len(snap["assessments"]), 21)
                self.assertFalse(any(x["status"] in {"proven", "formal"} for x in snap["entities"]))

    def test_watcher_records_failure_for_missing_source_and_no_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain = self.fixture(root)
            with ResearchStore(root / "memory.sqlite") as store:
                bootstrap(root, store)
                result = run_watch(root, store, brain=brain, interval=0, max_cycles=2, max_seconds=3)
                self.assertEqual(result["cycles"], 2)
                self.assertTrue(result["failures"])
                self.assertEqual(result["scientific_promotions"], 0)
                self.assertLess(result["elapsed_seconds"], 3)

    def test_watcher_is_quiet_without_changes_and_invalidates_changed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain = self.fixture(root)
            # Complete the fixed allowlist using harmless local fixtures.
            from uft.inventory import SOURCE_FILES
            for name in SOURCE_FILES["brain"]:
                path = brain / name
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_text("{}" if name.endswith(".json") else "# Test fixture")
            write_json(root / "data/source_inventory.json", collect_inventory(brain))
            with ResearchStore(root / "memory.sqlite") as store:
                bootstrap(root, store)
                quiet = run_watch(root, store, brain=brain, interval=0, max_cycles=1)
                self.assertTrue(quiet["quiet"])
                self.assertEqual(quiet["changes"], [])
                (brain / "partes/meta_liston.json").write_text('{"new_information": true}')
                changed = run_watch(root, store, brain=brain, interval=0, max_cycles=1)
                self.assertEqual(len(changed["changes"]), 1)
                self.assertEqual(store.get_entity("GOAL-QG")["status"], "review")
                again = run_watch(root, store, brain=brain, interval=0, max_cycles=1)
                self.assertTrue(again["quiet"])

    def test_watcher_rejects_missing_and_excessive_budgets_before_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with ResearchStore(root / "memory.sqlite") as store:
                for kwargs in ({}, {"max_cycles": 0}, {"max_seconds": 100000}, {"interval": -1}, {"max_bytes": 99999999}):
                    with self.assertRaises(ValueError):
                        run_watch(root, store, **kwargs)


class ReportContractTests(unittest.TestCase):
    def record(self):
        return {"id": "TEST-REPORT", "title": "Test fixture, not scientific evidence",
                "sections": {name: "Declared finite test scope." for name in REPORT_SECTIONS},
                "criteria": {key: {"status": "Pendiente", "evidence": "No scientific evidence in a test fixture",
                                    "limitations": "Not a physical theory", "next_check": "Obtain actual evidence"} for key in CRITERIA},
                "discriminating_tests": [], "prediction_gap": "No predictions; define a physical model first."}

    def test_report_requires_all_sections_and_no_invented_predictions(self):
        record = self.record()
        text = render_scientific_report(record)
        self.assertIn("11. Próxima comprobación prioritaria", text)
        self.assertIn("No predictions", text)
        record.pop("prediction_gap")
        with self.assertRaises(ValueError):
            render_scientific_report(record)

    def test_report_rejects_unsupported_criteria_and_more_than_five_tests(self):
        record = self.record()
        record["criteria"]["testability"]["status"] = "95% true"
        with self.assertRaises(ValueError):
            render_scientific_report(record)
        record = self.record()
        record["discriminating_tests"] = [{"test": "fixture", "failure_questions": "fixture", "scope": "fixture"}] * 6
        with self.assertRaises(ValueError):
            render_scientific_report(record)

    def test_dashboard_does_not_execute_untrusted_source_markup(self):
        malicious = "</script><script>alert('TEST_FIXTURE')</script>"
        output = dashboard({"entities": [{"id": "UNTRUSTED", "statement": malicious, "status": "proposal", "objectives": ["googly"]}], "links": []})
        self.assertNotIn(malicious, output)
        self.assertIn("\\u003c/script", output)
        self.assertIn("textContent", output)


class CycleAcceptanceTests(unittest.TestCase):
    def test_cycle_compares_artifacts_and_preserves_previous_runs(self):
        from uft.cycles import run_cycle
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cycle"
            result = run_cycle(ROOT, output)
            self.assertTrue(result["successful"])
            self.assertTrue(result["executions"][1]["comparison_verified"])
            first_id = result["executions"][0]["execution_id"]
            self.assertNotEqual(first_id, result["executions"][1]["execution_id"])
            with self.assertRaisesRegex(ValueError, "preserve provenance"):
                run_cycle(ROOT, output)

    def test_cycle_rejects_exit_zero_checker_without_valid_comparison(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from uft.cycles import run_cycle
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cycle"
            def fake_process(command, **kwargs):
                artifact = Path(command[command.index("--output") + 1])
                write_json(artifact, {"passed": True})
                return SimpleNamespace(returncode=0, stdout="", stderr="")
            with patch("uft.cycles.subprocess.run", side_effect=fake_process):
                result = run_cycle(ROOT, output)
            self.assertFalse(result["successful"])
            self.assertFalse(result["executions"][1]["comparison_verified"])

    def test_programme_team_has_explicit_lqg_physics_role(self):
        from genius.catalogue import load_profiles
        from uft.teams import select_research_team
        profiles = load_profiles(ROOT / "institute/registry/profiles.jsonl")
        result = select_research_team(profiles, "LQG relational time", programme="quantum_gravity")
        physics = next(a for a in result["assignments"] if a["role"] == "physics")
        self.assertTrue(physics["profile_id"].startswith("G5K-LQG-"))
        self.assertEqual(len(result["selected_profiles"]), 7)
        self.assertEqual(result["actual_llm_executions"], 0)


if __name__ == "__main__":
    unittest.main()
