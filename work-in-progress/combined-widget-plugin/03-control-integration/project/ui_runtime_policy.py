"""Keep host UI exception messages stable at the measured HotSpot boundary.

This does not alter the APK or normalize log strings. A warmed-up reflection call
site can otherwise omit a generated NPE message while direct Java retains it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

JVM_FLAGS = ("-XX:-OmitStackTraceInFastThrow", "-XX:+ShowCodeDetailsInExceptionMessages")
EXPECTED = {"OmitStackTraceInFastThrow": False, "ShowCodeDetailsInExceptionMessages": True}


def parse_effective_flags(text: str) -> dict[str, bool]:
    observed = {}
    for name, expected in EXPECTED.items():
        rows = re.findall(r"^\s*bool\s+" + re.escape(name) + r"\s*=\s*(true|false)\s+.*$", text, re.M)
        if len(rows) != 1:
            raise RuntimeError("Missing or ambiguous effective UI JVM flag: " + name)
        observed[name] = rows[0] == "true"
        if observed[name] is not expected:
            raise RuntimeError("Unexpected effective UI JVM flag: " + name)
    return observed


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(reports: Path) -> dict:
    """Record the actual Java/VM identities and reject an ineffective flag policy."""
    reports.mkdir(parents=True, exist_ok=True)
    output = reports / "ui-runtime-policy.json"
    output.unlink(missing_ok=True)
    java = shutil.which("java")
    if java is None:
        raise RuntimeError("Java is unavailable for the required UI runtime policy")
    executable = Path(java).resolve(strict=True)
    vm = executable.parent.parent / "lib/server/libjvm.so"
    if not vm.is_file():
        raise RuntimeError("The measured HotSpot VM library is unavailable")
    argv = [str(executable), *JVM_FLAGS, "-XX:+PrintFlagsFinal", "-version"]
    log = reports / "ui-runtime-policy.log"
    with log.open("w") as stream:
        stream.write("COMMAND: " + json.dumps(argv) + "\n")
        stream.flush()
        completed = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT, timeout=30)
    if completed.returncode != 0:
        raise RuntimeError("Unable to verify the UI runtime policy")
    flags = parse_effective_flags(log.read_text())
    result = {"passed": True, "androidRuntime": False,
              "scope": "Host UI exception runtime only; unchanged APK and exact injected messages",
              "java_executable": str(executable), "java_sha256": digest(executable),
              "vm_library": str(vm), "vm_library_sha256": digest(vm),
              "argv": argv, "effective_flags": flags,
              "log": log.name, "log_sha256": digest(log)}
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result
