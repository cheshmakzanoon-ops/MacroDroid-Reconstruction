# Explicit nulls in the combined UI report

Run 38248170022 at 97322c18273818b0241fa1fa962da9d4a445afd1 built both APKs
and returned zero for all sixteen application acceptance gates. The independent
finalizer then rejected the UI observer controls. The original job remains a
failure and its original reports are unchanged.

The UI report and the standalone control call the same observer producer. The
UI writer's Gson configuration omitted null-valued object members, even though
the shared observer had already built a JSON tree containing those members.
The standalone writer explicitly serialized nulls. The sole differing fields
are the null returnIndex on the positive record and rejected records 0, 1, 2,
and 4. Rejected record 3 has the non-null integer 0 and agrees. The other four
parts of the finalizer's conjunction match exactly, as do all remaining fields
of the observer controls. The five-value diagnosis is retained in this capsule.

This successor changes one line in tests/java/UiParityTests.java. Its final
Files.writeString call now uses G.newBuilder().serializeNulls().create() to
serialize the report. The shared G instance used during comparisons, all case
and observer implementations, and the strict finalizer equality stay unchanged.
The two previously reviewed recorder successor source files are copied exactly.
The complete overlay remains twenty-one paths. The complete logical future
inventory retains 81,304 entries and changes only this test harness source row.
This derivation is not a substitute for the next physical source verification.

## Executed boundary regression

Six bounded commands are retained with exact argv, environment, start/finish
clocks, exit codes and raw streams: source preparation; Java and javac version
observations; compilation; original writer; corrected writer. Both Java runs use
-Xverify:all. The boundary harness mechanically includes the actual unchanged
G initializer and the exact old and corrected final write statements. It calls
the already compiled, archived DayLookupParityCases.observerControls on the
exact 371-entry pinned input inventory. Its generated controls are first compared
strictly with the closed standalone record from the failed run.

The original writer exits 2, reproduces exactly the five missing fields, and
matches the original closed UI observer object. The corrected writer exits 0
and retains strict equality for the whole JSON tree, including nested nulls,
null array entries, empty containers, empty strings, zero, false, escaped text,
and all six observer records. The five generated mutations are rejected by the
unchanged compiled observer. All 53 copied source/control inputs and the Java,
javac, Python and pinned Gson-containing JAR remain unchanged. The original
writer's failed result is preserved as a failure.

These are host report serialization controls. They execute no recovered app
method, complete UI parity harness, APK build, Android process, alarm or macro.
They add no application case or recovered-body credit. A fresh full hosted run
with unchanged strict finalization is still required before source promotion.
The 40 exact runtime classes and all boundary outputs are retained here; the
large existing dependency JAR is identified by hash and is not duplicated.
