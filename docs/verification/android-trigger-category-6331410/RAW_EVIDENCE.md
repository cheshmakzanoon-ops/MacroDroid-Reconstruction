# Unchanged twelve-screen Android evidence

Run 38216299675 checked out commit
6331410cfd2391389270564803623079e8355ad8. Both original and combined-candidate
journeys completed all twelve declared screens. The exact comparator rejected
five changed pixels on the TRIGGERS intro page; the other eleven paired frames,
including the Date/Time category, matched. Recorded crashes and process events
remain part of the evidence. This is a finite measured journey, and whole-app
runtime parity remains unestablished.

The original 42,199,893-byte ZIP is preserved without recompression in six
ordered archive parts. `manifest.json` binds the complete container for
`scripts/assemble_artifact.py`. All 2,944 exact members are under `extracted/`;
the original extraction receipt is unchanged. Independent replay, full-frame
measurements, source bindings and scope details are under `analysis/`.

The raw emulator log includes one ephemeral ADB public-key line. Its original
bytes are retained as authorized public material, and the value is omitted from
this summary. Any separate review log is explicitly labeled as transformed and
does not replace the original raw member. No private-key finding was reported
by the preserved scan.
