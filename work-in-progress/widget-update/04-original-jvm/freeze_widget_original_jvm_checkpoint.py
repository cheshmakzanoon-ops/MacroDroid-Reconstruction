#!/usr/bin/env python3
"""Freeze the four measured Widget studies and their exact private Java inputs."""
from __future__ import annotations

import datetime
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import tarfile


ROOT = Path(__file__).resolve().parent
STUDIES = (
    "widget-study-04-initial",
    "widget-study-04-expanded",
    "widget-study-04-original-jvm",
    "widget-study-04-final",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_checked(source: Path, target: Path, digest: str | None = None) -> None:
    digest = digest or sha(source)
    if sha(source) != digest:
        raise RuntimeError("Frozen input changed: " + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha(target) != digest or source.stat().st_ino == target.stat().st_ino:
        raise RuntimeError("Copied input mismatch or hardlink: " + str(target))


def main() -> None:
    output = ROOT / "checkpoints/04-original-jvm"
    output.mkdir(parents=True, exist_ok=False)
    final_dir = ROOT / "reports" / STUDIES[-1]
    final = json.loads((final_dir / "study.json").read_text())
    parity = json.loads((final_dir / "parity.json").read_text())
    if not (final["pass"] and parity["passed"] and parity["cases"] == 2342
            and parity["failedCases"] == 0 and parity["unsupportedExecutions"] == 0
            and parity["independentExpectedResultChecks"] == 198
            and parity["expectedResultFailures"] == 0
            and parity["fullInstructionAndConditionalCoverage"]
            and len(parity["generatedNullMessageExclusions"]) == 2):
        raise RuntimeError("Final Widget result does not meet its declared gate")
    private = Path(final["private_work"])
    final_inputs = json.loads((final_dir / "inputs.json").read_text())["files"]
    sources = []
    for row in final_inputs:
        if row["origin"] == "widget-overlay":
            copy_checked(private / row["private_copy"], output / row["path"], row["sha256"])
            sources.append({"path": row["path"], "sha256": row["sha256"],
                            "bytes": row["bytes"], "source": "exact final compiled private input"})

    for relative in ("widget_original_jvm_study.py", "WIDGET_HARNESS.md",
                     "freeze_widget_original_jvm_checkpoint.py"):
        copy_checked(ROOT / relative, output / relative)
    copy_checked(final_dir / "original-widget-method.dex", output / "tests/fixtures/original-widget-method.dex", final["fixture"]["sha256"])
    write_json(output / "tests/fixtures/widget-provenance.json", {
        "fixture": final["fixture"], "original_apk": final["original_apk"],
        "preserved_original": final["preserved_original"],
        "target_method": final["target_method"],
        "scope": "One-method fixture freshly extracted from unchanged original APK; test only, never APK input",
    })

    history = []
    for name in STUDIES:
        study_dir = ROOT / "reports" / name
        study = json.loads((study_dir / "study.json").read_text())
        inputs = json.loads((study_dir / "inputs.json").read_text())["files"]
        work = Path(study["private_work"])
        for source in sorted(study_dir.rglob("*")):
            if source.is_file():
                copy_checked(source, output / "evidence" / name / source.relative_to(study_dir))
        for row in inputs:
            copy_checked(work / row["private_copy"],
                         output / "evidence" / name / "exact-inputs" / row["path"], row["sha256"])
        p = study["parity"]
        input_map = {row["path"]: row for row in inputs}
        history.append({
            "study": name, "passed": study["pass"], "status": study["status"],
            "cases": p["cases"], "failed_cases": p["failedCases"],
            "unsupported_executions": p["unsupportedExecutions"],
            "expected_checks": p["independentExpectedResultChecks"],
            "expected_failures": p["expectedResultFailures"],
            "coverage": p["instructionCoverage"],
            "helper_sha256": input_map["source/java/recovered/ui/WidgetUpdateMethods.java"]["sha256"],
            "oracle_sha256": input_map["tests/java/BytecodeOracle.java"]["sha256"],
            "exact_private_inputs_preserved": len(inputs),
            "inputs_sha256": sha(study_dir / "inputs.json"),
            "report_sha256": sha(study_dir / "study.json"),
        })
    summary = {
        "status": "ORIGINAL_JVM_FULL_COVERAGE_PASSED_MUTANTS_AND_SIGNED_PROOF_PENDING",
        "target_method": final["target_method"], "paths": 2,
        "cases": parity["cases"], "failed_cases": 0, "unsupported_executions": 0,
        "independent_expected_checks": 198, "coverage": parity["instructionCoverage"],
        "history": history,
        "generated_message_exclusions": parity["generatedNullMessageExclusions"],
        "exact_message_controls": ["widget-injected-null-message-stays-exact", "widget-external-cast-message-stays-exact"],
        "one_injected_return_guard_case": "widget-invalid-label-injected-return",
        "host_parent_constructor_adapters": parity["hostParentConstructorAdapters"],
        "host_parent_constructor_adapter_calls": parity["hostParentConstructorAdapterCalls"],
        "scope": parity["scope"], "constructor_scope": parity["constructorScope"],
        "active_registry_changed": False, "apk_built": False, "rebuilt_compared": False,
        "android_executed": False, "deliberate_fault_controls_run": False,
    }
    write_json(ROOT / "reports/widget-harness-recovery.json", summary)
    copy_checked(ROOT / "reports/widget-harness-recovery.json", output / "evidence/widget-harness-recovery.json")
    copy_checked(ROOT / "reports/widget-ui-baseline.json", output / "evidence/widget-ui-baseline.json")

    baseline = json.loads((ROOT / "reports/widget-ui-baseline.json").read_text())
    baseline_file = Path(baseline["baseline_root"]) / baseline["path"]
    if sha(baseline_file) != baseline["baseline_sha256"]:
        raise RuntimeError("Parent UiParityTests baseline changed; merge patch requires exact baseline")
    patch = "".join(difflib.unified_diff(
        baseline_file.read_text().splitlines(keepends=True),
        (output / baseline["path"]).read_text().splitlines(keepends=True),
        fromfile="a/" + baseline["path"], tofile="b/" + baseline["path"],
    ))
    (output / "patches").mkdir()
    (output / "patches/widget-ui-parity.patch").write_text(patch)
    for path in sorted(output.rglob("*")):
        if path.is_file() and not path.is_relative_to(output / "evidence"):
            relative = path.relative_to(output).as_posix()
            if not any(row["path"] == relative for row in sources):
                sources.append({"path": relative, "sha256": sha(path), "bytes": path.stat().st_size})
    sources.sort(key=lambda row: row["path"])
    evidence = [{"path": path.relative_to(output / "evidence").as_posix(),
                 "sha256": sha(path), "bytes": path.stat().st_size}
                for path in sorted((output / "evidence").rglob("*")) if path.is_file()]
    archive = ROOT / "checkpoints/04-original-jvm-evidence.tar.gz"
    if archive.exists():
        raise RuntimeError("Evidence archive already exists")
    with tarfile.open(archive, "w:gz") as stream:
        for row in evidence:
            stream.add(output / "evidence" / row["path"], arcname=row["path"], recursive=False)
    with tarfile.open(archive, "r:gz") as stream:
        members = stream.getmembers()
        if len(members) != len(evidence):
            raise RuntimeError("Evidence archive entry count mismatch")
        by_name = {row["path"]: row for row in evidence}
        for member in members:
            data = stream.extractfile(member).read()
            row = by_name.pop(member.name)
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError("Evidence archive content mismatch: " + member.name)
        if by_name:
            raise RuntimeError("Evidence archive omitted entries")
    checkpoint = {
        "status": summary["status"], "frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Inactive Widget-only two-path proof with complete intermediate failures and exact private inputs. No active registry/APK changes.",
        "method": final["target_method"], "cases": 2342, "failed_cases": 0,
        "unsupported_executions": 0, "paths": 2, "expected_checks": 198,
        "coverage": parity["instructionCoverage"], "original_apk_sha256": final["original_apk"]["sha256"],
        "fixture": final["fixture"], "helper_sha256": history[-1]["helper_sha256"],
        "oracle_sha256": history[-1]["oracle_sha256"], "history": history,
        "merge_instructions": "Root owns helper, oracle, constructor pipeline and signed integration. Apply Widget UI patch only after baseline hash check; do not overwrite incoming plugin-upload UI changes.",
        "files": sources, "evidence_files": evidence,
        "evidence_bundle": {"path": str(archive), "bytes": archive.stat().st_size, "sha256": sha(archive)},
        "archive_members_hash_verified": True,
    }
    write_json(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"),
                      "sha256": sha(output / "checkpoint.json"), "files": len(sources),
                      "evidence_files": len(evidence), "archive": checkpoint["evidence_bundle"]}, indent=2))


if __name__ == "__main__":
    main()
