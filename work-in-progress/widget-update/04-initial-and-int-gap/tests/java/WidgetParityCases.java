import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProviderInfo;
import android.content.Context;
import com.arlosoft.macrodroid.widget.custom.WidgetUpdateManager;
import com.arlosoft.macrodroid.widget.custom.b;
import com.google.gson.*;
import defpackage.*;
import java.io.IOException;
import java.util.*;
import java.util.function.Supplier;

/** Selected original instructions and recovered JVM body, using controlled widget boundaries.
 * No Android widget, renderer, scheduler or continuation implementation is executed.
 */
public final class WidgetParityCases {
    static final String KEY=UiParityTests.PREFIX+"widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;";
    static Fixture current;

    /** This adapter is explicit, belongs to this exact method, and is validated against its DEX.
     * The child constructor is only a host reflection adapter; ART proof is separate.
     */
    static void configure(BytecodeOracle oracle)throws Exception {
        JsonObject entry=UiParityTests.registry.get(KEY);
        if(entry==null)return;
        JsonArray mappings=entry.getAsJsonArray("constructor_owner_mappings");
        if(mappings==null||mappings.size()!=1)throw new IllegalArgumentException("Widget needs exactly its pinned constructor adapter");
        JsonObject mapping=mappings.get(0).getAsJsonObject();
        if(!"Lzhh;".equals(mapping.get("allocated_type").getAsString())
                ||!"Lrff;".equals(mapping.get("original_owner").getAsString())
                ||!"<init>(ILm73;)V".equals(mapping.get("constructor").getAsString())
                ||mapping.get("occurrences").getAsInt()!=1)
            throw new IllegalArgumentException("Unexpected Widget constructor adapter");
        oracle.allowParentConstructor(KEY,"Lzhh;","Lrff;","<init>(ILm73;)V",1);
    }

    static final class PlainCompletion extends o73 {}
    static final class EqualSuspended {
        int equalsCalls;
        @Override public boolean equals(Object other){equalsCalls++;WidgetControl.hit("marker.equals:"+WidgetControl.id(other));return other==v93.COROUTINE_SUSPENDED;}
        @Override public int hashCode(){return 11;}
    }
    static final class ObservedNumber extends Number {
        int value, reads;
        ObservedNumber(int value){this.value=value;}
        public int intValue(){reads++;WidgetControl.hit("number.int:"+WidgetControl.id(this)+":"+value);return value;}
        public long longValue(){throw new AssertionError("Unexpected number.longValue");}
        public float floatValue(){throw new AssertionError("Unexpected number.floatValue");}
        public double doubleValue(){throw new AssertionError("Unexpected number.doubleValue");}
        public String toString(){return "observed-number("+value+")";}
    }
    static final class ObservedFailure extends IOException {
        final String text;
        int messageReads;
        Throwable messageFailure;
        ObservedFailure(String text){super(text);this.text=text;}
        @Override public String getMessage(){
            messageReads++;WidgetControl.hit("exception.message:"+WidgetControl.id(this));
            if(messageFailure!=null)WidgetControl.raise(messageFailure);
            return text;
        }
    }
    static final class FakeIterator implements Iterator<Object> {
        final List<Object> values;
        int position,hasNextReads,nextReads;
        FakeIterator(List<Object> values){this.values=values;}
        public boolean hasNext(){hasNextReads++;WidgetControl.hit("iterator.hasNext:"+WidgetControl.id(this)+":"+position);return position<values.size();}
        public Object next(){
            nextReads++;WidgetControl.hit("iterator.next:"+WidgetControl.id(this)+":"+position);
            if(position>=values.size())throw new NoSuchElementException("scripted iterator exhausted");
            return values.get(position++);
        }
        public void remove(){throw new AssertionError("Unexpected iterator.remove");}
    }
    static final class FakeList extends AbstractList<Object> {
        final List<Object> values=new ArrayList<Object>();
        FakeIterator iterator;
        Boolean emptyOverride;
        int emptyReads,iteratorReads;
        FakeList(Object... values){Collections.addAll(this.values,values);iterator=new FakeIterator(this.values);}
        @Override public boolean isEmpty(){emptyReads++;WidgetControl.hit("list.empty:"+WidgetControl.id(this));return emptyOverride==null?values.isEmpty():emptyOverride;}
        @Override public Iterator<Object> iterator(){iteratorReads++;WidgetControl.hit("list.iterator:"+WidgetControl.id(this));return iterator;}
        @Override public Object get(int index){throw new AssertionError("Unexpected List.get");}
        @Override public int size(){throw new AssertionError("Unexpected List.size");}
    }
    static final class Fixture {
        final WidgetUpdateManager owner=new WidgetUpdateManager(),otherOwner=new WidgetUpdateManager();
        final Context context=new Context(),otherContext=new Context();
        final PlainCompletion plain=new PlainCompletion();
        final FakeList ids,otherIds=new FakeList(91);
        final List<Throwable> externalErrors=new ArrayList<Throwable>();
        final List<ObservedFailure> observedFailures=new ArrayList<ObservedFailure>();
        final List<ObservedNumber> numbers=new ArrayList<ObservedNumber>();
        final List<Object> resumeInputs=new ArrayList<Object>();
        final List<Runnable> resumeChanges=new ArrayList<Runnable>();
        final List<String> steps=new ArrayList<String>();
        final EqualSuspended equal=new EqualSuspended();
        final AppWidgetManager backend,otherBackend=new AppWidgetManager();
        b supplied;
        wx6 suppliedManager;
        hn9 suppliedRenderer;
        mh0 suppliedIdentifier;
        Object argumentOwner,argumentContext,argumentList;
        o73 completion;
        int initialContinuations,initialManagers,initialRenderers,initialIdentifiers,initialFactories;

