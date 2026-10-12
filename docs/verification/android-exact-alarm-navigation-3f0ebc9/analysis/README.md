# Exact-alarm Settings: completed fourteen-screen observation

Run **38240023189**, artifact **11742624179**, executed the workflow at `3f0ebc910be72beeb9d7f2443928df2df2258c7d`. Both APKs completed **14 screens and 13 inputs**. The recorded outcome is **EXACT_ALARM_NAVIGATION_FOURTEEN_SCREEN_DIFFERENCE** with valid evidence and `journey_equal: false`.

The independent replay reproduced the entire captured comparison and the entire workflow verdict, excluding only the replay's new verification timestamp. It reconstructed all **295** prepared input roles, checked all **3,507 raw files** against the single original ZIP, and verified every raw byte and both compared APKs unchanged afterwards. Its own command completed with exit code zero in **204.243 seconds**. The replay issued no Android action. Successful replay verifies the recorded difference; the device result remains a difference.

## Full-frame and hierarchy result

The full RGBA changed-pixel vector is `[0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`. All fourteen paired hierarchies are byte-identical and thirteen paired PNGs are byte-identical. The **35** differing pixels occur on `intro-2` inside exclusive bounds `[313, 1184, 352, 1200]` at the page indicator. Every changed coordinate and both colors are retained. No region was masked and no pixel tolerance was used. This run does not establish the cause of the indicator variation.

The replay checked **54 accepted snapshot ledgers**, **54 capture ledgers**, **108 recorded frame observations**, **2940 unique referenced artifacts**, and all **1,091 commands**. The global command check binds all **2,182 streams**, **26 planned inputs** and **six install/launch setup mutations**, with zero unbound mutations. All **209 journey**, **10 animation**, and **6 downloader** host tests have individual successful raw log entries. The nineteen zero-scale commands and owned runtime cleanup also verify.

## Exact-alarm navigation and observed Settings controls

Both APKs reached `com.android.settings/com.android.settings.spa.SpaActivity` through the previously observed **OK** button. The paired terminal PNGs are exactly 88,338 bytes with SHA-256 `ac9f9f81790687fece02cbba46be83b574b31a8f3bb3f155e940a5245aac1b9c`; the XMLs are exactly 6,919 bytes with SHA-256 `44247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e`. The root viewed the full original PNG and read both hierarchies.

The page identifies **MacroDroid 5.67.8**. Its **Allow setting alarms and reminders** row is enabled, clickable and checkable, with `checked=false`. The actual clickable ancestor bounds are `[0,688][720,855]`, giving center `(360,771)`. The visible **Navigate up** control has clickable ancestor bounds `[8,56][104,152]`, giving center `(56,104)`. Full node and ancestor attributes are retained in `observed-settings-controls.json`.

This run contains **zero Settings inputs**, no permission grant, no confirmed trigger configuration, and no saved or executed macro. A separate extension can bind these observed controls, enable the switch, verify the resulting checked state and then use Navigate up to observe the returned app surface. Those next actions have not been performed by this run or replay.

## Process observations and limits

Both notification readiness phases contain four `HOME_WITH_SAME_PID` observations and accept the first eligible sequence `[0,3]`. Both runs also record the known Fragment LB `java.lang.IllegalStateException`, followed by continuation in a replacement process. Complete raw crash and readiness evidence remains in the comparison and artifact. This is not a crash-free run, and the notification action is not established as the cause of that exception.

Full runtime 1:1 and animation timing parity remain unestablished. This evidence applies to the fourteen declared still screens and thirteen inputs with the two fixed APK identities. Historical failures and comparisons retain their original outcomes.

## Preserved files

The capsule includes every closed replay output, the exact replay source, the exact bounded command wrapper, complete command stdout/stderr and timing, full paired captures, source identities, complete verdicts and inventories. `external-evidence.json` binds the unchanged original ZIP and its complete extraction. Only the already identified ephemeral public ADB value is omitted from a clearly marked review copy of the boot log; original raw bytes remain unchanged.
