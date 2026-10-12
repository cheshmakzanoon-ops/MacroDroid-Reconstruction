"""Keep the new reconstruction evidence tied to exact methods and fail-closed gates."""
import hashlib,json,unittest
import build,linkage_verify as link

class EnvironmentMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=json.loads((build.ROOT/'source/environment-methods.json').read_text())
        cls.registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
        cls.index={x['descriptor']:x for x in build.index().values()}
    def test_fifteen_methods_in_seven_classes(self):
        self.assertEqual(len(self.entries),15)
        self.assertEqual(len({e['target'] for e in self.entries}),7)
    def test_registry_is_exact_partition(self):
        self.assertEqual(self.entries,[e for e in self.registry if e.get('proof_family')=='v7-environment'])
    def test_original_source_pins(self):
        for e in self.entries:
            text=(build.ROOT/self.index[e['target']]['path']).read_text()
            self.assertEqual(hashlib.sha256(build.methods(text)[e['method']].encode()).hexdigest(),e['original_method_sha256'])
    def test_no_java_placeholder_implementations(self):
        for e in self.entries:
            source=(build.ROOT/e['java_source']).read_text()
            self.assertNotIn('UnsupportedOperationException',source)
            self.assertNotIn('Method not decompiled',source)
    def test_clock_only_under_test_support(self):
        self.assertTrue((build.ROOT/'test-support/java/defpackage/TestClock.java').is_file())
        self.assertFalse((build.ROOT/'source/java/defpackage/TestClock.java').exists())
        for e in self.entries:self.assertNotIn('TestClock',(build.ROOT/e['java_source']).read_text())
    def test_clock_agent_excludes_non_recovered_classes(self):
        source=(build.ROOT/'tests/java/TestClockAgent.java').read_text()
        self.assertIn('!name.startsWith("recovered/")',source)
        self.assertIn('owner.equals("java/util/Calendar")',source)
        self.assertIn('desc.equals("()Ljava/util/Calendar;")',source)
    def test_alias_fixture_count(self):
        aliases=json.loads((build.ROOT/'tests/fixtures/wifi-any-network-aliases.json').read_text())
        self.assertEqual(len(aliases['values']),33)
    def test_suite_families_do_not_overlap(self):
        selected=[e for e in self.registry if e.get('proof_family') in ['v6-core','v7-environment']]
        self.assertEqual(len(selected),25)
        self.assertEqual(len({(e['target'],e['method']) for e in selected}),25)

class LinkageValidatorTests(unittest.TestCase):
    def test_static_call(self):self.assertEqual(link.check_method('LA;','invoke-static','LB;','LB;','x()V',frozenset(['public','static']),frozenset()),[])
    def test_wrong_static_call(self):self.assertTrue(link.check_method('LA;','invoke-virtual','LB;','LB;','x()V',frozenset(['public','static']),frozenset()))
    def test_private_same_class_direct(self):self.assertEqual(link.check_method('LA;','invoke-direct','LA;','LA;','x()V',frozenset(['private']),frozenset()),[])
    def test_private_other_class_rejected(self):self.assertTrue(link.check_method('LA;','invoke-direct','LB;','LB;','x()V',frozenset(['private']),frozenset()))
    def test_interface_range(self):self.assertEqual(link.check_method('LA;','invoke-interface/range','LI;','LI;','x()V',frozenset(['public','abstract']),frozenset(['interface'])),[])
    def test_constructor_requires_direct(self):self.assertTrue(link.check_method('LA;','invoke-virtual','LB;','LB;','<init>()V',frozenset(['public','constructor']),frozenset()))
    def test_field_static_mismatch(self):self.assertTrue(link.check_field('LA;','iget','LB;',frozenset(['static'])))
    def test_private_field_cross_class(self):self.assertTrue(link.check_field('LA;','iget','LB;',frozenset(['private'])))
    def test_private_field_same_class(self):self.assertEqual(link.check_field('LA;','iget','LA;',frozenset(['private'])),[])
    def test_declaration_parser(self):
        d=link.parse('# comment\n.class public final LA;\n.super LB;\n.implements LI;\n.field private flag:Z\n.field public static x:I = 0x3\n.method public x()V\n.end method\n')
        self.assertEqual(d.parent,'LB;');self.assertEqual(d.interfaces,('LI;',));self.assertEqual(d.fields['x:I'],frozenset(['public','static']));self.assertEqual(d.methods['x()V'],frozenset(['public']))
    def test_missing_class_rejected(self):
        with self.assertRaises(ValueError):link.parse('garbage')

if __name__=='__main__':unittest.main()
