set -euo pipefail
python3 -B -m unittest discover -s tools/android -p 'test_download_retry.py' -v 2>&1 | tee ci-exact-alarm-enable-return/download-tests.log
python3 -B -m unittest discover -s ci-exact-alarm-enable-return/reviewed-source/tools/parity_journeys -p 'test_*.py' -v 2>&1 | tee ci-exact-alarm-enable-return/journey-host-tests.log
python3 -B -m unittest discover -s work-in-progress/trigger-category/07-zero-animation-source -p 'test_enable_still_animations.py' -v 2>&1 | tee ci-exact-alarm-enable-return/animation-host-tests.log
