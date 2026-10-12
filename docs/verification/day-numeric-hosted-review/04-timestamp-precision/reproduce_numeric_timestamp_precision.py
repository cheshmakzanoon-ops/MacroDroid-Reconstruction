"""Read-only deterministic timestamp-boundary study against the failed job source."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import sys

root = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-timestamp-review')
root.mkdir(exist_ok=False)
source = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-run-38232050667/extracted/job-source/tools/day_numeric_acceptance')
sys.dont_write_bytecode = True
before = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in ('verify.py', 'inputs.py', 'pins.json')}
assert before['verify.py'] == 'e58525d32a71170f08520caf18c4d6cfc67b4bc87d7e18f692322dac4a886a39'
sys.path.insert(0, str(source))
import verify

epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
base = datetime(2026, 10, 12, 9, 46, 48, tzinfo=timezone.utc)
def integer_ns(value):
    delta = value.astimezone(timezone.utc) - epoch
    return ((delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds) * 1000

rows = []
for microseconds in range(1000):
    value = base + timedelta(microseconds=microseconds)
    text = value.isoformat()
    exact = integer_ns(value)
    observed = verify.epoch_ns(text)
    rows.append({'iso': text, 'exact_encoded_ns': exact, 'old_epoch_ns': observed,
                 'error_ns': observed - exact})
nonzero = [row for row in rows if row['error_ns']]
assert nonzero and any(row['error_ns'] > 0 for row in rows) and any(row['error_ns'] < 0 for row in rows)

recorded = base.replace(microsecond=123456)
floor = integer_ns(recorded)
true_child_end = floor + 900
true_wrapper_finish = floor + 950
old_completion = verify.epoch_ns(recorded.isoformat())
truncation = {'recorded_finished_utc': recorded.isoformat(),
              'exact_encoded_microsecond_floor_ns': floor,
              'synthetic_actual_child_end_ns': true_child_end,
              'synthetic_actual_wrapper_finish_ns': true_wrapper_finish,
              'true_child_end_precedes_true_wrapper_finish': true_child_end < true_wrapper_finish,
              'old_converted_completion_ns': old_completion,
              'literal_old_end_le_completion': true_child_end <= old_completion,
              'integer_conversion_alone_end_le_floor': true_child_end <= floor,
              'precision_note': 'The fixed synthetic instants differ within one microsecond and encode the same ISO microsecond; this does not assert an actual measured nanosecond time for the hosted failure.'}
assert truncation['true_child_end_precedes_true_wrapper_finish'] and not truncation['literal_old_end_le_completion']
after = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in before}
assert before == after
result = {'schema': 1, 'status': 'DETERMINISTIC_TIMESTAMP_PRECISION_LIMIT_REPRODUCED',
          'source_binding': before, 'source_unchanged': before == after,
          'scope': 'Exact old epoch_ns function and its completion predicate, not a full acceptance replay',
          'iso_values_checked': len(rows), 'inexact_conversions': len(nonzero),
          'minimum_float_error_ns': min(r['error_ns'] for r in rows),
          'maximum_float_error_ns': max(r['error_ns'] for r in rows),
          'first_positive_error': next(r for r in rows if r['error_ns'] > 0),
          'first_negative_error': next(r for r in rows if r['error_ns'] < 0),
          'separate_iso_precision_counterexample': truncation,
          'app_build_or_android_executed': False}
(root / 'conversion-results.json').write_text(json.dumps(rows, indent=2) + '\n')
(root / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
(root / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
print(json.dumps(result))
