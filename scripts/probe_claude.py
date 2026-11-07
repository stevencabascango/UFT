#!/usr/bin/env python3
"""One bounded native-Claude availability attempt; never fabricates a report.

Uses existing authentication/configuration. Does not print credentials or change
permissions. Failure leaves cross-model comparison pending.
"""
from datetime import datetime, timezone
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidence/claude-availability.json"))
    parser.add_argument("--seconds", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 30:
        raise ValueError("Probe timeout must be 1–30 seconds")
    executable = shutil.which("claude")
    record = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "cli_available": bool(executable),
              "model": None, "max_model_attempts": 1, "max_seconds": args.seconds,
              "comparison": "pending", "scientific_claims": [], "execution_status": "unavailable"}
    if executable:
        prompt = ("Bounded availability probe, not a research report. Return only the word AVAILABLE. "
                  "No tools, file access, subagents, research or external writes. No hidden reasoning requested.")
        command = [executable, "-p", prompt, "--output-format", "json", "--tools", "",
                   "--no-session-persistence", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                   "--settings", '{"disableAllHooks":true}']
        with tempfile.TemporaryDirectory(prefix="uft-claude-probe-") as directory:
            process = subprocess.Popen(command, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, start_new_session=True)
            try:
                stdout, stderr = process.communicate(timeout=args.seconds)
                record.update(returncode=process.returncode, execution_status="completed" if process.returncode == 0 else "failed")
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
                record.update(returncode=process.returncode, execution_status="timeout")
        def redact(text):
            text = re.sub(r"(?:sk-|gh[pousr]_)[A-Za-z0-9_-]+", "[REDACTED]", text)
            return text[:5000]
        record.update(stdout=redact(stdout), stderr=redact(stderr),
                      limitations="Availability only. Even a successful probe is not an independently closed scientific report.")
        if process.returncode == 0:
            try:
                data = json.loads(stdout)
                record["model"] = data.get("model")
                record["usage_reported_by_cli"] = data.get("usage")
            except ValueError:
                pass
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("cli_available", "execution_status", "comparison")}))


if __name__ == "__main__":
    main()
