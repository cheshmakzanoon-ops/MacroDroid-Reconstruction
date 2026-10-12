# Independent Widget ART workflow proposal

## Ready for publication and a new disposable Android job

The proposed repository change is exactly `.github/workflows/widget-method-probe.yml`. It runs the already reviewed, immutable `work-in-progress/widget-art/01-wrapper-review` probe package against the original APK and the inactive Widget APK. Existing editor, reconstruction and constructor workflows are unchanged. The proposal has passed offline validation; **no Android execution has occurred in this workflow preparation**.

The original input is reconstructed from `vendor/original/manifest.json`: `MacroDroid-5.67.8-original.apk`, 95,725,918 bytes, SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The candidate is reconstructed from the durable `work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json`: `MacroDroid-5.67.8-widget-update-06.apk`, 94,683,439 bytes, SHA-256 `b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`. That manifest retains the historically correct initial host-metadata failure. The artifact bytes are also the independently verified later successful Widget candidate; the workflow does not rewrite historical evidence.

The probe DEX remains 7,580 bytes, SHA-256 `79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07`. Its frozen checkpoint SHA-256 is `aa979100f925ba216d1a78dbb9de9c293d5b2e4b771210c2862556bf6946585a`. The workflow neither rebuilds the probe nor substitutes host Android/application classes.

## Execution and evidence scope

Push triggers are limited to the new workflow's own path and the frozen Widget ART package, on `main`; `workflow_dispatch` is also available. The job uses the exact checkout and upload action commit pins from the existing editor workflow, a read-only repository token, and no persisted checkout credential. Concurrent runs are queued rather than cancelling an active evidence collection.

Preflight checks ten fixed script/checkpoint/manifest SHA-256 values and all eleven files from the hash-bound probe checkpoint. It records and copies these exact inputs plus the executing workflow. The two artifact manifests additionally require their exact expected filename, size and whole-APK SHA-256. Assembly then verifies every multipart file and the full APK bytes using the current repository assembler. No complete application source tree or active current APK is materialized.

The job runs the current six downloader controls and all 27 packaged wrapper controls. The latter remain explicitly simulated host tests; complete simulated command/evidence trees are saved under `host-control-evidence`. The frozen wrapper's execution backend and result validator keep these traces distinct from real device execution.

The Android bootstrap must start in a fresh `$RUNNER_TEMP/macrodroid-widget-tooling` directory. The existing checksum-pinned downloader and AVD creation logic are unchanged. The job saves verified installation logs, package metadata, AVD configuration and observed host binary hashes. It starts `MacroDroid_API35_Disposable` on `emulator-5560` with the pinned runtime service, KVM enabled and no snapshot. The existing readiness helper is bounded at 900 seconds; the probe independently checks the exact device fingerprint, SDK, ABI, native bridge, boot state and AVD again.

`runtime_job.py` submits the approved wrapper with a 720-second outer queue bound. Each original/candidate AndroidRuntime process retains the wrapper's 120-second guest bound, `app_process64 -Xverify:all`, exact two-file classpath, empty late VM option guard, unchanged input checks and fresh owned device directory. The probe checks all eight bounded original/candidate cases. It records semantic outcomes separately from stderr cleanliness, and only the wrapper's complete strict success exits zero. No application installation, UI capture, real widgets, API upload or network call is requested by this job.

The EXIT handler is installed immediately after the owned service PID is captured and before writing its PID receipt. It collects bounded lifecycle diagnostics, writes `STOP` only into the job's freshly created queue, and waits at most 60 seconds for that service to exit. A nonzero service exit, missing STOP, timed-out service wait or failure to save the cleanup receipt makes a previously successful step fail. An existing nonzero probe status is retained. Auxiliary logcat failure remains explicitly recorded as a diagnostic outcome; it cannot manufacture a probe success. A service timeout is recorded as unconfirmed cleanup, never silently accepted as stopped. No unrelated process, AVD or file directory is stopped or deleted.

The final pinned upload action runs under `always()` and includes the complete `ci-widget-method/` tree: input copies, both manifest assembly logs, downloader/wrapper test logs, all simulated control evidence, bootstrap and toolchain metadata, driver/service/readiness/lifecycle logs, complete runtime queue requests/responses, complete device probe command streams and postchecks, and the owned-service cleanup receipt. Partial failures are retained.

## Measured offline validation

The actual validation completed at 2026-10-12 04:56:56 UTC. All five shell run blocks passed `bash -n`. The complete preflight executed successfully against private copies of the exact 22 selected baseline/package files. Nine deliberate preflight controls were rejected: changed original manifest, changed candidate manifest, changed bootstrap, changed runtime service, changed frozen checkpoint, changed wrapper, changed probe DEX, a symlinked runtime script, and a pre-existing output directory. Failure JSON and command streams are retained.

Four harmless local service simulations executed the workflow's extracted cleanup function: ordinary success, retaining a probe exit status of 7, rejecting service exit status 5, and rejecting failure to write the cleanup evidence. Each used a temporary fake ADB executable and a bounded local process, with the exact new STOP path and no Android device. All four preserved the expected result and owned cleanup behavior.

The actual six downloader unit tests and 27 packaged wrapper unit tests then passed from independent byte-verified copies. The validation's complete 21-command record, exact script extracts, all preflight artifacts and simulated wrapper traces are archived. `baseline-inputs.json` records the exact source hashes; `reports/validation-01/result.json` records the observed outcomes and the workflow SHA-256. These controls validate workflow guards and failure handling, not the real APK's Android behavior. That remaining result must come from the new hosted job.

## Integration handoff

Publish only the proposed workflow to the active workflow path. Preserve this complete proposal and evidence under an inactive Widget ART workflow-review checkpoint. Existing pinned Android tooling, frozen probe files and APK manifests should remain byte-identical; if any changes, this job intentionally fails preflight until a new review binds those inputs. The repository transfer agent owns the commit, push and dispatch. No current app registry, source, signing configuration, APK manifest or existing workflow is changed by this proposal.
