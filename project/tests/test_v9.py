"""Recovery provenance and adversarial tests for host/device acceptance tooling.
All device reports here are synthetic test fixtures; no Android execution occurs.
"""
import contextlib,copy,hashlib,io,json,struct,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
from unittest.mock import patch
import android_acceptance as recorder
import android_compare as compare
import build
from test import aggregate_reports,validate_method_partition


def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)

def png(pixels=b'\x10\x20\x30\xff',width=1,height=1,color=6,filter_type=0):
    bpp=4 if color==6 else 3;stride=width*bpp;raw=bytearray();previous=bytes(stride)
    for y in range(height):
        row=pixels[y*stride:(y+1)*stride];raw.append(filter_type)
        for x,v in enumerate(row):
            a=row[x-bpp] if x>=bpp else 0;b=previous[x];c=previous[x-bpp] if x>=bpp else 0
            if filter_type==0:p=0
            elif filter_type==1:p=a
            elif filter_type==2:p=b
            elif filter_type==3:p=(a+b)//2
            else:
                p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c);p=a if pa<=pb and pa<=pc else b if pb<=pc else c
            raw.append((v-p)&255)
        previous=row
    return compare.PNG_MAGIC+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,color,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(raw)))+chunk(b'IEND',b'')

class UiSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=json.loads((build.ROOT/'source/ui-methods.json').read_text());cls.registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
        cls.index={x['descriptor']:x for x in build.index().values()}
    def test_exact_seven_methods_and_classes(self):self.assertEqual((len(self.entries),len({e['target'] for e in self.entries})),(7,7))
    def test_registry_partition(self):self.assertEqual(self.entries,[e for e in self.registry if e.get('proof_family')=='v9-ui'])
    def test_each_original_hash(self):
        for e in self.entries:
            original=(build.ROOT/self.index[e['target']]['path']).read_text()
            self.assertEqual(hashlib.sha256(build.methods(original)[e['method']].encode()).hexdigest(),e['original_method_sha256'])
    def test_reference_inventory_inputs_are_pinned(self):
        import release_integrity
        included={p.relative_to(build.ROOT).as_posix() for p in release_integrity.inputs()}
        expected={p.relative_to(build.ROOT).as_posix() for p in (build.ROOT/'reference').rglob('*.java')}
        self.assertEqual(len(expected),1893);self.assertTrue(expected.issubset(included))
    def test_migrated_descriptors_resolve_in_one_partition(self):
        import collections
        counts=collections.Counter(x['descriptor'] for x in build.index().values())
        self.assertTrue(all(counts[e['target']]==1 for e in self.registry))
    def test_no_stubs_or_placeholder_imports_in_helpers(self):
        for entry in self.entries:
            text=(build.ROOT/entry['java_source']).read_text()
            for forbidden in ['UiTrace','UiCursor','BytecodeOracle','Method not decompiled','UnsupportedOperationException','TODO']:
                self.assertNotIn(forbidden,text)
    def test_float_conversion_fixture_is_separate(self):
        self.assertIn('float-to-int',(build.ROOT/'tests/fixtures/ui-opcodes.smali').read_text())
        self.assertFalse((build.ROOT/'source/java/UiNumericProbe.java').exists())
    def test_signed_variant_filename_v9(self):self.assertIn("'MacroDroid-5.67.8-v9-'+variant+'.apk'",(build.ROOT/'build.py').read_text())

