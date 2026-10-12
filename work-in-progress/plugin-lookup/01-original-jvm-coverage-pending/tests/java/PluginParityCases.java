import android.os.Bundle;
import com.arlosoft.macrodroid.plugins.*;
import com.arlosoft.macrodroid.plugins.api.AppBrainApi;
import com.arlosoft.macrodroid.plugins.data.AppBrainPackageInfo;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.*;
import defpackage.*;
import java.io.IOException;
import java.util.*;
import java.util.function.Supplier;
import retrofit2.HttpException;

/** Bounded plugin/coroutine boundary comparison. No network or coroutine scheduler is run. */
public final class PluginParityCases {
    static final String KEY=UiParityTests.PREFIX+"plugins/j;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;";
    static Fixture current;

    static final class KnownList extends ArrayList<Object> {
        int containsCalls,addCalls;
        void seed(Object value){super.add(value);}
        @Override public boolean contains(Object value){containsCalls++;PluginControl.hit("known.contains:"+PluginControl.id(this)+":"+PluginControl.id(value));return super.contains(value);}
        @Override public boolean add(Object value){addCalls++;PluginControl.hit("known.add:"+PluginControl.id(this)+":"+PluginControl.id(value));return super.add(value);}
    }
    static final class Keys extends AbstractList<Object> {
        final ArrayList<Object> values=new ArrayList<Object>();int reads,sizeReads;
        @Override public Object get(int index){reads++;PluginControl.hit("keys.get:"+PluginControl.id(this)+":"+index);return values.get(index);}
        @Override public int size(){sizeReads++;PluginControl.hit("keys.size:"+PluginControl.id(this));return values.size();}
    }
    static final class ApiCall {
        final Object receiver,continuation;final String key,packageName;
        Object result;Throwable error;
        ApiCall(Object receiver,String key,String packageName,Object continuation){this.receiver=receiver;this.key=key;this.packageName=packageName;this.continuation=continuation;}
    }
    static final class FakeApi implements AppBrainApi {
        Object[] results;Object fallback;int reads;
        final List<ApiCall> calls=new ArrayList<ApiCall>();
        public Object getApp(String key,String packageName,m73 continuation){
            ApiCall call=new ApiCall(this,key,packageName,continuation);calls.add(call);int index=reads++;
            PluginControl.hit("api.get:"+PluginControl.id(this)+":"+PluginControl.id(key)+":"+PluginControl.id(packageName)+":"+PluginControl.id(continuation));
            Object value=index<results.length?results[index]:fallback;
            if(value instanceof Throwable){call.error=(Throwable)value;PluginControl.raise((Throwable)value);}
            call.result=value;return value;
        }
    }
    static final class Fixture {
        final j self=new j();final b owner=new b(),other=new b();
        final KnownList known=new KnownList(),otherKnown=new KnownList();
        final Keys keys=new Keys(),otherKeys=new Keys();
        final FakeApi api=new FakeApi(),otherApi=new FakeApi();
        final AppBrainPackageInfo info=new AppBrainPackageInfo("info0"),otherInfo=new AppBrainPackageInfo("info1");
        final FirebaseAnalytics otherAnalytics=new FirebaseAnalytics();
        final String packageName=new String("app.example.Ω"),otherPackage=new String("app.other.λ");
        final List<HttpException> http=new ArrayList<HttpException>();
        final List<Throwable> externalErrors=new ArrayList<Throwable>();
        final List<Object> resumeInputs=new ArrayList<Object>();
        final List<String> steps=new ArrayList<String>();
        Object input=blg.a;
        Fixture(int label,int attempts,int keyCount){
            current=this;PluginControl.self=self;
            self.this$0=owner;self.$packageName=packageName;self.label=label;self.I$0=label==2?0:23;self.I$1=label==2?0:-17;
            owner.h=attempts;other.h=91;owner.g=known;other.g=otherKnown;owner.c=api;other.c=otherApi;
            api.results=new Object[]{info};api.fallback=otherInfo;otherApi.results=new Object[]{otherInfo};otherApi.fallback=info;
            Object[] named={self,owner,other,known,otherKnown,keys,otherKeys,api,otherApi,info,otherInfo,owner.j,other.j,sz5.b,otherAnalytics,packageName,otherPackage,b.k};
            String[] names={"self","owner0","owner1","known0","known1","keys0","keys1","api0","api1","info0","info1","sink0","sink1","analytics0","analytics1","package0","package1","companion0"};
            for(int i=0;i<named.length;i++)PluginControl.name(named[i],names[i]);
            for(int i=0;i<keyCount;i++){String key=new String("synthetic-key-"+i);keys.values.add(key);PluginControl.name(key,"key"+i);}
            String otherKey=new String("synthetic-other-key");otherKeys.values.add(otherKey);PluginControl.name(otherKey,"otherKey");
            b.l=keys;
            if(label==1)input=Boolean.TRUE;if(label==2)input=info;
            PluginControl.active=true;
        }
        HttpException http(int... codes){HttpException e=new HttpException("scripted HTTP "+Arrays.toString(codes),codes);PluginControl.name(e,"http"+http.size());http.add(e);externalErrors.add(e);return e;}
        <T extends Throwable>T error(T value){PluginControl.name(value,"error"+externalErrors.size());externalErrors.add(value);return value;}
        Object outcome(int code){
            switch(code){
                case 0:return info;
                case 1:return http(400);
                case 2:return http(429);
                case 3:return http(500);
                case 4:return error(new IOException("scripted API checked exception"));
                case 5:return error(new AssertionError("scripted API Error"));
                case 6:return v93.COROUTINE_SUSPENDED;
                case 7:return null;
                case 8:return "wrong-info";
                case 9:return Boolean.TRUE;
                case 10:{g3d failure=new g3d(error(new IOException("result failure object")));PluginControl.name(failure,"resultFailure");return failure;}
                case 11:return http(400,429);
                case 12:return http(429,400);
                default:throw new AssertionError(code);
            }
        }
        void response(int code){
            Object value=outcome(code);
            if(self.label==2){
                input=value instanceof Throwable?new g3d((Throwable)value):value;
                if(input instanceof g3d)PluginControl.name(input,"resumeFailure");
                api.results=new Object[]{info};
            } else api.results=code==2?new Object[]{value,info}:new Object[]{value};
        }
        void gate(int code){
            Object value;
            switch(code){case 0:value=Boolean.TRUE;break;case 1:value=Boolean.FALSE;break;case 2:value=v93.COROUTINE_SUSPENDED;break;case 3:value=null;break;case 4:value="wrong-boolean";break;case 5:value=error(new IOException("scripted precheck checked exception"));break;case 6:value=error(new AssertionError("scripted precheck Error"));break;default:throw new AssertionError(code);}
            owner.precheckResults=new Object[]{value};
        }
        Object[] args(){return new Object[]{self,input};}
    }
    static Object[] make(int label,int attempts,int keys,int response){Fixture f=new Fixture(label,attempts,keys);f.response(response);return f.args();}
    static Object execute(String path,Object[] args)throws Throwable {
        Object value;
        try{value=UiParityTests.call(KEY,path,args);recordStep(value,null);}
        catch(Throwable failure){recordStep(null,failure);throw failure;}
        if(current!=null)for(Object input:current.resumeInputs){
            try{value=UiParityTests.call(KEY,path,new Object[]{current.self,input});recordStep(value,null);}
            catch(Throwable failure){recordStep(null,failure);throw failure;}
        }
        return value;
    }
    static void recordStep(Object value,Throwable failure){
        if(current==null)return;j self=current.self;
        current.steps.add((failure==null?"return:"+PluginControl.id(value):"throw:"+failure.getClass().getName())+":"+self.label+":"+self.I$0+":"+self.I$1+":"+PluginControl.id(self.this$0)+":"+(self.this$0==null?"null":self.this$0.h));
    }
    static JsonElement id(Object value){return value==null?JsonNull.INSTANCE:new JsonPrimitive(PluginControl.id(value));}
    static String kind(Object value){
        if(value==null)return "null";
        if(value instanceof d)return "found";if(value instanceof c)return "notFound";if(value instanceof g)return "denied";
        if(value instanceof b$b$a)return "connectionError";if(value instanceof b$b$b)return "attemptLimit";return value.getClass().getName();
    }
    static JsonArray publications(List<PluginControl.Publication> calls){JsonArray a=new JsonArray();for(PluginControl.Publication call:calls){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.add("value",id(call.value));x.addProperty("kind",kind(call.value));a.add(x);}return a;}
    static JsonArray analytics(List<PluginControl.Analytics> calls){JsonArray a=new JsonArray();for(PluginControl.Analytics call:calls){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.add("bundle",id(call.bundle));x.addProperty("event",call.event);x.add("values",UiParityTests.canonical(call.values));a.add(x);}return a;}
    static JsonArray apiCalls(FakeApi api){JsonArray a=new JsonArray();for(ApiCall call:api.calls){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.add("key",id(call.key));x.addProperty("keyText",call.key);x.add("package",id(call.packageName));x.addProperty("packageText",call.packageName);x.add("continuation",id(call.continuation));x.add("result",id(call.result));x.add("error",id(call.error));a.add(x);}return a;}
    static void observe(Object[] args,JsonObject result){
        JsonObject s=new JsonObject();result.add("pluginState",s);
        s.addProperty("resultKind",PluginControl.escaped==null?"return":"throw");s.add("returned",id(PluginControl.returned));
        s.addProperty("returnedUnitIdentity",PluginControl.escaped==null&&PluginControl.returned==blg.a);
        s.addProperty("returnedSuspendedIdentity",PluginControl.escaped==null&&PluginControl.returned==v93.COROUTINE_SUSPENDED);
        s.add("boundaries",UiParityTests.canonical(PluginControl.boundaries));s.add("boundaryStates",UiParityTests.canonical(PluginControl.states));s.addProperty("boundaryCalls",PluginControl.boundaryCalls);
        s.add("publicationAttempts",publications(PluginControl.publicationAttempts));s.add("publications",publications(PluginControl.publications));
        ArrayList<String> kinds=new ArrayList<String>();for(PluginControl.Publication call:PluginControl.publications)kinds.add(kind(call.value));s.add("publishedKinds",UiParityTests.canonical(kinds));
        s.add("analyticsAttempts",analytics(PluginControl.analyticsAttempts));s.add("analytics",analytics(PluginControl.analytics));
        ArrayList<String> events=new ArrayList<String>();for(PluginControl.Analytics call:PluginControl.analytics)events.add(call.event);s.add("analyticsEvents",UiParityTests.canonical(events));
        JsonArray bundles=new JsonArray();for(Bundle value:PluginControl.bundles){JsonObject x=new JsonObject();x.add("identity",id(value));x.add("values",UiParityTests.canonical(value.values));bundles.add(x);}s.add("bundles",bundles);
        JsonArray created=new JsonArray();for(PluginControl.Constructed value:PluginControl.created){JsonObject x=new JsonObject();x.add("identity",id(value.object));x.addProperty("kind",value.kind);x.add("argument",id(value.value));Object field=value.object instanceof c?((c)value.object).a:value.object instanceof d?((d)value.object).a:((g)value.object).a;x.add("storedValue",id(field));created.add(x);}s.add("created",created);
        if(PluginControl.escaped!=null){
            Throwable error=PluginControl.escaped;boolean external=error==PluginControl.failure||current!=null&&current.externalErrors.contains(error);
            s.addProperty("escapedInjectedIdentity",error==PluginControl.failure);s.addProperty("escapedExternalIdentity",external);
            if(external){s.add("escaped",id(error));s.addProperty("exceptionMessage",error.getMessage());}
            else if(!(error instanceof NullPointerException)&&!(error instanceof ClassCastException))s.addProperty("exceptionMessage",error.getMessage());
        }
        if(current==null)return;Fixture f=current;
        s.addProperty("label",f.self.label);s.addProperty("I0",f.self.I$0);s.addProperty("I1",f.self.I$1);s.add("owner",id(f.self.this$0));s.add("package",id(f.self.$packageName));
        s.addProperty("attempts",f.owner.h);s.addProperty("otherAttempts",f.other.h);s.addProperty("denied",f.owner.i);
        s.addProperty("prechecks",f.owner.precheckReads);s.addProperty("otherPrechecks",f.other.precheckReads);s.add("precheckPackage",id(f.owner.lastPackage));s.add("precheckContinuation",id(f.owner.lastContinuation));
        s.addProperty("containsCalls",f.known.containsCalls);s.addProperty("addCalls",f.known.addCalls);s.add("known",UiParityTests.canonical(f.known));s.add("otherKnown",UiParityTests.canonical(f.otherKnown));
        s.addProperty("keyReads",f.keys.reads);s.addProperty("keySizeReads",f.keys.sizeReads);s.addProperty("otherKeyReads",f.otherKeys.reads);s.addProperty("otherKeySizeReads",f.otherKeys.sizeReads);
        s.add("keys",UiParityTests.canonical(f.keys.values));s.add("activeKeys",id(b.l));s.add("companion",id(b.k));s.add("analyticsReceiver",id(sz5.b));
        s.addProperty("apiCalls",f.api.reads);s.addProperty("otherApiCalls",f.otherApi.reads);s.add("api",apiCalls(f.api));s.add("otherApi",apiCalls(f.otherApi));
        s.add("steps",UiParityTests.canonical(f.steps));
        JsonArray http=new JsonArray();for(HttpException error:f.http){JsonObject x=new JsonObject();x.add("identity",id(error));x.addProperty("reads",error.reads);x.add("codes",UiParityTests.canonical(error.codes));http.add(x);}s.add("http",http);
        if(PluginControl.failure instanceof HttpException)s.addProperty("injectedStatusReads",((HttpException)PluginControl.failure).reads);
    }
    static JsonObject expected(Object... pairs){JsonObject root=new JsonObject(),s=new JsonObject();root.add("pluginState",s);for(int i=0;i<pairs.length;i+=2)s.add((String)pairs[i],UiParityTests.canonical(pairs[i+1]));return root;}
    static void expectException(JsonObject expected,Class<?> type){expected.addProperty("exception",type.getName());expected.getAsJsonObject("pluginState").addProperty("resultKind","throw");}
    static void check(String label,Supplier<Object[]> make,JsonObject expected){UiParityTests.check(KEY,label,make,UiParityTests.UNKNOWN,false,expected);}

