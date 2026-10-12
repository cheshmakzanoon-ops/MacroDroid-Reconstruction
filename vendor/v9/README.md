# Immutable v9 source and toolchain snapshot

This directory stores the complete previously delivered v9 source and toolchain
archives as ordinary Git binary parts. The parts preserve the original ZIP bytes;
they are not Git LFS pointers. Each part is at most 8 MiB.

`manifest.json` records the ordered parts, their sizes, SHA-256 checksums and Git
blob identities, plus the original archive size, SHA-256 and extracted file count.
The source archive contains 81,903 files (893,573,243 expanded bytes). The toolchain
archive contains 14 files (122,067,246 expanded bytes). The combined archive size is
328,955,278 bytes across 40 parts.

Verify the checked-in bytes from the repository root with Python 3.11 or newer:

```sh
python3 scripts/materialize_v9.py --verify-only
```

Create the working project, including the latest authored files in `project/`:

```sh
python3 scripts/materialize_v9.py
```

The default destination is `workspace/MacroDroid_v9`. To examine the immutable
snapshot without the current overlay, add `--without-overlay`. Choose a fresh
`--destination` when a working directory already exists; existing edits are never
silently replaced. You can also concatenate each archive's listed parts in order
and use `scripts/import_v9.py` with the resulting ZIPs.

The manifest's archive checksums describe historical v9. Files in `project/` are
the current development overlay and may intentionally differ from that snapshot.
Keep changes to authored source, build scripts and verification tools visible in
`project/`; do not rewrite the historical archive for each change.

The snapshot retains the openly distributed development signing identity bundled
with the v9 toolchain. It is a test identity, not the publisher's signing key. The
original APK is not contained in these 40 source/toolchain parts.

Archive integrity, file recovery and successful compilation do not establish 1:1
Android runtime behavior. Consult the current project verification reports for
measured progress and outstanding acceptance gates.
