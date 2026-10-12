#!/usr/bin/env python3
"""Freeze the closed plugin/runtime integration proof without editing a Git checkout."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--combined", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    w, combined, dest = args.workspace.resolve(), args.combined.resolve(), args.destination.resolve()
    repo, source, runtime = w / "MacroDroid-Reconstruction", w / "current/MacroDroid_v9", w / "runtime-forward"
    dest.mkdir(parents=True, exist_ok=False)
    evidence = Path("docs/verification/plugin-runtime-integration")
    base_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    baseline_paths: dict[str, str | None] = {}

    def copy(src: Path, relative: Path | str, expected: str | None = None) -> None:
        relative = Path(relative)
        assert not relative.is_absolute() and ".." not in relative.parts
        assert src.is_file() and not src.is_symlink(), src
        actual = digest(src)
        if expected is not None:
            assert actual == expected, (str(src), actual, expected)
        target = dest / relative
        assert not target.exists(), target
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        assert digest(target) == actual
        prior = repo / relative
        baseline_paths[str(relative)] = digest(prior) if prior.is_file() else None

    old = json.loads((repo / "project/reports/release-input-snapshot.json").read_text())
    new = json.loads((source / "reports/release-input-snapshot.json").read_text())
    assert old["snapshot_sha256"] == "8c8999f971f61def792cdf4ecd7999220c2fa2e56a5bdfecf3b04dee113bf7b0"
    assert new["snapshot_sha256"] == "19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183"
    assert new["files"] == len(new["entries"]) == 81245
    assert digest(source / "reports/release-input-snapshot.json") == "713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883"
    assert digest(combined / "reports/release-input-snapshot.json") == digest(source / "reports/release-input-snapshot.json")
    assert not (set(old["entries"]) - set(new["entries"]))
    changed = sorted(p for p, record in new["entries"].items() if old["entries"].get(p) != record)
    assert len(changed) == 54
    for path in changed:
        record = new["entries"][path]
        assert (source / path).stat().st_size == record["size"]
        assert digest(combined / path) == record["sha256"], path
        prior = repo / "project" / path
        if prior.exists():
            assert old["entries"].get(path, {}).get("sha256") == digest(prior), path
        copy(source / path, Path("project") / path, record["sha256"])
    copy(source / "reports/release-input-snapshot.json", "project/reports/release-input-snapshot.json")

    status = source / "RECONSTRUCTION_STATUS.md"
    text = status.read_text()
    text = text.replace(
        "**The plugin lookup recovery passed its isolated signed three-path proof and all 37 UI fault controls. The integrated checkpoint has passed 259 Python checks. Fresh combined APK/host verification is in progress; its next hosted full acceptance and newly added Android scopes remain pending. Whole-application 1:1 runtime parity is not established.**",
        "**The integrated checkpoint passed all five planned clean build/code/resource/host/integrity checks, including 188,791 three-path cases across all 1,240 methods and 259 Python tests. It reproduced the isolated signed plugin candidate exactly. The isolated plugin proof also passed all 37 UI fault controls. The next hosted full acceptance and newly added Android scopes remain pending. Whole-application 1:1 runtime parity is not established.**")
    text = text.replace("The isolated plugin candidate that the integrated build must reproduce is", "The freshly built integrated hybrid APK is")
    anchor = "## Completed hosted source acceptance\n"
    inserted = (
        "## Fresh combined host proof\n\n"
        "A separate, fully hash-checked copy of all 81,245 pinned inputs passed hybrid assembly, complete hybrid bytecode verification, resource verification, the complete original/JVM/signed-DEX host suite, and final input integrity. All five command logs and ten declared fresh report hashes were independently rechecked against the closed output files. The build checked 71,267 classes and 349,972 method definitions, with exactly 1,240 intended body changes and zero unexpected changes. Resource verification preserved all 23,854 IDs: 7,211 of 7,212 files were byte-identical, with only the documented equivalent enum-order difference.\n\n"
        "The complete [combined evidence](../docs/verification/plugin-runtime-integration/) retains every report, merge receipt, source-copy inventory and exact artifact identity. This run passed 259 Python tests and 188,791 cases over all three execution paths. The separate integrated Android-tooling host suite passed all 27 tests. No Android device was executed by either host run; the forthcoming 16-gate workflow and post-intro/ART measurements have their own acceptance results.\n\n")
    assert anchor in text
    text = text.replace(anchor, inserted + anchor, 1)
    status.write_text(text)
    for name in ["ANDROID_ACCEPTANCE.md", "FOLLOWON_ASSESSMENT.md", "PLUGIN_RECOVERY.md", "RECONSTRUCTION_STATUS.md", "RUNTIME_CAPTURE.md", "UI_RECOVERY.md"]:
        copy(source / name, Path("project") / name)

    rt = json.loads((runtime / "reports/runtime-tools-checkpoint.json").read_text())
    assert digest(runtime / "reports/runtime-tools-checkpoint.json") == "4587be10a5ef1a6df2e3794762144da6729b8817c325cf0313f2bf78fb490b0f"
    for record in json.loads((runtime / "reports/runtime-tools-baseline.json").read_text())["files"]:
        assert digest(repo / record["path"]) == record["sha256"], record["path"]
    for record in rt["files"]:
        assert (runtime / record["path"]).stat().st_size == record["bytes"]
        assert digest(runtime / record["path"]) == record["sha256"]
        if record["path"].startswith(("tools/", ".github/")):
            copy(runtime / record["path"], record["path"], record["sha256"])
    ri = json.loads((runtime / "integration/checkpoint.json").read_text())
    assert ri["complete_tooling_tests"] == 27
    for record in ri["files"]:
        assert digest(runtime / record["path"]) == record["sha256"]
    for record in ri["docs"]:
        assert digest(dest / record["repository_path"]) == record["final"]["sha256"]

    result = json.loads((combined / "reports/combined-integration-01/result.json").read_text())
    assert result["passed"] and len(result["commands"]) == 5
    verified_logs = []
    for record in result["commands"]:
        assert record["passed"] and record["exit_code"] == 0
        assert digest(combined / record["log"]) == record["log_sha256"]
        verified_logs.append({"path": record["log"], "sha256": record["log_sha256"]})
    for path, expected in result["fresh_report_sha256"].items():
        assert digest(combined / "reports" / path) == expected, path
    parity = json.loads((combined / "reports/java-all-path-parity.json").read_text())
    assert parity["passed"] and parity["cases"] == 188791 and parity["methodsCovered"] == 1240
    assert parity["paths"] == 3 and parity["failedCases"] == parity["unsupportedExecutions"] == 0
    assert re.search(r"Ran 259 tests in [\d.]+s\s+OK\s*$", (combined / "reports/python-unit-tests.log").read_text())
    apk = combined / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    assert apk.stat().st_size == result["apk"]["bytes"] == 94683497
    assert digest(apk) == result["apk"]["sha256"] == "9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2"
    shutil.copyfile(apk, source / "dist/MacroDroid-5.67.8-v9-hybrid.apk")
    assert digest(source / "dist/MacroDroid-5.67.8-v9-hybrid.apk") == digest(apk)

    def archive(root: Path, name: str) -> dict:
        files = [p for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
        records = []
        target = dest / evidence / (name + ".tar.gz")
        target.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(target, "w:gz", compresslevel=6) as tar:
            for path in files:
                assert not path.is_symlink()
                relative = path.relative_to(root)
                record = {"path": str(relative), "bytes": path.stat().st_size, "sha256": digest(path)}
                records.append(record)
                tar.add(path, arcname=str(relative), recursive=False)
        with tarfile.open(target, "r:gz") as tar:
            assert len(tar.getmembers()) == len(records)
            for member, record in zip(tar.getmembers(), records):
                assert member.isfile() and member.name == record["path"] and member.size == record["bytes"]
                assert hashlib.sha256(tar.extractfile(member).read()).hexdigest() == record["sha256"]
        inventory = {"files": records, "file_count": len(records), "expanded_bytes": sum(r["bytes"] for r in records), "archive_bytes": target.stat().st_size, "archive_sha256": digest(target)}
        write_json(dest / evidence / (name + "-inventory.json"), inventory)
        return {k: v for k, v in inventory.items() if k != "files"}

    combined_archive = archive(combined / "reports", "complete-combined-reports")
    runtime_archive = archive(runtime, "complete-runtime-forward")
    compact = sorted(set(result["fresh_report_sha256"]) | {"combined-integration-01/result.json", "java-core-three-path-parity.json", "java-engine-three-path-parity.json", "java-environment-three-path-parity.json", "java-three-path-parity.json"})
    for path in compact:
        copy(combined / "reports" / path, evidence / "reports" / path)
    for name in ["combined-isolated-checkout.json", "plugin-integration-merge.json", "constructor-integration-merge.json", "post-intro-integration-merge.json", "combined-integration-python-01.log", "constructor-active-integration-tests.log"]:
        copy(source / "reports" / name, evidence / "integration" / name)
    copy(Path(__file__).resolve(), evidence / "freeze_checkpoint.py")
    write_json(dest / evidence / "verification-recheck.json", {"status": "ALL_CLOSED_EVIDENCE_HASHES_MATCH", "checked_utc": datetime.now(timezone.utc).isoformat(), "command_logs": verified_logs, "fresh_report_sha256": result["fresh_report_sha256"], "apk": result["apk"], "source_snapshot_sha256": new["snapshot_sha256"], "scope": "Hash and schema checks on the actual closed outputs; not a new execution of those commands"})

    readme = (repo / "README.md").read_text()
    readme = readme.replace("contains 1,239 recovered Java method bodies across 602 classes", "contains 1,240 recovered Java method bodies across 603 classes", 1)
    readme = readme.replace(
        "results are recorded below. The latest hosted checkpoint passed all 16 source\nacceptance gates and exact cold-launch/four-page intro still comparisons.\nThe [verification workflow](.github/workflows/reconstruction.yml) rebuilds the\ncommitted source and separately measures Android cold launches and four English\nintro pages; its",
        "results are recorded below. The new combined checkpoint passed all five planned\nclean host/artifact checks and reproduced its signed candidate exactly. Its full\nhosted acceptance and new Android measurements remain pending. The previous\n1,239-body checkpoint passed all 16 hosted source gates and exact cold-launch/\nfour-page intro still comparisons. The [verification workflow](.github/workflows/reconstruction.yml)\nrebuilds the committed source and separately measures cold launch, four English\nintro pages, the observed post-intro surface, and a bounded ART constructor probe; its")
    readme = readme.replace("94,683,342 bytes, SHA-256\n`be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.", "94,683,497 bytes, SHA-256\n`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.", 1)
    readme = readme.replace("## What has actually passed\n\n", "## What has actually passed\n\nThe active 1,240-body plugin/runtime checkpoint passed five clean integration\nchecks: fresh signed hybrid assembly, complete code and resource verification,\nthe full three-path host suite, and final source-input integrity. It ran 188,791\ncases with zero mismatches or unsupported executions, and 259 Python tests. The\nseparate integrated Android-tooling suite passed 27 host tests. Every closed report\nand source-merge receipt is retained in [the combined evidence](docs/verification/plugin-runtime-integration/).\nThe matching isolated plugin proof also passed all 37 UI deliberate-fault controls.\nIts new full hosted acceptance and Android scopes are not yet measured.\n\n", 1)
    readme = readme.replace("The combined 1,239-body scene, recorder and device-helper checkpoint", "The previous combined 1,239-body scene, recorder and device-helper checkpoint", 1)
    readme = readme.replace("| Current source checkpoint on GitHub |", "| Previous hosted 1,239-body source checkpoint |", 1)
    readme = readme.replace("| Current hosted UI deliberate-fault checks |", "| Previous hosted UI deliberate-fault checks |", 1)
    readme = readme.replace("| Current source", "| Current source")
    table_anchor = "| --- | --- | --- |\n"
    current_rows = "| Active combined host/artifact proof | All five planned checks; 188,791 three-path cases across 1,240 bodies; 259 Python tests; exact signed candidate reproduced | [Complete combined evidence](docs/verification/plugin-runtime-integration/) |\n| Isolated plugin lookup proof | 3,053 cases; all 198 instructions and 34 conditional edges; all 37 UI fault controls and clean restoration | [Signed plugin checkpoint](work-in-progress/plugin-lookup/04-signed-proof/) |\n"
    readme = readme.replace(table_anchor, table_anchor + current_rows, 1)
    readme = readme.replace("Successful 16-gate hosted source acceptance for the current 1,239-body scene/runtime checkpoint.", "Successful 16-gate hosted source acceptance for the previous 1,239-body scene/runtime checkpoint.")
    readme = readme.replace("| `docs/verification/source-ci-95077fc/`", "| `docs/verification/plugin-runtime-integration/` | Active 1,240-body source merge, five-check clean proof, complete reports and new Android-tooling host checks. |\n| `docs/verification/source-ci-95077fc/`", 1)
    (dest / "README.md").write_text(readme)
    baseline_paths["README.md"] = digest(repo / "README.md")

    transfer = (repo / "docs/TRANSFER_STATUS.md").read_text()
    transfer = transfer.replace("artifacts/current/`; it is 94,683,342 bytes with SHA-256\n`be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.", "artifacts/current/`; it is 94,683,497 bytes with SHA-256\n`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.", 1)
    transfer = transfer.replace("## Latest scene and runtime checkpoint\n\nThe active overlay now contains", "## Previous scene and runtime checkpoint\n\nThat checkpoint introduced", 1)
    transfer += (
        "\n## Active plugin and runtime integration\n\n"
        "The active overlay contains 1,240 recovered bodies across 603 classes. Its 81,245 build/test inputs have canonical SHA-256 `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`. The exact input-manifest file SHA-256 is `713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883`. The [integration checkpoint](verification/plugin-runtime-integration/checkpoint.json) preserves the 54 changed build/test inputs, six current project documents, eight Android tooling/workflow files and full evidence archives. The prior scene APK remains preserved by its manifest and historical commits.\n\n"
        "All five planned clean integration checks passed: hybrid assembly, full code/resource verification, all three-path host suites, and final unchanged-input verification. The fresh APK reproduced the already preserved final plugin candidate exactly. Actual counts were 188,791 cases, 1,240 methods, zero mismatches/unsupported executions and 259 Python tests. The independent integrated Android-tooling host suite passed all 27 tests. The original plugin checkpoint's 37 deliberate-fault controls retain their isolated scope.\n\n"
        "The guarded constructor-owner facility is now integrated with zero active mappings and zero applied corrections in all three build/static/linkage gates. Fresh-generation compiler staging and the reviewed post-intro recorder are also active. The updated workflow requests full source acceptance and actual cold/intro/post-intro measurements plus a separate bounded ART allocation probe. Those new hosted outcomes remain pending at this freeze. No Widget recovery or plugin-upload body is activated by this integration, and no whole-application 1:1 claim is made.\n")
    (dest / "docs/TRANSFER_STATUS.md").parent.mkdir(parents=True, exist_ok=True)
    (dest / "docs/TRANSFER_STATUS.md").write_text(transfer)
    baseline_paths["docs/TRANSFER_STATUS.md"] = digest(repo / "docs/TRANSFER_STATUS.md")

    proof_readme = """# Plugin and runtime integration: closed host proof

