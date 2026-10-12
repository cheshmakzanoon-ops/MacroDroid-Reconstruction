"""Keep a rejecting input-command control beside both stale-capture examples."""
from pathlib import Path
import copy
import json
import sys

ROOT = Path('/workspace/scratch/4130730d15aa')
SOURCE = ROOT / 'trigger-catalog-forward/checkpoints/02-reviewed-host-success/replay-source/tools/parity_journeys'
OUT = ROOT / 'trigger-category-review'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCE))
import editor_journey as runner
import trigger_category_journey as twelve
import favourite_info_journey as ten
from test_observed_journey import proof

results = []
for name, folder, adapter in [('twelve', OUT, twelve), ('ten', OUT / 'ten-screen', ten)]:
    with adapter.configured_plan():
        original = json.loads((folder / 'mutated-synthetic-report.json').read_text())
        assert runner.compare(folder / 'synthetic-artifacts', original, proof)['journey_equal'] is True
        invalid = copy.deepcopy(original)
        invalid['runs'][1]['transitions'][-1]['command']['argv'] = ['shell', 'input tap 1 1']
        result = runner.compare(folder / 'synthetic-artifacts', invalid, proof)
        assert result['journey_equal'] is False and 'Input command differs' in result['reason'], result
        (folder / 'wrong-tap-report.json').write_text(json.dumps(invalid, indent=2) + '\n')
        (folder / 'wrong-tap-result.json').write_text(json.dumps(result, indent=2) + '\n')
        results.append(dict(scope=name, changed_field='candidate final command.argv',
                            expected='REJECTED', actual=result['status'], reason=result['reason'], android_executed=False))
(OUT / 'wrong-tap-controls.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
