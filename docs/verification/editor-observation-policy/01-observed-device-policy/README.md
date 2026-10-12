# Observed editor policy: frozen host proof and next Android capture

This checkpoint contains the reviewed opt-in process-boundary/full-frame recorder and separate ten-screen Favourite Triggers adapter. **All 76 host tests passed. Actual execution of this new policy on Android is pending.** The latest actual editor run remains failed with a 26-pixel TRIGGERS difference, shared Java crashes, and incomplete catalog navigation; see [its preserved evidence](../../../../docs/verification/editor-journey/run-38202401351-attempt-1/analysis/README.md).

## Active change

The active source files are under `source/`; `checkpoint.json` records each repository destination, prior hash (or required absence), and final hash. The two modified existing files are the common recorder and editor workflow. The external reference adapter, fourteen-step plan, XML ParseError retry adapter, downloader code, download tests, bootstrap logs, lifecycle logs, and prior fixture/tests remain unchanged.

The workflow baseline is the exact `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d` version. Its change selects `favourite_info_journey.py` and enables `--observe-denial-handoff --settle-full-frames`; all existing infrastructure and artifact steps remain intact. The original app source and APK are not modified by this checkpoint.

The new ten-screen plan retains the first eight reference steps, observes the Favourite Triggers information dialog, verifies its exact title/message/unique enabled OK button and fresh installed APK/PID/EditMacroActivity, taps OK once, captures the first resulting app surface, and stops. The previous thirteen- and fourteen-step action sequences retain their default behavior. A future match after both known crashes is labeled `MATCHED_POST_CRASH_CONTINUATION_ONLY`, never crash-free or full runtime parity.

## Evidence checks

The recorder accepts the first pair of consecutive identical complete PNG/XML byte observations. Six attempts and a 30-second shared capture deadline bound settling; the existing ParseError-only retry retains every partial acquisition within that same deadline. The 15-second input freshness bound includes installed-APK/diagnostic work, both full-frame observations, and final live PID/component checks. New PID anchoring is restricted to the observed notification-denial boundary, with two complete process lists, old PID absence, fresh installed SHA-256, stable new PID/NewHomeScreenActivity, and raw before/after crash diagnostics. Later or within-input restarts remain failures.

The actual LB fatal stack is recognized only from a newly recorded exact fatal block for the old PID. Raw messages, runtime instance IDs, timestamps, PIDs, and complete logs remain available. Unexpected fatal stacks fail closed. An empty or unavailable Java crash buffer does not prove the absence of crashes. Paired lifecycle/crash outcomes and all final pixels/XML attributes are compared.

The bounded cache stores at most four **pure decode results**, keyed by the exact complete PNG bytes and decoder function. It avoids repeated decoding inside the unchanged input deadline; every artifact is still read/hash-checked and every device observation still occurs. The dedicated control checks identical, different, corrupt, and different-decoder inputs plus the size bound. The actual full-image timing check recorded 11 calls with one miss and ten hits, with all RGBA bytes identical to the direct decoder; timings are one local host observation, not a hosted runtime result.

## Host results and retained failures

The final command was:

```sh
python3 -B -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v
```

It passed all **76 tests in 60.285 seconds**, including all 31 unchanged legacy tests and 45 new tests. The new controls cover complete synthetic ten/fourteen-screen captures, changed pixels/XML, paired process outcomes, old PID persistence, wrong/reused installed checksums, process/component changes, stale/late input observations, every retained settling attempt, actual XML ParseError retries, exact observed dialog geometry, raw known crash fixtures, unknown/truncated fatal blocks, and command timeout output. The virtual ADB controls execute the actual recorder and input code but do not execute Android.

Numbered failed attempts are preserved under `host-attempts/`:

- **02:** The actual XML fixture rejected a proposed message constant containing literal backslash-n sequences instead of the two actual newline characters in the parsed message. Both failing controls and the source state are retained. The pre-fix source bytes were recreated from the recorded one-line correction; their hash was not recorded during the failed run. That reconstruction is explicitly labeled in the attempt manifest.
- **03:** The existing PID guard correctly raised `android_compare.CaptureError` and stopped the input. A new test had incorrectly expected only the narrower `JourneyError`. The corrected test requires the actual specific PID/component rejection message through their `ValueError` contract. The runtime guard was not relaxed.

Historical 61-test and pre-cache 75-test logs are retained as development history; they do not replace the final 76-test gate or establish an Android result. Full unchanged fixture PNG/XML/log lines, their provenance, the final source, exact text patch, baseline receipts, and final command/log hashes are bound by the checkpoint.

To reproduce the host gate, overlay the `source/` paths onto a checkout matching the recorded baselines and run the command above. The unchanged project comparator and archived existing fixture used by the tests are pinned in the input receipt. `reports/measure_decode_cache.py` can be copied into that checkout's `reports/` directory for the same bounded measurement.
