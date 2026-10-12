# Ink indicator: exact source dossier and retained-fraction hypothesis

## Finding and scope

The strongest current hypothesis is a retained joining fraction caused by the indicator's animation finishing before the ViewPager's independent scroll. The original callback logic permits this state to remain after scrolling stops. Its affected geometry is consistent with the five changed pixels in the exact Zero12 captures. **The actual callback sequence and private fields were not recorded, and the cause of those five pixels remains unproven.**

This dossier contains read-only APK disassembly, exact source comparisons, full-frame comparison of every retained TRIGGERS frame, public framework source, and four explicitly labeled source-derived state traces. It performs no Android run, APK build, active-source edit, coverage exemption, image alteration, or relaxed parity check. The separate Android experiment remains a proposal in `PROPOSED_ANDROID_EXPERIMENT.md`.

The prior eighteen-class audit is retained at `indicator-diagnosis/checkpoints/01-preserved-source-audit/checkpoint.json`, SHA-256 `8792b2936e0d2832361c98699b707ceb7982373cbb661048b549bedfcce174ab`. That audit has eighteen classes in total, including InkPageIndicator. This study verifies every one against both captured APKs and adds eight specific source dependencies.

## Exact artifact and capture bindings

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Original APK | 95,725,918 | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Combined candidate APK used by Zero12 | 94,683,119 | `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` |
| Original downloaded Zero12 artifact ZIP | 42,199,893 | `1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3` |
| Captured journey JSON | 839,255 | `a6253dfea14353a2d8fe552e3772e4fe5e58a693e2339bafcce9f0d008a61409` |
| Original accepted TRIGGERS PNG | 75,366 | `9c5afe54308ce2bf5cf00fd5a95c24ad589f83ff590ecad3cb95cf6f94576322` |
| Candidate accepted TRIGGERS PNG | 75,368 | `92a14136c68347341c9dd190adef81f5453a91190dc857585b04ce8a65e1e25e` |
| Both accepted TRIGGERS XML files | 6,689 each | `840d3f966746dea5dffe838eda7b46b0c7f48ee37b59d33cbcb28336f199dfd8` |

The raw run is `38216299675` at source head `6331410cfd2391389270564803623079e8355ad8`. Its preserved outcome remains a twelve-screen difference, with five pixels on TRIGGERS. The report here does not relabel its separate permission-denial/crash boundary.

Both captured environments report API 35, `emulator-5560`, 720 × 1280 pixels, density 320, font scale 1.0, timezone UTC, and all three animation scales equal to zero. The exact fingerprint is `google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`. Complete before/after environment objects are saved in report 03.

## What the fresh byte comparison establishes

`collect_indicator_evidence.py` used the pinned JDK and the production baksmali implementation with `--api 23 --use-locals -j 2`, selecting exact descriptors directly from each APK's `classes.dex` and `classes3.dex` entries. It wrote only selected class disassemblies. Four bounded subprocesses returned zero; their exact argv, elapsed times, stdout, stderr, and output hashes are retained.

All **36 comparisons for the historical eighteen classes** match complete preserved smali bytes. The eight additional classes are the actual saved-state creator/state, data-set observer, page-color callback, next-page Runnable, float helper, styleable array, and ViewPager dispatcher. Across the extended scope, **51 of 52 complete-class comparisons match**.

The initial all-class assertion correctly failed for `Lq77;` in the candidate. Its `B(String,String,StringBuilder)` body is an existing registered string recovery. The failed result, full difference, command evidence, and the exact collector used (`ec84ee7d904340236eaddfbb6bcf947c157fa0f2817ceb03630fe540a4c3df02`) remain in report 01.

Report 03 gives the narrower supported conclusion. Every original method signature and all non-method metadata in q77 are unchanged. Its sole changed body is the exact registered B method. The indicator and interpolator call `t(FFFF)F`; that complete method body matches original, preserved source, and candidate. The report records the precise registration and retains the full invoked method. It does not describe q77's whole class as equal.

The corrected review rechecked 209 input identity observations before and after execution. It reused the closed disassemblies and performed no additional disassembly. Its bounded process returned zero in 3.756 seconds with empty stderr. Report 01's broader failure remains a distinct result.

## Exact raw pixel observations

Report 03 independently compares all four retained TRIGGERS frames per APK: the first and second accepted acquisition frames, and the first and second fresh frames before the next input. Each of the sixteen PNG/XML files matches its bytes inside the exact original downloaded ZIP. Every comparison covers the complete 720 × 1280 RGBA frame.

All twelve within-APK pairs have zero changed pixels. All sixteen cross-APK pairs have the same five changed pixels. The analysis makes no choice of a more favorable frame.

