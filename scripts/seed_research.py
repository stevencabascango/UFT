#!/usr/bin/env python3
"""Import the closed first-cycle records, optionally replaying reviewed audits.

The opt-in audit import trusts the explicitly identified internal review, checks
its immutable artifacts, and uses GENIUS's audit gates. It does not infer proofs
from numerical tests or promote a complete physical theory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from genius.memory import ScientificMemory
from uft.inventory import write_json
from uft.store import ResearchStore
from uft.workflow import bootstrap


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply-reviewed-audits", action="store_true")
    args = parser.parse_args(argv)
    os.chdir(ROOT)
    items_path = ROOT / "research/items.json"
    items = json.loads(items_path.read_text(encoding="utf-8"))
    version = hashlib.sha256(items_path.read_bytes()).hexdigest()
    with ResearchStore(ROOT / ".uft/research.sqlite") as store:
        bootstrap(ROOT, store)
        event = store.ingest({"id": "FIRST-CYCLE-" + version[:20], "source": "research/items.json", "version": version,
                              "entities": items["entities"], "links": items["links"]})
        if event["status"] != "completed":
            raise ValueError("Seed intake failed: " + json.dumps(event))
        connections = ROOT / "data/connections.json"
        if connections.is_file():
            known_links = {link["id"] for link in store.snapshot()["links"]}
            for connection in json.loads(connections.read_text(encoding="utf-8"))["links"]:
                if connection["id"] not in known_links:
                    store.add_link(connection)
        promoted = []
        if args.apply_reviewed_audits:
            audit_path = ROOT / "evidence/scientific-review.json"
            review = json.loads(audit_path.read_text(encoding="utf-8"))
            if review["execution_status"] != "completed" or review["review_scope"] != "internal":
                raise ValueError("No closed internal review available")
            for relative, artifact in review["artifacts"].items():
                path = ROOT / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
                    raise ValueError("Reviewed artifact changed; obtain a new review: " + relative)
            verdicts = {v["id"]: v for v in review["claims"]}
            with ScientificMemory(ROOT / ".uft/claims.sqlite") as memory:
                for execution in (ROOT / "collaboration/codex/producer-execution.json", audit_path):
                    record = json.loads(execution.read_text(encoding="utf-8"))
                    try:
                        memory.register_execution(execution)
                    except sqlite3.IntegrityError:
                        # Replays must still pass the core artifact-integrity check.
                        memory._execution(record["execution_id"])
                for item in items["entities"]:
                    identifier = item["id"]
                    verdict = verdicts.get(identifier)
                    if not verdict:
                        continue
                    try:
                        claim = memory.get(identifier)
                    except KeyError:
                        claim = memory.add({"id": identifier, "statement": item["statement"],
                                            "hypotheses": list(dict.fromkeys(item["hypotheses"] + verdict["hypotheses"])),
                                            "sources": item.get("sources", []), "artifacts": [e["path"] for e in item["evidence"] if isinstance(e, dict) and e.get("path")],
                                            "dependencies": item["dependencies"], "status": item["status"],
                                            "scope": verdict["scope"]})
                    if verdict["verdict"].startswith("CONFIRMADO") and claim["status"] == "pending_audit":
                        memory.audit(identifier, audit_id=review["audit_id"] + "-" + identifier,
                                     verdict="confirmed", producer_execution="uft-physics-drafting-20261106",
                                     reviewer_execution=review["execution_id"], checks=review["checks"],
                                     artifacts=[str(p) for p in [audit_path, ROOT / "research/audits/mathematical_review.md", *[ROOT / p for p in claim["artifacts"]]]],
                                     scope="internal", limitations=verdict["scope"] + "; shared-model systematic errors remain possible; not formal or external peer review")
                        claim = memory.promote(identifier, "proven", audit_id=review["audit_id"] + "-" + identifier)
                    if claim["status"] in {"proven", "formal"}:
                        store.import_claim(memory, identifier, objectives=item["objectives"])
                        promoted.append(identifier)
                memory.export(ROOT / "memory/claims.json")
            for connection in store.snapshot()["links"]:
                if connection["id"] == "UFT-LINK-SHIFT-BV":
                    connection.update(status="reviewed", review={"status": "reviewed", "audit_id": review["audit_id"],
                                                                 "scope": "Conditional mathematical degree-shift correspondence only; no physical equivalence",
                                                                 "source": "research/audits/scientific_review.md"})
                    for key in ("invalidated_by", "invalidation_reason"):
                        connection.pop(key, None)
                    store.add_link(connection)
        from uft.reporting import export_snapshot
        export_snapshot(store.snapshot(), ROOT / "exports")
        print(json.dumps({"event": event["status"], "reviewed_scoped_claims_imported": promoted,
                          "physical_goals_completed": 0, "external_reviews": 0, "formal_verifications": 0}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
