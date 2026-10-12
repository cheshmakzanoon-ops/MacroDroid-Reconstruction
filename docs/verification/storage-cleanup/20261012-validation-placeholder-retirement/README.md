# Closed validation payload retirement with exact provenance

The final operation retired only payloads in transfer-validation and overlay-bootstrap-validation after every original file matched the already committed source/toolchain archive inventory. Each of the 60,809 paths was atomically replaced by a zero-byte placeholder; names deliberately remain and these validation copies are no longer usable project materializations. Authoritative archives and active source are retained.

The first stricter attempt stopped before deletion because other processes cwd/fd views were denied. The next approved guarded deletion verified all payloads but stopped when paths reappeared. Both exact scripts, available process/retained-file records and reported failures are preserved. No permission or infrastructure setting was changed.

The approved final criterion used explicit closure confirmations from all four task owners and two readable physical-process comm/argv inventories while other agent writes were paused. Unavailable cwd/fd checks are recorded as unavailable, not passed. After replacement, all 60,809 files were zero-length with zero allocated file blocks, and all 909 selected original/source/evidence hashes remained unchanged.

The full before/after per-file metadata is compressed in placeholder-retirement/full-before-after.json.gz; its uncompressed size and SHA-256 are in the final receipt. It binds 913,364,812 original logical bytes and 1,056,043,008 allocated file bytes to the previously published exact archive inventory. Observed free space increased by 1,050,210,304 bytes to 1,297,334,272 bytes at the final check, with concurrent private acceptance work explicitly noted. No continuing absence or permanent free-space claim is made.
