from pathlib import Path
import ast
import hashlib

ROOT = Path(__file__).resolve().parent
PARENT = Path('/dev/shm/macrodroid-exact-alarm-navigation/source-01/repository')
TARGET = ROOT / 'source-01/repository/tools/parity_journeys'
fixture = ROOT / 'design-01/observed-fixtures'
original = (fixture / 'original-after-exact-alarm-ok-acquisition-1-frame-2.xml').read_bytes()
candidate = (fixture / 'candidate-after-exact-alarm-ok-acquisition-1-frame-2.xml').read_bytes()
assert original == candidate
assert len(original) == 6919
assert hashlib.sha256(original).hexdigest() == '44247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e'
template = (ROOT / 'new-tests-template.py.txt').read_text()
assert template.count('__OBSERVED_OFF_XML__') == 1
data = template.replace('__OBSERVED_OFF_XML__', repr(original)).encode()
(TARGET / 'test_exact_alarm_enable_return.py').write_bytes(data)
old = (PARENT / 'tools/parity_journeys/test_exact_alarm_readiness.py').read_text()
data = (old.replace('exact fourteen-screen', 'exact sixteen-screen')
    .replace('exact_alarm_journey as alarm', 'exact_alarm_enable_return as alarm')
    .replace('exact_alarm_readiness as ready', 'exact_alarm_enable_return_readiness as ready')
    .replace('from test_exact_alarm_journey import FourteenFixture', 'from test_exact_alarm_enable_return import SixteenFixture')
    .replace('FourteenFixture', 'SixteenFixture')
    .replace('class ExactAlarmPhaseControls', 'class EnableReturnPhaseControls')
    .replace('class ExactAlarmReadinessReportControls', 'class EnableReturnReadinessReportControls')
    .replace("len(result['screens']), 14", "len(result['screens']), 16")
    .replace("result['settings_inputs'], 0", "result['settings_inputs'], 4")
    .replace("result['permission_granted']", "result['permission_api_result_observed']")
    .replace('Settings-only scope', 'visible enabled-state and return scope')
    .replace('requires schema6', 'requires schema7')
    .replace('for schema in (2, 3, 5):', 'for schema in (2, 3, 5, 6):')).encode()
(TARGET / 'test_exact_alarm_enable_return_readiness.py').write_bytes(data)
for name in ('test_exact_alarm_enable_return.py', 'test_exact_alarm_enable_return_readiness.py'):
    data = (TARGET / name).read_bytes(); ast.parse(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
