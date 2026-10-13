# Android render-drift investigation — run 38373019802

This is a **diagnostic only** investigation of the 13 October 2026 KVM Android 35 cold-start evidence. It does not turn the failed Android CI job green and does not modify either APK.

Evidence: GitHub Actions run [38373019802](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38373019802), artifact `android-cold-launch-ff1f6d9cccc685dfa24d471b08de31ef1230ac75` (ID `11799464324`). Exact image members are `capture/original-intro-2.png`, `capture/candidate-intro-2.png`, `capture/original-post-intro.png`, and `capture/candidate-post-intro.png`. Reference APK SHA-256: `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; rebuilt APK SHA-256: `bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2`.

## Exact findings

| Frame | Changed decoded RGBA pixels | Inclusive bounds (x1,y1,x2,y2) | Result |
| --- | ---: | --- | --- |
| TRIGGERS introduction | 26 / 921,600 | `(313,1184,351,1199)` | Mismatch inside the bottom page-indicator region |
| Notification-permission surface | 570,819 / 921,600 | `(0,0,719,1279)` | Full-frame mismatch dominated by background dimming |

The dialog itself appears in both captures. Its foreground XML matches in the earlier strict comparator; this diagnostic rechecks complete PNG pixels and **does not suppress the observed differences**. The most frequent changed pixel pair on the permission screen is original RGBA `[107,163,104,255]` to candidate `[43,65,42,255]` (522,040 positions), consistent with different background dimming in these snapshots. This observation alone cannot establish why it happened or whether it persists after the rendering settles.

The machine-readable [exact audit](android-render-drift-38373019802.json) includes both image hashes, complete changed-pixel counts, bounding boxes, row coverage, and leading RGBA transformations. It was generated with `tools/android/audit_render_pairs.py`, using the repository's strict PNG decoder. Ten host regressions passed, including corrupt PNG rejection, alpha-difference detection, dimension mismatch, and input-file alias rejection.

## Next evidence gate

Capture a short, timestamped **multi-frame series** at both surfaces separately for both APKs on the same configured emulator. Retain every full screenshot, live process checks and UI hierarchies; compare full frames without masks or tolerance, and keep the original startup test failed until it actually matches. Only then should an application-source fix be selected. A 26-pixel transient dot difference and a window-dim transition must not be guessed into a source-code change.

This evidence has no bearing on macro saving/execution, scheduled triggers, persistent data, background services, integrations or whole-app 1:1 parity.
