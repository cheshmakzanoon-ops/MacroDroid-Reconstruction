#!/usr/bin/env python3
"""Derive a second bounded operation; retain every recovered-class cache file."""
from pathlib import Path
import difflib, hashlib, json

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'checkpoints/01-exact-source-duplicates/retire_verified_smali_duplicates.py'
BASE_SHA = 'be1e1863363fe67b5674ab4a4d58e4c6b5814309cc9f3d02b99b63a6fccbb17d'
TARGET = ROOT / 'retire_verified_hybrid_duplicates.py'

def replace_once(text, old, new):
    if text.count(old) != 1: raise RuntimeError('Derivation anchor is not unique: ' + repr(old[:100]))
    return text.replace(old, new, 1)

def main():
    if TARGET.exists(): raise RuntimeError('Derived operation already exists')
    original = BASE.read_text()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA: raise RuntimeError('Reviewed base operation changed')
    text = replace_once(original, "CACHE = PROJECT / 'build/verify-baseline'", "CACHE = PROJECT / 'build/verify-hybrid'")
    text = replace_once(text, "DURABLE_COMMIT = 'c9373851d4408fb4db63c21873ac2d0bb6867270'",
        "DURABLE_COMMIT = 'c9373851d4408fb4db63c21873ac2d0bb6867270'\n"
        "REGISTRY_SHA = '73a37f1ac4148c03a1dc0df9810e899ebb8ff7bcc6f1df7c1672fd525d66a20e'\n"
        "FROZEN_REGISTRY = Path('/workspace/scratch/4130730d15aa/combined-recovery/checkpoints/05-full-acceptance/project/source/java-method-map.json')")
    text = replace_once(text, "paths = [PROJECT / 'source/class-index.json', PROJECT / 'build.py']",
                        "paths = [PROJECT / 'source/class-index.json', PROJECT / 'source/java-method-map.json', PROJECT / 'build.py']")
    text = replace_once(text, '        protected = protected_files()\n        save(output / \'protected-before.json\', protected)',
        "        registry_path = PROJECT / 'source/java-method-map.json'\n"
        "        if identity(registry_path)['sha256'] != REGISTRY_SHA or identity(FROZEN_REGISTRY)['sha256'] != REGISTRY_SHA:\n"
        "            raise ValueError('Published recovered-method registry changed')\n"
        "        registry = json.loads(registry_path.read_text())\n"
        "        retained_descriptors = {row['target'] for row in registry}\n"
        "        if len(registry) != 1242 or len(retained_descriptors) != 605:\n"
        "            raise ValueError('Exact recovered-method/class counts changed')\n"
        "        protected = protected_files()\n"
        "        retained = []\n"
        "        retained_paths = set()")
    text = replace_once(text,
        "                if original['sha256'] != entry['sha256'] or identity(cache) != original or identity(canonical) != original:\n"
        "                    raise ValueError('Cache/source/published member are not exact duplicates: ' + name)",
        "                if original['sha256'] != entry['sha256'] or identity(canonical) != original:\n"
        "                    raise ValueError('Canonical/published member changed: ' + name)\n"
        "                if entry['descriptor'] in retained_descriptors:\n"
        "                    cached = identity(cache)\n"
        "                    retained.append({'descriptor': entry['descriptor'], 'cache': str(cache),\n"
        "                                     'source': str(canonical), 'cache_identity': cached, 'source_identity': original})\n"
        "                    protected.extend([{'path': str(cache), **cached}, {'path': str(canonical), **original}])\n"
        "                    consumed.add(name)\n"
        "                    retained_paths.add(cache)\n"
        "                    continue\n"
        "                if identity(cache) != original:\n"
        "                    raise ValueError('Unrecovered cache class is not an exact published source duplicate: ' + name)")
    text = replace_once(text,
        "        if consumed != set(expected) or cache_paths != {path for path in CACHE.rglob('*.smali') if path.is_file()}:\n"
        "            raise ValueError('Complete canonical/cache membership differs')",
        "        if (consumed != set(expected) or cache_paths & retained_paths\n"
        "                or cache_paths | retained_paths != {path for path in CACHE.rglob('*.smali') if path.is_file()}\n"
        "                or {row['descriptor'] for row in retained} != retained_descriptors\n"
        "                or len(retained) != 605 or count != 70662):\n"
        "            raise ValueError('Complete eligible/retained canonical-cache partition differs')\n"
        "        save(output / 'protected-before.json', protected)\n"
        "        save(output / 'retained-recovered-classes.json', retained)\n"
        "        result['retained_recovered_classes'] = len(retained)\n"
        "        result['registry_sha256'] = REGISTRY_SHA\n"
        "        result['complete_canonical_partition'] = {'eligible_exact_duplicates': count, 'retained_recovered_classes': len(retained), 'total': len(expected)}")
    text = replace_once(text, "'root': 'Closed full acceptance and cache sample reads.'",
                        "'root': 'Closed local full acceptance; read-only hybrid-cache assessment only.'")
    text = replace_once(text, "'build_environment': 'No active or planned reads; complete combined review closed and durable.'",
                        "'build_environment': 'No current or planned verify-hybrid reader; local and hosted acceptance review closed.'")
    text = replace_once(text, "'recover_touch_action': 'No active or planned reads; future micro-D8 excludes this cache.'",
                        "'recover_touch_action': 'No current or planned verify-hybrid reader; only isolated frozen proof/class inputs used.'")
    text = replace_once(text, "'repository_transfer': 'No current or planned reader/writer; only frozen proofs and repo objects used.'",
                        "'repository_transfer': 'No active or planned verify-hybrid reader; repository and closed CI ZIP/checkpoint inputs only.'")
    text = replace_once(text,
        "        result.update(status='CLOSED_DUPLICATE_CACHE_RETIRED_WITH_PROTECTED_BYTES_UNCHANGED',",
        "        retained = json.loads((assessment / 'retained-recovered-classes.json').read_text())\n"
        "        if len(retained) != 605:\n"
        "            raise ValueError('Retained recovered-class inventory changed')\n"
        "        result['retained_recovered_classes_unchanged'] = len(retained)\n"
        "        result['complete_canonical_source_files_unchanged'] = len(rows) + len(retained)\n"
        "        result.update(status='CLOSED_DUPLICATE_CACHE_RETIRED_WITH_PROTECTED_BYTES_UNCHANGED',")
    TARGET.write_text(text)
    (ROOT / 'hybrid-retirement-derivation.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True), text.splitlines(True),
        fromfile='reviewed/retire_verified_smali_duplicates.py', tofile='proposed/retire_verified_hybrid_duplicates.py')))
    print(json.dumps({'status': 'BOUNDED_HYBRID_RETIREMENT_OPERATION_DERIVED', 'path': str(TARGET),
                      'sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(), 'mutationsPerformed': False}, indent=2))

if __name__ == '__main__': main()
