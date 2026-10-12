import json, re
from pathlib import Path
rows = []
for name, expected in [('download-tests.log', 6), ('wrapper-tests.log', 42)]:
    raw = (Path('ci-day-numeric-art') / name).read_text()
    summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', raw, re.M)
    if len(summaries) != 1 or int(summaries[0][0]) != expected or not raw.rstrip().endswith('OK'):
        raise SystemExit('The exact full host control inventory did not pass: ' + name)
    rows.append({'log': name, 'tests': expected, 'seconds': summaries[0][1]})
Path('ci-day-numeric-art/host-control-summary.json').write_text(json.dumps(rows, indent=2) + '\n')
