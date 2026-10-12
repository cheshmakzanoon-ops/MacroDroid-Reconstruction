"""Guard source-migration identity and source-only incremental build caching."""
import hashlib,json,struct,tempfile,unittest,zlib
from pathlib import Path
import build

class CoreMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core=json.loads((build.ROOT/'source/core-methods.json').read_text())
        cls.registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
        cls.by={v['descriptor']:v for v in build.index().values()}
    def test_ten_nonconstant_core_bodies(self):
        self.assertEqual(len(self.core),10)
        self.assertTrue(all(e['proof_family']=='v6-core' for e in self.core))
    def test_core_registry_consistency(self):
        self.assertEqual(self.core,[e for e in self.registry if e.get('proof_family')=='v6-core'])
    def test_each_core_original_hash(self):
        for e in self.core:
            old=build.methods((build.ROOT/self.by[e['target']]['path']).read_text())[e['method']]
            self.assertEqual(hashlib.sha256(old.encode()).hexdigest(),e['original_method_sha256'])
    def test_core_has_no_placeholder_throw(self):
        for e in self.core:
            text=(build.ROOT/e['java_source']).read_text()
            self.assertNotIn('Method not decompiled',text)
            self.assertNotIn('UnsupportedOperationException',text)
    def test_no_core_compile_stub_in_source_tree(self):
        self.assertFalse((build.ROOT/'source/java/defpackage/CoreTrace.java').exists())
        self.assertTrue((build.ROOT/'test-support/java/defpackage/CoreTrace.java').is_file())

class SourceCacheTests(unittest.TestCase):
    def test_fingerprint_changes_with_source(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'A.smali';p.write_text('one')
            a=build.partition_fingerprint(Path(d),'compiler');p.write_text('two')
            self.assertNotEqual(a,build.partition_fingerprint(Path(d),'compiler'))
    def test_fingerprint_changes_with_compiler(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'A.smali').write_text('one')
            self.assertNotEqual(build.partition_fingerprint(Path(d),'a'),build.partition_fingerprint(Path(d),'b'))
    def test_fingerprint_stable_across_locations(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            for d in [a,b]:
                (Path(d)/'A.smali').write_text('one')
                (Path(d)/'B.smali').write_text('two')
            self.assertEqual(build.partition_fingerprint(Path(a),'x'),build.partition_fingerprint(Path(b),'x'))
    def test_fingerprint_changes_with_rename(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'A.smali';p.write_text('one');a=build.partition_fingerprint(Path(d),'x');p.rename(Path(d)/'B.smali')
            self.assertNotEqual(a,build.partition_fingerprint(Path(d),'x'))
    def test_fingerprint_ignores_non_source_files(self):
        with tempfile.TemporaryDirectory() as d:
            a=build.partition_fingerprint(Path(d),'x');(Path(d)/'notes.txt').write_text('notes')
            self.assertEqual(a,build.partition_fingerprint(Path(d),'x'))
    def test_non_dex_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'not.dex';p.write_bytes(b'bad')
            with self.assertRaises(ValueError):build.dex_integrity(p)
    def test_original_fixture_internal_integrity(self):
        p=build.ROOT/'tests/fixtures/original-methods.dex'
        self.assertEqual(build.dex_integrity(p),hashlib.sha256(p.read_bytes()).hexdigest())
    def test_cached_dex_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            raw=bytearray((build.ROOT/'tests/fixtures/original-methods.dex').read_bytes());raw[-1]^=1
            p=Path(d)/'bad.dex';p.write_bytes(raw)
            with self.assertRaises(ValueError):build.dex_integrity(p)
    def test_cached_dex_size_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            raw=bytearray((build.ROOT/'tests/fixtures/original-methods.dex').read_bytes());struct.pack_into('<I',raw,32,len(raw)+4)
            p=Path(d)/'bad.dex';p.write_bytes(raw)
            with self.assertRaises(ValueError):build.dex_integrity(p)

if __name__=='__main__':unittest.main()
