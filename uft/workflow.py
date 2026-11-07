"""Local incremental workflow. No scientific claim is promoted automatically."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import time

from .inventory import SOURCE_FILES, MAX_SOURCE_BYTES, utc_now, write_json
from .reporting import CRITERIA, as_rows, export_snapshot

COVERAGE_ITEMS = {
    "mathematical": ("Definiciones y objetos", "Axiomas e hipótesis", "Espacios, categorías y estructuras",
                     "Ecuaciones y relaciones", "Simetrías e invariantes", "Regularidad y contorno",
                     "Existencia y unicidad", "Local y global", "Integrabilidad y obstrucciones", "Dependencias"),
    "physical": ("Variables físicas", "Estados y observables", "Dinámica", "Causalidad", "Dimensiones y unidades",
                 "Simetrías y restricciones", "Grados de libertad", "Condiciones de realidad", "Conservación y estabilidad",
                 "Cuantización y aproximaciones", "Régimen de validez", "Predicciones y datos"),
    "documentary": ("Antecedentes", "Resultados establecidos", "Supuestos nuevos", "Alternativas", "Objeciones",
                    "Contraejemplos", "Evidencias disponibles", "Dependencias no verificadas", "Preguntas pendientes"),
    "operational": ("Herramientas y datos", "Tiempo y cálculo", "Especialistas", "Comprobaciones pendientes", "Parada y continuación"),
}


def entity(identifier: str, kind: str, objectives: list[str], statement: str, *, status="proposal",
           hypotheses=None, evidence=None, dependencies=None, sources=None, **extra) -> dict:
    return {"id": identifier, "kind": kind, "objectives": objectives, "statement": statement,
            "hypotheses": hypotheses or [], "evidence": evidence or [], "dependencies": dependencies or [],
            "sources": sources or [], "status": status, "review": None, **extra}


def source_entity(row: dict) -> dict:
    return entity(row["id"], "document", ["googly", "unification", "quantum_gravity"],
                  f"Documento compartido {row['collection']}/{row['relative_path']}; procedencia observada, contenido científico pendiente de revalidación en UFT.",
                  status="proposal" if row["access"] == "consulted" else "review",
                  evidence=[{"source_sha256": row.get("sha256"), "access": row["access"]}],
                  sources=[{"path": row["collection"] + "/" + row["relative_path"], "verified": False,
                            "result_used": "Source inventory only; no scientific promotion"}],
                  source_version=row.get("sha256"), domain="documentary_provenance")


def _existing(store, identifier: str) -> bool:
    try:
        store.get_entity(identifier)
        return True
    except KeyError:
        return False


def bootstrap(root: Path, store) -> dict:
    """Add the portable seed once; preserve all subsequent user research edits."""
    inventory = json.loads((root / "data/source_inventory.json").read_text(encoding="utf-8"))
    goals = json.loads((root / "data/goals.json").read_text(encoding="utf-8"))["goals"]
    created = []
    for row in inventory["sources"]:
        if not _existing(store, row["id"]):
            store.upsert_entity(source_entity(row))
            created.append(row["id"])
    for goal in goals:
        if _existing(store, goal["id"]):
            continue
        store.upsert_entity(entity(goal["id"], "objective", [goal["programme"]], goal["statement"],
                                   dependencies=["SRC-BRAIN-partes-meta_liston-json"],
                                   evidence=[{"path": "data/goals.json", "source_sha256": goal["source_sha256"]}],
                                   sources=[{"path": goal["source"], "verified": False,
                                             "result_used": "Current goal definition, not a physical theorem"}],
                                   theory_level="research_programme"))
        created.append(goal["id"])
        for dimension, items in COVERAGE_ITEMS.items():
            for item in items:
                partial = dimension == "documentary" and item in {"Antecedentes", "Resultados establecidos", "Preguntas pendientes"}
                store.set_coverage(goal["id"], dimension, item, "partial" if partial else "pending",
                                   "Manifestos y hojas de ruta localizados; se conservan sus etiquetas sin volver a auditar cada resultado."
                                   if partial else "Fuera de lo verificado por la instantánea inicial; requiere investigación delimitada.",
                                   evidence=["data/source_inventory.json", "data/goals.json"] if partial else [])
        for key in CRITERIA:
            store.set_assessment(goal["id"], key, "pending", ["data/goals.json"],
                                 "Un programa abierto no satisface este criterio por disponer de infraestructura o un modelo finito.",
                                 "Definir una propuesta y registrar evidencia específica para el dominio pretendido.")
        for milestone in goal["milestones"]:
            mid = "MILESTONE-" + milestone["id"]
            if _existing(store, mid):
                continue
            store.upsert_entity(entity(mid, "question", [goal["programme"]], milestone["hito"],
                                       hypotheses=["Prerregistros y condiciones originales deben respetarse; una calibración no completa el hito."],
                                       evidence=[{"path": "data/goals.json", "milestone": milestone["id"]}],
                                       success_criterion=milestone.get("exito", "Consultar fuente"),
                                       failure_criterion=milestone.get("fracaso", "Consultar fuente")))
            created.append(mid)
    known_links = {item["id"] for item in store.snapshot()["links"]}
    for goal in goals:
        lid = "PROVENANCE-" + goal["id"]
        if lid not in known_links:
            store.add_link({"id": lid, "source": "SRC-BRAIN-partes-meta_liston-json", "target": goal["id"],
                            "relation": "dependency", "map": "Map the named canonical roadmap entry to the physical goal statement and milestone IDs.",
                            "foundation": "Documentary precedence in data/goals.json; no physical theorem is imported.",
                            "hypotheses": ["Use current META and explicit user instructions over dated summaries"],
                            "sources": ["data/source_inventory.json", "data/goals.json"],
                            "review": {"status": "reviewed", "scope": "documentary provenance only"}, "status": "reviewed"})
    scientific = root / "research/items.json"
    if scientific.is_file():
        seed = json.loads(scientific.read_text(encoding="utf-8"))
        for item in seed["entities"]:
            if not _existing(store, item["id"]):
                store.upsert_entity(item)
                created.append(item["id"])
        known_links = {item["id"] for item in store.snapshot()["links"]}
        for item in seed["links"]:
            if item["id"] not in known_links:
                store.add_link(item)
    return {"created": created, "count": len(created), "scientific_promotions": 0}


def run_watch(root: Path, store, *, brain: Path | None = None, master: Path | None = None,
              interval: float = 60, max_cycles: int = 1, max_seconds: float = 300,
              max_files: int = 64, max_bytes: int = MAX_SOURCE_BYTES) -> dict:
    """Observe only shared allowlisted sources; all runs have enforced bounds."""
    if not (1 <= max_cycles <= 10000 and .01 <= max_seconds <= 86400 and 0 <= interval <= 3600
            and 1 <= max_files <= 64 and 1 <= max_bytes <= MAX_SOURCE_BYTES):
        raise ValueError("Invalid watcher budget")
    roots = {"brain": brain, "master": master}
    entries = [(group, directory, name) for group, directory in roots.items() if directory is not None
               for name in SOURCE_FILES[group]]
    if not entries:
        raise ValueError("Select at least one canonical directory; watch does not scan the home directory")
    if len(entries) > max_files:
        raise ValueError("Allowlisted source count exceeds max_files; no partial coverage silently accepted")
    start = time.monotonic()
    cycles, processed, changed, failures = 0, 0, [], []
    while cycles < max_cycles and time.monotonic() - start < max_seconds:
        for group, directory, name in entries:
            if time.monotonic() - start >= max_seconds:
                break
            path = directory / name
            try:
                if not path.resolve().is_relative_to(directory.resolve()):
                    raise ValueError("Symlink outside selected scientific source root")
                if path.stat().st_size > max_bytes:
                    raise ValueError("Source exceeds watcher file budget")
                with path.open("rb") as stream:
                    raw = stream.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise ValueError("Source grew beyond watcher file budget")
                raw.decode("utf-8")
                digest = hashlib.sha256(raw).hexdigest()
                sid = "SRC-" + group.upper() + "-" + name.replace("/", "-").replace(".", "-")
                event_id = "WATCH-" + hashlib.sha256((sid + digest).encode()).hexdigest()
                # Comparing the current source revision before emitting an event
                # suppresses alerts when canonical files have not changed.
                if _existing(store, sid) and store.get_entity(sid).get("source_version") == digest:
                    processed += 1
                    continue
                document = source_entity({"id": sid, "collection": group, "relative_path": name,
                                          "access": "consulted", "sha256": digest})
                result = store.ingest({"id": event_id, "source": group + "/" + name,
                                       "version": digest, "entity": document})
                if result.get("status") not in {"completed", "duplicate"}:
                    raise ValueError("Intake did not complete: " + json.dumps(result, ensure_ascii=False))
                changed.append({"source": group + "/" + name, "event": result})
                processed += 1
            except (OSError, UnicodeError, ValueError, KeyError) as error:
                failures.append({"source": group + "/" + name, "error": str(error),
                                 "action": "Restore accessibility and retry this bounded watcher; no scientific update was inferred."})
        cycles += 1
        remaining = max_seconds - (time.monotonic() - start)
        if cycles < max_cycles and remaining > 0 and interval:
            time.sleep(min(interval, remaining))
    result = {"schema_version": "1.0", "completed_utc": utc_now(), "mode": "bounded_file_events",
              "cycles": cycles, "processed_sources": processed, "changes": changed, "failures": failures,
              "quiet": not changed and not failures, "successful": not failures,
              "elapsed_seconds": time.monotonic() - start,
              "budgets": {"max_cycles": max_cycles, "max_seconds": max_seconds, "max_files": max_files, "max_bytes": max_bytes},
              "model_calls": 0, "scientific_promotions": 0,
              "limitations": "No background scheduler is implied. Research and central-claim audits remain separate budgeted executions."}
    write_json(root / ".uft/watch-last.json", result)
    return result


def export_project(root: Path, store, output: Path | None = None) -> dict:
    return export_snapshot(store.snapshot(), output or root / "exports")
