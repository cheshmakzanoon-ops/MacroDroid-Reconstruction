# No eligible hybrid-smali cache files

The exhaustive read-only assessment retained all 71,267 cache entries. Of these,
70,662 share their physical inode with canonical source and have multiple links;
the other 605 are registered recovered classes. Zero files are eligible for
retirement under the conservative exact-duplicate policy. No cache or source
payload was changed. All canonical/cache identities and 1,469 protected file
identities were checked before and after; result.json carries the actual count.
Unavailable process checks remain unavailable, never passing checks.

The original checkpoint.json is preserved byte-for-byte. Its 97,324,105-byte
retained-classes.json is represented without data loss by retained-classes.json.gz.
publication-layout.json binds the original length, SHA-256 and mode to the exact
compressed container. Decompression was independently streamed and verified.
Use materialize_retained_classes.py with an explicit output file to reconstruct
that original checkpoint member; all other declared members are stored normally.

The unusually large expanded retained list contributed to a full workspace.
This fact does not authorize retirement of any cache or authoritative evidence.
The accompanying publisher transport receipt is a separate operation on exact,
already-published JSON duplicates and reported no observed free-space increase.
