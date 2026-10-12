#!/usr/bin/env python3
"""Freeze exact closed Widget D8 prerequisites as an inactive checkpoint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from prepare_signed_study import BASE_PIN, copy_checked, now, record, require, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preparation_path = args.preparation.resolve()
    preparation = json.loads(preparation_path.read_text())
    require(preparation["passed"] is True and preparation["status"] == "PRIVATE_WIDGET_D8_STATIC_LINKAGE_PASSED", "Prerequisites did not pass")
    root = Path(preparation["private_project"])
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    baseline = json.loads(args.baseline.read_text())
    candidate = json.loads((root / "reports/release-input-snapshot.json").read_text())
    require(baseline["snapshot_sha256"] == BASE_PIN and candidate["snapshot_sha256"] == preparation["candidate_inputs"]["snapshot_sha256"], "Unexpected baseline/candidate pin")
    changed = preparation["input_delta"]["added"] + preparation["input_delta"]["changed"]
    records = []

    def copy(source, relative, expected=None, baseline_sha256=None):
        value = copy_checked(source, output / relative, expected)
        records.append({"path": relative, **value, "baseline_sha256": baseline_sha256})

    for relative in sorted(changed):
        copy(root / relative, "project/" + relative, candidate["entries"][relative], baseline["entries"].get(relative, {}).get("sha256"))
    copy(root / "reports/release-input-snapshot.json", "project/reports/release-input-snapshot.json")
    copy(preparation_path, "evidence/preparation.json")
    for command in preparation["commands"]:
        require(command["returncode"] == 0 and command["timed_out"] is False, "Closed command was not positive")
        copy(preparation_path.parent / command["log"]["path"], "evidence/" + command["log"]["path"], command["log"])
    for relative in ["migration-static-proof.json", "migration-linkage-check.json", "java-staging.json",
                     "compile-build-tools.log", "javac-methods.log", "d8-methods.log", "disassemble-java-methods.log"]:
        copy(root / "reports" / relative, "evidence/" + relative)
    for relative in ["dex/classes.dex", "inputs.jar", "smali/recovered/ui/WidgetUpdateMethods.smali"]:
        copy(root / "build/java" / relative, "compiled/" + relative)
    proofs = []
    for name in ["migration-static-proof.json", "migration-linkage-check.json"]:
        report = json.loads((output / "evidence" / name).read_text())
        require(report["pass"] is True and len(report["constructor_owner_corrections"]) == 1, "Missing one-reference prerequisite proof")
        proofs.append(report["constructor_owner_corrections"][0])
    require(proofs[0] == proofs[1], "Static and linkage constructor proofs differ")
    for relative in ["prepare_signed_study.py", "run_signed_proof.py", "freeze_prerequisites.py"]:
        copy(Path(__file__).resolve().parent / relative, relative)
    readme = """# Widget D8 and linkage prerequisites: inactive checkpoint

The fresh private study copied and hash-checked all 81,245 published active inputs,
with no hardlinks or generated caches. It added the frozen Widget helper and host
boundaries, the reviewed original/JVM case harness and strict oracle, two explicit
constructor/numeric conformance fixtures, and exactly one migration registry entry.
The resulting candidate has 1,241 Java bodies across 604 classes and 9 UI methods.

All six preparation commands passed: extractor bootstrap, fresh full original
fixture extraction, candidate input recording, actual javac/D8/disassembly, static
migration validation, and linkage validation. The 81,264 candidate input files have
canonical SHA-256 `a729f01fc4b0dc136c980501c144b43769332c324f8c6f63438107d605291691`.
The full original-method fixture is test-only and is never an APK build input.

The actual D8 body uses `new-instance Lzhh;` and a non-range direct constructor
call. The guarded pipeline restores exactly one owner reference from `Lzhh;` to
the original `Lrff;-><init>(ILm73;)V`. Static validation checks 633 distinct member
references and resolves 427 application members, with no new external references
or errors. Both verifiers produce the identical source-bound correction record;
no allocated type changes and no constructor is added. The narrow guard needed no
range-call extension. Exact D8 output, input JAR, disassembly and logs are retained.

This checkpoint does not activate the method and does not contain a newly built
application APK. The five-command signed/code/resource/three-path/input-integrity
study is separate ongoing work. Method-only deliberate-fault controls, the earlier
two-path Widget study and the independently verified ART allocation probe each
retain their distinct scopes. No whole-application 1:1 result is asserted.
"""
    (output / "README.md").write_text(readme)
    records.append({"path": "README.md", **record(output / "README.md"), "baseline_sha256": None})
    checkpoint = {"status": "WIDGET_D8_STATIC_LINKAGE_PASSED_SIGNED_PROOF_PENDING", "frozen_utc": now(),
                  "baseline_input_snapshot_sha256": BASE_PIN, "source_input_snapshot_sha256": candidate["snapshot_sha256"],
                  "source_input_files": candidate["files"], "registered_methods": 1241, "registered_classes": 604,
                  "changed_build_test_inputs": len(changed), "constructor_owner_correction": proofs[0],
                  "scope": "Inactive exact Widget preparation and D8/static/linkage proof; separate signed study pending", "files": records}
    write(output / "checkpoint.json", checkpoint)
    for entry in records:
        require(record(output / entry["path"]) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}, "Frozen file recheck failed")
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **record(output / "checkpoint.json"), "files": len(records)}, indent=2))


if __name__ == "__main__":
    main()
