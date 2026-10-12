import com.google.gson.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;
import java.util.function.Supplier;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.*;
import com.arlosoft.macrodroid.triggers.*;
import com.arlosoft.macrodroid.action.WaitUntilTriggerAction;
import com.arlosoft.macrodroid.variables.*;
import com.arlosoft.macrodroid.events.ShowActionBlockTestSummaryEvent;
import com.arlosoft.macrodroid.actionblock.data.ActionBlock;
import defpackage.*;

/** Three-way tests of the actual migrated core bodies. NOT an Android emulator.
 * Macro storage, logging, configuration accessors, Android context and matching
 * helpers are explicitly controlled boundaries. Nested migrated bodies execute
 * through original instructions, Java, or rebuilt instructions, respectively.
 */
public final class CoreParityTests {
 static final Gson GSON=new GsonBuilder().setPrettyPrinting().create();
 static final Object SKIP=new Object();
 static final String P="Lcom/arlosoft/macrodroid/";
 static final String CTX="Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;";
 static final String CHECK=P+"macro/Macro;->canInvoke("+CTX+"ZZ)Z";
 static final String FORCED=P+"macro/Macro;->canInvoke("+CTX+"Z)Z";
 static final String SIMPLE=P+"macro/Macro;->canInvoke("+CTX+")Z";
 static final String LIGHT=P+"constraint/LightLevelConstraint;->X("+CTX+")Z";
 static final String RUNNING=P+"constraint/MacroRunningConstraint;->X("+CTX+")Z";
 static final String WEATHER=P+"triggers/WeatherTrigger;->z0("+P+"data/b;"+P+"data/b;)Z";
 static final String CATEGORY=P+"triggers/WeatherTrigger;->x0(I)I";
 static final String TEMPERATURE="Lcah;->a(Z)D";
 static final String VARIABLE=P+"variables/s0;->equals(Ljava/lang/Object;)Z";
 static final String SUMMARY=P+"events/ShowActionBlockTestSummaryEvent;->equals(Ljava/lang/Object;)Z";
 static BytecodeOracle original,rebuilt;
 static Map<String,JsonObject> registry=new TreeMap<>();
 static Set<String> visited=new TreeSet<>();
 static Map<String,Integer> families=new TreeMap<>(),exceptions=new TreeMap<>();
 static List<JsonObject> failures=new ArrayList<>();
 static int cases,mismatches,unsupported,expectedChecks,expectedFailures;
 static JsonElement canon(Object v){
  if(v==null)return JsonNull.INSTANCE;
  if(v instanceof Double)return new JsonPrimitive("double:"+Long.toHexString(Double.doubleToLongBits((Double)v)));
  if(v instanceof Float)return new JsonPrimitive("float:"+Integer.toHexString(Float.floatToIntBits((Float)v)));
  return GSON.toJsonTree(v);
 }
 static List<String> types(String signature){return ParityTests.types(signature);}
 static Object javaCall(String key,Object[] args) throws Throwable {
  JsonObject e=registry.get(key);
  String descriptor=e.get("helper_method").getAsString()+"("+(e.get("instance").getAsBoolean()?e.get("target").getAsString():"")+e.get("method").getAsString().split("\\(",2)[1];
  List<String> ts=types(descriptor);Class<?>[] cs=new Class<?>[ts.size()];for(int i=0;i<cs.length;i++)cs[i]=BytecodeOracle.type(ts.get(i));
  try{return BytecodeOracle.type(e.get("helper").getAsString()).getDeclaredMethod(e.get("helper_method").getAsString(),cs).invoke(null,args);}
  catch(InvocationTargetException ex){throw ex.getCause();}
 }
 static JsonObject outcome(String key,String path,Supplier<Object[]> make){
  JsonObject out=new JsonObject();
  Macro.sMacroDroidEnabled=true;rl9.a=new rl9();rl9.debugging=false;com.arlosoft.macrodroid.macro.b.k=new vq9();
  Object[] args=make.get();CoreTrace.reset();sr9.calls.clear();
  try{
   Object value=path.equals("original")?original.invoke(key,args):path.equals("rebuilt")?rebuilt.invoke(key,args):javaCall(key,args);
   out.add("value",canon(value));
  }catch(Throwable ex){
   out.addProperty("exception",ex.getClass().getName());
   if(path.equals("original"))exceptions.merge(ex.getClass().getName(),1,Integer::sum);
   if(ex instanceof BytecodeOracle.Unsupported || !(ex instanceof NullPointerException || ex instanceof ClassCastException || ex instanceof IllegalStateException)){
    unsupported++;out.addProperty("unsupported",ex.toString());
   }
  }
  out.add("boundaryOrder",GSON.toJsonTree(CoreTrace.calls));
  out.add("expansionCalls",GSON.toJsonTree(sr9.calls));
  if(args.length>0&&args[0] instanceof Macro){
   Macro m=(Macro)args[0];JsonArray assigned=new JsonArray();
   if(m.m_constraintList!=null)for(Object x:m.m_constraintList)if(x instanceof Constraint)assigned.add(((Constraint)x).macro==m);
   out.add("assignedToInvokingMacro",assigned);
  }
  return out;
 }
 static void check(String key,String label,Supplier<Object[]> make,Object expected){
  cases++;visited.add(key);families.merge(key,1,Integer::sum);
  JsonObject a=outcome(key,"original",make),b=outcome(key,"java",make),c=rebuilt==null?null:outcome(key,"rebuilt",make);
  boolean expectedBad=false;
  if(expected!=SKIP){expectedChecks++;expectedBad=!a.has("value")||!a.get("value").equals(canon(expected));if(expectedBad)expectedFailures++;}
  if(expectedBad||!a.equals(b)||(c!=null&&!a.equals(c))||a.has("unsupported")||b.has("unsupported")||(c!=null&&c.has("unsupported"))){
   mismatches++;if(failures.size()<60){JsonObject f=new JsonObject();f.addProperty("method",key);f.addProperty("case",label);f.add("original",a);f.add("java",b);if(c!=null)f.add("rebuilt",c);if(expected!=SKIP)f.add("expected",canon(expected));failures.add(f);}
  }
 }
 static Constraint constraint(int i,boolean enabled,boolean result,boolean silent){Constraint c=new Constraint();c.testId="constraint"+i;c.configured="configured"+i;c.system="system"+i;c.enabled=enabled;c.result=result;c.loggingDisabled=silent;return c;}
 static Object[] gate(int flags,int pattern,int contextKind,int waitKind,String method){
  Macro m=new Macro();m.isActionBlock=(flags&1)!=0;rl9.debugging=(flags&2)!=0;Macro.sMacroDroidEnabled=(flags&4)!=0;m.categoryDisabled=(flags&8)!=0;m.orMode=(flags&16)!=0;m.detailExcluded=(flags&32)!=0;
  Trigger t=new Trigger();t.testId="trigger";t.configured="motion";t.system="motion-system";
  TriggerContextInfo c=contextKind==0?null:new TriggerContextInfo();if(c!=null)c.trigger=contextKind==2?null:t;
  m.m_triggerList.add(new Trigger());m.m_triggerList.add(t);
  switch(pattern){
   case 1:m.m_constraintList.add(constraint(0,true,false,false));break;
   case 2:m.m_constraintList.add(constraint(0,true,true,false));break;
   case 3:m.m_constraintList.add(constraint(0,false,false,false));break;
   case 4:m.m_constraintList.add(constraint(0,false,false,true));m.m_constraintList.add(constraint(1,true,false,false));break;
   case 5:m.m_constraintList.add(constraint(0,true,false,false));m.m_constraintList.add(constraint(1,true,true,false));break;
   case 6:m.m_constraintList.add(constraint(0,true,true,false));m.m_constraintList.add(constraint(1,true,false,false));break;
   case 7:m.m_constraintList.add(constraint(0,false,false,true));m.m_constraintList.add(constraint(1,false,true,false));break;
   case 8:m.m_constraintList.add(constraint(0,true,false,false));m.m_constraintList.add(constraint(1,true,false,false));break;
   case 9:m.m_constraintList=null;break;
   case 10:m.m_constraintList.add(null);break;
   case 11:Constraint x=constraint(0,true,false,false);x.failure=new IllegalStateException("fixture constraint");m.m_constraintList.add(x);break;
   case 12:Constraint n=constraint(0,true,false,false);n.configured=null;m.m_constraintList.add(n);m.m_constraintList.add(constraint(1,true,false,false));break;
  }
  if(waitKind>0){m.actionWaitingForTriggerActive=new WaitUntilTriggerAction();if(waitKind==1)m.actionWaitingForTriggerActive.triggers.add(t);if(waitKind==2)m.actionWaitingForTriggerActive.triggers.add(null);if(waitKind==3)m.actionWaitingForTriggerActive.triggers=null;}
  if(method.equals(SIMPLE))return new Object[]{m,c};
  if(method.equals(FORCED))return new Object[]{m,c,(flags&64)!=0};
  return new Object[]{m,c,(flags&64)!=0,(flags&128)!=0};
 }
 static Object gateExpected(int flags,int pattern,int context){
  if((flags&1)!=0)return true;
  if((flags&2)!=0)return context==1?false:SKIP;
  if((flags&64)==0&&(flags&4)==0)return false;
  if((flags&8)!=0)return false;
  if(pattern==0||pattern==3||pattern==7)return true;
  if((flags&16)!=0)return pattern==2||pattern==5||pattern==6;
  return pattern==2;
 }
 static void macros(){
  for(int f=0;f<256;f++)for(int p=0;p<9;p++)for(int c=0;c<3;c++){final int flags=f,pattern=p,context=c;check(CHECK,f+":"+p+":"+c,()->gate(flags,pattern,context,0,CHECK),gateExpected(f,p,c));}
  for(int f=0;f<256;f+=3)for(int p=0;p<9;p++)for(int c=0;c<3;c++){final int flags=f,pattern=p,context=c;check(FORCED,f+":"+p+":"+c,()->gate(flags,pattern,context,0,FORCED),SKIP);}
  for(int f=0;f<256;f+=7)for(int p=0;p<9;p++)for(int c=0;c<3;c++)for(int w=0;w<3;w++){final int flags=f,pattern=p,context=c,wait=w;check(SIMPLE,f+":"+p+":"+c+":"+w,()->gate(flags,pattern,context,wait,SIMPLE),SKIP);}
  for(int p=9;p<=12;p++)for(int f:new int[]{4,20,132,148})for(int c=0;c<3;c++){final int flags=f,pattern=p,context=c;check(CHECK,"failure:"+f+":"+p+":"+c,()->gate(flags,pattern,context,0,CHECK),SKIP);}
 }
 static void light(){
  float[] values={Float.NEGATIVE_INFINITY,-Float.MAX_VALUE,-1f,-0f,0f,Float.MIN_VALUE,1f,Math.nextDown(10f),10f,Math.nextUp(10f),Float.MAX_VALUE,Float.POSITIVE_INFINITY,Float.NaN};
  for(int option:new int[]{-2,-1,0,1,2,100})for(int legacy:new int[]{-1,0,1,-2,Integer.MIN_VALUE,Integer.MAX_VALUE})for(float threshold:values)for(float current:values){
   float t=legacy==-1?threshold:(float)legacy;boolean expected=option==0?current<t:option==1&&current>t;
   check(LIGHT,option+":"+legacy+":"+threshold+":"+current,()->{LightLevelConstraint x=new LightLevelConstraint();x.m_option=option;x.m_lightLevel=legacy;x.m_lightLevelFloat=threshold;LightLevelConstraint.s_lightLevel=current;return new Object[]{x,null};},expected);
  }
 }
 static com.arlosoft.macrodroid.data.b weatherData(double value,int humidity,int direction,int[] codes){
  var b=new com.arlosoft.macrodroid.data.b();b.b.a=value;b.c.a=value;b.e=humidity;b.f=direction;for(int code:codes)b.a.add(new com.arlosoft.macrodroid.data.b.a(code));return b;
 }
 static double converted(double k,boolean celsius){double c=k-273.15;return celsius?c:((c*9.0)/5.0)+32.0;}
 static void weather(){
  for(int n=-20;n<=1200;n++){final int code=n;int expected=n>=200&&n<=232?3:n>=300&&n<=531?2:n>=600&&n<=622?4:n>=800&&n<=801?0:n>=802&&n<=804?1:-1;check(CATEGORY,"code:"+n,()->new Object[]{code},expected);}
  for(int code:new int[]{Integer.MIN_VALUE,Integer.MAX_VALUE})check(CATEGORY,"bound:"+code,()->new Object[]{code},-1);
  double[] values={Double.NEGATIVE_INFINITY,-Double.MAX_VALUE,-1.0,-0.0,0.0,Double.MIN_VALUE,Math.nextDown(10.0),10.0,Math.nextUp(10.0),273.15,283.15,Double.MAX_VALUE,Double.POSITIVE_INFINITY,Double.NaN};
  for(double v:values)for(boolean c:new boolean[]{false,true})check(TEMPERATURE,v+":"+c,()->new Object[]{new cah(v),c},converted(v,c));
  Random random=new Random(640510L);for(int i=0;i<512;i++){final double v=Double.longBitsToDouble(random.nextLong());final boolean c=i%2==0;check(TEMPERATURE,"raw:"+i,()->new Object[]{new cah(v),c},converted(v,c));}
  for(int option:new int[]{0,1})for(double old:values)for(double now:values)for(int threshold:new int[]{-10,0,10})for(boolean direction:new boolean[]{false,true})for(boolean absent:new boolean[]{false,true})for(boolean extra:new boolean[]{false,true}){
   double before=option==0?converted(old,extra):old,after=option==0?converted(now,extra):now;
   double boundary=option==1&&extra?22.0/2.23694:(double)threshold;
   boolean below=option==0?direction:!direction;
   boolean expected=below?(after<=boundary&&(absent||before>boundary)):(after>=boundary&&(absent||before<boundary));
   check(WEATHER,"numeric:"+option+":"+old+":"+now+":"+threshold+":"+direction+":"+absent+":"+extra,()->{
    WeatherTrigger w=new WeatherTrigger();w.m_option=option;w.m_temperature=threshold;w.m_tempBelow=direction;w.m_tempCelcius=extra;w.m_windSpeedAbove=direction;w.m_windSpeedValue=threshold;w.m_windSpeedValueMph=extra?22:0;
    return new Object[]{w,absent?null:weatherData(old,0,0,new int[0]),weatherData(now,0,0,new int[0])};
   },expected);
  }
  for(int old:new int[]{Integer.MIN_VALUE,-1,0,49,50,51,101,Integer.MAX_VALUE})for(int now:new int[]{Integer.MIN_VALUE,-1,0,49,50,51,101,Integer.MAX_VALUE})for(int threshold:new int[]{0,50,100})for(boolean above:new boolean[]{false,true})for(boolean absent:new boolean[]{false,true}){
   boolean expected=above?(now>=threshold&&(absent||old<threshold)):(now<=threshold&&(absent||old>threshold));
   check(WEATHER,"humidity:"+old+":"+now+":"+threshold+":"+above+":"+absent,()->{WeatherTrigger w=new WeatherTrigger();w.m_option=2;w.m_humidityAbove=above;w.m_humidityValue=threshold;return new Object[]{w,absent?null:weatherData(0,old,0,new int[0]),weatherData(0,now,0,new int[0])};},expected);
  }
  int[][] codeSets={{},{200},{300,500},{600},{800},{802,804},{999},{200,600},{200,200}};
  for(int[] before:codeSets)for(int[] after:codeSets)for(int choice=-1;choice<6;choice++)for(boolean absent:new boolean[]{false,true}){
   final int selected=choice;Set<Integer> oldSet=new HashSet<>(),newSet=new HashSet<>();if(!absent)for(int x:before)oldSet.add(recovered.core.WeatherMethods.category(x));for(int x:after)newSet.add(recovered.core.WeatherMethods.category(x));
   check(WEATHER,"conditions:"+Arrays.toString(before)+":"+Arrays.toString(after)+":"+choice+":"+absent,()->{WeatherTrigger w=new WeatherTrigger();w.m_option=3;w.m_weatherCondition=selected;return new Object[]{w,absent?null:weatherData(0,0,0,before),weatherData(0,0,0,after)};},!oldSet.contains(choice)&&newSet.contains(choice));
  }
  for(int option:new int[]{-1,0,1,2,3,4,5,6,Integer.MAX_VALUE})for(int a=0;a<3;a++)for(int b=0;b<3;b++){final int old=a,now=b;check(WEATHER,"null:"+option+":"+a+":"+b,()->{WeatherTrigger w=new WeatherTrigger();w.m_option=option;var p=old==0?null:weatherData(1,2,old,new int[]{200});var q=now==0?null:weatherData(1,2,now,new int[]{200});if(old==2){p.a=null;p.b=null;p.c=null;}if(now==2){q.a=null;q.b=null;q.c=null;}return new Object[]{w,p,q};},option<0||option==4||option>5?true:SKIP);}
 }
 static void running(){
  for(String text:new String[]{null,"","macro","needle","missing"})for(int option:new int[]{-2,0,1,2})for(int match:new int[]{-1,0,1})for(long id:new long[]{-1,0,7,Long.MIN_VALUE,Long.MAX_VALUE})for(int mode=0;mode<9;mode++){
   final int scenario=mode;check(RUNNING,text+":"+option+":"+match+":"+id+":"+mode,()->{
    MacroRunningConstraint c=new MacroRunningConstraint();c.testId="runningConstraint";c.textToMatch=text;c.option=option;c.matchOption=match;c.macroId=id;c.macroName="named";
    Macro first=new Macro();first.name="needle macro";first.testId="first";first.running=scenario%2==0;
    Macro second=new Macro();second.name="needle macro";second.testId="second";second.running=!first.running;
    Macro host=new Macro();host.testId="owner";host.running=scenario%2!=0;c.macro=scenario==5?null:host;
    var store=com.arlosoft.macrodroid.macro.b.k.store;
    if(scenario!=0){store.macros.add(first);store.macros.add(second);}if(scenario==8)store.macros.add(0,null);
    store.byId=scenario==1?first:null;store.byName=scenario==2?second:null;
    if(scenario==6)c.context=null;if(scenario==7)com.arlosoft.macrodroid.macro.b.k=null;
    return new Object[]{c,new TriggerContextInfo()};
   },SKIP);
  }
 }
 static void equality(){
  for(int a=0;a<6;a++)for(int b=0;b<6;b++)for(int mode=0;mode<6;mode++){final int left=a,right=b,kind=mode;check(VARIABLE,a+":"+b+":"+mode,()->{
   s0 x=new s0(),y=new s0();var d1=new VariableValue.DictionaryEntry("key",null,null);var d2=new VariableValue.DictionaryEntry("key",null,null);
   x.a=left==0?null:d1;y.a=right==0?null:(right%2==0?d1:d2);x.b=left==1?null:new String("v"+(left%2));y.b=right==1?null:new String("v"+(right%2));x.c=left;y.c=right;
   return new Object[]{x,kind==0?x:kind==1?null:kind==2?"wrong type":kind==3?y:kind==4?new Object():y};
  },mode==0?true:mode==1||mode==2||mode==4?false:SKIP);}
  for(int a=0;a<8;a++)for(int b=0;b<8;b++)for(int mode=0;mode<5;mode++){final int left=a,right=b,kind=mode;check(SUMMARY,a+":"+b+":"+mode,()->{
   ShowActionBlockTestSummaryEvent x=new ShowActionBlockTestSummaryEvent(),y=new ShowActionBlockTestSummaryEvent();ActionBlock shared=new ActionBlock();x.a=left==0?null:shared;y.a=right==0?null:right%2==0?shared:new ActionBlock();
   x.b=left==1?null:new ArrayList<>(Arrays.asList("b",left%2));y.b=right==1?null:new ArrayList<>(Arrays.asList("b",right%2));x.c=left==2?null:List.of("c",left%3);y.c=right==2?null:List.of("c",right%3);
   return new Object[]{x,kind==0?x:kind==1?null:kind==2?new Object():y};
  },mode==0?true:mode==1||mode==2?false:SKIP);}
 }
 public static void main(String[] args)throws Exception{
  Path root=Paths.get(args[0]);for(JsonElement v:JsonParser.parseString(Files.readString(root.resolve("source/core-methods.json"))).getAsJsonArray()){JsonObject e=v.getAsJsonObject();registry.put(e.get("target").getAsString()+"->"+e.get("method").getAsString(),e);}
  original=new BytecodeOracle(root.resolve("tests/fixtures/original-methods.dex"),registry.keySet());if(original.methods.size()!=registry.size())throw new IllegalStateException("Missing original core methods");
  if(args.length>1){rebuilt=new BytecodeOracle();try(var paths=Files.list(Paths.get(args[1]))){for(Path path:paths.filter(p->p.toString().endsWith(".dex")).toList())rebuilt.add(path,registry.keySet());}if(rebuilt.methods.size()!=registry.size())throw new IllegalStateException("Missing rebuilt core methods");}
  Locale saved=Locale.getDefault();Locale.setDefault(Locale.ROOT);try{macros();light();weather();running();equality();}finally{Locale.setDefault(saved);}
  JsonObject report=new JsonObject();report.addProperty("passed",mismatches==0&&unsupported==0&&visited.equals(registry.keySet()));report.addProperty("cases",cases);report.addProperty("failedCases",mismatches);report.addProperty("unsupportedExecutions",unsupported);report.addProperty("independentExpectedResultChecks",expectedChecks);report.addProperty("expectedResultFailures",expectedFailures);report.addProperty("methodsCovered",visited.size());report.add("methodKeys",GSON.toJsonTree(visited));report.addProperty("paths",rebuilt==null?2:3);report.addProperty("androidRuntime",false);report.add("methods",GSON.toJsonTree(families));report.add("expectedInputExceptions",GSON.toJsonTree(exceptions));report.add("failures",GSON.toJsonTree(failures));
  JsonObject coverage=new JsonObject();for(String key:registry.keySet()){JsonObject x=new JsonObject();int total=0;for(var instruction:original.methods.get(key).getImplementation().getInstructions())total++;x.addProperty("originalInstructions",total);x.addProperty("executedOriginalInstructionOffsets",original.executed.getOrDefault(key,Set.of()).size());x.addProperty("observedOriginalBranchEdges",original.branchEdges.getOrDefault(key,Set.of()).size());coverage.add(key,x);}report.add("boundedInstructionCoverage",coverage);
  report.addProperty("scope","Original selected instructions vs Java vs rebuilt selected instructions. CoreTrace records boundary order/logs and macro assignment effects. Store lookup, pattern matching, context, configuration accessors, debugger state and DictionaryEntry equality are controlled host boundaries. No Android, services, UI, persistence or concurrency proof.");
  Files.writeString(root.resolve("reports/java-core-"+(rebuilt==null?"two":"three")+"-path-parity.json"),GSON.toJson(report));System.out.println("core cases="+cases+" methods="+visited.size()+" mismatches="+mismatches+" unsupported="+unsupported+" expectedChecks="+expectedChecks);if(!report.get("passed").getAsBoolean())System.exit(2);
 }
}
