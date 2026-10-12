# Local combined acceptance stopped at hybrid staging

The local acceptance run for source checkpoint `95077fcb1d3c86f3b1c91026619642d99198f149`
verified its 81,211-file input pin and completed the baseline build command, then
failed the third configured command, `hybrid-build`. The remaining 13 configured
gates were not executed. This run does not establish combined host acceptance or
Android runtime behavior.

[The exact result](reports/acceptance-20261012T020321783797Z/result.json) records
canonical input digest
`8c8999f971f61def792cdf4ecd7999220c2fa2e56a5bdfecf3b04dee113bf7b0`.
The baseline log records reuse of verified source caches. The hybrid log records
`File exists` for `build/hybrid-smali`; it does not record a newly completed hybrid
APK. The previous frozen scene candidate remains separately identified by its
committed artifact manifest.

At this source checkpoint, `hybrid_source` attempted to remove its staging
directory with `shutil.rmtree(..., ignore_errors=True)` before creating it again.
The observed remaining directory requires a cleanup correction and a subsequent
measured build. The failure is preserved unchanged; it is not converted into a
pass by the proposed fix.

[manifest.json](manifest.json) pins all five exact files: the three command logs,
the result JSON and the console progress log. Each command log was checked against
its hash inside the original result. The fresh hosted run
[38194498356](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38194498356)
is independent and retains its own measured outcome. The earlier successful
1,238-body hosted acceptance remains in [source-ci-bebf448](../source-ci-bebf448/).
