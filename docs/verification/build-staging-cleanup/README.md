# Java staging cleanup and repeated compilation

The acceptance attempt in `acceptance-before-fix/` passed its input-integrity
check and fresh baseline APK build, then failed in `compile_java()` while
creating an already existing `build/java/dex` directory. It did not execute the
remaining acceptance commands. Its original JSON result and three command logs
are retained here.

The previous cleanup used `shutil.rmtree(..., ignore_errors=True)`. The correction
checks whether the generated Java directory exists and removes it without
suppressing cleanup errors before creating fresh compiler output directories.
An unsuccessful cleanup now stops the build at that operation. The underlying
reason a directory persisted under the prior ignored-error cleanup was not
established; the evidence does not assign it to a specific filesystem mechanism.

`java-staging-repeat-build.json` records the failed pre-fix repeat. An intermediate
diagnostic with non-ignoring cleanup completed two removals; its raw observations
are in `java-staging-cleanup-diagnostic.json`. After the source correction,
[`tools/diagnostics/check_java_staging.py`](../../../tools/diagnostics/check_java_staging.py)
performed two actual consecutive Java compilations. Both passed and produced the
same helper DEX SHA-256, as recorded in `java-staging-repeat-fixed.json`.

This is a build-staging check. It does not establish application behavior or
replace the full configured acceptance suite.
