"""Transactional research records, justified links and incremental impact analysis.

This index validates provenance and workflow constraints, never scientific truth.
Strong claims enter only through the existing GENIUS scientific-memory audit gate.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from genius.io import digest, now, write_json
from genius.memory import ScientificMemory
from .schema import (
    ASSESSMENT_ALIASES, ASSESSMENT_STATES, COHERENCE_CHECKS, COVERAGE_ALIASES,
    COVERAGE_STATES, CRITERIA, DIMENSIONS, RELATIONS, SCHEMA_VERSION,
    SCIENTIFIC_STATES, canonical_json, fingerprint, require_list, require_text,
    statement_fingerprint, validate_entity, validate_link,
)


class ResearchStore:
    """SQLite working index with immutable revision and event records.

    Use ``export`` for portable, reviewable JSON. The database path can be
    ``:memory:`` in tests. No constructor starts a daemon or performs network I/O.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path) if str(path) != ":memory:" else None
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path), timeout=15, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self._savepoint = 0
        self.db.executescript("""
            PRAGMA foreign_keys=ON;
            PRAGMA busy_timeout=15000;
            CREATE TABLE IF NOT EXISTS uft_entities (
                id TEXT PRIMARY KEY, revision INTEGER NOT NULL,
                content_sha256 TEXT NOT NULL, statement_sha256 TEXT NOT NULL,
                data TEXT NOT NULL, updated TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS uft_statement_idx ON uft_entities(statement_sha256);
            CREATE TABLE IF NOT EXISTS uft_dependencies (
                entity_id TEXT NOT NULL REFERENCES uft_entities(id),
                prerequisite_id TEXT NOT NULL REFERENCES uft_entities(id),
                PRIMARY KEY(entity_id, prerequisite_id));
            CREATE TABLE IF NOT EXISTS uft_links (
                id TEXT PRIMARY KEY, data TEXT NOT NULL, content_sha256 TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS uft_coverage (
                entity_id TEXT NOT NULL REFERENCES uft_entities(id),
                dimension TEXT NOT NULL, item TEXT NOT NULL, data TEXT NOT NULL,
                PRIMARY KEY(entity_id, dimension, item));
            CREATE TABLE IF NOT EXISTS uft_assessments (
                entity_id TEXT NOT NULL REFERENCES uft_entities(id),
                criterion TEXT NOT NULL, data TEXT NOT NULL,
                PRIMARY KEY(entity_id, criterion));
            CREATE TABLE IF NOT EXISTS uft_history (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL,
                action TEXT NOT NULL, data TEXT NOT NULL, recorded TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS uft_events (
                id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL UNIQUE,
                source TEXT NOT NULL, version TEXT NOT NULL,
                status TEXT NOT NULL, attempts INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL, data TEXT NOT NULL,
                result TEXT, error TEXT, updated TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS uft_alerts (
                id TEXT PRIMARY KEY, dedup_key TEXT NOT NULL UNIQUE,
                data TEXT NOT NULL, recorded TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS uft_comparisons (
                id TEXT PRIMARY KEY, data TEXT NOT NULL);
        """)

    def close(self) -> None:
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    @contextmanager
    def _transaction(self):
        outer = not self.db.in_transaction
        self._savepoint += 1
        savepoint = f"uft_{self._savepoint}"
        self.db.execute("BEGIN IMMEDIATE" if outer else f"SAVEPOINT {savepoint}")
        try:
            yield
        except BaseException:
            self.db.execute("ROLLBACK" if outer else f"ROLLBACK TO {savepoint}")
            if not outer:
                self.db.execute(f"RELEASE {savepoint}")
            raise
        else:
            self.db.execute("COMMIT" if outer else f"RELEASE {savepoint}")

    def _history(self, subject: str, action: str, data: dict) -> None:
        self.db.execute("INSERT INTO uft_history(subject,action,data,recorded) VALUES(?,?,?,?)",
                        (subject, action, canonical_json(data), now()))

    def get_entity(self, entity_id: str) -> dict:
        row = self.db.execute("SELECT * FROM uft_entities WHERE id=?", (entity_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown entity: {entity_id}")
        return {**json.loads(row["data"]), "revision": row["revision"],
                "content_sha256": row["content_sha256"], "updated": row["updated"]}

    get = get_entity

    def _save_entity(self, entity: dict, *, action: str) -> dict:
        # metadata is generated only here; scientific content has a stable hash.
        clean = {k: v for k, v in entity.items() if k not in {"revision", "updated", "content_sha256"}}
        previous = self.db.execute("SELECT revision FROM uft_entities WHERE id=?", (clean["id"],)).fetchone()
        revision = previous[0] + 1 if previous else 1
        checksum = fingerprint(clean)
        self.db.execute("""INSERT INTO uft_entities VALUES(?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET revision=excluded.revision,
            content_sha256=excluded.content_sha256,statement_sha256=excluded.statement_sha256,
            data=excluded.data,updated=excluded.updated""",
            (clean["id"], revision, checksum, statement_fingerprint(clean["statement"]), canonical_json(clean), now()))
        self.db.execute("DELETE FROM uft_dependencies WHERE entity_id=?", (clean["id"],))
        self.db.executemany("INSERT INTO uft_dependencies VALUES(?,?)",
                            [(clean["id"], dep) for dep in sorted(set(clean["dependencies"] + clean["conditional_on"]))])
        saved = self.get_entity(clean["id"])
        self._history(clean["id"], action, saved)
        return saved

    def _arcs(self) -> dict[str, set[str]]:
        """Information flows prerequisite -> dependent, unlike dependency lists."""
        arcs = {r[0]: set() for r in self.db.execute("SELECT id FROM uft_entities")}
        for row in self.db.execute("SELECT entity_id,prerequisite_id FROM uft_dependencies"):
            arcs.setdefault(row[1], set()).add(row[0])
        for row in self.db.execute("SELECT data FROM uft_links"):
            link = json.loads(row[0])
            if link["propagates"] and link["status"] != "rejected":
                arcs.setdefault(link["source"], set()).add(link["target"])
        return arcs

    @staticmethod
    def _reachable(arcs: dict[str, set[str]], start: str) -> set[str]:
        seen, pending = set(), list(arcs.get(start, ()))
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            pending.extend(arcs.get(current, ()))
        return seen

    def _check_dependencies(self, entity: dict) -> None:
        ids = set(entity["dependencies"] + entity["conditional_on"] + entity["contradicts"])
        for identifier in ids:
            self.get_entity(identifier)
        arcs = self._arcs()
        # Remove the old prerequisite -> this-entity arcs before testing replacement.
        old = self.db.execute("SELECT prerequisite_id FROM uft_dependencies WHERE entity_id=?", (entity["id"],))
        for row in old:
            arcs[row[0]].discard(entity["id"])
        downstream = self._reachable(arcs, entity["id"])
        if downstream.intersection(entity["dependencies"] + entity["conditional_on"]):
            raise ValueError("Circular logical dependency")
        if entity["status"] in {"established", "evidence", "proven", "formal"}:
            bad = [key for key in entity["dependencies"] + entity["conditional_on"]
                   if self.get_entity(key)["status"] in {"review", "refuted"}]
            if bad:
                raise ValueError(f"Unresolved/refuted dependency: {bad}")

    @staticmethod
    def _check_artifacts(entity: dict) -> None:
        for evidence in entity["evidence"]:
            if not isinstance(evidence, dict) or "path" not in evidence:
                continue
            path = Path(evidence["path"])
            if not path.is_file():
                raise ValueError(f"Evidence file is missing: {path}")
            actual = digest(path)
            if evidence.get("sha256") and evidence["sha256"] != actual:
                raise ValueError(f"Evidence file changed: {path}")
            evidence["sha256"] = actual

    def _invalidate(self, identifiers: set[str], *, origin: str, reason: str, include_origin: bool = False) -> list[str]:
        affected = set(identifiers)
        if not include_origin:
            affected.discard(origin)
        for identifier in sorted(affected):
            entity = self.get_entity(identifier)
            entity["review"] = {"status": "pending", "reason": reason, "dependency": origin,
                                "previous_review": entity.get("review")}
            if entity["status"] != "refuted":
                entity["status"] = "review"
            self._save_entity(entity, action="dependency_invalidated")
        targets = affected | {origin}
        for identifier in sorted(targets):
            for table, key in (("uft_coverage", "dimension"), ("uft_assessments", "criterion")):
                for row in list(self.db.execute(f"SELECT rowid,data FROM {table} WHERE entity_id=?", (identifier,))):
                    data = json.loads(row["data"])
                    if data.get("invalidated_by") == origin and data.get("status") == "Pendiente":
                        continue
                    data.update(previous_status=data["status"], status="Pendiente", invalidated_by=origin,
                                invalidation_reason=reason, updated=now())
                    self.db.execute(f"UPDATE {table} SET data=? WHERE rowid=?", (canonical_json(data), row["rowid"]))
                    self._history(identifier, "coverage_invalidated" if key == "dimension" else "assessment_invalidated", data)
        for row in list(self.db.execute("SELECT id,data FROM uft_links")):
            link = json.loads(row["data"])
            if link["status"] != "rejected" and ({link["source"], link["target"]} & targets):
                link.update(status="review", invalidated_by=origin, invalidation_reason=reason)
                self.db.execute("UPDATE uft_links SET data=?,content_sha256=? WHERE id=?",
                                (canonical_json(link), fingerprint(link), row["id"]))
                self._history(row["id"], "link_invalidated", link)
        return sorted(affected)

    def _upsert_entity(self, raw: dict, *, audited_import: bool = False) -> dict:
        entity = validate_entity(raw)
        if entity["status"] in {"proven", "formal"} and not audited_import:
            raise ValueError("Proven/formal records require import_claim from an audited ScientificMemory")
        self._check_artifacts(entity)
        try:
            existing = self.get_entity(entity["id"])
        except KeyError:
            existing = None
        if existing and existing["status"] == "refuted" and entity["status"] != "refuted":
            raise ValueError("A refuted claim cannot be promoted; a materially different proposal needs a new ID")
        if existing and not set(existing["conditional_on"]).issubset(entity["conditional_on"]):
            raise ValueError("Conditional premises cannot be erased from an existing claim ID; use a separately justified new result")
        self._check_dependencies(entity)
        duplicate_ids = [r[0] for r in self.db.execute(
            "SELECT id FROM uft_entities WHERE statement_sha256=? AND id!=? ORDER BY id",
            (statement_fingerprint(entity["statement"]), entity["id"]))]
        if existing and fingerprint(entity) == existing["content_sha256"]:
            return {"entity": existing, "changed": False, "affected": [], "duplicates": duplicate_ids}
        downstream = self._reachable(self._arcs(), entity["id"]) if existing else set()
        if existing:
            content_keys = ("statement", "hypotheses", "dependencies", "conditional_on", "evidence", "sources", "domain")
            content_changed = any(existing.get(k) != entity.get(k) for k in content_keys)
            if content_changed and not audited_import and entity["status"] != "refuted":
                entity["reported_status"] = entity["status"]
                entity["status"] = "review"
                entity["review"] = {"status": "pending", "reason": "Scientific content changed",
                                    "previous_review": existing.get("review")}
        saved = self._save_entity(entity, action="entity_revised" if existing else "entity_created")
        affected = self._invalidate(downstream, origin=entity["id"], reason="Dependency content or status changed") if existing else []
        if duplicate_ids:
            self._alert("duplicate:" + fingerprint([entity["id"], duplicate_ids]), {
                "kind": "operational", "priority": "medium", "objectives": entity["objectives"],
                "change": "An obvious duplicate statement was detected", "source": entity["id"],
                "scientific_status": saved["status"], "dependents": [],
                "consequence": "Records remain distinct; equivalence is not established by textual similarity",
                "recommended_action": "Compare hypotheses and merge only after review", "analysis": entity["id"],
            })
        if saved["status"] == "refuted" and (not existing or existing["status"] != "refuted"):
            self._alert("refuted:" + entity["id"] + ":" + saved["content_sha256"], {
                "kind": "scientific", "priority": "high", "objectives": entity["objectives"],
                "change": "A documented refutation was registered", "source": entity["id"],
                "scientific_status": "refuted", "dependents": affected,
                "consequence": "The claim cannot support a proved conclusion",
                "recommended_action": "Inspect the counterexample and dependent claims", "analysis": entity["id"],
            })
        if affected:
            self._alert("impact:" + entity["id"] + ":" + saved["content_sha256"], {
                "kind": "scientific", "priority": "high", "objectives": entity["objectives"],
                "change": "A dependency changed; transitive results require revalidation", "source": entity["id"],
                "scientific_status": saved["status"], "dependents": affected,
                "consequence": "Affected results, links, coverage and assessments are pending review",
                "recommended_action": "Reconstruct affected arguments using the new dependency revision",
                "analysis": entity["id"],
            })
        for contrary in entity["contradicts"]:
            self._alert("contradiction:" + fingerprint(sorted([entity["id"], contrary])), {
                "kind": "scientific", "priority": "high", "objectives": entity["objectives"],
                "change": "A possible explicit contradiction was reported", "source": entity["id"],
                "scientific_status": "review", "dependents": [contrary],
                "consequence": "Incompatible statements require common hypotheses to be checked",
                "recommended_action": "Identify the inconsistent subset and a discriminating calculation",
                "analysis": entity["id"],
            })
        return {"entity": saved, "changed": True, "affected": affected, "duplicates": duplicate_ids}

    def upsert_entity(self, entity: dict) -> dict:
        with self._transaction():
            return self._upsert_entity(entity)

    def add_link(self, raw: dict) -> dict:
        link = validate_link(raw)
        with self._transaction():
            source, target = self.get_entity(link["source"]), self.get_entity(link["target"])
            level = link.get("transfer_level")
            if level and source["status"] in {"refuted", "review"}:
                raise ValueError("A refuted or invalidated result cannot be transferred")
            if level and target["status"] == "refuted":
                raise ValueError("A result transfer cannot promote a refuted conclusion")
            if level == "A" and source["status"] not in {"established", "proven", "formal"}:
                raise ValueError("Level A requires an established or audited source")
            if level == "B":
                if source["id"] not in target["conditional_on"]:
                    raise ValueError("Level B target must explicitly declare conditional_on the source ID")
                if target["status"] in {"established", "proven", "formal"}:
                    raise ValueError("Level B does not establish an unconditional result")
            if link["propagates"]:
                arcs = self._arcs()
                if link["source"] in self._reachable(arcs, link["target"]):
                    raise ValueError("Circular propagating dependency")
            link["source_revision"] = source["revision"]
            link["target_revision"] = target["revision"]
            checksum = fingerprint(link)
            previous = self.db.execute("SELECT content_sha256,data FROM uft_links WHERE id=?", (link["id"],)).fetchone()
            if previous:
                prior_endpoints = json.loads(previous["data"])
                if prior_endpoints["source"] != link["source"] or prior_endpoints["target"] != link["target"]:
                    raise ValueError("Link endpoints are immutable; use a new connection ID")
            if previous and previous[0] == checksum:
                return {**link, "changed": False}
            self.db.execute("INSERT INTO uft_links VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data,content_sha256=excluded.content_sha256",
                            (link["id"], canonical_json(link), checksum))
            self._history(link["id"], "link_revised" if previous else "link_created", link)
            semantic_fields = ("relation", "map", "foundation", "hypotheses", "sources", "propagates", "transfer_level", "coherence")
            prior = json.loads(previous["data"]) if previous else None
            changed_premise = prior is not None and (prior["propagates"] or link["propagates"]) and any(
                prior.get(key) != link.get(key) for key in semantic_fields)
            if prior is not None and (prior["propagates"] or link["propagates"]):
                changed_premise = changed_premise or ((prior["status"] == "rejected") != (link["status"] == "rejected"))
            newly_required = (prior is None and link["propagates"] and target["status"] in {"established", "evidence", "proven", "formal"}
                              and source["id"] not in target["dependencies"] + target["conditional_on"])
            if changed_premise or newly_required:
                affected = {target["id"]} | self._reachable(self._arcs(), target["id"])
                self._invalidate(affected, origin=link["id"], reason="Propagating connection or its hypotheses changed")
                # Return the actual persisted review state, not the pre-invalidation request.
                link = json.loads(self.db.execute("SELECT data FROM uft_links WHERE id=?", (link["id"],)).fetchone()[0])
            if link["relation"] == "incompatibility":
                self._alert("incompatibility:" + checksum, {
                    "kind": "scientific", "priority": "high", "objectives": sorted(set(source["objectives"] + target["objectives"])),
                    "change": "An incompatibility was documented", "source": link["id"],
                    "scientific_status": link["status"], "dependents": [target["id"]],
                    "consequence": link["foundation"], "recommended_action": "Check the incompatible assumptions",
                    "analysis": link["id"],
                })
            return {**link, "changed": True}

    def set_coverage(self, entity_id: str, dimension: str, item: str, status: str,
                     justification: str, evidence: list | None = None) -> dict:
        self.get_entity(entity_id)
        if dimension not in DIMENSIONS:
            raise ValueError("Unknown coverage dimension")
        status = COVERAGE_ALIASES.get(status, status)
        if status not in COVERAGE_STATES:
            raise ValueError("Unknown coverage state")
        require_text(item, "item")
        require_text(justification, "justification")
        evidence = [] if evidence is None else require_list(evidence, "evidence")
        if status == "Revisado" and not evidence:
            raise ValueError("Reviewed coverage requires concrete evidence")
        record = {"entity_id": entity_id, "dimension": dimension, "item": item, "status": status,
                  "justification": justification, "evidence": evidence,
                  "entity_revision": self.get_entity(entity_id)["revision"]}
        with self._transaction():
            previous = self.db.execute("SELECT data FROM uft_coverage WHERE entity_id=? AND dimension=? AND item=?",
                                       (entity_id, dimension, item)).fetchone()
            if previous and json.loads(previous[0]) == record:
                return record
            self.db.execute("INSERT INTO uft_coverage VALUES(?,?,?,?) ON CONFLICT(entity_id,dimension,item) DO UPDATE SET data=excluded.data",
                            (entity_id, dimension, item, canonical_json(record)))
            self._history(entity_id, "coverage_assessed", record)
        return record

    def set_assessment(self, entity_id: str, criterion: str, status: str, evidence: list,
                       limitations: str, next_check: str, *, justification: str = "") -> dict:
        entity = self.get_entity(entity_id)
        if criterion not in CRITERIA:
            raise ValueError("Unknown scientific evaluation criterion")
        status = ASSESSMENT_ALIASES.get(status, status)
        if status not in ASSESSMENT_STATES:
            raise ValueError("Unknown assessment state")
        require_list(evidence, "evidence")
        require_text(limitations, "limitations")
        require_text(next_check, "next_check")
        if status == "Cumplido en el alcance declarado" and not evidence:
            raise ValueError("An achieved criterion needs concrete evidence")
        if status == "No aplicable, con justificación":
            require_text(justification, "justification")
        record = {"entity_id": entity_id, "criterion": criterion, "label": CRITERIA[criterion],
                  "status": status, "evidence": evidence, "limitations": limitations,
                  "next_check": next_check, "justification": justification, "entity_revision": entity["revision"]}
        with self._transaction():
            previous = self.db.execute("SELECT data FROM uft_assessments WHERE entity_id=? AND criterion=?",
                                       (entity_id, criterion)).fetchone()
            if previous and json.loads(previous[0]) == record:
                return record
            self.db.execute("INSERT INTO uft_assessments VALUES(?,?,?) ON CONFLICT(entity_id,criterion) DO UPDATE SET data=excluded.data",
                            (entity_id, criterion, canonical_json(record)))
            self._history(entity_id, "criterion_assessed", record)
        return record

    def _alert(self, dedup_key: str, data: dict) -> dict:
        identifier = "ALERT-" + hashlib.sha256(dedup_key.encode()).hexdigest()[:20]
        record = {**data, "id": identifier, "date": now()}
        previous = self.db.execute("SELECT data FROM uft_alerts WHERE dedup_key=?", (dedup_key,)).fetchone()
        if previous:
            return json.loads(previous[0])
        self.db.execute("INSERT INTO uft_alerts VALUES(?,?,?,?)", (identifier, dedup_key, canonical_json(record), record["date"]))
        self._history(identifier, "alert_created", record)
        return record

    def emit_alert(self, data: dict, *, dedup_key: str | None = None) -> dict:
        for key in ("kind", "priority", "objectives", "change", "source", "scientific_status", "dependents", "consequence", "recommended_action", "analysis"):
            if key not in data:
                raise ValueError(f"Missing alert field: {key}")
        if data["kind"] not in {"scientific", "operational"} or data["priority"] not in {"low", "medium", "high", "critical"}:
            raise ValueError("Invalid alert kind/priority")
        with self._transaction():
            return self._alert(dedup_key or fingerprint(data), data)

    def ingest(self, event: dict, *, max_attempts: int = 3) -> dict:
        """Apply an event atomically; failed attempts remain retryable and bounded.

        ``entities`` are in prerequisite-first order. An invalid item rolls back
        every scientific mutation in that attempt, but retains the failed event.
        """
        require_text(event.get("source"), "event.source")
        require_text(event.get("version"), "event.version")
        if type(max_attempts) is not int or not 1 <= max_attempts <= 10:
            raise ValueError("max_attempts must be an integer between 1 and 10")
        payload = json.loads(canonical_json(event))
        identifier = payload.get("id") or "EVENT-" + fingerprint(payload)[:24]
        require_text(identifier, "event.id")
        payload["id"] = identifier
        checksum = fingerprint({k: v for k, v in payload.items() if k != "id"})
        with self._transaction():
            previous = self.db.execute("SELECT * FROM uft_events WHERE id=? OR fingerprint=?", (identifier, checksum)).fetchone()
            if previous:
                if previous["fingerprint"] != checksum:
                    raise ValueError("An event ID cannot be reused for different content/version")
                identifier = previous["id"]
                if previous["status"] == "completed":
                    return {**json.loads(previous["result"]), "idempotent": True}
                if previous["attempts"] >= previous["max_attempts"]:
                    return {"event_id": identifier, "status": "exhausted", "attempts": previous["attempts"], "changed": False, "error": previous["error"]}
            else:
                self.db.execute("INSERT INTO uft_events VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                (identifier, checksum, payload["source"], payload["version"], "pending", 0,
                                 max_attempts, canonical_json(payload), None, None, now()))
        try:
            with self._transaction():
                current = self.db.execute("SELECT * FROM uft_events WHERE id=?", (identifier,)).fetchone()
                # Another process may have completed while this caller waited.
                if current["status"] == "completed":
                    return {**json.loads(current["result"]), "idempotent": True}
                attempts = current["attempts"] + 1
                self.db.execute("UPDATE uft_events SET status='processing',attempts=?,updated=? WHERE id=?", (attempts, now(), identifier))
                entities = payload.get("entities", [payload["entity"]] if "entity" in payload else [])
                links = payload.get("links", [])
                require_list(entities, "event.entities")
                require_list(links, "event.links")
                results = [self.upsert_entity(entity) for entity in entities]
                link_results = [self.add_link(link) for link in links]
                result = {"event_id": identifier, "status": "completed", "attempts": attempts,
                          "changed": any(r["changed"] for r in results + link_results),
                          "entities": [r["entity"]["id"] for r in results],
                          "affected": sorted({key for r in results for key in r["affected"]}),
                          "duplicates": sorted({key for r in results for key in r["duplicates"]}),
                          "links": [r["id"] for r in link_results], "idempotent": False}
                self.db.execute("UPDATE uft_events SET status='completed',result=?,error=NULL,updated=? WHERE id=?",
                                (canonical_json(result), now(), identifier))
                self._history(identifier, "event_completed", result)
                return result
        except (ValueError, KeyError, TypeError, sqlite3.IntegrityError) as error:
            # Scientific mutations rolled back; the attempt itself must persist.
            with self._transaction():
                current = self.db.execute("SELECT attempts,max_attempts FROM uft_events WHERE id=?", (identifier,)).fetchone()
                attempts = current["attempts"] + 1
                status = "exhausted" if attempts >= current["max_attempts"] else "failed"
                description = f"{type(error).__name__}: {error}"
                self.db.execute("UPDATE uft_events SET status=?,attempts=?,error=?,updated=? WHERE id=?",
                                (status, attempts, description, now(), identifier))
                result = {"event_id": identifier, "status": status, "attempts": attempts,
                          "changed": False, "error": description}
                self._history(identifier, "event_failed", result)
                self._alert("event_failure:" + identifier + ":" + description, {
                    "kind": "operational", "priority": "high", "objectives": [],
                    "change": "An intake event could not be validated", "source": payload["source"],
                    "scientific_status": "review", "dependents": [], "consequence": description,
                    "recommended_action": "Repair the missing source or submit a corrected new event version",
                    "analysis": identifier,
                })
                return result

    def recover(self, event_id: str) -> dict:
        row = self.db.execute("SELECT data,max_attempts FROM uft_events WHERE id=?", (event_id,)).fetchone()
        if row is None:
            raise KeyError(event_id)
        return self.ingest(json.loads(row[0]), max_attempts=row[1])

    def import_claim(self, memory: ScientificMemory, claim_id: str, *, entity_id: str | None = None,
                      objectives: list[str], kind: str = "result") -> dict:
        """Import an already-audited core claim after rechecking its evidence.

        This reuses the GENIUS audit record and artifact schema; it does not invent
        another proof workflow or infer mathematical validity from the record.
        """
        claim = memory.get(claim_id)
        if claim["status"] not in {"proven", "formal"}:
            raise ValueError("Import a proved/formal claim only after the GENIUS audit gate")
        audit = memory.db.execute("SELECT * FROM audits WHERE id=?", (claim.get("audit_id"),)).fetchone()
        if not audit or audit["claim_id"] != claim_id or audit["revision"] != claim["revision"] or audit["verdict"] != "confirmed":
            raise ValueError("Missing confirming audit for this claim revision")
        if memory.db.execute("SELECT 1 FROM audits WHERE claim_id=? AND revision=? AND verdict!='confirmed'", (claim_id, claim["revision"])).fetchone():
            raise ValueError("Unresolved audit objection")
        memory._execution(audit["producer_execution"])
        memory._execution(audit["reviewer_execution"])
        audit_data = json.loads(audit["data"])
        for path, checksum in audit_data["artifact_hashes"].items():
            if not Path(path).is_file() or digest(path) != checksum:
                raise ValueError("Core audit evidence changed after review")
        for dependency in claim["dependencies"]:
            if memory.get(dependency)["status"] not in {"established", "evidence", "proven", "formal"}:
                raise ValueError("An audited core dependency is no longer valid")
        entity = {
            "id": entity_id or claim_id, "kind": kind, "objectives": objectives,
            "statement": claim["statement"], "hypotheses": claim["hypotheses"],
            "evidence": [{"path": str(p), "sha256": digest(p)} for p in claim["artifacts"]],
            "dependencies": claim["dependencies"], "status": claim["status"],
            "sources": claim["sources"], "conditional_on": [],
            "review": {"scope": audit["scope"], "audit_id": audit["id"],
                       "producer_execution": audit["producer_execution"], "reviewer_execution": audit["reviewer_execution"],
                       "limitations": audit_data["limitations"], "source_memory": str(memory.path),
                       "core_claim_id": claim_id, "core_revision": claim["revision"]},
        }
        if claim["status"] == "formal":
            entity["formal_verification"] = claim.get("formal_verification")
            formal = entity["formal_verification"] or {}
            for path in [*formal.get("files", []), formal.get("log", "")]:
                if not Path(path).is_file():
                    raise ValueError("Formal verification artifact is missing")
        with self._transaction():
            return self._upsert_entity(entity, audited_import=True)

    def record_comparison(self, comparison_id: str, *, claude: str | Path | None = None,
                          codex: str | Path | None = None, disagreements: list | None = None) -> dict:
        """A pair of reports is ready for cross-review, not automatically reviewed."""
        require_text(comparison_id, "comparison_id")
        reports = {}
        for environment, path in (("claude", claude), ("codex", codex)):
            if path is not None:
                file = Path(path)
                if not file.is_file():
                    raise ValueError(f"Missing {environment} report: {file}")
                reports[environment] = {"path": str(file), "sha256": digest(file)}
        if len(reports) == 2 and Path(claude).resolve() == Path(codex).resolve():
            raise ValueError("Separated development requires distinct report files")
        data = {"id": comparison_id, "reports": reports, "status": "ready_for_cross_review" if len(reports) == 2 else "pending",
                "missing": sorted({"claude", "codex"} - reports.keys()),
                "disagreements": disagreements or [], "reviewed": False,
                "limitation": "Distinct files do not establish independent contexts, models or external review"}
        with self._transaction():
            self.db.execute("INSERT INTO uft_comparisons VALUES(?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
                            (comparison_id, canonical_json(data)))
            self._history(comparison_id, "comparison_registered", data)
        return data

    def snapshot(self) -> dict[str, Any]:
        def records(table: str, order: str) -> list:
            return [json.loads(r[0]) for r in self.db.execute(f"SELECT data FROM {table} ORDER BY {order}")]
        events = []
        for row in self.db.execute("SELECT * FROM uft_events ORDER BY id"):
            item = dict(row)
            for key in ("data", "result"):
                item[key] = json.loads(item[key]) if item[key] else None
            events.append(item)
        history = []
        for row in self.db.execute("SELECT * FROM uft_history ORDER BY sequence"):
            item = dict(row)
            item["data"] = json.loads(item["data"])
            history.append(item)
        return {
            "schema_version": SCHEMA_VERSION,
            "vocabulary": {"scientific_states": SCIENTIFIC_STATES, "relations": RELATIONS,
                           "dimensions": DIMENSIONS, "coverage_states": COVERAGE_STATES,
                           "criteria": CRITERIA, "assessment_states": ASSESSMENT_STATES},
            "entities": [self.get_entity(row[0]) for row in self.db.execute("SELECT id FROM uft_entities ORDER BY id")],
            "links": records("uft_links", "id"), "coverage": records("uft_coverage", "entity_id,dimension,item"),
            "assessments": records("uft_assessments", "entity_id,criterion"),
            "alerts": records("uft_alerts", "recorded,id"), "comparisons": records("uft_comparisons", "id"),
            "events": events, "history": history,
            "limitations": ["Record validation is not mathematical proof or empirical confirmation",
                            "Internal audit and separated files do not imply independent model errors",
                            "Text duplicate detection does not decide scientific equivalence",
                            "No background execution or network requests are started by this store"],
        }

    def export(self, path: str | Path) -> dict:
        record = self.snapshot()
        write_json(path, record)
        return record
