#!/usr/bin/env python3
"""Apply exact, recorded source replacements in the owned inactive overlay."""
from __future__ import annotations
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation/source-01')
SOURCE = ROOT / 'repository/tools/parity_journeys'
changes = []

def sha(data):
    return hashlib.sha256(data).hexdigest()

def replace(text, old, new, count=1):
    if text.count(old) != count:
        raise RuntimeError('Expected replacement occurrence count differs: ' + old[:100])
    return text.replace(old, new)

def save(relative, before, after, new=False):
    path = SOURCE / relative
    if new and path.exists():
        raise RuntimeError('New source path already exists: ' + relative)
    path.write_text(after)
    patch = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                       fromfile='parent/' + relative, tofile='successor/' + relative))
    (ROOT / 'derivation' / (relative + '.patch')).write_text(patch)
    changes.append({'path': 'tools/parity_journeys/' + relative,
                    'before_sha256': None if new else sha(before.encode()),
                    'derived_from_sha256': sha(before.encode()),
                    'after_sha256': sha(after.encode()), 'new': new})

def main():
    (ROOT / 'derivation').mkdir(exist_ok=False)
    old = (SOURCE / 'notification_readiness.py').read_text()
    assert sha(old.encode()) == '08a838681c6b3ece018240d54013996bafd4204133bdd3eaa6a6c2dddeea6f85'
    new = replace(old, 'REPORT_SCHEMA = 5', 'REPORT_SCHEMA = 6')
    new = replace(new, '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb',
                  '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c')
    new = replace(new, '    import day_time_journey\n    day_time_journey.require_plan()',
                  '    import exact_alarm_journey\n    exact_alarm_journey.require_plan()')
    new = replace(new, 'Notification readiness requires the exact thirteen-screen plan',
                  'Notification readiness requires the exact new fourteen-screen plan')
    new = replace(new, 'def require_policy(report):\n    require_plan()\n',
                  'def require_policy(report):\n    require_plan()\n    import exact_alarm_journey\n'
                  '    exact_alarm_journey.require_navigation_policy(report)\n')
    save('exact_alarm_readiness.py', old, new, new=True)

    old = (SOURCE / 'observed_journey.py').read_text()
    new = replace(old, 'def information_adapter():\n',
                  "def exact_alarm_plan():\n    return runner.fingerprint(runner.PLAN) == "
                  "'4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'\n\n\n"
                  "def readiness_adapter(schema=None):\n"
                  "    if schema == 6 or (schema is None and exact_alarm_plan()):\n"
                  "        import exact_alarm_readiness as adapter\n"
                  "    else:\n        import notification_readiness as adapter\n"
                  "    return adapter\n\n\ndef information_adapter():\n")
    new = replace(new, '    elif len(runner.PLAN) == 13:\n        import day_time_journey as adapter\n',
                  '    elif len(runner.PLAN) == 13:\n        import day_time_journey as adapter\n'
                  '    elif exact_alarm_plan():\n        import exact_alarm_journey as adapter\n')
    new = replace(new, '    if len(runner.PLAN) in (10, 12, 13):\n',
                  '    if len(runner.PLAN) in (10, 12, 13) or exact_alarm_plan():\n')
    new = replace(new, '    if len(runner.PLAN) in (12, 13):\n',
                  '    if len(runner.PLAN) in (12, 13) or exact_alarm_plan():\n', count=2)
    new = replace(new, 'def report_policy(report):\n    import notification_readiness\n',
                  'def report_policy(report):\n    import exact_alarm_journey\n'
                  "    if exact_alarm_plan() and report.get('schema') != exact_alarm_journey.REPORT_SCHEMA:\n"
                  "        raise runner.JourneyError('Exact-alarm navigation requires schema6 and both declared policies')\n"
                  "    if report.get('schema') != exact_alarm_journey.REPORT_SCHEMA and exact_alarm_journey.contains_evidence(report):\n"
                  "        raise runner.JourneyError('Exact-alarm navigation evidence cannot use an older schema')\n"
                  "    notification_readiness = readiness_adapter(report.get('schema'))\n")
    save('observed_journey.py', old, new)

    old = (SOURCE / 'editor_journey.py').read_text()
    new = replace(old,
                  "    if shot['owner'] not in (PACKAGE, PERMISSION) or not proof.valid_live_interval(shot['sample_interval_seconds']):\n"
                  "        raise JourneyError('Invalid snapshot owner or live interval')\n",
                  "    if shot['owner'] not in (PACKAGE, PERMISSION):\n"
                  "        import exact_alarm_journey\n"
                  "        if not exact_alarm_journey.is_configured() or shot['owner'] != exact_alarm_journey.SETTINGS:\n"
                  "            raise JourneyError('Invalid snapshot owner or live interval')\n"
                  "        exact_alarm_journey.validate_settings_snapshot(folder, shot, proof)\n"
                  "    if not proof.valid_live_interval(shot['sample_interval_seconds']):\n"
                  "        raise JourneyError('Invalid snapshot owner or live interval')\n")
    new = replace(new, '            import notification_readiness\n',
                  "            notification_readiness = observed_journey.readiness_adapter(report['schema'])\n")
    new = replace(new, "                result['notification_readiness_policy'] = notification_readiness.POLICY\n",
                  "                result['notification_readiness_policy'] = notification_readiness.POLICY\n"
                  "                if observed_journey.exact_alarm_plan():\n"
                  "                    import exact_alarm_journey\n"
                  "                    result[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY\n")
    new = replace(new,
                  "                result['status'] = 'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n",
                  "                result['status'] = 'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n"
                  "            elif observed_journey.exact_alarm_plan():\n"
                  "                result['scope'] = 'Observed Day/Time exact-alarm explanation, one observed OK tap and the resulting Settings surface only'\n"
                  "                result['catalog_navigation_established'] = True\n"
                  "                result['trigger_type_tapped'] = True\n"
                  "                result['exact_alarm_explanation_ok_tapped'] = True\n"
                  "                result['settings_navigation_observed'] = True\n"
                  "                result['settings_inputs'] = 0\n"
                  "                result['permission_granted'] = False\n"
                  "                result['trigger_configuration_confirmed'] = False\n"
                  "                result['status'] = 'EXACT_ALARM_SETTINGS_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n")
    new = replace(new, '    args = ap.parse_args()\n',
                  '    args = ap.parse_args()\n    import observed_journey\n'
                  "    if observed_journey.exact_alarm_plan() and not args.observe_notification_readiness:\n"
                  "        ap.error('Exact-alarm navigation requires --observe-notification-readiness')\n")
    new = replace(new, '    if args.observe_notification_readiness:\n        import notification_readiness\n',
                  '    if args.observe_notification_readiness:\n'
                  '        notification_readiness = observed_journey.readiness_adapter()\n')
    new = replace(new, '                      notification_readiness_policy=notification_readiness.POLICY)\n',
                  '                      notification_readiness_policy=notification_readiness.POLICY)\n'
                  '        if observed_journey.exact_alarm_plan():\n'
                  '            import exact_alarm_journey\n'
                  '            report[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY\n')
    save('editor_journey.py', old, new)
    (ROOT / 'derivation/changes.json').write_text(json.dumps(changes, indent=2) + '\n')
    print(json.dumps({'status': 'INACTIVE_SOURCE_DERIVED', 'changes': changes}))

if __name__ == '__main__':
    main()
