def checked_clock(value, role):
    inputs.require(isinstance(value, dict) and set(value) == {'unix_ns', 'monotonic_ns', 'utc'},
                   'Exact clock fields differ: ' + role)
    inputs.require(type(value['unix_ns']) is int and value['unix_ns'] > 0
                   and type(value['monotonic_ns']) is int and value['monotonic_ns'] > 0,
                   'Missing exact integer clocks: ' + role)
    seconds, fraction = divmod(value['unix_ns'], 1_000_000_000)
    expected = datetime.fromtimestamp(seconds, timezone.utc).replace(microsecond=fraction // 1000).isoformat(timespec='microseconds')
    inputs.require(value['utc'] == expected, 'ISO text is not the exact integer-clock truncation: ' + role)
    return value


def row_clock(row, prefix, role):
    return checked_clock({'unix_ns': row.get(prefix + '_unix_ns'),
                          'monotonic_ns': row.get(prefix + '_monotonic_ns'),
                          'utc': row.get(prefix + '_utc')}, role)


def clocks_ordered(first, second, role, strict=False):
    for name in ('unix_ns', 'monotonic_ns'):
        inputs.require(first[name] < second[name] if strict else first[name] <= second[name],
                       'Command clocks reverse or escape their ordered operation: ' + role)


def checked_stat(value, role):
    fields = {'device', 'inode', 'mode', 'links', 'bytes', 'mtime_ns', 'ctime_ns'}
    inputs.require(isinstance(value, dict) and set(value) == fields
                   and all(type(value[key]) is int for key in fields), 'Exact filesystem stat fields differ: ' + role)
    inputs.require(value['device'] > 0 and value['inode'] > 0 and stat.S_ISREG(value['mode'])
                   and value['links'] == 1 and value['bytes'] >= 0
                   and value['mtime_ns'] > 0 and value['ctime_ns'] > 0,
                   'File is not one owned regular inode: ' + role)
    return value


def verify_file_creation(receipt, name, artifacts, witness=False):
    """Check recorded creation against the live host file, not extracted ZIP stats."""
    fields = {'path', 'exclusive_mode', 'open_started', 'initial_stat', 'initial_sha256', 'opened',
              'closing', 'final_stat', 'closed', 'bytes', 'sha256', 'hashed'}
    inputs.require(isinstance(receipt, dict) and set(receipt) == fields
                   and receipt.get('path') == name and receipt.get('exclusive_mode') == 'xb',
                   'Exclusive file role or creation receipt differs: ' + name)
    clocks = [checked_clock(receipt[stage], name + ':' + stage)
              for stage in ('open_started', 'opened', 'closing', 'closed', 'hashed')]
    for first, second in zip(clocks, clocks[1:]):
        clocks_ordered(first, second, name)
    initial = checked_stat(receipt['initial_stat'], name + ':initial')
    final = checked_stat(receipt['final_stat'], name + ':final')
    inputs.require(initial['bytes'] == 0 and receipt['initial_sha256'] == hashlib.sha256(b'').hexdigest()
                   and initial['mtime_ns'] == initial['ctime_ns'], 'Exclusive file was not initially empty: ' + name)
    inputs.require(all(initial[key] == final[key] for key in ('device', 'inode', 'mode', 'links')),
                   'Exclusive file inode ownership changed: ' + name)
    inputs.require(initial['mtime_ns'] <= final['mtime_ns'] and initial['ctime_ns'] <= final['ctime_ns'],
                   'File metadata predates its recorded exclusive creation: ' + name)
    artifacts.hash(name, receipt['sha256'])
    actual = artifacts.rows[name]
    inputs.require({key: actual[key] for key in final} == final,
                   'Live file differs from the recorded final fstat: ' + name)
    count(receipt['bytes'], final['bytes'], 'Final stream byte count differs')
    if witness:
        inputs.require(initial == final and final['bytes'] == 0
                       and receipt['sha256'] == hashlib.sha256(b'').hexdigest(),
                       'Filesystem witness was written, changed or substituted: ' + name)
    return receipt


def verify_command_stream_evidence(row, prefix, label, artifacts):
    value = row.get('stream_evidence')
    fields = {'schema', 'started', 'streams', 'after_witnesses', 'after_witness_attempt_limit',
              'after_witness_poll_ns', 'filesystem_bracket_complete', 'before_witness',
              'invocation_started', 'invocation_finished', 'finished'}
    inputs.require(isinstance(value, dict) and set(value) == fields,
                   'Missing, partial or additional command creation evidence: ' + label)
    count(value['schema'], 2, 'Command creation evidence schema differs')
    count(value['after_witness_attempt_limit'], 16, 'Filesystem witness attempt bound differs')
    count(value['after_witness_poll_ns'], 5_000_000, 'Filesystem witness polling bound differs')
    inputs.require(value['filesystem_bracket_complete'] is True, 'Actual filesystem bracket did not complete')
    start = checked_clock(value['started'], label + ':start')
    end = checked_clock(value['finished'], label + ':finish')
    clocks_ordered(start, end, label, strict=True)
    inputs.require(row_clock(row, 'started', label) == start and row_clock(row, 'ended', label) == end,
                   'Command timestamps differ from its stream-creation evidence')
    inputs.require(type(row.get('duration_seconds')) in (int, float)
                   and math.isfinite(row['duration_seconds'])
                   and row['duration_seconds'] == (end['monotonic_ns'] - start['monotonic_ns']) / 1_000_000_000,
                   'Command duration differs from its exact monotonic interval')
    prefix = prefix + '/' if prefix else ''
    before = verify_file_creation(value['before_witness'], prefix + label + '.filesystem-before.log', artifacts, True)
    clocks_ordered(start, before['open_started'], label + ':before-witness')
    inputs.require(isinstance(value['streams'], dict) and set(value['streams']) == {'stdout', 'stderr'},
                   'Exclusive command stream inventory differs')
    previous = before['hashed']
    receipts = []
    for stream in ('stdout', 'stderr'):
        name = prefix + label + '.' + stream + '.log'
        receipt = verify_file_creation(value['streams'][stream], name, artifacts)
        inputs.require(row.get(stream) == {key: receipt[key] for key in ('path', 'bytes', 'sha256')},
                       'Command reused, renamed or substituted another stream: ' + name)
        clocks_ordered(previous, receipt['open_started'], name + ':open')
        previous = receipt['opened']
        receipts.append(receipt)
    invocation_start = checked_clock(value['invocation_started'], label + ':invocation-start')
    invocation_end = checked_clock(value['invocation_finished'], label + ':invocation-end')
    clocks_ordered(previous, invocation_start, label + ':invoke')
    clocks_ordered(invocation_start, invocation_end, label + ':return')
    previous = invocation_end
    for receipt in reversed(receipts):
        clocks_ordered(previous, receipt['closing'], receipt['path'] + ':close')
        previous = receipt['hashed']
    witnesses = value['after_witnesses']
    inputs.require(isinstance(witnesses, list) and 1 <= len(witnesses) <= 16, 'After-witness inventory differs')
    for index, witness in enumerate(witnesses):
        witness = verify_file_creation(witness, prefix + label + f'.filesystem-after-{index:02d}.log', artifacts, True)
        clocks_ordered(previous, witness['open_started'], label + ':after-witness')
        if index:
            inputs.require(witness['open_started']['monotonic_ns'] - previous['monotonic_ns'] >= 5_000_000,
                           'After-witness retry omitted its recorded polling interval')
        previous = witness['hashed']
        floor, ceiling = before['final_stat'], witness['final_stat']
        complete = all(floor['device'] == observed['device'] == ceiling['device']
            and floor['ctime_ns'] <= observed['mtime_ns'] <= ceiling['ctime_ns']
            and floor['ctime_ns'] <= observed['ctime_ns'] <= ceiling['ctime_ns']
            for receipt in receipts for observed in (receipt['initial_stat'], receipt['final_stat']))
        inputs.require(complete is (index == len(witnesses) - 1),
                       'Witness inventory did not stop at the first actual filesystem bracket')
    clocks_ordered(previous, end, label + ':complete')
    return start, end
