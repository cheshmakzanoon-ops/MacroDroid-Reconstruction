#!/usr/bin/env python3
"""Freeze the unchanged-classpath experiment and its five-input host policy fix."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tarfile

from prepare_signed_study import copy_checked, now, record, require, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    experiment = source / "reports/jvm-exception-flag-01"
    correction = source / "reports/signed-integration-06-runtime-policy"
    before = source / "reports/jvm-exception-default-observation"
    measured = json.loads((experiment / "result.json").read_text())
    fixed = json.loads((correction / "result.json").read_text())
    preparation = json.loads((correction / "preparation.json").read_text())
    root = Path(preparation["private_project"])
    require(measured["passed"] is True and measured["cases"] == 20818 and measured["failed_cases"] == 0
            and measured["inputs_unchanged"] is True and measured["same_execution_inventory_and_original_coverage"] is True,
            "The unchanged classpath flag study is not positive")
    require(fixed["passed"] is True and fixed["apk_unchanged"] is True and fixed["application_input_changes"] == [],
            "Host-only correction failed")
    require(json.loads((experiment / "inputs-before.json").read_text()) == json.loads((experiment / "inputs-after.json").read_text()),
            "The full 901-file classpath/fixture/APK binding changed")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    files = []

    def add(path, relative):
        files.append({"path": relative, **copy_checked(path, output / relative)})

    for folder, name in ((experiment, "unchanged-ui-experiment"), (correction, "policy-installation"), (before, "default-flags")):
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                add(path, name + "/" + path.relative_to(folder).as_posix())
    for row in fixed["changed_inputs"]:
        require(record(root / row["path"]) == {"bytes": row["after"]["size"], "sha256": row["after"]["sha256"]},
                "Installed policy source changed")
        add(root / row["path"], "project/" + row["path"])
    for name in ("jvm_exception_flag_study.py", "install_runtime_policy.py", "run_signed_proof.py", "freeze_runtime_policy.py"):
        add(source / name, name)
    pin = root / "reports/release-input-snapshot.json"
    pin_identity = record(pin)
    archive = output / "input-snapshot.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=6) as target:
        target.add(pin, arcname="project/reports/release-input-snapshot.json", recursive=False)
    with tarfile.open(archive, "r:gz") as target:
        members = target.getmembers()
        require(len(members) == 1 and members[0].isfile() and members[0].name == "project/reports/release-input-snapshot.json"
                and members[0].size == pin_identity["bytes"]
                and hashlib.sha256(target.extractfile(members[0]).read()).hexdigest() == pin_identity["sha256"],
                "Compressed input manifest differs")
    files.append({"path": archive.name, **record(archive)})
    (output / "README.md").write_text("""# Explicit host UI exception runtime policy

The default HotSpot runtime had fast-throw stack/message omission enabled. In the
full UI suite its warmed-up reflection call site logged a null NPE message, while
the direct Java call retained a helpful message. The earlier complete failed
report is preserved in `06-corrected-message-failure`; no failure was rewritten.

The unchanged full UI harness passed all 20,818 cases across nine methods and
three paths when `-XX:-OmitStackTraceInFastThrow` was supplied. All 901 bound files
(APK, fixtures, classpath code and critical source inputs), method/case inventory,
and original instruction/branch coverage stayed identical. Exact raw messages
from all three paths are retained. The narrow existing message normalizer and
its injected/external lookalike cases were not changed.

Five host test/acceptance inputs now consistently apply and verify that flag plus
explicit `-XX:+ShowCodeDetailsInExceptionMessages`. Both the positive UI command,
all deliberate UI mutations and final restoration receive the same policy. The
effective runtime report records the Java binary, HotSpot library, effective
flags and raw command output. Six focused policy rejection tests pass. Full
acceptance also requires fresh hashes for both new oracle-conformance reports
and the runtime-policy report.

Application inputs and the signed `b79b0010…` APK remain unchanged. The new input
pin is `00634710968ddf2fcd7400699ea3c1bb179209ff13e8062d28e64dc098fd7c99`
(81,266 files). The exact manifest is retained in `input-snapshot.tar.gz`.
The final full signed five-gate rerun is separate and pending in this checkpoint.
""")
    files.append({"path": "README.md", **record(output / "README.md")})
    checkpoint = {"status": "UNCHANGED_UI_FLAG_EXPERIMENT_PASSED_HOST_POLICY_INSTALLED",
                  "frozen_utc": now(), "cases": 20818, "methods": 9, "paths": 3,
                  "bound_files_unchanged": 901, "policy_adversarial_tests_passed": 6,
                  "changed_host_inputs": fixed["changed_paths"], "application_input_changes": [],
                  "normalization_changed": False, "apk_changed": False, "android_executed": False,
                  "full_signed_rerun_passed": False, "input_snapshot_sha256": fixed["input_snapshot_after"],
                  "input_manifest": pin_identity, "input_manifest_archive": record(archive), "files": files}
    write(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **record(output / "checkpoint.json"), "files": len(files)}, indent=2))


if __name__ == "__main__":
    main()
