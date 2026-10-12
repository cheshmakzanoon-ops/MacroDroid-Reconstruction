#!/usr/bin/env python3
"""Apply the reviewed creation-evidence contract only to the private verifier."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'source/tools/day_numeric_acceptance/verify.py'


def replace_function(text, name, replacement):
    start = text.index('def ' + name + '(')
    end = text.index('\n\ndef ', start + 4)
    return text[:start] + replacement.rstrip() + text[end:]


def main():
    raw = TARGET.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == 'e58525d32a71170f08520caf18c4d6cfc67b4bc87d7e18f692322dac4a886a39'
    text = raw.decode().replace('import shutil\n', 'import shutil\nimport stat\n', 1)
    text = text.replace('    return int(parsed.timestamp() * 1_000_000_000)',
        "    delta = parsed - datetime(1970, 1, 1, tzinfo=timezone.utc)\n    return (delta.days * 86400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1000", 1)
    text = text.replace("'mtime_ns': status.st_mtime_ns, 'ctime_ns': status.st_ctime_ns}",
        "'mtime_ns': status.st_mtime_ns, 'ctime_ns': status.st_ctime_ns,\n               'mode': status.st_mode, 'links': status.st_nlink}", 1)
    marker = '\ndef verify_execution(execution, prepared, pins):\n'
    assert text.count(marker) == 1
    text = text.replace(marker, '\n' + (ROOT / 'verify_stream_recording.py').read_text() + '\n' + marker, 1)
    text = replace_function(text, 'verify_wrapper_streams', '''def verify_wrapper_streams(execution, prepared, output):
    """Bind outer streams to exact live files and separately ordered integer clocks."""
    count(execution.get('schema'), 2, 'Wrapper creation-evidence schema differs')
    beginning = row_clock(execution, 'started', 'wrapper-start')
    completion = row_clock(execution, 'finished', 'wrapper-finish')
    clocks_ordered(beginning, completion, 'wrapper', strict=True)
    versions = execution.get('java_versions')
    inputs.require(isinstance(versions, list) and len(versions) == 2, 'Java observation inventory differs')
    expected = [('java-version', ['java', '-version'], versions[0], 15),
                ('javac-version', ['javac', '-version'], versions[1], 15),
                ('acceptance', [sys.executable, '-B', 'acceptance.py'], execution['execution'], None)]
    last = execution['execution'].get('stream_evidence', {}).get('after_witnesses')
    inputs.require(isinstance(last, list) and 1 <= len(last) <= 16, 'Missing final wrapper filesystem witness')
    # These bounds come from the live expected witness files. Their recorded
    # identity and actual exclusive-open operation are checked below as well.
    first_path = inputs.regular(output, 'java-version.filesystem-before.log')
    final_path = inputs.regular(output, f'acceptance.filesystem-after-{len(last)-1:02d}.log')
    artifacts = Artifacts(output, first_path.stat().st_ctime_ns, final_path.stat().st_ctime_ns)
    previous = beginning
    for label, argv, row, timeout in expected:
        inputs.require(row.get('argv') == argv and row.get('cwd') == prepared['project']
                       and row.get('timed_out') is False and 'error' not in row,
                       'Outer child invocation or outcome differs: ' + label)
        count(row.get('returncode'), 0, 'Outer child did not exit zero: ' + label)
        if timeout is not None:
            count(row.get('timeout_seconds'), timeout, 'Java observation timeout differs')
        start, end = verify_command_stream_evidence(row, '', label, artifacts)
        clocks_ordered(previous, start, 'outer child:' + label)
        clocks_ordered(end, completion, 'outer completion:' + label)
        previous = end
    return sorted(artifacts.rows.values(), key=lambda row: row['path'])
''')
    text = replace_function(text, 'verify_numeric_commands', '''def verify_numeric_commands(report, folder, artifacts, java):
    expected = expected_numeric_commands(artifacts.root, folder, java)
    commands = report.get('commands')
    count(report.get('schema'), 2, 'Numeric command creation-evidence schema differs')
    inputs.require(isinstance(commands, list) and len(commands) == len(expected) == 17, 'Numeric actual command inventory differs')
    previous = row_clock(report, 'started', 'numeric-report-start')
    completion = row_clock(report, 'finished', 'numeric-report-finish')
    clocks_ordered(previous, completion, 'numeric report', strict=True)
    inputs.require(artifacts.started_ns <= previous['unix_ns']
                   and completion['unix_ns'] <= artifacts.ended_ns, 'Numeric report is outside acceptance')
    for row, (subdir, label, code, argv) in zip(commands, expected):
        inputs.require(row.get('name') == label, 'Numeric command order differs')
        inputs.require(row.get('argv') == argv, 'Numeric exact command, JVM policy or input role differs: ' + label)
        count(row.get('returncode'), code, 'Numeric actual subprocess outcome differs')
        count(row.get('timeout_seconds'), 120, 'Numeric child timeout differs')
        prefix = folder + ('/' + subdir if subdir else '')
        start, end = verify_command_stream_evidence(row, prefix, label, artifacts)
        clocks_ordered(previous, start, 'numeric child:' + label)
        clocks_ordered(end, completion, 'numeric completion:' + label)
        previous = end
''')
    old = "for key, expected in [('schema', 1), ('primary_recovered_methods', 1), ('original_dependency_methods', 3),"
    assert text.count(old) == 1
    text = text.replace(old, "for key, expected in [('schema', 2), ('primary_recovered_methods', 1), ('original_dependency_methods', 3),", 1)
    old = "'complete_high_level_java_kotlin_source': False}\n    artifacts = None"
    assert text.count(old) == 1
    text = text.replace(old, "'complete_high_level_java_kotlin_source': False,\n              'file_metadata_verification_scope': 'Live host filesystem; archived recorded inode/ctime values are historical observations, not extracted-file metadata'}\n    artifacts = None", 1)
    TARGET.write_text(text)
    print(TARGET, len(text.encode()), hashlib.sha256(text.encode()).hexdigest())


if __name__ == '__main__':
    main()
