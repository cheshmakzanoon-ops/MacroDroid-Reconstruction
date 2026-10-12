# Current reconstruction candidate

This directory preserves the signed hybrid candidate containing **1,238 recovered
Java method bodies across 602 classes**, including the recovered touch-blocking
action. The APK is a development candidate. Whole-app 1:1 Android runtime parity
has not been established.

| Property | Value |
| --- | --- |
| Source recovery checkpoint | `06bbded7b0428144a0da24308b76bc6148b97ec0` |
| APK bytes | 94,683,307 |
| SHA-256 | `2eabb2d883598254ca71f99999297e1b98fa9ea56fb24c200d5f053456cff4d6` |
| Ordinary Git parts | 12, each at most 8 MiB |
| Build output compatibility name | `dist/MacroDroid-5.67.8-v9-hybrid.apk` |

Reassemble the exact candidate from the repository root:

```sh
python3 scripts/assemble_artifact.py artifacts/current/manifest.json
```

The default output is
`workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk`. Add `--verify-only` to
check every committed part and the full APK checksum without writing an output.
The assembly command does not install or run the app.

Use the SHA-256 and committed verification reports to identify the exact tested
candidate; the legacy `v9` build filename is not a claim that these bytes equal the
historical 1,237-body v9 APK. Original-reference bytes are preserved separately in
`vendor/original/`; the complete historical source/toolchain snapshot remains in
`vendor/v9/`.

The candidate uses the distributed development signing identity. Source recovery,
successful assembly, host differential tests and Android runtime behavior are
separate acceptance gates. Read `project/RECONSTRUCTION_STATUS.md` and the current
reports under `docs/verification/` for measured progress and remaining limits.
