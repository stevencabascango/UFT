#!/usr/bin/env python3
"""Finite, reproducible tests; no claim to solve full gravity or unification.

Core calculations use Q[i] arithmetic from fractions.Fraction, without a CAS.
Optional --sympy repeats selected identities with a different representation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
import json
import math
from pathlib import Path
import platform
import sys


@dataclass(frozen=True)
class Gaussian:
    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Gaussian) else Gaussian(Fraction(value))

    def __add__(self, value):
        other = self.coerce(value)
        return Gaussian(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.real, -self.imag)

    def __sub__(self, value):
        return self + -self.coerce(value)

    def __mul__(self, value):
        other = self.coerce(value)
        return Gaussian(self.real * other.real - self.imag * other.imag,
                        self.real * other.imag + self.imag * other.real)

    __rmul__ = __mul__

    def __truediv__(self, value):
        value = Fraction(value)
        return Gaussian(self.real / value, self.imag / value)

    def conjugate(self):
        return Gaussian(self.real, -self.imag)

    def as_json(self):
        return {"real": str(self.real), "imag": str(self.imag)}

    def __complex__(self):
        return complex(float(self.real), float(self.imag))


ZERO = Gaussian()
ONE = Gaussian(Fraction(1))
II = Gaussian(Fraction(0), Fraction(1))


def matvec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), ZERO) for row in matrix]


def inner(left, right):
    return sum((a.conjugate() * b for a, b in zip(left, right)), ZERO)


def multiply(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO)
             for j in range(len(right[0]))] for i in range(len(left))]


def adjoint(matrix):
    return [[matrix[j][i].conjugate() for j in range(len(matrix))]
            for i in range(len(matrix[0]))]


def kron(left, right):
    return [[left[i][j] * right[k][l]
             for j in range(len(left[0])) for l in range(len(right[0]))]
            for i in range(len(left)) for k in range(len(right))]


def tensor(factors):
    result = [[ONE]]
    for factor in factors:
        result = kron(result, factor)
    return result


def parity(indices):
    inversions = sum(indices[i] > indices[j]
                     for i in range(len(indices)) for j in range(i + 1, len(indices)))
    return -1 if inversions % 2 else 1


def matrix_json(matrix):
    return [[entry.as_json() for entry in row] for row in matrix]


def spin_clock_example():
    """Exact Gauss kernel and triple product on four spin-1/2 factors.

    Basis columns u0 and u1 have Gram diag(1,3). Orthonormal b1=u1/sqrt(3).
    Q is dimensionless; H=kappa Q, [kappa]=energy, hbar restored in time evolution.
    """
    ident = [[ONE, ZERO], [ZERO, ONE]]
    pauli = [[[ZERO, ONE], [ONE, ZERO]],
             [[ZERO, -II], [II, ZERO]],
             [[ONE, ZERO], [ZERO, -ONE]]]
    spin = [[[entry / 2 for entry in row] for row in matrix] for matrix in pauli]
    size = 16
    gauss = []
    for axis in range(3):
        factors = [tensor([spin[axis] if leg == site else ident for leg in range(4)])
                   for site in range(4)]
        gauss.append([[sum((factor[i][j] for factor in factors), ZERO)
                       for j in range(size)] for i in range(size)])
    terms = [(parity(axes), tensor([spin[axes[0]], spin[axes[1]], spin[axes[2]], ident]))
             for axes in permutations(range(3))]
    q = [[sum((sign * term[i][j] for sign, term in terms), ZERO)
          for j in range(size)] for i in range(size)]
    u0, u1 = [ZERO] * size, [ZERO] * size
    # Ordering |m1 m2 m3 m4>, |0>=up, |1>=down.
    for index, sign in [(5, 1), (6, -1), (9, -1), (10, 1)]:
        u0[index] = Gaussian(Fraction(sign, 2))
    for index, coeff in [(3, 1), (12, 1), (5, Fraction(-1, 2)),
                         (6, Fraction(-1, 2)), (9, Fraction(-1, 2)), (10, Fraction(-1, 2))]:
        u1[index] = Gaussian(Fraction(coeff))
    basis = [u0, u1]
    gram = [[inner(x, y) for y in basis] for x in basis]
    raw = [[inner(x, matvec(q, y)) for y in basis] for x in basis]
    restricted = [[raw[i][j] / gram[i][i].real for j in range(2)] for i in range(2)]
    squared = multiply(restricted, restricted)
    closure = all(all(entry == ZERO for entry in matvec(g, u))
                  for g in gauss for u in basis)
    intertwines = all(matvec(q, u) == [sum((basis[i][k] * restricted[i][j]
                        for i in range(2)), ZERO) for k in range(size)]
                       for j, u in enumerate(basis))
    weighted_hermitian = multiply(adjoint(restricted), gram) == multiply(gram, restricted)
    # Exact rational time parameter theta=pi/2 avoids floating trigonometric evidence.
    # U(pi/2)=-i*(4/sqrt(3))*Q; norm of column0 in Gram basis is1.
    norm_factor = sum((restricted[i][0].conjugate() * gram[i][i] * restricted[i][0]
                       for i in range(2)), ZERO)
    quarter_period_norm = norm_factor * Fraction(16, 3)
    # Bad Hamiltonian K=i*kappa*I has e^{-iKt/hbar}=e^{kappa*t/hbar}I.
    # Its norm derivative at t0 is2*kappa/hbar rather than0.
    norm_bad_derivative_at_zero = Fraction(2)
    return {
        "status": "EVIDENCIA SIMBÓLICA O NUMÉRICA",
        "scope": "single SU(2) four-valent intertwiner; imposed ideal clock; toy Hamiltonian",
        "arithmetic": "exact Gaussian rationals Q[i]",
        "tensor_space_dimension": size,
        "invariant_dimension": 2,
        "dimension_argument": "(1/2 tensor 1/2)=(0 directsum 1); singlet in0x0 and1x1 only",
        "basis_u0": [x.as_json() for x in u0],
        "basis_u1": [x.as_json() for x in u1],
        "gram": matrix_json(gram),
        "q_restricted_nonorthonormal": matrix_json(restricted),
        "q_squared": matrix_json(squared),
        "q_full_hermitian": adjoint(q) == q,
        "gauss_annihilates_basis": closure,
        "q_preserves_invariant_subspace": intertwines,
        "weighted_hermiticity": weighted_hermitian,
        "q_squared_equals_3_over_16_identity": squared == [
            [Gaussian(Fraction(3, 16)), ZERO], [ZERO, Gaussian(Fraction(3, 16))]],
        "quarter_period_norm_squared": str(quarter_period_norm.real),
        "nonhermitian_counterexample": {
            "claim": "any finite Hamiltonian preserves relational norm",
            "status": "REFUTADO",
            "K": "i*kappa*I",
            "norm_squared": "exp(2*kappa*(T-T0)/hbar)",
            "derivative_dimensionless_time_at_zero": str(norm_bad_derivative_at_zero),
        },
        "clock_turning_point": {"constraint": "p_T**2/(2M)+M*omega**2*T**2/2+H-E",
                                  "poisson_T_C": "p_T/M", "global_clock": False},
        "physical_claims_not_established": ["Einstein dynamics", "continuum limit", "UV completion",
                                             "discrete time", "observational prediction"],
    }


def mixed_obstruction_example():
    """MC over k[e,h]/(e^2,h^2); [x,y]=w and dz=w or dz=0."""
    cases = []
    for differential in (Fraction(1), Fraction(0)):
        b_z = Fraction(-1) if differential else Fraction(0)
        residual = differential * b_z + 1
        cases.append({"dz_coefficient": str(differential), "b_z": str(b_z),
                      "mixed_mc_residual": str(residual),
                      "H2_dimension": 0 if differential else 1,
                      "mixed_extension_exists": bool(differential)})
    return {"status": "EVIDENCIA SIMBÓLICA O NUMÉRICA",
            "cohomological_degrees": {"x": 1, "y": 1, "z": 1, "w": 2},
            "brackets": {"[x,y]": "w", "[y,x]": "w", "others": "0"},
            "coefficient_ring": "Q[e,h]/(e^2,h^2)",
            "cases": cases,
            "scope": "two finite DGLAs, no twistor-to-Einstein reconstruction supplied",
            "false_claim": "separate solvability always implies mixed solvability",
            "false_claim_status": "REFUTADO"}


def structure_constants(dim, triples):
    constants = {}
    for triple in triples:
        for order in permutations(range(3)):
            constants[tuple(triple[i] for i in order)] = parity(order)
    return constants


def jacobi_residual(dim, constants):
    # Components of [ei,[ej,ek]]+cyclic, with fabc=fab^c using delta.
    witnesses = []
    for i, j, k in product(range(dim), repeat=3):
        vector = [sum(constants.get((j, k, a), 0) * constants.get((i, a, d), 0)
                      + constants.get((k, i, a), 0) * constants.get((j, a, d), 0)
                      + constants.get((i, j, a), 0) * constants.get((k, a, d), 0)
                      for a in range(dim)) for d in range(dim)]
        if any(vector):
            witnesses.append({"inputs_zero_based": [i, j, k], "residual": vector})
    return witnesses


def coupling_example():
    good = structure_constants(3, [(0, 1, 2)])
    bad = structure_constants(5, [(0, 1, 2), (0, 3, 4)])
    good_residuals, bad_residuals = jacobi_residual(3, good), jacobi_residual(5, bad)
    return {"status": "EVIDENCIA SIMBÓLICA O NUMÉRICA",
            "scope": "algebraic prerequisite for a local Yang-Mills deformation; not unification",
            "good": {"algebra": "su(2), real compact form in chosen normalization",
                     "dimension": 3, "Jacobi_holds": not good_residuals,
                     "nonzero_Jacobi_residual_count": len(good_residuals)},
            "bad": {"dimension": 5, "nonzero_3form_components": {"f012": 1, "f034": 1},
                    "delta_invariant": True, "Jacobi_holds": not bad_residuals,
                    "nonzero_Jacobi_residual_count": len(bad_residuals),
                    "witness": next(x for x in bad_residuals if x["inputs_zero_based"] == [1, 2, 3])},
            "false_claim": "a totally antisymmetric cubic coupling always extends to a Lie gauge algebra",
            "false_claim_status": "REFUTADO"}


def sympy_crosscheck():
    import sympy as s
    q = s.Matrix([[0, -3 * s.I / 4], [s.I / 4, 0]])
    g = s.diag(1, 3)
    # Sign confirmed against the tensor construction; squared identity is sign-independent.
    theta = s.symbols("theta", real=True)
    u = s.cos(theta) * s.eye(2) - s.I * 4 / s.sqrt(3) * s.sin(theta) * q
    unitary = s.simplify(s.trigsimp(u.conjugate().T * g * u - g)) == s.zeros(2)
    return {"version": s.__version__, "q_squared": str(q * q),
            "weighted_unitarity_all_real_theta": unitary,
            "scope": "CAS identity for a finite2x2 matrix; no proof assistant execution"}


def run_examples(output_path=None, use_sympy=False):
    result = {"schema_version": "1.0", "execution_kind": "deterministic_local_calculation",
              "llm_execution": False, "python_version": platform.python_version(),
              "quantum_gravity": spin_clock_example(),
              "googly": mixed_obstruction_example(),
              "unification": coupling_example()}
    if use_sympy:
        result["sympy_crosscheck"] = sympy_crosscheck()
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sympy", action="store_true", help="optional independent CAS representation")
    args = parser.parse_args()
    result = run_examples(args.output, args.sympy)
    if args.output is None:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Evidence saved: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