class ExactCoverageTests(unittest.TestCase):
    def setUp(self):
        self.registry=[{'target':'LA;','method':'a()V'},{'target':'LB;','method':'b()V'}]
        self.reports={'first':{'methodsCovered':1,'methodKeys':['LA;->a()V']},'second':{'methodsCovered':1,'methodKeys':['LB;->b()V']}}
    def test_partition_valid(self):validate_method_partition(self.reports,self.registry)
    def test_equal_counts_duplicate_methods_rejected(self):
        self.reports['second']['methodKeys']=['LA;->a()V']
        with self.assertRaises(RuntimeError):validate_method_partition(self.reports,self.registry)
    def test_wrong_method_rejected(self):
        self.reports['second']['methodKeys']=['LC;->c()V']
        with self.assertRaises(RuntimeError):validate_method_partition(self.reports,self.registry)
    def test_missing_list_rejected(self):
        del self.reports['first']['methodKeys']
        with self.assertRaises(RuntimeError):validate_method_partition(self.reports,self.registry)
    def test_duplicate_registry_rejected(self):
        with self.assertRaises(RuntimeError):validate_method_partition(self.reports,[self.registry[0],self.registry[0]])
    def test_negative_failures_cannot_cancel(self):
        r={k:{'passed':True,'cases':1,'methodsCovered':1,'paths':3,'failedCases':0,'unsupportedExecutions':0} for k in ['legacy','core','environment','engine','ui']}
        r['core']['failedCases']=1;r['ui']['failedCases']=-1
        self.assertFalse(aggregate_reports(r,5,3)['passed'])
    def test_boolean_count_not_valid(self):
        r={k:{'passed':True,'cases':True,'methodsCovered':1,'paths':3,'failedCases':0,'unsupportedExecutions':0} for k in ['legacy','core','environment','engine','ui']}
        self.assertFalse(aggregate_reports(r,5,3)['passed'])
    def test_missing_ui_rejected(self):
        r={k:{'passed':True,'cases':1,'methodsCovered':1,'paths':3,'failedCases':0,'unsupportedExecutions':0} for k in ['legacy','core','environment','engine']}
        self.assertFalse(aggregate_reports(r,4,3)['passed'])

class DecoderTests(unittest.TestCase):
    def test_all_five_filters_rgb_and_rgba(self):
        for color,bpp in [(2,3),(6,4)]:
            pixels=bytes((i*47+211)%256 for i in range(4*3*bpp))
            expected=pixels if color==6 else b''.join(pixels[i:i+3]+b'\xff' for i in range(0,len(pixels),3))
            for filtering in range(5):self.assertEqual(compare.png_pixels(png(pixels,4,3,color,filtering)),(4,3,expected))
    def test_bad_crc(self):
        data=bytearray(png());data[20]^=1
        with self.assertRaises(compare.CaptureError):compare.png_pixels(bytes(data))
    def test_truncation_and_trailing_bytes(self):
        for data in [png()[:-1],png()+b'junk',compare.PNG_MAGIC]:
            with self.assertRaises(compare.CaptureError):compare.png_pixels(data)
    def test_dimensions_bound(self):
        data=compare.PNG_MAGIC+chunk(b'IHDR',struct.pack('>IIBBBBB',100000,100000,8,6,0,0,0))
        with self.assertRaises(compare.CaptureError):compare.png_pixels(data)
    def test_no_app_nodes(self):
        with self.assertRaises(compare.CaptureError):compare.xml_state(b'<hierarchy><node package="android"/></hierarchy>')
    def test_entity_declaration_rejected(self):
        with self.assertRaises(compare.CaptureError):compare.xml_state(b'<!DOCTYPE hierarchy [<!ENTITY x "xx">]><hierarchy/>')
    def test_attribute_order_not_node_order(self):
        first=b'<hierarchy><node package="com.arlosoft.macrodroid" text="A"/></hierarchy>'
        second=b'<hierarchy>\n <node text="A" package="com.arlosoft.macrodroid"/>\n</hierarchy>'
        self.assertEqual(compare.xml_state(first),compare.xml_state(second))
    def test_node_order_retained(self):
        node=lambda text:f'<node package="{compare.PACKAGE}" text="{text}"/>'
        a=('<hierarchy>'+node('A')+node('B')+'</hierarchy>').encode();b=('<hierarchy>'+node('B')+node('A')+'</hierarchy>').encode()
        self.assertNotEqual(compare.xml_state(a),compare.xml_state(b))

