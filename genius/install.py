"""Conservative project installation: never replace an existing file or setting."""
from __future__ import annotations

import os
from pathlib import Path
import shutil

COMPONENTS = ("genius", "uft", "institute", ".agents", ".claude", ".codex", "docs", "scripts",
              "research", "verification", "collaboration", "memory", "references", "data", "config",
              "automation", "alerts", "exports", "evidence", "Descargas", "tests",
              "AGENTS.md", "CLAUDE.md", "README.md", "CONTRIBUTING.md", "pyproject.toml", ".gitignore", "LICENSE")


def _private_or_working(relative: Path) -> bool:
    """Working databases, credentials and generated state are not installation assets."""
    return (any(part in {"__pycache__", ".uft", ".venv", ".git", ".pytest_cache"} for part in relative.parts)
            or relative.suffix in {".pyc", ".pyo", ".db", ".log"}
            or ".sqlite" in relative.name or relative.name.endswith((".db-wal", ".db-shm", ".db-journal"))
            or relative.name == ".env" or relative.name.startswith(".env.")
            or relative.name in {"settings.local.json", "auth.json", "credentials.json", "tokens.json"}
            or relative == Path("automation/local-state.json"))


def install_project(source: str | Path, destination: str | Path, *, dry_run: bool = False) -> dict:
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Use a separate target project, outside the source tree and its parents")
    result = {"copied": [], "unchanged": [], "conflicts_preserved": [], "dry_run": dry_run,
              "unsafe_source_links": [], "global_configuration_modified": False,
              "runtime": "uft" if (source / "uft/__main__.py").is_file() else "genius",
              "scope": "Project-local runtime, scientific assets and adapters; no global configuration or model installation"}
    for component in COMPONENTS:
        start = source / component
        if not start.exists() and not start.is_symlink():
            continue
        paths = [start] if start.is_file() or start.is_symlink() else sorted(start.rglob("*"))
        for path in paths:
            relative = path.relative_to(source)
            if _private_or_working(relative):
                continue
            if path.is_dir() and not path.is_symlink():
                continue
            target = destination / relative
            link_target = None
            if path.is_symlink():
                # An archive/checkout must not install a pointer to unrelated
                # local files. Rebase internal absolute links for portability.
                try:
                    resolved = path.resolve(strict=True)
                except (OSError, RuntimeError):
                    result["unsafe_source_links"].append(str(relative))
                    continue
                if not resolved.is_relative_to(source) or _private_or_working(resolved.relative_to(source)):
                    result["unsafe_source_links"].append(str(relative))
                    continue
                link_target = os.path.relpath(destination / resolved.relative_to(source), target.parent)
            parent = target.parent
            blocked_parent = False
            while parent != destination:
                if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                    blocked_parent = True
                    break
                parent = parent.parent
            if blocked_parent:
                result["conflicts_preserved"].append(str(relative))
                continue
            if target.exists() or target.is_symlink():
                same = path.is_symlink() and target.is_symlink() and link_target == os.readlink(target)
                if not path.is_symlink() and target.is_file() and not target.is_symlink():
                    same = path.read_bytes() == target.read_bytes()
                result["unchanged" if same else "conflicts_preserved"].append(str(relative))
                continue
            result["copied"].append(str(relative))
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if path.is_symlink():
                    target.symlink_to(link_target)
                else:
                    shutil.copy2(path, target)
    result["complete"] = not result["conflicts_preserved"] and not result["unsafe_source_links"]
    return result
