# GitHub transfer status (October 11, 2026)

The named GitHub repository is **public**. The connected GitHub API can write text and Git objects, but the session's local git cannot reach github.com (DNS resolution fails), and the connector cannot directly ingest a local 225 MB ZIP or an 81,000-file tree.

**Pushed:** repository index, four exact Java recovered-source samples, release inventory/checksums, quality and delivery reports, importer, safeguards and provenance.

**Not pushed:** the complete v9 executable sources (71,267 smali class files; 1,237 Java-migrated methods among the project), Android assets, native libraries, original and rebuilt APKs, third-party build tool binaries, development signing keystore, unreviewed historic raw dumps. They remain in the conversation's v9 download artifacts, not GitHub. Any claim that the full source has been pushed would be inaccurate.

To assemble a local working project, download the two v9 archives from the conversation and follow the README importer instructions. Before making any code/assets public, ensure redistribution permission from their copyright holders. If authorized, an authenticated local Git client can publish selected sources using an appropriate license and .gitignore rules. Avoid huge single-file Git objects; use permitted releases/LFS for binaries.

**Static build equivalence is not whole-app equivalence:** host tests and canonical instruction comparisons are documented, but Android runtime tests were unavailable and have not established 1:1 feature behavior.

This status is about the present repo contents, not a claim that remote release attachments exist.
