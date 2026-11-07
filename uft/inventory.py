"""Bounded, read-only inventory of explicitly selected scientific sources.

An imported source is not a new scientific audit. No recursive home/OneDrive
scan is performed. The portable snapshot works without the author's folders.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    "brain": ("META.md", "ALERTAS.md", "NUCLEO.md", "CEREBRO2.md", "CEREBRO3.md",
              "EXPLORACION.md", "PREGUNTAS_TAGA.md", "PROMETEDORAS.md",
              "EQUIVALENCIAS.md", "ADMIN_WEB.md", "partes/meta_liston.json"),
    "master": ("00_PROJECT_MANIFEST/research_protocol.md",
               "00_PROJECT_MANIFEST/conventions.md", "00_PROJECT_MANIFEST/objectives.md"),
}
MAX_SOURCE_BYTES = 2 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def collect_inventory(brain: Path | None = None, master: Path | None = None) -> dict:
    roots = {"brain": brain, "master": master}
    records = []
    for group, names in SOURCE_FILES.items():
        root = roots[group]
        for name in names:
            row = {"id": "SRC-" + group.upper() + "-" + name.replace("/", "-").replace(".", "-"),
                   "collection": group, "relative_path": name,
                   "scientific_validation": "not_reaudited_on_import"}
            if root is None:
                row.update(access="unavailable", reason="Canonical directory not supplied; portable snapshot available")
            else:
                path = root / name
                try:
                    if not path.resolve().is_relative_to(root.resolve()):
                        raise ValueError("Source resolves outside the selected canonical directory")
                    stat = path.stat()
                    if stat.st_size > MAX_SOURCE_BYTES:
                        raise ValueError("Source exceeds the documented 2 MiB bound")
                    raw = path.read_bytes()
                    text = raw.decode("utf-8")
                    row.update(access="consulted", bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                               modified_utc=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                               headings=[line[:250] for line in text.splitlines() if line.startswith("#")][:30])
                except (OSError, ValueError, UnicodeError) as error:
                    row.update(access="unavailable", reason=str(error))
            records.append(row)
    return {"schema_version": "1.0", "captured_utc": utc_now(), "sources": records,
            "scope": "Allowlisted shared manifests, goals and public scientific summaries; no independent research branches or private documents.",
            "limits": ["Source labels are preserved as reports, not certified by import.",
                       "Unlisted literature and inaccessible sources are outside this finite inventory."]}


def collect_goals(brain: Path, master: Path | None = None) -> dict:
    meta_path = brain / "partes/meta_liston.json"
    if meta_path.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("Oversized canonical roadmap")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    programmes = (
        ("GOAL-GOOGLY", "googly", "Problema de Googly", "hoja_googly",
         "Construcción y reconstrucción twistorial más allá de sectores autoduales, con ambas helicidades, realidad, gauge y dinámica de Einstein delimitadas."),
        ("GOAL-UFT", "unification", "Unificación de campos", "hoja_unificacion",
         "Construcción física que relacione gravedad, campos gauge y materia con dinámica, simetrías, parámetros, límites y observables explícitos."),
        ("GOAL-QG", "quantum_gravity", "Gravedad cuántica, tiempo y LQG", "hoja_gravedad_cuantica",
         "Cuantizar la relatividad general: estados físicos, observables, restricciones, dinámica, tratamiento UV y límite semiclásico; estudiar tiempo relacional y LQG sin inferir discreción temporal del área."),
    )
    goals = []
    for identifier, key, title, roadmap, statement in programmes:
        current = meta.get(roadmap, {})
        goals.append({"id": identifier, "programme": key, "title": title, "statement": statement,
                      "achieved": False, "theory_level": "research_programme",
                      "source": "brain/partes/meta_liston.json", "source_sha256": sha256(meta_path),
                      "milestones": current.get("hitos", []),
                      "reported_prior_state": current.get("estado", {}),
                      "import_review": "Prior labels retained for traceability; exact artifacts and hypotheses must be checked before transfer.",
                      "independence": "Independent programme; unification with another goal is a hypothesis requiring an explicit dictionary."})
    return {"schema_version": "1.0", "captured_utc": utc_now(), "goals": goals,
            "precedence": "Latest explicit user request and canonical META + conventions override dated summaries.",
            "ambiguities": [{"source": "master/00_PROJECT_MANIFEST/objectives.md",
                             "finding": "Dated summary lists objectives I–III; current conventions also include quantizing GR (IV).",
                             "resolution": "Retain as antecedent. Use the three physical goals of current META; I–IV are not four different physical theories."}],
            "candidate_policy": "Three independent conditional programmes. Shared tools are permitted, no asserted common final theory."}


def import_snapshot(root: Path, *, brain: Path | None = None, master: Path | None = None) -> dict:
    inventory = collect_inventory(brain, master)
    write_json(root / "data" / "source_inventory.json", inventory)
    if brain is not None:
        write_json(root / "data" / "goals.json", collect_goals(brain, master))
    return inventory
