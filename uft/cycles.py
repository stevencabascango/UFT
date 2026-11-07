"""Execute producer/checker artifacts with bounded subprocesses and real logs."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from .inventory import utc_now, sha256, write_json


def run_cycle(root: Path, output: Path, *, use_sympy=False) -> dict:
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    execution_group = output.name + "-" + uuid.uuid4().hex[:12]
    python = shutil.which("scipython") if use_sympy else sys.executable
    if not python:
        raise ValueError("--sympy requires scipython; install the optional scientific environment explicitly")
    commands = [
        ("producer", [python, str(root / "scripts/science_examples.py"), "--output", str(output / "producer.json")] + (["--sympy"] if use_sympy else [])),
        ("independent_checker", [python, str(root / "scripts/independent_science_audit.py"), "--output", str(output / "independent.json"), "--producer", str(output / "producer.json")]),
    ]
    records = []
    for role, command in commands:
        artifact = output / ("producer.json" if role == "producer" else "independent.json")
        # A failed new process cannot inherit the success artifact of an old run.
        if artifact.exists():
            raise ValueError("Cycle output already contains results; select a new output directory to preserve provenance")
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=90)
        checked = None
        if role == "independent_checker" and artifact.is_file():
            checked = json.loads(artifact.read_text(encoding="utf-8"))
        verified = role != "independent_checker" or (checked is not None and checked.get("passed") is True
                                                     and checked.get("producer_artifact", {}).get("comparison", {}).get("passed") is True
                                                     and checked.get("producer_artifact", {}).get("sha256") == sha256(output / "producer.json"))
        record = {"execution_id": execution_group + "-" + role, "role": role, "backend": "deterministic_local_program",
                  "llm": False, "command": command, "returncode": result.returncode,
                  "stdout": result.stdout[:15000], "stderr": result.stderr[:15000], "completed_utc": utc_now(),
                  "artifact": str(artifact), "artifact_sha256": sha256(artifact) if artifact.is_file() else None,
                  "comparison_verified": verified if role == "independent_checker" else None,
                  "status": "completed" if result.returncode == 0 and artifact.is_file() and verified else "failed"}
        records.append(record)
        write_json(output / (role + "-execution.json"), record)
        if record["status"] != "completed":
            break
    report = {"id": output.name, "successful": len(records) == 2 and all(r["status"] == "completed" for r in records),
              "executions": records, "scientific_status": "finite symbolic or numerical evidence; mathematical review recorded separately",
              "registered_profiles": 5000, "llm_agents_executed_by_this_command": 0,
              "separation": "Two different implementations and subprocesses; not external peer review or formal proof.",
              "model_comparison": "pending unless both separately sealed model reports exist",
              "scientific_promotions": 0, "completed_utc": utc_now()}
    write_json(output / "cycle.json", report)
    return report
