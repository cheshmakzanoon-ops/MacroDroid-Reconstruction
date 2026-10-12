# Incomplete fixed indicator runtime draft — inactive checkpoint

This checkpoint preserves authored work before its first host validation. It is not runnable acceptance tooling, is not an activated workflow, and reports no Android execution, measured pixel result, parity credit, or source-method recovery. The independent prefix/experiment verifier, complete CLI integration, host controls, runtime file manifest, and workflow are still being completed. Calls to not-yet-implemented functions in this draft are pending work, not executed successes.

The frozen design is `fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec`, published at commit `39250fac022aee5551f36782bafd72cabbc33718`, under `work-in-progress/indicator-fixed-sampling/01-bounded-design`. All sixteen parent declarations remain pinned to `6331410cfd2391389270564803623079e8355ad8`.

Root approved three explicit implementation deltas: (1) exact AAPT2 6,135,688 bytes / `6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745` as a read-only, 60-second `dump badging` dependency; (2) eight separately queued fixed-index slots bounded at 900 seconds apiece, in separate owned directories, preserving the unchanged parent's 3,600-second queue limit and one global 7,200-second deadline, aborting the remaining schedule after a failure; and (3) lossless streamed gzip records containing a four-byte row-major pixel index and two four-byte RGBA tuples, with dimensions/count/hashes and an independent decode/recount. No frame choice, settling, masks, tolerance or additional comparison credit is introduced.

All 40 planned post-input observations and 92 predetermined comparisons remain required. The two APK identities, condition A then B, O/C/C/O order, single observed NEXT selector, 2-second post-input wait and 1-second completion-to-next-start gap are unchanged. The initial draft is retained separately under `evidence/draft-00-before-slot-isolation`.

This checkpoint is immutable. Further implementation and its actual failed/passed checks will be frozen as a separate successor. No application source, APK, existing recorder or existing comparison policy has been edited.
