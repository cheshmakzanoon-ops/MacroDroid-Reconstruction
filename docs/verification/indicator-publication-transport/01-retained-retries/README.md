# Exact-byte publication retries

Two blob calls stopped the inactive indicator publication before a ref update. The first call did not satisfy the strict expected Git blob SHA check. Its response body was not retained, so this record does not classify it as a wrong returned digest rather than an error or missing digest. An identical-byte retry returned the exact expected SHA; that response is preserved.

The later call's retained response explicitly reports an MCP internal error. The unchanged pending bytes were retried through the same strict SHA check. Both final payloads were independently read from the fetched commit and checked for complete byte size, SHA-256 and Git blob SHA-1. The complete 3,484-path fetched verification is retained here. No active source, APK, workflow or application outcome changed in these transport steps.

The only uploader edit added diagnostic response retention immediately before its unchanged strict acceptance check. The original and successor implementations and their exact diff are preserved. The root cause of the first missing response and of the connector internal error is not established here.
