#!/usr/bin/env python3
"""Record two cold launches on an explicitly disposable ARM64 Android device.
Both APKs are prevalidated before any package removal. Installing removes the
known target and its data, so --accept-package-data-removal is required. This
recorder never grants permissions, signs in, bypasses integrity, or claims full
app parity. android_compare.py separately checks the captured launch evidence.
"""
from __future__ import annotations
import argparse,hashlib,json,re,shlex,shutil,subprocess,sys,time,uuid,zipfile
from datetime import datetime,timezone
from pathlib import Path
from android_compare import CaptureError,foreground_ok,launch_ok,live_pids,png_pixels,xml_state
PACKAGE='com.arlosoft.macrodroid'
ORIGINAL_SHA256='84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
ROOT=Path(__file__).resolve().parent
PROPERTIES=['ro.product.cpu.abilist','ro.product.cpu.abi','ro.build.version.sdk','ro.build.fingerprint',
            'ro.kernel.qemu','ro.hardware','ro.dalvik.vm.native.bridge','ro.dalvik.vm.isa.arm64',
            'persist.sys.locale','persist.sys.timezone']

class Blocked(RuntimeError):pass

def positive_timeout(value:str)->int:
    """Software CPU emulation may need longer waits; a timeout is never a pass."""
    try:seconds=int(value)
    except ValueError as exc:raise argparse.ArgumentTypeError('Timeout must be an integer number of seconds') from exc
    if not 1<=seconds<=1800:raise argparse.ArgumentTypeError('Timeout must be between 1 and 1800 seconds')
    return seconds

def sha(path:Path)->str:
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def badging_metadata(text:str)->dict:
    found=re.search(r"^package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'",text,re.M)
    if not found:raise Blocked('APK package metadata could not be read')
    name,code,version=found.groups()
    if (name,code,version)!=(PACKAGE,'896700008','5.67.8'):raise Blocked('APK is not the expected package/version')
    minimum=re.search(r"^(?:minSdkVersion|sdkVersion):'([^']+)'",text,re.M);target=re.search(r"^targetSdkVersion:'([^']+)'",text,re.M)
    if not minimum or not target or (minimum[1],target[1])!=('23','36'):raise Blocked('APK SDK metadata differs from comparison target')
    return {'package':name,'version_code':code,'version_name':version,'min_sdk':23,'target_sdk':36}

