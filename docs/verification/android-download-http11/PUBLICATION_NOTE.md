# Publication of the prepared HTTP/1.1 correction

The files named by `checkpoint.json` are the exact closed, prepared correction supplied before publication. Its only executable change was adding `--http1.1`; its checks and limitations remain recorded in `verification.json` and the frozen README.

Before this capsule was published, concurrent commit [cada56c8a11ff5cbd892ec6d0beaeab60b3e644d](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/commit/cada56c8a11ff5cbd892ec6d0beaeab60b3e644d) updated the active downloader with HTTP/1.1, HTTPS-only redirects, bounded transport retries, and validation before archive promotion. It also added offline transport regressions and editor workflow diagnostics. The publisher read its complete three-file diff and retained all three files byte-for-byte.

The prepared single-line version in this directory is historical evidence; it was not applied over the concurrent active implementation. The active application source, input snapshot and APK manifest are unchanged by publication of this capsule. This evidence publication does not establish hosted download success or Android parity.

Preserved active downloader SHA-256: `8ae2a365cc5ec5109c76967642d6ee7f6655df96287cf8feb3355444e14e4e36`.
Prepared minimal downloader SHA-256: `8d0d8ece84479b75dc2efa03fd174aa340611747fa6381ebe2fb05291d9d314f`.
