# Custom scene work in progress

`01-original-jvm/` preserves a source-only recovery checkpoint for `CustomSceneAction.W`. Its 37 code, test and support files plus `checkpoint.json` are retained exactly as produced by the recovery work. The checkpoint hashes every changed or new input.

This checkpoint passed 4,070 scene cases against the original instructions and JVM implementation, visiting all 405 original instructions and 40 conditional edges. Rebuilt signed-APK comparison and the new deliberate-fault controls were still pending when the checkpoint was captured. See [the checkpoint report](01-original-jvm/SCENE_RECOVERY.md) for scope and limitations.

These files are not applied by `scripts/materialize_v9.py`; that command overlays only `project/`. The active project remains the separately tested 1,238-body reconstruction with 181,668 three-way host cases. The 1,239-body registry here belongs to this inactive checkpoint until the remaining gates complete and a coherent source update is published.
