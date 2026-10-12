"""Prepare the 24 frozen Widget faults with exact occurrence and source guards."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

CATALOG_PATH = "tests/fixtures/widget-method-mutants.json"
CATALOG_SHA256 = "01f3b482ff62378d78d295eaf96e96cf54de7c165e7edbc2f2f4b8f0bd0b6159"
HELPER_PATH = "source/java/recovered/ui/WidgetUpdateMethods.java"
HELPER_SHA256 = "dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79"
METHOD = "Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;"


def apply_edits(source: str, edits: list[dict]) -> str:
    if not isinstance(edits, list) or not edits:
        raise RuntimeError("A Widget mutation needs explicit edits")
    result = source
    for edit in edits:
        if (not isinstance(edit, dict) or set(edit) != {"find", "replace", "count"}
                or type(edit["count"]) is not int or edit["count"] < 1
                or not isinstance(edit["find"], str) or not edit["find"]
                or not isinstance(edit["replace"], str) or edit["find"] == edit["replace"]):
            raise RuntimeError("Invalid Widget mutation edit")
        if result.count(edit["find"]) != edit["count"]:
            raise RuntimeError("Widget mutation occurrence count differs")
        result = result.replace(edit["find"], edit["replace"])
    if result == source:
        raise RuntimeError("Widget mutation did not change its source")
    return result


def load_widget_mutations(root: Path) -> list[dict]:
    data = (root / CATALOG_PATH).read_bytes()
    original = (root / HELPER_PATH).read_bytes()
    if hashlib.sha256(data).hexdigest() != CATALOG_SHA256:
        raise RuntimeError("Widget mutation catalog differs from its frozen bytes")
    if hashlib.sha256(original).hexdigest() != HELPER_SHA256:
        raise RuntimeError("Widget helper differs from the measured positive source")
    catalog = json.loads(data)
    if (catalog.get("method") != METHOD or catalog.get("helper_path") != HELPER_PATH
            or catalog.get("helper_sha256") != HELPER_SHA256):
        raise RuntimeError("Widget catalog identifies another target")
    controls = catalog.get("controls")
    if not isinstance(controls, list) or len(controls) != 24:
        raise RuntimeError("Exactly 24 Widget mutations are required")
    jobs = []
    names = set()
    for control in controls:
        if (not isinstance(control, dict)
                or set(control) != {"name", "reason", "edits", "expected_failure_labels"}
                or not isinstance(control["name"], str)
                or re.fullmatch(r"[a-z][A-Za-z0-9-]+", control["name"]) is None
                or control["name"] in names):
            raise RuntimeError("Invalid or duplicate Widget mutation name")
        names.add(control["name"])
        required = control["expected_failure_labels"]
        if (not isinstance(required, list) or not required or len(set(required)) != len(required)
                or any(not isinstance(label, str) or not label.startswith("widget-") for label in required)):
            raise RuntimeError("Widget mutation must name every required observed failure")
        jobs.append({"name": "widget-" + control["name"], "classname": "WidgetUpdateMethods",
                     "source": root / HELPER_PATH, "mutant": apply_edits(original.decode(), control["edits"]),
                     "required_cases": list(required), "catalog_sha256": CATALOG_SHA256,
                     "reason": control["reason"], "widget": True})
    return jobs


DAY_CATALOG_PATH = "tests/fixtures/day-numeric-mutants.json"
DAY_CATALOG_SHA256 = "1e008b16aa92c2e7c42aa88ecea9913391ee4f41b95ed73cd7a4ea17c914f4de"
DAY_HELPER_PATH = "source/java/recovered/ui/DayTriggerValueMethods.java"
DAY_HELPER_SHA256 = "b99984c0ca9128f9def8658d874f98d9a8e4529433d0f76f7f86e9e8299cc792"
DAY_METHOD = "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I"
DAY_INPUT_INVENTORY_SHA256 = "e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79"


def load_day_mutations(root: Path) -> list[dict]:
    """Load the thirteen measured numeric faults without changing Widget controls."""
    data, original = (root / DAY_CATALOG_PATH).read_bytes(), (root / DAY_HELPER_PATH).read_bytes()
    if hashlib.sha256(data).hexdigest() != DAY_CATALOG_SHA256:
        raise RuntimeError("Day numeric mutation catalog differs from its frozen bytes")
    if hashlib.sha256(original).hexdigest() != DAY_HELPER_SHA256:
        raise RuntimeError("Day numeric helper differs from its measured positive source")
    catalog = json.loads(data)
    if (catalog.get("schema") != 1 or type(catalog.get("schema")) is not int
            or catalog.get("method") != DAY_METHOD or catalog.get("helper_path") != DAY_HELPER_PATH
            or catalog.get("helper_sha256") != DAY_HELPER_SHA256
            or catalog.get("input_inventory_sha256") != DAY_INPUT_INVENTORY_SHA256):
        raise RuntimeError("Day numeric catalog identifies another method or case inventory")
    controls = catalog.get("controls")
    if not isinstance(controls, list) or len(controls) != 13:
        raise RuntimeError("Exactly thirteen Day numeric mutations are required")
    jobs, names = [], set()
    for control in controls:
        if (not isinstance(control, dict)
                or set(control) != {"name", "reason", "edits", "expected_failure_labels"}
                or not isinstance(control["name"], str)
                or re.fullmatch(r"[a-z][a-z0-9-]+", control["name"]) is None
                or control["name"] in names):
            raise RuntimeError("Invalid or duplicate Day numeric mutation name")
        names.add(control["name"])
        required = control["expected_failure_labels"]
        if (not isinstance(required, list) or not required or len(set(required)) != len(required)
                or any(not isinstance(label, str) or not label.startswith("day-numeric:") for label in required)):
            raise RuntimeError("Day numeric mutation must name its required observed failure")
        jobs.append({"name": "day-numeric-" + control["name"], "classname": "DayTriggerValueMethods",
                     "source": root / DAY_HELPER_PATH, "mutant": apply_edits(original.decode(), control["edits"]),
                     "required_cases": list(required), "catalog_sha256": DAY_CATALOG_SHA256,
                     "reason": control["reason"], "widget": False, "day_numeric": True})
    return jobs
