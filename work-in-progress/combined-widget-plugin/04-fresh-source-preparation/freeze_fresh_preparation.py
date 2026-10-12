#!/usr/bin/env python3
"""Freeze the prepared combined source and staged workflow before acceptance."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

from prepare_merge_overlay import BASE_MANIFEST, BASE_PIN, identity, require, sha, write_json
from prepare_combined_project import copy_checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", required=True, type=Path)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    preparation = json.loads(args.preparation.read_text())
    require(preparation["passed"] is True and preparation["status"] == "PRIVATE_COMBINED_SOURCE_PREPARED", "Source preparation incomplete")
    root = Path(preparation["private_project"])
    pin_path = root / "reports/release-input-snapshot.json"
    pin = json.loads(pin_path.read_text())
    require({key: value for key, value in pin.items() if key != "entries"} == preparation["candidate_inputs"], "Candidate pin differs")
    require(hashlib.sha256(json.dumps(pin["entries"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == pin["snapshot_sha256"],
            "Candidate canonical hash differs")
    for relative, expected in pin["entries"].items():
        require(identity(root / relative) == {"bytes": expected["size"], "sha256": expected["sha256"]}, "Combined source changed: " + relative)
    baseline_path = args.base / "reports/release-input-snapshot.json"
    require(sha(baseline_path) == BASE_MANIFEST, "Baseline manifest differs")
    baseline = json.loads(baseline_path.read_text())
    require(baseline["snapshot_sha256"] == BASE_PIN, "Baseline source pin differs")
    require(not baseline["entries"].keys() - pin["entries"].keys(), "Combined source removed an input")
    changed = sorted(relative for relative, expected in pin["entries"].items() if baseline["entries"].get(relative) != expected)
    require(changed == sorted(preparation["input_delta"]["added"] + preparation["input_delta"]["changed"]), "Prepared source delta differs")
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=False)
    files = []

    def add(path, relative):
        files.append({"path": relative, **copy_checked(path, output / relative)})

    for path in sorted(args.preparation.parent.rglob("*")):
        if path.is_file():
            add(path, "preparation/" + path.relative_to(args.preparation.parent).as_posix())
    for path in sorted((source / "reports/04-prepared-documentation").rglob("*")):
        if path.is_file():
            add(path, "initial-documentation/" + path.relative_to(source / "reports/04-prepared-documentation").as_posix())
    add(source / "reports/04-documentation-table-fix.json", "documentation-table-fix.json")
    for relative in changed:
        add(root / relative, "project/" + relative)
    for relative in ("README.md", "UI_RECOVERY.md", "COMBINED_RECOVERY.md", "RECONSTRUCTION_STATUS.md"):
        add(root / relative, "project/" + relative)
    for name in ("prepare_merge_overlay.py", "prepare_combined_project.py", "run_combined_acceptance.py",
                 "update_combined_docs.py", "fix_combined_table.py", "freeze_fresh_preparation.py"):
        add(source / name, name)
    archive = output / "input-snapshot.tar.gz"
    expected = identity(pin_path)
    with tarfile.open(archive, "w:gz", compresslevel=6) as target:
        target.add(pin_path, arcname="project/reports/release-input-snapshot.json", recursive=False)
    with tarfile.open(archive, "r:gz") as target:
        members = target.getmembers()
        require(len(members) == 1 and members[0].isfile() and members[0].size == expected["bytes"]
                and hashlib.sha256(target.extractfile(members[0]).read()).hexdigest() == expected["sha256"], "Compressed input manifest differs")
    files.append({"path": archive.name, **identity(archive)})
    (output / "README.md").write_text("""# Fresh combined source prepared; full acceptance pending

All 81,245 active baseline input files were independently copied and checked
against the published pin before and after copying. No input was hardlinked and
no generated cache was copied. The frozen combined source overlay was verified
and applied, then the original-method fixture was freshly extracted from the
unchanged supplied APK for exactly 1,242 methods across 605 classes. Its actual
hash, byte size and inventory are bound in fixture provenance.

The 81,291-file candidate input pin is
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`.
Every input was independently rehashed again before this freeze. All exact
delta inputs and the compressed complete input manifest are included.

Review of the previous control runner identified an unbounded final positive
UI child. This follow-up explicitly logs that command and limits it to the same
300 seconds as every fault execution. The actual 54-control plugin gate took
1,962.871 seconds, so the combined 78-control acceptance budget is 5,400 seconds;
other gate budgets remain 1,200 seconds. Raw measured evidence and exact patches
are retained. The staged source workflow allows 120 minutes and preserves every
report and nested mutant artifact. It must only activate with the verified
combined candidate, not as a standalone current-source workflow change.

The expected combined run covers 193,489 cases, ten UI methods / 23,174 UI cases,
15,326 independent UI expectations, 273 Python tests and 78 actual UI fault
controls. Those full combined gates have not executed in this checkpoint.
The active source/APK remain unchanged. No Android or whole-app parity is claimed.
""")
    files.append({"path": "README.md", **identity(output / "README.md")})
    checkpoint = {"status": "PRIVATE_COMBINED_SOURCE_PREPARED", "frozen_utc": datetime.now(timezone.utc).isoformat(),
                  "passed": True, "input_files_rehashed": pin["files"], "input_snapshot_sha256": pin["snapshot_sha256"],
                  "input_manifest": expected, "changed_input_files": len(changed), "registry_methods": 1242,
                  "registry_classes": 605, "ui_methods": 10, "expected_cases": 193489, "expected_ui_cases": 23174,
                  "expected_ui_controls": 78, "expected_python_tests": 273,
                  "compiled": False, "full_acceptance_executed": False, "android_executed": False,
                  "active_source_changed": False, "active_apk_changed": False, "files": files}
    write_json(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **identity(output / "checkpoint.json"),
                      "files": len(files), "changed_inputs": len(changed)}, indent=2))


if __name__ == "__main__":
    main()
