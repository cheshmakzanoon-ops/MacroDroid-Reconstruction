# Point-in-time AVD reappearance

The original closed disposable AVD removal succeeded at its recorded observation. A later read-only inventory at **2026-10-12 06:01:01.373677 UTC** found the same path present again, with all **23 regular files matching the previously retired sizes and SHA-256 hashes**. It occupied 921,440,256 allocated bytes at this later observation; free space was 250,372,096 bytes. Sparse allocation can differ even when file content matches.

`reappearance.json` preserves all thirty directory/file entries, the original inventory hash, the exact path and sibling-name observation, and physical `/proc/self` PID 94272 separately from namespace PID 5. This probe did not delete or write the AVD. It shows that the earlier absence was not persistent; it does not alter the earlier successful point-in-time receipt or infer an unobserved exact restoration time.

The original removal and its explicit process-visibility correction are retained in the parent evidence directory and were published in commit `dfa130a90a271ad591dcdb86ec34ac4b6de8ddfb`. The authorized subsequent payload-only retirement is recorded separately under `../payload-retirement/`. No installation binaries, APKs, source, or capture evidence is contained in or changed by this follow-up.
