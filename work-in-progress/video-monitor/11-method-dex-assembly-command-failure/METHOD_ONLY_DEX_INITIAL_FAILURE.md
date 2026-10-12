# Initial method-only DEX study: wrapper assembly command failed

`reports/method-only-three-path-11` is an actual closed failed run. Its free-space preflight observed 104,321,024 bytes, above the 96 MiB guard. The study verified the immutable 07 original/JVM checkpoint and 02 compiled host archive, copied the exact production relocation/transplant code and one original target class, and sent only the relocated recovered helper class to D8.

D8 succeeded in 3.149376 seconds, and the helper DEX disassembly succeeded in 0.822338 seconds. The next command returned 1 after 0.271326 seconds because this newly authored wrapper named `com.android.tools.smali.Main`. The tool JAR contains the production assembler entry point `com.android.tools.smali.smali.Main`, as used by the pinned production `build.py`. The exact stderr is retained:

```
Error: Could not find or load main class com.android.tools.smali.Main
Caused by: java.lang.ClassNotFoundException: com.android.tools.smali.Main
```

This is a wrapper command error. No assembled target DEX, three-path application execution, static accounting, or APK proof is claimed for this run. The raw original 259/262 coverage failures remain unchanged. The separately recorded javac preflight in `reports/dex-launcher-compile-11` did compile the new origin launcher and three-path study against the unchanged frozen harness, but that preflight executed no application method either.

The follow-up changes only the two assembler main-class strings in the private runner to the exact production entry point, then reruns in a new directory when the same storage guard permits it. Original Java, test cases, original fixture, interpreter, active registries, production pipeline files, and APKs remain unchanged. All files produced by this failed run, including its exact input snapshots, D8 class/DEX/smali outputs, proposed transplanted smali, logs, traceback and result, remain frozen separately.
