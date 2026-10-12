#!/usr/bin/env python3
"""Freeze the exact inactive merge preparation, including unresolved merge output."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    stage, output = args.stage.resolve(), args.output.resolve()
    state = json.loads((stage / "result.json").read_text())
    if state["status"] != "INACTIVE_SOURCE_UNION_PREPARED" or state["passed"] is not True:
        raise RuntimeError("Only a completed preparation can be frozen here")
    for row in state["files"]:
        path = stage / row["path"]
        if sha(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise RuntimeError("Prepared source changed: " + row["path"])
    output.mkdir(parents=True, exist_ok=False)
    for source in sorted(stage.rglob("*")):
        if source.is_symlink():
            raise RuntimeError("Unexpected symlink in source capsule")
        if source.is_file():
            destination = output / source.relative_to(stage)
            destination.parent.mkdir(parents=True, exist_ok=True)
            before = sha(source)
            shutil.copyfile(source, destination)
            if not sha(source) == before == sha(destination):
                raise RuntimeError("Input changed during freezing")
    for name in ("prepare_merge_overlay.py", "freeze_merge_overlay.py"):
        shutil.copyfile(Path(__file__).resolve().parent / name, output / name)
    (output / "README.md").write_text("""# Inactive combined source merge preparation

This checkpoint preserves the reviewable union of the isolated plugin-upload
and Widget recoveries. It does not change the active project or APK and is not
a build or parity result.

The 55 overlaid files retain the current strict build/runtime tools. The shared
UI harness was resolved from the exact published baseline and both frozen
branches. The raw six-conflict `git merge-file` output and the final union patch
are retained. Both families' dispatch, reset, observation, exception support,
instruction/conditional coverage and final failure conditions are present.
The Widget constructor/numeric oracle conformance remains in the test driver.

The registries propose 1,242 methods across 605 classes, with ten UI methods.
Expected case totals (not yet measured here) are 193,489 overall, 23,174 UI,
and 15,326 independent UI expected-result checks. All 37 previous controls and
17 plugin-upload controls are retained. Integration of the 24 Widget controls
is still pending.

Fresh whole-source copy verification, full original-fixture extraction and
provenance, combined compilation, signed artifact checks, full host acceptance,
actual fault controls, and Android measurements remain required. The original
and isolated fixtures are not interchangeable with the future combined fixture.
""")
    rows = [{"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
            for path in sorted(output.rglob("*")) if path.is_file()]
    checkpoint = {"status": "INACTIVE_SOURCE_UNION_FROZEN_VALIDATION_PENDING",
                  "frozen_utc": datetime.now(timezone.utc).isoformat(),
                  "scope": state["scope"], "active_source_changed": False,
                  "active_apk_changed": False, "preparation_sha256": sha(output / "result.json"),
                  "files": rows, "files_count": len(rows),
                  "files_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                  "all_prepared_members_verified": True}
    (output / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n")
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), "sha256": sha(output / "checkpoint.json"), "files": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