        /** entry: 0=null completion, 1=foreign completion, 2=b without high bit, 3=reused b. */
        Fixture(int entry,int label,Object... values){
            current=this;backend=WidgetControl.backend;ids=new FakeList(values);
            WidgetControl.name(owner,"owner");WidgetControl.name(otherOwner,"other-owner");
            WidgetControl.name(context,"context");WidgetControl.name(otherContext,"other-context");
            WidgetControl.name(plain,"completion");WidgetControl.name(ids,"ids");WidgetControl.name(ids.iterator,"iterator");
            WidgetControl.name(otherIds,"other-ids");WidgetControl.name(otherIds.iterator,"other-iterator");
            WidgetControl.name(otherBackend,"other-backend");WidgetControl.name(equal,"equal-suspended");
            context.testContextId="context";otherContext.testContextId="other-context";
            for(Object value:values)if(value instanceof Number && !(value instanceof ObservedNumber))provider(((Number)value).intValue(),true);
            provider(417,true);provider(91,true);
            argumentOwner=owner;argumentContext=context;argumentList=ids;
            if(entry>=2){
                supplied=new b(otherOwner,plain);supplied.label=entry==3?Integer.MIN_VALUE|label:label;
                supplied.I$0=13;supplied.I$1=417;supplied.I$2=-9;supplied.result=blg.a;
                suppliedManager=new wx6(context);suppliedRenderer=new hn9();suppliedIdentifier=new mh0(417);
                setSaved(context,otherIds,suppliedManager,suppliedRenderer,otherIds,ids.iterator,"unread-L6",suppliedIdentifier);
                completion=supplied;
                if(entry==3&&label!=0){argumentContext=otherContext;argumentList=otherIds;}
            }else completion=entry==0?null:plain;
            initialContinuations=WidgetControl.continuations.size();initialManagers=WidgetControl.managers.size();
            initialRenderers=WidgetControl.renderers.size();initialIdentifiers=WidgetControl.identifiers.size();initialFactories=WidgetControl.factories.size();
            WidgetControl.active=true;
        }
        void provider(int widgetId,boolean present){
            if(present){AppWidgetProviderInfo value=new AppWidgetProviderInfo();WidgetControl.name(value,"provider:"+widgetId);backend.providers.put(widgetId,value);}
            else backend.providers.remove(widgetId);
        }
        void setSaved(Object... values){
            supplied.L$0=values[0];supplied.L$1=values[1];supplied.L$2=values[2];supplied.L$3=values[3];
            supplied.L$4=values[4];supplied.L$5=values[5];supplied.L$6=values[6];supplied.L$7=values[7];
        }
        void saved(int index,Object value){
            Object[] values={supplied.L$0,supplied.L$1,supplied.L$2,supplied.L$3,supplied.L$4,supplied.L$5,supplied.L$6,supplied.L$7};
            values[index]=value;setSaved(values);
        }
        <T extends Throwable>T error(T value){WidgetControl.name(value,"error"+externalErrors.size());externalErrors.add(value);return value;}
        ObservedFailure observed(String text){ObservedFailure failure=error(new ObservedFailure(text));observedFailures.add(failure);return failure;}
        ObservedNumber number(int value){ObservedNumber number=new ObservedNumber(value);WidgetControl.name(number,"number"+numbers.size());numbers.add(number);return number;}
        Object response(int code){
            switch(code){
                case 0:return "ordinary-result";
                case 1:return v93.COROUTINE_SUSPENDED;
                case 2:return null;
                case 3:{g3d value=new g3d(observed("scripted widget checked exception"));WidgetControl.name(value,"wrapped-checked"+externalErrors.size());return value;}
                case 4:{g3d value=new g3d(error(new AssertionError("scripted widget Error")));WidgetControl.name(value,"wrapped-error"+externalErrors.size());return value;}
                case 5:return error(new IOException("exception returned as ordinary value"));
                case 6:return equal;
                case 7:return Integer.valueOf(932);
                default:throw new AssertionError(code);
            }
        }
        Object[] args(){return new Object[]{argumentOwner,argumentContext,argumentList,completion};}
    }

