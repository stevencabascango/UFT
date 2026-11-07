"""Adversarial acceptance tests for the integrated research store.

Fixtures exercise workflow enforcement, not physics or scientific competence.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from genius.memory import ScientificMemory
from uft.schema import ASSESSMENT_STATES, COHERENCE_CHECKS, COVERAGE_STATES, CRITERIA
from uft.store import ResearchStore


def entity(identifier="A", *, dependencies=None, status="proposal", statement=None, **extra):
    return {"id": identifier, "kind": "hypothesis", "objectives": ["quantum_gravity"],
            "statement": statement or f"Precise scoped assertion {identifier}",
            "hypotheses": ["Finite dimensional test case"], "evidence": [],
            "dependencies": dependencies or [], "status": status, "review": None, **extra}


def link(identifier="L", source="A", target="B", relation="dependency", **extra):
    return {"id": identifier, "source": source, "target": target, "relation": relation,
            "map": "Map the input state to the same labelled state in the target construction",
            "foundation": "The target statement explicitly uses the source hypothesis",
            "hypotheses": ["Common finite-dimensional domain"], "sources": ["local fixture definition"],
            "review": {"status": "pending", "limitations": "Fixture only"}, "status": "proposed", **extra}


def coherence():
    return {key: {"passed": True, "justification": f"Explicit scoped fixture justification for {key}"}
            for key in COHERENCE_CHECKS}


class ResearchStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = ResearchStore(self.root / "research.sqlite")

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def add_chain(self):
        self.store.upsert_entity(entity("A"))
        self.store.upsert_entity(entity("B", dependencies=["A"]))
        self.store.upsert_entity(entity("C", dependencies=["B"]))

    def test_entity_required_fields_vocabulary_and_unique_ids(self):
        self.store.upsert_entity(entity())
        repeated = self.store.upsert_entity(entity())
        self.assertFalse(repeated["changed"])
        self.assertEqual(len(self.store.snapshot()["entities"]), 1)
        bad = entity("B")
        bad.pop("review")
        with self.assertRaises(ValueError):
            self.store.upsert_entity(bad)
        for extra in ({"kind": "genius"}, {"objectives": ["administration"]}, {"hypotheses": "assumptions"}):
            with self.assertRaises(ValueError):
                self.store.upsert_entity(entity("B", **extra))

    def test_status_labels_normalized_and_no_automatic_strong_promotion(self):
        stored = self.store.upsert_entity(entity(status="CONJETURA"))["entity"]
        self.assertEqual(stored["status"], "conjecture")
        for status in ("proven", "formal"):
            with self.assertRaisesRegex(ValueError, "audited ScientificMemory"):
                self.store.upsert_entity(entity("B", status=status))
        with self.assertRaisesRegex(ValueError, "verified identified source"):
            self.store.upsert_entity(entity("B", status="established", sources=["I recall a theorem"]))

    def test_established_requires_exact_consulted_source(self):
        source = {"id": "REF-1", "verified": True, "result_used": "Finite-dimensional spectral theorem"}
        self.store.upsert_entity(entity(status="established", sources=[source]))
        self.assertEqual(self.store.get("A")["status"], "established")

    def test_obvious_duplicate_detection_preserves_separate_hypotheses(self):
        self.store.upsert_entity(entity(statement="Shared statement."))
        result = self.store.upsert_entity(entity("B", statement=" SHARED   statement "))
        self.assertEqual(result["duplicates"], ["A"])
        self.assertEqual(len(self.store.snapshot()["alerts"]), 1)
        self.assertEqual(self.store.snapshot()["alerts"][0]["kind"], "operational")

    def test_dependencies_must_exist_and_remain_acyclic(self):
        with self.assertRaises(KeyError):
            self.store.upsert_entity(entity(dependencies=["MISSING"]))
        self.add_chain()
        with self.assertRaisesRegex(ValueError, "Circular"):
            self.store.upsert_entity(entity("A", dependencies=["C"]))
        self.assertEqual(self.store.get("A")["dependencies"], [])

    def test_dependency_change_invalidates_transitive_results_and_assessments(self):
        self.add_chain()
        self.store.set_coverage("C", "mathematical", "Definitions", "reviewed", "Compared explicit definitions", ["fixture.txt"])
        self.store.set_assessment("C", "mathematical_coherence", "fulfilled", ["fixture.txt"], "Only this model", "Check global case")
        self.store.add_link(link("L-AB"))
        result = self.store.upsert_entity(entity("A", statement="Corrected convention for A"))
        self.assertEqual(result["affected"], ["B", "C"])
        self.assertEqual([self.store.get(k)["status"] for k in ("A", "B", "C")], ["review"] * 3)
        snapshot = self.store.snapshot()
        self.assertEqual(snapshot["coverage"][0]["status"], "Pendiente")
        self.assertEqual(snapshot["assessments"][0]["status"], "Pendiente")
        self.assertEqual(snapshot["links"][0]["status"], "review")
        self.assertEqual(len([a for a in snapshot["alerts"] if a["kind"] == "scientific"]), 1)

    def test_refuted_cannot_be_laundered_through_review_and_preserves_negative_status(self):
        self.add_chain()
        rejected = entity("B", dependencies=["A"], status="refuted", evidence=["Explicit counterexample: the third eigenvalue is negative"])
        self.store.upsert_entity(rejected)
        for status in ("review", "pending_audit", "proposal", "proven"):
            with self.assertRaises(ValueError):
                self.store.upsert_entity(entity("B", dependencies=["A"], status=status, evidence=rejected["evidence"]))
        self.store.upsert_entity(entity("A", statement="A changed again"))
        self.assertEqual(self.store.get("B")["status"], "refuted")
        self.assertEqual(self.store.get("C")["status"], "review")

    def test_changed_connection_hypothesis_invalidates_target_and_descendants(self):
        self.add_chain()
        self.store.add_link(link("CHANGING"))
        self.store.set_coverage("C", "physical", "Dimensions", "reviewed", "Fixture dimensions checked", ["fixture"])
        self.store.set_assessment("C", "correspondence", "fulfilled", ["fixture"], "Fixture only", "General case")
        changed = link("CHANGING", hypotheses=["A new nontrivial boundary assumption"])
        actual = self.store.add_link(changed)
        self.assertEqual(self.store.get("B")["status"], "review")
        self.assertEqual(self.store.get("C")["status"], "review")
        self.assertEqual(actual["status"], "review")
        self.assertEqual(self.store.snapshot()["coverage"][0]["status"], "Pendiente")
        self.assertEqual(self.store.snapshot()["assessments"][0]["status"], "Pendiente")

    def test_link_endpoints_cannot_change_by_turning_off_propagation(self):
        self.add_chain()
        self.store.add_link(link("IMMUTABLE"))
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.store.add_link(link("IMMUTABLE", source="A", target="C", relation="analogy", propagates=False))

    def test_rejecting_propagating_link_invalidates_dependent_results(self):
        self.add_chain()
        self.store.add_link(link("RETRACTED"))
        result = self.store.add_link(link("RETRACTED", status="rejected"))
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(self.store.get("B")["status"], "review")
        self.assertEqual(self.store.get("C")["status"], "review")

    def test_evidence_files_hashes_are_checked(self):
        path = self.root / "calculation.txt"
        path.write_text("Exact calculation", encoding="utf-8")
        stored = self.store.upsert_entity(entity(status="evidence", evidence=[{"path": str(path)}]))["entity"]
        evidence = copy.deepcopy(stored["evidence"])
        path.write_text("Changed calculation", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Evidence file changed"):
            self.store.upsert_entity(entity("B", status="evidence", evidence=evidence))

    def test_validated_dependency_cannot_silently_rely_on_refuted_result(self):
        self.store.upsert_entity(entity(status="refuted", evidence=["Counterexample documented"]))
        with self.assertRaisesRegex(ValueError, "Unresolved/refuted dependency"):
            self.store.upsert_entity(entity("B", dependencies=["A"], status="evidence", evidence=["Numerical output"]))

    def test_typed_link_rejects_missing_map_sources_and_cycles(self):
        self.add_chain()
        bad = link()
        bad["map"] = ""
        with self.assertRaises(ValueError):
            self.store.add_link(bad)
        with self.assertRaisesRegex(ValueError, "Circular"):
            self.store.add_link(link("L-CA", source="C", target="A"))
        record = self.store.add_link(link())
        self.assertTrue(record["changed"])
        self.assertFalse(self.store.add_link(link())["changed"])

    def test_analogy_does_not_establish_equivalence_or_propagate_by_default(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity("B"))
        result = self.store.add_link(link(relation="analogy"))
        self.assertFalse(result["propagates"])
        self.store.upsert_entity(entity(statement="Changed source interpretation"))
        self.assertEqual(self.store.get("B")["status"], "proposal")
        self.assertEqual(self.store.snapshot()["links"][0]["status"], "review")

    def test_level_b_transfer_carries_conditions_and_source_invalidation(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity("B", conditional_on=["A"]))
        self.store.add_link(link(transfer_level="B", coherence=coherence()))
        with self.assertRaises(ValueError):
            self.store.upsert_entity(entity("C", conditional_on=["A"], status="established", sources=[{"id": "R", "verified": True, "result_used": "Claim"}]))
        changed = self.store.upsert_entity(entity(status="refuted", evidence=["Actual counterexample"]))
        self.assertIn("B", changed["affected"])
        self.assertEqual(self.store.get("B")["status"], "review")

    def test_conditional_premises_cannot_be_erased_in_a_second_revision(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity("B", conditional_on=["A"]))
        with self.assertRaisesRegex(ValueError, "cannot be erased"):
            self.store.upsert_entity(entity("B"))
        self.assertEqual(self.store.get("B")["conditional_on"], ["A"])

    def test_level_a_preserves_explicit_source_hypotheses_without_claiming_equivalence(self):
        source = {"id": "REF-1", "verified": True, "result_used": "Finite-dimensional spectral theorem"}
        self.store.upsert_entity(entity(status="established", sources=[source]))
        self.store.upsert_entity(entity("B"))
        record = self.store.add_link(link(transfer_level="A", coherence=coherence()))
        self.assertEqual(record["hypotheses"], ["Common finite-dimensional domain"])
        self.assertEqual(record["relation"], "dependency")
        self.assertEqual(self.store.get("B")["status"], "proposal")

    def test_transfer_requires_all_six_checks_and_honest_category(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity("B"))
        with self.assertRaisesRegex(ValueError, "explicitly declare conditional_on"):
            self.store.add_link(link(transfer_level="B", coherence=coherence()))
        with self.assertRaisesRegex(ValueError, "Level A requires"):
            self.store.add_link(link(transfer_level="A", coherence=coherence()))
        for key in COHERENCE_CHECKS:
            checks = coherence()
            checks[key]["passed"] = False
            with self.subTest(check=key), self.assertRaisesRegex(ValueError, "coherence check"):
                self.store.add_link(link(transfer_level="A", coherence=checks))
        with self.assertRaisesRegex(ValueError, "not result transfers"):
            self.store.add_link(link(relation="analogy", transfer_level="A", propagates=True, coherence=coherence()))

    def test_coverage_and_seven_criteria_do_not_invent_evidence(self):
        self.store.upsert_entity(entity())
        with self.assertRaisesRegex(ValueError, "concrete evidence"):
            self.store.set_coverage("A", "physical", "Measurements", "reviewed", "No evidence")
        with self.assertRaises(ValueError):
            self.store.set_assessment("A", "mathematical_coherence", "fulfilled", [], "Finite scope", "Try an example")
        for criterion in CRITERIA:
            self.store.set_assessment("A", criterion, "pending", [], "No evaluation executed", "Run the relevant scoped check")
        self.assertEqual(len(self.store.snapshot()["assessments"]), 7)
        self.assertEqual(len(COVERAGE_STATES), 5)
        self.assertEqual(len(ASSESSMENT_STATES), 5)
        with self.assertRaises(ValueError):
            self.store.set_assessment("A", "testability", "not_applicable", [], "Mathematical object only", "Document physical dictionary")

    def test_event_intake_is_idempotent_and_quiet_on_no_change(self):
        event = {"id": "I1", "source": "local:goals", "version": "1", "entity": entity()}
        first = self.store.ingest(event)
        before = self.store.snapshot()
        repeat = self.store.ingest(event)
        self.assertTrue(first["changed"])
        self.assertTrue(repeat["idempotent"])
        self.assertEqual(before, self.store.snapshot())
        observation = self.store.ingest({**event, "id": "I2", "version": "2"})
        self.assertFalse(observation["changed"])
        self.assertEqual(self.store.snapshot()["alerts"], [])
        with self.assertRaisesRegex(ValueError, "event ID cannot be reused"):
            self.store.ingest({**event, "version": "3"})

    def test_event_rolls_back_batch_and_recovers_when_missing_dependency_arrives(self):
        event = {"id": "I1", "source": "fixture", "version": "1", "entities": [entity("B"), entity("C", dependencies=["MISSING"])]}
        failed = self.store.ingest(event)
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(self.store.snapshot()["entities"], [])
        self.store.upsert_entity(entity("MISSING"))
        recovered = self.store.recover("I1")
        self.assertEqual(recovered["status"], "completed")
        self.assertEqual(recovered["attempts"], 2)
        self.assertEqual(len(self.store.snapshot()["entities"]), 3)

    def test_failures_have_bounded_retries_and_deduplicated_alerts(self):
        event = {"id": "I1", "source": "fixture", "version": "1", "entity": entity(dependencies=["MISSING"])}
        self.assertEqual(self.store.ingest(event, max_attempts=2)["status"], "failed")
        self.assertEqual(self.store.recover("I1")["status"], "exhausted")
        self.assertEqual(self.store.recover("I1")["attempts"], 2)
        self.assertEqual(len(self.store.snapshot()["alerts"]), 1)
        self.assertEqual(self.store.snapshot()["events"][0]["attempts"], 2)

    def test_explicit_contradiction_has_traceable_alert_without_automatic_refutation(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity("B", contradicts=["A"], evidence=["Competing scoped assertion"]))
        alert = self.store.snapshot()["alerts"][0]
        self.assertEqual(alert["scientific_status"], "review")
        self.assertEqual(self.store.get("A")["status"], "proposal")
        self.assertEqual(alert["analysis"], "B")

    def test_cross_model_comparison_remains_pending_if_report_missing(self):
        path = self.root / "codex.md"
        path.write_text("Actual report", encoding="utf-8")
        record = self.store.record_comparison("CROSS-1", codex=path)
        self.assertEqual(record["status"], "pending")
        self.assertEqual(record["missing"], ["claude"])
        other = self.root / "claude.md"
        other.write_text("Another actual report", encoding="utf-8")
        ready = self.store.record_comparison("CROSS-1", codex=path, claude=other, disagreements=["An unresolved convention"])
        self.assertEqual(ready["status"], "ready_for_cross_review")
        self.assertFalse(ready["reviewed"])
        self.assertEqual(ready["disagreements"], ["An unresolved convention"])
        with self.assertRaises(ValueError):
            self.store.record_comparison("BAD", codex=path, claude=path)

    def test_snapshot_export_is_portable_and_history_append_only(self):
        self.store.upsert_entity(entity())
        self.store.upsert_entity(entity(statement="Corrected A with recorded uncertainty"))
        export = self.root / "snapshot.json"
        result = self.store.export(export)
        self.assertEqual(json.loads(export.read_text()), json.loads(json.dumps(result)))
        self.assertEqual([h["action"] for h in result["history"]], ["entity_created", "entity_revised"])
        self.assertEqual(result["entities"][0]["revision"], 2)
        self.assertEqual(len(result["entities"][0]["content_sha256"]), 64)
        self.store.close()
        self.store = ResearchStore(self.root / "research.sqlite")
        self.assertEqual(self.store.snapshot()["entities"], result["entities"])

    def test_forged_audited_claim_cannot_enter_through_import(self):
        with ScientificMemory(self.root / "core.sqlite") as core:
            core.add({"id": "A", "statement": "Proposed only", "hypotheses": [], "sources": [], "artifacts": [], "dependencies": []})
            with self.assertRaisesRegex(ValueError, "GENIUS audit gate"):
                self.store.import_claim(core, "A", objectives=["quantum_gravity"])
            # A changed SQL row still lacks the independent execution audit.
            forged = core.get("A")
            forged["status"] = "proven"
            core.db.execute("UPDATE claims SET status='proven',data=? WHERE id='A'", (json.dumps(forged),))
            core.db.commit()
            with self.assertRaisesRegex(ValueError, "Missing confirming audit"):
                self.store.import_claim(core, "A", objectives=["quantum_gravity"])

    def test_real_core_audit_gate_import_and_evidence_tampering(self):
        proof = self.root / "fixture-proof.txt"
        proof.write_text("Test-only finite assertion and reconstruction, not a research result", encoding="utf-8")
        with ScientificMemory(self.root / "core.sqlite") as core:
            for identifier, role in (("producer", "mathematics"), ("reviewer", "audit")):
                record = self.root / f"{identifier}-completion.json"
                record.write_text(json.dumps({"execution_id": identifier, "role": role,
                                              "backend": "test_fixture", "execution_status": "completed"}))
                core.register_execution(record)
            core.add({"id": "A", "statement": "Scoped fixture theorem", "hypotheses": ["Fixture only"],
                      "sources": [], "artifacts": [str(proof)], "dependencies": [], "status": "pending_audit"})
            checks = {key: True for key in ("statement", "hypotheses", "logic", "dependencies", "conventions", "limits", "physical_scope", "tool_scope")}
            core.audit("A", audit_id="AUDIT-1", verdict="confirmed", producer_execution="producer",
                       reviewer_execution="reviewer", checks=checks, artifacts=[str(proof)],
                       limitations="Workflow fixture, not an actual scientific audit")
            core.promote("A", "proven", audit_id="AUDIT-1")
            result = self.store.import_claim(core, "A", objectives=["quantum_gravity"])
            self.assertEqual(result["entity"]["status"], "proven")
            self.assertEqual(result["entity"]["review"]["scope"], "internal")
            self.assertNotEqual(result["entity"]["review"]["producer_execution"], result["entity"]["review"]["reviewer_execution"])
            proof.write_text("Changed after audit", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "evidence changed"):
                self.store.import_claim(core, "A", objectives=["quantum_gravity"])


if __name__ == "__main__":
    unittest.main()
