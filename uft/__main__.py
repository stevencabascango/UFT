"""Command-line entry point for integrated, bounded research workflows."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .inventory import import_snapshot, write_json


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python3 -m uft")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--database", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Initialize from the portable scientific inventory, preserving existing edits")
    inventory = sub.add_parser("inventory", help="Refresh allowlisted canonical source provenance")
    inventory.add_argument("--brain", type=Path)
    inventory.add_argument("--master", type=Path)
    inventory.add_argument("--refresh", action="store_true")
    team = sub.add_parser("team", help="Select profiles; no model is executed by selection")
    team.add_argument("problem", nargs="?", default="LQG quantum gravity relational time gauge constraints")
    team.add_argument("--size", type=int, default=7)
    team.add_argument("--programme", choices=["googly", "unification", "quantum_gravity"], default="quantum_gravity")
    team.add_argument("--output", type=Path)
    ingest = sub.add_parser("ingest", help="Process a versioned event; scientific promotion is never automatic")
    ingest.add_argument("event", type=Path)
    inspect = sub.add_parser("show")
    inspect.add_argument("identifier")
    sub.add_parser("status")
    export = sub.add_parser("export", help="JSON, CSV, typed DOT graph and interactive local dashboard")
    export.add_argument("--output", type=Path)
    watch = sub.add_parser("watch", help="Read-only bounded file-event watcher; no paid model calls")
    watch.add_argument("--brain", type=Path)
    watch.add_argument("--master", type=Path)
    watch.add_argument("--interval", type=float, default=60)
    watch.add_argument("--max-cycles", type=int, default=1)
    watch.add_argument("--max-seconds", type=float, default=300)
    watch.add_argument("--max-files", type=int, default=64)
    watch.add_argument("--max-bytes", type=int, default=2097152)
    watch.add_argument("--quiet", action="store_true")
    render = sub.add_parser("report", help="Validate and render the mandatory eleven-section report schema")
    render.add_argument("record", type=Path)
    render.add_argument("--output", type=Path, required=True)
    science = sub.add_parser("cycle", help="Run finite scientific examples and an independent checker in distinct processes")
    science.add_argument("--output", type=Path, default=Path(".uft/cycle"))
    science.add_argument("--sympy", action="store_true")
    validate = sub.add_parser("validate")
    validate.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "inventory":
            if args.refresh:
                if args.brain is None:
                    raise ValueError("--refresh needs --brain; a missing canonical source must not erase the portable goal snapshot")
                result = import_snapshot(root, brain=args.brain, master=args.master)
            else:
                result = json.loads((root / "data/source_inventory.json").read_text(encoding="utf-8"))
        elif args.command == "team":
            from genius.catalogue import load_profiles
            from .teams import select_research_team
            result = select_research_team(load_profiles(root / "institute/registry/profiles.jsonl"), args.problem, args.size, args.programme)
            if args.output:
                write_json(args.output, result)
        elif args.command == "report":
            from .reporting import render_scientific_report
            text = render_scientific_report(json.loads(args.record.read_text(encoding="utf-8")))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            result = {"written": str(args.output), "sections": 11, "criteria": 7}
        elif args.command == "validate":
            from .validation import validate_project
            result = validate_project(root)
            if args.output:
                write_json(args.output, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["valid"] else 1
        elif args.command == "cycle":
            from .cycles import run_cycle
            result = run_cycle(root, args.output, use_sympy=args.sympy)
        else:
            from .store import ResearchStore
            from .workflow import bootstrap, export_project, run_watch
            database = args.database or root / ".uft/research.sqlite"
            with ResearchStore(database) as store:
                if args.command == "init":
                    result = bootstrap(root, store)
                elif args.command == "ingest":
                    result = store.ingest(json.loads(args.event.read_text(encoding="utf-8")))
                elif args.command == "show":
                    result = store.get_entity(args.identifier)
                elif args.command == "export":
                    result = export_project(root, store, args.output)
                elif args.command == "watch":
                    result = run_watch(root, store, brain=args.brain, master=args.master,
                                       interval=args.interval, max_cycles=args.max_cycles, max_seconds=args.max_seconds,
                                       max_files=args.max_files, max_bytes=args.max_bytes)
                    if args.quiet and result["quiet"]:
                        return 0
                else:
                    snap = store.snapshot()
                    result = {"entities": len(snap.get("entities", [])), "links": len(snap.get("links", [])),
                              "coverage_cells": len(snap.get("coverage", [])), "criteria_assessments": len(snap.get("assessments", [])),
                              "alerts": len(snap.get("alerts", [])), "database": str(database),
                              "automation": "Manual and bounded event runs; consult evidence/automation.json for actual scheduler status."}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command in {"cycle", "watch"} and result.get("successful") is False:
            return 1
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"error": str(error), "scientific_promotions": 0}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
