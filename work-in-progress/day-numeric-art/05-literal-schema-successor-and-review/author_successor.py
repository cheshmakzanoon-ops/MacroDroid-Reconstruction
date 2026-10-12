#!/usr/bin/env python3
"""Create only two schema guards and one additional focused control from frozen 6ca."""
from __future__ import annotations

import ast
import copy
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat

OWN = Path('/dev/shm/macrodroid-day-numeric-art-schema-02')
DRAFT = Path('/dev/shm/macrodroid-day-numeric-art/wrapper-draft-01')
SOURCE = OWN / 'source'
NEW_TEST = '''
    def test_literal_integer_schema_is_required_for_provenance_and_result_replay(self):
        code, report, simulator = self.execute()
        self.assertEqual(code, 0, report.get('evidence_error'))
        self.assertEqual(simulator.executions, ['original', 'candidate'])
        self.assertEqual(len(report['commands']), 60)
        self.assertFalse(report['android_runtime_executed'])
        positive = copy.deepcopy(report)
        observations = []
        for label, version in [('integer-two', 2), ('float-two', 2.0),
                               ('string-two', '2'), ('boolean-true', True),
                               ('boolean-false', False)]:
            with self.subTest(label=label):
                changed_provenance = copy.deepcopy(self.inputs['provenance']['content'])
                changed_provenance['schema_version'] = version
                changed_report = copy.deepcopy(report)
                changed_report['schema_version'] = version
                row = {'label': label, 'schema_value': version,
                       'python_type': type(version).__name__}
                if type(version) is int:
                    probe.validate_provenance(changed_provenance)
                    self.assertTrue(probe.verify_result(self.args.output, changed_report,
                        serial=self.args.serial, allow_simulated=True))
                    row.update(provenance_accepted=True, report_replay_accepted=True)
                else:
                    with self.assertRaisesRegex(probe.ProbeError, 'frozen 1291-case') as first:
                        probe.validate_provenance(changed_provenance)
                    with self.assertRaisesRegex(probe.ProbeError, 'exact scope') as second:
                        probe.verify_result(self.args.output, changed_report,
                            serial=self.args.serial, allow_simulated=True)
                    row.update(provenance_accepted=False, report_replay_accepted=False,
                               provenance_error=str(first.exception), report_error=str(second.exception))
                observations.append(row)
                (self.args.output / 'schema-observations.json').write_text(json.dumps({
                    'scope': 'Explicit simulated positive and schema-only host controls',
                    'android_executed': False, 'observations': observations}, indent=2) + '\\n')
        self.assertEqual(report, positive)
        self.assertTrue(probe.verify_result(self.args.output, report,
            serial=self.args.serial, allow_simulated=True))
        self.assertFalse(report['numeric_cases_on_art_verified'])

'''


def identity(path):
    value = path.lstat()
    assert stat.S_ISREG(value.st_mode), str(path)
    return {'bytes': value.st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(value.st_mode)}


def save(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def test_methods(tree):
    owner = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'NumericProbeControls')
    return {n.name: ast.dump(n, include_attributes=False) for n in owner.body
            if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}


