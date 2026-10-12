#!/usr/bin/env python3
"""Prepare the independent stream-receipt regression successor without old edits."""
from pathlib import Path

target = Path('/dev/shm/day-numeric-hosted-02/source/tools/day_numeric_acceptance/test_day_numeric_acceptance.py')
text = target.read_text()
assert 'def observed_command' not in text
text = text.replace('import copy\n', 'import copy\nimport hashlib\nimport shutil\n')
text = text.replace('    def tearDown(self):\n        self.temp.cleanup()\n', '''    def tearDown(self):
        # Hosted failures retain actual receipts and original metadata even though
        # an artifact copy cannot preserve the host's inode or ctime.
        retained = os.environ.get('DAY_NUMERIC_CONTROL_EVIDENCE_ROOT')
        if retained:
            output = Path(retained) / self.id()
            output.mkdir(parents=True, exist_ok=False)
            rows = []
            for path in sorted(self.root.rglob('*')):
                relative = path.relative_to(self.root).as_posix()
                status = path.lstat()
                if path.is_symlink():
                    rows.append({'path': relative, 'type': 'inert-symlink-description',
                                 'target': os.readlink(path)})
                elif path.is_file():
                    destination = output / 'files' / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, destination)
                    rows.append({'path': relative, 'type': 'regular', **inputs.identity(path),
                                 'observed_stat': run_acceptance.command_file_stat(status)})
            values = {}
            for key, value in vars(self).items():
                if key.startswith('_') and key != '_control_observations':
                    continue
                try:
                    json.dumps(value, allow_nan=False)
                except (TypeError, ValueError):
                    continue
                values[key] = value
            inputs.write_json(output / 'observations.json', {
                'schema': 1, 'test': self.id(), 'original_temporary_root': str(self.root),
                'scope': 'Tool policy fixtures and declared small Python subprocesses only; no application build or Java parity claim',
                'metadata_scope': 'Recorded original live stat; copied inode/ctime are not substituted',
                'values': values, 'files': rows})
        self.temp.cleanup()

    def observed_command(self, prefix, label, **row):
        """Use real exclusive files; the contents explicitly remain synthetic."""
        folder = self.root / prefix
        folder.mkdir(parents=True, exist_ok=True)
        observed = run_acceptance.CommandStreamEvidence(
            self.root, folder / (label + '.stdout.log'), folder / (label + '.stderr.log'))
        with observed as stream:
            for name in ('stdout', 'stderr'):
                stream.handles[name].write(('SYNTHETIC COMMAND POLICY ONLY ' + prefix + '/' + label + ':' + name).encode())
        observed.add_to(row)
        self.__dict__.setdefault('_control_observations', []).append(copy.deepcopy(row))
        return row

    @staticmethod
    def set_flat_clock(row, prefix, value):
        row[prefix + '_unix_ns'] = value['unix_ns']
        row[prefix + '_monotonic_ns'] = value['monotonic_ns']
        row[prefix + '_utc'] = value['utc']

    @staticmethod
    def changed_clock(value, unix_delta=0, mono_delta=0):
        changed = copy.deepcopy(value)
        changed['unix_ns'] += unix_delta
        changed['monotonic_ns'] += mono_delta
        seconds, fraction = divmod(changed['unix_ns'], 1_000_000_000)
        changed['utc'] = datetime.fromtimestamp(seconds, timezone.utc).replace(
            microsecond=fraction // 1000).isoformat(timespec='microseconds')
        return changed
''')
text = text.replace("self.root / 'stdout.log', self.root / 'stderr.log', timeout", "self.root / 'actual.stdout.log', self.root / 'actual.stderr.log', timeout")
text = text.replace("(self.root / 'stdout.log').read_bytes()", "(self.root / 'actual.stdout.log').read_bytes()")
text = text.replace("(self.root / 'stderr.log').read_bytes()", "(self.root / 'actual.stderr.log').read_bytes()")
text = text.replace('    def make_report(self, alias_first_streams=False):\n        self.start = time.time_ns() - 10_000_000\n        self.report = {\'started_utc\': datetime.now(timezone.utc).isoformat(), \'commands\': []}', '''    def make_report(self):
        self.report = {'schema': 2, 'commands': []}
        self.set_flat_clock(self.report, 'started', run_acceptance.command_clock())''')
start = text.index('        for index, (subdir, label, code, argv) in enumerate(rows):')
end = text.index('\n    def check(self):', start)
text = text[:start] + '''        for subdir, label, code, argv in rows:
            prefix = self.folder + ('/' + subdir if subdir else '')
            self.report['commands'].append(self.observed_command(
                prefix, label, name=label, argv=argv, returncode=code, timeout_seconds=120))
        self.set_flat_clock(self.report, 'finished', run_acceptance.command_clock())
        # This is the command guard alone, not a synthetic full acceptance claim.
        # Its encompassing fixture bounds include the actual filesystem witnesses.
        first = self.report['commands'][0]['stream_evidence']['before_witness']['final_stat']['ctime_ns']
        final = self.report['commands'][-1]['stream_evidence']['after_witnesses'][-1]['final_stat']['ctime_ns']
        self.start = min(first, self.report['started_unix_ns'])
        self.end = max(final, self.report['finished_unix_ns'])
''' + text[end:]
text = text.replace('    def test_exact_seventeen_synthetic_command_rows_preserve_thirty_four_distinct_streams(self):\n        self.assertEqual(34, len(self.check().rows))', '''    def test_exact_seventeen_synthetic_command_rows_preserve_streams_and_all_witnesses(self):
        rows = self.check().rows
        self.assertEqual(34, len([name for name in rows if name.endswith(('.stdout.log', '.stderr.log'))]))
        expected = sum(3 + len(row['stream_evidence']['after_witnesses']) for row in self.report['commands'])
        self.assertEqual(expected, len(rows))''')
