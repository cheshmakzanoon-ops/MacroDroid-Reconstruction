# Numeric hosted timestamp precision review

A deterministic read-only check reproduced two distinct limitations in the
verifier used by failed hosted run `38232050667`, commit
`5c402b43ce7851a49072e8a36e93c3d88b615f75`.

The first issue is floating-point conversion. The exact old `epoch_ns` function
was invoked for 1,000 fixed, microsecond-resolution ISO timestamps. Its result
differed from integer-only conversion for 968 values, with errors between -240
and +240 nanoseconds. [conversion-results.json](conversion-results.json) retains
every input and both results.

The second issue remains even if conversion uses integer arithmetic. A synthetic
child ending 900 ns after an encoded microsecond and a wrapper completing 950 ns
after that microsecond are correctly ordered. The wrapper's microsecond ISO text
does not encode either submicrosecond remainder. Comparing the nanosecond child
end directly with the encoded microsecond floor therefore rejects this valid
ordering. [result.json](result.json) preserves the exact fixed values and literal
old predicate result.

These are direct conversion and boundary studies. They do not claim that the
synthetic nanosecond values were the actual timestamps of the hosted failure.
They do not constitute a full acceptance replay, an application build, a
correction or Android evidence. The original source remained unchanged. Any
correction must account explicitly for the producer's timestamp precision and
preserve genuine stale or reordered evidence rejection.

The reviewed old verifier is SHA-256
`e58525d32a71170f08520caf18c4d6cfc67b4bc87d7e18f692322dac4a886a39`.
Its exact bytes and dependencies are preserved in the failed-run raw artifact
and in the already published hosted package. The executed reviewer source is
[reproduce_numeric_timestamp_precision.py](reproduce_numeric_timestamp_precision.py).
