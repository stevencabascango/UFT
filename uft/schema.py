"""Canonical vocabulary for the integrated research index.

Validation concerns records and provenance. It is not a theorem prover or a
physical-consistency oracle. Spanish labels are presentation, stable keys APIs.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from genius.memory import STATES as SCIENTIFIC_STATES

SCHEMA_VERSION = "1.0"
OBJECTIVES = ("googly", "unification", "quantum_gravity")
KINDS = (
    "objective", "definition", "axiom", "postulate", "hypothesis",
    "approximation", "result", "prediction", "counterexample", "reference",
    "obstruction", "question", "convention", "candidate", "observable",
    "calculation", "audit", "disagreement", "equation", "document", "goal", "open_problem",
)
DIMENSIONS = {
    "mathematical": "Dimensión matemática",
    "physical": "Dimensión física",
    "documentary": "Dimensión documental y crítica",
    "operational": "Dimensión operativa",
}
COVERAGE_STATES = (
    "Revisado", "Parcialmente revisado", "Pendiente", "Bloqueado",
    "No aplicable, con justificación",
)
CRITERIA = {
    "mathematical_coherence": "Coherencia matemática",
    "testability": "Contrastabilidad",
    "correspondence": "Correspondencia",
    "operational_definitions": "Definiciones operacionales",
    "explanation_unification": "Explicación y unificación",
    "parsimony": "Parsimonia",
    "non_empirical": "Evaluación no empírica",
}
ASSESSMENT_STATES = (
    "Cumplido en el alcance declarado", "Parcial", "Pendiente", "Incumplido",
    "No aplicable, con justificación",
)
RELATIONS = {
    "dependency": "Dependencia", "implication": "Implicación",
    "equivalence": "Equivalencia", "correspondence": "Correspondencia",
    "compatibility": "Compatibilidad", "incompatibility": "Incompatibilidad",
    "analogy": "Analogía", "proposed_connection": "Conexión propuesta",
}
COHERENCE_CHECKS = (
    "map", "hypotheses", "conventions", "category", "frontiers", "registration",
)
TESTABILITY_STATES = (
    "Contrastable actualmente", "Contrastable en principio",
    "Ruta de contraste pendiente", "Sin consecuencias observacionales identificadas",
)
COVERAGE_ALIASES = dict(zip(("reviewed", "partial", "pending", "blocked", "not_applicable"), COVERAGE_STATES))
ASSESSMENT_ALIASES = dict(zip(("fulfilled", "partial", "pending", "failed", "not_applicable"), ASSESSMENT_STATES))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value


def require_list(value: Any, field: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    return value


def scientific_state(value: str) -> str:
    if value in SCIENTIFIC_STATES:
        return value
    for key, label in SCIENTIFIC_STATES.items():
        if value == label:
            return key
    raise ValueError(f"Unknown scientific state: {value}")


def statement_fingerprint(statement: str) -> str:
    """Catch obvious duplicates; mathematical equivalence needs human review."""
    text = re.sub(r"\s+", " ", statement.casefold()).strip().rstrip(". ")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_entity(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("An entity must be an object")
    entity = json.loads(canonical_json(raw))
    for name in ("id", "kind", "objectives", "statement", "hypotheses", "evidence", "dependencies", "status", "review"):
        if name not in entity:
            raise ValueError(f"Missing entity field: {name}")
    require_text(entity["id"], "id")
    require_text(entity["statement"], "statement")
    if entity["kind"] not in KINDS:
        raise ValueError(f"Unknown entity kind: {entity['kind']}")
    for name in ("objectives", "hypotheses", "evidence", "dependencies"):
        require_list(entity[name], name)
    if not entity["objectives"] or not set(entity["objectives"]).issubset(OBJECTIVES):
        raise ValueError("Entities must name at least one of the three scientific objectives")
    for name in ("dependencies", "conditional_on", "contradicts"):
        entity.setdefault(name, [])
        require_list(entity[name], name)
        for item in entity[name]:
            require_text(item, name)
        if len(entity[name]) != len(set(entity[name])):
            raise ValueError(f"Duplicate {name} ID")
    if entity["id"] in entity["dependencies"] or entity["id"] in entity["conditional_on"]:
        raise ValueError("An entity cannot depend on itself")
    entity["status"] = scientific_state(entity["status"])
    entity.setdefault("sources", [])
    require_list(entity["sources"], "sources")
    if entity["review"] is not None and not isinstance(entity["review"], dict):
        raise ValueError("review must be an object or null")
    if entity["status"] == "established":
        consulted = [s for s in entity["sources"] if isinstance(s, dict) and s.get("verified") is True
                     and s.get("result_used") and (s.get("url") or s.get("path") or s.get("id"))]
        if not consulted:
            raise ValueError("Established results need a verified identified source and the exact result used")
    if entity["status"] in {"evidence", "refuted"} and not entity["evidence"]:
        raise ValueError("Evidence or refutation needs documented evidence")
    if entity.get("testability") and entity["testability"] not in TESTABILITY_STATES:
        raise ValueError("Unknown testability classification")
    if entity["conditional_on"] and entity["status"] in {"established", "proven", "formal"}:
        raise ValueError("Conditional scientific conclusions cannot be stored as unconditional established/proven/formal results")
    # Caller-supplied storage metadata cannot overwrite revision history.
    for name in ("revision", "updated", "created", "content_sha256", "statement_sha256"):
        entity.pop(name, None)
    return entity


def validate_link(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("A link must be an object")
    link = json.loads(canonical_json(raw))
    for name in ("id", "source", "target", "relation", "map", "foundation", "hypotheses", "sources", "review", "status"):
        if name not in link:
            raise ValueError(f"Missing link field: {name}")
    for name in ("id", "source", "target", "map", "foundation", "status"):
        require_text(link[name], name)
    if link["source"] == link["target"]:
        raise ValueError("Self-links do not establish a connection")
    if link["relation"] not in RELATIONS:
        raise ValueError("Unknown relation type")
    if link["status"] not in {"proposed", "reviewed", "rejected", "review"}:
        raise ValueError("Unknown link review state")
    for name in ("hypotheses", "sources"):
        require_list(link[name], name)
    if not link["sources"]:
        raise ValueError("Connections must identify their documentary or calculation source")
    if not isinstance(link["review"], dict):
        raise ValueError("A link must record review information, even when pending")
    link.setdefault("propagates", link["relation"] == "dependency")
    if type(link["propagates"]) is not bool:
        raise ValueError("propagates must be a boolean")
    if link.get("transfer_level") not in {None, "A", "B"}:
        raise ValueError("Transfer level must be A or B")
    if link.get("transfer_level"):
        coherence = link.get("coherence", {})
        for key in COHERENCE_CHECKS:
            check = coherence.get(key)
            if not isinstance(check, dict) or check.get("passed") is not True:
                raise ValueError(f"Transfer coherence check failed or missing: {key}")
            require_text(check.get("justification"), f"coherence.{key}.justification")
        if not link["propagates"]:
            raise ValueError("Transfers must propagate changes to the target")
        if link["relation"] in {"analogy", "incompatibility", "proposed_connection"}:
            raise ValueError("Analogies, incompatibilities and unproved connections are not result transfers")
    return link