| Coordinate, zero based | Original RGBA | Candidate RGBA |
| --- | --- | --- |
| (317, 1186) | (172, 36, 36, 255) | (200, 109, 109, 255) |
| (319, 1189) | (172, 36, 36, 255) | (200, 109, 109, 255) |
| (335, 1192) | (172, 36, 36, 255) | (200, 109, 109, 255) |
| (319, 1194) | (172, 36, 36, 255) | (200, 109, 109, 255) |
| (336, 1195) | (190, 83, 83, 255) | (212, 140, 140, 255) |

The XML identifies the indicator at `[128,1184][592,1200]`. The unchanged layout specifies diameter 8 dp, gap 8 dp, and animation duration 320 ms. At the captured density, the measured layout and original `onMeasure` formula imply radius 8 pixels and centers `(312,1192)`, `(344,1192)`, `(376,1192)`, `(408,1192)`, assuming the zero indicator padding shown by this layout.

Four differing candidate pixels take the same ink color as the unselected dot interior. The fifth is consistent with extra ink beneath the selected circle's antialiased edge. All five lie on the facing sides of the old first dot and selected second dot. The color and location interpretation is an inference from the raw pixels and source geometry. No private Paint or Path state was captured.

## Later run variation and scale-one limitation

Report 07 independently binds the later DayTime13 run `38221713675` to its exact ZIP, SHA-256 `ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4`. It uses the same original and combined candidate APK identities and reports all three scales as zero. Every one of its five available paired screens has zero RGBA differences and identical XML: intro1, intro2, intro3, intro4, and notification request. The original then fails, while the candidate has thirteen completed screens. The journey remains `RECORDED_NOT_PARITY` and supplies no thirteen-screen parity claim.

Both later intro2 PNGs are 75,316 bytes with SHA-256 `6e98d2ba0e7d3bd76b15f3e9f6de6ab698f763caa6d89f43672d00a75067a845`. Comparing these complete frames to the earlier run gives:

| Exact accepted-frame pair | Changed pixels |
| --- | ---: |
| Earlier original / earlier candidate | 5 |
| Later original / later candidate | 0 |
| Earlier original / later original | 31 |
| Earlier candidate / later candidate | 34 |

All 31/34 cross-run changed coordinates fall within `[313,1184]` through `[351,1199]`, inside the indicator bounds. This establishes raster variation between real runs for unchanged APK identities. The internal timing, state, or rendering cause remains unknown. Every coordinate and RGBA pair is retained; the original five-pixel failure is unchanged.

Report 08 independently binds the prior all-scales-one run `38212813248` to its 28,080,813-byte ZIP, SHA-256 `93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92`. This older run used original `84333011…` and candidate **`9108b581…`**, so it is not a scale-one observation of combined candidate `5f635e…`. Both stopped at intro2. The original retained five completed acquisitions before its command deadline expired; the older candidate retained six before the consecutive-frame limit failed.

All nine consecutive full-frame pairs in those failed acquisitions differ, by 8,223 through 16,312 pixels, while their XML remains identical. Their changed coordinates are in the animated central content, away from the indicator. This independently confirms the practical full-frame settling obstacle cited by root for the continuing intro2 Lottie animation. The exact failure reasons and raw ledger copies are retained. These are failed full-frame captures, regardless of any local indicator stability.

## Source callback sequence

The full selected classes are retained in report 01. Report 06 also retains 22 complete method excerpts from nine classes, with individual hashes. These are the relevant operations:

| Source | Observed operation and consequence |
| --- | --- |
| `InkPageIndicator.setSelectedPage(I)` | Stores old page in `v`, new page in `u`, and sets `E=true`. Builds selected-circle animator H and retreat animator I. H has a start delay of `k/4` when `x` was true and duration `3*k/4`; I has duration `k/2`. |
| `x82.onAnimationUpdate`, arm 5 | Stores H's animated float in `w`, invokes I's threshold test, then posts invalidation. |
| `oz7.b(F)` | Starts a not-yet-started dependent animator on a strict threshold crossing. |
| `iz7.onAnimationStart`, arm 1 | Sets `x=false` for the selected-circle animation. |
| `iz7.onAnimationEnd`, arm 1 | Sets `x=true`. |
| `kz7.onAnimationUpdate` | Stores the retreat boundary, posts invalidation, then tests reveal animator thresholds. |
| `lz7.onAnimationStart` | Clears joining fractions, seeds relevant reveal fractions, sets retreat boundaries, and posts invalidations. |
| `lz7.onAnimationEnd` | Sets `A=B=-1` and posts invalidation. |
| `iz7.onAnimationEnd`, arm 0 | Calls `f()`, then sets `E=false`. |
| `f()` | Replaces `z` and `C` with zeroed arrays, sets `A=B=-1`, and sets `x=true`. |
| `x82.onAnimationUpdate`, arm 6 | Stores the reveal fraction and posts invalidation. |
| `v6.onAnimationEnd`, arm 3 | Clears that reveal fraction and posts invalidation twice. |
| `lt1.run`, next-page arm | Calls `ViewPager.setCurrentItem`, clears all joining fractions, and posts invalidation. |
| `InkPageIndicator.c(I)` | Scroll-state callback has no effect. |

