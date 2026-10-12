# Correction after the measured first attempt

The complete first attempt remains frozen in checkpoint 01. Its arbitrary fourteen-step plan passed the old policy because only three prefix steps and the total length were checked. The corrected guard binds every step of the already reviewed historical fourteen-step plan to its canonical SHA256; adding a screen to the new thirteen-step plan now rejects. The historical positive remains supported with its exact identity.

The other error came from a test assuming the existing reference context could be entered while already inside the new context. The reference context correctly rejects a changed base plan. The corrected test asserts that rejection, confirms the current plan is preserved and checks the twelve-screen router under a temporary explicit plan. No existing reference-context implementation changes.
