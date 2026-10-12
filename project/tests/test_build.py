"""Regression and release-input tests. These do not execute Android."""
from __future__ import annotations
import hashlib,io,json,struct,sys,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build,resource_pack,android_acceptance
import contextlib,tempfile
from unittest.mock import patch
from migrate_constants import constant,descriptor_types,bridge_type,java_string


def block(signature:str,code:str,flags:str='public')->str:
    return f'.method {flags} {signature}\n    .locals 2\n{code}\n.end method'


def pool(values:list[str],utf8:bool)->bytes:
    data=bytearray();offsets=[]
    for text in values:
        offsets.append(len(data));n=len(text.encode('utf-16le'))//2
        if utf8:
            raw=text.encode('utf-8');data+=resource_pack.encode_length8(n)+resource_pack.encode_length8(len(raw))+raw+b'\0'
        else:data+=resource_pack.encode_length16(n)+text.encode('utf-16le')+b'\0\0'
    data+=b'\0'*((-len(data))%4);start=28+4*len(values)
    return struct.pack('<HHI5I',1,28,start+len(data),len(values),0,(256 if utf8 else 0)|1,start,0)+struct.pack('<'+'I'*len(offsets),*offsets)+data

class ConstantRecoveryTests(unittest.TestCase):
    def test_integer(self):self.assertEqual(constant(block('answer()I','const/4 v0, 0x7\nreturn v0'))['value'],7)
    def test_negative(self):self.assertEqual(constant(block('answer()I','const/4 v0, -0x1\nreturn v0'))['value'],-1)
    def test_boolean(self):self.assertEqual(constant(block('answer()Z','const/4 v0, 0x1\nreturn v0'))['java'],'true')
    def test_void(self):self.assertEqual(constant(block('ignore()V','return-void'))['kind'],'void')
    def test_null(self):self.assertEqual(constant(block('none()Ljava/lang/Object;','const/4 v0, 0x0\nreturn-object v0'))['kind'],'null')
    def test_string(self):self.assertEqual(constant(block('s()Ljava/lang/String;','const-string v0, "a\\nb"\nreturn-object v0'))['value'],'a\nb')
    def test_long(self):self.assertEqual(constant(block('n()J','const-wide/16 v0, -0x1\nreturn-wide v0'))['value'],-1)
    def test_zero_double(self):self.assertEqual(constant(block('n()D','const-wide/16 v0, 0x0\nreturn-wide v0'))['kind'],'double')
    def test_constructor_rejected(self):self.assertIsNone(constant(block('<init>()V','return-void')))
    def test_initializer_rejected(self):self.assertIsNone(constant(block('<clinit>()V','return-void','static')))
    def test_field_read_rejected(self):self.assertIsNone(constant(block('x()I','iget v0, p0, Lx;->v:I\nreturn v0')))
    def test_field_write_rejected(self):self.assertIsNone(constant(block('x()V','iput v0, p0, Lx;->v:I\nreturn-void')))
    def test_call_rejected(self):self.assertIsNone(constant(block('x()V','invoke-static {}, Lx;->f()V\nreturn-void')))
    def test_conditional_rejected(self):self.assertIsNone(constant(block('x()I','if-eqz p1, :a\nconst/4 v0, 0x0\n:a\nreturn v0')))
    def test_exception_handler_rejected(self):self.assertIsNone(constant(block('x()I','const/4 v0, 0x0\nreturn v0\n.catch Ljava/lang/Exception; {:a .. :b} :c')))
    def test_wrong_register_rejected(self):self.assertIsNone(constant(block('x()I','const/4 v0, 0x0\nreturn v1')))
    def test_noncanonical_boolean_rejected(self):self.assertIsNone(constant(block('x()Z','const/4 v0, 0x2\nreturn v0')))
    def test_array_descriptor(self):self.assertEqual(descriptor_types('I[[Ljava/lang/String;[IJD'),['I','[[Ljava/lang/String;','[I','J','D'])
    def test_bridge_reference(self):self.assertEqual(bridge_type('Ljava/util/List;'),('Object','Ljava/lang/Object;'))
    def test_bridge_wide_primitive(self):self.assertEqual(bridge_type('J'),('long','J'))
    def test_string_escaping(self):self.assertEqual(java_string('"\\\n'),'"\\"\\\\\\012"')
    def test_supplementary_unicode(self):self.assertEqual(java_string('😀'),'"\\ud83d\\ude00"')
    def test_lone_surrogate(self):self.assertEqual(java_string('\ud800'),'"\\ud800"')

