# Immutable host-accepted numeric APK

This exact 94,683,136-byte APK, SHA-256 `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`, was produced by successful isolated numeric host run [38238858564](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38238858564). The complete source manifest binds 81,298 inputs to snapshot `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545`. The host result covers 1,243 registered bodies and 194,780 three-path cases. No runtime parity or active application promotion is claimed here.

All twelve parts were streamed directly from the unique APK member in artifact `11741869868`. [apk-container-binding.json](apk-container-binding.json) and [manifest.json](manifest.json) retain the exact container, source, run and byte bindings. No second APK download or full duplicate APK file was created.

```bash
python3 scripts/assemble_artifact.py work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json --verify-only
python3 scripts/assemble_artifact.py work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json
```

The existing fixed indicator experiment keeps its own previous APK pin. This candidate is available only to workflows that explicitly bind this immutable manifest and commit. Changing the active project/current manifest requires a separate coherent promotion.
