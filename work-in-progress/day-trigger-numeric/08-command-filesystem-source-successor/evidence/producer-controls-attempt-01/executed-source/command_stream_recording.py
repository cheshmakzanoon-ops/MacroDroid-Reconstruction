def command_clock():
    """Record exact clocks; the ISO text is a display of this same Unix value."""
    unix_ns = time.time_ns()
    monotonic_ns = time.monotonic_ns()
    seconds, nanos = divmod(unix_ns, 1_000_000_000)
    utc = datetime.fromtimestamp(seconds, timezone.utc).replace(microsecond=nanos // 1000)
    return {'unix_ns': unix_ns, 'monotonic_ns': monotonic_ns,
            'utc': utc.isoformat(timespec='microseconds')}


def command_file_stat(value):
    return {'device': value.st_dev, 'inode': value.st_ino, 'mode': value.st_mode,
            'links': value.st_nlink, 'bytes': value.st_size,
            'mtime_ns': value.st_mtime_ns, 'ctime_ns': value.st_ctime_ns}


class CommandStreamEvidence:
    """Observe exclusive files using both clocks and actual filesystem witnesses.

    Witnesses contain no invented timestamps. Every attempted after-witness is
    retained; the first whose actual filesystem clock brackets the closed streams
    is used. The bounded wait changes no timestamp and adds no acceptance slack.
    """
    WITNESS_ATTEMPTS = 16
    WITNESS_POLL_NS = 5_000_000

    def __init__(self, root, stdout, stderr):
        self.root = Path(root).resolve()
        self.paths = {'stdout': Path(stdout), 'stderr': Path(stderr)}
        if self.paths['stdout'].parent != self.paths['stderr'].parent:
            raise RuntimeError('Command streams must share a filesystem witness directory')
        if not self.paths['stdout'].name.endswith('.stdout.log'):
            raise RuntimeError('Command stdout role differs')
        self.label = self.paths['stdout'].name[:-len('.stdout.log')]
        if self.paths['stderr'].name != self.label + '.stderr.log':
            raise RuntimeError('Command stderr role differs')
        self.folder = self.paths['stdout'].parent
        self.handles = {}
        self.value = {'schema': 2, 'started': command_clock(), 'streams': {},
                      'after_witnesses': [], 'after_witness_attempt_limit': self.WITNESS_ATTEMPTS,
                      'after_witness_poll_ns': self.WITNESS_POLL_NS,
                      'filesystem_bracket_complete': False}

    def open_file(self, path):
        name = path.relative_to(self.root).as_posix()
        row = {'path': name, 'exclusive_mode': 'xb', 'open_started': command_clock()}
        handle = path.open('xb')
        try:
            row['initial_stat'] = command_file_stat(os.fstat(handle.fileno()))
            row['initial_sha256'] = hashlib.sha256(b'').hexdigest()
            row['opened'] = command_clock()
            value = row['initial_stat']
            if not stat.S_ISREG(value['mode']) or value['links'] != 1 or value['bytes'] != 0:
                raise RuntimeError('Exclusive command file is not a new empty regular inode')
            return handle, row
        except BaseException:
            handle.close()
            raise

    def close_file(self, handle, row):
        handle.flush()
        row['closing'] = command_clock()
        row['final_stat'] = command_file_stat(os.fstat(handle.fileno()))
        handle.close()
        row['closed'] = command_clock()
        path = self.root / row['path']
        before = command_file_stat(path.stat())
        if before != row['final_stat'] or path.is_symlink():
            raise RuntimeError('Command file changed inode or metadata during closure')
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        after = command_file_stat(path.stat())
        if after != before:
            raise RuntimeError('Command file changed while hashing')
        first = row['initial_stat']
        if any(first[key] != before[key] for key in ('device', 'inode', 'mode', 'links')):
            raise RuntimeError('Exclusive command file ownership changed')
        row.update(bytes=before['bytes'], sha256=digest, hashed=command_clock())

    def witness(self, suffix):
        handle, row = self.open_file(self.folder / (self.label + '.' + suffix + '.log'))
        try:
            self.close_file(handle, row)
        finally:
            if not handle.closed:
                handle.close()
        return row

    def __enter__(self):
        try:
            self.value['before_witness'] = self.witness('filesystem-before')
            for name in ('stdout', 'stderr'):
                handle, row = self.open_file(self.paths[name])
                self.handles[name] = handle
                self.value['streams'][name] = row
            self.value['invocation_started'] = command_clock()
            return self
        except BaseException as error:
            self.value['error'] = repr(error)
            for name, handle in self.handles.items():
                if not handle.closed:
                    try:
                        self.close_file(handle, self.value['streams'][name])
                    except BaseException as cleanup_error:
                        self.value.setdefault('cleanup_errors', []).append(repr(cleanup_error))
                        if not handle.closed:
                            handle.close()
            self.value['finished'] = command_clock()
            raise

    def __exit__(self, kind, error, traceback):
        self.value['invocation_finished'] = command_clock()
        if error is not None:
            self.value['error'] = repr(error)
        cleanup_error = None
        for name in ('stderr', 'stdout'):
            handle = self.handles[name]
            try:
                self.close_file(handle, self.value['streams'][name])
            except BaseException as failure:
                self.value.setdefault('cleanup_errors', []).append(repr(failure))
                cleanup_error = failure
            finally:
                if not handle.closed:
                    handle.close()
        try:
            before = self.value['before_witness']['final_stat']
            streams = [self.value['streams'][name][phase]
                       for name in ('stdout', 'stderr') for phase in ('initial_stat', 'final_stat')]
            for index in range(self.WITNESS_ATTEMPTS):
                witness = self.witness(f'filesystem-after-{index:02d}')
                self.value['after_witnesses'].append(witness)
                after = witness['final_stat']
                complete = all(before['device'] == value['device'] == after['device']
                    and before['ctime_ns'] <= value['mtime_ns'] <= after['ctime_ns']
                    and before['ctime_ns'] <= value['ctime_ns'] <= after['ctime_ns'] for value in streams)
                if complete:
                    self.value['filesystem_bracket_complete'] = True
                    break
                if index + 1 < self.WITNESS_ATTEMPTS:
                    time.sleep(self.WITNESS_POLL_NS / 1_000_000_000)
            if not self.value['filesystem_bracket_complete']:
                raise RuntimeError('Actual filesystem witnesses did not bracket command stream timestamps')
        except BaseException as failure:
            self.value.setdefault('cleanup_errors', []).append(repr(failure))
            cleanup_error = failure
        self.value['finished'] = command_clock()
        if error is None and cleanup_error is not None:
            raise cleanup_error
        return False

    def add_to(self, row):
        for prefix, name in (('started', 'started'), ('ended', 'finished')):
            value = self.value.get(name)
            if value is not None:
                row[prefix + '_unix_ns'] = value['unix_ns']
                row[prefix + '_monotonic_ns'] = value['monotonic_ns']
                row[prefix + '_utc'] = value['utc']
        if 'finished' in self.value:
            row['duration_seconds'] = (self.value['finished']['monotonic_ns'] - self.value['started']['monotonic_ns']) / 1_000_000_000
        for name in ('stdout', 'stderr'):
            value = self.value['streams'].get(name)
            if value is not None and all(key in value for key in ('path', 'bytes', 'sha256')):
                row[name] = {key: value[key] for key in ('path', 'bytes', 'sha256')}
            else:
                row[name] = None
        row['stream_evidence'] = self.value
