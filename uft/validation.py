"""Repository structure/provenance checks; not a scientific truth oracle."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def validate_project(root: Path) -> dict:
    from genius.catalogue import load_profiles, validate_profiles
    from .skills import validate_skills
    errors = []
    registry = validate_profiles(load_profiles(root / "institute/registry/profiles.jsonl"))
    skills = validate_skills(root)
    if not registry["valid"]:
        errors.extend(registry["errors"])
    if not skills["valid"]:
        errors.extend(skills["errors"])
    goals = json.loads((root / "data/goals.json").read_text(encoding="utf-8"))
    if {g["programme"] for g in goals["goals"]} != {"googly", "unification", "quantum_gravity"} or len(goals["goals"]) != 3:
        errors.append("Exactly three distinct physical programmes required")
    if any(g.get("achieved") for g in goals["goals"]):
        errors.append("Goal completion is not established by this software release")
    upstream = json.loads((root / "data/upstream_genius5000.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256((root / "institute/registry/profiles.jsonl").read_bytes()).hexdigest()
    expected = upstream.get("registry_sha256") or upstream.get("profiles_sha256")
    if expected and digest != expected:
        errors.append("Registry differs from the documented upstream snapshot")
    return {"valid": not errors, "registry": registry, "skills": skills, "goals": 3,
            "registry_sha256": digest, "errors": errors,
            "scope": "Structural validation; individual scientific competence and completeness of physical theories remain unestablished."}
