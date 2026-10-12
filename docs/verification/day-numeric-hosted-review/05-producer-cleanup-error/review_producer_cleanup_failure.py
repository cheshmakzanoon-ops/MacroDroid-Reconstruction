"""Source-bound, direct-context cleanup fault; no Java/D8/Android invocation."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/producer-cleanup-review')
SOURCE = Path('/dev/shm/day-numeric-hosted-02/source-successor/project/day_numeric_dex_controls.py')
EXPECTED = '8e8c26a472c42843147d5aeca159cc48c61dd9d66ad7228059ce2d7d24808591'
ROOT.mkdir(exist_ok=False)
raw = SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
(ROOT / 'reviewed-day-numeric-dex-controls.py').write_bytes(raw)
tree = ast.parse(raw)
selected = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.name in {'command_clock', 'command_file_stat', 'CommandStreamEvidence'}]
assert len(selected) == 3
namespace = dict(datetime=datetime, timezone=timezone, hashlib=hashlib, json=json,
                 os=os, Path=Path, stat=stat, time=time)
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE), 'exec'), namespace)
Evidence = namespace['CommandStreamEvidence']


class FailingFlushAndClose:
    """Simulate a buffered writer whose flush and close both report I/O failure."""
    def __init__(self, underlying):
        self.underlying = underlying

    @property
    def closed(self):
        return self.underlying.closed

    def fileno(self):
        return self.underlying.fileno()

    def flush(self):
        raise OSError('review-only injected flush failure')

    def close(self):
        self.underlying.close()
        raise OSError('review-only injected close failure after descriptor closure')


results = []
for label, fault in [('normal-empty-streams', False), ('flush-and-close-error', True)]:
    folder = ROOT / label
    folder.mkdir()
    context = Evidence(folder, folder / 'probe.stdout.log', folder / 'probe.stderr.log')
    context.__enter__()
    if fault:
        context.handles['stderr'] = FailingFlushAndClose(context.handles['stderr'])
    error = None
    try:
        context.__exit__(None, None, None)
    except BaseException as failure:
        error = repr(failure)
    observed = dict(label=label, injected_fault=fault, error=error,
                    stdout_closed_by_producer=context.handles['stdout'].closed,
                    stderr_closed_by_producer=context.handles['stderr'].closed,
                    finished_recorded='finished' in context.value,
                    stream_evidence=context.value)
    if fault:
        assert error and not observed['stdout_closed_by_producer']
        assert observed['stderr_closed_by_producer'] and not observed['finished_recorded']
        context.handles['stdout'].close()
        observed['remaining_stdout_closed_by_reviewer_after_observation'] = True
    else:
        assert error is None and observed['stdout_closed_by_producer']
        assert observed['stderr_closed_by_producer'] and observed['finished_recorded']
        assert context.value['filesystem_bracket_complete'] is True
    (folder / 'observation.json').write_text(json.dumps(observed, indent=2) + '\n')
    results.append({key: value for key, value in observed.items() if key != 'stream_evidence'})
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
summary = dict(schema=1, status='PARTIAL_ERROR_DESCRIPTOR_CLEANUP_GAP_REPRODUCED',
               completed_utc=datetime.now(timezone.utc).isoformat(),
               source_path=str(SOURCE), source_sha256=EXPECTED,
               source_unchanged=True, cases=results,
               scope='Direct source-bound context calls with synthetic I/O errors; no child process or full verifier replay',
               application_or_android_execution=False, false_acceptance_claimed=False)
(ROOT / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
(ROOT / 'review_producer_cleanup_failure.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(summary))