    static void gates(){
        int[] attempts={Integer.MIN_VALUE,-1,0,3,4,5,6,Integer.MAX_VALUE};
        for(boolean denied:new boolean[]{false,true})for(boolean known:new boolean[]{false,true})for(int count:attempts)for(int gate=0;gate<7;gate++){
            final int g=gate;boolean blocked=denied||known||count>=5;String publication=denied?"denied":known?"notFound":count>=5?"attemptLimit":gate==0?"found":null;
            boolean success=!blocked&&gate==0;int finalLabel=blocked?0:success?2:1;
            JsonObject exp=expected("resultKind","return","attempts",success?0:count,"label",finalLabel,"prechecks",blocked?0:1,"apiCalls",success?1:0,"containsCalls",denied?0:1,"publishedKinds",publication==null?Collections.emptyList():Arrays.asList(publication));
            if(!blocked&&(gate==3||gate==4||gate==5||gate==6))expectException(exp,gate==3?NullPointerException.class:gate==4?ClassCastException.class:gate==5?IOException.class:AssertionError.class);
            else exp.getAsJsonObject("pluginState").addProperty("returned",!blocked&&gate==2?"suspended":"unit");
            check("plugin-gate:"+denied+":"+known+":"+count+":"+gate,()->{Fixture f=new Fixture(0,count,2);f.owner.i=denied;if(known)f.known.seed(f.packageName);f.gate(g);return f.args();},exp);
        }
    }
    static JsonObject flowExpected(int label,int attempts,int keys,int response){
        boolean resume=label==2;boolean reachedApi=resume||keys>0;boolean failureBeforeApi=!resume&&keys==0;
        boolean retry=response==2&&keys>1&&reachedApi;
        boolean error=response==5&&reachedApi;
        boolean suspend=response==6&&!resume&&reachedApi;
        boolean success=response==0&&reachedApi||retry;
        int calls=resume?(retry?1:0):failureBeforeApi?0:retry?2:1;
        int count=success?0:resume?attempts:attempts+1;
        ArrayList<String> kinds=new ArrayList<String>();
        if(success)kinds.add("found");
        else if(!error&&!suspend&&!(response==2&&reachedApi))kinds.add((response==1||response==11)&&reachedApi?"notFound":"connectionError");
        ArrayList<String> events=new ArrayList<String>();
        int made=resume?(retry?1:0):retry?2:1;for(int i=0;i<made;i++)events.add("app_brain_api_call_made");
        if(response==2&&reachedApi&&!retry)events.add("app_brain_calls_exceeded");
        JsonObject exp=expected("resultKind",error?"throw":"return","attempts",count,"apiCalls",calls,"publishedKinds",kinds,"analyticsEvents",events,
            "prechecks",label==0?1:0,"label",failureBeforeApi?1:2);
        if(error)expectException(exp,AssertionError.class);else exp.getAsJsonObject("pluginState").addProperty("returned",suspend?"suspended":"unit");
        return exp;
    }
    static void flows(){
        for(int label=0;label<3;label++)for(int count:new int[]{Integer.MIN_VALUE,-1,0,4,Integer.MAX_VALUE})for(int keys=0;keys<4;keys++)for(int response=0;response<13;response++){
            if(label==0&&count>=5)continue;
            final int l=label,k=keys,r=response;
            check("plugin-flow:"+l+":"+count+":"+k+":"+r,()->make(l,count,k,r),flowExpected(l,count,k,r));
        }
    }
    static void resumedState(){
        int[] values={Integer.MIN_VALUE,-1,0,1,Integer.MAX_VALUE};
        for(int retry:values)for(int index:values)for(int response:new int[]{0,1,2,3,4,5,7,8,11,12})for(int keys:new int[]{1,3}){
            final int r=response;
            check("plugin-resume-state:"+retry+":"+index+":"+r+":"+keys,()->{Object[] args=make(2,7,keys,r);current.self.I$0=retry;current.self.I$1=index;return args;},null);
        }
        check("plugin-resume-nonzero-flag-generic",()->{Object[] args=make(2,7,2,3);current.self.I$0=1;return args;},expected("returned","unit","apiCalls",1,"attempts",0,"publishedKinds",Arrays.asList("connectionError","found")));
        check("plugin-resume-index-overflow",()->{Object[] args=make(2,7,1,2);current.self.I$1=Integer.MAX_VALUE;return args;},expected("returned","unit","apiCalls",1,"attempts",0,"publishedKinds",Arrays.asList("found")));
        check("plugin-resume-index-exhausted",()->{Object[] args=make(2,7,3,2);current.self.I$1=2;return args;},expected("returned","unit","apiCalls",0,"attempts",7,"publishedKinds",Collections.emptyList(),"analyticsEvents",Arrays.asList("app_brain_calls_exceeded")));
    }
    static Throwable fault(int type){
        switch(type){case 0:return new IllegalStateException("injected state");case 1:return new NullPointerException("injected null message");case 2:return new ClassCastException("injected cast message");case 3:return new AssertionError("injected Error");case 4:return new IOException("injected checked exception");case 5:return new SecurityException("injected security exception");case 6:return new HttpException("injected 400",400);case 7:return new HttpException("injected 429",429);default:throw new AssertionError(type);}
    }
    static List<String> boundaries(Supplier<Object[]> make){UiParityTests.outcome(KEY,"original",make,false);return new ArrayList<String>(PluginControl.boundaries);}
    static void faults(){
        List<Supplier<Object[]>> paths=Arrays.asList(
            ()->make(0,0,2,0),()->make(0,0,2,1),()->make(0,0,2,2),()->make(0,0,1,2),()->make(2,9,2,2),
            ()->{Fixture f=new Fixture(0,4,2);f.owner.i=true;return f.args();},
            ()->{Fixture f=new Fixture(0,4,2);f.known.seed(f.packageName);return f.args();},
            ()->{Fixture f=new Fixture(0,5,2);return f.args();});
        for(int p=0;p<paths.size();p++){
            Supplier<Object[]> make=paths.get(p);List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int type=0;type<8;type++){
                final int index=at,t=type;
                check("plugin-fault:"+p+":"+at+":"+type,()->{Object[] args=make.get();PluginControl.failAt=index;PluginControl.failure=fault(t);PluginControl.name(PluginControl.failure,"injected");return args;},null);
            }
        }
    }
    static void run(){gates();flows();resumedState();faults();}
}
