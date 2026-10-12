# Editor device setup rejected a real radio-type change

[Editor run 38214498409](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498409) failed before the app journey was queued. The complete device-configuration evidence reports `CAPTURE_DEVICE_CONFIGURATION_FAILED`: **the primary radio changed from LTE to WCDMA at the final configuration check**, while the computed signal level stayed at 4. This is a device precondition failure. There is no app-image or app-behavior conclusion from this run.

The exact source commit is `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. The [configuration report](raw/device/capture-device.json) preserves its own precise reason: `Primary radio type or computed level changed at configuration completion`. The independent analysis re-parsed the actual final raw telephony outputs using the helper's source from that exact Git commit; it did not rely solely on the summary fields.

| Observation | Actual primary type | Computed level |
| --- | --- | ---: |
| Confirmed after 15.178 seconds of stability | `CellSignalStrengthLte` | 4 |
| Completion observation | `CellSignalStrengthWcdma` | 4 |

The earlier raw LTE measurements vary inside the same computed level and remain retained. The final change is in the primary radio type itself, which is one of the existing guard's two declared fields. All 41 ADB commands returned exit code 0; their 82 stdout/stderr files and hashes are intact. The final command succeeded at obtaining the changed state, and the guard then correctly rejected it.

The raw completion reads show all three animation scales at zero and SystemUI demo mode enabled, but the report deliberately keeps `requested_animation_scales_observed=false`: it failed before reaching the overall final verification. This analysis preserves that flag and does not turn partial settings changes into successful configuration. Battery, app resources and screenshots were not changed by the helper.

The [service log](raw/service.log) records one configuration queue job exiting 2. No `ci-editor/journey/` member exists in the artifact, so there is no recorded original/candidate journey, no app screenshot pair, and no comparison result. PNG fixtures inside the uploaded verifier source are historical test fixtures, not device captures from this run. The original [workflow source](reviewed-source/editor-journey.yml) and [helper source](reviewed-source/configure_capture_device.py) are copied from the exact commit for review; the read-only analysis invokes only the parser, never the helper's Android command entry point.

The exact artifact remains in the previously published [evidence.zip](../evidence.zip): 659,380 bytes, SHA256 `888eec110a622313bfc1a0fa4eb183b14d6b7302f38d4b0bf5c063a8844d37a9`, artifact ID `11731511399`. All 149 ZIP members were checked against the GitHub-bound manifest and local extracted bytes before and after analysis. The complete actual device configuration, command streams, runtime status/properties, service/lifecycle logs and host logs have unchanged review copies under [raw](raw/). The [complete member inventory](all-149-member-identities.json), [extraction receipt](extraction-receipt.json), [derived result](independent-editor-analysis.json), source pins, analyzer and freezer preserve the exact bindings.

The actual host logs passed all 148 verifier controls and six downloader controls. Those host outcomes were checked as recorded; they do not establish any Android journey result. No additional Android retry was performed by this analysis, and no active guard or source was changed. The separately authorized twelve-screen workflow starts from its own fresh complete device configuration and must satisfy its unchanged checks independently.