def prevalidate_pair(original:Path,candidate:Path)->list[dict]:
    """No ADB calls or device mutations occur in this preflight."""
    import build
    result=[]
    for label,apk in [('original',original),('candidate',candidate)]:
        if not apk.is_file() or not zipfile.is_zipfile(apk):raise Blocked(label+' APK is missing or invalid')
        with zipfile.ZipFile(apk) as z:
            names=z.namelist()
            if len(names)!=len(set(names)) or 'AndroidManifest.xml' not in names or 'classes.dex' not in names:raise Blocked(label+' APK structure is invalid')
            if z.testzip() is not None:raise Blocked(label+' APK CRC check failed')
        digest=sha(apk)
        if label=='original' and digest!=ORIGINAL_SHA256:raise Blocked('The original APK does not match the supplied comparison target')
        p=subprocess.run([str(build.aapt()),'dump','badging',str(apk.resolve())],capture_output=True,text=True,timeout=60)
        if p.returncode:raise Blocked(label+' APK badging failed')
        result.append({'label':label,'path':str(apk.resolve()),'apk_sha256':digest,'bytes':apk.stat().st_size,'metadata':badging_metadata(p.stdout)})
    if result[0]['apk_sha256']==result[1]['apk_sha256']:raise Blocked('Candidate is identical to original; this does not test reconstruction')
    return result

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--serial',help='Explicit disposable device serial; no default device is selected.')
    ap.add_argument('--original',type=Path);ap.add_argument('--candidate',type=Path)
    ap.add_argument('--accept-package-data-removal',action='store_true')
    ap.add_argument('--allow-physical-device',action='store_true',help='Allow an explicitly selected disposable physical device.')
    ap.add_argument('--probe-only',action='store_true',help='Availability only; installs nothing.')
    ap.add_argument('--install-timeout',type=positive_timeout,default=180,
                    help='Maximum seconds for each APK install (default: 180).')
    ap.add_argument('--launch-timeout',type=positive_timeout,default=90,
                    help='Maximum seconds for each activity start (default: 90).')
    ap.add_argument('--ui-timeout',type=positive_timeout,default=90,
                    help='Maximum seconds for each UI hierarchy dump (default: 90).')
    ap.add_argument('--output',type=Path,default=ROOT/'reports/android-runtime')
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    report={'schema_version':2,'time_utc':datetime.now(timezone.utc).isoformat(),'android_runtime_executed':False,
            'full_parity_established':False,'status':'BLOCKED','runs':[],'scope':'Cold-launch capture only; no feature parity claim'}
    report['command_timeouts_seconds']={'install':args.install_timeout,'launch':args.launch_timeout,'ui_dump':args.ui_timeout}
    adb=shutil.which('adb')
    def command(argv,*,timeout=60,binary=False):return subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=not binary,timeout=timeout,check=False)
    def device(argv,**kw):return command([adb,'-s',args.serial,*argv],**kw)
    def shell(argv,**kw):return device(['shell',shlex.join(argv)],**kw)
    def evidence(name,data):
        p=args.output/name;p.write_bytes(data)
        return {'path':name,'bytes':len(data),'sha256':sha(p)}
    def save(name,result):
        stdout=result.stdout.encode('utf-8',errors='replace') if isinstance(result.stdout,str) else result.stdout
        stderr=result.stderr.encode('utf-8',errors='replace') if isinstance(result.stderr,str) else result.stderr
        return {'returncode':result.returncode,'stdout':evidence(name+'.stdout.txt',stdout),'stderr':evidence(name+'.stderr.txt',stderr)}
    def checked(name,result):
        saved=save(name,result)
        if result.returncode:raise CaptureError('Device command failed: '+name)
        return saved['stdout']
    def environment():
        props={'serial':args.serial}
        for key in PROPERTIES:
            r=shell(['getprop',key])
            if r.returncode:raise Blocked('Device properties unreadable')
            props[key]=r.stdout.strip()
        for key,cmd in [('display_size',['wm','size']),('display_density',['wm','density']),
                        ('font_scale',['settings','get','system','font_scale']),
                        ('airplane_mode_on',['settings','get','global','airplane_mode_on']),
                        ('wifi_on',['settings','get','global','wifi_on']),
                        ('mobile_data',['settings','get','global','mobile_data'])]:
            r=shell(cmd)
            if r.returncode:raise Blocked('Device display settings unreadable')
            props[key]=r.stdout.strip()
        return props
    try:
        if not adb:raise Blocked('ADB is not installed or not on PATH. No Android process was executed.')
        if not args.serial:raise Blocked('An explicit disposable device --serial is required.')
        report['device_listing']=save('devices',command([adb,'devices','-l']))
        state=device(['get-state'])
        if state.returncode or state.stdout.strip()!='device':raise Blocked('Selected device is unavailable or unauthorized.')
        props=environment();report['device']=props
        if args.probe_only:report['status']='AVAILABLE_NOT_EXECUTED';return 0
        if not args.accept_package_data_removal:raise Blocked('Explicit --accept-package-data-removal is required; target data will be deleted between runs.')
        if props['ro.kernel.qemu']!='1' and not args.allow_physical_device:raise Blocked('Physical device rejected without --allow-physical-device.')
        if 'arm64-v8a' not in props['ro.product.cpu.abilist'].split(','):raise Blocked('ARM64 support is required. No libraries are removed or patched.')
        if args.original is None or args.candidate is None:raise Blocked('--original and --candidate are both required.')
        # Crucial safety boundary: both are fully checked BEFORE the first uninstall.
        pair=prevalidate_pair(args.original,args.candidate);report['apk_preflight']=pair
        for entry in pair:
            apk=Path(entry['path'])
            if sha(apk)!=entry['apk_sha256']:raise Blocked('APK changed after preflight; no further package removal.')
            label=entry['label'];run={'label':label,'apk_sha256':entry['apk_sha256'],'status':'NOT_INSTALLED','android_runtime_executed':False,'artifacts':{}};report['runs'].append(run)
            try:
                run['environment']=environment()
                run['uninstall']=save(label+'-uninstall',device(['uninstall',PACKAGE]))
                present=shell(['pm','path',PACKAGE]);run['after_uninstall']=save(label+'-absent',present)
                if 'package:' in present.stdout:raise CaptureError('Target package still installed after explicit removal')
                installed=device(['install','--no-streaming',str(apk)],timeout=args.install_timeout);run['install']=save(label+'-install',installed)
                if installed.returncode or installed.stdout.strip()!='Success':raise CaptureError('APK installation did not succeed')
                run['status']='INSTALLED_NOT_EXECUTED'
                resolved=shell(['cmd','package','resolve-activity','--brief','-a','android.intent.action.MAIN','-c','android.intent.category.LAUNCHER','-p',PACKAGE]);run['resolve']=save(label+'-resolve',resolved)
                components=[line.strip() for line in resolved.stdout.splitlines() if re.fullmatch(re.escape(PACKAGE)+r'/[A-Za-z0-9_.$]+',line.strip())]
                if resolved.returncode or not components:raise CaptureError('Launcher could not be resolved')
                run['component']=components[-1];checked(label+'-stop',shell(['am','force-stop',PACKAGE]))
                started=shell(['am','start','-W','-n',components[-1]],timeout=args.launch_timeout);run['launch_exit']=started.returncode
                run['artifacts']['launch']=save(label+'-launch',started)['stdout']
                if not launch_ok(started.returncode,started.stdout):raise CaptureError('Launcher did not report a successful start')
                time.sleep(3);first=shell(['pidof',PACKAGE]);run['artifacts']['pid_first']=checked(label+'-pid-first',first)
                sampled=time.monotonic();time.sleep(2);second=shell(['pidof',PACKAGE]);run['sample_interval_seconds']=time.monotonic()-sampled
                run['artifacts']['pid_second']=checked(label+'-pid-second',second);pids=live_pids(first.stdout,second.stdout)
                run['android_runtime_executed']=True;report['android_runtime_executed']=True
                foreground=shell(['dumpsys','activity','activities']);run['artifacts']['foreground']=checked(label+'-foreground',foreground)
                if not foreground_ok(foreground.stdout):raise CaptureError('Application was not the foreground resumed activity')
                remote='/data/local/tmp/mdrecovery-'+uuid.uuid4().hex+'.xml'
                try:
                    checked(label+'-ui-dump',shell(['uiautomator','dump',remote],timeout=args.ui_timeout))
                    hierarchy=device(['exec-out','cat',remote],binary=True)
                    if hierarchy.returncode:raise CaptureError('UI hierarchy retrieval failed')
                    _,nodes=xml_state(hierarchy.stdout);run['app_ui_nodes']=nodes
                    run['artifacts']['hierarchy']=evidence(label+'-hierarchy.xml',hierarchy.stdout)
                finally:save(label+'-ui-cleanup',shell(['rm','-f',remote]))
                screenshot=device(['exec-out','screencap','-p'],binary=True)
                if screenshot.returncode:raise CaptureError('Screenshot retrieval failed')
                width,height,_=png_pixels(screenshot.stdout);run['screen_size']=[width,height]
                run['artifacts']['screenshot']=evidence(label+'.png',screenshot.stdout)
                # Logs are restricted to the observed app PID, not the entire device.
                run['logcat']=save(label+'-logcat',device(['logcat','-d','--pid='+pids[0],'-v','threadtime','-t','500']))
                # Detect a crash/process replacement during screenshot/UI collection too.
                final=shell(['pidof',PACKAGE]);run['artifacts']['pid_final']=checked(label+'-pid-final',final)
                live_pids(second.stdout,final.stdout)
                if environment()!=run['environment']:raise CaptureError('Device environment changed during capture')
                run['status']='APP_CAPTURE_RECORDED'
            except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:
                run['status']='CAPTURE_FAILED';run['reason']=str(exc)
            (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        complete=len(report['runs'])==2 and all(r['status']=='APP_CAPTURE_RECORDED' for r in report['runs'])
        report['status']='CAPTURES_RECORDED_NOT_PARITY' if complete else 'CAPTURE_INCOMPLETE'
        return 0 if complete else 2
    except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:report['reason']=str(exc);return 2
    finally:
        (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':sys.exit(main())
