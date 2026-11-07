"""Select bounded design profiles with an explicit programme-specific physics role."""
from __future__ import annotations

import hashlib
import json
import re

from genius.planning import select_team

PHYSICS_DIVISION = {"googly": "twistors", "unification": "qft", "quantum_gravity": "lqg"}


def select_research_team(profiles: list[dict], problem: str, size: int = 7,
                         programme: str = "quantum_gravity") -> dict:
    if programme not in PHYSICS_DIVISION:
        raise ValueError("Unknown physical programme")
    selected = select_team(profiles, problem, size)
    assignment = next(a for a in selected["assignments"] if a["role"] == "physics")
    used_other = {a["profile_id"] for a in selected["assignments"] if a["role"] != "physics"}
    terms = set(re.findall(r"[\w-]+", problem.casefold()))
    candidates = [p for p in profiles if p["division"] == PHYSICS_DIVISION[programme] and p["id"] not in used_other]
    def score(profile):
        text = json.dumps({k: v for k, v in profile.items() if k in {"specialty", "subspecialties", "objects", "problems", "methods"}}, ensure_ascii=False).casefold()
        return (sum(term in text for term in terms), hashlib.sha256((problem + profile["id"]).encode()).hexdigest())
    candidate = max(candidates, key=score)
    old = assignment["profile_id"]
    assignment.update(profile_id=candidate["id"], selection_score=score(candidate)[0],
                      programme_requirement="Explicit division coverage; no evaluated competence inferred")
    selected["selected_profiles"] = list(dict.fromkeys(a["profile_id"] for a in selected["assignments"]))
    # Small teams may combine functions. If replacing a shared physics profile
    # would exceed the requested size, retain the original bounded assignment.
    if len(selected["selected_profiles"]) > size:
        assignment["profile_id"] = old
        assignment["programme_requirement"] = "Small-team combined role; request seven profiles for explicit division coverage"
        selected["selected_profiles"] = list(dict.fromkeys(a["profile_id"] for a in selected["assignments"]))
    selected.update(primary_programme=programme, actual_llm_executions=0,
                    selection_method="Deterministic role coverage plus explicit primary-programme division; design profiles only")
    return selected
