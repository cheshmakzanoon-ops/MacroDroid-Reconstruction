# Reconstruction history

- **v2:** Editable Dalvik instruction listings and a limited executable-bytecode patch workflow. No high-level source build.
- **v3:** All nine DEX partitions assembled from smali; manifest/resources recompiled with stable IDs.
- **v4:** Hybrid Java/smali compilation introduced; 74 Java-migrated method bodies.
- **v5:** 1,195 Java-migrated bodies; split-array logic and many constant-return/no-op methods.
- **v6:** 1,205 methods; macro-invocation eligibility, weather and constraint logic.
- **v7:** 1,220 methods; system settings, Wi-Fi/hotspot, parsing, solar logic.
- **v8:** 1,232 methods; action dispatcher, navigation, flow-control helpers.
- **v9 (latest):** 1,237 methods; drag handling, sound recognition, SMS validation, scene-state serialization. Reports show 179,248 bounded three-way host comparison cases, and no observed Android execution.

Earlier reports are retained under `docs/history/` for traceability, not as proof of later acceptance. The complete application sources and APKs have not been uploaded to this public repository.
