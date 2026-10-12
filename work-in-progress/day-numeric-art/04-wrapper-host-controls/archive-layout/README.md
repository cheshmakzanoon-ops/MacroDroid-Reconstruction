# Exact numeric ART 41-control archive layout

The historical checkpoint 14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb and its 25 non-archive payloads are preserved unchanged. Its 16,898,593-byte evidence.tar.gz is represented by three exact binary parts; it was neither recompressed nor edited.

The complete SHA-256 is 56e15009933932b5f197d4f985f4cd7677116b74bf5b3484a36fcbb4088ee47f. The manifest binds canonical part paths, byte counts, SHA-256 values and Git blob identities. The original evidence-inventory.json binds all 7,629 members and their 96,481,154 total expanded bytes, which were individually rechecked here.

Before validating the complete original capsule, run the existing scripts/assemble_artifact.py with work-in-progress/day-numeric-art/04-wrapper-host-controls/archive-layout/manifest.json and --output work-in-progress/day-numeric-art/04-wrapper-host-controls/evidence.tar.gz, then set the output mode to 0644. Recheck the complete digest, all 26 original file identities and every archived member. The published parts resolve the logical archive; an absent assembled archive alone is not a complete materialized capsule.

The fetched assembler was invoked with --verify-only against the three exact parts and created no assembled duplicate. Its exact source/stdout/stderr are retained. This transport check adds no Android or application credit. The old 41-control result stays historical: the subsequently observed schema-2.0 acceptance and its separate literal-type correction are not rewritten into it.