This checkpoint activates the reviewed plugin lookup recovery, fresh-generation build staging, guarded constructor-owner support with zero active mappings, and post-intro Android capture/tooling. It preserves all prior measurements under their original source and APK identities.

The source pin covers 81,245 files, canonical SHA-256 `19ea47f8563262c2551d11632bfc404eb68819f332ececdf68d0a686643c183`. The exact canonical value is also machine-readable in `checkpoint.json` and the active `project/reports/release-input-snapshot.json`; use those checked values for automation.

## Actual combined result

The clean private source copy passed all five commands between 03:04:59 and 03:17:13 UTC on 12 October 2026: hybrid assembly, whole hybrid code comparison, resources, all three-path host tests, and final input integrity. The fresh signed APK is 94,683,497 bytes, SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`, exactly matching the earlier isolated plugin candidate.

| Measurement | Result |
| --- | --- |
| Original instructions / recovered JVM / signed rebuilt DEX | 188,791 cases over all 1,240 registered bodies; zero mismatches and unsupported executions |
| UI scope | 18,476 cases over eight bodies, with 14,552 independent expected-result checks |
| New plugin body | 3,053 cases covering all 198 original instructions and all 34 conditional edges |
| Whole signed hybrid round trip | 71,267 classes, 349,972 methods, exactly 1,240 intended body changes; no unexpected changes |
| Resource comparison | 7,212 expected and actual files; 7,211 byte-identical, one equivalent enum-order difference; all 23,854 resource IDs preserved |
| Python tests in the actual clean host run | 259 passed |
| Integrated Android-tooling host tests | 27 passed; no Android executed by this host suite |
| Guarded constructor support | Zero active rules and zero corrections reported in build/static/linkage gates |

`complete-combined-reports.tar.gz` contains every closed report and command log, including the exact input snapshot. Its inventory pins every extracted member and the whole compressed file. `reports/` exposes the main results directly. `verification-recheck.json` records the independent checks of all five command-log hashes, ten declared fresh-report hashes, and the exact APK identity. `integration/` retains the source-copy hash inventory, merge receipts and parent host-check logs.

`complete-runtime-forward.tar.gz` preserves all authored runtime/tooling files, patches, baselines, synthetic controls, reviewed constructor provenance, the actual 27-test integration result and documentation verification. Its per-member inventory is separate. The active source/tooling paths are also individually listed in the checkpoint's file manifest with baseline hashes for conflict-safe publication.

## Scope

This is a five-command combined proof, not a completed 16-gate acceptance run or an Android result. The separate final plugin checkpoint previously passed all 37 UI deliberate-fault controls and clean restoration; those controls were not rerun by this five-command integration. The next hosted workflow runs the complete configured source acceptance plus device capture and the independent constructor probe. Cold launch and four intro stills already matched for the earlier `be1138a5…` candidate under its recorded environment. New post-intro and ART scopes remain pending here.

No full Widget body, plugin-upload body, real external API, coroutine scheduler, macro feature journey, animation-motion comparison, native source, or publisher signing identity is established by this checkpoint. Preserved smali and native payload still implement most of the application.
"""
    proof_readme = proof_readme.replace("19ea47f8563262c2551d11632bfc404eb68819f332ececdf68d0a686643c183", new["snapshot_sha256"])
    (dest / evidence / "README.md").write_text(proof_readme)
    files = []
    for path in sorted(dest.rglob("*")):
        if path.is_file():
            relative = str(path.relative_to(dest))
            files.append({"path": relative, "bytes": path.stat().st_size, "sha256": digest(path), "baseline_sha256": baseline_paths.get(relative)})
    checkpoint = {
        "checkpoint": "plugin-runtime-integration-01", "status": "COMBINED_FIVE_CHECKS_PASSED_HOSTED_SOURCE_AND_ANDROID_PENDING",
        "frozen_utc": datetime.now(timezone.utc).isoformat(), "repository_baseline_commit": base_head,
        "source_input_files": new["files"], "source_input_snapshot_sha256": new["snapshot_sha256"],
        "source_manifest_file_sha256": digest(source / "reports/release-input-snapshot.json"),
        "changed_build_test_inputs": len(changed), "removed_paths": [],
        "registered_java_bodies": 1240, "registered_java_classes": 603,
        "combined_commands": 5, "combined_three_path_cases": 188791, "combined_python_tests": 259,
        "integrated_android_tooling_host_tests": 27, "isolated_plugin_ui_fault_controls": 37,
        "candidate_apk": result["apk"], "candidate_parts_already_preserved": "work-in-progress/plugin-lookup/04-signed-proof (same candidate as checkpoint03)",
        "combined_report_archive": combined_archive, "runtime_forward_archive": runtime_archive,
        "full_configured_acceptance_executed_for_this_pin": False, "android_executed_for_this_pin": False,
        "full_runtime_1_to_1_established": False, "files": files,
    }
    write_json(dest / "checkpoint.json", checkpoint)
    write_json(dest / evidence / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(dest / "checkpoint.json"), "sha256": digest(dest / "checkpoint.json"), "files": len(files), "bytes": sum(r["bytes"] for r in files), "combined_archive": combined_archive, "runtime_archive": runtime_archive}, indent=2))


if __name__ == "__main__":
    main()
