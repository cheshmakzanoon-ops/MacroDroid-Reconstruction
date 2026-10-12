# Combined source: all sixteen acceptance gates passed

The exact combined plugin-upload and Widget candidate passed the complete
configured host acceptance suite, including signed baseline/hybrid assembly,
complete code and resource comparisons, all deliberate-fault families, the
signed source-edit experiment and final complete positive restoration.

The three-path comparison ran 193,489 cases across all 1,242 registered Java
method bodies in 605 classes, with zero mismatches or unsupported executions.
The UI group ran 23,174 cases over ten methods with 15,326 independent expected
checks. All 78 actual UI faults were detected and the full positive baseline
was restored exactly. All 273 Python tests passed. Sixteen gate logs, all 22
fresh report hashes, and 78 retained mutant source/class pairs were independently
rechecked after acceptance. Every closed report, including nested mutation
artifacts and the full input manifest, is preserved in the verified archive.

All 81,291 pinned source/tool/test inputs were independently rehashed before and
after acceptance and freezing. The source pin is
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`.
The 94,683,119-byte signed candidate SHA256 is
`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`;
its exact bytes are retained in twelve ordered, independently verified parts.
The baseline remains `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.

This is a completed local host/artifact measurement for the new combined input
pin. It is separate from previous isolated candidates and hosted/device runs.
It does not itself activate source or APKs, execute Android features, resolve
the observed old-candidate 26-pixel difference, or establish whole-app parity.
Most application logic remains editable smali and native/opaque dependencies
remain original binaries. The publisher's signing identity is unavailable.
