#!/usr/bin/env python3
"""Derive only the multipart preparation and its bounded offline controls."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
BEFORE = ROOT / 'derived-01'
AFTER = ROOT / 'source-02'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Expected one exact source anchor: ' + repr(old[:200]))
    return text.replace(old, new, 1)


AFTER.mkdir(exist_ok=False)
names = ['prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py',
         '.github/workflows/editor-exact-alarm-enable-return.yml']
for name in names:
    target = AFTER / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BEFORE / name, target)

p = AFTER / names[0]
text = p.read_text()
text = once(text, 'import sys\n', 'import sys\nimport stat\nimport tarfile\n')
text = once(text, 'def expected_inputs(root):\n',
            (ROOT / 'multipart_guard_template.py.txt').read_text() + 'def expected_inputs(root):\n')
text = once(text, '    for package, count in [(GUARD, 181), (ANIMATION, 9)]:\n',
            '    verify_guard_archive(root)\n    for package, count in [(GUARD, 181), (ANIMATION, 9)]:\n')
text = once(text, "            name = package + '/' + row['path']\n            add(name, row['sha256'], row['bytes'])\n",
            "            name = package + '/' + row['path']\n            if package == GUARD and (type(row['mode']) is not int\n                    or stat.S_IMODE(checked_file(root, name).stat().st_mode) != row['mode']):\n                raise ValueError('Frozen source payload mode changed: ' + name)\n            add(name, row['sha256'], row['bytes'])\n")
text = once(text, '    try:\n        for row in expected_inputs(root):\n',
            "    try:\n        report['guard_archive_preparation'] = {}\n        prepare_guard_archive(root, output, report['guard_archive_preparation'])\n        for row in expected_inputs(root):\n")
ast.parse(text)
p.write_text(text)

p = AFTER / names[2]
text = p.read_text()
text = once(text, "    parser.add_argument('--candidate-apk', type=Path, required=True)\n",
            "    parser.add_argument('--candidate-apk', type=Path, required=True)\n    parser.add_argument('--checkout', type=Path, required=True)\n    parser.add_argument('--original-apk', type=Path, required=True)\n    parser.add_argument('--aapt2', type=Path, required=True)\n")
start = text.index('    def source(name):\n')
end = text.index('    try:\n', start)
text = text[:start] + '''    def source(name):
        if name == preparation.WORKFLOW:
            return home / name
        if name.startswith(preparation.PACKAGE + '/'):
            return home / name[len(preparation.PACKAGE) + 1:]
        return args.checkout.resolve() / name
''' + text[end:]
text = once(text, "        report['workflow_sha256'] = preparation.identity(workflow)['sha256']\n",
            "        report['workflow_sha256'] = preparation.identity(workflow)['sha256']\n        own_before = {name: preparation.identity(home / name) for name in [\n            preparation.WORKFLOW, 'prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py']}\n        report['helpers_before'] = own_before\n")
text = once(text, '        inputs = []\n',
            "        # A literal checkout contains the two committed parts, not their logical archive.\n        names.remove(preparation.GUARD_ARCHIVE)\n        if (args.checkout.resolve() / preparation.GUARD_ARCHIVE).exists():\n            raise ValueError('Offline literal checkout unexpectedly contains a logical archive')\n        inputs = []\n")
text = once(text, '            shutil.copyfile(original, target)\n',
            '            shutil.copy2(original, target)\n')
text = once(text, "        report['prepared_input_copies'] = len(clean['files'])\n",
            "        report['prepared_input_copies'] = len(clean['files'])\n        if (clean['guard_archive_preparation']['action'] != 'ASSEMBLED_MISSING_LOGICAL_ARCHIVE'\n                or clean['guard_archive_preparation']['verified']['verified_members'] != 353):\n            raise ValueError('Literal multipart checkout was not fully assembled and verified')\n        report['multipart_preparation'] = clean['guard_archive_preparation']\n        case_input_names = {entry['path'] for entry in inputs} | {preparation.GUARD_ARCHIVE}\n")
text = once(text, "            ('changed-reviewed-finalizer', preparation.PACKAGE + '/verify_trigger_journey.py', 'bytes'),\n",
            "            ('changed-reviewed-finalizer', preparation.PACKAGE + '/verify_trigger_journey.py', 'bytes'),\n            ('missing-archive-part-1-with-existing-logical', preparation.GUARD_TRANSPORT[1][0], 'missing'),\n            ('missing-archive-part-2-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'missing'),\n            ('changed-archive-part-1-with-existing-logical', preparation.GUARD_TRANSPORT[1][0], 'same-size'),\n            ('truncated-archive-part-2-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'truncated'),\n            ('changed-archive-manifest', preparation.GUARD_TRANSPORT[0][0], 'bytes'),\n            ('symlinked-archive-part-with-existing-logical', preparation.GUARD_TRANSPORT[2][0], 'symlink'),\n            ('wrong-existing-logical-archive', preparation.GUARD_ARCHIVE, 'wrong-logical'),\n")
text = once(text, "            for entry in inputs:\n                target = case / entry['path']\n                target.parent.mkdir(parents=True, exist_ok=True)\n                os.link(root / entry['path'], target)\n",
            "            for name_to_copy in sorted(case_input_names):\n                target = case / name_to_copy\n                target.parent.mkdir(parents=True, exist_ok=True)\n                os.link(root / name_to_copy, target)\n")
text = once(text, "            if mode == 'bytes':\n                path.write_bytes(raw + b'\\nDELIBERATE_OFFLINE_INPUT_FAULT\\n')\n            else:\n                path.symlink_to(root / name)\n",
            "            if mode == 'bytes':\n                path.write_bytes(raw + b'\\nDELIBERATE_OFFLINE_INPUT_FAULT\\n')\n            elif mode == 'missing':\n                pass\n            elif mode == 'same-size':\n                path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])\n            elif mode == 'truncated':\n                path.write_bytes(raw[:-1])\n            elif mode == 'wrong-logical':\n                path.write_bytes(b'DELIBERATE_WRONG_EXISTING_LOGICAL_ARCHIVE\\n')\n            else:\n                path.symlink_to(root / name)\n")
text = once(text, "            report['checks'].append(label + ': rejected')\n",
            "            if label in {entry[0] for entry in mutations[-7:]}:\n                failed = json.loads((case / 'ci-exact-alarm-enable-return/input-preflight.json').read_bytes())\n                if failed.get('passed') is not False or failed.get('files') != []:\n                    raise ValueError('Archive fault reached copied-code preparation: ' + label)\n                report['checks'].append({'multipart_fault': label, 'rejected_before_any_copy': True,\n                                         'reason': failed.get('reason')})\n            else:\n                report['checks'].append(label + ': rejected')\n")
text = once(text, "        row = execute('existing-output', ['bash', str(output / 'step-01.sh')])\n",
            "        matching = output / 'matching-existing-logical'\n        matching.mkdir()\n        for name in sorted(case_input_names):\n            target = matching / name\n            target.parent.mkdir(parents=True, exist_ok=True)\n            os.link(root / name, target)\n        row = execute('matching-existing-logical-preflight', ['bash', str(output / 'step-01.sh')],\n                      cwd=matching, extra={'GITHUB_WORKSPACE': str(matching)})\n        existing = json.loads((matching / 'ci-exact-alarm-enable-return/input-preflight.json').read_bytes())\n        if (row['exit_code'] or existing.get('passed') is not True\n                or existing['guard_archive_preparation']['action'] != 'VERIFIED_EXISTING_LOGICAL_ARCHIVE'\n                or existing['files'] != clean['files']):\n            raise ValueError('Matching existing logical archive failed full preparation')\n        report['checks'].append({'matching_existing_logical_archive_accepted': True,\n                                 'all_parts_still_verified': True, 'copies': len(existing['files'])})\n        row = execute('existing-output', ['bash', str(output / 'step-01.sh')])\n")
text = once(text, "(workspace / 'recovered/automation android app', 'workspace/artifacts/' + preparation.APKS[0][1])",
            "(args.original_apk.resolve(), 'workspace/artifacts/' + preparation.APKS[0][1])")
text = once(text, "(workspace / 'current/MacroDroid_v9/tools/prebuilt/linux/aapt2', 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2')",
            "(args.aapt2.resolve(), 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2')")
text = once(text, "            runtime_before.append({'source': str(original), 'path': relative, **preparation.identity(original)})\n",
            "            runtime_before.append({'source': str(original), 'path': relative, **preparation.identity(original),\n                'transport': 'READ_ONLY_HARDLINK' if original.stat().st_dev == root.stat().st_dev else 'READ_ONLY_BYTE_COPY',\n                'source_device': original.stat().st_dev, 'destination_device': target.stat().st_dev})\n")
text = once(text, "        inventory_names = {entry['path'] for entry in inputs + runtime_before}\n",
            "        inventory_names = {entry['path'] for entry in inputs + runtime_before} | {preparation.GUARD_ARCHIVE}\n")
text = once(text, "        closed_source = json.loads((args.guard.resolve() / 'checkpoint.json').read_bytes())\n",
            "        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))\n        for index, script in enumerate(host.splitlines()[1:]):\n            if index == 1:\n                continue  # This exact 259-test source suite is already closed; hosted still executes it.\n            row = execute('packaged-host-controls-' + str(index), ['bash', '-o', 'pipefail', '-c', script], timeout=600)\n            if row['exit_code']:\n                raise ValueError('Packaged animation or downloader controls failed')\n        closed_source = json.loads((args.guard.resolve() / 'checkpoint.json').read_bytes())\n")
text = once(text, "        if preparation.identity(workflow)['sha256'] != report['workflow_sha256']:\n            raise ValueError('Workflow changed during validation')\n",
            "        report['helpers_after'] = {name: preparation.identity(home / name) for name in own_before}\n        if report['helpers_after'] != own_before:\n            raise ValueError('Workflow or helper changed during validation')\n        if preparation.verify_guard_archive(root) != clean['guard_archive_preparation']['verified']:\n            raise ValueError('Prepared guard archive changed during validation')\n")
ast.parse(text)
p.write_text(text)

p = AFTER / names[3]
text = p.read_text()
text = once(text, identity(BEFORE / names[0])['sha256'], identity(AFTER / names[0])['sha256'])
text = once(text, '      - name: Verify and copy the frozen exact-alarm guard and sixteen-screen source\n',
            '      - name: Verify both source archive parts, assemble and copy the frozen sixteen-screen source\n')
p.write_text(text)
changes = [{'path': name, 'before': identity(BEFORE / name), 'after': identity(AFTER / name)} for name in names]
patch = ''.join(''.join(difflib.unified_diff((BEFORE / name).read_text().splitlines(True),
    (AFTER / name).read_text().splitlines(True), fromfile='derived-01/' + name,
    tofile='multipart-successor/' + name)) for name in names)
(AFTER / 'derivation.patch').write_text(patch)
(AFTER / 'derivation.json').write_text(json.dumps({'scope': 'Multipart source-evidence input preparation and literal offline validation only.',
    'generator_unchanged': identity(ROOT / 'inputs/derive_workflow.py'),
    'published_source_and_transport_commit': 'fc825ede39a40249e33c8ba75b93128a98bd5e3c',
    'source_checkpoint_sha256': '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051',
    'source_files': 102, 'complete_source_capsule_payloads': 181,
    'archive_members': 353, 'closed_source_host_tests_reused': 259,
    'new_application_or_device_action': False, 'active_files': [], 'changes': changes}, indent=2) + '\n')
print(json.dumps({'source': str(AFTER), 'files': changes, 'android_executed': False}, indent=2))