def main():
    assert identity(DRAFT / 'checkpoint.json')['sha256'] == '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6'
    assert json.loads((OWN / 'reports/counterexample-01/result.json').read_bytes())['counterexample_reproduced'] is True
    cap = json.loads((DRAFT / 'checkpoint.json').read_bytes())
    source_rows = [row for row in cap['files'] if row['path'].startswith('source/')]
    assert len(source_rows) == 9
    for row in source_rows:
        assert identity(DRAFT / row['path']) == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
    SOURCE.mkdir(exist_ok=False)
    for row in source_rows:
        destination = SOURCE / row['path'].removeprefix('source/')
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DRAFT / row['path'], destination)
        destination.chmod(row['mode'])
    wrapper = SOURCE / 'android_day_numeric_method_probe.py'
    before_wrapper = wrapper.read_text()
    old = "if (not isinstance(info, dict) or info.get('schema_version') != 2 or"
    new = "if (not isinstance(info, dict) or type(info.get('schema_version')) is not int or\n            info.get('schema_version') != 2 or"
    assert before_wrapper.count(old) == 1
    after_wrapper = before_wrapper.replace(old, new)
    old = "if (report.get('schema_version') != 2 or report.get('scope') != PROBE_SCOPE or"
    new = "if (type(report.get('schema_version')) is not int or\n                report.get('schema_version') != 2 or report.get('scope') != PROBE_SCOPE or"
    assert after_wrapper.count(old) == 1
    after_wrapper = after_wrapper.replace(old, new)
    wrapper.write_text(after_wrapper)
    tests = SOURCE / 'test_android_day_numeric_method_probe.py'
    before_tests = tests.read_text()
    marker = "\nif __name__ == '__main__':\n"
    assert before_tests.count(marker) == 1
    after_tests = before_tests.replace(marker, NEW_TEST + marker)
    tests.write_text(after_tests)
    changed = []
    bindings = []
    for row in source_rows:
        relative = row['path'].removeprefix('source/')
        before, after = identity(DRAFT / row['path']), identity(SOURCE / relative)
        bindings.append({'path': relative, 'before': before, 'after': after})
        if before != after:
            changed.append(relative)
    assert changed == ['android_day_numeric_method_probe.py', 'test_android_day_numeric_method_probe.py']
    before_ast, after_ast = ast.parse(before_wrapper), ast.parse(after_wrapper)
    normalized = copy.deepcopy(after_ast)
    guards = []
    for name, receiver in [('validate_provenance', 'info'), ('verify_result', 'report')]:
        function = next(n for n in normalized.body if isinstance(n, ast.FunctionDef) and n.name == name)
        expected = ast.dump(ast.parse("type(" + receiver + ".get('schema_version')) is not int", mode='eval').body)
        hits = 0
        for node in ast.walk(function):
            if isinstance(node, ast.BoolOp):
                selected = [n for n in node.values if ast.dump(n) == expected]
                hits += len(selected)
                node.values = [n for n in node.values if ast.dump(n) != expected]
        assert hits == 1, (name, hits)
        guards.append({'function': name, 'added_guard': expected, 'occurrences': hits})
    assert ast.dump(normalized, include_attributes=False) == ast.dump(before_ast, include_attributes=False)
    old_tests, new_tests = test_methods(ast.parse(before_tests)), test_methods(ast.parse(after_tests))
    assert len(old_tests) == 41 and len(new_tests) == 42
    assert all(new_tests[name] == value for name, value in old_tests.items())
    added = sorted(set(new_tests) - set(old_tests))
    assert added == ['test_literal_integer_schema_is_required_for_provenance_and_result_replay']
    patch = ''.join(difflib.unified_diff(before_wrapper.splitlines(True), after_wrapper.splitlines(True),
        fromfile='before/android_day_numeric_method_probe.py', tofile='source/android_day_numeric_method_probe.py'))
    patch += ''.join(difflib.unified_diff(before_tests.splitlines(True), after_tests.splitlines(True),
        fromfile='before/test_android_day_numeric_method_probe.py', tofile='source/test_android_day_numeric_method_probe.py'))
    with (OWN / 'source-successor.patch').open('x') as stream:
        stream.write(patch)
    save(OWN / 'source-bindings.json', bindings)
    save(OWN / 'ast-derivation.json', {'status': 'EXACT_TWO_SCHEMA_GUARDS_AND_ONE_ADDED_TEST',
        'changed_source_paths': changed, 'unchanged_source_paths': len(source_rows) - len(changed),
        'wrapper_ast_exact_after_removing_only_two_guards': True, 'guards': guards,
        'parent_named_test_bodies_unchanged': len(old_tests), 'final_named_test_count': len(new_tests),
        'added_test_names': added, 'build_executed': False, 'android_executed': False})
    print(json.dumps({'status': 'SOURCE_SUCCESSOR_AUTHORED', 'changed': changed,
                      'parent_test_bodies_unchanged': len(old_tests), 'new_tests': added}))


if __name__ == '__main__':
    main()