    static Object[] make(int entry,int label,int first,int second,Object... ids){
        Fixture f=new Fixture(entry,label,ids);
        WidgetControl.firstResults.add(f.response(first));WidgetControl.secondResults.add(f.response(second));
        return f.args();
    }
    static Object execute(String path,Object[] args)throws Throwable {
        Object result;
        try{result=UiParityTests.call(KEY,path,args);step(result,null);}catch(Throwable failure){step(null,failure);throw failure;}
        if(current!=null)for(int index=0;index<current.resumeInputs.size();index++){
            if(result!=v93.COROUTINE_SUSPENDED)throw new AssertionError("Script attempted to resume a completed Widget call");
            b state=WidgetControl.current;
            if(state==null)throw new AssertionError("Suspension has no captured continuation");
            if(index<current.resumeChanges.size()&&current.resumeChanges.get(index)!=null)current.resumeChanges.get(index).run();
            state.result=current.resumeInputs.get(index);state.label|=Integer.MIN_VALUE;
            try{result=UiParityTests.call(KEY,path,new Object[]{current.argumentOwner,current.otherContext,current.otherIds,state});step(result,null);}
            catch(Throwable failure){step(null,failure);throw failure;}
        }
        return result;
    }
    static void step(Object value,Throwable failure){if(current!=null)current.steps.add((failure==null?"return:"+WidgetControl.id(value):"throw:"+failure.getClass().getName())+":"+WidgetControl.state(WidgetControl.current));}
    static JsonElement id(Object value){return value==null?JsonNull.INSTANCE:new JsonPrimitive(WidgetControl.id(value));}
    static JsonArray identities(List<?> values){JsonArray out=new JsonArray();for(Object value:values)out.add(id(value));return out;}
    static JsonArray calls(List<WidgetControl.Call> values){
        JsonArray out=new JsonArray();
        for(WidgetControl.Call call:values){JsonObject x=new JsonObject();x.add("receiver",id(call.receiver));x.add("context",id(call.context));x.add("identifier",id(call.identifier));x.add("factory",id(call.factory));x.add("continuation",id(call.continuation));x.addProperty("state",call.state);out.add(x);}
        return out;
    }
    static JsonObject iterator(FakeIterator value){
        JsonObject out=new JsonObject();if(value==null){out.addProperty("present",false);return out;}
        out.addProperty("present",true);out.addProperty("position",value.position);out.addProperty("hasNextReads",value.hasNextReads);out.addProperty("nextReads",value.nextReads);out.add("values",identities(value.values));return out;
    }
    static void observe(Object[] args,JsonObject result){
        JsonObject out=new JsonObject();result.add("widgetState",out);
        out.addProperty("resultKind",WidgetControl.escaped==null?"return":"throw");out.add("returned",id(WidgetControl.returned));
        out.addProperty("returnedUnitIdentity",WidgetControl.escaped==null&&WidgetControl.returned==blg.a);
        out.addProperty("returnedSuspendedIdentity",WidgetControl.escaped==null&&WidgetControl.returned==v93.COROUTINE_SUSPENDED);
        out.add("boundaries",UiParityTests.canonical(WidgetControl.boundaries));out.add("boundaryStates",UiParityTests.canonical(WidgetControl.states));out.addProperty("boundaryCalls",WidgetControl.boundaryCalls);
        out.add("firstCalls",calls(WidgetControl.firstCalls));out.add("secondCalls",calls(WidgetControl.secondCalls));out.addProperty("firstCount",WidgetControl.firstReads);out.addProperty("secondCount",WidgetControl.secondReads);
        JsonArray states=new JsonArray();for(b state:WidgetControl.continuations)states.add(WidgetControl.state(state));out.add("continuations",states);
        out.addProperty("currentState",WidgetControl.state(WidgetControl.current));out.addProperty("label",WidgetControl.current==null?null:WidgetControl.current.label);
        out.addProperty("savedIndex",WidgetControl.current==null?null:WidgetControl.current.I$0);out.addProperty("savedId",WidgetControl.current==null?null:WidgetControl.current.I$1);out.addProperty("savedPhase",WidgetControl.current==null?null:WidgetControl.current.I$2);
        JsonArray factories=new JsonArray();for(rff factory:WidgetControl.factories){JsonObject x=new JsonObject();x.add("identity",id(factory));x.addProperty("class",factory.getClass().getName());x.addProperty("arity",factory.widgetArity);x.add("completion",id(factory.widgetCompletion));factories.add(x);}out.add("factories",factories);
        JsonArray identifiers=new JsonArray();for(mh0 identifier:WidgetControl.identifiers){JsonObject x=new JsonObject();x.add("identity",id(identifier));x.addProperty("widgetId",identifier.id);identifiers.add(x);}out.add("identifiers",identifiers);
        JsonArray managers=new JsonArray();for(wx6 manager:WidgetControl.managers){JsonObject x=new JsonObject();x.add("identity",id(manager));x.add("context",id(manager.context));x.add("backend",id(manager.b));managers.add(x);}out.add("managers",managers);out.add("renderers",identities(WidgetControl.renderers));
        List<String> logs=new ArrayList<String>();for(String text:CoreTrace.calls)if(text.startsWith("log.error:"))logs.add(text.substring("log.error:".length()));out.add("logs",UiParityTests.canonical(logs));out.addProperty("logCount",logs.size());
        Throwable escaped=WidgetControl.escaped;
        if(escaped!=null){
            boolean external=escaped==WidgetControl.failure||current!=null&&current.externalErrors.contains(escaped);
            out.addProperty("escapedInjectedIdentity",escaped==WidgetControl.failure);out.addProperty("escapedExternalIdentity",external);
            if(external)out.add("escaped",id(escaped));
            if(escaped instanceof ObservedFailure)out.addProperty("exceptionMessage",((ObservedFailure)escaped).text);
            else if(external||!(escaped instanceof NullPointerException)&&!(escaped instanceof ClassCastException))out.addProperty("exceptionMessage",escaped.getMessage());
        }
        if(current==null)return;
        Fixture f=current;out.add("ownerInitializationContexts",identities(f.owner.initializationContexts));out.add("otherOwnerInitializationContexts",identities(f.otherOwner.initializationContexts));
        out.add("backendReads",UiParityTests.canonical(f.backend.reads));out.add("otherBackendReads",UiParityTests.canonical(f.otherBackend.reads));
        out.addProperty("listEmptyReads",f.ids.emptyReads);out.addProperty("listIteratorReads",f.ids.iteratorReads);out.addProperty("otherListEmptyReads",f.otherIds.emptyReads);out.addProperty("otherListIteratorReads",f.otherIds.iteratorReads);
        out.add("iterator",iterator(f.ids.iterator));out.add("otherIterator",iterator(f.otherIds.iterator));out.add("steps",UiParityTests.canonical(f.steps));
        out.addProperty("newContinuations",WidgetControl.continuations.size()-f.initialContinuations);out.addProperty("newManagers",WidgetControl.managers.size()-f.initialManagers);out.addProperty("newRenderers",WidgetControl.renderers.size()-f.initialRenderers);out.addProperty("newIdentifiers",WidgetControl.identifiers.size()-f.initialIdentifiers);out.addProperty("newFactories",WidgetControl.factories.size()-f.initialFactories);out.addProperty("markerEqualsCalls",f.equal.equalsCalls);
        out.addProperty("suppliedContinuationReused",f.supplied!=null&&WidgetControl.current==f.supplied);
        JsonArray messages=new JsonArray();for(ObservedFailure error:f.observedFailures){JsonObject x=new JsonObject();x.add("identity",id(error));x.addProperty("text",error.text);x.addProperty("messageReads",error.messageReads);messages.add(x);}out.add("observedMessages",messages);
        JsonArray numbers=new JsonArray();for(ObservedNumber number:f.numbers){JsonObject x=new JsonObject();x.add("identity",id(number));x.addProperty("value",number.value);x.addProperty("intReads",number.reads);numbers.add(x);}out.add("numbers",numbers);
    }
    static JsonObject expected(Object... fields){JsonObject result=new JsonObject(),state=new JsonObject();result.add("widgetState",state);for(int i=0;i<fields.length;i+=2)state.add((String)fields[i],UiParityTests.canonical(fields[i+1]));return result;}
    static JsonObject exception(JsonObject result,Class<?> type){result.addProperty("exception",type.getName());result.getAsJsonObject("widgetState").addProperty("resultKind","throw");return result;}
    static void check(String label,Supplier<Object[]> make,JsonObject expected){UiParityTests.check(KEY,label,make,UiParityTests.UNKNOWN,false,expected);}
    static Throwable fault(int type){switch(type){case 0:return new IllegalStateException("injected widget state");case 1:return new NullPointerException("injected widget null");case 2:return new ClassCastException("injected widget cast");case 3:return new AssertionError("injected widget Error");case 4:return new IOException("injected widget checked exception");case 5:return new IllegalArgumentException("injected widget argument");case 6:return new SecurityException("injected widget security");default:throw new AssertionError(type);}}
    static List<String> boundaries(Supplier<Object[]> make){UiParityTests.outcome(KEY,"original",make,false);return new ArrayList<String>(WidgetControl.boundaries);}
    static int boundary(List<String> calls,String prefix){for(int i=0;i<calls.size();i++)if(calls.get(i).startsWith(prefix))return i;throw new AssertionError("Missing Widget boundary "+prefix+" in "+calls);}

