#!/usr/bin/env python3
"""Combine authored lookup cases with exact previously reviewed provenance utilities."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parent = ROOT / 'parent-study-source.java.txt'
    if sha(parent) != '4542b75d3ca2e5e8299fcdf218f90807e46af312531f2cdafd976b4c265a7442':
        raise ValueError('The pinned original provenance/coverage utility source changed')
    text = parent.read_text()
    utilities = text[text.index('    static String sha('):text.index('    static Observed observe(')]
    coverage = text[text.index('    static JsonObject coverage('):text.index('    public static void main(')]
    source = ROOT / 'inputs/DayLookupStudy.java.in'
    target = ROOT / 'inputs/DayLookupStudy.java'
    if target.exists():
        raise ValueError('Composed study already exists')
    composed = source.read_text()
    for marker, replacement in [('    // PINNED_SHARED_PROVENANCE_UTILITIES', utilities),
                                ('    // PINNED_SHARED_COVERAGE_UTILITY', coverage)]:
        if composed.count(marker) != 1:
            raise ValueError('Study composition marker changed')
        composed = composed.replace(marker, replacement)
    if '// LOOKUP_STUDY_MAIN' in composed:
        raise ValueError('Authored study entry point is not complete')
    target.write_text(composed)
    report = {'parent_utility_source_sha256': sha(parent), 'authored_template_sha256': sha(source),
              'composed_source_sha256': sha(target), 'android_executed': False,
              'provenance_utility_sha256': hashlib.sha256(utilities.encode()).hexdigest(),
              'coverage_utility_sha256': hashlib.sha256(coverage.encode()).hexdigest()}
    (ROOT / 'composition.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
