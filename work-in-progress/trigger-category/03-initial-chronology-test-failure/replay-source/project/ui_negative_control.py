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
]

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->None:
    host=build.WORK/'java/hostclasses'
    apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    if not host.is_dir() or not apk.is_file():raise RuntimeError('Build hybrid and run test.py --three-way first.')
    pins={p:sha(p) for p in [apk,build.ROOT/'tests/fixtures/original-methods.dex',*(build.ROOT/'source/java/recovered/ui').glob('*.java')]}
    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]));records=[]
    for name,classname,old,new,case in CONTROLS:
        source=build.ROOT/'source/java/recovered/ui'/(classname+'.java');text=source.read_text()
        count=text.count(old)
        # The boolean expression occurs for multiple fields: mutate only its first use.
        if count<1 or (name!='parcel-nonzero-boolean' and count!=1):raise RuntimeError('Mutation anchor invalid: '+name)
        folder=build.WORK/'negative-ui'/name;build.remove_generated_directory(folder)
        java=folder/'src/recovered/ui'/(classname+'.java');java.parent.mkdir(parents=True)
        java.write_text(text.replace(old,new,1));classes=folder/'classes';classes.mkdir()
        build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,java],name+'-negative-javac.log')
        output=folder/'result.json'
        command=['java','-Xmx1000m','-Dui.report='+str(output),'-cp',str(classes)+os.pathsep+cp,
                 'UiParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
        with (build.REPORTS/(name+'-negative-run.log')).open('w') as stream:
            code=subprocess.run(command,cwd=build.ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
        report=json.loads(output.read_text());labels=set(report.get('failedCaseLabels',[]))
        unchanged=all(sha(p)==value for p,value in pins.items())
        passed=(code==2 and report.get('passed') is False and report.get('failedCases',0)>0 and
                report.get('unsupportedExecutions')==0 and report.get('paths')==3 and case in labels and unchanged)
        record={'mutation':name,'pass':passed,'failedCases':report['failedCases'],'requiredCase':case,
                'requiredCaseRejected':case in labels,'unsupportedExecutions':report['unsupportedExecutions'],
                'exitCode':code,'sourceFixtureAndApkUnchanged':unchanged}
        records.append(record)
        (build.REPORTS/(name+'-negative-failures.json')).write_text(json.dumps(report,indent=2)+'\n')
        if not passed:raise RuntimeError('Deliberate fault not correctly detected: '+json.dumps(record))
    positive=build.REPORTS/'ui-positive-restoration.json'
    build.run(['java','-Xmx1000m','-Dui.report='+str(positive),'-cp',cp,'UiParityTests',build.ROOT,build.WORK/'hybrid'],'ui-positive-restoration.log')
    good=json.loads(positive.read_text())
    if good.get('passed') is not True or good.get('paths')!=3 or not all(sha(p)==value for p,value in pins.items()):raise RuntimeError('Positive restoration not confirmed')
    result={'pass':all(x['pass'] for x in records),'controls':records,'positiveRestorationPassed':True,
            'restorationCases':good['cases'],'androidRuntime':False,'sourceFixtureAndApkUnchanged':True}
    (build.REPORTS/'ui-negative-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