class ResourceTests(unittest.TestCase):
    def test_length8_roundtrip(self):
        for n in [0,1,127,128,255,32767]:self.assertEqual(resource_pack.length8(resource_pack.encode_length8(n),0)[0],n)
    def test_length16_roundtrip(self):
        for n in [0,1,32767,32768,99999]:self.assertEqual(resource_pack.length16(resource_pack.encode_length16(n),0)[0],n)
    def test_length8_rejects_negative(self):
        with self.assertRaises(ValueError):resource_pack.encode_length8(-1)
    def test_length8_rejects_overflow(self):
        with self.assertRaises(ValueError):resource_pack.encode_length8(32768)
    def check_pool(self,utf8):
        original=pool(['res/old.xml','é😀',''],utf8)
        changed,names=resource_pack.replace_pool(original,{'res/old.xml':'res/new.xml'})
        self.assertEqual(names,{'res/old.xml'});restored,names=resource_pack.replace_pool(changed,{'res/new.xml':'res/old.xml'})
        # A replacement legitimately clears the sorted flag, even when reverted.
        original=bytearray(original);flags=struct.unpack_from('<I',original,16)[0];struct.pack_into('<I',original,16,flags&~1)
        self.assertEqual(restored,bytes(original))
    def test_utf8_pool(self):self.check_pool(True)
    def test_utf16_pool(self):self.check_pool(False)
    def test_invalid_pool_rejected(self):
        b=bytearray(pool(['x'],True));struct.pack_into('<H',b,0,2)
        with self.assertRaises(ValueError):resource_pack.replace_pool(bytes(b),{})
    def test_invalid_table_rejected(self):
        with self.assertRaises((ValueError,struct.error)):resource_pack.replace_table_paths(b'not a resource table',{})
    def test_missing_pool_rejected(self):
        with self.assertRaises(ValueError):resource_pack.replace_table_paths(struct.pack('<HHII',2,12,12,1),{})
    def test_ambiguous_path_rejected(self):
        with self.assertRaises(ValueError):resource_pack.file_values('    resource 0x7f010001 x\n      () (file) res/a\n      () (file) res/b')
    def test_aligned_zip(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            for name in ['tiny','lib/arm64-v8a/a.so','resources.arsc']:build.write_aligned(z,name,b'abcd')
        raw=b.getvalue()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            self.assertIsNone(z.testzip())
            for f in z.infolist():
                nl,el=struct.unpack_from('<HH',raw,f.header_offset+26)
                self.assertEqual((f.header_offset+30+nl+el)%(16384 if f.filename.endswith('.so') else 4),0)

class ReleaseSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index=build.index();cls.registry=json.loads((ROOT/'source/java-method-map.json').read_text())
    def test_all_baseline_source_hashes(self):
        failures=[]
        for item in self.index.values():
            p=ROOT/item['path']
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:failures.append(item['path'])
        self.assertEqual(failures,[])
    def test_original_inventory_count(self):self.assertEqual(len(self.index),71267)
    def test_method_inventory_count(self):self.assertEqual(sum(i['methods'] for i in self.index.values()),349972)
    def test_nine_partitions(self):self.assertEqual(len(json.loads((ROOT/'source/partitions.json').read_text())),9)
    def test_registry_count(self):self.assertEqual(len(self.registry),1243)
    def test_registry_unique(self):self.assertEqual(len({(e['target'],e['method']) for e in self.registry}),len(self.registry))
    def test_registered_classes_count(self):self.assertEqual(len({e['target'] for e in self.registry}),605)
    def test_constant_coverage(self):self.assertEqual(sum(e.get('proof_family')=='constant' for e in self.registry),1119)
    def test_split_coverage(self):self.assertEqual(sum(e.get('proof_family')=='split-array' for e in self.registry),2)
    def test_registered_sources_exist(self):
        for entry in self.registry:self.assertTrue((ROOT/entry['java_source']).is_file(),entry['java_source'])
    def test_windows_case_collisions(self):
        paths=[v['path'].casefold() for v in self.index.values()];self.assertEqual(len(paths),len(set(paths)))
    def test_fixture_provenance(self):
        p=json.loads((ROOT/'tests/fixtures/provenance.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'tests/fixtures/original-methods.dex').read_bytes()).hexdigest(),p['fixture_sha256'])
        self.assertEqual(p['methods'],1246)
        self.assertEqual(p['registered_methods'],1243)
        self.assertEqual(p['dependency_methods'],3)
        self.assertEqual(p['methods'],p['registered_methods']+p['dependency_methods'])
        self.assertEqual(p['classes'],607)
        self.assertEqual(p['dependency_declaration_sha256'],hashlib.sha256((ROOT/'tests/fixtures/original-dependencies.json').read_bytes()).hexdigest())
    def test_carrier_has_no_executable_dex_or_compiled_resources(self):
        with zipfile.ZipFile(ROOT/'source/payload.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertEqual([p for p in z.namelist() if p.endswith('.dex') or p in ['resources.arsc','AndroidManifest.xml']],[])
    def test_source_contains_no_build_cache(self):
        self.assertEqual(list((ROOT/'source').rglob('*.class')),[])
    def test_recovered_class_relocator_rejects_other_bytes(self):
        with self.assertRaises(ValueError):build.relocate_class(b'not java')

class AndroidRecorderFailClosedTests(unittest.TestCase):
    def test_no_adb_is_blocked_not_passed(self):
        with tempfile.TemporaryDirectory() as d, patch.object(sys,'argv',['android_acceptance.py','--probe-only','--output',d]), patch('android_acceptance.shutil.which',return_value=None), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(android_acceptance.main(),2)
            report=json.loads((Path(d)/'result.json').read_text())
            self.assertEqual(report['status'],'BLOCKED')
            self.assertFalse(report['android_runtime_executed'])
            self.assertFalse(report['full_parity_established'])
    def test_no_implicit_device_selection(self):
        with tempfile.TemporaryDirectory() as d, patch.object(sys,'argv',['android_acceptance.py','--probe-only','--output',d]), patch('android_acceptance.shutil.which',return_value='/test/adb'), patch('android_acceptance.subprocess.run') as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(android_acceptance.main(),2);run.assert_not_called()
    def test_known_package_only(self):
        self.assertEqual(android_acceptance.PACKAGE,'com.arlosoft.macrodroid')

if __name__=='__main__':unittest.main()
