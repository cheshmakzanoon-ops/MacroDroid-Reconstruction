import copy
import json
from pathlib import Path
import sys
sys.path[:0] = [sys.argv[1], sys.argv[2], sys.argv[3]]
import verify_trigger_journey as verifier
import exact_alarm_enable_return as alarm
import exact_alarm_enable_return_readiness as readiness
positive = {'schema': 7, 'plan': alarm.expected_plan(), 'plan_sha256': alarm.PLAN_SHA256,
            alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY), readiness.POLICY_KEY: copy.deepcopy(readiness.POLICY)}
verifier.require_workflow_policies(positive)
controls = []
for label in ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-readiness', 'changed-readiness',
              'missing-navigation', 'changed-navigation', 'nested-navigation', 'changed-plan', 'changed-plan-hash']:
    value = copy.deepcopy(positive)
    if label == 'legacy-schema': value['schema'] = 6
    elif label == 'unregistered-schema': value['schema'] = 8
    elif label == 'boolean-schema': value['schema'] = True
    elif label == 'missing-readiness': del value[readiness.POLICY_KEY]
    elif label == 'changed-readiness': value[readiness.POLICY_KEY]['max_seconds'] = 11
    elif label == 'missing-navigation': del value[alarm.POLICY_KEY]
    elif label == 'changed-navigation': value[alarm.POLICY_KEY]['settings_inputs_total'] = 1
    elif label == 'nested-navigation': value['unexpected'] = {alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY)}
    elif label == 'changed-plan': value['plan'][-1][1] = 'com.example.foreign'
    elif label == 'changed-plan-hash': value['plan_sha256'] = '0' * 64
    try:
        verifier.require_workflow_policies(value)
    except Exception as error:
        if not any(text in str(error) for text in ['Missing or altered notification readiness policy',
                                                  'Missing, altered or misplaced exact-alarm enable/return policy or plan']):
            raise
        controls.append({'label': label, 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Workflow policy substitution accepted: ' + label)
verifier.require_workflow_policies(positive)
result = {'passed': True, 'android_executed': False,
          'scope': 'Required complete plan and both policy formats only; compare separately requires complete raw evidence and every command role.',
          'positive_and_restore': True, 'negative_controls': controls}
Path(sys.argv[4]).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
