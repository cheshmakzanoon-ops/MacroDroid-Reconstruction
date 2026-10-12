#!/usr/bin/env python3
"""Derive a bounded, inactive numeric ART wrapper from the retained Widget wrapper."""
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat

BASE = Path('/dev/shm/macrodroid-day-numeric-art')
PARENT = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction/work-in-progress/widget-art/04-avd-parser-fix')
COMPILED = BASE / 'checkpoints/02-compiled-probe-and-corpus'
OUT = BASE / 'wrapper-draft-01'
SOURCE = OUT / 'source'
CORPUS_SHA = 'e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79'
SCOPE = 'All 1291 frozen DayTrigger r0 numeric/other/null-entry cases on real original and candidate APK classes; only null-entry exception class is compared, with its raw UTF16 message retained'
EXCEPTION_POLICY = {'only_kind': 'null-entry', 'class': 'java.lang.NullPointerException',
                    'message_encoding': 'null or utf16: followed by zero or more lowercase four-hex-digit code units',
                    'message_equality_required': False, 'raw_message_retained': True}


def ident(path):
    a = path.lstat(); assert stat.S_ISREG(a.st_mode), str(path)
    data = path.read_bytes(); b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(b.st_mode)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        f.write(json.dumps(value, indent=2) + '\n')


def copy(source, target):
    value = ident(source); target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f:
        f.write(source.read_bytes())
    target.chmod(value['mode']); assert ident(target) == ident(source) == value


