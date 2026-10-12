"""Reject reuse of evidence files across a complete post-onboarding session.

Equal bytes from separate observations are legitimate. Reusing the same resolved
file (including a symlink, dot alias or hard link) for two observations is not.
This validates recorded evidence bindings, not an adversarial recorder's honesty.
"""
from __future__ import annotations
from pathlib import Path
import stat
import editor_journey as runner

SNAPSHOT_KEYS = {'pid_first', 'foreground', 'hierarchy', 'screenshot', 'pid_final'}
IDENTITY_KEYS = ('package_path', 'checksum', 'pid', 'foreground')


class EvidenceLedger:
    """One ledger for both APK runs; register observation roles, not command logs."""
    def __init__(self, folder: Path, proof):
        self.folder, self.proof = Path(folder), proof
        self.paths: dict[Path, str] = {}
        self.files: dict[tuple[int, int], str] = {}

    def claim(self, record: dict, role: str) -> None:
        # Includes confinement, existence, size and SHA-256 checks.
        path = runner.artifact_path(self.folder, record, self.proof)
        metadata = path.stat()
        if not stat.S_ISREG(metadata.st_mode):
            raise runner.JourneyError('Evidence is not a regular file: ' + role)
        identity = (metadata.st_dev, metadata.st_ino)
        earlier = self.paths.get(path) or self.files.get(identity)
        if earlier is not None:
            raise runner.JourneyError('Reused session evidence: ' + role + ' aliases ' + earlier)
        self.paths[path] = role
        self.files[identity] = role

    def group(self, records: dict, expected: set[str], role: str) -> None:
        if not isinstance(records, dict) or set(records) != expected:
            raise runner.JourneyError('Unexpected session evidence group: ' + role)
        for key in sorted(expected):
            self.claim(records[key], role + '/' + key)

    def command(self, command: dict, role: str) -> None:
        for stream in ('stdout', 'stderr'):
            self.claim(command[stream], role + '/' + stream)


def verify_session_evidence(folder: Path, runs: list, start: int, proof) -> dict:
    """Register every in-scope snapshot, input and endpoint observation once.

    Summary references and the raw command journal intentionally bind the same
    bytes; those references are not treated as new observations. Capture groups,
    immediate checks, input outputs and endpoint outputs are distinct observations.
    """
    ledger = EvidenceLedger(folder, proof)
    for run in runs:
        label = run['label']
        screens = run['screens']
        for index in range(start, len(screens)):
            shot = screens[index]
            role = label + '/screen-' + str(index)
            ledger.group(shot['artifacts'], SNAPSHOT_KEYS, role)
            if index in (start, len(screens) - 1):
                identity = shot['session_identity']
                if set(identity) != {'environment', *IDENTITY_KEYS}:
                    raise runner.JourneyError('Unexpected session endpoint evidence')
                for key in IDENTITY_KEYS:
                    ledger.command(identity[key], role + '/endpoint/' + key)
            if index > start:
                transition = run['transitions'][index - 1]
                ledger.group(transition['before']['artifacts'], SNAPSHOT_KEYS, role + '/before')
                ledger.group(transition['preinput_artifacts'], {'pid', 'foreground'}, role + '/preinput')
                ledger.command(transition['command'], role + '/input')
    return {'policy': 'session-wide-resolved-path-and-file-identity-v1',
            'unique_observation_files': len(ledger.paths),
            'reused_observation_files': 0}
