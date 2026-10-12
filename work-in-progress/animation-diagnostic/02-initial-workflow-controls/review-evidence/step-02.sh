set -euo pipefail
python3 -B -m unittest discover -s tools/android -p 'test_download_retry.py' -v 2>&1 | tee ci-normal-animation/download-tests.log
python3 -B -m unittest discover -s ci-normal-animation/reviewed-source/tools/parity_journeys -p 'test_*.py' -v 2>&1 | tee ci-normal-animation/journey-host-tests.log
python3 -B -m unittest discover -s work-in-progress/animation-diagnostic/01-normal-animation-source -p 'test_enable_normal_animations.py' -v 2>&1 | tee ci-normal-animation/animation-host-tests.log