This graph includes multiple explicit completion invalidations. A theory based solely on `f()` lacking its own invalidation is incomplete.

### The retained old slot

The original `b(IFI)` scroll callback first chooses `previous = E ? v : u`. If `previous != position`, it replaces the fraction with `1 - fraction`, using float arithmetic. It then writes only `z[position]` and posts invalidation. The special position adjustment happens only when the complemented fraction is exactly one.

For the first transition, after retreat completion, `u=1` and `E=false`. A late callback with `position=0` and a fraction just below one therefore stores a small positive value in `z[0]`. The terminal callback `b(1,0,...)` stores zero in `z[1]`. It does not clear `z[0]`. The empty scroll-state callback supplies no later reset.

The preserved ViewPager supplies that possible change of position. `computeScroll()` obtains integer coordinates from Scroller, scrolls the View, and calls `n(int)`. Its `i()` chooses the item containing the current scroll coordinate; `n()` computes that item's fraction and calls `k()`, which dispatches `b()` to the registered listeners. At an exact page boundary it can select the new item at fraction zero.

For a zero-velocity one-page movement with width 720, page width factor one and zero page margin, ViewPager's original `t(IIZZ)` computes a 200 ms scroll duration and passes it directly to `Scroller.startScroll(IIIII)`. Its code does not consult ValueAnimator's duration scale. These geometry/velocity assumptions fit a next-page button transition, but this dossier does not claim to have observed the actual Scroller fields.

### Why the resulting drawing can remain different

With `A=-1` and `0 < z[0] <= 0.5`, the unchanged `onDraw()` takes the two facing cubic/arc-lobe branch. A zero fraction takes the ordinary-circle branch. Thus a small retained positive fraction changes the generated geometry even after H, I, and all reveal animators have completed.

Each draw rewinds the working paths. Persistent pixels therefore do not prove a persistent Path object payload; the persistent input fraction can reconstruct the same geometry on every draw. The original code also appends the prior aggregate into the working path and then appends that working path back into the aggregate. That duplication is common to both APKs and is preserved here. This study does not attribute a renderer defect to it.

## Public framework corroboration and its limit

Reports 02 and 04 retain the exact HTTP base64 payloads and decoded Java source from the public `android-15.0.0_r1` tag:

| Public source | Decoded SHA-256 | Relevant behavior |
| --- | --- | --- |
| [ValueAnimator.java](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/animation/ValueAnimator.java) | `3aafaafec131af7e0a24f7fc92cfbfd6b92bd88df2b5817efb43e937ddfea059` | Scales duration and start delay; a zero scaled duration reaches final fraction on a pulse and ends. |
| [AnimationHandler.java](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/animation/AnimationHandler.java) | `83fdf46aec4ce558e5314aeb9f9f456e992f224de7dea46948d7e9ce6af42d2e` | Snapshots callback count for a frame; newly registered child animators are not added to that same iteration. |
| [Scroller.java](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/widget/Scroller.java) | `aade9e1845d0941044145323af21f97c9fe007789849922d7ca54c340b6312ee` | Stores the explicit startScroll duration and advances using animation clock time. |

These sources make an early indicator completion under scale zero plausible while a 200 ms Scroller continues to dispatch positions. The Google API emulator's framework files have not been extracted or byte-compared to this public tag. The source explanation is conditional on the described runtime behavior; it is not a measured callback chronology from the captured process.

## Source-derived witness and preserved failures

`source_derived_ordering.py` records four small float32 traces. They assume the last nonterminal scroll coordinate is either 718 or 719 before a terminal coordinate of 720. If the retreat reset comes first, the last two callbacks leave different positive `z[0]` values while `z[1]` is zero in both. If the reset follows the terminal callback, both values become zero.

This is a transcribed state model. It executes neither original DEX nor candidate DEX, adds zero parity cases, and predicts no exact pixel count. Its assumed 718/719 samples were not observed. It demonstrates that the source admits the proposed retained state and identifies what a runtime experiment needs to distinguish.

The first model excerpt selection used an incorrect `lt1.onClick` name. The exact class implements Runnable. That KeyError and the exact failed model source are preserved in report 05. The corrected report 06 selects `run()V`, records all 22 excerpts, and closes with four labeled traces. No historical output was overwritten.

## Next reviewable step

The proposed experiment uses unchanged APKs and an identical one-tap intro prefix within each condition. It varies only the animator-duration scale between zero and one, keeps window and transition scales zero, retains every predetermined full-frame capture, and repeats both APKs in a fixed crossover order. The prior all-scales-one failure above motivates a fixed five-sample diagnostic schedule, with all animation and full-frame differences retained. Indicator-local observations supply no full-frame parity criterion. The older and later runs already establish cross-run variation, so the proposed experiment's remaining purpose is to test the specific scale dependency. Its exact action and evidence contract is written separately for root review. No workflow or runtime action is activated by this dossier.
