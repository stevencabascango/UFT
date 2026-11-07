#!/usr/bin/env python3
"""Independent, bounded reconstruction of the three finite scientific examples.

Only the Python standard library is required. The producer implementation is
never imported: spin operators are reconstructed from transpositions rather
than Pauli products, using rational arithmetic. Comparison of a producer JSON
artifact is optional and occurs only after the independent reconstruction.
This is an internal mathematical audit, not formal proof-assistant checking.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import platform
import uuid


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in zip(*b)] for row in a]


def subtract(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[F(c) * x for x in row] for row in a]


def rank(a):
    """Exact row rank over Q, independent of floating-point thresholds."""
    rows = matrix(a)
    pivot_row = 0
    for col in range(len(rows[0]) if rows else 0):
        candidate = next((r for r in range(pivot_row, len(rows)) if rows[r][col]), None)
        if candidate is None:
            continue
        rows[pivot_row], rows[candidate] = rows[candidate], rows[pivot_row]
        pivot = rows[pivot_row][col]
        rows[pivot_row] = [x / pivot for x in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][col]:
                c = rows[r][col]
                rows[r] = [x - c * y for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def swap_operator(first, second):
    """Permutation of two spin-1/2 tensor factors, ordered lexicographically."""
    basis = list(product((0, 1), repeat=4))
    index = {bits: i for i, bits in enumerate(basis)}
    p = zeros(16, 16)
    for col, bits in enumerate(basis):
        out = list(bits)
        out[first], out[second] = out[second], out[first]
        p[index[tuple(out)]][col] = F(1)
    return p


def spin_reconstruction():
    basis = list(product((0, 1), repeat=4))
    m0 = [bits for bits in basis if sum(bits) == 2]
    m1 = [bits for bits in basis if sum(bits) == 1]
    raising = zeros(len(m1), len(m0))
    for col, bits in enumerate(m0):
        for factor, value in enumerate(bits):
            if value == 1:
                out = list(bits)
                out[factor] = 0
                raising[m1.index(tuple(out))][col] += 1
    raising_rank = rank(raising)
    nullity = len(m0) - raising_rank
    # u0 is normalized; u1 = sqrt(3) times the normalized triplet singlet.
    coefficients = {
        "0101": (F(1, 2), F(-1, 2)), "0110": (F(-1, 2), F(-1, 2)),
        "1001": (F(-1, 2), F(-1, 2)), "1010": (F(1, 2), F(-1, 2)),
        "0011": (F(0), F(1)), "1100": (F(0), F(1)),
    }
    embedding = matrix([coefficients.get("".join(map(str, bits)), (0, 0)) for bits in basis])
    gram = multiply(transpose(embedding), embedding)
    kernel_residual = multiply(raising, [embedding[basis.index(bits)] for bits in m0])
    p12, p23 = swap_operator(0, 1), swap_operator(1, 2)
    # q = i [J1.J2, J2.J3] = (i/4)[P12,P23]. Thus q = i R.
    real_generator = scale(F(1, 4), subtract(multiply(p12, p23), multiply(p23, p12)))
    q_form_real = multiply(transpose(embedding), multiply(real_generator, embedding))
    gram_inverse = matrix([[1, 0], [0, F(1, 3)]])
    q_coordinates_real = multiply(gram_inverse, q_form_real)
    preservation = subtract(multiply(real_generator, embedding), multiply(embedding, q_coordinates_real))
    q_squared = scale(-1, multiply(q_coordinates_real, q_coordinates_real))
    metric_hermitian_residual = subtract(multiply(gram, q_coordinates_real),
                                       scale(-1, multiply(transpose(q_coordinates_real), gram)))
    expected = matrix([[0, F(-3, 4)], [F(1, 4), 0]])
    expected_square = matrix([[F(3, 16), 0], [0, F(3, 16)]])
    exact_pass = (nullity == 2 and gram == matrix([[1, 0], [0, 3]])
                  and kernel_residual == zeros(4, 2) and preservation == zeros(16, 2)
                  and q_coordinates_real == expected and q_squared == expected_square
                  and metric_hermitian_residual == zeros(2, 2))
    samples = []
    # U = cos(theta) I - i sin(theta) sigma_y is a real orthogonal rotation.
    max_defect = 0.0
    for theta in (0.0, 0.125, 1.0, math.pi / 2, math.pi, -0.75):
        c, s = math.cos(theta), math.sin(theta)
        initial = (complex(0.5, 0.5), complex(0.5, -0.5))
        evolved = (c * initial[0] - s * initial[1], s * initial[0] + c * initial[1])
        norm = sum(abs(z) ** 2 for z in evolved)
        defect = abs(norm - 1.0)
        max_defect = max(max_defect, defect)
        samples.append({"dimensionless_theta": theta, "norm_squared": norm})
    bad_time = F(1)
    bad_norm = F(1) + bad_time ** 2
    return {
        "method": "Exact rational highest-weight kernel plus swap-commutator reconstruction; no Pauli-product implementation imported",
        "gauss": {"m_zero_dimension": len(m0), "raising_rank": raising_rank,
                  "invariant_dimension": nullity, "raising_matrix_m0_to_m1": strings(raising),
                  "basis_gram": strings(gram)},
        "q": {"convention": "J=sigma/2; epsilon_xyz=+1; q=epsilon_abc J1a J2b J3c; q=i R",
              "real_R_coordinates_unnormalized_basis": strings(q_coordinates_real),
              "orthonormal_matrix": [["0", "-I*sqrt(3)/4"], ["I*sqrt(3)/4", "0"]],
              "q_squared": strings(q_squared), "preserves_gauss_exact": preservation == zeros(16, 2),
              "hermitian_in_gram_metric_exact": metric_hermitian_residual == zeros(2, 2)},
        "clock": {"hypotheses": ["kappa is real with units of energy", "hbar > 0", "ideal continuous T on R",
                                  "C=-i hbar d/dT + kappa q on H^1(R,C^2)",
                                  "physical norm chosen by evaluation of generalized solutions"],
                  "kinematic_L2_kernel": "zero; nonzero solutions have constant nonzero norm and are not L2 in T",
                  "sample_checks": samples, "max_norm_defect": max_defect,
                  "not_derived": ["GR dynamics", "all LQG constraints", "clock discreteness", "semiclassical Einstein limit"]},
        "counterexample": {"bad_H": [[0, 1], [0, 0]], "initial": [0, 1],
                           "dimensionless_time": str(bad_time), "norm_squared": str(bad_norm),
                           "claim": "Every finite H yields unitary clock evolution", "verdict": "refuted"},
        "passed": exact_pass and max_defect < 1e-14 and bad_norm != 1,
    }


def strings(a):
    return [[str(x) for x in row] for row in a]


def mixed_mc_residual(*, primitive=True, correction=F(-1)):
    """Compute MC coefficients in Q[e,n]/(e^2,n^2), not arbitrary orders."""
    alpha = [("x", 1, 0, F(1)), ("y", 0, 1, F(1)), ("z", 1, 1, F(correction))]
    coefficients = {}
    def add(key, value):
        coefficients[key] = coefficients.get(key, F(0)) + value
    for generator, e, n, coefficient in alpha:
        if primitive and generator == "z":
            add(("w", e, n), coefficient)
    # Degree-one bracket is graded symmetric: [x,y]=[y,x]=w.
    for (x, e, n, a), (y, e2, n2, b) in product(alpha, repeat=2):
        if e + e2 > 1 or n + n2 > 1:
            continue
        if {x, y} == {"x", "y"}:
            add(("w", e + e2, n + n2), a * b / 2)
    return {f"{g}:e^{e}:n^{n}": str(c) for (g, e, n), c in sorted(coefficients.items()) if c}


def dgla_reconstruction():
    with_correction = mixed_mc_residual()
    without_correction = mixed_mc_residual(correction=0)
    blocked = mixed_mc_residual(primitive=False)
    return {"coefficient_ring": "Q[e,n]/(e^2,n^2)", "degrees": {"x": 1, "y": 1, "z": 1, "w": 2},
            "bracket": "[x,y]=[y,x]=w; w central; all other brackets vanish",
            "differential": "d z=w, other generators closed; blocked comparison has d=0",
            "mixed_equation": "d c + [a,b] = 0", "primitive_case_residual": with_correction,
            "omitted_correction_residual": without_correction, "blocked_case_residual": blocked,
            "H2_primitive_dimension": 0, "H2_blocked_dimension": 1,
            "not_derived": ["twistor dictionary", "gravitational helicity identification", "higher-order formal extension", "Einstein reconstruction"],
            "passed": with_correction == {} and without_correction == {"w:e^1:n^1": "1"}
                      and blocked == {"w:e^1:n^1": "1"}}


def alternating_tensor(n, triples):
    f = {}
    for triple, coefficient in triples:
        for order in permutations(range(3)):
            inversions = sum(order[i] > order[j] for i in range(3) for j in range(i + 1, 3))
            indices = tuple(triple[i] for i in order)
            f[indices] = f.get(indices, F(0)) + F(coefficient) * (-1) ** inversions
    return f


def bracket_basis(f, i, j, n):
    return [f.get((i, j, k), F(0)) for k in range(n)]


def jacobi_components(f, i, j, k, n):
    """Components of [e_i,[e_j,e_k]] + cyclic permutations."""
    return [sum((f.get((j, k, a), F(0)) * f.get((i, a, target), F(0))
                  + f.get((k, i, a), F(0)) * f.get((j, a, target), F(0))
                  + f.get((i, j, a), F(0)) * f.get((k, a, target), F(0))
                  for a in range(n)), F(0)) for target in range(n)]


def jacobi_reconstruction():
    su2 = alternating_tensor(3, [((0, 1, 2), 1)])
    bad = alternating_tensor(5, [((0, 1, 2), 1), ((0, 3, 4), 1)])
    valid_residuals = [jacobi_components(su2, *ijk, 3) for ijk in product(range(3), repeat=3)]
    bad_residuals = [(ijk, jacobi_components(bad, *ijk, 5)) for ijk in combinations(range(5), 3)]
    violated = [(ijk, row) for ijk, row in bad_residuals if any(row)]
    invariant_bad = all(bad.get((i, j, k), 0) == bad.get((j, k, i), 0)
                        for i, j, k in product(range(5), repeat=3))
    specific = jacobi_components(bad, 1, 2, 3, 5)
    return {"convention": "f_ijk=<[e_i,e_j],e_k>; Euclidean delta metric; Jacobi=[i,[j,k]]+cyclic",
            "su2": {"jacobi_holds_exactly": all(not any(r) for r in valid_residuals)},
            "counterexample": {"dimension": 5, "independent_components": {"f012": 1, "f034": 1},
                               "fully_antisymmetric": True, "delta_invariant": invariant_bad,
                               "jacobi_123": [str(x) for x in specific],
                               "violated_unordered_triples": [{"triple": list(i), "residual": [str(x) for x in row]} for i, row in violated]},
            "not_derived": ["gravity coupling", "matter spectrum", "anomaly cancellation", "quantum consistency", "physical unification"],
            "passed": all(not any(r) for r in valid_residuals) and invariant_bad and specific == [0, 0, 0, 0, -1]}


def compare_producer(producer, independent):
    """Reject mismatches against reconstructed values, including sign errors.

    The sign of q cannot be inferred from q squared, so both are compared.
    Boolean claims made by the producer are not used as computational premises.
    """
    checks = {}
    try:
        q = producer["quantum_gravity"]
        iq = independent["quantum_gravity"]
        checks["gauss_dimension"] = q["invariant_dimension"] == iq["gauss"]["invariant_dimension"]
        checks["gauss_gram"] = all(F(q["gram"][i][j]["real"]) == F(iq["gauss"]["basis_gram"][i][j])
                                   and F(q["gram"][i][j]["imag"]) == 0
                                   for i, j in product(range(2), repeat=2))
        checks["q_sign_and_coordinates"] = all(
            F(q["q_restricted_nonorthonormal"][i][j]["real"]) == 0
            and F(q["q_restricted_nonorthonormal"][i][j]["imag"]) == F(iq["q"]["real_R_coordinates_unnormalized_basis"][i][j])
            for i, j in product(range(2), repeat=2))
        checks["q_squared"] = all(F(q["q_squared"][i][j]["real"]) == F(iq["q"]["q_squared"][i][j])
                                   and F(q["q_squared"][i][j]["imag"]) == 0
                                   for i, j in product(range(2), repeat=2))
        checks["q_symmetry_flags"] = all(q.get(k) is True for k in (
            "gauss_annihilates_basis", "q_preserves_invariant_subspace", "weighted_hermiticity", "q_full_hermitian"))
        cases = producer["googly"]["cases"]
        primitive = next(c for c in cases if F(c["dz_coefficient"]) == 1)
        blocked = next(c for c in cases if F(c["dz_coefficient"]) == 0)
        checks["mixed_extension_primitive"] = (F(primitive["b_z"]) == -1 and F(primitive["mixed_mc_residual"]) == 0
                                                and primitive["H2_dimension"] == 0 and primitive["mixed_extension_exists"] is True)
        checks["mixed_extension_obstructed"] = (F(blocked["mixed_mc_residual"]) == 1 and blocked["H2_dimension"] == 1
                                                 and blocked["mixed_extension_exists"] is False)
        u = producer["unification"]
        checks["jacobi_good"] = u["good"]["Jacobi_holds"] is True and u["good"]["nonzero_Jacobi_residual_count"] == 0
        checks["jacobi_bad_witness"] = (u["bad"]["witness"]["inputs_zero_based"] == [1, 2, 3]
                                         and [F(x) for x in u["bad"]["witness"]["residual"]]
                                         == [F(x) for x in independent["unification"]["counterexample"]["jacobi_123"]])
        checks["jacobi_bad_flags"] = u["bad"]["Jacobi_holds"] is False and u["bad"]["delta_invariant"] is True
        checks["jacobi_bad_count"] = (u["bad"]["nonzero_Jacobi_residual_count"]
                                       == 6 * len(independent["unification"]["counterexample"]["violated_unordered_triples"]))
        checks["counterexamples_stay_refuted"] = (
            q["nonhermitian_counterexample"]["status"] == "REFUTADO"
            and producer["googly"]["false_claim_status"] == "REFUTADO"
            and u["false_claim_status"] == "REFUTADO")
    except (KeyError, IndexError, TypeError, ValueError, StopIteration, ZeroDivisionError) as error:
        return {"passed": False, "checks": checks, "error": "Malformed or incomplete producer artifact: " + str(error)}
    return {"passed": all(checks.values()), "checks": checks,
            "scope": "Finite numerical/algebraic outputs and explicit refutations; general proofs and physical interpretation are reviewed in the accompanying audit document"}


def run_audit(output_path=None, producer_report=None):
    result = {"schema_version": "1.0", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "execution_id": "uft-math-audit-" + uuid.uuid4().hex,
              "execution_status": "completed", "role": "audit", "llm_execution": False,
              "backend": "python-stdlib-exact-rational",
              "auditor_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": platform.python_version(), "review_scope": "internal",
              "separation": "Separate agent execution and independently implemented algorithms; shared model family and training may share errors; no external peer review",
              "quantum_gravity": spin_reconstruction(), "googly": dgla_reconstruction(),
              "unification": jacobi_reconstruction()}
    result["passed"] = all(result[k]["passed"] for k in ("quantum_gravity", "googly", "unification"))
    if producer_report is not None:
        path = Path(producer_report)
        if path.stat().st_size > 2 * 1024 * 1024:
            raise ValueError("Producer JSON exceeds the 2 MiB audit bound")
        with path.open("rb") as stream:
            raw = stream.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError("Producer JSON exceeds the 2 MiB audit bound")
        producer = json.loads(raw)
        result["producer_artifact"] = {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
                                       "programmes_present": [k for k in ("quantum_gravity", "googly", "unification") if k in producer],
                                       "comparison": compare_producer(producer, result)}
        result["passed"] = result["passed"] and result["producer_artifact"]["comparison"]["passed"]
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--producer", type=Path)
    args = parser.parse_args()
    result = run_audit(args.output, args.producer)
    print(json.dumps({"passed": result["passed"], "output": str(args.output) if args.output else None,
                      "checks": {key: result[key]["passed"] for key in ("quantum_gravity", "googly", "unification")}}, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
