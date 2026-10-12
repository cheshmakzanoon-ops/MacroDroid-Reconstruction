# Numeric command filesystem evidence successor

This inactive source capsule changes only `day_numeric_dex_controls.py` from the previously frozen nineteen-file overlay. The other eighteen source files, every Java body, the original fixture, helper/D8 identities, command arguments, 120-second subprocess timeout, and application acceptance expectations remain unchanged. The complete future input manifest has 81,298 entries and is retained in a lossless gzip container; `evidence/source-binding.json` pins both its compressed and decompressed bytes.

## Actual failure and diagnosis

Hosted run 38232050667 failed before materialization or application build: 67 tooling tests ran, with 64 successes, two errors and one dependent failure. The exact twelve-member raw artifact is preserved at `docs/verification/day-numeric-hosted-run-5c402b4/`. That log did not retain the failing fixtures' exact stat values, so this capsule does not invent hosted nanosecond deltas.

The unchanged-source diagnosis separately ran 32 synthetic numeric fixtures and 32 wrapper fixtures successfully on local tmpfs. Eight actual empty Python subprocesses then produced sixteen streams whose mtime/ctime were earlier than their recorded precise wall-clock start, despite exclusive creation after that start. All exact observations and original source are retained. The kernel documentation explains that inode times can use coarse clock values; Python datetime records microseconds, and conversion through a floating-point timestamp introduces an additional precision loss. These are distinct limitations.

## Exact producer contract

Each command records integer Unix and monotonic nanoseconds. ISO text is derived from that same Unix value using integer seconds and microseconds. Before opening stdout/stderr it exclusively creates an empty filesystem witness in the same directory. Each stream is opened with `xb`; the producer records its open-operation clocks, initial empty fstat/hash, final fstat/hash, and closure clocks. The file must retain one regular inode and one link.

After both streams close, the producer creates and retains filesystem witnesses until the actual timestamp of one brackets all recorded initial/final stream timestamps. A coarse filesystem clock may need to advance after a fine write timestamp, so this is a bounded observation sequence: at most sixteen separate empty witnesses, with a requested five-millisecond wait between failed observations (at most fifteen waits). It uses the first actual bracket, never changes timestamps, never discards unsuccessful witnesses, and never adds a timestamp tolerance. If no bracket is observed, the command evidence fails. The real subprocess timeout remains exactly the existing caller-supplied timeout.

The first producer attempt passed thirteen controls but an independent review found an exceptional-I/O cleanup gap. Its exact source/results and the published counterexample remain preserved. The corrected attempt passed sixteen controls: both producer copies share an identical helper AST; actual empty/nonempty/nonzero subprocess outputs are retained; preexisting files/symlinks, borrowed witnesses, inode/link substitution and an actual stale mtime are rejected. Additional injected flush-plus-close errors demonstrate cleanup of the other owned stream, retention of the original exception, and a recorded finish. These are host producer/evidence controls, with no Java, D8, application build, or Android execution.

## Verification scope

The successor independent hosted verifier will compare recorded metadata against the live files, enforce both integer-clock orderings, exact argv/path/hash/physical ownership, complete witness ordering, and the first actual bracket. It is still being prepared separately; the full sixteen application gates remain pending. Archived fstat values describe the host observations at capture time. Extraction does not preserve original inode or ctime, and an archive replay must not treat extraction metadata as the hosted filesystem observation.

Primary documentation: [Linux multigrain timestamps](https://cdn.kernel.org/doc/html/latest/filesystems/multigrain-ts.html), [Linux timekeeping accessors](https://cdn.kernel.org/doc/html/latest/core-api/timekeeping.html), and [Python datetime](https://docs.python.org/3.12/library/datetime.html).
