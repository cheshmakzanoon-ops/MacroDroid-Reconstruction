# Exact published JSON transport duplicates

This closed bounded operation verified 58 publisher-owned JSON staging files
against exact Git objects in fetched commit a58c9560d0658e29c63bedb97c748d41a107e421
and unchanged authoritative repository files, including modes. Each selected
staging file had one link and a distinct inode from its authoritative copy.
Only these verified transport duplicates were truncated to zero-byte placeholders.

All repository files, source/checkpoint originals, APKs, archives and Git history
were preserved. The full before inventory and executed verifier/operation code
are included. The observed allocated total was 10,743,808 bytes, but free space
was zero both before and after. No reclaimed-capacity or persistent-absence claim
is made. JSON text transport wrappers were excluded because their wrapper bytes
were not themselves proven to be a fetched Git object.
