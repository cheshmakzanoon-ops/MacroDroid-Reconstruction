"""Exercise constructor mapping across build/static/linkage with synthetic source."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

prototype = Path(__file__).resolve().parents[1] / 'integration/project'
if prototype.is_dir():
    sys.path.insert(0, str(prototype))
import build
import linkage_verify
import validate_migration
from constructor_owner import ConstructorOwnerError, restore_from_preserved_source
from test_constructor_owner import CHILD, COMPILED, ORIGINAL, PARENT


class ConstructorPipelineTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.work = self.root / 'build'
        self.work.mkdir()
        self.reports = self.root / 'reports'
        self.reports.mkdir()
        self.entry = {
            'target': 'LTarget;', 'method': 'create()LChild;', 'instance': False,
            'helper': 'Lrecovered/probe/Helper;', 'helper_method': 'create',
            'java_source': 'source/java/recovered/probe/Helper.java',
            'original_method_sha256': hashlib.sha256(ORIGINAL.encode()).hexdigest(),
            'constructor_owner_mappings': [{'allocated_type': 'LChild;', 'original_owner': 'LParent;',
                                            'constructor': '<init>(ILContinuation;)V', 'occurrences': 1}]}
        self.classes = {
            'LTarget;': '.class public LTarget;\n.super Ljava/lang/Object;\n' + ORIGINAL + '\n',
            'LChild;': CHILD, 'LParent;': PARENT}
        self.index = {}
        for descriptor, text in self.classes.items():
            relative = 'source/smali/classes/' + descriptor[1:-1] + '.smali'
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            self.index['classes:' + descriptor] = {
                'descriptor': descriptor, 'partition': 'classes', 'path': relative,
                'sha256': hashlib.sha256(text.encode()).hexdigest(), 'methods': len(build.methods(text))}
        self.registry = self.root / 'source/java-method-map.json'
        self.registry.write_text(json.dumps([self.entry]))
        helper = self.work / 'java/smali/recovered/probe/Helper.smali'
        helper.parent.mkdir(parents=True)
        helper.write_text('.class public Lrecovered/probe/Helper;\n.super Ljava/lang/Object;\n' + COMPILED + '\n')
        for name, value in [('ROOT', self.root), ('WORK', self.work), ('REPORTS', self.reports)]:
            patcher = patch.object(build, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(build, 'index', return_value=self.index)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_pipeline(self):
        generated = build.hybrid_source(self.work / 'java')
        with contextlib.redirect_stdout(io.StringIO()):
            static = validate_migration.verify()
            linkage = linkage_verify.verify()
        integrated = json.loads((self.reports / 'java-integration.json').read_text())
        return generated, integrated, static, linkage

    def test_all_three_gates_use_the_identical_pinned_correction(self):
        generated, integrated, static, linkage = self.run_pipeline()
        self.assertTrue(static['pass'])
        self.assertTrue(linkage['pass'])
        proof = integrated['constructor_owner_corrections']
        self.assertEqual(len(proof), 1)
        self.assertEqual(static['constructor_owner_corrections'], proof)
        self.assertEqual(linkage['constructor_owner_corrections'], proof)
        self.assertEqual(proof[0]['source_domain'], 'main')
        self.assertEqual(proof[0]['owner_references_changed'], 1)
        self.assertEqual(linkage['original_invocations_checked'], 1)
        self.assertEqual(linkage['external_or_unresolved'], 0)
        self.assertEqual(static['app_members_resolved'], 1)
        body = build.methods((generated / 'classes/Target.smali').read_text())[self.entry['method']]
        self.assertIn('LParent;-><init>(ILContinuation;)V', body)
        self.assertNotIn('LChild;-><init>', body)
        for descriptor, original in self.classes.items():
            self.assertEqual((self.root / self.index['classes:' + descriptor]['path']).read_text(), original)

    def test_no_mapping_keeps_existing_missing_constructor_rejection(self):
        del self.entry['constructor_owner_mappings']
        self.registry.write_text(json.dumps([self.entry]))
        generated = build.hybrid_source(self.work / 'java')
        body = (generated / 'classes/Target.smali').read_text()
        self.assertIn('LChild;-><init>', body)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, 'Migration validation failed'):
            validate_migration.verify()
        report = json.loads((self.reports / 'migration-static-proof.json').read_text())
        self.assertFalse(report['pass'])
        self.assertEqual(report['constructor_owner_corrections'], [])
        self.assertEqual(report['errors'][0]['owner'], 'LChild;')
        self.assertEqual(report['errors'][0]['reason'], 'Missing member in preserved application/library source')

    def test_changed_class_hash_is_rejected_by_each_gate(self):
        parent = self.root / self.index['classes:LParent;']['path']
        parent.write_text(PARENT + '# changed\n')
        for gate in [lambda: build.hybrid_source(self.work / 'java'), validate_migration.verify, linkage_verify.verify]:
            with self.subTest(gate=gate), self.assertRaisesRegex(ConstructorOwnerError, 'pinned class-index SHA-256'):
                gate()

    def test_wrong_original_method_is_rejected_before_transformation(self):
        changed = ORIGINAL.replace('create()', 'other()')
        self.entry['original_method_sha256'] = hashlib.sha256(changed.encode()).hexdigest()
        with self.assertRaisesRegex(ConstructorOwnerError, 'preserved migration target'):
            restore_from_preserved_source(self.entry, COMPILED, changed, self.index, self.root)

    def test_index_hash_cannot_substitute_for_target_class_identity(self):
        path = self.root / self.index['classes:LTarget;']['path']
        changed = path.read_text().replace('.class public LTarget;', '.class public LNotTarget;')
        path.write_text(changed)
        self.index['classes:LTarget;']['sha256'] = hashlib.sha256(changed.encode()).hexdigest()
        with self.assertRaisesRegex(ConstructorOwnerError, 'class declaration does not match its identity'):
            restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)

    def test_duplicate_migration_target_is_rejected(self):
        self.index['other:LTarget;'] = copy.deepcopy(self.index['classes:LTarget;'])
        with self.assertRaisesRegex(ConstructorOwnerError, 'unambiguous migration target'):
            restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)

    def test_duplicate_owner_in_target_domain_is_rejected(self):
        self.index['other:LParent;'] = copy.deepcopy(self.index['classes:LParent;'])
        with self.assertRaisesRegex(ConstructorOwnerError, 'missing or ambiguous in source domain'):
            restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)

    def test_embedded_owner_does_not_satisfy_main_loader_reference(self):
        self.index['classes:LParent;']['partition'] = 'embedded_plugin'
        with self.assertRaisesRegex(ConstructorOwnerError, 'missing or ambiguous in source domain'):
            restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)

    def test_separate_embedded_duplicate_cannot_override_main_owner(self):
        self.index['embedded:LParent;'] = {
            **self.index['classes:LParent;'], 'partition': 'embedded_plugin',
            'path': 'source/smali/embedded_plugin/Unrelated.smali', 'sha256': 'untrusted'}
        _, evidence = restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)
        self.assertEqual(evidence[0]['source_domain'], 'main')
        self.assertEqual(evidence[0]['owner_class_sha256'], hashlib.sha256(PARENT.encode()).hexdigest())

    def test_source_path_escape_is_rejected(self):
        path = self.root / 'outside.smali'
        path.write_text(PARENT)
        self.index['classes:LParent;']['path'] = 'outside.smali'
        with self.assertRaisesRegex(ConstructorOwnerError, 'outside preserved smali source'):
            restore_from_preserved_source(self.entry, COMPILED, ORIGINAL, self.index, self.root)

    def test_unconfigured_methods_need_no_new_source_lookup(self):
        self.assertEqual(restore_from_preserved_source({}, COMPILED, '', {}, self.root), (COMPILED, []))


if __name__ == '__main__':
    unittest.main()
