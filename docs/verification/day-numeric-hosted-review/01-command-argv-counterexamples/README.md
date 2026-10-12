# Numeric subprocess argument verifier counterexamples

This is an inactive, direct synthetic review of `verify_numeric_commands` in the
unchanged job verifier with SHA-256
`c0ba5c0df54530eb94a293b4dae9b548e2679dd0251e77c14b3d06e7aa65708a`.
It does not report a complete verifier pass or a completed numeric build.

The old guard checks the 17 command labels, expected return codes, bounded
timestamps and 34 distinct raw stream roles. Its argument check requires only a
nonempty list. Four substitutions were therefore accepted: `/bin/true` in place
of a D8 command, an omitted JVM flag, different config/result arguments, and a
boolean argument element. The fixtures are explicitly synthetic; no described
Java, D8 or Android command was executed.

Three negative controls were correctly rejected: an empty argument list, a
boolean return code, and a reused stream role. The original nominal envelope and
its byte-exact restoration both passed this direct guard, with 34 distinct
stream inodes. All five copied reviewed source files remained unchanged.

The build agent independently found the same gap and is correcting the proposed
job verifier to reconstruct all 17 exact argument lists from fixed source/input
roles, the observed Java executable and the pinned JVM policy. That correction
will be preserved separately. This capsule changes no active application, APK,
workflow or existing proof.
