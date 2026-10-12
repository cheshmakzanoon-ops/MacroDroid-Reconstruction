# Unchanged promoted-candidate Android evidence

Run 38214498395 checked out the combined reconstruction at
dbcad968c5c3e8f084205393a6c0d2d06a203c71. Its Android job reported a failed
strict intro comparison while the separate constructor allocation probe passed.
The raw 426-file capture/ART artifact and separate one-file tooling-test artifact
are preserved unchanged with their original ZIPs and exact extraction receipts.
The complete source acceptance job is a different job in this workflow.

All original member paths are under `extracted/`; tooling host evidence is under
`host-tools/`. `manifest.json` and `host-tools/manifest.json` bind exact ZIP byte
streams for `scripts/assemble_artifact.py`. Derived replay and visual measurements
are separate from these original bytes. No whole-application parity is claimed.
