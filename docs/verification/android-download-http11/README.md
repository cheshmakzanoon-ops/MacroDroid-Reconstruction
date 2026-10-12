# Pinned Android download transport correction

The editor run [38201362423](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38201362423) stopped during emulator download with curl exit 92 (`HTTP/2 INTERNAL_ERROR`). Its 31 host tests passed, but it never executed the Android journey. That failed run remains separately archived.

This single-line change asks curl to use HTTP/1.1 for the official pinned downloads. It retains every URL, exact archive size, checksum, retry count, 600-second transfer bound, 625-second process bound and extraction/installation guard. Existing verified installations are reused as before.

The local curl command advertises `--http1.1` and the edited Python source parses. No fresh network download or Android run was performed by this preparation check; a subsequent hosted run must establish whether acquisition succeeds. This change supplies no application parity evidence.
