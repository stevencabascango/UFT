"""Independent audit must detect consequential changes in finite evidence."""
from copy import deepcopy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("uft_independent_audit", ROOT / "scripts/independent_science_audit.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class IndependentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reconstruction = audit.run_audit()
        cls.producer = json.loads((ROOT / "research/calculations/first_cycle.json").read_text(encoding="utf-8"))

    def test_exact_highest_weight_rank_and_swap_method(self):
        gauss = self.reconstruction["quantum_gravity"]["gauss"]
        self.assertEqual(gauss["raising_rank"], 4)
        self.assertEqual(gauss["invariant_dimension"], 2)
        self.assertTrue(self.reconstruction["quantum_gravity"]["q"]["preserves_gauss_exact"])

    def test_optional_producer_comparison_confirms_reconstructed_outputs(self):
        compared = audit.compare_producer(self.producer, self.reconstruction)
        self.assertTrue(compared["passed"])
        self.assertGreaterEqual(len(compared["checks"]), 9)

    def test_wrong_q_sign_is_detected_even_though_square_is_unchanged(self):
        altered = deepcopy(self.producer)
        for i in range(2):
            for j in range(2):
                entry = altered["quantum_gravity"]["q_restricted_nonorthonormal"][i][j]
                entry["imag"] = str(-Fraction(entry["imag"]))
        compared = audit.compare_producer(altered, self.reconstruction)
        self.assertFalse(compared["passed"])
        self.assertTrue(compared["checks"]["q_squared"])
        self.assertFalse(compared["checks"]["q_sign_and_coordinates"])

    def test_wrong_gauss_dimension_is_detected_without_trusting_label(self):
        altered = deepcopy(self.producer)
        altered["quantum_gravity"]["invariant_dimension"] = 3
        self.assertFalse(audit.compare_producer(altered, self.reconstruction)["checks"]["gauss_dimension"])

    def test_omitting_mixed_correction_leaves_nonzero_obstruction(self):
        self.assertEqual(audit.mixed_mc_residual(), {})
        self.assertEqual(audit.mixed_mc_residual(correction=0), {"w:e^1:n^1": "1"})
        self.assertEqual(audit.mixed_mc_residual(primitive=False, correction=-200), {"w:e^1:n^1": "1"})

    def test_falsely_declared_mixed_solution_is_rejected(self):
        altered = deepcopy(self.producer)
        altered["googly"]["cases"][1]["mixed_extension_exists"] = True
        self.assertFalse(audit.compare_producer(altered, self.reconstruction)["checks"]["mixed_extension_obstructed"])

    def test_jacobi_witness_detects_false_antisymmetry_sufficiency(self):
        u = self.reconstruction["unification"]
        self.assertTrue(u["counterexample"]["delta_invariant"])
        self.assertEqual(u["counterexample"]["jacobi_123"], ["0", "0", "0", "0", "-1"])
        altered = deepcopy(self.producer)
        altered["unification"]["bad"]["witness"]["residual"] = [0] * 5
        self.assertFalse(audit.compare_producer(altered, self.reconstruction)["passed"])

    def test_refuted_claim_cannot_be_relabelled_as_proven_in_evidence(self):
        altered = deepcopy(self.producer)
        altered["unification"]["false_claim_status"] = "DEMOSTRADO"
        self.assertFalse(audit.compare_producer(altered, self.reconstruction)["checks"]["counterexamples_stay_refuted"])

    def test_malformed_producer_is_rejected_with_a_record(self):
        compared = audit.compare_producer({}, self.reconstruction)
        self.assertFalse(compared["passed"])
        self.assertIn("Malformed", compared["error"])
        altered = deepcopy(self.producer)
        altered["quantum_gravity"]["gram"] = []
        compared = audit.compare_producer(altered, self.reconstruction)
        self.assertFalse(compared["passed"])
        self.assertIn("Malformed", compared["error"])

    def test_audit_evidence_is_portable_and_scoped(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "audit.json"
            result = audit.run_audit(path, ROOT / "research/calculations/first_cycle.json")
            self.assertTrue(result["passed"])
            self.assertEqual(json.loads(path.read_text()), result)
            self.assertEqual(result["review_scope"], "internal")
            self.assertIn("zero", result["quantum_gravity"]["clock"]["kinematic_L2_kernel"])


if __name__ == "__main__":
    unittest.main()
