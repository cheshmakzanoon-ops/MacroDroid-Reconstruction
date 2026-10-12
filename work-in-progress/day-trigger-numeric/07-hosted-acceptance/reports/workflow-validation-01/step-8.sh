python3 -B job-source/tools/day_numeric_acceptance/verify.py \
  --baseline-repository baseline-repository \
  --overlay-repository overlay-repository \
  --output hosted-proof \
  --runtime-manifest-sha256 "$DAY_NUMERIC_RUNTIME_MANIFEST_SHA256"
