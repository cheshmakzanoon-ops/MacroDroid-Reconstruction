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
from android_compare import (CaptureError,ORIGINAL_SHA256,absence_ok,foreground_ok,
                             install_ok,installed_path,installed_digest,launch_ok,live_pids,png_pixels,xml_state)
PACKAGE='com.arlosoft.macrodroid'
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
    ap.add_argument('--intro-pages',action='store_true',
                    help='Also record four English intro pages using three observed app Next buttons.')
    ap.add_argument('--post-intro',action='store_true',
                    help='After --intro-pages, tap the observed completion button once and capture the first resulting surface; makes no permission choice.')
    ap.add_argument('--install-timeout',type=positive_timeout,default=180,
                    help='Maximum seconds for each APK install (default: 180).')
    ap.add_argument('--launch-timeout',type=positive_timeout,default=90,
                    help='Maximum seconds for each activity start (default: 90).')
    ap.add_argument('--ui-timeout',type=positive_timeout,default=90,
                    help='Maximum seconds for each UI hierarchy dump (default: 90).')
    ap.add_argument('--output',type=Path,default=ROOT/'reports/android-runtime')
    args=ap.parse_args()
    if args.post_intro and not args.intro_pages:ap.error('--post-intro requires --intro-pages')
    if not args.probe_only and args.output.is_dir() and any(args.output.iterdir()):ap.error('A new or empty capture output directory is required')
    args.output.mkdir(parents=True,exist_ok=True)
    report={'schema_version':3,'time_utc':datetime.now(timezone.utc).isoformat(),'android_runtime_executed':False,
            'full_parity_established':False,'status':'BLOCKED','runs':[],'scope':'Cold-launch capture only; no feature parity claim'}
    report['command_timeouts_seconds']={'install':args.install_timeout,'launch':args.launch_timeout,'ui_dump':args.ui_timeout}
    report['intro_pages_requested']=args.intro_pages
    report['post_intro_requested']=args.post_intro
    if args.intro_pages:report['scope']='Cold launch plus four intro pages and three Next transitions only'
    if args.post_intro:report['scope']='Cold launch, four intro page stills, and first surface after one observed completion tap; no permission choice'
    # A killed or timed-out capture must leave a current non-success result.
    (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
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
                        ('mobile_data',['settings','get','global','mobile_data']),
                        ('sysui_demo_allowed',['settings','get','global','sysui_demo_allowed']),
                        ('sysui_tuner_demo_on',['settings','get','global','sysui_tuner_demo_on']),
                        ('animator_duration_scale',['settings','get','global','animator_duration_scale']),
                        ('window_animation_scale',['settings','get','global','window_animation_scale']),
                        ('transition_animation_scale',['settings','get','global','transition_animation_scale'])]:
            r=shell(cmd)
            if r.returncode:raise Blocked('Device display settings unreadable')
            props[key]=r.stdout.strip()
        return props
    def capture_intro(run,label):
        import android_intro as intro
        initial=run['artifacts']
        sequence={'status':'RECORDING','pages':[], 'transitions':[]};run['intro_sequence']=sequence
        first={'page':1,'sample_interval_seconds':run['sample_interval_seconds'],'artifacts':{
            'pid_first':initial['pid_first'],'pid_final':initial['pid_final'],
            'foreground':initial['foreground'],'hierarchy':initial['hierarchy'],'screenshot':initial['screenshot']}}
        sequence['pages'].append(first)
        hierarchy=(args.output/initial['hierarchy']['path']).read_bytes()
        foreground=(args.output/initial['foreground']['path']).read_text()
        if not intro.intro_foreground(foreground):raise CaptureError('Intro activity was not observed before navigation')
        first['title']=intro.page_title(hierarchy,1)
        identities=[intro.page_identity(hierarchy)]
        anchor=(args.output/initial['pid_final']['path']).read_text()
        width,height=run['screen_size']
        for number in range(2,intro.PAGE_COUNT+1):
            previous=sequence['pages'][-1]
            hierarchy=(args.output/previous['artifacts']['hierarchy']['path']).read_bytes()
            name=f'{label}-intro-{number}'
            before={}
            remote='/data/local/tmp/mdrecovery-'+uuid.uuid4().hex+'.xml'
            # Include dump and retrieval latency in the age of the UI observation.
            observed=time.monotonic()
            try:
                checked(name+'-before-ui-dump',shell(['uiautomator','dump',remote],timeout=args.ui_timeout))
                fresh=device(['exec-out','cat',remote],binary=True)
                if fresh.returncode:raise CaptureError('Intro input precondition could not be captured')
                before['hierarchy']=evidence(name+'-before-hierarchy.xml',fresh.stdout)
            finally:save(name+'-before-ui-cleanup',shell(['rm','-f',remote]))
            if xml_state(fresh.stdout)[0]!=xml_state(hierarchy)[0]:raise CaptureError('Intro UI changed before input')
            current_pid=shell(['pidof',PACKAGE]);before['pid']=checked(name+'-before-pid',current_pid)
            live_pids(anchor,current_pid.stdout)
            front=shell(['dumpsys','activity','activities']);before['foreground']=checked(name+'-before-foreground',front)
            if not intro.intro_foreground(front.stdout):raise CaptureError('Intro activity was not foreground before input')
            coordinates=intro.next_target(fresh.stdout,width,height)
            argv=['input','tap',*map(str,coordinates)]
            transition={'from_page':number-1,'to_page':number,'selector':intro.NEXT_ID,
                        'coordinates':list(coordinates),'precondition_hierarchy':before['hierarchy'],
                        'precondition_artifacts':before,
                        'shell_argv':argv}
            sequence['transitions'].append(transition)
            age=time.monotonic()-observed;transition['precondition_age_seconds']=age
            if age>intro.MAX_PRECONDITION_AGE:raise CaptureError('Intro UI precondition expired before input')
            tapped=shell(argv);transition['command']=save(name+'-tap',tapped)
            if tapped.returncode or tapped.stdout.strip() or tapped.stderr.strip():raise CaptureError('Intro Next tap did not complete cleanly')
            time.sleep(3)
            page={'page':number,'artifacts':{}};sequence['pages'].append(page);a=page['artifacts']
            before=shell(['pidof',PACKAGE]);a['pid_first']=checked(name+'-pid-first',before);sampled=time.monotonic()
            live_pids(anchor,before.stdout)
            front=shell(['dumpsys','activity','activities']);a['foreground']=checked(name+'-foreground',front)
            if not intro.intro_foreground(front.stdout):raise CaptureError('Intro activity left the foreground during navigation')
            remote='/data/local/tmp/mdrecovery-'+uuid.uuid4().hex+'.xml'
            try:
                checked(name+'-ui-dump',shell(['uiautomator','dump',remote],timeout=args.ui_timeout))
                hierarchy_result=device(['exec-out','cat',remote],binary=True)
                if hierarchy_result.returncode:raise CaptureError('Intro hierarchy retrieval failed')
                hierarchy=hierarchy_result.stdout;_,nodes=xml_state(hierarchy);page['app_ui_nodes']=nodes
                a['hierarchy']=evidence(name+'-hierarchy.xml',hierarchy)
            finally:save(name+'-ui-cleanup',shell(['rm','-f',remote]))
            identity=intro.page_identity(hierarchy)
            if identity in identities:raise CaptureError('Intro Next did not reach a distinct page')
            identities.append(identity)
            page['title']=intro.page_title(hierarchy,number)
            screenshot=device(['exec-out','screencap','-p'],binary=True)
            if screenshot.returncode:raise CaptureError('Intro screenshot retrieval failed')
            width,height,_=png_pixels(screenshot.stdout);page['screen_size']=[width,height]
            a['screenshot']=evidence(name+'.png',screenshot.stdout)
            time.sleep(max(0,1-(time.monotonic()-sampled)))
            after=shell(['pidof',PACKAGE]);a['pid_final']=checked(name+'-pid-final',after)
            page['sample_interval_seconds']=time.monotonic()-sampled
            live_pids(anchor,before.stdout,after.stdout)
            if environment()!=run['environment']:raise CaptureError('Device environment changed during intro navigation')
        sequence['status']='INTRO_PAGES_RECORDED'
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
                if not absence_ok(present.returncode,present.stdout,present.stderr):raise CaptureError('Target package absence was not verified after removal')
                installed=device(['install','--no-streaming',str(apk)],timeout=args.install_timeout);run['install']=save(label+'-install',installed)
                if not install_ok(installed.returncode,installed.stdout,installed.stderr):raise CaptureError('APK installation did not succeed')
                on_device=shell(['pm','path',PACKAGE]);run['installed_apk']={'package_path':save(label+'-installed-path',on_device)}
                base_apk=installed_path(on_device.returncode,on_device.stdout,on_device.stderr)
                checksum=shell(['sha256sum',base_apk]);run['installed_apk']['checksum']=save(label+'-installed-sha256',checksum)
                observed=installed_digest(checksum.returncode,checksum.stdout,checksum.stderr,base_apk)
                run['installed_apk']['sha256']=observed
                if observed!=entry['apk_sha256']:raise CaptureError('Installed APK differs from the prevalidated input')
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
                if args.intro_pages:
                    try:capture_intro(run,label)
                    except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:
                        sequence=run.setdefault('intro_sequence',{})
                        sequence['status']='INTRO_CAPTURE_FAILED';sequence['reason']=str(exc)
                if args.post_intro and run.get('intro_sequence',{}).get('status')=='INTRO_PAGES_RECORDED':
                    # Save earlier evidence before entering the additional scope.
                    def checkpoint():
                        (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
                    checkpoint()
                    try:
                        from android_post_intro import CaptureIO,capture_after_intro
                        io=CaptureIO(args.output,args.ui_timeout,shell,device,save,checked,evidence,environment,checkpoint)
                        capture_after_intro(run,label,io)
                    except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:
                        post=run.setdefault('post_intro',{})
                        post['status']='POST_INTRO_CAPTURE_FAILED';post['reason']=str(exc)
            except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:
                run['status']='CAPTURE_FAILED';run['reason']=str(exc)
            (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        complete=len(report['runs'])==2 and all(r['status']=='APP_CAPTURE_RECORDED' for r in report['runs'])
        intro_complete=not args.intro_pages or all(r.get('intro_sequence',{}).get('status')=='INTRO_PAGES_RECORDED' for r in report['runs'])
        post_complete=not args.post_intro or all(r.get('post_intro',{}).get('status')=='POST_INTRO_SURFACE_RECORDED' for r in report['runs'])
        report['cold_intro_capture_complete']=complete and intro_complete
        report['requested_capture_complete']=complete and intro_complete and post_complete
        report['status']='CAPTURES_RECORDED_NOT_PARITY' if complete else 'CAPTURE_INCOMPLETE'
        if complete and not intro_complete:report['status']='COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE'
        if complete and intro_complete and not post_complete:report['status']='COLD_AND_INTRO_CAPTURES_RECORDED_POST_INTRO_INCOMPLETE'
        return 0 if report['requested_capture_complete'] else 2
    except (Blocked,CaptureError,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:report['reason']=str(exc);return 2
    finally:
        (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':sys.exit(main())
