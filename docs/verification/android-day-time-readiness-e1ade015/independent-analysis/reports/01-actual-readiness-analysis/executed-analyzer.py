#!/usr/bin/env python3
"""Independent, read-only audit of the closed readiness run and full-frame pixels."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import time
import traceback
import xml.etree.ElementTree as ET
import zipfile
import zlib

import numpy as np
from PIL import Image, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388')
RAW = SOURCE / 'extracted'
JOURNEY = RAW / 'journey'
GUARD = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard')
ZIP_SHA = 'c8f0af87e5d91efe2dfc49b8ca76acc1a0943b2a2b8e17ffe279892726d2c80f'
RECEIPT_SHA = '61c47bb315336958869a5cf3b945c7cbdb649de65786495f04b105ce5fa33419'
HEAD = 'e1ade015f938339479216a1a91518e556902fce8'
PLAN_SHA = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'
APP = 'com.arlosoft.macrodroid'
HOME = APP + '/' + APP + '.homescreen.NewHomeScreenActivity'
EXPECTED_PNG_CHANGES = [0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def require(value, reason):
    if not value: raise AssertionError(reason)

def sha(data): return hashlib.sha256(data).hexdigest()

def identity(path):
    require(path.is_file() and not path.is_symlink(), 'Not a regular direct file: ' + str(path))
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}

def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def number(value):
    return type(value) in (int, float) and math.isfinite(value)

def artifact(ref):
    require(set(ref) == {'path', 'bytes', 'sha256'}, 'Unexpected artifact reference fields')
    path = Path(ref['path'])
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe artifact reference')
    path = JOURNEY / path
    require(identity(path) == {k: ref[k] for k in ('bytes', 'sha256')}, 'Artifact reference differs: ' + ref['path'])
    return path

def png_metadata(path):
    data = path.read_bytes(); require(data[:8] == b'\x89PNG\r\n\x1a\n', 'Invalid PNG signature')
    at, rows, ended = 8, [], False
    while at < len(data):
        require(at + 12 <= len(data), 'Truncated PNG chunk')
        size = struct.unpack('>I', data[at:at+4])[0]; kind = data[at+4:at+8]; end = at + 12 + size
        require(end <= len(data), 'Truncated PNG chunk body')
        body = data[at+8:at+8+size]
        require(zlib.crc32(kind + body) & 0xffffffff == struct.unpack('>I', data[at+8+size:end])[0], 'PNG CRC mismatch')
        if kind != b'IDAT': rows.append({'type': kind.decode('ascii'), 'bytes': size, 'sha256': sha(body)})
        at = end
        if kind == b'IEND':
            require(size == 0 and at == len(data), 'Data after PNG end'); ended = True; break
    require(ended, 'Missing PNG end'); return rows

def rgba(path):
    with Image.open(path) as img:
        img.load(); return np.asarray(img.convert('RGBA')).copy()

def pid(path):
    data = path.read_bytes()
    require(re.fullmatch(rb'[1-9][0-9]*\r?\n?', data) is not None, 'PID output is not exactly one PID')
    return data.decode().strip()

def resumed_process(path):
    text = path.read_text()
    tops = re.findall(r'^\s*topResumedActivity=ActivityRecord\{([^}\n]+)\}\s*$', text, re.M)
    require(len(tops) == 1, 'Expected one literal topResumedActivity')
    tokens = tops[0].split(); require(len(tokens) >= 3 and tokens[1] == 'u0', 'Unexpected top resumed activity layout')
    record, component = tokens[0], tokens[2]
    owner, cls = component.split('/', 1)
    if cls.startswith('.'): cls = owner + cls
    component = owner + '/' + cls
    lines = text.splitlines(); candidates = []
    for index, line in enumerate(lines):
        if re.search(r'\* Hist\s+#\d+: ActivityRecord\{' + re.escape(record) + r'\s', line):
            block = []
            for tail in lines[index+1:]:
                if re.search(r'\* Hist\s+#\d+: ActivityRecord\{', tail): break
                if tail.strip().startswith('Task{'): break
                block.append(tail)
            found = re.findall(r'^\s*app=ProcessRecord\{[^ ]+ ([1-9][0-9]*):([^/\s}]+)/[^}]+\}\s*$', '\n'.join(block), re.M)
            candidates.extend(item for item in found if item[1] == owner)
    require(len(candidates) == 1, 'Expected one process for top resumed ActivityRecord')
    return {'component': component, 'pid': candidates[0][0], 'process': candidates[0][1], 'record': record}

def main():
    output = ROOT / 'reports/01-actual-readiness-analysis'
    output.mkdir(parents=True, exist_ok=False)
    (output / 'executed-analyzer.py').write_bytes(Path(__file__).read_bytes())
    result = {'status': 'RUNNING', 'source_mutated': False, 'new_android_execution': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'commands_executed_again': 0}
    start = time.monotonic()
    try:
        archive = SOURCE / 'readiness-run-38230072388.zip'; receipt_path = SOURCE / 'extracted-extraction.json'
        require(identity(archive) == {'bytes': 44543663, 'sha256': ZIP_SHA}, 'Wrong artifact ZIP')
        require(identity(receipt_path) == {'bytes': 581735, 'sha256': RECEIPT_SHA}, 'Wrong extraction receipt')
        receipt = json.loads(receipt_path.read_text())
        rows = receipt['files']; require(len(rows) == 3258 and len({row['path'] for row in rows}) == 3258, 'Wrong receipt inventory')
        before = {row['path']: identity(RAW / row['path']) for row in rows}
        require(all(before[row['path']] == {k: row[k] for k in ('bytes', 'sha256')} for row in rows), 'Raw extraction differs from receipt')
        require(set(before) == {p.relative_to(RAW).as_posix() for p in RAW.rglob('*') if p.is_file()}, 'Unrecorded raw artifact file')
        require(sum(row['bytes'] for row in rows) == 70899613, 'Wrong raw expanded bytes')
        with zipfile.ZipFile(archive) as zipped:
            members = [m for m in zipped.infolist() if not m.is_dir()]
            require(len(members) == len(before) and len({m.filename for m in members}) == len(before), 'ZIP inventory mismatch')
            require({m.filename for m in members} == set(before), 'ZIP/extracted name mismatch')
            for member in members:
                data = zipped.read(member)
                require({'bytes': len(data), 'sha256': sha(data)} == before[member.filename], 'ZIP/raw bytes mismatch')
        result['raw_artifact_integrity'] = {'zip_sha256': ZIP_SHA, 'receipt_sha256': RECEIPT_SHA,
                                           'files': 3258, 'bytes': 70899613, 'every_zip_member_and_extracted_file_rehashed': True}
        preflight = json.loads((RAW / 'input-preflight.json').read_text())
        require(preflight['status'] == 'FROZEN_DAY_TIME_READINESS_INPUTS_VERIFIED' and preflight['passed'] is True
                and preflight['github_sha'] == HEAD and preflight['requested_report_schema'] == 5
                and preflight['requested_scales'] == '0' and preflight['plan_sha256'] == PLAN_SHA,
                'Wrong actual input-preflight scope')
        copied = preflight['files']; require(len(copied) == 252 and len({r['copy'] for r in copied}) == 252, 'Wrong input-copy inventory')
        for row in copied:
            p = Path(row['copy']); require(not p.is_absolute() and '..' not in p.parts, 'Unsafe executed-copy path')
            require(identity(RAW / p) == {k: row[k] for k in ('bytes', 'sha256')}, 'Executed input copy differs')
        guard_cp_path = GUARD / 'checkpoint.json'
        require(identity(guard_cp_path)['sha256'] == 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3', 'Wrong reviewed guard checkpoint')
        guard_cp = json.loads(guard_cp_path.read_text())
        guard_files = {row['path'][len('replay-source/'):]: row for row in guard_cp['files'] if row['path'].startswith('replay-source/')}
        require(len(guard_files) == 81, 'Wrong reviewed guard replay inventory')
        for name, row in guard_files.items():
            require(identity(RAW / 'reviewed-source' / name) == {k: row[k] for k in ('bytes', 'sha256')}, 'Actually reviewed source differs from reviewed guard')
        workflow = RAW / 'executed-inputs/.github/workflows/editor-day-time-readiness.yml'
        require(identity(workflow)['sha256'] == '56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930', 'Actual workflow changed')
        result['executed_source_binding'] = {'copied_input_roles': 252, 'reviewed_runtime_files': 81,
                                            'guard_checkpoint_sha256': identity(guard_cp_path)['sha256'],
                                            'workflow_sha256': identity(workflow)['sha256'], 'head_sha': HEAD,
                                            'network_refetch_performed': False}
        journey = json.loads((JOURNEY / 'journey.json').read_text())
        comparison = json.loads((JOURNEY / 'comparison.json').read_text())
        verification = json.loads((RAW / 'day-time-readiness-verification.json').read_text())
        require(journey['schema'] == 5 and journey['plan_sha256'] == PLAN_SHA and journey['status'] == 'RECORDED_NOT_PARITY', 'Wrong raw journey')
        require(comparison['status'] == 'JOURNEY_DIFFERENCE' and comparison['journey_equal'] is False
                and verification['status'] == 'DAY_TIME_READINESS_THIRTEEN_SCREEN_DIFFERENCE'
                and verification['evidence_valid'] is True, 'Unexpected literal outcome')
        result['literal_outcomes'] = {name: value for name, value in (
            ('journey', journey['status']), ('comparison', comparison['status']), ('finalizer', verification['status']),
            ('evidence_valid', verification['evidence_valid']), ('full_runtime_1_to_1_established', verification['full_runtime_1_to_1_established']),
            ('crash_free_run_established', comparison['crash_free_run_established']))}
        commands = journey['commands']; require(len(commands) == 1021, 'Unexpected actual command count')
        ledger_by_stream = {}; prior = -math.inf
        for index, command in enumerate(commands):
            s, f, timeout = (command[k] for k in ('started_monotonic', 'finished_monotonic', 'timeout_seconds'))
            require(number(s) and number(f) and number(timeout) and prior <= s <= f and timeout > 0, 'Nonchronological or invalid actual command')
            require(command['timed_out'] is False and type(command['returncode']) is int, 'Command timeout or invalid return code')
            prior = f
            for name in ('stdout', 'stderr'): artifact(command[name])
            key = command['stdout']['path']; require(key not in ledger_by_stream, 'Duplicate command stdout ownership')
            ledger_by_stream[key] = (index, command)
        result['global_command_integrity'] = {'commands': len(commands), 'finite_chronological_nonoverlapping': True,
                                              'stdout_stderr_files_rehashed': 2042, 'timeouts': 0,
                                              'return_codes': dict(Counter(str(c['returncode']) for c in commands))}
        phases = []; screens = []; terminal = []; settling = []
        event_by_path = {}
        for ref in journey['capture_events']:
            event = json.loads(artifact(ref).read_text()); event_by_path[ref['path']] = event
            require(event['schema'] == 1 and event['status'] == 'CONSECUTIVE_FULL_FRAMES_IDENTICAL', 'Settling event incomplete')
            attempts = event['attempts']; require(2 <= len(attempts) <= 6 and event['max_attempts'] == 6 and event['max_seconds'] == 30, 'Settling bounds changed')
            require(event['finished_monotonic'] - event['started_monotonic'] <= 30, 'Settling time budget exceeded')
            require(event['accepted_pair'] == [len(attempts)-2, len(attempts)-1], 'Settling selected another pair')
            prior_frame = None; first_equal = None
            for index, frame in enumerate(attempts):
                require(frame['observation']['started_monotonic'] >= event['started_monotonic']
                        and frame['observation']['finished_monotonic'] <= event['finished_monotonic'], 'Frame outside settling interval')
                paths = {key: artifact(value) for key, value in frame['artifacts'].items()}
                require(pid(paths['pid_first']) == pid(paths['pid_final']), 'PID changed inside settling frame')
                if prior_frame is not None:
                    same = paths['screenshot'].read_bytes() == prior_frame['screenshot'].read_bytes() and paths['hierarchy'].read_bytes() == prior_frame['hierarchy'].read_bytes()
                    if same and first_equal is None: first_equal = [index - 1, index]
                prior_frame = paths
            require(event['accepted_pair'] == first_equal, 'Settling did not select its first consecutive exact pair')
            settling.append({'path': ref['path'], 'label': event['label'], 'attempts': len(attempts), 'accepted_pair': first_equal,
                             'seconds': event['finished_monotonic'] - event['started_monotonic']})
        require(len(settling) == 50, 'Wrong settling event count')
        write(output / 'settling-events.json', settling)
        require([r['label'] for r in journey['runs']] == ['original', 'candidate'], 'Wrong run order')
        for run in journey['runs']:
            label = run['label']; require(run['status'] == 'COMPLETE' and len(run['screens']) == 13 and len(run['transitions']) == 12, 'Run incomplete')
            handoff = next(t for t in run['transitions'] if t['to'] == 'reference-promotion')
            phase = json.loads(artifact(handoff['pre_capture_readiness']).read_text())
            require(phase['status'] == 'READY' and phase['schema'] == 1 and phase['label'] == label + '-notification-readiness', 'Wrong readiness phase')
            require(phase['policy'] == journey['notification_readiness_policy'] and phase['policy']['plan_sha256'] == PLAN_SHA, 'Readiness policy differs')
            denial = handoff['command']; denial_index, actual_denial = ledger_by_stream[denial['stdout']['path']]
            require(denial == actual_denial and denial['argv'] == ['shell', 'input tap 360 820'] and denial['returncode'] == 0, 'Wrong denial command')
            require(handoff['action'] == {'resource-id': 'com.android.permissioncontroller:id/permission_deny_button'}, 'Wrong denial selector')
            phase_start, phase_end = phase['started_monotonic'], phase['finished_monotonic']
            require(number(phase_start) and number(phase_end) and phase_start >= denial['finished_monotonic'] + 2
                    and 0 <= phase_end - phase_start <= 10, 'Readiness wait or deadline violation')
            observations = phase['observations']; require(2 <= len(observations) <= 16, 'Readiness count outside budget')
            first_start = None; qualifying = None; observed_rows = []; final_finish = None
            for index, row in enumerate(observations):
                require(type(row['index']) is int and row['index'] == index, 'Wrong readiness observation index')
                cs = row['commands']; require(len(cs) == 3, 'Wrong readiness command count')
                require([c['argv'] for c in cs] == [['shell', 'pidof ' + APP], ['shell', 'dumpsys activity activities'], ['shell', 'pidof ' + APP]], 'Wrong readiness command protocol')
                for offset, c in enumerate(cs):
                    actual_index, actual = ledger_by_stream[c['stdout']['path']]
                    require(actual == c and actual_index == denial_index + 1 + index * 3 + offset, 'Readiness command is not uniquely adjacent to denial in ledger')
                    require(c['returncode'] == 0 and artifact(c['stderr']).read_bytes() == b'' and 0 < c['timeout_seconds'] <= 10
                            and phase_start <= c['started_monotonic'] <= c['finished_monotonic'] <= phase_end
                            and row['started_monotonic'] <= c['started_monotonic'] <= c['finished_monotonic'] <= row['finished_monotonic'], 'Readiness command boundary failure')
                first_pid, final_pid = pid(artifact(cs[0]['stdout'])), pid(artifact(cs[2]['stdout']))
                foreground = resumed_process(artifact(cs[1]['stdout']))
                require(first_pid == final_pid == phase['ready_pid'] and foreground['component'] == HOME and foreground['pid'] == first_pid,
                        'Readiness PID/foreground does not actually match')
                require(row['observation'] == {'state': 'HOME_WITH_SAME_PID', 'pid_first': first_pid, 'pid_final': final_pid, 'component': HOME}, 'Recorded readiness observation differs from raw commands')
                if first_start is None: first_start = cs[0]['started_monotonic']
                final_finish = cs[2]['finished_monotonic']; span = final_finish - first_start
                if index >= 1 and span >= 1.05 and qualifying is None: qualifying = [0, index]
                observed_rows.append({'index': index, 'pid': first_pid, 'component': foreground['component'],
                                      'first_pid_command_start': cs[0]['started_monotonic'],
                                      'final_pid_command_finish': final_finish, 'ready_span_from_first_pid_start': span})
            require(phase['accepted_sequence'] == qualifying == [0, len(observations)-1], 'Readiness not first eligible raw-endpoint sequence')
            require(phase['old_pid'] == pid(artifact(handoff['preinput_artifacts']['pid'])) and phase['old_pid'] != phase['ready_pid'], 'Wrong old PID binding')
            require(len(phase['gaps']) == len(observations) - 1, 'Wrong readiness gap count')
            for index, gap in enumerate(phase['gaps']):
                require(type(gap['after_index']) is int and gap['after_index'] == index and gap['requested_seconds'] == 0.25
                        and gap['started_monotonic'] >= observations[index]['finished_monotonic']
                        and gap['finished_monotonic'] <= observations[index+1]['started_monotonic']
                        and gap['finished_monotonic'] - gap['started_monotonic'] >= 0.25, 'Readiness gap interval violation')
            promotion = next(s for s in run['screens'] if s['name'] == 'reference-promotion')
            promotion_event = event_by_path[promotion['settling']['path']]
            require(promotion_event['started_monotonic'] >= phase_end, 'Frame capture overlaps readiness')
            require(pid(artifact(promotion['artifacts']['pid_first'])) == phase['ready_pid'], 'Promotion uses another ready PID')
            phases.append({'label': label, 'status': phase['status'], 'old_pid': phase['old_pid'], 'ready_pid': phase['ready_pid'],
                           'observations': observed_rows, 'accepted_sequence': qualifying,
                           'phase_seconds': phase_end - phase_start, 'raw_ready_span_seconds': final_finish - first_start,
                           'post_denial_wait_seconds': phase_start - denial['finished_monotonic'],
                           'first_capture_after_phase_seconds': promotion_event['started_monotonic'] - phase_end,
                           'read_only_pid_foreground_commands': len(observations) * 3,
                           'continuous_liveness_or_crash_free_credit': False})
            last = run['screens'][-1]; last_xml = artifact(last['artifacts']['hierarchy'])
            nodes = ET.fromstring(last_xml.read_bytes()).iter()
            controls = [{k: n.attrib.get(k) for k in ('text', 'resource-id', 'class', 'clickable', 'enabled', 'bounds')}
                        for n in nodes if n.attrib.get('text') or n.attrib.get('clickable') == 'true']
            require([n['text'] for n in controls] == ['Permission Required', 'To use this feature MacroDroid requires permission to set exact alarms.\n\nOn the next screen please grant access to MacroDroid.', 'CANCEL', 'OK'], 'Unexpected terminal controls')
            require(all(n['clickable'] == n['enabled'] == 'true' for n in controls[-2:]), 'Terminal buttons not enabled/clickable')
            require(run['transitions'][-1]['to'] == 'after-day-time-trigger' and all(t['to'] != 'after-exact-alarm-permission' for t in run['transitions']), 'Unexpected post-terminal action')
            terminal.append({'label': label, 'screen': last['name'], 'controls': controls,
                             'subsequent_transition_count': 0, 'configuration_confirmed': False,
                             'foreground': resumed_process(artifact(last['artifacts']['foreground']))})
        write(output / 'readiness-intervals.json', phases); write(output / 'terminal-controls.json', terminal)
        for old, new in zip(journey['runs'][0]['screens'], journey['runs'][1]['screens']):
            require(old['name'] == new['name'], 'Paired screen order differs')
            op = artifact(old['artifacts']['screenshot']); npng = artifact(new['artifacts']['screenshot'])
            ox = artifact(old['artifacts']['hierarchy']); nx = artifact(new['artifacts']['hierarchy'])
            a, b = rgba(op), rgba(npng); require(a.shape == b.shape == (1280, 720, 4), 'Wrong full screenshot dimensions')
            changes = np.any(a != b, axis=2); count = int(np.count_nonzero(changes)); points = np.argwhere(changes)
            row = {'name': old['name'], 'original_png': old['artifacts']['screenshot'], 'candidate_png': new['artifacts']['screenshot'],
                   'png_bytes_identical': op.read_bytes() == npng.read_bytes(), 'rgba_changed_pixels': count,
                   'hierarchy_bytes_identical': ox.read_bytes() == nx.read_bytes(), 'png_non_idat_metadata_identical': png_metadata(op) == png_metadata(npng),
                   'dimensions': [720, 1280], 'crop_mask_tolerance_or_frame_selection_used': False}
            if count:
                row['inclusive_changed_bbox'] = [int(points[:,1].min()), int(points[:,0].min()), int(points[:,1].max()), int(points[:,0].max())]
                row['changed_coordinates_and_rgba'] = [{'x': int(x), 'y': int(y), 'original': list(map(int, a[y,x])), 'candidate': list(map(int,b[y,x]))} for y,x in points]
            screens.append(row)
        require([s['rgba_changed_pixels'] for s in screens] == EXPECTED_PNG_CHANGES, 'Independent full-frame count differs from recorded result')
        require(all(s['hierarchy_bytes_identical'] and s['png_non_idat_metadata_identical'] for s in screens), 'Hierarchy or PNG metadata differs')
        require(all(row['changed_pixels'] == actual['rgba_changed_pixels'] and row['name'] == actual['name'] for row, actual in zip(comparison['screens'], screens)), 'Stored comparison differs from independent pixel count')
        write(output / 'paired-full-frames.json', screens)
        require(comparison['trigger_type_tapped'] is True and comparison['trigger_configuration_confirmed'] is False
                and comparison['macros_saved'] is False and comparison['macros_executed'] is False,
                'Recorded journey claims exceed actions')
        result.update(status='INDEPENDENT_ACTUAL_READINESS_DIFFERENCE_CONFIRMED',
                      semantic_success_claim=False, readiness_phases=phases, complete_runs=2,
                      screens_each=13, inputs_each=12, full_frame_pixel_counts=[s['rgba_changed_pixels'] for s in screens],
                      all_thirteen_hierarchies_byte_identical=True, exact_equal_full_frame_pairs=12,
                      settling_events=len(settling), settling_frames=sum(s['attempts'] for s in settling),
                      first_eligible_settling_pairs_checked=True, terminal_controls_equal=terminal[0]['controls'] == terminal[1]['controls'],
                      terminal_is_exact_alarm_permission_dialog=True, trigger_configuration_confirmed=False,
                      masks_tolerance_or_cross_frame_selection_used=False,
                      diagnostic_scope='Independent raw readiness/settling/terminal and full-frame audit. Parent separately replays the complete pinned production analyzer.',
                      decoder={'pillow': PILLOW_VERSION, 'numpy': np.__version__, 'mode': 'full image RGBA, all four channels'})
        require({row['path']: identity(RAW / row['path']) for row in rows} == before, 'Raw inputs changed during review')
        require(identity(archive)['sha256'] == ZIP_SHA and identity(receipt_path)['sha256'] == RECEIPT_SHA, 'Raw archive/receipt changed during review')
        result['all_3258_raw_files_unchanged'] = True
        write(output / 'raw-input-identities.json', before)
    except Exception as error:
        result.update(status='INDEPENDENT_REVIEW_FAILED', error_type=type(error).__name__, error=str(error))
        (output / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); result['elapsed_seconds'] = time.monotonic() - start
        write(output / 'result.json', result)
        print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
