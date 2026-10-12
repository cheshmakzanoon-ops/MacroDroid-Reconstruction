#!/usr/bin/env python3
"""Record exact-identity proof guards and preserve the former substring-check limit."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def extra_throw(text):
    old = '       6: return\n'
    new = ('       6: new           #999 // class java/lang/RuntimeException\n'
           '       9: dup\n      10: invokespecial #1000 // Method java/lang/RuntimeException."<init>":()V\n'
           '      13: athrow\n      14: return\n')
    if old not in text:
        raise RuntimeError('Expected complete default-constructor disassembly')
    return text.replace(old, new, 1)


def main():
    output = HERE / 'reports/handler-guard-followup-04b'
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Synthetic proof-input validation only. No classfile or app body is executed; no original coverage credit or policy change.',
        'original_coverage_credit_added': 0, 'coverage_exemption_implemented': False,
        'app_method_executions': 0, 'commands': []}
    try:
        old_root = HERE / 'checkpoints/04-handler-dataflow-review'
        if sha(old_root / 'checkpoint.json') != '053ee22c427813258cc64f7363c150353ce1f5bbc8118aa12dbb9af049b8e754':
            raise RuntimeError('Frozen prior review changed')
        old = load(old_root / 'verify_handler_dataflow.py', 'video_old_handler_facts')
        current_path = HERE / 'verify_handler_dataflow.py'
        new = load(current_path, 'video_pinned_handler_facts')
        report['old_verifier_sha256'] = sha(old_root / 'verify_handler_dataflow.py')
        report['new_verifier_sha256'] = sha(current_path)
        shutil.copyfile(current_path, output / 'executed-verifier.py')
        evidence = HERE / 'reports/handler-dataflow-04'
        texts = {name: (evidence / ('javap-' + name + '.stdout.txt')).read_text()
                 for name in ('StringBuilder', 'AbstractStringBuilder', 'StringUTF16', 'Object')}
        modified = dict(texts); modified['StringBuilder'] = extra_throw(texts['StringBuilder'])
        (output / 'synthetic-added-throw-javap.txt').write_text(modified['StringBuilder'])
        old_accepted = old.constructor_facts(modified)['default_capacity'] == 16
        new_rejected = False; reason = None
        try:
            new.constructor_facts(modified)
        except ValueError as error:
            new_rejected = True; reason = str(error)
        if not old_accepted or not new_rejected:
            raise RuntimeError('Expected old substring acceptance/new exact-identity rejection')
        report['added_throw_comparison'] = {'old_substring_guard_accepted': old_accepted,
            'new_complete_disassembly_guard_rejected': new_rejected, 'new_rejection_reason': reason,
            'scope': 'Modified disassembly text only; the original class bytes and all historical reports remain unchanged.'}
        for name in ('rehashed-added-throw-disassembly', 'rehashed-changed-jrt-class'):
            folder = output / 'controls' / name
            inputs = folder / 'inputs'; shutil.copytree(evidence, inputs)
            collector = json.loads((inputs / 'result.json').read_text())
            if name == 'rehashed-added-throw-disassembly':
                relative = 'javap-StringBuilder.stdout.txt'
                (inputs / relative).write_text(modified['StringBuilder'])
            else:
                relative = 'jrt-classfiles/StringBuilder.class'
                value = bytearray((inputs / relative).read_bytes()); value[-1] ^= 1
                (inputs / relative).write_bytes(value)
            item = next(item for item in collector['files'] if item['path'] == relative)
            item['bytes'] = (inputs / relative).stat().st_size; item['sha256'] = sha(inputs / relative)
            (inputs / 'result.json').write_text(json.dumps(collector, indent=2) + '\n')
            command = [sys.executable, '-B', str(current_path), '--evidence', str(inputs), '--output', str(folder / 'verification')]
            out, err = folder / 'stdout.txt', folder / 'stderr.txt'; started = time.monotonic()
            with out.open('wb') as stdout, err.open('wb') as stderr:
                completed = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=60)
            verified = json.loads((folder / 'verification/result.json').read_text())
            rejected = (completed.returncode == 1 and verified['status'] == 'STRUCTURAL_FACT_REVIEW_FAILED'
                        and 'Independently pinned collector manifest changed' in verified['error'])
            report['commands'].append({'label': name, 'argv': command, 'returncode': completed.returncode,
                'timeout_seconds': 60, 'seconds': round(time.monotonic() - started, 6),
                'stdout_sha256': sha(out), 'stderr_sha256': sha(err), 'rejected': rejected,
                'altered_file': relative, 'altered_file_sha256': sha(inputs / relative),
                'rehashed_collector_sha256': sha(inputs / 'result.json')})
            if not rejected:
                raise RuntimeError('Rehashed evidence was not rejected')
        actual = json.loads((HERE / 'reports/handler-facts-04b-pinned/result.json').read_text())
        if actual['status'] != 'STRUCTURAL_FACTS_VERIFIED_SYNCHRONOUS_HOST_ARGUMENT_FOR_REVIEW' or len(actual['synthetic_fact_guard_controls']) != 11:
            raise RuntimeError('All eleven structural guards must pass on original facts')
        if sha(current_path) != report['new_verifier_sha256'] or sha(evidence / 'result.json') != new.COLLECTION_SHA:
            raise RuntimeError('Review inputs changed during controls')
        report['structural_guards_rejected'] = 11; report['rehashed_evidence_controls_rejected'] = 2
        report['passed'] = True; report['status'] = 'PINNED_PROOF_GUARDS_PASSED_NO_COVERAGE_POLICY_CHANGE'
    except Exception as error:
        report['status'] = 'PINNED_PROOF_GUARD_FOLLOWUP_FAILED'; report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n'); print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
