import android.content.Context;
import android.content.Intent;
import com.arlosoft.macrodroid.action.CustomSceneAction;
import com.arlosoft.macrodroid.actionblock.data.ActionBlock;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.data.ResumeMacroInfo;
import com.arlosoft.macrodroid.events.ClearSceneByExactNameEvent;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.scene.data.*;
import com.arlosoft.macrodroid.scene.display.*;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean;
import com.google.gson.*;
import defpackage.*;
import java.util.*;
import java.util.function.Supplier;

/** Controlled dependency observations for CustomSceneAction.W, not Android rendering.
 * Every check runs the original instructions, recovered JVM method and optional rebuilt DEX.
 */
public final class SceneParityCases {
    static final String KEY=UiParityTests.PREFIX+"action/CustomSceneAction;->W(ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V";
    static final String ROOT="com.arlosoft.macrodroid.";
    static final String OVERLAY=ROOT+"scene.display.SceneOverlayDisplayService";
    static final String ACCESS=ROOT+"triggers.services.MacroDroidAccessibilityServiceJellyBean";
    static final String DIALOG=ROOT+"scene.display.SceneDialogActivity";
    static final String DISPLAY=ROOT+"scene.display.SceneDisplayActivity";
    static final String ACTION="com.arlosoft.macrodroid.triggers.services.SHOW_SCENE_OVERLAY";
    static final long GUID=0x12345678fedcba98L, ITEM=0xfedcba9876543210L;
    static final int NEXT=-71;
    static Fixture current;

