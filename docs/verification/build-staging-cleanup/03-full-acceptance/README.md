# Complete f83 host acceptance: durable evidence

The historical **1,239-method f83 input snapshot passed all 16 configured host gates** in its isolated temporary checkout. This capsule preserves the exact completed evidence: 185,738 bounded original/JVM/rebuilt cases, 209 passing Python controls, all gate logs, all 19 fresh report bindings, and the unchanged 81,212-file input inventory. See the [frozen report](review/README.md), [acceptance result](review/reports/acceptance-latest.json), and [independent verification](review/independent-verification.json).

The result belongs to input pin `f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85` and hybrid APK `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`. It does not validate the later 1,240-method candidate. Android was not executed in this acceptance invocation; its availability probe was blocked by ADB being absent from that process's PATH. The earlier failed attempts remain preserved separately.

## Complete archive and review copies

The exact **21,777,639-byte ZIP** is stored in three binary parts, with SHA-256 `83ca0584390aa8d70b0b15f44ddf4e2c72459e3ab837e2e455fa3e883a1efd52`. Its 228 members include every one of the 219 completed report files. All ZIP member bytes were independently compared against the frozen checkpoint and the source files before publication.

The `review/` directory contains 218 unchanged member copies, including all 16 gate logs, the final acceptance reports, test logs, authoring/verifying code, and full input manifest. 10 larger resource-table or negative-control files are available in full in the ZIP. [The extraction receipt](extraction-receipt.json) identifies every member, its hash, and its review path or archive-only status. The frozen README inside `review/` describes the complete extracted capsule; its statement that `reports/` is complete applies to the ZIP extraction.

From the repository root:

```sh
python scripts/assemble_artifact.py docs/verification/build-staging-cleanup/03-full-acceptance/manifest.json --verify-only
python scripts/assemble_artifact.py docs/verification/build-staging-cleanup/03-full-acceptance/manifest.json
python -m zipfile -e workspace/artifacts/f83-complete-host-acceptance.zip workspace/evidence/f83-complete-host-acceptance
```

[The exact checkpoint](checkpoint.json) and [original delivery receipt](delivery.json) remain unchanged. No report was truncated, rewritten, or converted from failure to success. This publication performs no generated-cache removal; a later authorized cleanup requires its own receipt and must preserve source, reports, and APKs.
