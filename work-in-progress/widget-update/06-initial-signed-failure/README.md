# Initial signed Widget study: metadata failure preserved

The actual hybrid assembly, complete bytecode round trip and resource comparison
passed. The host stage then ran all 259 Python tests and correctly failed exactly
three: the common method count still expected 1,240, the class count still expected
603, and the original-fixture provenance still named the preceding fixture hash.
The candidate actually contains 1,241 bodies in 604 classes and a freshly extracted
full original-method fixture. The implementation and D8/static/linkage prerequisites
retain their independently recorded results; no three-path host pass is claimed.

This checkpoint preserves every closed report, all four outer gate logs, the
initial omitted metadata/test inputs, the exact signed APK and each archive/part
hash. The APK is 94,683,439 bytes, SHA-256
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`.
The source pin is `a729f01fc4b0dc136c980501c144b43769332c324f8c6f63438107d605291691`.
The original extraction, 30 source/test changes and exact D8 prerequisites are
retained in the adjacent immutable `06-d8-prerequisites` checkpoint.

A numbered follow-up corrects only the two omitted metadata/test files, records a
new input pin and reruns the full signed study. This failed result is never changed
into a passing result. The method remains inactive in the published application.
