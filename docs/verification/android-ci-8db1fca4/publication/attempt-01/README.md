# Publisher-only raw-freezer assertion failure

The first full freezer stopped at line 85 because it searched for the literal substring `Upload` in a successful job step name. The actual successful step 9 is named `Preserve measured runtime outcomes, including failures`. Its source and complete partial-output inventory are retained here. The full first invocation's stderr was displayed by the execution tool but was not saved as a raw file; no reconstructed full stderr is presented.

The separate, executed focused replay retains its own actual stdout, stderr and exit code and reproduces the same assertion failure against the unchanged job metadata. The successor binds the exact observed step name, number, completion and success. This is a publication metadata correction; no raw member, application code, acceptance rule or Android outcome changes.
