# Lookup integration: exact class registry and bounded proof scopes

This addendum corrects the plan's shorthand “exact two-body target set.” The actual numeric19 registry already contains the constant recovery `requiresScheduleExactAlarm()Z`, besides the numeric `r0` mapping. Appending `p0` leaves **three registered methods in the DayTrigger class**:

| Method | Helper | Role in this overlay |
| --- | --- | --- |
| `requiresScheduleExactAlarm()Z` | `source/java/recovered/constants/DayTrigger_74d1108d.java` | Existing mapping retained exactly. |
| `r0(DictionaryEntry)I` | `source/java/recovered/ui/DayTriggerValueMethods.java` | Numeric19 mapping and executable helper retained exactly. |
| `p0(Dictionary,String)DictionaryEntry` | `source/java/recovered/ui/DayTriggerLookupMethods.java` | New lookup mapping. |

The freshly extracted fixture preserves the complete prior 1,246-method selection byte for byte when that subset is rebuilt. Its only additions are the original `p0` body and the two original field-getter dependencies. This does not remove or reclassify the existing constant mapping.

The one-method micro-D8 compiler replaces only `p0` in the preserved original DayTrigger smali. It checks every other method and non-target class byte against that original input, so its count of 33 unchanged other methods is scoped **only to that micro-DEX**. Those include the original `r0` body. The micro-DEX does not model the complete signed class's three registered replacements.

The new acceptance entry separately checks the full emitted `p0` instruction listing against the freshly signed APK, verifies the exact three-entry class registry, binds both getters to the same signed APK member, and retains the signed numeric method's listing before and after lookup controls. Existing complete-class/static/linkage/APK verification remains required. No claim that all 33 other methods in the combined signed class are original is made.

The private integration study uses the existing signed APK only as an exact source of unchanged getter bytes. Its old `p0` instruction listing is separately compared with the new micro-D8 body. A mismatch is retained as evidence that this old APK cannot satisfy the future signed-primary gate. The private study cannot promote a candidate or substitute for that gate.

The starting numeric checkpoint remains `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f`. The independently authored numeric command-evidence successor has not been merged. Its future integration must preserve both the new timing/filesystem witness correction and this overlay's exact combined dependency declarations under explicit before-hash checks.
