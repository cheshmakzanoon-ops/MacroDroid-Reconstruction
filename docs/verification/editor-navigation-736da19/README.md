# Historical navigation inspection and exact local host evidence

This capsule preserves the read-only inspection of Android run 38204928419 at source commit `736da1920f7dada1d0c3444032ffcf4eb8759888`. It is not a new Android run and does not convert the historical continuous-startup rejection into a pass.

The original artifact remains in `../editor-journey/run-38204928419-attempt-1/evidence.zip`: 10,973,841 bytes, SHA-256 `1120c0bdcff9d054a08bf3e52f733000597ca18c28a5a17230276e0fd7fad785`. Both APKs completed all 16 recorded screens. Every corresponding raw UI XML was identical, but the full screenshots were not all identical. The exact pixel counts and exclusive difference rectangles are preserved in `full-frame-inspection.json` inside this capsule. Several frames differ in a status icon, the second intro frame also differs near the page indicator, and the notification frame differs more broadly. No mask, crop or tolerance is used to produce the comparison result.

The final five paired frames (editor after trigger-back, action catalog, editor after action-back, constraint catalog and editor after constraint-back) have zero unequal pixels. These individual observations do not certify the complete earlier sequence. The shared onboarding process change remains a failed continuous-process prerequisite.

The capsule contains the actual replay program and complete derived JSON, plus the exact local logs for 33 first-use tests, 93 combined session/parity-tool tests and five archive controls. These host tests do not establish Android execution. The later reviewed stale-evidence guard findings and their correction have separate records and do not rewrite these historical bytes.

Assemble and verify the 10,661-byte ZIP with the existing repository helper:

```sh
python3 scripts/assemble_artifact.py docs/verification/editor-navigation-736da19/manifest.json
```

The six small binary parts were checked against their actual Git blob SHA values before publication. The assembled ZIP SHA-256 is `2031b3c1e8989883191966ba9097383717514c63eee76db3c4f3bbc8ca629f00`. Its six member names, lengths and hashes are listed in the manifest. `replay_frames.py` operates only on preserved evidence and requires Pillow and NumPy; it never installs an APK or operates a device.
