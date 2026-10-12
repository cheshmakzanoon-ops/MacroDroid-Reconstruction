# Corrected normal-animation diagnostic workflow

The materialized-input check and final verifier now independently reconstruct
the entire ordered input inventory from literal file pins, pinned checkpoint
inventories and the workflow's literal helper digests. Both reject omitted,
empty, duplicate, reordered, extra or rehashed report rows. The shared guard is
the reviewed Trigger05 physical-identity and chronology correction. Historical
Normal02 and its demonstrated mutable-row omission remain separate and intact.

This closed offline validation preserves every command and all input/fault
data. Each unique payload is archived once with a complete per-path mapping;
exact already-published APK/tool payloads are referenced by their verified SHA256
instead of duplicating them for every fault. Deliberate symlinks remain inert
metadata. This representation preserves every regular byte and original role.

This package is inactive until the reviewed workflow is published. The proposed
Android diagnostic fixes the same original and 9108 candidate APKs, requires
animation scale one before and after both runs, and compares ten full PNG/XML
observations using the unchanged zero-pixel rule. Offline controls are not
Android execution, and no whole-application, animation-timing or crash-free
lifecycle parity is claimed. The existing scale-zero 26-pixel failure remains.
