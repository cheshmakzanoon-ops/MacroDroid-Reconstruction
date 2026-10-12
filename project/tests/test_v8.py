"""Engine source provenance and fail-closed suite accounting."""
import copy,hashlib,json,unittest
import build
from test import aggregate_reports

class EngineMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=json.loads((build.ROOT/'source/engine-methods.json').read_text())
        cls.registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
        cls.index={x['descriptor']:x for x in build.index().values()}
    def test_twelve_selected_methods(self):self.assertEqual(len(self.entries),12)
    def test_five_target_classes(self):self.assertEqual(len({e['target'] for e in self.entries}),5)
    def test_exact_registry_partition(self):self.assertEqual(self.entries,[e for e in self.registry if e.get('proof_family')=='v8-engine'])
    def test_source_provenance(self):
        for e in self.entries:
            original=(build.ROOT/self.index[e['target']]['path']).read_text()
            self.assertEqual(hashlib.sha256(build.methods(original)[e['method']].encode()).hexdigest(),e['original_method_sha256'])
    def test_no_placeholder_methods(self):
        for e in self.entries:
            s=(build.ROOT/e['java_source']).read_text()
            for bad in ['Method not decompiled','UnsupportedOperationException','TODO']:self.assertNotIn(bad,s)
    def test_host_substitutes_never_imported_by_runtime_helpers(self):
        for e in self.entries:
            s=(build.ROOT/e['java_source']).read_text()
            for bad in ['EngineRuntime','CoreTrace','BytecodeOracle','TestClock']:self.assertNotIn(bad,s)
    def test_primary_dispatch_signature(self):
        rows=[e for e in self.entries if e['helper_method']=='dispatch']
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['target'],'Lcom/arlosoft/macrodroid/macro/Macro;')
        self.assertIn('Ljava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;',rows[0]['method'])
    def test_engine_fixture_present(self):
        self.assertIn('monitor-enter',(build.ROOT/'tests/fixtures/engine-opcodes.smali').read_text())
        self.assertIn('monitor-exit',(build.ROOT/'tests/fixtures/engine-opcodes.smali').read_text())

class AggregationTests(unittest.TestCase):
    def setUp(self):
        self.r={k:{'passed':True,'methodsCovered':1,'cases':5,'failedCases':0,'unsupportedExecutions':0,'paths':3} for k in ['legacy','core','environment','engine','ui']}
    def test_all_required_suites_pass(self):self.assertTrue(aggregate_reports(self.r,5,3)['passed'])
    def test_missing_engine_fails_even_if_total_changed(self):
        self.r.pop('engine');self.assertFalse(aggregate_reports(self.r,3,3)['passed'])
    def test_missing_methods_fails(self):self.assertFalse(aggregate_reports(self.r,6,3)['passed'])
    def test_extra_methods_fails(self):self.assertFalse(aggregate_reports(self.r,4,3)['passed'])
    def test_empty_suite_fails(self):
        self.r['engine']['cases']=0;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_false_pass_fails(self):
        self.r['engine']['passed']=False;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_recorded_failure_overrides_pass_flag(self):
        self.r['engine']['failedCases']=1;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_unsupported_execution_fails(self):
        self.r['engine']['unsupportedExecutions']=1;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_two_paths_cannot_be_reported_as_three(self):
        self.r['engine']['paths']=2;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_boolean_pass_alias(self):
        del self.r['engine']['passed'];self.r['engine']['pass']=True;self.assertTrue(aggregate_reports(self.r,5,3)['passed'])
    def test_engine_failure_count_alias(self):
        del self.r['engine']['failedCases'];self.r['engine']['failures']=1;self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_string_true_not_valid(self):
        self.r['engine']['passed']='true';self.assertFalse(aggregate_reports(self.r,5,3)['passed'])
    def test_no_android_claim(self):self.assertFalse(aggregate_reports(self.r,5,3)['androidRuntime'])

if __name__=='__main__':unittest.main()
