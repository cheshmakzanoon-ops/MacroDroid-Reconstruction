# Custom scene recovery checkpoints

These immutable source checkpoints preserve the recovery of `CustomSceneAction.W`. The source files include their own exact-byte checkpoint manifests. They are historical evidence; `scripts/materialize_v9.py` overlays only `project/`, whose reconstruction status describes the active build inputs.

## 01: Original instruction and JVM comparison

`01-original-jvm/` contains 37 code, test and support files plus `checkpoint.json`. At its freeze point, 4,070 scene cases passed against the original instructions and JVM implementation, visiting all 405 original instructions and 40 conditional edges. Rebuilt signed-APK comparison and the new deliberate-fault controls were still pending. The then-active project was the separate 1,238-body reconstruction with 181,668 three-way host cases.

## 02: Signed reconstruction and negative controls

`02-signed-proof/` contains 40 frozen changed or new source/test/documentation files plus its manifest. This isolated checkpoint records 1,239 registered bodies, 185,738 three-way host cases, all 22 deliberate-fault controls, and a clean restoration pass across 15,423 UI cases. Its signed APK has SHA-256 `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.

The [main recovery report](02-signed-proof-evidence/custom-scene-recovery.json) explains the checks and their limits. All 135 original reports and logs are preserved byte for byte in the accompanying archive; `archive-contents.json` identifies every member. Reassemble it from the repository root:

```sh
python3 scripts/assemble_artifact.py work-in-progress/custom-scene/02-signed-proof-evidence/manifest.json
```

The second checkpoint completed the isolated source-body gates before integration with the active recorder and build fixes. It does not establish Android scene delivery/rendering or whole-application runtime parity. Its merge policies require deliberate integration with current files; do not blindly overlay it onto a newer `project/`.
