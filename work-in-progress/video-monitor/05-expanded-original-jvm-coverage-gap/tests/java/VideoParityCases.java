import com.arlosoft.macrodroid.action.services.BaseVideoRecordingService;
import com.arlosoft.macrodroid.action.services.a;
import com.google.gson.*;
import defpackage.*;
import java.io.IOException;
import java.util.*;
import java.util.function.Supplier;

/** Original and recovered video-monitor body with bounded host-only dependencies. */
public final class VideoParityCases {
    static final String KEY=UiParityTests.PREFIX+"action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;";
    static final long MB=1048576L;
    static Fixture current;
    static String caseLabel="discovery",executionPath;
    static int discoveryExecutions;
    static final List<JsonObject> generatedEscapedMessages=new ArrayList<JsonObject>();

    static final class EqualSuspended {
        int equalsCalls;
        @Override public boolean equals(Object other){equalsCalls++;VideoControl.hit("marker.equals:"+VideoControl.id(other));return other==v93.COROUTINE_SUSPENDED;}
        @Override public int hashCode(){return 37;}
    }
    static final class ObservedFailure extends IOException {
        final String text;
        int messageReads;
        Throwable messageFailure;
        ObservedFailure(String text){super(text);this.text=text;}
        @Override public String getMessage(){
            messageReads++;VideoControl.hit("exception.message:"+VideoControl.id(this));
            if(messageFailure!=null)VideoControl.raise(messageFailure);
            return text;
        }
    }
    static final class Fixture {
        final a self=new a();
        final BaseVideoRecordingService owner=new BaseVideoRecordingService(),other=new BaseVideoRecordingService();
        final VideoFile file=new VideoFile("file"),directory=new VideoFile("directory"),otherFile=new VideoFile("otherFile"),otherDirectory=new VideoFile("otherDirectory");
        final qnc flag=new qnc();
        final android.os.ParcelFileDescriptor descriptor=new android.os.ParcelFileDescriptor();
        final EqualSuspended equal=new EqualSuspended();
        final List<Throwable> externalErrors=new ArrayList<Throwable>();
        final List<ObservedFailure> observedFailures=new ArrayList<ObservedFailure>();
        final List<Object> resumeInputs=new ArrayList<Object>();
        final List<Runnable> resumeChanges=new ArrayList<Runnable>();
        final List<String> steps=new ArrayList<String>();
        Object argumentSelf,input=blg.a;
        Fixture(int label,int profile){
            current=this;VideoControl.current=self;
            VideoControl.name(self,"continuation");VideoControl.name(owner,"owner");VideoControl.name(other,"other");
            VideoControl.name(flag,"savedFlag");VideoControl.name(descriptor,"descriptor");VideoControl.name(equal,"equalSuspended");
            VideoControl.owners.add(owner);VideoControl.owners.add(other);
            self.label=label;self.this$0=owner;self.L$0=flag;self.L$1=file;flag.element=true;
            argumentSelf=self;
            owner.s=73;owner.t=file;owner.v=1024;owner.w=1;owner.x=0;owner.available=256*MB;owner.videoExternalFilesDir=directory;
            other.s=109;other.t=otherFile;other.v=17;other.w=6;other.x=401*MB;other.available=512*MB;other.videoExternalFilesDir=otherDirectory;
            file.parent=directory;file.lengthValue=2048;otherFile.parent=otherDirectory;otherFile.lengthValue=8192;
            BaseVideoRecordingService.B=true;
            switch(profile){
                case 0:break;
                case 1:owner.available=128*MB-1;break;
                case 2:file.lengthValue=1024;owner.w=2;break;
                case 3:owner.t=null;owner.videoExternalFilesDir=null;owner.v=0;break;
                case 4:owner.t=null;owner.u=descriptor;owner.videoExternalFilesDir=null;break;
                case 5:file.parent=null;owner.videoExternalFilesDir=null;break;
                case 6:file.present=false;break;
                case 7:file.existsResults.add(new g3d(observed("exists failed")));break;
                case 8:owner.availableResults.add(new g3d(observed("available failed")));break;
                default:throw new AssertionError(profile);
            }
            VideoControl.active=true;
        }
        <T extends Throwable>T error(T value){VideoControl.name(value,"error"+externalErrors.size());externalErrors.add(value);return value;}
        ObservedFailure observed(String text){ObservedFailure value=error(new ObservedFailure(text));observedFailures.add(value);return value;}
        Object response(int code){
            switch(code){
                case 0:return blg.a;
                case 1:return v93.COROUTINE_SUSPENDED;
                case 2:return null;
                case 3:return new g3d(observed("scripted checked failure"));
                case 4:return new g3d(error(new AssertionError("scripted Error")));
                case 5:return equal;
                case 6:return error(new IOException("returned exception object"));
                default:throw new AssertionError(code);
            }
        }
        Object[] args(){return new Object[]{argumentSelf,input};}
    }
    static Object execute(String path,Object[] args)throws Throwable {
        executionPath=path;Object value;
        try{value=UiParityTests.call(KEY,path,args);step(value,null);}catch(Throwable failure){step(null,failure);throw failure;}
        if(current!=null)for(int index=0;index<current.resumeInputs.size();index++){
            if(value!=v93.COROUTINE_SUSPENDED)throw new AssertionError("Script attempted to resume a completed video call");
            if(index<current.resumeChanges.size()&&current.resumeChanges.get(index)!=null)current.resumeChanges.get(index).run();
            try{value=UiParityTests.call(KEY,path,new Object[]{current.argumentSelf,current.resumeInputs.get(index)});step(value,null);}
            catch(Throwable failure){step(null,failure);throw failure;}
        }
        return value;
    }
    static void step(Object value,Throwable failure){if(current!=null)current.steps.add((failure==null?"return:"+VideoControl.id(value):"throw:"+failure.getClass().getName())+":"+VideoControl.state(current.self));}
    static JsonElement id(Object value){return value==null?JsonNull.INSTANCE:new JsonPrimitive(VideoControl.id(value));}
    static void observe(Object[] args,JsonObject result){
        JsonObject out=new JsonObject();result.add("videoState",out);
        out.addProperty("resultKind",VideoControl.escaped==null?"return":"throw");out.add("returned",id(VideoControl.returned));
        out.addProperty("returnedUnitIdentity",VideoControl.escaped==null&&VideoControl.returned==blg.a);
        out.addProperty("returnedSuspendedIdentity",VideoControl.escaped==null&&VideoControl.returned==v93.COROUTINE_SUSPENDED);
        out.add("boundaries",UiParityTests.canonical(VideoControl.boundaries));out.add("boundaryStates",UiParityTests.canonical(VideoControl.states));
        out.addProperty("boundaryCalls",VideoControl.boundaryCalls);out.addProperty("recording",BaseVideoRecordingService.B);
        out.addProperty("state",VideoControl.state(VideoControl.current));
        if(VideoControl.current!=null){out.addProperty("label",VideoControl.current.label);out.add("saved0",id(VideoControl.current.L$0));out.add("saved1",id(VideoControl.current.L$1));out.add("owner",id(VideoControl.current.this$0));}
        JsonObject owners=new JsonObject();
        for(BaseVideoRecordingService owner:VideoControl.owners){
            JsonObject state=new JsonObject();state.addProperty("id",owner.s);state.addProperty("v",owner.v);state.addProperty("w",owner.w);state.addProperty("x",owner.x);
            state.add("file",id(owner.t));state.add("descriptor",id(owner.u));state.addProperty("spaceReads",owner.availableReads);state.addProperty("directoryReads",owner.videoDirectoryReads);owners.add(VideoControl.id(owner),state);
        }
        out.add("owners",owners);
        JsonObject files=new JsonObject();for(VideoFile file:VideoControl.files){JsonObject state=new JsonObject();state.addProperty("parentReads",file.parentReads);state.addProperty("existsReads",file.existsReads);state.addProperty("lengthReads",file.lengthReads);files.add(VideoControl.id(file),state);}out.add("files",files);
        JsonArray delays=new JsonArray();for(VideoControl.DelayCall call:VideoControl.delays){JsonObject item=new JsonObject();item.addProperty("milliseconds",call.milliseconds);item.add("continuation",id(call.continuation));item.addProperty("state",call.state);delays.add(item);}out.add("delays",delays);out.addProperty("delayCount",VideoControl.delayReads);
        JsonArray callbacks=new JsonArray();for(d31 callback:VideoControl.callbacks){JsonObject item=new JsonObject();item.add("identity",id(callback));item.add("owner",id(callback.this$0));item.add("completion",id(callback.completion));item.addProperty("arity",callback.widgetArity);callbacks.add(item);}out.add("callbacks",callbacks);out.addProperty("callbackCount",VideoControl.callbacks.size());
        JsonArray dispatches=new JsonArray();for(VideoControl.DispatchCall call:VideoControl.dispatches){JsonObject item=new JsonObject();item.add("dispatcher",id(call.dispatcher));item.add("callback",id(call.callback));item.add("continuation",id(call.continuation));item.addProperty("state",call.state);dispatches.add(item);}out.add("dispatches",dispatches);out.addProperty("dispatchCount",VideoControl.dispatchReads);
        if(current!=null){
            out.add("steps",UiParityTests.canonical(current.steps));out.addProperty("equalsCalls",current.equal.equalsCalls);
            JsonArray reads=new JsonArray();for(ObservedFailure failure:current.observedFailures){JsonObject item=new JsonObject();item.add("identity",id(failure));item.addProperty("reads",failure.messageReads);reads.add(item);}out.add("exceptionMessageReads",reads);
        }
        Throwable escaped=VideoControl.escaped;
        if(escaped!=null){
            boolean external=escaped==VideoControl.failure||VideoControl.failures.containsValue(escaped)||current!=null&&current.externalErrors.contains(escaped);
            out.addProperty("escapedInjectedIdentity",escaped==VideoControl.failure);out.addProperty("escapedExternalIdentity",external);
            if(external){out.add("escaped",id(escaped));out.addProperty("exceptionMessage",escaped instanceof ObservedFailure?((ObservedFailure)escaped).text:escaped.getMessage());}
            else if(escaped instanceof NullPointerException||escaped instanceof ClassCastException){
                out.addProperty("vmGeneratedEscapedMessageExcluded",true);
                JsonObject raw=new JsonObject();raw.addProperty("case",caseLabel);raw.addProperty("path",executionPath);raw.addProperty("exception",escaped.getClass().getName());raw.addProperty("rawMessage",escaped.getMessage());generatedEscapedMessages.add(raw);
            }else out.addProperty("exceptionMessage",escaped.getMessage());
        }
    }
    static JsonObject expected(Object... pairs){JsonObject result=new JsonObject(),state=new JsonObject();for(int i=0;i<pairs.length;i+=2)state.add((String)pairs[i],UiParityTests.canonical(pairs[i+1]));result.add("videoState",state);return result;}
    static JsonObject exception(Class<?> type){JsonObject result=new JsonObject();result.addProperty("exception",type.getName());return result;}
    static void check(String label,Supplier<Object[]> make,JsonObject expected){caseLabel=label;UiParityTests.check(KEY,label,make,UiParityTests.UNKNOWN,false,expected);}
    static List<String> discover(Supplier<Object[]> make){
        caseLabel="boundary-discovery";JsonObject value=UiParityTests.outcome(KEY,"original",make,false);discoveryExecutions++;
        if(value.has("exception")||value.has("unsupported"))throw new AssertionError("Invalid boundary profile: "+value);
        return new ArrayList<String>(VideoControl.boundaries);
    }
    static int boundary(List<String> calls,String prefix){for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith(prefix))return i;throw new AssertionError("Missing "+prefix+" in "+calls);}

    static void entryCases(){
        for(int label:new int[]{0,1,2,3,-1,4,Integer.MIN_VALUE,Integer.MAX_VALUE})for(boolean active:new boolean[]{false,true})for(int response=0;response<7;response++){
            final int r=response;check("video-entry:"+label+":"+active+":"+r,()->{Fixture f=new Fixture(label,0);BaseVideoRecordingService.B=active;f.input=f.response(r);return f.args();},null);
        }
        check("video-invalid-guard-returns-injected",()->{Fixture f=new Fixture(19,0);VideoControl.invalidLabelReturns=true;return f.args();},expected("returned",null,"label",19,"callbackCount",0,"delayCount",0));
        for(int label:new int[]{0,1,2,3})check("video-inactive-label:"+label,()->{Fixture f=new Fixture(label,0);BaseVideoRecordingService.B=false;return f.args();},expected("returned",label==0?"suspended":"unit","label",label==0?1:label,"delayCount",label==0?1:0));
        for(int left=0;left<4;left++)for(int right=0;right<4;right++){
            final int l=left,r=right;check("video-dead-casts:"+l+":"+r,()->{Fixture f=new Fixture(2,0);f.self.L$0=l==0?null:l==1?f.flag:l==2?f.file:"bad-flag";f.self.L$1=r==0?null:r==1?f.file:r==2?f.flag:"bad-file";return f.args();},l<2&&r<2?expected("returned","unit","label",2,"boundaryCalls",1):exception(ClassCastException.class));
        }
    }
    static void ordinaryCases(){
        for(int profile=0;profile<9;profile++)for(int label:new int[]{1,3}){
            final int p=profile;check("video-profile:"+p+":"+label,()->new Fixture(label,p).args(),null);
        }
        for(long space:new long[]{Long.MIN_VALUE,-1,0,128*MB-1,128*MB,128*MB+1,256*MB,Long.MAX_VALUE})
            for(long previous:new long[]{Long.MIN_VALUE,-1,0,1,100*MB-1,100*MB,356*MB-1,356*MB,356*MB+1,Long.MAX_VALUE}){
                check("video-space:"+space+":"+previous,()->{Fixture f=new Fixture(1,0);f.owner.available=space;f.owner.x=previous;return f.args();},expected("returned",space<128*MB?"unit":"suspended","label",space<128*MB?2:3,"dispatchCount",space<128*MB?1:0));
            }
        for(long size:new long[]{Long.MIN_VALUE,-1,0,1,1023,1024,1025,2048,Long.MAX_VALUE})
            for(long previous:new long[]{-1,0,1,1024,2048,Long.MAX_VALUE})for(int counter:new int[]{Integer.MIN_VALUE,-1,0,1,2,3,Integer.MAX_VALUE}){
                check("video-size:"+size+":"+previous+":"+counter,()->{Fixture f=new Fixture(1,0);f.file.lengthValue=size;f.owner.v=previous;f.owner.w=counter;return f.args();},null);
            }
        for(int delay=0;delay<7;delay++)for(int label:new int[]{0,1,3}){
            final int d=delay;check("video-delay-result:"+label+":"+d,()->{Fixture f=new Fixture(label,0);VideoControl.delayResults.add(f.response(d));return f.args();},d==3||d==4?null:expected("returned","suspended","equalsCalls",0));
        }
        for(int response=0;response<7;response++){
            final int r=response;check("video-dispatch-result:"+r,()->{Fixture f=new Fixture(1,1);VideoControl.dispatchResults.add(f.response(r));return f.args();},r==3||r==4?null:expected("returned",r==1?"suspended":"unit","label",2,"saved0",null,"saved1",null,"equalsCalls",0));
        }
    }
    static void faultCases(){
        for(int profile:new int[]{0,1,2,4,7,8}){
            final int p=profile;Supplier<Object[]> make=()->new Fixture(1,p).args();List<String> calls=discover(make);
            for(int at=0;at<calls.size();at++)for(int type=0;type<4;type++){
                final int index=at,t=type;check("video-fault:"+p+":"+index+":"+t,()->{Object[] args=make.get();VideoControl.failAt=index;
                    Throwable fault=t==0?current.observed("injected checked"):t==1?current.error(new AssertionError("injected Error")):t==2?current.error(new NullPointerException("injected exact null message")):current.error(new IllegalStateException("injected exact state message"));
                    VideoControl.failure=fault;return args;},null);
            }
        }
        for(int response=3;response<=4;response++){
            final int r=response;check("video-label-two-resume-failure:"+r,()->{Fixture f=new Fixture(2,0);f.input=f.response(r);return f.args();},r==3?expected("returned","suspended","label",3):exception(AssertionError.class));
        }
    }
    static void mutationCases(){
        for(int profile:new int[]{0,1,2,7,8}){
            final int p=profile;Supplier<Object[]> make=()->new Fixture(1,p).args();List<String> calls=discover(make);
            for(int at=0;at<calls.size();at++)for(int change=0;change<4;change++){
                final int index=at,c=change;check("video-mutation:"+p+":"+index+":"+c,()->{Object[] args=make.get();Fixture f=current;VideoControl.mutateAt=index;
                    VideoControl.mutation=()->{if(c==0)f.self.this$0=f.other;else if(c==1)f.owner.t=f.otherFile;else if(c==2){f.owner.w=7;f.owner.v=17;f.owner.s=997;f.owner.x=999*MB;}else BaseVideoRecordingService.B=false;};return args;},null);
            }
        }
        check("video-three-stage-resume",()->{Fixture f=new Fixture(0,0);f.resumeInputs.add(blg.a);f.resumeInputs.add(blg.a);f.resumeChanges.add(null);f.resumeChanges.add(()->BaseVideoRecordingService.B=false);return f.args();},expected("returned","unit","label",3,"delayCount",2,"dispatchCount",0));
        check("video-stop-then-resume",()->{Fixture f=new Fixture(1,1);VideoControl.dispatchResults.add(v93.COROUTINE_SUSPENDED);f.resumeInputs.add(blg.a);return f.args();},expected("returned","unit","label",2,"delayCount",0,"dispatchCount",1));
        check("video-repeat-delay-outside-catch",()->{Fixture f=new Fixture(1,0);VideoControl.delayResults.add(new g3d(f.observed("repeat delay failure")));return f.args();},exception(ObservedFailure.class));
    }
    static JsonObject ownerExpected(long size,int counter,long available){
        JsonObject result=new JsonObject(),state=new JsonObject(),owners=new JsonObject(),owner=new JsonObject();
        owner.addProperty("v",size);owner.addProperty("w",counter);owner.addProperty("x",available);
        owners.add("owner",owner);state.add("owners",owners);result.add("videoState",state);return result;
    }
    static void numericContracts(){
        long[][] rows={
            {-1,1024,1,1024,1,0},{Long.MIN_VALUE,17,Integer.MIN_VALUE,17,Integer.MIN_VALUE,0},
            {0,0,7,0,7,0},{1024,-1,7,1024,7,0},{2048,1024,7,2048,0,0},
            {1024,1024,1,1024,2,0},{1024,1024,2,1024,3,1},{1,1024,2,1,3,1},
            {1024,1024,Integer.MAX_VALUE,1024,Integer.MIN_VALUE,0},
            {1024,1024,Integer.MAX_VALUE-1,1024,Integer.MAX_VALUE,1},
            {1024,1024,Integer.MIN_VALUE,1024,Integer.MIN_VALUE+1,0},
            {Long.MAX_VALUE,1,5,Long.MAX_VALUE,0,0},{0,Long.MAX_VALUE,0,0,1,0}
        };
        for(int index=0;index<rows.length;index++){
            long[] row=rows[index];JsonObject expected=ownerExpected(row[3],(int)row[4],256*MB);
            expected.getAsJsonObject("videoState").addProperty("returned",row[5]==1?"unit":"suspended");
            expected.getAsJsonObject("videoState").addProperty("dispatchCount",row[5]);
            check("video-numeric-contract:"+index,()->{Fixture f=new Fixture(1,0);f.file.lengthValue=row[0];f.owner.v=row[1];f.owner.w=(int)row[2];return f.args();},expected);
        }
        for(long delta:new long[]{-1,0,1}){
            long space=256*MB+delta;long expectedX=delta<0?space:356*MB;
            check("video-exact-storage-report-threshold:"+delta,()->{Fixture f=new Fixture(1,0);f.owner.x=356*MB;f.owner.available=space;return f.args();},ownerExpected(2048,0,expectedX));
        }
        JsonObject availableFloor=expected("returned","unit","label",2);
        availableFloor.add("coreCalls",UiParityTests.canonical(Arrays.asList(
            "log.info:73:Recording Video - Available storage: 0MB",
            "log.guid:73:CRITICAL: Storage space exhausted (0MB remaining). Stopping recording.")));
        check("video-negative-one-byte-log-division",()->{Fixture f=new Fixture(1,1);f.owner.available=-1;return f.args();},availableFloor);
        JsonObject maxCounter=expected("returned","unit","label",2);
        maxCounter.add("coreCalls",UiParityTests.canonical(Arrays.asList(
            "log.info:73:Recording Video - Available storage: 256MB",
            "log.info:73:Current file size: 1KB",
            "log.info:73:File size not growing: check 2147483647/3",
            "log.guid:73:CRITICAL: Video file stopped growing for 6442450941 seconds. Storage may be full. Stopping recording.")));
        check("video-counter-seconds-remain-long",()->{Fixture f=new Fixture(1,2);f.owner.w=Integer.MAX_VALUE-1;return f.args();},maxCounter);
    }
    static void expandedResumes(){
        for(int response=0;response<7;response++)for(int initial:new int[]{0,1}){
            final int r=response;check("video-resume-result:"+initial+":"+r,()->{Fixture f=new Fixture(initial,0);f.resumeInputs.add(f.response(r));f.resumeChanges.add(()->BaseVideoRecordingService.B=false);return f.args();},r==3?exception(ObservedFailure.class):r==4?exception(AssertionError.class):expected("returned","unit","label",initial==0?1:3));
        }
        for(int loops=0;loops<5;loops++){
            final int n=loops;JsonObject expected=ownerExpected((n+2)*1024L,0,256*MB);
            expected.getAsJsonObject("videoState").addProperty("delayCount",n+1);
            expected.getAsJsonObject("videoState").addProperty("returned","suspended");
            expected.getAsJsonObject("videoState").addProperty("dispatchCount",0);
            check("video-synchronous-repeat-chain:"+n,()->{Fixture f=new Fixture(1,0);for(int i=0;i<n;i++)VideoControl.delayResults.add(i%2==0?blg.a:f.equal);for(int i=0;i<=n;i++)f.file.lengthResults.add((i+2)*1024L);return f.args();},expected);
        }
        for(int resumes=1;resumes<=4;resumes++){
            final int count=resumes;check("video-multiple-resume-chain:"+count,()->{Fixture f=new Fixture(0,0);for(int i=0;i<count;i++){f.resumeInputs.add(blg.a);f.resumeChanges.add(i==count-1?()->BaseVideoRecordingService.B=false:null);f.file.lengthResults.add((i+2)*1024L);}return f.args();},expected("returned","unit","delayCount",count,"label",count==1?1:3,"equalsCalls",0));
        }
        check("video-resumed-stop-failure-then-exit",()->{Fixture f=new Fixture(1,1);VideoControl.dispatchResults.add(v93.COROUTINE_SUSPENDED);f.resumeInputs.add(new g3d(f.observed("stop resumed failure")));f.resumeInputs.add(blg.a);f.resumeChanges.add(null);f.resumeChanges.add(()->BaseVideoRecordingService.B=false);return f.args();},expected("returned","unit","label",3,"delayCount",1,"dispatchCount",1));
        check("video-synchronous-then-storage-exhaustion",()->{Fixture f=new Fixture(1,0);f.owner.availableResults.add(256*MB);f.owner.availableResults.add(128*MB-1);VideoControl.delayResults.add(blg.a);return f.args();},expected("returned","unit","label",2,"delayCount",1,"dispatchCount",1));
        for(int cast=0;cast<2;cast++){
            final int slot=cast;check("video-resumed-stop-dead-cast:"+slot,()->{Fixture f=new Fixture(1,1);VideoControl.dispatchResults.add(v93.COROUTINE_SUSPENDED);f.resumeInputs.add(blg.a);f.resumeChanges.add(()->{if(slot==0)f.self.L$0="bad-resume-flag";else f.self.L$1="bad-resume-file";});return f.args();},exception(ClassCastException.class));
        }
    }
    static void nestedFailures(){
        for(int profile:new int[]{7,8})for(int type=0;type<3;type++){
            final int p=profile,t=type;
            check("video-error-getMessage-throws:"+p+":"+t,()->{Fixture f=new Fixture(1,p);f.observedFailures.get(0).messageFailure=t==0?f.observed("secondary message failure"):t==1?f.error(new AssertionError("message Error")):f.error(new NullPointerException("message explicit null failure"));return f.args();},p==7&&t!=1?expected("returned","suspended","label",3):t==0?exception(ObservedFailure.class):t==1?exception(AssertionError.class):exception(NullPointerException.class));
        }
        for(int profile:new int[]{7,8}){
            final int p=profile;Supplier<Object[]> clean=()->new Fixture(1,p).args();List<String> calls=discover(clean);
            for(String prefix:new String[]{"exception.message:","string.concat:","log.error:"})for(int type=0;type<3;type++){
                int at=boundary(calls,prefix);final int index=at,t=type;
                check("video-nested-boundary-fault:"+p+":"+prefix+":"+t,()->{Object[] args=clean.get();VideoControl.failAt=index;VideoControl.failure=t==0?current.observed("second checked failure"):t==1?current.error(new AssertionError("second Error")):current.error(new ClassCastException("explicit cast-looking text"));return args;},p==7&&t!=1?expected("returned","suspended","label",3):t==0?exception(ObservedFailure.class):t==1?exception(AssertionError.class):exception(ClassCastException.class));
            }
        }
        Supplier<Object[]> inner=()->new Fixture(1,7).args();int firstLog=boundary(discover(inner),"log.error:");
        Supplier<Object[]> twoFailures=()->{Object[] args=inner.get();VideoControl.failAt=firstLog;VideoControl.failure=current.observed("inner logger failed");return args;};
        check("video-inner-logger-caught-by-outer",twoFailures,expected("returned","suspended","label",3));
        List<String> calls=discover(twoFailures);int outerLog=-1;for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith("log.error:")&&i>firstLog)outerLog=i;
        if(outerLog<0)throw new AssertionError("Outer logger was not observed");
        final int last=outerLog;
        for(int type=0;type<3;type++){
            final int t=type;check("video-outer-logger-escapes-after-inner:"+t,()->{Object[] args=twoFailures.get();VideoControl.failures.put(last,t==0?current.observed("outer logger checked failure"):t==1?current.error(new AssertionError("outer logger Error")):current.error(new IllegalStateException("outer logger state failure")));return args;},t==0?exception(ObservedFailure.class):t==1?exception(AssertionError.class):exception(IllegalStateException.class));
        }
        for(int response=3;response<=4;response++)for(int boundary=0;boundary<3;boundary++){
            final int r=response,b=boundary;Supplier<Object[]> resumeFailure=()->{Fixture f=new Fixture(2,0);f.input=new g3d(f.observed("resumed stopped failure"));return f.args();};
            List<String> planned=discover(resumeFailure);int at=boundary(planned,b==0?"exception.message:":b==1?"string.concat:":"log.error:");
            check("video-resume-two-outer-error-escapes:"+b+":"+r,()->{Object[] args=resumeFailure.get();VideoControl.failAt=at;VideoControl.failure=r==3?current.observed("resume logger failure"):current.error(new AssertionError("resume logger Error"));return args;},r==3?exception(ObservedFailure.class):exception(AssertionError.class));
        }
    }
    static void capturedOwnerContracts(){
        Supplier<Object[]> stopping=()->new Fixture(1,1).args();int available=boundary(discover(stopping),"storage.available:");
        check("video-captured-storage-owner-survives-field-null",()->{Object[] args=stopping.get();Fixture f=current;VideoControl.mutateAt=available;VideoControl.mutation=()->f.self.this$0=null;return args;},expected("returned","unit","owner",null,"label",2,"dispatchCount",1));
        for(long previous:new long[]{Long.MIN_VALUE,-1,0,1,100*MB,Long.MAX_VALUE}){
            check("video-captured-owner-x-changed-at-space-call:"+previous,()->{Object[] args=stopping.get();Fixture f=current;VideoControl.mutateAt=available;VideoControl.mutation=()->{f.self.this$0=f.other;f.owner.x=previous;};return args;},expected("returned","unit","owner","other","label",2));
        }
        for(boolean recording:new boolean[]{false,true})check("video-companion-before-recording:"+recording,()->{Fixture f=new Fixture(1,0);BaseVideoRecordingService.B=recording;BaseVideoRecordingService.A=null;return f.args();},exception(NullPointerException.class));
        for(int label:new int[]{0,1,2,3})check("video-null-receiver:"+label,()->{Fixture f=new Fixture(label,0);f.argumentSelf=null;return f.args();},exception(NullPointerException.class));
        for(int label:new int[]{1,2,3})check("video-null-owner-on-no-owner-path:"+label,()->{Fixture f=new Fixture(label,0);f.self.this$0=null;BaseVideoRecordingService.B=false;return f.args();},expected("returned","unit","label",label));
        Supplier<Object[]> healthy=()->new Fixture(1,0).args();int exists=boundary(discover(healthy),"file.exists:");
        check("video-file-length-rereads-captured-owner-file",()->{Object[] args=healthy.get();Fixture f=current;VideoControl.mutateAt=exists;VideoControl.mutation=()->f.owner.t=f.otherFile;return args;},ownerExpected(8192,0,256*MB));
        check("video-file-length-keeps-captured-owner",()->{Object[] args=healthy.get();Fixture f=current;VideoControl.mutateAt=exists;VideoControl.mutation=()->f.self.this$0=f.other;return args;},expected("owner","other","returned","suspended","label",3));
    }
    static void run(){entryCases();ordinaryCases();faultCases();mutationCases();numericContracts();expandedResumes();nestedFailures();capturedOwnerContracts();}
}
