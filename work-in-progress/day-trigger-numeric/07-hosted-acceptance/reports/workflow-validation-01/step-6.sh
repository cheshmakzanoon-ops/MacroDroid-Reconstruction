python3 -B job-source/tools/day_numeric_acceptance/prepare.py \
  --baseline-repository baseline-repository \
  --overlay-repository overlay-repository \
  --destination numeric-workspace \
  --output hosted-proof \
  --expected-job-commit "$GITHUB_SHA" \
  --runtime-manifest-sha256 "$DAY_NUMERIC_RUNTIME_MANIFEST_SHA256"
