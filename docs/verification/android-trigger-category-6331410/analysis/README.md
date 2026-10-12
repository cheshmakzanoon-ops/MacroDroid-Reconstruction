# Zero-scale twelve-screen run: exact evidence replay, five-pixel failure

Both apps complete all twelve declared screens, including the expanded Date/Time trigger category. **The full journey comparison fails because five pixels differ on the TRIGGERS introduction page.** All twelve hierarchy files match byte for byte, and the other eleven full PNGs match byte for byte. No mask, crop, pixel tolerance, or cross-app frame selection was used.

This is [run 38216299675](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38216299675), job `114701722464`, commit `6331410cfd2391389270564803623079e8355ad8`. The installed original is SHA256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the installed candidate is SHA256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. The workflow changes only the disposable-device observation procedure and uses the already published candidate. The exact APK and complete frozen workflow input identities are rechecked by the preserved final verifier.

## Full-frame results

| Declared screen | Changed RGBA pixels | Exact XML bytes | Complete unmodified screenshots |
| --- | ---: | --- | --- |
| intro-1 | 0 | Yes | [original](review-captures/original-intro-1-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-1-acquisition-1-frame-2.png) |
| intro-2 | 5 | Yes | [original](review-captures/original-intro-2-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-2-acquisition-1-frame-2.png) |
| intro-3 | 0 | Yes | [original](review-captures/original-intro-3-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-3-acquisition-1-frame-2.png) |
| intro-4 | 0 | Yes | [original](review-captures/original-intro-4-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-4-acquisition-1-frame-2.png) |
| notification-request | 0 | Yes | [original](review-captures/original-notification-request-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-notification-request-acquisition-1-frame-2.png) |
| reference-promotion | 0 | Yes | [original](review-captures/original-reference-promotion-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-reference-promotion-acquisition-1-frame-2.png) |
| home | 0 | Yes | [original](review-captures/original-home-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-home-acquisition-1-frame-2.png) |
| empty-editor | 0 | Yes | [original](review-captures/original-empty-editor-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-empty-editor-acquisition-1-frame-2.png) |
| favourite-triggers-info | 0 | Yes | [original](review-captures/original-favourite-triggers-info-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-favourite-triggers-info-acquisition-1-frame-2.png) |
| after-favourite-info | 0 | Yes | [original](review-captures/original-after-favourite-info-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-after-favourite-info-acquisition-1-frame-2.png) |
| trigger-catalog | 0 | Yes | [original](review-captures/original-trigger-catalog-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-trigger-catalog-acquisition-1-frame-2.png) |
| after-trigger-date-category | 0 | Yes | [original](review-captures/original-after-trigger-date-category-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-after-trigger-date-category-acquisition-1-frame-2.png) |

The actual final status is `TRIGGER_CATEGORY_TWELVE_SCREEN_DIFFERENCE`, with `evidence_valid=true` and `journey_equal=false`. The comparison reports `catalog_navigation_established=true` and `trigger_selected=false`. The final independent verifier reproduces that result; its nonzero result is a retained visual failure. Both journey records are complete, with twelve captures and eleven inputs each. No input follows the Date/Time category capture.

The five changed coordinates are `(317,1186)`, `(319,1189)`, `(335,1192)`, `(319,1194)`, and `(336,1195)`, inside exclusive bounds `[317,1186,337,1196)`. Their exact original/candidate RGBA values are retained in [all twelve full-frame pairs](all-twelve-full-frame-pairs.json). They lie in the existing introduction page indicator region; this observation does not identify a new app-source cause. The previous runs and their different measured pixel counts remain separate evidence.

All 46 acquisition ledgers accept the first two consecutive identical full PNG/XML frames. The diagnostic verifies 552 physically distinct observation artifacts. Four retained TRIGGERS frames per app include the accepted screen and the fresh pre-input capture. All twelve within-app frame-pair comparisons contain zero changed pixels; all sixteen cross-app combinations retain exactly five changed pixels. The complete timings, identities and frame comparisons are in [the frame diagnostic](frame-and-selector-observations/result.json), [all 46 ledgers](frame-and-selector-observations/all46-stabilization-ledgers.json), and [all 28 pair comparisons](frame-and-selector-observations/all28-within-and-cross-trigger-frame-pairs.json). No intermediate frame was discarded to obtain equality.

## Recorded crashes and continuation