    static final class Fixture {
        CustomSceneAction self=new CustomSceneAction();
        TriggerContextInfo info=new TriggerContextInfo();
        ResumeMacroInfo resume=new ResumeMacroInfo();
        Stack<Object> stack=new Stack<Object>();
        ActionBlock block=new ActionBlock(), otherBlock=new ActionBlock();
        Macro plain=new Macro();
        SceneDescription description, otherDescription;
        SceneConfig config, otherConfig;
        SceneDisplayActivity existing=new SceneDisplayActivity();
        Context alternateContext=new Context(), thirdContext=new Context();
        aj5 otherBus=new aj5();
        Object[] args;
    }
    static SceneDisplayOption option(int mode) {
        switch(mode) {case 0:return new SceneDisplayOption.Overlay(false);case 1:return new SceneDisplayOption.Overlay(true);
            case 2:return new SceneDisplayOption.Dialog();case 3:return new SceneDisplayOption.FullScreen();default:return null;}
    }
    static Object[] make(int mode,int macroKind,boolean foreground,boolean permission,int existing,boolean isTest,int nulls) {
        SceneControl.active=true;Fixture f=new Fixture();current=f;
        f.self.testId="scene-action";f.self.configured="Display scene";f.self.context.testContextId="scene-context";
        f.alternateContext.testContextId="context-alternate";f.thirdContext.testContextId="context-third";
        f.self.macroGuid=GUID;f.self.itemGuid=ITEM;
        f.block.testId="action-block";f.otherBlock.testId="other-block";f.plain.testId="plain-macro";
        f.self.macro=macroKind==0?null:macroKind==1?f.plain:f.block;
        f.config=new SceneConfig("config0","Scene Ω",option(mode));
        f.otherConfig=new SceneConfig("config1","Other scene",option(mode));
        f.description=new SceneDescription("description0",f.config);
        f.otherDescription=new SceneDescription("description1",f.otherConfig);
        f.self.sceneDescription=f.description;
        f.stack.add(Integer.MIN_VALUE);f.stack.add(null);f.stack.add(23);f.stack.add(Integer.MAX_VALUE);
        f.existing.testContextId="existing-scene";f.existing.finishing=existing==2||existing==4;f.existing.destroyed=existing==3||existing==4;
        if(existing!=0)SceneDisplayActivity.Q.put("Scene Ω",f.existing);
        MacroDroidApplication.F.u=foreground;SceneControl.overlayPermission=permission;
        f.args=new Object[]{f.self,NEXT,(nulls&1)==0?f.info:null,isTest,f.stack,(nulls&2)==0?f.resume:null};
        Object[] named={f.self,f.self.context,f.alternateContext,f.thirdContext,f.info,f.resume,f.stack,f.block,f.otherBlock,f.plain,
            f.description,f.otherDescription,f.config,f.otherConfig,f.existing,SceneControl.eventBus,f.otherBus};
        String[] ids={"action","context0","context1","context2","info","resume","stack","block","otherBlock","macro",
            "description0","description1","config0","config1","existing","bus0","bus1"};
        for(int i=0;i<named.length;i++)SceneControl.name(named[i],ids[i]);
        return f.args;
    }
    static Object[] base(int mode,boolean live,boolean warning) {return make(mode,2,!warning,!warning,live?1:0,true,0);}
    static JsonElement id(Object value) {return value==null?JsonNull.INSTANCE:new JsonPrimitive(SceneControl.id(value));}
    static JsonObject intent(Intent value) {
        JsonObject r=new JsonObject();r.addProperty("id",value.id);r.add("context",id(value.context));
        r.addProperty("target",value.target==null?null:value.target.getName());r.addProperty("action",value.action);r.addProperty("flags",value.flags);
        JsonArray extras=new JsonArray();
        for(Map.Entry<String,Object> e:value.extras.entrySet()) {
            JsonObject x=new JsonObject();x.addProperty("key",e.getKey());String type=value.extraTypes.get(e.getKey());x.addProperty("type",type);
            x.add("value",type.equals("parcelable")||type.equals("serializable")?id(e.getValue()):UiParityTests.canonical(e.getValue()));extras.add(x);
        }
        r.add("extras",extras);return r;
    }
    static JsonArray intents(List<Intent> values) {JsonArray r=new JsonArray();for(Intent i:values)r.add(intent(i));return r;}
    static JsonArray events(List<Object> values) {
        JsonArray out=new JsonArray();for(Object value:values){JsonObject e=new JsonObject();e.add("identity",id(value));e.addProperty("name",((ClearSceneByExactNameEvent)value).sceneName);out.add(e);}return out;
    }
    static JsonObject task(eld task) {
        JsonObject t=new JsonObject();t.add("identity",id(task));t.add("activity",id(task.b));t.add("info",id(task.c));t.addProperty("guid",task.d);
        t.addProperty("item",task.e);t.add("stack",id(task.f));t.addProperty("test",task.g);t.add("resume",id(task.h));t.addProperty("next",task.i);t.addProperty("kind",task.a);return t;
    }
    static void observe(Object[] args,JsonObject result) {
        JsonObject s=new JsonObject();result.add("sceneState",s);
        s.add("intents",intents(TouchControl.intents));s.add("services",intents(TouchControl.starts));s.add("activities",intents(SceneControl.activityStarts));
        s.add("createdEvents",events(SceneControl.createdEvents));s.add("postedEvents",events(SceneControl.postedEvents));
        JsonArray tasks=new JsonArray();for(eld task:SceneControl.tasks)tasks.add(task(task));s.add("tasks",tasks);
        JsonArray queued=new JsonArray();for(Runnable task:SceneControl.queuedTasks)queued.add(id(task));s.add("queuedTasks",queued);
        s.addProperty("runCalls",SceneControl.runCalls);s.addProperty("permissionReads",SceneControl.permissionReads);s.addProperty("warnings",SceneControl.permissionWarnings);
        s.addProperty("nullGuards",SceneControl.nullGuards);s.addProperty("nullGuardReturns",SceneControl.nullGuardReturns);
        s.addProperty("boundaryCalls",TouchControl.boundaryCalls);s.addProperty("logs",TouchControl.logCalls);
        if(TouchControl.logCalls>0){s.addProperty("loggedPrefix",TouchControl.loggedPrefix);s.addProperty("loggedFailureIdentity",TouchControl.loggedFailure==TouchControl.failure);}
        // VM-generated null/cast messages differ between the bounded interpreter, JVM and ART.
        // Their exception class, ordering and partial effects are still compared exactly.
        if(SceneControl.escaped!=null){boolean injected=SceneControl.escaped==TouchControl.failure;s.addProperty("escapedFailureIdentity",injected);if(injected||(!(SceneControl.escaped instanceof NullPointerException)&&!(SceneControl.escaped instanceof ClassCastException)))s.addProperty("exceptionMessage",SceneControl.escaped.getMessage());}
        if(current==null)return;
        Fixture f=current;CustomSceneAction self=f.self;
        s.addProperty("contextReads",self.contextReads);s.addProperty("macroReads",self.macroReads);s.addProperty("guidReads",self.guidReads);s.addProperty("itemReads",self.itemReads);s.addProperty("nameReads",self.nameReads);
        s.addProperty("displaying",f.block.displayingScene);s.addProperty("displayingWrites",f.block.displayingSceneWrites);
        s.addProperty("otherDisplaying",f.otherBlock.displayingScene);s.addProperty("otherDisplayingWrites",f.otherBlock.displayingSceneWrites);
        s.add("description",id(self.sceneDescription));s.add("macro",id(self.macro));s.addProperty("guid",self.macroGuid);s.addProperty("item",self.itemGuid);
        s.add("stackValues",UiParityTests.canonical(f.stack));
        s.addProperty("configReads",f.description.configReads);s.addProperty("otherConfigReads",f.otherDescription.configReads);
        s.addProperty("optionReads",f.config.optionReads);s.addProperty("otherOptionReads",f.otherConfig.optionReads);
        s.addProperty("configNameReads",f.config.nameReads);s.addProperty("otherConfigNameReads",f.otherConfig.nameReads);
        s.addProperty("finishingReads",f.existing.finishingReads);s.addProperty("destroyedReads",f.existing.destroyedReads);s.addProperty("dispatches",f.existing.dispatches);
        s.addProperty("existingFinishing",f.existing.finishing);s.addProperty("existingDestroyed",f.existing.destroyed);
        s.addProperty("applicationCompanion",MacroDroidApplication.E!=null);s.addProperty("application",MacroDroidApplication.F!=null);
        s.addProperty("overlayCompanion",SceneOverlayDisplayService.d!=null);s.addProperty("accessCompanion",MacroDroidAccessibilityServiceJellyBean.u!=null);
        s.addProperty("dialogCompanion",SceneDialogActivity.R!=null);s.addProperty("displayCompanion",SceneDisplayActivity.P!=null);s.addProperty("baseCompanion",SceneBaseActivity.D!=null);
        s.addProperty("descriptionKey",SceneBaseActivity.E);s.add("bus",id(SceneControl.eventBus));
    }
    static JsonObject expectedIntent(int mode,boolean isTest,int nulls,long guid,long item,int next,String context,String description,String key) {
        JsonObject r=new JsonObject();r.addProperty("id",0);r.addProperty("context",context);r.addProperty("target",mode==0?OVERLAY:mode==1?ACCESS:mode==2?DIALOG:DISPLAY);
        if(mode==1)r.addProperty("action",ACTION);else r.add("action",JsonNull.INSTANCE);r.addProperty("flags",mode<2?0:0x18000000);
        String[] keys=mode<2?new String[]{mode==0?"sceneDescription":"scene_description","MacroGuid","SelectableItemId","TriggerContextInfo","SkipEndifIndex","IsTest","resume_macro_info","NextActionIndex","force_not_enabled"}:
            new String[]{key,"TriggerContextInfo","MacroGuid","SelectableItemId","SkipEndifIndex","resume_macro_info","NextActionIndex","IsTest","force_not_enabled"};
        String[] types=mode<2?new String[]{"parcelable","long","long","parcelable","serializable","boolean","parcelable","int","boolean"}:
            new String[]{"parcelable","parcelable","long","long","serializable","parcelable","int","boolean","boolean"};
        Object info=(nulls&1)==0?"info":null,resume=(nulls&2)==0?"resume":null;
        Object[] values=mode<2?new Object[]{description,guid,item,info,"stack",isTest,resume,next,false}:
            new Object[]{description,info,guid,item,"stack",resume,next,isTest,false};
        JsonArray extras=new JsonArray();for(int i=0;i<keys.length;i++){JsonObject e=new JsonObject();e.addProperty("key",keys[i]);e.addProperty("type",types[i]);e.add("value",UiParityTests.canonical(values[i]));extras.add(e);}r.add("extras",extras);return r;
    }
    static JsonObject expected(int mode,int macroKind,boolean foreground,boolean permission,int existing,boolean isTest,int nulls,long guid,long item,int next) {
        boolean overlay=mode<2,warning=!overlay&&!foreground&&!permission,live=!overlay&&existing==1;
        JsonObject r=new JsonObject(),s=new JsonObject();r.add("value",JsonNull.INSTANCE);r.add("sceneState",s);
        s.addProperty("macroReads",macroKind==2?2:1);s.addProperty("displaying",macroKind==2);s.addProperty("displayingWrites",macroKind==2?1:0);
        s.addProperty("contextReads",overlay?1:1+(foreground?0:1)+(warning?1:0));s.addProperty("guidReads",warning?2:1);s.addProperty("itemReads",1);s.addProperty("nameReads",warning?1:0);
        s.addProperty("permissionReads",!overlay&&!foreground?1:0);s.addProperty("warnings",warning?1:0);s.addProperty("logs",0);s.addProperty("runCalls",0);s.addProperty("nullGuards",0);
        s.addProperty("optionReads",2);s.addProperty("configReads",overlay?2:(live?3:4)+(warning?1:0));s.addProperty("configNameReads",overlay?0:(live?1:2)+(warning?1:0));
        s.addProperty("finishingReads",!overlay&&existing!=0?1:0);s.addProperty("destroyedReads",!overlay&&(existing==1||existing==3)?1:0);s.addProperty("dispatches",live?1:0);
        JsonArray intents=new JsonArray(),services=new JsonArray(),activities=new JsonArray(),events=new JsonArray(),tasks=new JsonArray(),queued=new JsonArray();
        if(live) {
            JsonObject t=new JsonObject();t.addProperty("identity","task0");t.addProperty("activity","existing");t.add("info",UiParityTests.canonical((nulls&1)==0?"info":null));
            t.addProperty("guid",guid);t.addProperty("item",item);t.addProperty("stack","stack");t.addProperty("test",isTest);t.add("resume",UiParityTests.canonical((nulls&2)==0?"resume":null));t.addProperty("next",next);t.addProperty("kind",mode==2?0:1);tasks.add(t);queued.add("task0");
        } else {
            JsonObject i=expectedIntent(mode,isTest,nulls,guid,item,next,"context0","description0","scene_description");intents.add(i);if(overlay)services.add(i);else activities.add(i);
            if(!overlay){JsonObject e=new JsonObject();e.addProperty("identity","event0");e.addProperty("name","Scene Ω");events.add(e);}
        }
        s.add("intents",intents);s.add("services",services);s.add("activities",activities);s.add("createdEvents",events);s.add("postedEvents",events);s.add("tasks",tasks);s.add("queuedTasks",queued);
        return r;
    }
    static void check(String label,Supplier<Object[]> make,JsonObject expected) {UiParityTests.check(KEY,label,make,UiParityTests.UNKNOWN,false,expected);}
    static JsonObject exception(Class<?> type) {return UiParityTests.exceptionExpected(type);}
    static List<String> boundaries(Supplier<Object[]> make) {
        JsonObject result=UiParityTests.outcome(KEY,"original",make,false);
        if(result.has("exception")||result.has("unsupported"))throw new AssertionError("Invalid clean scene boundary discovery "+result);
        return new ArrayList<String>(TouchControl.boundaries);
    }
    static int boundary(List<String> calls,String prefix) {return UiParityTests.boundary(calls,prefix);}