text = text.replace("with self.assertRaisesRegex(ValueError, 'reused another stream'):", "with self.assertRaisesRegex(ValueError, 'reused, renamed or substituted'):")
start = text.index('    def test_physical_numeric_stream_alias_rejects_even_with_matching_hashes(self):')
end = text.index('    def test_omitted_last_numeric_child_rejects(self):', start)
text = text[:start] + '''    def test_physical_numeric_stream_alias_rejects_even_with_matching_hashes(self):
        row = self.report['commands'][0]
        first, second = (self.root / row[stream]['path'] for stream in ('stdout', 'stderr'))
        second.unlink()
        os.link(first, second)
        for stream in ('stdout', 'stderr'):
            receipt = row['stream_evidence']['streams'][stream]
            receipt['final_stat'] = run_acceptance.command_file_stat((self.root / receipt['path']).stat())
            receipt.update(inputs.identity(self.root / receipt['path']))
            row[stream] = {key: receipt[key] for key in ('path', 'bytes', 'sha256')}
        with self.assertRaisesRegex(ValueError, 'one owned regular inode'):
            self.check()

    def test_stream_from_before_its_own_numeric_child_rejects(self):
        row = self.report['commands'][0]
        value = row['stream_evidence']
        value['started'] = copy.deepcopy(value['invocation_finished'])
        self.set_flat_clock(row, 'started', value['started'])
        row['duration_seconds'] = (value['finished']['monotonic_ns'] - value['started']['monotonic_ns']) / 1_000_000_000
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

''' + text[end:]
start = text.index('class WrapperStreamControls(OwnedTemporary):')
end = text.index('class NumericProvenanceControls', start)
text = text[:start] + '''class WrapperStreamControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.prepared = {'project': '/synthetic/project'}
        self.execution = {'schema': 2, 'java_versions': []}
        self.set_flat_clock(self.execution, 'started', run_acceptance.command_clock())
        for label, argv, timeout in [('java-version', ['java', '-version'], 15),
                                      ('javac-version', ['javac', '-version'], 15),
                                      ('acceptance', [sys.executable, '-B', 'acceptance.py'], 6600)]:
            row = self.observed_command('', label, argv=argv, cwd=self.prepared['project'],
                                        timeout_seconds=timeout, returncode=0, timed_out=False)
            if label == 'acceptance':
                self.execution['execution'] = row
            else:
                self.execution['java_versions'].append(row)
        self.set_flat_clock(self.execution, 'finished', run_acceptance.command_clock())

    def check(self):
        return verify.verify_wrapper_streams(self.execution, self.prepared, self.root)

    def test_exact_synthetic_child_stream_roles_and_intervals_are_accepted(self):
        rows = self.check()
        self.assertEqual(6, len([row for row in rows if row['path'].endswith(('.stdout.log', '.stderr.log'))]))
        expected = sum(3 + len(row['stream_evidence']['after_witnesses'])
                       for row in self.execution['java_versions'] + [self.execution['execution']])
        self.assertEqual(expected, len(rows))

    def test_java_version_streams_cannot_replace_acceptance_streams(self):
        for stream in ('stdout', 'stderr'):
            (self.root / self.execution['execution'][stream]['path']).unlink()
            self.execution['execution'][stream] = copy.deepcopy(self.execution['java_versions'][0][stream])
        with self.assertRaises((ValueError, FileNotFoundError)):
            self.check()

    def test_dot_alias_does_not_create_a_new_acceptance_stream_role(self):
        self.execution['execution']['stdout']['path'] = './acceptance.stdout.log'
        with self.assertRaisesRegex(ValueError, 'reused, renamed or substituted'):
            self.check()

    def test_version_command_cannot_be_replaced_by_true(self):
        self.execution['java_versions'][0]['argv'] = ['/bin/true']
        with self.assertRaisesRegex(ValueError, 'Outer child invocation'):
            self.check()

    def test_old_acceptance_stream_fails_its_recorded_creation_order(self):
        row = self.execution['execution']
        evidence = row['stream_evidence']
        evidence['started'] = copy.deepcopy(evidence['invocation_finished'])
        self.set_flat_clock(row, 'started', evidence['started'])
        row['duration_seconds'] = (evidence['finished']['monotonic_ns'] - evidence['started']['monotonic_ns']) / 1_000_000_000
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

    def test_acceptance_interval_cannot_precede_the_java_observations(self):
        row = self.execution['execution']
        first = self.execution['java_versions'][0]
        delta = first['started_unix_ns'] - row['started_unix_ns'] - 1_000_000_000
        def shift(value):
            if isinstance(value, dict):
                if set(value) == {'unix_ns', 'monotonic_ns', 'utc'}:
                    return self.changed_clock(value, delta, delta)
                return {key: shift(item) for key, item in value.items()}
            if isinstance(value, list):
                return [shift(item) for item in value]
            return value
        row['stream_evidence'] = shift(row['stream_evidence'])
        self.set_flat_clock(row, 'started', row['stream_evidence']['started'])
        self.set_flat_clock(row, 'ended', row['stream_evidence']['finished'])
        with self.assertRaisesRegex(ValueError, 'outer child:acceptance'):
            self.check()


''' + text[end:]
target.write_text(text)
print(target)
