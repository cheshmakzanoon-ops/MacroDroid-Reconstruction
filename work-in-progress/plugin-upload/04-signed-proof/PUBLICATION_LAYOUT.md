# Complete signed K proof, preserved as an inactive checkpoint

All 50 actual source-capsule files are copied unchanged: the 35 candidate delta files, three narrow merge patches, five study tools, the evidence-only build recipe, three documentary patches, two evidence summaries and the frozen checkpoint itself.

The exact 17,491,687-byte evidence archive is preserved in three bounded parts under `evidence-archive/`. Every one of its 445 member sizes and SHA-256 hashes was independently verified: 279 complete project reports, 162 actual mutant source/class/result artifacts, two prior checkpoint manifests and two final summaries. All 363 members of at most 250,000 bytes, plus every authored mutant Java source, are also copied under `evidence/`; larger reports remain complete in the archive. `publication-verification.json` records the exact mapping.

The bounded signed original/JVM/rebuilt comparison passes 191,147 cases across 1,241 registered methods. Code/resource verification, all 54 fault controls and the 20,832-case clean restoration passed. The frozen reports retain their exact exception-comparison scope and source, fixture and APK identities. Actual Android execution and any future combined candidate require separate proof.

```bash
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/04-signed-proof/evidence-archive/manifest.json --verify-only
```

The exact e464 APK is already durable at commit `5024b1b46056de6a6e76a61883b469521a89ea44`, represented by `work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json`. This publication does not change active app source or APKs. The isolated build recipe remains evidence only; it must not overwrite the parent's current cleanup, constructor or runtime policies.
