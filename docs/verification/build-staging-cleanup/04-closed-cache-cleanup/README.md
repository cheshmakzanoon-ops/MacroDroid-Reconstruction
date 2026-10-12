# Closed f83 build cache cleanup

The completed private f83 acceptance build cache was removed only after its complete proof was published and fetched back successfully at [`e1ee954d9bd57b716a3987d92a38fa79d571a280`](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/commit/e1ee954d9bd57b716a3987d92a38fa79d571a280). The preserved full acceptance is in [the preceding evidence capsule](../03-full-acceptance/README.md). This cleanup does not change that result or establish another acceptance run.

[receipt.json](receipt.json) records the actual operation, performed from 03:55:12.539177 to 03:56:40.416607 UTC on 2026-10-12. Its only deletion target was `/tmp/macrodroid-acceptance-f83e1b-0_znx0sx/MacroDroid_v9/build`. A process check found no active process referring to the closed private checkout before deletion. The cache contained 410,650 regular files, 14,645 directories, no symlinks, and 4,858,539,401 logical file bytes. Strict removal completed and the target was absent afterward.

The cleanup program then verified the preserved material:

- All 81,212 configured source, test, tool, and reference inputs still match the frozen manifest. Their independently recomputed snapshot remains `f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85`.
- All 219 final report files retain their exact hashes.
- Both baseline and hybrid APKs in `dist/` retain their exact hashes.
- All root Markdown files retain their exact hashes.
- No other path was deleted by the program.

The receipt includes the full pre-removal report/APK/Markdown hash inventory. [cleanup_closed_f83_cache.py](cleanup_closed_f83_cache.py) is the exact program that ran; it validates the published proof bindings, requires the closed acceptance to have passed, limits deletion to the fixed `build/` path, and rechecks preserved inputs and evidence afterward.

Filesystem-wide free space was 4,666,228,736 bytes before and 7,721,500,672 bytes after the operation. These are observations of a shared filesystem, so concurrent unrelated work can affect the difference. They are not a measurement of physical bytes reclaimed from this cache alone.

The final recorded status is `CLOSED_GENERATED_CACHE_REMOVED_INPUTS_AND_EVIDENCE_PRESERVED`. Source, reports, and `dist/` remain available. This follow-up is separate from the immutable full-acceptance capsule and leaves its preceding failed attempts intact.