def replace_function(text, name, replacement):
    nodes = [node for node in ast.parse(text).body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    assert len(nodes) == 1, name
    node = nodes[0]; lines = text.splitlines(keepends=True)
    return ''.join(lines[:node.lineno - 1]) + replacement.rstrip() + '\n' + ''.join(lines[node.end_lineno:])


EXPECTED_FUNCTION = '''def expected_numeric(row):
    """Independent integer arithmetic; never use a host float-to-int cast."""
    bits = int(row['rawBitsHex'], 16)
    if row['kind'] == 'null-entry':
        return 'exception:java.lang.NullPointerException'
    if row['kind'] == 'integer':
        value = bits & 0xffffffff
        if value & 0x80000000:
            value -= 1 << 32
    elif row['kind'] == 'decimal':
        exponent = (bits >> 52) & 0x7ff
        fraction = bits & ((1 << 52) - 1)
        negative = bool(bits >> 63)
        if exponent == 0x7ff:
            value = 0 if fraction else -(1 << 31) if negative else (1 << 31) - 1
        else:
            significand = fraction | (1 << 52) if exponent else fraction
            shift = (exponent if exponent else 1) - 1023 - 52
            magnitude = significand << shift if shift >= 0 else significand >> -shift
            value = -magnitude if negative else magnitude
            value = min((1 << 31) - 1, max(-(1 << 31), value))
    else:
        value = 0
    return 'value:' + str(value)
'''

OBSERVATION = r'''def observation(code, stdout: bytes, stderr: bytes, *, timed_out=False) -> dict:
    """Check every complete raw line; preserve the single declared exception message."""
    # Only LF-terminated ASCII lines belong to the Java wire protocol. The raw
    # streams remain artifacts even if decoding/framing or a case later fails.
    complete = stdout.split(b'\n')[:-1]
    prefix, exceptions = [], []
    header = bool(complete) and complete[0] == HEADER.encode('ascii')
    if header:
        for index, row in enumerate(CORPUS):
            if index + 1 >= len(complete):
                break
            raw = complete[index + 1]
            try:
                line = raw.decode('ascii', errors='strict')
            except UnicodeDecodeError:
                break
            if row['kind'] == 'null-entry':
                fields = line.split('\t')
                fixed = ['DAY_NUMERIC_ART_CASE', str(index), row['case'], row['kind'], row['rawBitsHex'],
                         'exception', 'java.lang.NullPointerException']
                if (len(fields) != 8 or fields[:7] != fixed or
                        re.fullmatch(r'null|utf16:(?:[0-9a-f]{4})*', fields[7]) is None):
                    break
                exceptions.append({'index': index, 'case': row['case'], 'class': fields[6],
                    'raw_message_encoding': fields[7], 'raw_line_hex': raw.hex()})
            elif line != CASE_LINES[index]:
                break
            prefix.append(row['case'])
    contract = (stdout.endswith(b'\n') and len(complete) == len(CORPUS) + 2 and header and
                len(prefix) == len(CORPUS) and complete[-1] == FOOTER.encode('ascii'))
    semantics = type(code) is int and code == 0 and timed_out is False and contract
    return {'completed_case_prefix': prefix, 'completed_cases': len(prefix),
            'exact_synthetic_stdout': stdout == EXPECTED_STDOUT.encode('ascii'),
            'complete_output_contract_matched': contract,
            'raw_exception_records': exceptions,
            'semantic_cases_passed': semantics, 'stderr_empty': stderr == b'',
            'diagnostic_bytes': len(stderr), 'strict_command_passed': semantics and stderr == b''}
'''

PROVENANCE_VALIDATOR = '''def validate_provenance(info: dict) -> None:
    if (not isinstance(info, dict) or info.get('schema_version') != 2 or
            info.get('main_class') != MAIN_CLASS or info.get('scope') != PROBE_SCOPE or
            info.get('target_method') != TARGET or info.get('original_method_sha256') != ORIGINAL_METHOD_SHA256 or
            info.get('candidate_helper_sha256') != HELPER_SHA256 or
            info.get('runtime_cases') != CASES or info.get('canonical_simulated_stdout_lines') != EXPECTED_LINES or
            info.get('exception_policy') != EXCEPTION_POLICY or
            info.get('android_runtime_executed_during_preparation') is not False):
        raise ProbeError('Probe provenance does not describe the frozen 1291-case preparation')
    if info.get('input_corpus') != {'bytes': CORPUS_BYTES, 'sha256': CORPUS_FILE_SHA256,
            'compact_sha256': CORPUS_SHA256, 'cases': 1291}:
        raise ProbeError('Probe provenance describes a changed input corpus')
    for key, _, size, expected in INPUT_SPECS:
        row = info['probe'] if key == 'probe' else info['apks'][key]
        if type(row.get('bytes')) is not int or row['bytes'] != size or row.get('sha256') != expected:
            raise ProbeError('Probe provenance contains another input identity: ' + key)
    row = info['probe']
    if (row.get('runtime_class') != PROBE_CLASS or row.get('runtime_class_count') != 1 or
            row.get('android_or_application_host_stub_definitions') != 0 or
            row.get('direct_android_or_application_type_references') != 0):
        raise ProbeError('Probe provenance contains additional runtime definitions or references')
'''

ADDITIONAL_TESTS = r'''
    def test_all_1291_input_rows_and_independent_expected_values_are_bound(self):
        self.assertEqual(len(probe.CORPUS), 1291)
        self.assertEqual(hashlib.sha256(json.dumps(probe.CORPUS, ensure_ascii=False,
            separators=(',', ':')).encode()).hexdigest(), probe.CORPUS_SHA256)
        expected = json.loads((probe.ROOT / 'fixtures/independent-python-expectations.json').read_bytes())
        self.assertEqual([{'case': row['case'], 'expected': probe.expected_numeric(row)}
                         for row in probe.CORPUS], expected)
        self.assertEqual(sum(row['kind'] == 'integer' for row in probe.CORPUS), 547)
        self.assertEqual(sum(row['kind'] == 'decimal' for row in probe.CORPUS), 734)

    def test_fixed_120_second_guest_has_no_case_selection_or_inventory_argument(self):
        remote = '/data/local/tmp/md-day-numeric-' + 'a' * 32
        for variant in ('original', 'candidate'):
            argv = probe.guest_argv(remote, variant, 120)
            self.assertEqual(len(argv), 10)
            self.assertEqual(argv[-1], probe.MAIN_CLASS)
            self.assertNotIn('--inventory', argv)
        for timeout in (30, 119, 121, 180, 120.0, True):
            with self.subTest(timeout=timeout), self.assertRaises(probe.ProbeError):
                probe.guest_argv(remote, 'original', timeout)

    def test_every_case_wire_field_and_numeric_lexeme_is_required(self):
        for field, replacement in enumerate(['OTHER', '1', 'wrong-case', 'decimal',
                                             'ffffffffffffffff', 'exception', '+0']):
            with self.subTest(field=field):
                lines = list(probe.EXPECTED_LINES)
                parts = lines[1].split('\t'); parts[field] = replacement
                lines[1] = '\t'.join(parts)
                observed = probe.observation(0, ('\n'.join(lines) + '\n').encode(), b'')
                self.assertFalse(observed['semantic_cases_passed'])
                self.assertEqual(observed['completed_cases'], 0)

    def test_duplicate_reordered_omitted_and_unterminated_case_rows_are_rejected(self):
        original = list(probe.EXPECTED_LINES)
        duplicate = original[:2] + [original[1]] + original[2:]
        reorder = list(original); reorder[1], reorder[2] = reorder[2], reorder[1]
        omitted = original[:2] + original[3:]
        for label, raw in [('duplicate', '\n'.join(duplicate) + '\n'),
                           ('reorder', '\n'.join(reorder) + '\n'),
                           ('omitted', '\n'.join(omitted) + '\n'),
                           ('unterminated', probe.EXPECTED_STDOUT[:-1])]:
            with self.subTest(label=label):
                self.assertFalse(probe.observation(0, raw.encode(), b'')['semantic_cases_passed'])

    def test_null_entry_exception_messages_are_lossless_and_not_required_identical(self):
        index = next(i for i, row in enumerate(probe.CORPUS) if row['kind'] == 'null-entry') + 1
        lines = list(probe.EXPECTED_LINES)
        message = 'utf16:00000009d800dc00ffff'
        lines[index] = lines[index].rsplit('\t', 1)[0] + '\t' + message
        raw = ('\n'.join(lines) + '\n').encode()
        observed = probe.observation(0, raw, b'')
        self.assertTrue(observed['semantic_cases_passed'])
        self.assertFalse(observed['exact_synthetic_stdout'])
        self.assertEqual(observed['raw_exception_records'][0]['raw_message_encoding'], message)
        self.assertEqual(observed['raw_exception_records'][0]['raw_line_hex'], lines[index].encode().hex())
        code, report, _ = self.execute(SimulatedADB(candidate_stdout=raw))
        self.assertEqual(code, 0, report.get('evidence_error'))
        self.assertNotEqual(report['executions']['original']['raw_exception_records'],
                            report['executions']['candidate']['raw_exception_records'])
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial, allow_simulated=True))

    def test_only_null_entry_may_report_exact_npe_class(self):
        index = next(i for i, row in enumerate(probe.CORPUS) if row['kind'] == 'null-entry') + 1
        bad_class = list(probe.EXPECTED_LINES)
        bad_class[index] = bad_class[index].replace('java.lang.NullPointerException', 'java.lang.IllegalStateException')
        wrong_kind = list(probe.EXPECTED_LINES)
        wrong_kind[1] = '\t'.join(wrong_kind[1].split('\t')[:5] + ['exception', 'java.lang.NullPointerException', 'null'])
        for lines in (bad_class, wrong_kind):
            self.assertFalse(probe.observation(0, ('\n'.join(lines) + '\n').encode(), b'')['semantic_cases_passed'])

    def test_incomplete_or_noncanonical_exception_message_encoding_is_rejected(self):
        index = next(i for i, row in enumerate(probe.CORPUS) if row['kind'] == 'null-entry') + 1
        for message in ('utf16:0', 'utf16:000', 'utf16:00000', 'utf16:ABCD', 'utf8:00',
                        'null ', 'None', 'utf16:000g', 'null\textra', 'null\r'):
            with self.subTest(message=message):
                lines = list(probe.EXPECTED_LINES)
                lines[index] = lines[index].rsplit('\t', 1)[0] + '\t' + message
                self.assertFalse(probe.observation(0, ('\n'.join(lines) + '\n').encode(), b'')['semantic_cases_passed'])
        for message in ('null', 'utf16:', 'utf16:0061'):
            lines = list(probe.EXPECTED_LINES)
            lines[index] = lines[index].rsplit('\t', 1)[0] + '\t' + message
            self.assertTrue(probe.observation(0, ('\n'.join(lines) + '\n').encode(), b'')['semantic_cases_passed'])

    def test_changed_rehashed_case_value_still_fails_independent_evidence_recheck(self):
        code, report, _ = self.execute()
        self.assertEqual(code, 0)
        changed = copy.deepcopy(report)
        row = next(row for row in changed['commands'] if row['label'] == 'execute-candidate')
        lines = list(probe.EXPECTED_LINES)
        parts = lines[1].split('\t'); parts[-1] = str(int(parts[-1]) + 1)
        lines[1] = '\t'.join(parts)
        raw = ('\n'.join(lines) + '\n').encode()
        folder = self.root / 'rehashed-case-value'
        shutil.copytree(self.args.output, folder)
        (folder / row['stdout']['path']).write_bytes(raw)
        row['stdout'].update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        changed['executions']['candidate']['command'] = row
        (folder / 'probe-result.json').write_text(json.dumps(changed, indent=2) + '\n')
        with self.assertRaises(probe.ProbeError):
            probe.verify_result(folder, changed, serial=self.args.serial, allow_simulated=True)
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial, allow_simulated=True))

    def test_host_inventory_branch_is_never_android_runtime_evidence(self):
        raw = (probe.ROOT / 'fixtures/original-host-input-inventory.stdout.txt').read_bytes()
        observed = probe.observation(0, raw, b'')
        self.assertFalse(observed['semantic_cases_passed'])
        self.assertEqual(observed['completed_cases'], 0)
        code, report, simulator = self.execute(SimulatedADB(original_stdout=raw))
        self.assertEqual(code, 2)
        self.assertEqual(simulator.executions, ['original'])
        self.assertFalse(report['android_runtime_executed'])

    def test_corpus_exception_policy_and_scope_are_mandatory_provenance_fields(self):
        original = self.inputs['provenance']['content']
        for key, value in [('input_corpus', {}), ('exception_policy', {}), ('scope', 'all features'),
                           ('schema_version', 1), ('canonical_simulated_stdout_lines', [])]:
            with self.subTest(key=key), self.assertRaises(probe.ProbeError):
                probe.validate_provenance({**original, key: value})
'''


def main():
    OUT.mkdir(exist_ok=False); SOURCE.mkdir()
    copy(Path(__file__), OUT / 'executed-author.py')
    parents = {name: ident(PARENT / name) for name in ['android_widget_method_probe.py',
               'test_android_widget_method_probe.py', 'fixtures/observed-avd-name-crlf.stdout.txt']}
    assert parents['android_widget_method_probe.py']['sha256'] == '4738616dd655fd74832b501b95390ae744c7c6050fbb3d16f17bf78300aec541'
    assert parents['test_android_widget_method_probe.py']['sha256'] == '1793d2b79bdf23aa44c4cfb1abd8bb999cae9a8c476e9bafda69d6ffcf3f8e43'
    assert ident(COMPILED / 'checkpoint.json')['sha256'] == 'e3c67ab9f469e39b637cba2efd0ca6bd1a0892e49cc6333638b0b6aab66fd5ad'
    for name in parents:
        copy(PARENT / name, OUT / 'parents' / name)
    copy(COMPILED / 'checkpoint.json', OUT / 'compiled-checkpoint.json')
    compiled = json.loads((COMPILED / 'checkpoint.json').read_bytes())
    for row in compiled['files']:
        assert ident(COMPILED / row['path']) == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
    corpus_path = COMPILED / 'evidence/exact-input-corpus.json'
    corpus = json.loads(corpus_path.read_bytes()); ci = ident(corpus_path)
    assert len(corpus) == 1291 and hashlib.sha256(json.dumps(corpus, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest() == CORPUS_SHA
    scope = {}; exec(EXPECTED_FUNCTION, scope)
    expected = scope['expected_numeric']
    assert [{'case': row['case'], 'expected': expected(row)} for row in corpus] == json.loads((COMPILED / 'evidence/independent-python-expectations.json').read_bytes())
    header = 'DAY_NUMERIC_ART_BEGIN\tcases=1291\tsha256=' + CORPUS_SHA
    footer = 'DAY_NUMERIC_ART_END\tcases=1291\tpassed=true'
    lines = []
    for index, row in enumerate(corpus):
        fixed = ['DAY_NUMERIC_ART_CASE', str(index), row['case'], row['kind'], row['rawBitsHex']]
        suffix = ['exception', 'java.lang.NullPointerException', 'null'] if row['kind'] == 'null-entry' else ['value', expected(row).split(':')[1]]
        lines.append('\t'.join(fixed + suffix))
    probe_metadata = json.loads((COMPILED / 'evidence/probe-dex-metadata.json').read_bytes())
    provenance = {'schema_version': 2, 'main_class': 'recovered.probe.DayNumericMethodProbe', 'scope': SCOPE,
      'probe': {'bytes': 14108, 'sha256': probe_metadata['sha256'], 'runtime_class_count': 1,
        'runtime_class': probe_metadata['runtime_class'], 'android_or_application_host_stub_definitions': 0,
        'direct_android_or_application_type_references': 0, 'type_references': probe_metadata['typed_references']},
      'apks': {'original': {'bytes': 95725918, 'sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'},
               'candidate': {'bytes': 94683136, 'sha256': '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'}},
      'target_method': 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I',
      'original_method_sha256': '8383c90ebe3d35afa63d52cf92cd4c92b54ed4525ca0d8a31a29fe603f9eef21',
      'candidate_helper_sha256': 'b99984c0ca9128f9def8658d874f98d9a8e4529433d0f76f7f86e9e8299cc792',
      'input_corpus': {'bytes': ci['bytes'], 'sha256': ci['sha256'], 'compact_sha256': CORPUS_SHA, 'cases': 1291},
      'runtime_cases': [row['case'] for row in corpus], 'canonical_simulated_stdout_lines': [header, *lines, footer],
      'exception_policy': EXCEPTION_POLICY,
      'reflective_invalid_heap_states': ['DictionaryEntry.variable=null after valid construction', 'StringValue.textValue=null after valid construction'],
      'constructor_observation_scope': 'Getter raw bits for all 547 integer and 734 decimal target-value cases; identity of the contained object in every outer entry; both deliberate null fields read back. The nested-entry case does not separately inspect its inner numeric getter or inner contained identity.',
      'android_runtime_executed_during_preparation': False, 'compiled_checkpoint_sha256': ident(COMPILED / 'checkpoint.json')['sha256']}
    save(SOURCE / 'probes/day-numeric-method-probe.json', provenance)
    prov_sha = ident(SOURCE / 'probes/day-numeric-method-probe.json')['sha256']
    for src, dst in [(COMPILED / 'evidence/dex/classes.dex', 'probes/day-numeric-method-probe.dex'),
        (COMPILED / 'evidence/source/recovered/probe/DayNumericMethodProbe.java', 'probes/DayNumericMethodProbe.java'),
        (corpus_path, 'probes/day-numeric-inputs.json'),
        (COMPILED / 'evidence/independent-python-expectations.json', 'fixtures/independent-python-expectations.json'),
        (COMPILED / 'evidence/commands/inventory-only-jvm/stdout.txt', 'fixtures/original-host-input-inventory.stdout.txt'),
        (PARENT / 'fixtures/observed-avd-name-crlf.stdout.txt', 'fixtures/observed-avd-name-crlf.stdout.txt')]:
        copy(src, SOURCE / dst)
    parent_wrapper = (PARENT / 'android_widget_method_probe.py').read_text()
    imports = parent_wrapper[parent_wrapper.index('from __future__'):parent_wrapper.index('ROOT =')]
    device = ast.literal_eval(next(node.value for node in ast.parse(parent_wrapper).body
                                  if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EXPECTED_DEVICE' for t in node.targets)))
    constants = f'''ROOT = Path(__file__).resolve().parent
ORIGINAL_SHA256 = {provenance['apks']['original']['sha256']!r}
ORIGINAL_BYTES = 95725918
CANDIDATE_SHA256 = {provenance['apks']['candidate']['sha256']!r}
CANDIDATE_BYTES = 94683136
PROBE_SHA256 = {probe_metadata['sha256']!r}
PROBE_BYTES = 14108
PROVENANCE_SHA256 = {prov_sha!r}
PROBE_CLASS = 'Lrecovered/probe/DayNumericMethodProbe;'
MAIN_CLASS = 'recovered.probe.DayNumericMethodProbe'
TARGET = {provenance['target_method']!r}
ORIGINAL_METHOD_SHA256 = {provenance['original_method_sha256']!r}
HELPER_SHA256 = {provenance['candidate_helper_sha256']!r}
PROBE_SCOPE = {SCOPE!r}
CORPUS_SHA256 = {CORPUS_SHA!r}
CORPUS_FILE_SHA256 = {ci['sha256']!r}
CORPUS_BYTES = {ci['bytes']}
CORPUS_PATH = ROOT / 'probes/day-numeric-inputs.json'
EXCEPTION_POLICY = {EXCEPTION_POLICY!r}
APP_PROCESS = '/system/bin/app_process64'
GUEST_TIMEOUT = '/system/bin/timeout'
DEFAULT_AVD = 'MacroDroid_API35_Disposable'
EXPECTED_DEVICE = {device!r}
REMOTE_PATTERN = r'/data/local/tmp/md-day-numeric-[0-9a-f]{{32}}'
UNCLAIMED_FLAGS = ['full_runtime_1_to_1_established', 'macro_configuration_verified',
    'alarm_scheduling_verified', 'macro_execution_verified', 'ui_behavior_verified',
    'app_apk_modified', 'app_installed', 'app_ui_interaction', 'compile_only_stubs_on_classpath']
INPUT_SPECS = (('probe', 'day-numeric-method-probe.dex', PROBE_BYTES, PROBE_SHA256),
    ('original', 'original.apk', ORIGINAL_BYTES, ORIGINAL_SHA256),
    ('candidate', 'candidate.apk', CANDIDATE_BYTES, CANDIDATE_SHA256))


class ProbeError(ValueError):
    pass


'''
    load_corpus = '''
def load_corpus():
    data = CORPUS_PATH.read_bytes()
    if len(data) != CORPUS_BYTES or hashlib.sha256(data).hexdigest() != CORPUS_FILE_SHA256:
        raise ProbeError('The frozen 1291-case input corpus changed')
    rows = json.loads(data)
    encoded = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()
    if len(rows) != 1291 or hashlib.sha256(encoded).hexdigest() != CORPUS_SHA256:
        raise ProbeError('The original compact numeric input identity changed')
    return rows


CORPUS = load_corpus()
CASES = [row['case'] for row in CORPUS]
HEADER = 'DAY_NUMERIC_ART_BEGIN\\tcases=1291\\tsha256=' + CORPUS_SHA256
FOOTER = 'DAY_NUMERIC_ART_END\\tcases=1291\\tpassed=true'
CASE_LINES = []
for _index, _row in enumerate(CORPUS):
    _prefix = ['DAY_NUMERIC_ART_CASE', str(_index), _row['case'], _row['kind'], _row['rawBitsHex']]
    _suffix = (['exception', 'java.lang.NullPointerException', 'null'] if _row['kind'] == 'null-entry'
               else ['value', expected_numeric(_row).split(':')[1]])
    CASE_LINES.append('\\t'.join(_prefix + _suffix))
# This is an explicitly synthetic fixture. A real NPE message is variable and
# must be retained losslessly; only the declared null-entry class is compared.
EXPECTED_LINES = [HEADER, *CASE_LINES, FOOTER]
EXPECTED_STDOUT = '\\n'.join(EXPECTED_LINES) + '\\n'


'''
    body = parent_wrapper[parent_wrapper.index('def digest'):]
    body = body.replace('widget-method-probe', 'day-numeric-method-probe').replace('md-widget-method-', 'md-day-numeric-')
    body = body.replace('widget_cases_on_art_verified', 'numeric_cases_on_art_verified').replace('WIDGET', 'NUMERIC').replace('Widget', 'Numeric')
    body = body.replace("'schema_version': 1,", "'schema_version': 2,")
    body = body.replace("'scope': 'Eight bounded Numeric method entry/restoration/type-check cases in real original and candidate APK classes',", "'scope': PROBE_SCOPE,")
    body = body.replace("'expected_stdout'", "'synthetic_stdout_fixture'")
    wrapper = '#!/usr/bin/env python3\n"""Bounded neutral 1291-case numeric ART probe; host controls are explicitly simulated."""\n' + imports + constants + EXPECTED_FUNCTION + load_corpus + body
    wrapper = replace_function(wrapper, 'observation', OBSERVATION)
    wrapper = replace_function(wrapper, 'validate_provenance', PROVENANCE_VALIDATOR)
    wrapper = wrapper.replace("if type(timeout) is not int or not 30 <= timeout <= 180:", "if type(timeout) is not int or timeout != 120:")
    wrapper = wrapper.replace('Guest timeout must be an integer between 30 and 180 seconds', 'Guest timeout must be exactly the integer 120 seconds')
    needle = "    result['provenance'] = provenance_row\n    return result"
    assert wrapper.count(needle) == 1
    wrapper = wrapper.replace(needle, """    result['provenance'] = provenance_row
    corpus_row = stable_identity(CORPUS_PATH)
    if corpus_row['bytes'] != CORPUS_BYTES or corpus_row['sha256'] != CORPUS_FILE_SHA256:
        raise ProbeError('Local input corpus differs from the fixed original cases')
    result['input_corpus'] = corpus_row
    return result""")
    wrapper = wrapper.replace("        report['probe_artifact'] = artifact('input-probe.dex', args.probe.read_bytes())", "        report['probe_artifact'] = artifact('input-probe.dex', args.probe.read_bytes())\n        report['corpus_artifact'] = artifact('input-corpus.json', CORPUS_PATH.read_bytes())")
    wrapper = wrapper.replace("        if (report.get('status') != expected_status or report.get('serial') != serial or", "        if (report.get('schema_version') != 2 or report.get('scope') != PROBE_SCOPE or\n                report.get('status') != expected_status or report.get('serial') != serial or")
    wrapper = wrapper.replace("        provenance = report['inputs_before']['provenance']", "        corpus = report['inputs_before']['input_corpus']\n        if corpus.get('sha256') != CORPUS_FILE_SHA256 or type(corpus.get('bytes')) is not int or corpus['bytes'] != CORPUS_BYTES:\n            raise ProbeError('Input corpus identity differs')\n        provenance = report['inputs_before']['provenance']")
    wrapper = wrapper.replace("                ('probe_artifact', 'input-probe.dex', PROBE_SHA256),", "                ('probe_artifact', 'input-probe.dex', PROBE_SHA256),\n                ('corpus_artifact', 'input-corpus.json', CORPUS_FILE_SHA256),")
    ast.parse(wrapper)
    (SOURCE / 'android_day_numeric_method_probe.py').write_text(wrapper)
    parent_tests = (PARENT / 'test_android_widget_method_probe.py').read_text()
    tests = parent_tests.replace('android_widget_method_probe', 'android_day_numeric_method_probe').replace('widget-method-probe', 'day-numeric-method-probe')
    tests = tests.replace('widget-art-host-control-', 'day-numeric-art-host-control-').replace('WidgetProbeControls', 'NumericProbeControls')
    tests = tests.replace('widget_cases_on_art_verified', 'numeric_cases_on_art_verified').replace('WIDGET', 'NUMERIC')
    # Retain the parent's two-case timeout and three-case partial checks with the
    # newly mandatory header included in their deliberately incomplete outputs.
    tests = tests.replace('probe.EXPECTED_LINES[:2]', 'probe.EXPECTED_LINES[:3]')
    tests = tests.replace("value = probe.observation(0, ('\\n'.join(probe.EXPECTED_LINES[:3])", "value = probe.observation(0, ('\\n'.join(probe.EXPECTED_LINES[:4])")
    tests = tests.replace("['completed_cases'], 8)", "['completed_cases'], 1291)")
    needle = "        self.inputs = {\n"
    assert tests.count(needle) == 1
    tests = tests.replace(needle, needle + "            'input_corpus': {'path': str(probe.CORPUS_PATH.resolve()), 'bytes': probe.CORPUS_BYTES, 'sha256': probe.CORPUS_FILE_SHA256},\n")
    assert tests.count("\n\nif __name__ == '__main__':") == 1
    tests = tests.replace("\n\nif __name__ == '__main__':", ADDITIONAL_TESTS + "\n\nif __name__ == '__main__':")
    ast.parse(tests)
    (SOURCE / 'test_android_day_numeric_method_probe.py').write_text(tests)
    inherited = [node.name for node in ast.walk(ast.parse(parent_tests)) if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
    final = [node.name for node in ast.walk(ast.parse(tests)) if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
    assert set(inherited) <= set(final) and len(final) == len(set(final))
    (OUT / 'wrapper-derivation.patch').write_text(''.join(difflib.unified_diff(parent_wrapper.splitlines(True), wrapper.splitlines(True), fromfile='parent/android_widget_method_probe.py', tofile='source/android_day_numeric_method_probe.py')))
    (OUT / 'controls-derivation.patch').write_text(''.join(difflib.unified_diff(parent_tests.splitlines(True), tests.splitlines(True), fromfile='parent/test_android_widget_method_probe.py', tofile='source/test_android_day_numeric_method_probe.py')))
    save(OUT / 'control-inheritance.json', {'inherited_names': inherited, 'new_names': sorted(set(final) - set(inherited)),
         'total_named_controls': len(final), 'executed': False,
         'scope': 'All parent control names retained; target/provenance/corpus names and header offsets adapted. No unchanged-test-body claim.'})
    save(OUT / 'parents-before.json', parents)
    after = {name: ident(PARENT / name) for name in parents}; assert parents == after
    save(OUT / 'parents-after.json', after)
    (OUT / 'README.md').write_text('''# Inactive numeric ART wrapper source draft

This source adapts the retained bounded Widget runtime wrapper to the exact 1,291-case neutral numeric probe. It changes the target, two APK identities, compiled DEX/provenance, strict numeric output contract and declared scope. The original 60-command successful sequence, disposable AVD identity/late-option guards, read-only device classpath, before/after hashes, separate processes, early stop on a failed original and owned cleanup remain in place. The timeout is narrowed to the fixed integer 120 seconds.

The copied input corpus is independently pinned and retained with the evidence. Its original compact identity is unchanged. Every case index, name, kind, raw bits and observed integer lexeme must match in fixed order, with exact LF framing and exact header/footer. A null-entry target exception must have exactly the NPE class. Its message is preserved as raw UTF16 code units and is not required identical across compilers. No other exception or case is normalized. The canonical stdout stored in provenance/report is explicitly a synthetic fixture with a null message; actual case success does not assert identical messages.

All 547 integer and 734 decimal target-value cases read back the real getter bits. Every outer entry checks its contained object identity, and the two deliberately invalid null-field states are read back. The nested-entry case does not separately check its inner numeric getter or inner identity. The target only inspects the outer contained type for that case. These limits refine the wording of the earlier source-design README without rewriting it.

The Java source and compiled DEX remain unchanged. This draft has only been authored and parsed for Python syntax. It has not run the wrapper controls, Android, any application build, UI interaction or alarms. All 31 parent control names are retained, with ten additional numeric output/corpus/exception controls. Actual execution counts belong to later evidence. No workflow or active source is changed here.
''')
    rows = [{'path': p.relative_to(OUT).as_posix(), **ident(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    save(OUT / 'checkpoint.json', {'schema': 1, 'status': 'INACTIVE_NUMERIC_ART_WRAPPER_SOURCE_DRAFT_NOT_EXECUTED',
         'repo_target': 'work-in-progress/day-numeric-art/03-wrapper-source-draft',
         'created_utc': datetime.now(timezone.utc).isoformat(), 'active_files': [],
         'android_executed': False, 'host_controls_executed': False, 'application_build_executed': False,
         'compiled_parent_sha256': ident(COMPILED / 'checkpoint.json')['sha256'],
         'named_host_controls': len(final), 'files': rows})
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **ident(OUT / 'checkpoint.json'),
                      'payloads': len(rows), 'bytes': sum(row['bytes'] for row in rows), 'host_controls': len(final)}))


if __name__ == '__main__':
    main()
