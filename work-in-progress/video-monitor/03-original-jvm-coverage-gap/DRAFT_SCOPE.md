# Video monitor draft: compiled, not yet differentially verified

This isolated, unregistered source overlay translates
`Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;`.
The frozen original inventory has 262 instructions and 46 conditional IF edges.
The active combined project retains its unchanged 1,242 registered bodies.

The first draft preserves the initial 5,000ms delay, recurring 3,000ms delay,
all four coroutine labels and invalid-label guard, the two saved-state dead
casts, Unit and suspension identity, repeated owner/file reads, strict storage
thresholds, file-size sentinel behavior, stall-counter arithmetic, callback
capture, and nested Exception-only handling. The outer error logger and repeat
delay remain outside the main catch. These are translation decisions grounded
in the retained original body; execution equivalence remains to be measured.

The host facades expose only controlled file parent/existence/length, external
directory, available space, logging, result checking, delay and stop-dispatch
boundaries. Their new files are test support and are excluded from APK injection.
The LifecycleService facade supplies only compile-time hierarchy; no Android
service or host filesystem operation is performed. Shared support files retain
their previous inactive behavior, with VideoControl hooks for this study. The
proposed method entry is a standalone file, not an active registry edit.

`reports/draft-compile-02/result.json` records the actual successful javac command:
841 Java inputs, 23 overlay Java files, 881 generated class files, and 6.372192
seconds with a 180-second bound. Every source was copied into a fresh private
directory and hash-checked before compilation; original and copied bytes were
checked again afterward. The complete input inventory and compiled-class archive
are retained. No mutable hardlinks were used.

The untouched baseline UiParityTests file was copied for forthcoming narrow
harness integration and has not participated in this javac-only command.
Original/JVM differential cases, measured visited coverage, deliberate compiled
faults, rebuilt DEX proof and Android execution are all pending at this freeze.
The source remains a draft until those relevant gates pass. No full application
parity claim is made.