Both apps retain an actual Java fatal exception during the notification-denial boundary: `java.lang.IllegalStateException` from `android.app.Fragment.getResources`, reached through `com.zx.lbua80.onShow`. The original process changes from PID 4191 to 5414, and the candidate from PID 7055 to 8118. The guarded boundary verifies the old PID is absent in both process lists, verifies the new single process and expected `NewHomeScreenActivity`, and obtains a fresh installed-APK hash before continuing.

The [recorded process-boundary summary](recorded-process-boundaries.json) links the exact command outputs, boundary records and literal crash buffers. The candidate buffer also retains earlier buffer contents; the recorded policy classifies the newly observed exception. Object identifiers and literal crash messages have not been normalized in those raw outputs. The paired continuation classification is equal, but no claim of equal literal crash messages or a crash-free run is made. `crash_free_run_established=false` remains explicit.

## Observed Date/Time category and next-step boundary

The final screen is foreground `com.arlosoft.macrodroid/com.arlosoft.macrodroid.selectableitemlist.AddTriggerActivity`. Both complete PNGs have SHA256 `7057b96a46d56c0e53a3b42a3475a24812b5867a753bcf81b528e9a8a6aefa92`; both XMLs have SHA256 `9bb3a60891fc9194b2f9ae493e513a041a6ee2e395125c13dbeb8cef648abcd0`.

The actual hierarchy contains seven enabled clickable rows: Calendar Event, Day of Week/Month, Day/Time, Regular Interval, Stopwatch, Sunset/Sunrise, and System Time. The `Day/Time` text node has resource ID `com.arlosoft.macrodroid:id/select_item_name` and is not itself clickable. Its unique enabled clickable ancestor is `com.arlosoft.macrodroid:id/select_item_row_frame`, with bounds `[14,574][354,678]`. Its center would be `(184,626)` for a future input after fresh identity/PID/component/XML guards. This run did not select that row or create, save, or execute a macro. The exact original and candidate selectors and all visible row bounds are preserved in [observed rows](frame-and-selector-observations/observed-date-time-category-rows.json).

## Device configuration and complete replay

The device configuration finishes with primary WCDMA signal level 4 after a 15.329-second stable interval and a declared SystemUI demo clock of `1200`. All 36 configuration commands and their 72 output hashes are verified. A separate explicit nineteen-command helper sets and verifies `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` to `0`. All original/candidate before/after recorded environments match. The actual commands and observations remain in the raw evidence and [configuration summary](configuration-summary.json). This still-frame configuration does not establish animation timing parity.

The independent replay reconstructs all 192 expected input-copy roles from the pinned preparer, rather than trusting a mutable preflight row list. It verifies all 2,944 raw files before and after replay, all 46 capture ledgers and 92 observations, and 2,498 unique referenced journey artifacts. It replays the exact pinned final verifier and captured comparator, matching both result objects except the explicitly fresh verification timestamp. A private hardlink view is used for the large immutable inputs; the generated final report has a distinct inode, and the view is removed afterward. No original archive, APK, source, screenshot, or runtime record is modified.

The actual hosted logs contain 130 guard-test successes in 37.469 seconds, ten zero-scale helper successes in 0.209 seconds, and six downloader successes in 0.004 seconds. The job's bounded owned-service cleanup succeeds despite the visual failure. The complete result, import pins, all member identities, reconstructed inventory, observation records, host-test summaries and actual replay logs accompany this README. This evidence establishes neither complete high-level source reconstruction nor full runtime 1:1.

## Original archive and explicitly labeled review log

Artifact `11732104868` is exactly 42,199,893 bytes, SHA256 `1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3`. Its 2,944 members total 65,045,879 bytes. The publisher preserves the whole unchanged ZIP through the parent directory's manifest and all unchanged members under `../extracted/`; the [complete member identities](all-2944-member-identities.json) and [original extraction receipt](original-extraction-receipt.json) bind them. No second raw archive or APK copy is created by this freeze.

The raw emulator boot log contains one ephemeral ADB public-key value. The original log and ZIP are preserved unchanged; public material alone is not a private credential. Only the clearly labeled [review-log copy](emulator-boot-public-value-omitted.review.log) omits that one value for readability, with the exact one-line transformation and both hashes in [its receipt](review-log-transformation.json). The extractor's documented scan of every member found no matching private-key pattern; that statement is limited to the actual scan, not a universal secret audit. The public value is not repeated in this summary.

This is an additive evidence capsule with no active-file changes. Existing complete analysis and selected raw review files are hardlinked during the local freeze to avoid duplicate payload allocation under disk pressure. Their exact content hashes are frozen in `checkpoint.json` and are not edited afterward.
