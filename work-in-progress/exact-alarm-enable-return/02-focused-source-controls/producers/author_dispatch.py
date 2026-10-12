from pathlib import Path
import ast,difflib
R=Path('/dev/shm/macrodroid-exact-alarm-enable-return');S=R/'source-01/repository/tools/parity_journeys';changes=[]
def replace(s,a,b,n=1):
 assert s.count(a)==n,(a,s.count(a),n)
 return s.replace(a,b)
p=S/'observed_journey.py';before=p.read_text();s=before
s=replace(s,'def readiness_adapter(schema=None):\n    if schema == 6',"def exact_alarm_enable_return_plan():\n    return runner.fingerprint(runner.PLAN) == 'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211'\n\n\ndef readiness_adapter(schema=None):\n    if schema == 7 or (schema is None and exact_alarm_enable_return_plan()):\n        import exact_alarm_enable_return_readiness as adapter\n    elif schema == 6")
s=replace(s,"    elif exact_alarm_plan():\n        import exact_alarm_journey as adapter", "    elif exact_alarm_enable_return_plan():\n        import exact_alarm_enable_return as adapter\n    elif exact_alarm_plan():\n        import exact_alarm_journey as adapter")
s=replace(s,'len(runner.PLAN) not in (10, 12, 13, 14)','len(runner.PLAN) not in (10, 12, 13, 14, 16)')
s=replace(s,'len(runner.PLAN) in (10, 12, 13) or exact_alarm_plan():','len(runner.PLAN) in (10, 12, 13) or exact_alarm_plan() or exact_alarm_enable_return_plan():')
s=replace(s,'len(runner.PLAN) in (12, 13) or exact_alarm_plan():','len(runner.PLAN) in (12, 13) or exact_alarm_plan() or exact_alarm_enable_return_plan():',2)
s=replace(s,'def report_policy(report):\n    import exact_alarm_journey',"def report_policy(report):\n    import exact_alarm_enable_return\n    if exact_alarm_enable_return_plan() and report.get('schema') != exact_alarm_enable_return.REPORT_SCHEMA:\n        raise runner.JourneyError('Exact-alarm enable/return requires schema7 and both declared policies')\n    if report.get('schema') != exact_alarm_enable_return.REPORT_SCHEMA and exact_alarm_enable_return.contains_evidence(report):\n        raise runner.JourneyError('Exact-alarm enable/return evidence cannot use another schema')\n    import exact_alarm_journey")
ast.parse(s);p.write_text(s);changes.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='parent/tools/parity_journeys/'+p.name,tofile='candidate/tools/parity_journeys/'+p.name))
p=S/'editor_journey.py';before=p.read_text();s=before
s=replace(s,"        import exact_alarm_journey\n        if not exact_alarm_journey.is_configured() or shot['owner'] != exact_alarm_journey.SETTINGS:\n            raise JourneyError('Invalid snapshot owner or live interval')\n        exact_alarm_journey.validate_settings_snapshot(folder, shot, proof)","        import exact_alarm_journey\n        import exact_alarm_enable_return\n        adapter = exact_alarm_enable_return if exact_alarm_enable_return.is_configured() else exact_alarm_journey\n        if not adapter.is_configured() or shot['owner'] != adapter.SETTINGS:\n            raise JourneyError('Invalid snapshot owner or live interval')\n        adapter.validate_settings_snapshot(folder, shot, proof)")
s=replace(s,"                if observed_journey.exact_alarm_plan():\n                    import exact_alarm_journey\n                    result[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY\n                    result['global_command_observations'] = exact_alarm_journey.verify_global_commands(folder, report, proof)","                if observed_journey.exact_alarm_plan() or observed_journey.exact_alarm_enable_return_plan():\n                    alarm = observed_journey.information_adapter()\n                    result[alarm.POLICY_KEY] = alarm.POLICY\n                    result['global_command_observations'] = alarm.verify_global_commands(folder, report, proof)")
s=replace(s,"    if observed_journey.exact_alarm_plan() and not args.observe_notification_readiness:","    if (observed_journey.exact_alarm_plan() or observed_journey.exact_alarm_enable_return_plan()) and not args.observe_notification_readiness:")
s=replace(s,"        if observed_journey.exact_alarm_plan():\n            import exact_alarm_journey\n            report[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY", "        if observed_journey.exact_alarm_plan() or observed_journey.exact_alarm_enable_return_plan():\n            alarm = observed_journey.information_adapter()\n            report[alarm.POLICY_KEY] = alarm.POLICY")
s=replace(s,"                if observed_journey.exact_alarm_plan():\n                    run['uninstall'] = uninstall_command", "                if observed_journey.exact_alarm_plan() or observed_journey.exact_alarm_enable_return_plan():\n                    run['uninstall'] = uninstall_command")
needle="        if result['journey_equal'] and result.get('post_crash_continuation_observed_in_both'):"
new="""            elif observed_journey.exact_alarm_enable_return_plan():
                result['scope'] = 'Observed exact-alarm Settings off state, one visible toggle, checked-on full state, one Navigate up tap and the resulting unassumed app surface'
                result['catalog_navigation_established'] = True
                result['trigger_type_tapped'] = True
                result['exact_alarm_explanation_ok_tapped'] = True
                result['settings_navigation_observed'] = True
                result['settings_inputs'] = 4
                result['settings_inputs_per_run'] = 2
                result['settings_enabled_state_observed'] = True
                result['settings_return_navigation_observed'] = True
                result['permission_api_result_observed'] = False
                result['trigger_configuration_confirmed'] = False
                result['status'] = 'EXACT_ALARM_ENABLED_RETURN_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
"""+needle
s=replace(s,needle,new)
ast.parse(s);p.write_text(s);changes.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='parent/tools/parity_journeys/'+p.name,tofile='candidate/tools/parity_journeys/'+p.name))
(R/'source-01/dispatch.patch').write_text(''.join(changes));print('two dispatch files parsed')
