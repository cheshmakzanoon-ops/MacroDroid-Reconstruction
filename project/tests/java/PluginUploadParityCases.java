import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import com.arlosoft.macrodroid.plugins.*;
import com.arlosoft.macrodroid.plugins.api.*;
import com.arlosoft.macrodroid.templatestore.model.User;
import com.google.gson.*;
import defpackage.*;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.*;
import java.util.function.Supplier;
import okhttp3.*;
import retrofit2.HttpException;

/** Exact selected-body comparison with controlled icon/upload boundaries; no Android or network. */
public final class PluginUploadParityCases {
    static final String KEY=UiParityTests.PREFIX+"plugins/k;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;";
    static Fixture current;

    static String snapshot(k self) {
        if(self==null)return "null";
        return self.label+":"+PluginControl.id(self.L$0)+":"+PluginControl.id(self.L$1)+":"+
                PluginControl.id(self.L$2)+":"+PluginControl.id(self.L$3)+":"+PluginControl.id(self.L$4)+":"+
                PluginControl.id(self.this$0)+":"+(self.this$0==null?"null":self.this$0.i+":"+self.this$0.h);
    }
    static final class ApiCall {
        final Object receiver,argument,continuation;final String kind,hash,state;
        Object result;Throwable error;
        ApiCall(Object receiver,String kind,String hash,Object argument,m73 continuation) {
            this.receiver=receiver;this.kind=kind;this.hash=hash;this.argument=argument;this.continuation=continuation;
            state=snapshot((k)continuation);
        }
    }
    static final class FakeApi implements PluginListApi {
        Object[] iconResults,uploadResults;Object iconFallback,uploadFallback=blg.a;
        int iconReads,uploadReads;boolean returnThrowableAsValue;final List<ApiCall> calls=new ArrayList<ApiCall>();
        public Object uploadNonPlayStoreAppIcon(MultipartBody$Part part,m73 continuation) {
            ApiCall call=new ApiCall(this,"icon",null,part,continuation);calls.add(call);int index=iconReads++;
            PluginControl.hit("upload.icon:"+PluginControl.id(this)+":"+PluginControl.id(part)+":"+PluginControl.id(continuation));
            Object value=index<iconResults.length?iconResults[index]:iconFallback;
            if(value instanceof Throwable&&!returnThrowableAsValue){call.error=(Throwable)value;PluginControl.raise((Throwable)value);}
            call.result=value;return value;
        }
        public Object uploadPlayStorePlugin(String hash,UploadPluginBody body,m73 continuation) {
            ApiCall call=new ApiCall(this,"plugin",hash,body,continuation);calls.add(call);int index=uploadReads++;
            PluginControl.hit("upload.plugin:"+PluginControl.id(this)+":"+PluginControl.id(hash)+":"+PluginControl.id(body)+":"+PluginControl.id(continuation));
            Object value=index<uploadResults.length?uploadResults[index]:uploadFallback;
            if(value instanceof Throwable&&!returnThrowableAsValue){call.error=(Throwable)value;PluginControl.raise((Throwable)value);}
            call.result=value;return value;
        }
    }
    static final class Fixture {
        final k self=new k();final b owner=new b(),other=new b();
        final FakeApi api=new FakeApi(),otherApi=new FakeApi();
        final jsg users=new jsg(),otherUsers=new jsg();final User user=new User(),otherUser=new User();
        final Drawable drawable=new Drawable(),otherDrawable=new Drawable();
        final Bitmap bitmap=new Bitmap(),otherBitmap=new Bitmap();
        final String name=new String("Example Ω"),otherName=new String("Changed λ");
        final String icon=new String("https://example.invalid/uploaded.png"),fallbackIcon=new String("stored-icon://Ω");
        final String otherIcon=new String("stored-icon://other");
        final List<HttpException> http=new ArrayList<HttpException>();
        final List<Throwable> externalErrors=new ArrayList<Throwable>();
        final List<Object> resumeInputs=new ArrayList<Object>();
        final List<Runnable> resumeChanges=new ArrayList<Runnable>();
        final List<String> steps=new ArrayList<String>();
        Object input=blg.a;
        Fixture(int label,boolean withDrawable) {
            current=this;self.label=label;self.this$0=owner;self.$drawable=withDrawable?drawable:null;
            owner.b=api;other.b=otherApi;owner.d=users;other.d=otherUsers;owner.h=37;other.h=-9;
            users.user=user;otherUsers.user=otherUser;user.userId=123;otherUser.userId=-456;
            drawable.bitmap=bitmap;otherDrawable.bitmap=otherBitmap;otherBitmap.bytes=new byte[]{9,-8,7};
            self.$name=name;self.$developerName=new String("developer λ");self.$shortDescription=new String("description\nΩ");
            self.$packageName=new String("app.example.upload");self.$downloadLink=new String("link://download");
            self.$iconUrl=fallbackIcon;self.$website=new String("site://example");self.$hash=new String("synthetic-hash");
            api.iconResults=new Object[]{icon};api.iconFallback=otherIcon;api.uploadResults=new Object[]{blg.a};
            otherApi.iconResults=new Object[]{otherIcon};otherApi.iconFallback=icon;otherApi.uploadResults=new Object[]{blg.a};
            Object[] objects={self,owner,other,api,otherApi,users,otherUsers,user,otherUser,drawable,otherDrawable,bitmap,otherBitmap,
                    owner.j,other.j,name,otherName,icon,fallbackIcon,otherIcon,self.$developerName,self.$shortDescription,
                    self.$packageName,self.$downloadLink,self.$website,self.$hash,PluginUploadControl.mediaType,
                    PluginUploadControl.requestBody,PluginUploadControl.part,MediaType.d,RequestBody.Companion,MultipartBody$Part.c,l1g.b};
            String[] names={"self","owner0","owner1","api0","api1","users0","users1","user0","user1","drawable0","drawable1","bitmap0","bitmap1",
                    "sink0","sink1","name0","name1","uploadedIcon","storedIcon","otherIcon","developer0","description0",
                    "package0","download0","website0","hash0","media0","request0","part0","mediaCompanion0","requestCompanion0","partCompanion0","logger0"};
            for(int i=0;i<objects.length;i++)PluginControl.name(objects[i],names[i]);
            if(label==0){Object[] values=new Object[5];for(int i=0;i<5;i++){values[i]=new Object();PluginControl.name(values[i],"saved"+i);}setSaved(values);}
            if(label==1){byte[] savedBytes=new byte[]{4,5};ByteArrayOutputStream stream=new ByteArrayOutputStream();PluginControl.name(savedBytes,"savedBytes");PluginControl.name(stream,"savedStream");setSaved(new Object[]{bitmap,stream,savedBytes,PluginUploadControl.requestBody,PluginUploadControl.part});input=icon;}
            if(label==2){UploadPluginBody saved=new UploadPluginBody(6,"old","old","old","old","old",null,"old","en");PluginControl.name(saved,"savedBody");self.L$0=fallbackIcon;self.L$1=saved;}
            PluginControl.created.clear();PluginControl.boundaries.clear();PluginControl.states.clear();PluginControl.boundaryCalls=0;
            PluginControl.continuationSnapshot=()->snapshot(self);PluginControl.active=true;
        }
        void setSaved(Object[] values){self.L$0=values[0];self.L$1=values[1];self.L$2=values[2];self.L$3=values[3];self.L$4=values[4];}
        HttpException http(int... codes){HttpException error=new HttpException("scripted upload HTTP "+Arrays.toString(codes),codes);PluginControl.name(error,"http"+http.size());http.add(error);externalErrors.add(error);return error;}
        <T extends Throwable>T error(T value){PluginControl.name(value,"error"+externalErrors.size());externalErrors.add(value);return value;}
        Object response(int code,boolean iconResult) {
            switch(code){
                case 0:return iconResult?icon:blg.a;
                case 1:return v93.COROUTINE_SUSPENDED;
                case 2:return null;
                case 3:return http(409);
                case 4:return http(403);
                case 5:return http(500);
                case 6:return error(new IOException("scripted upload checked exception"));
                case 7:return error(new AssertionError("scripted upload Error"));
                case 8:return Integer.valueOf(913);
                case 9:{g3d failure=new g3d(error(new IOException("scripted result failure")));PluginControl.name(failure,"resultFailure"+externalErrors.size());return failure;}
                case 10:return http(409,403);
                case 11:return http(403,409);
                case 12:{Object equal=new PluginParityCases.EqualSuspended();PluginControl.name(equal,"equalSuspended");return equal;}
                default:throw new AssertionError(code);
            }
        }
        Object resume(Object value){if(value instanceof Throwable){Object wrapped=new g3d((Throwable)value);PluginControl.name(wrapped,"resumeFailure"+externalErrors.size());return wrapped;}return value;}
        Object[] args(){return new Object[]{self,input};}
    }
    static Object[] make(int label,boolean drawable,int iconCode,int uploadCode,boolean compressResult) {
        Fixture f=new Fixture(label,drawable);f.bitmap.compressResult=compressResult;
        if(label==0){f.api.iconResults=new Object[]{f.response(iconCode,true)};f.api.uploadResults=new Object[]{f.response(uploadCode,false)};}
        else if(label==1){f.input=f.resume(f.response(iconCode,true));f.api.uploadResults=new Object[]{f.response(uploadCode,false)};}
        else if(label==2)f.input=f.resume(f.response(uploadCode,false));
        return f.args();
    }
    static Object execute(String path,Object[] args)throws Throwable {
        Object value;
        try{value=UiParityTests.call(KEY,path,args);recordStep(value,null);}catch(Throwable failure){recordStep(null,failure);throw failure;}
        if(current!=null)for(int i=0;i<current.resumeInputs.size();i++){
            if(i<current.resumeChanges.size()&&current.resumeChanges.get(i)!=null)current.resumeChanges.get(i).run();
            try{value=UiParityTests.call(KEY,path,new Object[]{current.self,current.resumeInputs.get(i)});recordStep(value,null);}
            catch(Throwable failure){recordStep(null,failure);throw failure;}
        }
        return value;
    }
    static void recordStep(Object value,Throwable failure){if(current!=null)current.steps.add((failure==null?"return:"+PluginControl.id(value):"throw:"+failure.getClass().getName())+":"+snapshot(current.self));}
    static JsonElement id(Object value){return value==null?JsonNull.INSTANCE:new JsonPrimitive(PluginControl.id(value));}
    static JsonArray ids(Object... values){JsonArray result=new JsonArray();for(Object value:values)result.add(id(value));return result;}
    static JsonArray bytes(byte[] values){JsonArray result=new JsonArray();if(values!=null)for(byte value:values)result.add(value);return result;}
    static Object[] fields(UploadPluginBody body){return new Object[]{body.userId,body.name,body.developerName,body.description,body.packageName,body.downloadLink,body.iconUrl,body.website,body.language};}
    static String kind(Object value){if(value instanceof f)return "uploaded";if(value instanceof g)return String.valueOf(((g)value).a);return value==null?"null":value.getClass().getName();}
    static JsonArray publications(List<PluginControl.Publication> calls){JsonArray result=new JsonArray();for(PluginControl.Publication call:calls){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.add("value",id(call.value));x.addProperty("kind",kind(call.value));result.add(x);}return result;}
    static JsonArray apiCalls(FakeApi api){JsonArray result=new JsonArray();for(ApiCall call:api.calls){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.addProperty("kind",call.kind);x.add("hash",id(call.hash));x.add("argument",id(call.argument));x.add("continuation",id(call.continuation));x.addProperty("state",call.state);x.add("result",id(call.result));x.add("error",id(call.error));result.add(x);}return result;}
    static void observe(Object[] args,JsonObject result) {
        JsonObject s=new JsonObject();result.add("uploadState",s);
        s.addProperty("resultKind",PluginControl.escaped==null?"return":"throw");s.add("returned",id(PluginControl.returned));
        s.addProperty("returnedUnitIdentity",PluginControl.escaped==null&&PluginControl.returned==blg.a);
        s.addProperty("returnedSuspendedIdentity",PluginControl.escaped==null&&PluginControl.returned==v93.COROUTINE_SUSPENDED);
        s.add("boundaries",UiParityTests.canonical(PluginControl.boundaries));s.add("boundaryStates",UiParityTests.canonical(PluginControl.states));s.addProperty("boundaryCalls",PluginControl.boundaryCalls);
        s.add("publicationAttempts",publications(PluginControl.publicationAttempts));s.add("publications",publications(PluginControl.publications));
        ArrayList<String> kinds=new ArrayList<String>(),receivers=new ArrayList<String>();for(PluginControl.Publication call:PluginControl.publications){kinds.add(kind(call.value));receivers.add(PluginControl.id(call.receiver));}
        s.add("publishedKinds",UiParityTests.canonical(kinds));s.add("publicationReceivers",UiParityTests.canonical(receivers));
        JsonArray created=new JsonArray(),payloads=new JsonArray();
        for(PluginControl.Constructed call:PluginControl.created){
            JsonObject x=new JsonObject();x.add("identity",id(call.object));x.addProperty("kind",call.kind);
            if(call.object instanceof UploadPluginBody){x.add("arguments",ids((Object[])call.value));x.add("stored",ids(fields((UploadPluginBody)call.object)));payloads.add(ids(fields((UploadPluginBody)call.object)));}
            else{x.add("argument",id(call.value));x.add("stored",id(call.object instanceof f?((f)call.object).a:((g)call.object).a));}
            created.add(x);
        }
        s.add("created",created);s.add("payloads",payloads);s.addProperty("payloadCount",payloads.size());
        JsonArray compressions=new JsonArray();for(PluginUploadControl.Compression call:PluginUploadControl.compressions){JsonObject x=new JsonObject();x.add("bitmap",id(call.bitmap));x.add("format",id(call.format));x.addProperty("quality",call.quality);x.add("stream",id(call.stream));x.addProperty("completed",call.completed);x.add("bytes",bytes(((ByteArrayOutputStream)call.stream).toByteArray()));compressions.add(x);}s.add("compressions",compressions);
        JsonArray requests=new JsonArray();for(PluginUploadControl.Request call:PluginUploadControl.requests){JsonObject x=new JsonObject();x.add("companion",id(call.companion));x.add("mediaType",id(call.mediaType));x.add("bytesIdentity",id(call.bytes));x.add("bytes",bytes(call.bytes));x.addProperty("offset",call.offset);x.addProperty("mask",call.mask);x.addProperty("completed",call.completed);requests.add(x);}s.add("requests",requests);JsonArray requestMediaTypes=new JsonArray();for(PluginUploadControl.Request call:PluginUploadControl.requests)requestMediaTypes.add(id(call.mediaType));s.add("requestMediaTypes",requestMediaTypes);JsonArray requestCompanions=new JsonArray();for(PluginUploadControl.Request call:PluginUploadControl.requests)requestCompanions.add(id(call.companion));s.add("requestCompanions",requestCompanions);
        JsonArray parts=new JsonArray();for(PluginUploadControl.Part call:PluginUploadControl.parts){JsonObject x=new JsonObject();x.addProperty("name",call.name);x.add("body",id(call.body));x.addProperty("completed",call.completed);parts.add(x);}s.add("parts",parts);
        s.add("parseInputs",UiParityTests.canonical(PluginUploadControl.parseInputs));s.addProperty("logAttempts",PluginUploadControl.logAttempts);s.addProperty("logCompletions",PluginUploadControl.logCompletions);
        if(PluginControl.escaped!=null){Throwable error=PluginControl.escaped;boolean external=error==PluginControl.failure||current!=null&&current.externalErrors.contains(error);s.addProperty("escapedInjectedIdentity",error==PluginControl.failure);s.addProperty("escapedExternalIdentity",external);if(external){s.add("escaped",id(error));s.addProperty("exceptionMessage",error.getMessage());}else if(!(error instanceof NullPointerException)&&!(error instanceof ClassCastException))s.addProperty("exceptionMessage",error.getMessage());}
        if(current==null)return;Fixture f=current;
        s.addProperty("label",f.self.label);s.add("saved",ids(f.self.L$0,f.self.L$1,f.self.L$2,f.self.L$3,f.self.L$4));s.add("owner",id(f.self.this$0));s.addProperty("snapshot",snapshot(f.self));
        s.addProperty("denied",f.owner.i);s.addProperty("otherDenied",f.other.i);s.addProperty("attempts",f.owner.h);s.addProperty("otherAttempts",f.other.h);
        s.addProperty("iconCalls",f.api.iconReads);s.addProperty("uploadCalls",f.api.uploadReads);s.addProperty("otherIconCalls",f.otherApi.iconReads);s.addProperty("otherUploadCalls",f.otherApi.uploadReads);s.add("api",apiCalls(f.api));s.add("otherApi",apiCalls(f.otherApi));
        s.addProperty("userReads",f.users.reads);s.addProperty("otherUserReads",f.otherUsers.reads);s.addProperty("idReads",f.user.reads);s.addProperty("otherIdReads",f.otherUser.reads);s.addProperty("userId",f.user.userId);s.addProperty("otherUserId",f.otherUser.userId);
        s.add("fields",ids(f.self.$name,f.self.$developerName,f.self.$shortDescription,f.self.$packageName,f.self.$downloadLink,f.self.$iconUrl,f.self.$website,f.self.$hash));s.add("steps",UiParityTests.canonical(f.steps));
        JsonArray http=new JsonArray();for(HttpException error:f.http){JsonObject x=new JsonObject();x.add("identity",id(error));x.addProperty("reads",error.reads);x.add("codes",UiParityTests.canonical(error.codes));http.add(x);}s.add("http",http);
        if(PluginControl.failure instanceof HttpException)s.addProperty("injectedStatusReads",((HttpException)PluginControl.failure).reads);
    }
    static JsonObject expected(Object... pairs){JsonObject root=new JsonObject(),s=new JsonObject();root.add("uploadState",s);for(int i=0;i<pairs.length;i+=2)s.add((String)pairs[i],UiParityTests.canonical(pairs[i+1]));return root;}
    static void exception(JsonObject result,Class<?> type){result.addProperty("exception",type.getName());result.getAsJsonObject("uploadState").addProperty("resultKind","throw");}
    static void check(String label,Supplier<Object[]> make,JsonObject expected){UiParityTests.check(KEY,label,make,UiParityTests.UNKNOWN,false,expected);}
    static boolean thrownResponse(int code){return code>=3&&code<=7||code==10||code==11;}
    static String errorKind(int code){return code==3||code==10?"ALREADY_EXISTS":code==4?"USER_NOT_ALLOWED":"CONNECTION_ERROR";}
    static JsonObject flowExpected(int label,boolean drawable,int icon,int upload) {
        int iconCalls=label==0&&drawable?1:0,uploadCalls=0,finalLabel=label,failed=0,userReads=0;
        boolean suspended=false,error=false;
        if(label==0&&drawable){finalLabel=1;if(icon==1)suspended=true;else if(thrownResponse(icon)||icon==8||icon==9||icon==12)failed=icon;}
        if(label==1&&(thrownResponse(icon)||icon==1||icon==8||icon==9||icon==12))failed=icon==1?8:icon;
        if(!suspended&&failed==0){
            if(label<2){userReads=1;uploadCalls=1;finalLabel=2;if(upload==1)suspended=true;else if(thrownResponse(upload))failed=upload;}
            else if(thrownResponse(upload)||upload==9)failed=upload;
        }
        if(failed==7)error=true;
        String publication=suspended||error?null:failed==0?"uploaded":errorKind(failed);
        int logs="CONNECTION_ERROR".equals(publication)?1:0;
        JsonObject exp=expected("label",finalLabel,"iconCalls",iconCalls,"uploadCalls",uploadCalls,"userReads",userReads,"idReads",userReads,
                "attempts",37,"otherAttempts",-9,"denied","USER_NOT_ALLOWED".equals(publication),"otherDenied",false,
                "logAttempts",logs,"logCompletions",logs,"publishedKinds",publication==null?Collections.emptyList():Arrays.asList(publication));
        if(error)exception(exp,AssertionError.class);else exp.getAsJsonObject("uploadState").addProperty("returned",suspended?"suspended":"unit");
        return exp;
    }
    static void flows() {
        for(int upload=0;upload<13;upload++){final int u=upload;check("upload-no-icon:"+u,()->make(0,false,0,u,true),flowExpected(0,false,0,u));}
        for(boolean compressed:new boolean[]{false,true})for(int icon=0;icon<13;icon++)for(int upload=0;upload<13;upload++){
            final int i=icon,u=upload;check("upload-flow:0:"+compressed+":"+i+":"+u,()->make(0,true,i,u,compressed),flowExpected(0,true,i,u));
        }
        for(int icon=0;icon<13;icon++)for(int upload=0;upload<13;upload++){
            final int i=icon,u=upload;check("upload-flow:1:"+i+":"+u,()->make(1,false,i,u,true),flowExpected(1,false,i,u));
        }
        for(int upload=0;upload<13;upload++){final int u=upload;check("upload-flow:2:"+u,()->make(2,false,0,u,true),flowExpected(2,false,0,u));}
    }
    static void storedCastsAndInputs() {
        for(int label:new int[]{1,2})for(int field=0;field<(label==1?5:2);field++)for(boolean bad:new boolean[]{false,true}){
            final int l=label,n=field;JsonObject exp=bad?expected("publishedKinds",Collections.emptyList(),"iconCalls",0,"uploadCalls",0,"boundaryCalls",0):null;if(bad)exception(exp,ClassCastException.class);
            check("upload-saved-cast:"+l+":"+n+":"+bad,()->{Fixture f=new Fixture(l,false);Object[] values={f.self.L$0,f.self.L$1,f.self.L$2,f.self.L$3,f.self.L$4};values[n]=bad?Integer.valueOf(99):null;f.setSaved(values);return f.args();},exp);
        }
        for(int label:new int[]{Integer.MIN_VALUE,-1,3,19,Integer.MAX_VALUE}){
            JsonObject exp=expected("publishedKinds",Collections.emptyList(),"boundaryCalls",1);exception(exp,IllegalStateException.class);
            check("upload-invalid-label:"+label,()->new Fixture(label,false).args(),exp);
        }
        check("upload-invalid-label-injected-return",()->{Fixture f=new Fixture(9,false);PluginControl.invalidLabelReturns=true;return f.args();},expected("returned",null,"publishedKinds",Collections.emptyList(),"boundaryCalls",1));
        JsonObject npe=expected("publishedKinds",Collections.emptyList(),"boundaryCalls",0);exception(npe,NullPointerException.class);
        check("upload-null-self",()->new Object[]{null,blg.a},npe);
        for(int type=0;type<8;type++){final int t=type;JsonObject exp=expected("publishedKinds",Collections.emptyList(),"iconCalls",0,"uploadCalls",0,"label",0);exception(exp,fault(type).getClass());
            check("upload-initial-result-failure:"+t,()->{Fixture f=new Fixture(0,true);f.input=new g3d(f.error(fault(t)));PluginControl.name(f.input,"initialFailure");return f.args();},exp);
        }
    }
    static Throwable fault(int type){switch(type){case 0:return new IllegalStateException("injected upload state");case 1:return new NullPointerException("injected upload null");case 2:return new ClassCastException("injected upload cast");case 3:return new AssertionError("injected upload Error");case 4:return new IOException("injected upload checked exception");case 5:return new IllegalArgumentException("injected upload argument");case 6:return new HttpException("injected upload409",409);case 7:return new HttpException("injected upload403",403);default:throw new AssertionError(type);}}
    static List<String> boundaries(Supplier<Object[]> make){UiParityTests.outcome(KEY,"original",make,false);return new ArrayList<String>(PluginControl.boundaries);}
    static int boundary(List<String> calls,String prefix){for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith(prefix))return i;throw new AssertionError("Missing boundary "+prefix+" in "+calls);}
    static void faults() {
        List<Supplier<Object[]>> paths=Arrays.asList(()->make(0,true,0,0,true),()->make(0,false,0,0,true),()->make(1,false,0,0,true),()->make(2,false,0,0,true),
                ()->make(0,true,3,0,true),()->make(0,true,0,4,true),()->make(0,true,0,5,true),
                ()->{Object[] a=make(0,true,0,0,true);PluginUploadControl.parseFailure=current.error(new IllegalArgumentException("scripted invalid media"));return a;});
        for(int p=0;p<paths.size();p++){
            Supplier<Object[]> make=paths.get(p);List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int type=0;type<8;type++){
                final int index=at,t=type;check("upload-fault:"+p+":"+at+":"+type,()->{Object[] args=make.get();PluginControl.failAt=index;PluginControl.failure=fault(t);PluginControl.name(PluginControl.failure,"injected");return args;},null);
            }
        }
    }
    static void mutate(Fixture f,int what) {
        switch(what){
            case 0:f.self.this$0=f.other;break;case 1:f.owner.b=f.otherApi;break;case 2:f.owner.d=f.otherUsers;break;case 3:f.users.user=f.otherUser;break;
            case 4:f.user.userId=Integer.MIN_VALUE;break;case 5:f.self.$name=f.otherName;break;case 6:f.self.$shortDescription=null;break;
            case 7:f.self.$downloadLink=f.otherName;break;case 8:f.self.$iconUrl=f.otherIcon;break;case 9:f.self.$website=null;break;
            case 10:f.self.$hash=f.otherName;break;case 11:f.self.$drawable=f.otherDrawable;break;case 12:f.drawable.bitmap=f.otherBitmap;break;
            case 13:f.bitmap.bytes=new byte[]{-128,0,127};break;case 14:RequestBody.Companion=null;break;case 15:MediaType.d=null;break;
            case 16:MultipartBody$Part.c=null;break;case 17:PluginUploadControl.requestBody=null;break;case 18:PluginUploadControl.part=null;break;
            case 19:f.self.label=91;break;case 20:f.setSaved(new Object[]{"changed0","changed1","changed2","changed3","changed4"});break;
            case 21:f.owner.j=f.other.j;break;case 22:l1g.b=null;break;case 23:f.owner.i=true;break;
            default:throw new AssertionError(what);
        }
    }
    static void mutations() {
        List<Supplier<Object[]>> paths=Arrays.asList(()->make(0,true,0,0,true),()->make(1,false,0,0,true),()->make(2,false,0,4,true),()->make(0,false,0,5,true));
        for(int p=0;p<paths.size();p++){
            Supplier<Object[]> make=paths.get(p);List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int what=0;what<24;what++){
                final int index=at,w=what;check("upload-mutate:"+p+":"+at+":"+what,()->{Object[] args=make.get();Fixture f=current;PluginControl.mutateAt=index;PluginControl.mutation=()->mutate(f,w);return args;},null);
            }
        }
    }
    static void payloadsAndNulls() {
        for(int userId:new int[]{Integer.MIN_VALUE,-1,0,1,Integer.MAX_VALUE})for(int text=0;text<10;text++){
            final int t=text;
            check("upload-payload:"+userId+":"+t,()->{Object[] a=make(0,false,0,0,true);Fixture f=current;f.user.userId=userId;switch(t){case 1:f.self.$name="";break;case 2:f.self.$name=null;break;case 3:f.self.$developerName=null;break;case 4:f.self.$shortDescription=null;break;case 5:f.self.$packageName=null;break;case 6:f.self.$downloadLink=null;break;case 7:f.self.$iconUrl=null;break;case 8:f.self.$website=null;break;case 9:f.self.$hash=null;break;}return a;},null);
        }
        for(int label=0;label<3;label++)for(int which=0;which<9;which++){
            final int l=label,w=which;
            check("upload-null-boundary:"+l+":"+w,()->{Object[] a=make(l,true,0,0,true);Fixture f=current;switch(w){case 0:f.self.this$0=null;break;case 1:f.owner.b=null;break;case 2:f.owner.d=null;break;case 3:f.users.user=null;break;case 4:f.drawable.bitmap=null;break;case 5:RequestBody.Companion=null;break;case 6:MediaType.d=null;break;case 7:MultipartBody$Part.c=null;break;case 8:f.owner.j=null;break;}return a;},null);
        }
        for(int type=0;type<8;type++){final int t=type;check("upload-media-parse:"+t,()->{Object[] a=make(0,true,0,0,true);PluginUploadControl.parseFailure=current.error(fault(t));return a;},null);}
        check("upload-compress-false-is-ignored",()->make(0,true,0,0,false),expected("returned","unit","iconCalls",1,"uploadCalls",1,"publishedKinds",Arrays.asList("uploaded")));
        check("upload-nested-media-argument-handler",()->{Object[] a=make(0,true,0,0,true);PluginUploadControl.parseFailure=current.error(new IllegalArgumentException("invalid media"));return a;},expected("returned","unit","iconCalls",1,"uploadCalls",1,"publishedKinds",Arrays.asList("uploaded"),"requestMediaTypes",Collections.singletonList(null)));
        check("upload-returned-failure-wrapper-is-ignored",()->make(0,false,0,9,true),expected("returned","unit","publishedKinds",Arrays.asList("uploaded")));
        check("upload-second-status-read-and-priority",()->make(0,false,0,10,true),expected("returned","unit","denied",false,"publishedKinds",Arrays.asList("ALREADY_EXISTS")));
        check("upload-icon-marker-identity",()->make(0,true,12,0,true),expected("returned","unit","uploadCalls",0,"publishedKinds",Arrays.asList("CONNECTION_ERROR")));
        check("upload-plugin-marker-identity",()->make(0,false,0,12,true),expected("returned","unit","publishedKinds",Arrays.asList("uploaded")));
    }
    static void explicitOrdering() {
        List<String> expectedBody=Arrays.asList("123","name0","developer0","description0","package0","download0","uploadedIcon","website0","en");
        check("upload-payload-order-and-uploaded-icon",()->make(0,true,0,0,true),expected("returned","unit","payloads",Arrays.asList(expectedBody)));
        List<String> fallbackBody=Arrays.asList("123","name0","developer0","description0","package0","download0","storedIcon","website0","en");
        check("upload-null-icon-fallback",()->make(0,true,2,0,true),expected("returned","unit","payloads",Arrays.asList(fallbackBody)));
        Supplier<Object[]> make=()->make(0,true,0,0,true);int parse=boundary(boundaries(make),"media.parse:");
        check("upload-request-companion-captured-before-media",()->{Object[] args=make.get();PluginControl.mutateAt=parse;PluginControl.mutation=()->RequestBody.Companion=null;return args;},expected("returned","unit","requestCompanions",Arrays.asList("requestCompanion0")));
        List<String> calls=boundaries(make);int found=-1;
        for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith("payload.new:")&&calls.get(i).contains(":uploaded:")){found=i;break;}
        if(found<0)throw new AssertionError("Missing success payload constructor");final int success=found;
        check("upload-success-sink-captured-before-payload",()->{Object[] args=make.get();Fixture f=current;PluginControl.mutateAt=success;PluginControl.mutation=()->f.owner.j=f.other.j;return args;},expected("returned","unit","publicationReceivers",Arrays.asList("sink0")));
    }
    static void sequences() {
        for(int resumeIcon:new int[]{0,2,3,4,5,6,7,8,9,10,11,12})for(int resumeUpload:new int[]{0,2,3,4,5,6,7,8,9,10,11,12}){
            final int i=resumeIcon,u=resumeUpload;
            check("upload-sequence:"+i+":"+u,()->{Fixture f=new Fixture(0,true);f.api.iconResults=new Object[]{v93.COROUTINE_SUSPENDED};f.api.uploadResults=new Object[]{v93.COROUTINE_SUSPENDED};f.resumeInputs.add(f.resume(f.response(i,true)));if(i==0||i==2)f.resumeInputs.add(f.resume(f.response(u,false)));return f.args();},null);
        }
        for(int what=0;what<24;what++){
            final int w=what;
            check("upload-suspended-mutation:"+w,()->{Fixture f=new Fixture(0,true);f.api.iconResults=new Object[]{v93.COROUTINE_SUSPENDED};f.api.uploadResults=new Object[]{v93.COROUTINE_SUSPENDED};f.resumeInputs.add(f.icon);f.resumeChanges.add(()->mutate(f,w));return f.args();},null);
        }
        check("upload-two-suspensions",()->{Fixture f=new Fixture(0,true);f.api.iconResults=new Object[]{v93.COROUTINE_SUSPENDED};f.api.uploadResults=new Object[]{v93.COROUTINE_SUSPENDED};f.resumeInputs.add(f.icon);f.resumeInputs.add(blg.a);return f.args();},expected("returned","unit","label",2,"saved",Arrays.asList(null,null,null,null,null),"iconCalls",1,"uploadCalls",1,"publishedKinds",Arrays.asList("uploaded")));
    }
    static void rawResultValues() {
        for(int which=0;which<6;which++){
            final int w=which;
            check("upload-initial-raw-value:"+w,()->{Fixture f=new Fixture(0,false);switch(w){case 0:f.input=null;break;case 1:f.input=Integer.valueOf(19);break;case 2:f.input="unused initial result";break;case 3:f.input=f.error(new IOException("bare result IOException"));break;case 4:f.input=f.error(new AssertionError("bare result Error"));break;case 5:f.input=f.http(403);break;}return f.args();},expected("returned","unit","denied",false,"publishedKinds",Arrays.asList("uploaded")));
        }
        check("upload-icon-throwable-as-returned-value",()->{Fixture f=new Fixture(0,true);f.api.iconResults=new Object[]{f.http(403)};f.api.returnThrowableAsValue=true;return f.args();},expected("returned","unit","denied",false,"publishedKinds",Arrays.asList("CONNECTION_ERROR")));
        check("upload-plugin-throwable-as-returned-value",()->{Fixture f=new Fixture(0,false);f.api.uploadResults=new Object[]{f.http(403)};f.api.returnThrowableAsValue=true;return f.args();},expected("returned","unit","denied",false,"publishedKinds",Arrays.asList("uploaded")));
        for(int label:new int[]{1,2}){
            check("upload-resume-bare-throwable:"+label,()->{Fixture f=new Fixture(label,false);f.input=f.http(403);return f.args();},expected("returned","unit","denied",false,"publishedKinds",Arrays.asList(label==1?"CONNECTION_ERROR":"uploaded")));
        }
    }
    static void run(){flows();storedCastsAndInputs();faults();mutations();payloadsAndNulls();explicitOrdering();sequences();rawResultValues();}
}
