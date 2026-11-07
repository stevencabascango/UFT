"""Discover the 22 inherited skills and five integrated UFT skills safely.

Discovery reads repository-local instructions only. It runs no model, installer,
scientific calculation, scheduler or state promotion.
"""
from __future__ import annotations

from pathlib import Path
import re

from genius.skills import REQUIRED_SECTIONS, SKILL_NAMES as CORE_SKILL_NAMES
from genius.skills import validate_skills as validate_core_skills

INTEGRATED_SKILL_NAMES = (
    "scientific-intake", "seven-criteria-assessment", "justified-transfer-audit",
    "relational-time-lqg", "continuous-research-report",
)
SKILL_NAMES = CORE_SKILL_NAMES + INTEGRATED_SKILL_NAMES
ENVIRONMENTS = ("canonical", "codex", "claude")


def skill_path(root: str | Path, name: str, *, environment: str = "codex") -> Path:
    """Resolve an allowlisted skill and reject escaping symlinks before reading."""
    if name not in SKILL_NAMES:
        raise ValueError(f"Unknown UFT skill: {name}")
    if environment not in ENVIRONMENTS:
        raise ValueError(f"Unknown skill environment: {environment}")
    root = Path(root).resolve()
    base = root / ".agents" / "skills"
    resolved_base = base.resolve(strict=True)
    if not resolved_base.is_relative_to(root):
        raise ValueError("Canonical skills directory escapes the repository")
    canonical = (base / name / "SKILL.md").resolve(strict=True)
    if not canonical.is_relative_to(resolved_base):
        raise ValueError(f"Canonical skill escapes the shared skill library: {name}")
    if not canonical.is_file():
        raise ValueError(f"Skill entry point is not a file: {name}")
    if environment == "claude":
        adapter = root / ".claude" / "skills" / name
        if not adapter.is_symlink():
            raise ValueError(f"Claude skill adapter must be a canonical directory symlink: {name}")
        resolved = (adapter / "SKILL.md").resolve(strict=True)
        if resolved != canonical:
            raise ValueError(f"Claude adapter does not resolve to its canonical skill: {name}")
        return resolved
    return canonical


def load_skill(root: str | Path, name: str, *, environment: str = "codex") -> str:
    return skill_path(root, name, environment=environment).read_text(encoding="utf-8")


def _metadata(content: str, name: str) -> dict:
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        raise ValueError(f"{name}: missing YAML frontmatter")
    frontmatter = match.group(1)
    if not re.search(rf"^name: {re.escape(name)}$", frontmatter, re.M):
        raise ValueError(f"{name}: frontmatter name mismatch")
    description = re.search(r"^description: (.+)$", frontmatter, re.M)
    if description is None or not description.group(1).strip():
        raise ValueError(f"{name}: missing description")
    return {"name": name, "description": description.group(1).strip()}


def discover_skills(root: str | Path, *, environment: str = "codex") -> list[dict]:
    skills = []
    for name in SKILL_NAMES:
        path = skill_path(root, name, environment=environment)
        metadata = _metadata(path.read_text(encoding="utf-8"), name)
        skills.append({**metadata, "path": str(path), "environment": environment,
                       "library": "genius_core" if name in CORE_SKILL_NAMES else "integrated_uft"})
    return skills


def validate_skills(root: str | Path) -> dict:
    root = Path(root).resolve()
    errors = []
    for name in SKILL_NAMES:
        try:
            content = load_skill(root, name)
            _metadata(content, name)
            load_skill(root, name, environment="claude")
        except (OSError, ValueError) as error:
            errors.append(f"{name}: {error}")
            continue
        for section in REQUIRED_SECTIONS:
            if f"## {section}\n" not in content:
                errors.append(f"{name}: missing section {section}")
        if name in INTEGRATED_SKILL_NAMES and "../../../docs/research_protocol.md" not in content:
            errors.append(f"{name}: missing shared integrated research protocol reference")
    # The inherited validator reads canonical files; do not invoke it if a path
    # failed confinement or adapter validation above.
    if not errors:
        errors.extend(validate_core_skills(root)["errors"])
    for document in ("scientific_protocol.md", "research_protocol.md"):
        if not (root / "docs" / document).is_file():
            errors.append(f"Missing shared protocol: docs/{document}")
    return {"valid": not errors, "count": len(SKILL_NAMES),
            "core_count": len(CORE_SKILL_NAMES), "integrated_count": len(INTEGRATED_SKILL_NAMES),
            "errors": errors, "scientific_goals_achieved": False,
            "scope": "Skill discovery, adapters and structural contracts; scientific effectiveness requires task-specific evidence."}
