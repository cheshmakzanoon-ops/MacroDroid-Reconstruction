#!/usr/bin/env python3
"""Freeze completed or failed inactive control preparation without rewriting it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

from prepare_merge_overlay import identity, require, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    stage, output = args.stage.resolve(), args.output.resolve()
    state = json.loads((stage / "result.json").read_text())
    require(state["status"] in {"COMBINED_CONTROL_OVERLAY_FAILED", "INACTIVE_COMBINED_CONTROL_OVERLAY_PREPARED"},
            "Cannot freeze running control preparation")
    output.mkdir(parents=True, exist_ok=False)

    def copy(path, destination):
        require(not path.is_symlink(), "Unexpected symlink")
        value = identity(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        require(value == identity(destination) == identity(path), "Source changed while freezing")

    for path in sorted(stage.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
            copy(path, output / path.relative_to(stage))
    for name in ("prepare_merge_overlay.py", "extend_control_overlay.py", "freeze_control_overlay.py"):
        copy(source / name, output / name)
    for path in sorted((source / "control-inputs").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy(path, output / path.relative_to(source))
    if state["passed"]:
        body = """The exact source union retains both recovered methods and the 54 previous
UI faults. The 24 frozen Widget faults are added with exact multi-edit and
occurrence-count handling; every named expected failure must be observed.
All 78 source mutations pass preflight and 14 focused runtime/catalog tests
pass. The UI runner uses the measured explicit HotSpot exception policy,
requires a positive current APK/fixture-bound baseline, retains actual mutant
source and class bytes, checks unchanged original coverage and case inventory,
and requires exact full positive restoration. No mutant was compiled or
executed by this preparation. Those actual gates remain pending.
"""
    else:
        body = """This preserves an actual failed preparation, before any mutation compilation
or execution. The initial name validator rejected the frozen catalog's literal
`leave-saved-L6-unread` name because it allowed lowercase letters only. The
catalog, helper and existing 54 faults were unchanged. No policy test, mutant
or Android action was run by this attempt. The saved result records the exact
failure; the faulty authored parser and all prepared source files are retained.
A separate numbered attempt accepts safe uppercase letters in the already
hash-pinned catalog names; this failure remains unchanged.
"""
    (output / "README.md").write_text("# Inactive combined control preparation\n\n" + body + "\nFresh full source copying, combined fixture extraction/provenance, compilation,\nsigned checks, complete host acceptance and Android measurements remain required.\nThe active source, registry and APK are unchanged by this checkpoint.\n")
    rows = [{"path": p.relative_to(output).as_posix(), **identity(p)} for p in sorted(output.rglob("*")) if p.is_file()]
    checkpoint = {"status": state["status"], "preparation_passed": state["passed"],
                  "frozen_utc": datetime.now(timezone.utc).isoformat(),
                  "active_source_changed": False, "active_apk_changed": False,
                  "compiled_mutants": 0, "executed_mutants": 0, "android_executed": False,
                  "preparation_result": identity(output / "result.json"), "files": rows,
                  "files_count": len(rows), "files_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
    write_json(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **identity(output / "checkpoint.json"), "files": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