    static void entryAndFlows(){
        for(int entry=0;entry<4;entry++)for(boolean empty:new boolean[]{false,true}){
            final int e=entry;int label=entry==3?0:17;
            check("widget-entry:"+entry+":"+empty,()->make(e,label,0,0,empty?new Object[]{}:new Object[]{7}),expected("returned","unit","newContinuations",entry==3?0:1,"suppliedContinuationReused",entry==3,"listEmptyReads",1,"firstCount",empty?0:1,"secondCount",empty?0:1,"logCount",0,"markerEqualsCalls",0));
        }
        for(int first=0;first<8;first++)for(int second=0;second<8;second++){
            final int a=first,z=second;boolean reachesSecond=first!=1&&first!=3&&first!=4;
            boolean error=first==4||reachesSecond&&second==4;boolean suspended=first==1||reachesSecond&&second==1;
            int logs=first==3||reachesSecond&&second==3?1:0;
            JsonObject exp=expected("firstCount",1,"secondCount",reachesSecond?1:0,"logCount",logs,"label",reachesSecond?2:1,"savedIndex",0,"savedPhase",0,"markerEqualsCalls",0);
            if(error)exception(exp,AssertionError.class);else exp.getAsJsonObject("widgetState").addProperty("returned",suspended?"suspended":"unit");
            check("widget-flow:"+first+":"+second,()->make(1,0,a,z,7),exp);
        }
        check("widget-invalid-provider-continues",()->{Fixture f=new Fixture(1,0,7,-1,8);f.provider(-1,false);return f.args();},expected("returned","unit","backendReads",Arrays.asList(7,-1,8),"firstCount",2,"secondCount",2,"savedIndex",0,"savedId",8,"logs",Arrays.asList("Failed to update custom widget instance -1: Invalid AppWidget ID.")));
        check("widget-empty-override-skips-initialization",()->{Fixture f=new Fixture(1,0,7);f.ids.emptyOverride=true;return f.args();},expected("returned","unit","newManagers",0,"newRenderers",0,"firstCount",0,"listIteratorReads",0));
        check("widget-nonempty-override-empty-iterator",()->{Fixture f=new Fixture(1,0);f.ids.emptyOverride=false;return f.args();},expected("returned","unit","newManagers",1,"newRenderers",1,"firstCount",0,"listIteratorReads",1));
        for(int label:new int[]{0,1,2,3,19,Integer.MAX_VALUE}){
            check("widget-no-high-bit-creates-new:"+label,()->new Fixture(2,label,7).args(),expected("returned","unit","newContinuations",1,"suppliedContinuationReused",false,"firstCount",1,"secondCount",1));
        }
        for(int label:new int[]{3,19,Integer.MAX_VALUE}){
            check("widget-invalid-label:"+label,()->new Fixture(3,label,7).args(),exception(expected("boundaryCalls",1,"newContinuations",0,"label",label,"firstCount",0,"secondCount",0,"exceptionMessage","call to 'resume' before 'invoke' with coroutine"),IllegalStateException.class));
        }
        check("widget-invalid-label-injected-return",()->{Fixture f=new Fixture(3,9,7);WidgetControl.invalidLabelReturns=true;return f.args();},expected("returned",null,"boundaryCalls",1,"label",9,"firstCount",0,"secondCount",0));
    }
    static void resumedInputsAndCasts(){
        for(int label:new int[]{1,2})for(int code=0;code<8;code++){
            final int l=label,c=code;
            JsonObject exp=expected("firstCount",0,"secondCount",label==1&&code!=3&&code!=4?1:0,"logCount",code==3?1:0,"newContinuations",0,"newFactories",0,"listEmptyReads",0,"listIteratorReads",0,"otherListEmptyReads",0,"otherListIteratorReads",0,"savedIndex",13,"markerEqualsCalls",0);
            if(code==4)exception(exp,AssertionError.class);else exp.getAsJsonObject("widgetState").addProperty("returned","unit");
            check("widget-resumed-result:"+label+":"+code,()->{Fixture f=new Fixture(3,l);f.supplied.result=f.response(c);return f.args();},exp);
        }
        for(int label:new int[]{1,2})for(int field:new int[]{7,5,4,3,2,1,0})for(boolean wrong:new boolean[]{false,true}){
            final int l=label,n=field;JsonObject exp=wrong?exception(expected("boundaryCalls",0,"firstCount",0,"secondCount",0,"label",label),ClassCastException.class):null;
            check("widget-saved-cast:"+label+":"+field+":"+wrong,()->{Fixture f=new Fixture(3,l);f.saved(n,wrong?Integer.valueOf(839):null);return f.args();},exp);
        }
        for(int label:new int[]{0,1,2})for(int code=0;code<7;code++){
            final int l=label,c=code;
            check("widget-resumed-failure-type:"+label+":"+code,()->{Fixture f=new Fixture(3,l);f.supplied.result=new g3d(f.error(fault(c)));WidgetControl.name(f.supplied.result,"injected-result");return f.args();},null);
        }
        for(int phase:new int[]{Integer.MIN_VALUE,-1,0,1,2,Integer.MAX_VALUE})for(int index:new int[]{Integer.MIN_VALUE,-1,0,37,Integer.MAX_VALUE}){
            check("widget-saved-integers:"+phase+":"+index,()->{Fixture f=new Fixture(3,1);f.supplied.I$2=phase;f.supplied.I$0=index;return f.args();},expected("returned","unit","firstCount",0,"secondCount",1,"savedIndex",index,"savedPhase",phase,"savedId",417));
        }
        for(int label:new int[]{1,2}){
            check("widget-saved-unread-L6:"+label,()->{Fixture f=new Fixture(3,label);f.saved(6,new Object());WidgetControl.name(f.supplied.L$6,"arbitrary-unread-slot");return f.args();},expected("returned","unit","firstCount",0,"secondCount",label==1?1:0));
        }
    }
    static void nullsAndNumbers(){
        for(int slot=0;slot<3;slot++)for(boolean empty:new boolean[]{false,true}){
            final int s=slot;check("widget-null-input:"+slot+":"+empty,()->{Fixture f=new Fixture(1,0,empty?new Object[]{}:new Object[]{7});Object[] args=f.args();args[s]=null;return args;},null);
        }
        check("widget-null-iterator-outside-catch",()->{Fixture f=new Fixture(1,0,7);f.ids.iterator=null;return f.args();},exception(expected("firstCount",0,"secondCount",0,"logCount",0),NullPointerException.class));
        for(int value:new int[]{Integer.MIN_VALUE,-1,0,1,417,Integer.MAX_VALUE}){
            check("widget-number:"+value,()->{Fixture f=new Fixture(1,0);f.ids.values.add(f.number(value));f.provider(value,true);return f.args();},expected("returned","unit","backendReads",Arrays.asList(value),"savedId",value,"savedIndex",0,"firstCount",1,"secondCount",1));
        }
        for(Object value:new Object[]{Long.valueOf(Long.MAX_VALUE),Double.NaN,Double.POSITIVE_INFINITY,Float.NEGATIVE_INFINITY,Double.valueOf(-0.75),Byte.valueOf((byte)-128)}){
            int expected=((Number)value).intValue();check("widget-numeric-conversion:"+value,()->new Fixture(1,0,value).args(),expected("returned","unit","backendReads",Arrays.asList(expected),"savedId",expected));
        }
        for(Object value:new Object[]{null,"not-a-number",new Object()}){
            check("widget-wrong-element:"+(value==null?"null":value.getClass().getName()),()->new Fixture(1,0,value).args(),exception(expected("firstCount",0,"secondCount",0,"logCount",0),value==null?NullPointerException.class:ClassCastException.class));
        }
    }
    static void faults(){
        List<Supplier<Object[]>> paths=Arrays.asList(
                ()->make(1,0,0,0,7,8),()->make(3,1,0,0,7),()->make(3,2,0,0,7),
                ()->{Fixture f=new Fixture(1,0,7,8);f.provider(7,false);return f.args();},
                ()->make(1,0,3,0,7,8),()->make(1,0,0,3,7,8),
                ()->{Fixture f=new Fixture(3,1,8);f.supplied.result=f.response(3);return f.args();},
                ()->{Fixture f=new Fixture(3,2,8);f.supplied.result=f.response(3);return f.args();},
                ()->{Fixture f=new Fixture(1,0);f.ids.values.add(f.number(7));f.provider(7,true);return f.args();});
        for(int p=0;p<paths.size();p++){
            Supplier<Object[]> make=paths.get(p);List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int type=0;type<7;type++){
                final int a=at,t=type;check("widget-fault:"+p+":"+at+":"+type,()->{Object[] args=make.get();WidgetControl.failAt=a;WidgetControl.failure=fault(t);WidgetControl.name(WidgetControl.failure,"injected");return args;},null);
            }
        }
    }
    static void mutation(Fixture f,int kind){
        b state=WidgetControl.current;
        switch(kind){
            case 0:state.label=91;break;
            case 1:state.I$0=Integer.MAX_VALUE;state.I$1=Integer.MIN_VALUE;state.I$2=37;break;
            case 2:state.this$0=f.otherOwner;state.completion=null;break;
            case 3:state.L$0=f.otherContext;break;
            case 4:state.L$1="unused-list-wrong-type";state.L$4="unused-iterable-wrong-type";break;
            case 5:state.L$2=null;state.L$3=null;break;
            case 6:state.L$5=f.otherIds.iterator;break;
            case 7:state.L$6="mutated-L6";state.L$7=null;break;
            case 8:WidgetControl.backend=f.otherBackend;break;
            case 9:for(wx6 manager:WidgetControl.managers)manager.b=f.otherBackend;break;
            case 10:f.backend.providers.clear();break;
            case 11:f.backend.providers.put(7,new AppWidgetProviderInfo());break;
            case 12:f.ids.values.add(91);break;
            case 13:f.ids.values.clear();break;
            case 14:state.result=new g3d(f.error(new IOException("mutated saved result")));WidgetControl.name(state.result,"mutated-result");break;
            case 15:WidgetControl.firstResults.clear();WidgetControl.firstResults.add(v93.COROUTINE_SUSPENDED);break;
            case 16:WidgetControl.secondResults.clear();WidgetControl.secondResults.add(v93.COROUTINE_SUSPENDED);break;
            default:throw new AssertionError(kind);
        }
    }
    static void mutations(){
        List<Supplier<Object[]>> paths=Arrays.asList(()->make(1,0,0,0,7,8),()->make(3,1,0,0,8),()->make(3,2,0,0,8),()->make(1,0,3,0,7,8));
        for(int p=0;p<paths.size();p++){
            Supplier<Object[]> make=paths.get(p);List<String> calls=boundaries(make);
            for(int at=0;at<calls.size();at++)for(int kind=0;kind<17;kind++){
                final int a=at,k=kind;check("widget-mutation:"+p+":"+at+":"+kind,()->{Object[] args=make.get();Fixture f=current;WidgetControl.mutateAt=a;WidgetControl.mutation=()->mutation(f,k);return args;},null);
            }
        }
    }
    static void sequencesAndOrder(){
        check("widget-two-suspensions",()->{
            Fixture f=new Fixture(1,0,7);WidgetControl.firstResults.add(v93.COROUTINE_SUSPENDED);WidgetControl.secondResults.add(v93.COROUTINE_SUSPENDED);
            f.resumeInputs.add(blg.a);f.resumeInputs.add(blg.a);return f.args();
        },expected("returned","unit","firstCount",1,"secondCount",1,"newContinuations",1,"label",2,"savedIndex",0,"savedId",7,"savedPhase",0,"otherListEmptyReads",0,"otherListIteratorReads",0));
        check("widget-multiple-widgets-four-suspensions",()->{
            Fixture f=new Fixture(1,0,7,8);WidgetControl.firstResults.add(v93.COROUTINE_SUSPENDED);WidgetControl.firstResults.add(v93.COROUTINE_SUSPENDED);WidgetControl.secondResults.add(v93.COROUTINE_SUSPENDED);WidgetControl.secondResults.add(v93.COROUTINE_SUSPENDED);
            for(int i=0;i<4;i++)f.resumeInputs.add(blg.a);return f.args();
        },expected("returned","unit","firstCount",2,"secondCount",2,"newContinuations",1,"label",2,"savedIndex",0,"savedId",8,"backendReads",Arrays.asList(7,8)));
        for(int label:new int[]{1,2})for(int kind:new int[]{3,4}){
            check("widget-suspended-failure:"+label+":"+kind,()->{
                Fixture f=new Fixture(1,0,7,8);if(label==1)WidgetControl.firstResults.add(v93.COROUTINE_SUSPENDED);else WidgetControl.secondResults.add(v93.COROUTINE_SUSPENDED);
                f.resumeInputs.add(f.response(kind));return f.args();
            },kind==4?exception(expected("logCount",0,"escapedExternalIdentity",true),AssertionError.class):expected("returned","unit","logCount",1,"savedId",8,"savedIndex",0));
        }
        Supplier<Object[]> success=()->make(1,0,0,0,7);
        int factory=boundary(boundaries(success),"factory.new:");
        JsonObject factoryExpected=new JsonObject();factoryExpected.addProperty("identity","factory0");factoryExpected.addProperty("class","defpackage.zhh");factoryExpected.addProperty("arity",2);factoryExpected.add("completion",JsonNull.INSTANCE);
        check("widget-factory-arity-and-null-completion",success,expected("returned","unit","factories",Arrays.asList(factoryExpected)));
        check("widget-factory-before-state-clear",()->{Object[] args=success.get();WidgetControl.failAt=factory;WidgetControl.failure=new IOException("factory construction failed");WidgetControl.name(WidgetControl.failure,"injected");return args;},expected("returned","unit","label",0,"newFactories",1,"firstCount",0,"secondCount",0,"logCount",1));
        int initialize=boundary(boundaries(success),"widget.initialize:");
        check("widget-manager-backend-read-after-initialize",()->{Object[] args=success.get();Fixture f=current;WidgetControl.mutateAt=initialize;WidgetControl.mutation=()->{WidgetControl.backend=f.otherBackend;f.otherBackend.providers.put(7,new AppWidgetProviderInfo());};return args;},expected("returned","unit","backendReads",Collections.emptyList(),"otherBackendReads",Arrays.asList(7),"firstCount",1,"secondCount",1));
        check("widget-message-accessor-failure-escapes",()->{Fixture f=new Fixture(1,0,7);ObservedFailure failure=f.observed("first error");failure.messageFailure=f.error(new IOException("message accessor failed"));WidgetControl.firstResults.add(new g3d(failure));return f.args();},exception(expected("firstCount",1,"secondCount",0,"logCount",0,"escapedExternalIdentity",true,"exceptionMessage","message accessor failed"),IOException.class));
        check("widget-null-exception-message",()->{Fixture f=new Fixture(1,0,7);WidgetControl.firstResults.add(new g3d(f.observed(null)));return f.args();},expected("returned","unit","logs",Arrays.asList("Failed to update custom widget instance 7: null")));
        for(int label:new int[]{1,2}){
            check("widget-resume-captured-fields:"+label,()->{Fixture f=new Fixture(3,label);WidgetControl.mutateAt=0;WidgetControl.mutation=()->{f.supplied.L$0=f.otherContext;f.supplied.L$2=null;f.supplied.L$3=null;f.supplied.L$5=null;f.supplied.L$7=null;f.supplied.I$0=99;f.supplied.I$1=-3;f.supplied.I$2=42;};return f.args();},expected("returned","unit","firstCount",0,"secondCount",label==1?1:0,"logCount",0));
        }
    }
    static void run(){entryAndFlows();resumedInputsAndCasts();nullsAndNumbers();faults();mutations();sequencesAndOrder();}
}