class DeviceGuardsTests(unittest.TestCase):
    def test_start_ok_does_not_prove_live_process(self):
        self.assertTrue(compare.launch_ok(0,'Status: ok\n'))
        with self.assertRaises(compare.CaptureError):compare.live_pids('','')
    def test_pid_restart_rejected(self):
        with self.assertRaises(compare.CaptureError):compare.live_pids('31','32')
    def test_bad_pid_rejected(self):
        for bad in ['0','-1','error','31 stderr']:
            with self.assertRaises(compare.CaptureError):compare.live_pids(bad,bad)
    def test_live_samples(self):self.assertEqual(compare.live_pids('31 42','42 31','31 42'),('31','42'))
    def test_status_error_override(self):self.assertFalse(compare.launch_ok(0,'Status: ok\nError: stopped'))
    def test_background_not_foreground(self):self.assertFalse(compare.foreground_ok('ActivityRecord{com.arlosoft.macrodroid/.Main}'))
    def test_settings_foreground_not_app(self):self.assertFalse(compare.foreground_ok('mResumedActivity: com.android.settings/.Main'))
    def test_correct_resumed(self):self.assertTrue(compare.foreground_ok('mResumedActivity: ActivityRecord{123 u0 com.arlosoft.macrodroid/.Main}'))
    def test_badging_pins_package_and_version(self):
        text="package: name='com.arlosoft.macrodroid' versionCode='896700008' versionName='5.67.8'\nminSdkVersion:'23'\ntargetSdkVersion:'36'"
        self.assertEqual(recorder.badging_metadata(text)['package'],compare.PACKAGE)
        for bad in [text.replace('macrodroid','notmacrodroid'),text.replace('896700008','10'),text.replace("minSdkVersion:'23'","minSdkVersion:'24'")]:
            with self.assertRaises(recorder.Blocked):recorder.badging_metadata(bad)
    def test_legacy_badging_minimum_name(self):
        text="package: name='com.arlosoft.macrodroid' versionCode='896700008' versionName='5.67.8'\nsdkVersion:'23'\ntargetSdkVersion:'36'"
        self.assertEqual(recorder.badging_metadata(text)['min_sdk'],23)
    def test_bad_candidate_preflight_never_removes_package(self):
        # Exercise main using a fake selected emulator. No fake install/launch is accepted.
        def fake(command,**kwargs):
            joined=' '.join(map(str,command))
            if 'uninstall' in command or 'install' in command:raise AssertionError('Device write before pair preflight')
            if 'get-state' in command:out='device\n'
            elif 'getprop ro.product.cpu.abilist' in joined:out='arm64-v8a\n'
            elif 'getprop ro.kernel.qemu' in joined:out='1\n'
            else:out='fixture\n'
            return subprocess.CompletedProcess(command,0,out,'')
        with tempfile.TemporaryDirectory() as d,patch.object(sys,'argv',['android_acceptance.py','--serial','emulator-55','--original','original.apk','--candidate','missing.apk','--accept-package-data-removal','--output',d]),patch('android_acceptance.shutil.which',return_value='/fake/adb'),patch('android_acceptance.subprocess.run',side_effect=fake),patch('android_acceptance.prevalidate_pair',side_effect=recorder.Blocked('candidate invalid')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(recorder.main(),2);report=json.loads((Path(d)/'result.json').read_text());self.assertFalse(report['android_runtime_executed']);self.assertEqual(report['runs'],[])

class CaptureComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        env={k:'synthetic-fixture' for k in recorder.PROPERTIES+['serial','display_size','display_density','font_scale']};env['ro.product.cpu.abilist']='arm64-v8a'
        self.report={'schema_version':2,'status':'CAPTURES_RECORDED_NOT_PARITY','runs':[]}
        for label,digest in [('original','1'*64),('candidate','2'*64)]:
            run={'label':label,'apk_sha256':digest,'environment':env.copy(),'component':compare.PACKAGE+'/.Main','status':'APP_CAPTURE_RECORDED','android_runtime_executed':True,'sample_interval_seconds':2.0,'launch_exit':0,'artifacts':{}}
            for kind,data in {'launch':b'Status: ok\n','pid_first':b'31','pid_second':b'31','pid_final':b'31','foreground':b'mResumedActivity: com.arlosoft.macrodroid/.Main','hierarchy':b'<hierarchy><node package="com.arlosoft.macrodroid" text="Home"/></hierarchy>','screenshot':png()}.items():
                self.put(run,kind,data)
            for name,code,stdout in [('install',0,b'Performing Push Install\nSuccess\n'),('after_uninstall',1,b'')]:
                self.put(run,name+'_stdout',stdout);self.put(run,name+'_stderr',b'')
                run[name]={'returncode':code,'stdout':run['artifacts'][name+'_stdout'],'stderr':run['artifacts'][name+'_stderr']}
            self.report['runs'].append(run)
    def tearDown(self):self.temp.cleanup()
    def put(self,run,kind,data):
        name=run['label']+'-'+kind;self.root.joinpath(name).write_bytes(data);run['artifacts'][kind]={'path':name,'bytes':len(data),'sha256':compare.sha(data)}
    def result(self):
        (self.root/'result.json').write_text(json.dumps(self.report));return compare.compare_capture(self.root)
    def test_synthetic_equal_is_launch_scope_not_feature_parity(self):
        r=self.result();self.assertTrue(r['cold_launch_capture_equal']);self.assertFalse(r['feature_parity_established']);self.assertFalse(r['full_runtime_1_to_1_established'])
    def test_changed_pixel_rejected(self):
        self.put(self.report['runs'][1],'screenshot',png(b'\x11\x20\x30\xff'));r=self.result();self.assertFalse(r['cold_launch_capture_equal']);self.assertEqual(r['changed_pixels'],1)
    def test_changed_ui_rejected(self):
        self.put(self.report['runs'][1],'hierarchy',b'<hierarchy><node package="com.arlosoft.macrodroid" text="Error"/></hierarchy>');self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_different_color_metadata_rejected(self):
        original=png();a=original[:33]+chunk(b'gAMA',struct.pack('>I',45455))+original[33:];b=original[:33]+chunk(b'gAMA',struct.pack('>I',100000))+original[33:]
        self.put(self.report['runs'][0],'screenshot',a);self.put(self.report['runs'][1],'screenshot',b)
        r=self.result();self.assertFalse(r['cold_launch_capture_equal']);self.assertFalse(r['color_metadata_equal'])
    def test_identical_apk_rejected(self):self.report['runs'][1]['apk_sha256']='1'*64;self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_stale_schema_rejected(self):self.report['schema_version']=1;self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_missing_capture_rejected(self):self.report['runs'].pop();self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_tampered_artifact_rejected(self):self.root.joinpath('candidate-launch').write_bytes(b'changed');self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_escaped_path_rejected(self):self.report['runs'][1]['artifacts']['launch']['path']='../outside';self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_environment_mismatch_rejected(self):self.report['runs'][1]['environment']['font_scale']='1.5';self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_incomplete_environment_rejected(self):
        for r in self.report['runs']:r['environment']={'serial':'same'}
        self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_dead_final_pid_rejected(self):self.put(self.report['runs'][1],'pid_final',b'');self.assertFalse(self.result()['cold_launch_capture_equal'])
    def test_system_dialog_not_counted_as_app_match(self):
        for r in self.report['runs']:self.put(r,'foreground',b'mResumedActivity: com.android.permissioncontroller/.Grant')
        self.assertFalse(self.result()['cold_launch_capture_equal'])

if __name__=='__main__':unittest.main()
