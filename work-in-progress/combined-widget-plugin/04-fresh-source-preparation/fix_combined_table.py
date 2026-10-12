#!/usr/bin/env python3
"""Keep the two new method mappings in the existing Markdown comparison table."""
import argparse
import json
from pathlib import Path
from prepare_merge_overlay import identity, replace_once, write_json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--preparation", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
root = Path(json.loads(args.preparation.read_text())["private_project"])
path = root / "UI_RECOVERY.md"
before = identity(path)
text = path.read_text()
path.write_text(replace_once(text, "\n\n| `plugins.k.invokeSuspend(Object)`", "\n| `plugins.k.invokeSuspend(Object)`", "contiguous method table"))
write_json(args.output, {"status": "METHOD_TABLE_FORMATTING_CORRECTED", "path": str(path), "before": before,
                         "after": identity(path), "application_inputs_changed": False})
