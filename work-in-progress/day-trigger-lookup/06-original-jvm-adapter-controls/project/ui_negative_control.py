#!/usr/bin/env python3
"""Require observable rejection of deliberate UI/serialization/service-dispatch defects.
Mutations exist in temporary host class directories only. The correct source,
selected original DEX fixture and signed hybrid APK must remain unchanged.
The suite is a bounded host comparison, not an Android execution.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess
from pathlib import Path
import build
import ui_runtime_policy
import ui_mutation_catalog
import day_numeric_dex_controls

CONTROLS=[
    ('cast-before-subtract','InteractionMethods','int distance = (int) event.getY(pointer) - self.g;',
     'int distance = (int) (event.getY(pointer) - self.g);','touch-numeric:0.9:1:7'),
    ('parcel-nonzero-boolean','SceneStateMethods','parcel.readInt() != 0,',
     'parcel.readInt() == 1,','parcel-read:1:1'),
    ('parcel-field-order','SceneStateMethods','parcel.writeInt(self.isBold ? 1 : 0);',
     'parcel.writeInt(self.isItalic ? 1 : 0);','parcel-write:1:0:0'),
    ('sms-catch-must-not-swallow-error','SelectionMethods',
     '} catch (Exception ignored) {\n            // Preserve the uploaded implementation;',
     '} catch (Throwable ignored) {\n            // Preserve the uploaded implementation;','provider:1:1:2:true'),
    ('sound-generic-token','SelectionMethods','return text.startsWith("[") && text.endsWith("]");',
     'return false;','sound:4:0'),
    ('block-toggle-snapshot','BlockTouchesMethods',
     'if (option != 0 && (option != 2 || blocking)) {',
     'if (option != 0 && (option != 2 || BlockTouchesService.j || MacroDroidAccessibilityServiceJellyBean.v)) {',
     'block:2:2:1:false:true'),
    ('block-option-must-be-reread','BlockTouchesMethods',
     '        option = self.option;\n        if (option != 0',
     '        option = option;\n        if (option != 0',
     'block-option-after-stop:1:0:0'),
    ('block-trigger-must-be-reread','BlockTouchesMethods',
     '                trigger = info == null ? null : info.getTrigger();',
     '                trigger = trigger;',
     'block:0:9:0:false:true'),
    ('block-width-payload','BlockTouchesMethods','start.putExtra("width", width);',
     'start.putExtra("width", height);','block:0:2:0:false:true'),
    ('block-hidden-color-sentinel','BlockTouchesMethods',
     '            if (!self.showBlockedArea) color = -1;',
     '            if (!self.showBlockedArea) color = 0;',
     'block:0:2:0:true:false'),
    ('block-catch-must-include-checked-exception','BlockTouchesMethods',
     '} catch (Exception error) {','} catch (RuntimeException error) {',
     'block-fault:accessibility:12:4'),
    ('block-catch-must-not-swallow-error','BlockTouchesMethods',
     '} catch (Exception error) {',
     '} catch (Throwable swallowed) { Exception error = new IllegalStateException(swallowed);',
     'block-fault:accessibility:12:3'),
    ('scene-permission-warning-falls-through','CustomSceneMethods',
     '            // The original warning deliberately falls through to scene dispatch.',
     '            return; // Deliberate fault: stop after the warning.',
     'scene:2:2:false:false:0:true:0'),
    ('scene-accessibility-description-key','CustomSceneMethods',
     'intent.putExtra("scene_description", description);',
     'intent.putExtra("sceneDescription", description);',
     'scene:1:2:true:true:0:true:0'),
    ('scene-dialog-runnable-discriminator','CustomSceneMethods',
     'isTest, resume, nextActionIndex, 0);',
     'isTest, resume, nextActionIndex, 1);',
     'scene:2:2:true:true:1:true:0'),
    ('scene-destroyed-activity-is-not-reused','CustomSceneMethods',
     '            if (existing != null && !((Activity) existing).isFinishing() && !((Activity) existing).isDestroyed()) {',
     '            if (existing != null && !((Activity) existing).isFinishing()) {',
     'scene:2:2:true:true:3:true:0'),
    ('scene-clear-event-precedes-launch','CustomSceneMethods',
     '        bus.e(clear);\n        context.startActivity(intent);',
     '        context.startActivity(intent);\n        bus.e(clear);',
     'scene:3:2:true:true:0:true:0'),
    ('scene-long-item-identifier','CustomSceneMethods',
     '                    intent.putExtra("SelectableItemId", itemId);',
     '                    intent.putExtra("SelectableItemId", guid);',
     'scene:1:2:true:true:0:true:0'),
    ('scene-description-reread-after-context','CustomSceneMethods',
     '                context.getClass();\n                description = self.sceneDescription;',
     '                context.getClass();\n                description = description;',
     'scene-description-after-context:1'),
    ('scene-catch-includes-checked-exception','CustomSceneMethods',
     '} catch (Exception error) {','} catch (RuntimeException error) {',
     'scene-fault:accessibility:22:4'),
    ('scene-catch-must-not-swallow-error','CustomSceneMethods',
     '} catch (Exception error) {',
     '} catch (Throwable swallowed) { Exception error = new IllegalStateException(swallowed);',
     'scene-fault:accessibility:22:3'),
    ('scene-description-key-is-read','CustomSceneMethods',
     '\n        String descriptionKey = SceneBaseActivity.E;',
     '\n        String descriptionKey = "scene_description";',
     'scene-dynamic-key-bus:3:0:false'),
    ('plugin-denied-guard','PluginLookupMethods',
     '            if (owner.i) {',
     '            if (false) {',
     'plugin-gate:true:false:0:0'),
    ('plugin-attempt-limit','PluginLookupMethods',
     '            if (owner.h >= 5) {',
     '            if (owner.h >= 6) {',
     'plugin-gate:false:false:5:0'),
    ('plugin-false-precheck','PluginLookupMethods',
     '            if (!permitted.booleanValue()) return blg.a;',
     '            if (permitted.booleanValue()) return blg.a;',
     'plugin-gate:false:false:0:1'),
    ('plugin-precheck-label','PluginLookupMethods',
     '            self.label = 1;',
     '            self.label = 0;',
     'plugin-continuation-labels-at-boundaries'),
    ('plugin-api-label','PluginLookupMethods',
     '                    self.label = 2;',
     '                    self.label = 1;',
     'plugin-sequence:0:2'),
    ('plugin-retry-original-key-index','PluginLookupMethods',
     '                    String key = (String) b.l.get(0);',
     '                    String key = (String) b.l.get(errorIndex);',
     'plugin-retry-keeps-index-zero'),
    ('plugin-status-must-be-read-twice','PluginLookupMethods',
     '                boolean badRequest = http && ((HttpException) failure).a() == 400;\n                boolean rateLimited = http && ((HttpException) failure).a() == 429;',
     '                int status = http ? ((HttpException) failure).a() : 0;\n                boolean badRequest = status == 400;\n                boolean rateLimited = status == 429;',
     'plugin-status-read-twice'),
    ('plugin-counter-reset-order','PluginLookupMethods',
     '                    ((hb9) sink).i(new d(info));\n                    self.this$0.h = 0;',
     '                    self.this$0.h = 0;\n                    ((hb9) sink).i(new d(info));',
     'plugin-counter-reset-after-publication'),
    ('plugin-catch-includes-checked-exception','PluginLookupMethods',
     '} catch (Exception apiFailure) {',
     '} catch (RuntimeException apiFailure) {',
     'plugin-fault:0:7:4'),
    ('plugin-catch-must-not-swallow-error','PluginLookupMethods',
     '} catch (Exception apiFailure) {',
     '} catch (Throwable apiFailure) {',
     'plugin-fault:0:7:3'),
    ('plugin-resume-error-index','PluginLookupMethods',
     '            errorIndex = self.I$1;',
     '            errorIndex = self.I$0;',
     'plugin-resume-index-exhausted'),
    ('plugin-retained-retry-flag','PluginLookupMethods',
     '                Throwable failure = pendingFailure;',
     '                retryFlag = 0;\n                Throwable failure = pendingFailure;',
     'plugin-resume-nonzero-flag-generic'),
    ('plugin-owner-captured-before-key','PluginLookupMethods',
     '                    b owner = self.this$0;\n                    b.k.getClass();\n                    String key = (String) b.l.get(0);',
     '                    b.k.getClass();\n                    String key = (String) b.l.get(0);\n                    b owner = self.this$0;',
     'plugin-owner-captured-before-key'),
    ('plugin-analytics-key-index','PluginLookupMethods',
     '                    ((BaseBundle) data).putInt("key_index", 0);',
     '                    ((BaseBundle) data).putInt("key_index", 1);',
     'plugin-flow:0:0:1:0'),
    ('plugin-suspension-uses-identity','PluginLookupMethods',
     '                if (pendingFailure == null && result == suspended) return suspended;',
     '                if (pendingFailure == null && result != null && result.equals(suspended)) return suspended;',
     'plugin-api-marker-identity'),
    ('upload-retain-saved-part-cast', 'PluginUploadMethods', '            MultipartBody$Part ignoredPart = (MultipartBody$Part) self.L$4;', '            Object ignoredPart = self.L$4;', 'upload-saved-cast:1:4:true'),
    ('upload-compression-result-is-ignored', 'PluginUploadMethods', '                        bitmap.compress(Bitmap$CompressFormat.PNG, 100, stream);', '                        if (!bitmap.compress(Bitmap$CompressFormat.PNG, 100, stream)) return blg.a;', 'upload-compress-false-is-ignored'),
    ('upload-nested-media-catch', 'PluginUploadMethods', '                        } catch (IllegalArgumentException invalidType) {', '                        } catch (NullPointerException invalidType) {', 'upload-nested-media-argument-handler'),
    ('upload-request-companion-capture', 'PluginUploadMethods', 'RequestBody$Companion.d(requestCompanion, mediaType, bytes, 0, 12);', 'RequestBody$Companion.d(RequestBody.Companion, mediaType, bytes, 0, 12);', 'upload-request-companion-captured-before-media'),
    ('upload-request-default-mask', 'PluginUploadMethods', 'RequestBody$Companion.d(requestCompanion, mediaType, bytes, 0, 12);', 'RequestBody$Companion.d(requestCompanion, mediaType, bytes, 0, 4);', 'upload-flow:0:true:0:0'),
    ('upload-icon-suspension-label', 'PluginUploadMethods', '                        self.label = 1;', '                        self.label = 0;', 'upload-two-suspensions'),
    ('upload-plugin-suspension-label', 'PluginUploadMethods', '                self.label = 2;', '                self.label = 1;', 'upload-two-suspensions'),
    ('upload-icon-clears-saved-part', 'PluginUploadMethods', '                        self.L$4 = null;\n                        self.label = 1;', '                        self.label = 1;', 'upload-flow:0:true:1:0'),
    ('upload-null-icon-uses-fallback', 'PluginUploadMethods', 'uploadedIcon == null ? self.$iconUrl : uploadedIcon,', 'uploadedIcon,', 'upload-null-icon-fallback'),
    ('upload-http-status-is-read-twice', 'PluginUploadMethods', '            boolean alreadyExists = failure instanceof HttpException\n                    && ((HttpException) failure).a() == 409;\n            boolean userNotAllowed = failure instanceof HttpException\n                    && ((HttpException) failure).a() == 403;', '            int status = failure instanceof HttpException ? ((HttpException) failure).a() : 0;\n            boolean alreadyExists = status == 409;\n            boolean userNotAllowed = status == 403;', 'upload-second-status-read-and-priority'),
    ('upload-denied-flag-before-publication', 'PluginUploadMethods', '                owner.i = true;\n                cne sink = owner.j;\n                ((hb9) sink).i(new g(b$c.USER_NOT_ALLOWED));', '                cne sink = owner.j;\n                ((hb9) sink).i(new g(b$c.USER_NOT_ALLOWED));\n                owner.i = true;', 'upload-no-icon:4'),
    ('upload-success-sink-before-payload', 'PluginUploadMethods', '            cne sink = self.this$0.j;\n            ((hb9) sink).i(new f(self.$name));', '            f value = new f(self.$name);\n            cne sink = self.this$0.j;\n            ((hb9) sink).i(value);', 'upload-success-sink-captured-before-payload'),
    ('upload-catch-includes-checked-exception', 'PluginUploadMethods', '        } catch (Exception failure) {', '        } catch (RuntimeException failure) {', 'upload-fault:0:1:4'),
    ('upload-catch-must-not-swallow-error', 'PluginUploadMethods', '        } catch (Exception failure) {', '        } catch (Throwable failure) {', 'upload-fault:0:1:3'),
    ('upload-error-publication-precedes-log', 'PluginUploadMethods', '                ((hb9) sink).i(new g(b$c.CONNECTION_ERROR));\n                l1g.b.getClass();\n                agd.j();', '                l1g.b.getClass();\n                agd.j();\n                ((hb9) sink).i(new g(b$c.CONNECTION_ERROR));', 'upload-no-icon:5'),
    ('upload-icon-suspension-uses-identity', 'PluginUploadMethods', '                        if (iconResult == suspended) return suspended;', '                        if (iconResult != null && iconResult.equals(suspended)) return suspended;', 'upload-icon-marker-identity'),
    ('upload-plugin-suspension-uses-identity', 'PluginUploadMethods', '                if (uploadResult == suspended) return suspended;', '                if (uploadResult != null && uploadResult.equals(suspended)) return suspended;', 'upload-plugin-marker-identity'),
]

def sha(path:Path)->str:
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def prepared_mutations():
    jobs=[]
    for name,classname,old,new,case in CONTROLS:
        source=build.ROOT/'source/java/recovered/ui'/(classname+'.java');text=source.read_text()
        count=text.count(old)
        # Retain the original first-field-only boolean control unchanged.
        if count<1 or (name!='parcel-nonzero-boolean' and count!=1):raise RuntimeError('Mutation anchor invalid: '+name)
        jobs.append({'name':name,'classname':classname,'source':source,'mutant':text.replace(old,new,1),
                     'required_cases':[case],'widget':False})
    jobs.extend(ui_mutation_catalog.load_widget_mutations(build.ROOT))
    if len(CONTROLS)!=54 or len(jobs)!=78 or len({job['name'] for job in jobs})!=78:
        raise RuntimeError('The exact 54 existing and 24 Widget fault controls are required')
    jobs.extend(ui_mutation_catalog.load_day_mutations(build.ROOT))
    if len(jobs)!=91 or len({job['name'] for job in jobs})!=91:
        raise RuntimeError('All 78 existing controls and thirteen Day numeric controls are required')
    jobs.extend(ui_mutation_catalog.load_lookup_mutations(build.ROOT))
    if len(jobs)!=101 or len({job['name'] for job in jobs})!=101:
        raise RuntimeError('All 91 existing controls and ten Day lookup controls are required')
    return jobs


def main()->None:
    host=build.WORK/'java/hostclasses'
    apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    if not host.is_dir() or not apk.is_file():raise RuntimeError('Build hybrid and run test.py --three-way first.')
    fixture=build.ROOT/'tests/fixtures/original-methods.dex'
    pins={p:sha(p) for p in [apk,fixture,*(build.ROOT/'source/java/recovered/ui').glob('*.java'),
        build.ROOT/'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',
        host/day_numeric_dex_controls.HELPER_CLASS,
        *(host/'com/arlosoft/macrodroid/variables').glob('VariableValue*.class')]}
    reference_path=build.REPORTS/'java-ui-three-path-parity.json'
    reference=json.loads(reference_path.read_text())
    registry=json.loads((build.ROOT/'source/ui-methods.json').read_text())
    keys={row['target']+'->'+row['method'] for row in registry}
    if (reference.get('passed') is not True or reference.get('paths')!=3 or reference.get('androidRuntime') is not False
            or reference.get('failedCases')!=0 or reference.get('unsupportedExecutions')!=0
            or reference.get('expectedResultFailures')!=0 or set(reference.get('methodKeys',[]))!=keys
            or reference.get('methodsCovered')!=len(keys) or reference.get('fixture_sha256')!=pins[fixture]
            or reference.get('rebuilt_apk_sha256')!=pins[apk] or reference.get('rebuilt_dex_compared_to_apk') is not True):
        raise RuntimeError('A complete current positive UI report bound to this fixture and APK is required')
    if (reference.get('dayNumericRecoveredMethods')!=1 or reference.get('dayNumericOriginalDependencyMethods')!=3
            or reference.get('dayNumericInputInventorySha256')!=ui_mutation_catalog.DAY_INPUT_INVENTORY_SHA256
            or reference.get('dayNumericInstructionAndConditionalCoverage') is not True
            or set(reference.get('dayNumericOriginalDependencyKeys',[]))!=set(day_numeric_dex_controls.GETTERS)):
        raise RuntimeError('The current numeric method and uncredited dependency coverage are required')
    reference_raw={k:v for k,v in reference.items() if k not in {
        'fixture_sha256','rebuilt_apk_sha256','rebuilt_dex_compared_to_apk'}}
    (build.REPORTS/'ui-negative-baseline.json').write_text(json.dumps(reference_raw,indent=2)+'\n')
    policy=ui_runtime_policy.verify(build.REPORTS)
    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]))
    jobs=prepared_mutations();records=[]
    result={'pass':False,'status':'RUNNING','controls':records,'expectedControlCount':91,
            'positiveBaselineSha256':sha(reference_path),'androidRuntime':False,
            'widgetCatalogSha256':ui_mutation_catalog.CATALOG_SHA256,
            'dayNumericCatalogSha256':ui_mutation_catalog.DAY_CATALOG_SHA256}
    destination=build.REPORTS/'ui-negative-controls.json'
    def save():destination.write_text(json.dumps(result,indent=2)+'\n')
    save()
    try:
        fixed=['cases','paths','methodsCovered','methodKeys','methods','instructionCoverage',
               'independentExpectedResultChecks','expectedResultFailures','unsupportedExecutions',
               'dayNumericRecoveredMethods','dayNumericOriginalDependencyMethods','dayNumericOriginalDependencyKeys',
               'dayNumericInputInventorySha256','dayNumericOriginalCoverage']
        for job in jobs:
            name,classname=job['name'],job['classname'];required=job['required_cases']
            folder=build.WORK/'negative-ui'/name;build.remove_generated_directory(folder)
            java=folder/'src/recovered/ui'/(classname+'.java');java.parent.mkdir(parents=True)
            java.write_text(job['mutant']);classes=folder/'classes';classes.mkdir()
            build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,java],name+'-negative-javac.log')
            target=classes/'recovered/ui'/(classname+'.class')
            original=host/'recovered/ui'/(classname+'.class')
            mutant_hash,original_hash=sha(target),sha(original)
            if mutant_hash==original_hash:raise RuntimeError('Mutation compiled to unchanged helper bytes: '+name)
            if job['widget'] and sorted(p.relative_to(classes).as_posix() for p in classes.rglob('*') if p.is_file())!=['recovered/ui/WidgetUpdateMethods.class']:
                raise RuntimeError('Widget mutation emitted another class')
            if job.get('day_numeric') and sorted(p.relative_to(classes).as_posix() for p in classes.rglob('*') if p.is_file())!=[day_numeric_dex_controls.HELPER_CLASS]:
                raise RuntimeError('Day numeric mutation emitted another class')
            retained=build.REPORTS/'ui-mutants'/name;retained.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(java,retained/java.name);shutil.copyfile(target,retained/target.name)
            output=folder/'result.json'
            command=[policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1000m','-Dui.report='+str(output),
                     '-cp',str(classes)+os.pathsep+cp,'UiParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
            with (build.REPORTS/(name+'-negative-run.log')).open('w') as stream:
                stream.write('COMMAND: '+json.dumps(command)+'\n');stream.flush()
                code=subprocess.run(command,cwd=build.ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
            report=json.loads(output.read_text());labels=set(report.get('failedCaseLabels',[]))
            unchanged=all(sha(p)==value for p,value in pins.items())
            inventory_matches=all(report.get(key)==reference_raw[key] for key in fixed)
            named=all(case in labels for case in required)
            passed=(code==2 and report.get('passed') is False and type(report.get('failedCases')) is int
                    and report['failedCases']>0 and report.get('unsupportedExecutions')==0
                    and report.get('paths')==3 and named and unchanged and inventory_matches)
            row={'mutation':name,'pass':passed,'failedCases':report['failedCases'],
                 'requiredCase':required[0],'requiredCases':required,'requiredCaseRejected':named,
                 'unsupportedExecutions':report['unsupportedExecutions'],'exitCode':code,
                 'sourceFixtureAndApkUnchanged':unchanged,'originalCoverageAndInventoryUnchanged':inventory_matches,
                 'mutantSourceSha256':sha(java),'mutantClassSha256':mutant_hash,'positiveClassSha256':original_hash,
                 'retainedSource':(retained/java.name).relative_to(build.ROOT).as_posix(),
                 'retainedClass':(retained/target.name).relative_to(build.ROOT).as_posix()}
            records.append(row)
            (build.REPORTS/(name+'-negative-failures.json')).write_text(json.dumps(report,indent=2)+'\n');save()
            if not passed:raise RuntimeError('Deliberate fault not correctly detected: '+json.dumps(row))
            print(name+': DETECTED',flush=True)
        positive=build.REPORTS/'ui-positive-restoration.json';positive.unlink(missing_ok=True)
        command=[policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1000m','-Dui.report='+str(positive),
                 '-cp',cp,'UiParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
        with (build.REPORTS/'ui-positive-restoration.log').open('w') as stream:
            stream.write('COMMAND: '+json.dumps(command)+'\n');stream.flush()
            code=subprocess.run(command,cwd=build.ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
        if code!=0:raise RuntimeError('Positive restoration exited unsuccessfully: '+str(code))
        good=json.loads(positive.read_text())
        if good!=reference_raw or not all(sha(p)==value for p,value in pins.items()):
            raise RuntimeError('Exact positive restoration not confirmed')
        result.update(status='ALL_91_JAVA_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED',
                      positiveRestorationPassed=True,positiveRestorationExactBaseline=True,
                      restorationCases=good['cases'],sourceFixtureAndApkUnchanged=True,controlsCount=len(records))
        save()
        numeric=day_numeric_dex_controls.run_controls(build.ROOT,records)
        result.update(dayNumericDexControlsPassed=numeric.get('passed') is True,
                      dayNumericDexControlsSha256=sha(build.REPORTS/'day-numeric-dex-controls.json'),
                      status='ALL_91_JAVA_AND_TWO_NUMERIC_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED')
        result['pass']=all(row['pass'] for row in records) and len(records)==91 and numeric.get('passed') is True
    except BaseException as error:
        result.update(status='UI_FAULT_CONTROL_FAILED',error=repr(error),controlsCount=len(records))
        raise
    finally:save()
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
