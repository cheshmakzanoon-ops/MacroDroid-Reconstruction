from pathlib import Path
import ast,hashlib,json
ROOT=Path('/dev/shm/macrodroid-exact-alarm-enable-return');S=ROOT/'source-01/repository/tools/parity_journeys';D=ROOT/'design-01'
raw=(D/'settings-contract.json').read_bytes();value=json.loads(raw);assert hashlib.sha256(raw).hexdigest()=='379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07'
source=(S/'exact_alarm_journey.py').read_text();nodes={n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
global_code=nodes['verify_global_commands'].replace("terminal.get('owner') != SETTINGS", "terminal.get('owner') != runner.PACKAGE").replace('has no Settings terminal','has no app return terminal')
old="    return {'commands': len(ledger), 'unique_command_streams': len(used_paths),"
new="""    settings_roles = [(run['label'], transition['to']) for run in runs
                      for index, transition in enumerate(run['transitions'])
                      if run['screens'][index]['owner'] == SETTINGS]
    if settings_roles != [(label, name) for label in ('original', 'candidate') for name in (ENABLED, TERMINAL)]:
        raise runner.JourneyError('Settings inputs differ from the four declared toggle/return roles')
    return {'commands': len(ledger), 'unique_command_streams': len(used_paths),"""
assert old in global_code;global_code=global_code.replace(old,new).replace("'settings_inputs': 0}","'settings_inputs': len(settings_roles)}")
text=(ROOT/'adapter-template.py.txt').read_text().replace('@@CONTRACT_BYTES@@',repr(raw)).replace('@@OFF_HASH@@',value['off_hierarchy_canonical_sha256']).replace('@@ON_HASH@@',value['predicted_on_hierarchy_canonical_sha256']).replace('@@COMMAND_KIND@@',nodes['_command_kind']).replace('@@GLOBAL_COMMANDS@@',global_code)
ast.parse(text);(S/'exact_alarm_enable_return.py').write_text(text)
ready=(S/'exact_alarm_readiness.py').read_text().replace('REPORT_SCHEMA = 6','REPORT_SCHEMA = 7').replace('4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c','ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211').replace('exact_alarm_journey','exact_alarm_enable_return').replace('fourteen-screen','sixteen-screen')
ast.parse(ready);(S/'exact_alarm_enable_return_readiness.py').write_text(ready)
print('two adapters parsed')