    static void combinations() {
        for(int mode=0;mode<5;mode++)for(int macro=0;macro<3;macro++)for(boolean foreground:new boolean[]{false,true})for(boolean permission:new boolean[]{false,true})
            for(int existing=0;existing<5;existing++)for(boolean isTest:new boolean[]{false,true})for(int nulls=0;nulls<4;nulls++) {
            final int m=mode,k=macro,e=existing,n=nulls;
            check("scene:"+m+":"+k+":"+foreground+":"+permission+":"+e+":"+isTest+":"+n,
                ()->make(m,k,foreground,permission,e,isTest,n),expected(m,k,foreground,permission,e,isTest,n,GUID,ITEM,NEXT));
        }
        long[] longs={Long.MIN_VALUE,-0x100000001L,-1,0,1,0x100000001L,Long.MAX_VALUE};
        int[] indexes={Integer.MIN_VALUE,-1,0,1,Integer.MAX_VALUE};
        for(int mode=0;mode<4;mode++)for(boolean live:new boolean[]{false,true})for(long guid:longs)for(int next:indexes) {
            final int m=mode;long item=~guid;
            check("scene-numeric:"+m+":"+live+":"+guid+":"+next,()->{Object[] a=base(m,live,false);current.self.macroGuid=guid;current.self.itemGuid=item;a[1]=next;return a;},
                expected(m,2,true,true,live?1:0,true,0,guid,item,next));
        }
        for(int mode=0;mode<2;mode++)for(boolean nil:new boolean[]{false,true}){
            final int m=mode;check("scene-ignored-service-result:"+m+":"+nil,()->{Object[] a=base(m,false,false);TouchControl.startReturnsNull=nil;return a;},expected(m,2,true,true,0,true,0,GUID,ITEM,NEXT));
        }
        check("scene-null-self",()->{current=null;SceneControl.active=true;return new Object[]{null,NEXT,null,true,null,null};},exception(NullPointerException.class));
    }
    static void failures() {
        int[] modes={0,1,2,2,3,3,2,3,3};boolean[] liveProfiles={false,false,false,true,false,true,false,true,false},warnings={false,false,false,false,false,false,true,true,false};
        String[] names={"overlay","accessibility","dialog-new","dialog-live","display-new","display-live","warning-new","warning-live","permission-allowed"};
        for(int p=0;p<modes.length;p++) {
            final int atProfile=p,mode=modes[p];Supplier<Object[]> make=()->{Object[] a=base(mode,liveProfiles[atProfile],warnings[atProfile]);if(atProfile==8)MacroDroidApplication.F.u=false;return a;};
            List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int kind=0;kind<5;kind++) {
                final int n=at,k=kind;String call=calls.get(at);boolean caught=mode==1&&kind!=3&&(call.startsWith("intent.")||call.startsWith("service.start:"));
                JsonObject expected=caught?new JsonObject():exception(UiParityTests.blockFailure(k).getClass());JsonObject state=new JsonObject();expected.add("sceneState",state);
                state.addProperty("logs",caught?1:0);if(caught){expected.add("value",JsonNull.INSTANCE);state.addProperty("loggedFailureIdentity",true);state.addProperty("loggedPrefix","Could not show scene overlay: ");}else state.addProperty("escapedFailureIdentity",true);
                check("scene-fault:"+names[p]+":"+n+":"+k,()->{Object[] a=make.get();TouchControl.failAt=n;TouchControl.failure=UiParityTests.blockFailure(k);return a;},expected);
            }
        }
        for(int mode=0;mode<5;mode++)for(int missing=0;missing<10;missing++) {
            final int m=mode,n=missing;
            boolean required=n==0||n==1||n==2||(n==3&&m==0)||(n==4&&m==1)||(n>=5&&n<=7&&m>=2)||(n==8&&m==2)||(n==9&&m>=2);
            check("scene-null-boundary:"+m+":"+n,()->{
                Object[] a=base(m,false,false);
                switch(n){case 0:current.self.context=null;break;case 1:current.self.macroGuid=null;break;case 2:a[4]=null;break;
                    case 3:SceneOverlayDisplayService.d=null;break;case 4:MacroDroidAccessibilityServiceJellyBean.u=null;break;
                    case 5:MacroDroidApplication.E=null;break;case 6:MacroDroidApplication.F=null;break;case 7:SceneDisplayActivity.P=null;break;case 8:SceneDialogActivity.R=null;break;case 9:SceneBaseActivity.D=null;break;}
                return a;
            },required?exception(NullPointerException.class):expected(m,2,true,true,0,true,0,GUID,ITEM,NEXT));
        }
        for(int mode:new int[]{2,3})for(boolean live:new boolean[]{false,true})for(int bad=0;bad<3;bad++) {
            final int b=bad;
            boolean fail=b<2||!live;
            check("scene-bad-map-bus:"+mode+":"+live+":"+b,()->{Object[] a=base(mode,live,false);if(b==0)SceneDisplayActivity.Q=null;else if(b==1)SceneDisplayActivity.Q.put("Scene Ω","wrong activity");else SceneControl.eventBus=null;return a;},
                fail?exception(b==1?ClassCastException.class:NullPointerException.class):expected(mode,2,true,true,1,true,0,GUID,ITEM,NEXT));
        }
        Supplier<Object[]> access=()->base(1,false,false);int start=boundary(boundaries(access),"service.start:");
        check("scene-error-logger-fails",()->{Object[] a=access.get();TouchControl.failAt=start;TouchControl.failure=new java.io.IOException("fixture start");TouchControl.mutateAt=start+1;TouchControl.mutation=()->{throw new AssertionError("fixture logger");};return a;},exception(AssertionError.class));
    }
    static void nullDescriptions() {
        int[] modes={0,0,0,1,2,2,2,3};
        String[] sites={null,"scene.option:config0:0","scene.overlayDraw:","scene.overlayDraw:","scene.permission:","scene.permissionWarning:","scene.item:","scene.item:"};
        for(int guard=0;guard<modes.length;guard++)for(boolean helperReturns:new boolean[]{false,true}) {
            final int g=guard;Supplier<Object[]> make=()->base(modes[g],false,g==4||g==5);
            int at=sites[g]==null?-1:boundary(boundaries(make),sites[g]);
            check("scene-null-description:"+g+":"+helperReturns,()->{Object[] a=make.get();SceneControl.nullGuardReturns=helperReturns;if(at<0)current.self.sceneDescription=null;else{Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->f.self.sceneDescription=null;}return a;},
                exception(helperReturns?NullPointerException.class:kotlin.UninitializedPropertyAccessException.class));
        }
        for(int mode=0;mode<5;mode++)for(int at=0;at<5;at++) {
            final int m=mode,index=at;Supplier<Object[]> make=()->base(m,false,false);List<String> calls=boundaries(make);List<Integer> reads=new ArrayList<Integer>();for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith("scene.config:description0:"))reads.add(i);
            if(index>=reads.size())continue;int boundary=reads.get(index);
            check("scene-null-config:"+m+":"+index,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=boundary;TouchControl.mutation=()->f.description.sceneConfig=null;return a;},exception(NullPointerException.class));
        }
        for(int first=0;first<5;first++)for(int second=0;second<5;second++) {
            final int x=first,y=second;
            JsonObject expected=x<2&&y>=2?exception(y==4?NullPointerException.class:ClassCastException.class):new JsonObject();if(!(x<2&&y>=2))expected.add("value",JsonNull.INSTANCE);
            check("scene-option-reread:"+x+":"+y,()->{Object[] a=base(x,false,false);current.config.options=new SceneDisplayOption[]{option(x),option(y)};return a;},expected);
        }
    }
    static void dependencyChanges() {
        for(int second=0;second<3;second++) {
            final int s=second;JsonObject expected=s==2?new JsonObject():exception(s==0?NullPointerException.class:ClassCastException.class);if(s==2)expected.add("value",JsonNull.INSTANCE);
            check("scene-macro-reread:"+s,()->{Object[] a=base(0,false,false);current.self.macroSequence=new Macro[]{current.block,s==0?null:s==1?current.plain:current.otherBlock};return a;},expected);
        }
        for(int mode=0;mode<4;mode++)for(boolean warning:new boolean[]{false,true}) {
            final int m=mode;
            check("scene-context-reread:"+m+":"+warning,()->{Object[] a=base(m,false,warning);Fixture f=current;f.self.contextSequence=new Context[]{f.self.context,f.alternateContext,f.thirdContext};f.self.guidSequence=new Long[]{GUID,~GUID};return a;},null);
        }
        for(int mode=0;mode<4;mode++) {
            final int m=mode;Supplier<Object[]> make=()->base(m,false,false);int at=boundary(boundaries(make),"scene.context:");
            check("scene-description-after-context:"+m,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->f.self.sceneDescription=f.otherDescription;return a;},null);
        }
        for(int mode=0;mode<4;mode++)for(int site=0;site<4;site++) {
            final int m=mode,w=site;Supplier<Object[]> make=()->base(m,false,false);List<String> calls=boundaries(make);
            int at=boundary(calls,w==0?"scene.guid:":w==1?"scene.item:":w==2?"intent.new:":m<2?"service.start:":"eventBus.get");
            check("scene-description-snapshot:"+m+":"+w,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->f.self.sceneDescription=f.otherDescription;return a;},null);
        }
        for(int mode=0;mode<4;mode++)for(boolean initialNull:new boolean[]{false,true}) {
            final int m=mode;Supplier<Object[]> make=()->base(m,false,false);int at=boundary(boundaries(make),"scene.context:");
            check("scene-companion-capture:"+m+":"+initialNull,()->{
                Object[] a=make.get();setCompanion(m,!initialNull);TouchControl.mutateAt=at;TouchControl.mutation=()->setCompanion(m,initialNull);return a;
            },initialNull?exception(NullPointerException.class):expected(m,2,true,true,0,true,0,GUID,ITEM,NEXT));
        }
        for(int mode:new int[]{2,3})for(boolean live:new boolean[]{false,true})for(int site=0;site<3;site++) {
            final int s=site;Supplier<Object[]> make=()->base(mode,live,false);List<String> calls=boundaries(make);
            int at=boundary(calls,s==0?"scene.configName:config0:0":s==1?"scene.map.get:":live?"activity.finishing:":"intent.new:");
            check("scene-name-liveness-change:"+mode+":"+live+":"+s,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->{f.config.name="renamed";f.existing.destroyed=true;};return a;},null);
        }
        for(int mode:new int[]{2,3})for(int site=0;site<3;site++)for(boolean nullKey:new boolean[]{false,true}) {
            final int s=site;Supplier<Object[]> make=()->base(mode,false,false);List<String> calls=boundaries(make);
            int at=boundary(calls,s==0?"intent.new:":s==1?"intent.parcelable:0:":"eventBus.get");
            check("scene-dynamic-key-bus:"+mode+":"+s+":"+nullKey,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->{SceneBaseActivity.E=nullKey?null:"dynamic_description";SceneControl.eventBus=f.otherBus;};return a;},null);
        }
        for(int mode:new int[]{2,3})for(boolean live:new boolean[]{false,true})for(int nulled=0;nulled<3;nulled++) {
            final int n=nulled;Supplier<Object[]> make=()->base(mode,live,false);List<String> calls=boundaries(make);
            int at=boundary(calls,n==0?"scene.configName:config0:0":n==1?"scene.map.get:":live?"activity.runOnUiThread:":"scene.configName:config0:1");
            check("scene-null-name:"+mode+":"+live+":"+n,()->{Object[] a=make.get();Fixture f=current;TouchControl.mutateAt=at;TouchControl.mutation=()->f.config.name=null;return a;},n==0||n==2&&!live?exception(NullPointerException.class):null);
        }
    }
    static void setCompanion(int mode,boolean present) {
        if(mode==0)SceneOverlayDisplayService.d=present?new SceneOverlayDisplayService.a():null;
        else if(mode==1)MacroDroidAccessibilityServiceJellyBean.u=present?new MacroDroidAccessibilityServiceJellyBean.a():null;
        else if(mode==2)SceneDialogActivity.R=present?new SceneDialogActivity.a():null;
        else SceneDisplayActivity.P=present?new SceneDisplayActivity.a():null;
    }
    static void run() {combinations();failures();nullDescriptions();dependencyChanges();}
}
