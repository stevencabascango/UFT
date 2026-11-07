"""Scientific regression tests for three deliberately restricted examples."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "science_examples.py"
SPEC = importlib.util.spec_from_file_location("science_examples_uft", PATH)
science = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = science
SPEC.loader.exec_module(science)


class ScienceExamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = science.run_examples()

    def test_spin_closure_and_hamiltonian_preserve_gauss(self):
        q = self.result["quantum_gravity"]
        self.assertTrue(q["gauss_annihilates_basis"])
        self.assertTrue(q["q_preserves_invariant_subspace"])
        self.assertEqual(q["gram"][1][1]["real"], "3")

    def test_exact_spectrum_and_nonorthogonal_metric(self):
        q = self.result["quantum_gravity"]
        self.assertTrue(q["q_full_hermitian"])
        self.assertTrue(q["weighted_hermiticity"])
        self.assertTrue(q["q_squared_equals_3_over_16_identity"])
        self.assertEqual(q["q_restricted_nonorthonormal"][0][1]["imag"], "-3/4")
        self.assertEqual(q["q_restricted_nonorthonormal"][1][0]["imag"], "1/4")

    def test_unitarity_counterexample_is_not_marked_proven(self):
        q = self.result["quantum_gravity"]
        self.assertEqual(q["quarter_period_norm_squared"], "1")
        self.assertEqual(q["nonhermitian_counterexample"]["status"], "REFUTADO")
        self.assertNotEqual(Fraction(q["nonhermitian_counterexample"]
                                     ["derivative_dimensionless_time_at_zero"]), 0)
        self.assertFalse(q["clock_turning_point"]["global_clock"])

    def test_mixed_sector_obstruction_not_erased_by_individual_solutions(self):
        exact, blocked = self.result["googly"]["cases"]
        self.assertEqual(exact["mixed_mc_residual"], "0")
        self.assertEqual(exact["H2_dimension"], 0)
        self.assertTrue(exact["mixed_extension_exists"])
        self.assertEqual(blocked["mixed_mc_residual"], "1")
        self.assertEqual(blocked["H2_dimension"], 1)
        self.assertFalse(blocked["mixed_extension_exists"])

    def test_antisymmetric_metric_compatible_bracket_can_fail_jacobi(self):
        u = self.result["unification"]
        self.assertTrue(u["good"]["Jacobi_holds"])
        self.assertTrue(u["bad"]["delta_invariant"])
        self.assertFalse(u["bad"]["Jacobi_holds"])
        self.assertEqual(u["bad"]["witness"]["residual"], [0, 0, 0, 0, -1])
        self.assertEqual(u["false_claim_status"], "REFUTADO")

    def test_independent_algebra_contraction_finds_all_bad_residuals(self):
        constants = science.structure_constants(5, [(0, 1, 2), (0, 3, 4)])
        residuals = science.jacobi_residual(5, constants)
        self.assertEqual(len(residuals), 24)
        self.assertTrue(all(any(w["residual"]) for w in residuals))

    def test_calculation_evidence_serializes_and_has_honest_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "evidence.json"
            result = science.run_examples(output)
            self.assertEqual(json.loads(output.read_text()), result)
            self.assertFalse(result["llm_execution"])
            self.assertIn("Einstein dynamics", result["quantum_gravity"]["physical_claims_not_established"])
            self.assertIn("no twistor-to-Einstein", result["googly"]["scope"])

    def test_gaussian_rational_arithmetic_has_no_rounding(self):
        a = science.Gaussian(Fraction(1, 3), Fraction(2, 7))
        b = a * a.conjugate()
        self.assertEqual(b.imag, Fraction(0))
        self.assertEqual(b.real, Fraction(1, 9) + Fraction(4, 49))


if __name__ == "__main__":
    unittest.main()
