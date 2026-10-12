import com.google.gson.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;
import java.math.*;
import java.time.*;
import java.util.function.Supplier;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.*;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import android.net.wifi.*;
import defpackage.*;

/** Original selected DEX / recovered Java / rebuilt DEX, under controlled host
 * Android services and a deterministic clock. NOT Android or an ART emulator.
 * Matching, long parsing and solar mathematics execute as real migrated bodies,
 * including nested calls. Android providers, permissions, radio data and locations
 * are test doubles. Only host-loaded recovered code receives the test clock agent.
 */
public final class EnvironmentParityTests {
 static final Gson JSON=new GsonBuilder().setPrettyPrinting().create();
 static final Object SKIP=new Object();
 static final String C="Lcom/arlosoft/macrodroid/constraint/", CTX="Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;";
 static final String SET=C+"SystemSettingConstraint;->X("+CTX+")Z", INTS=C+"SystemSettingConstraint;->r0(J"+CTX+")Z", TEXT=C+"SystemSettingConstraint;->t0(Ljava/lang/String;"+CTX+")Z";
 static final String WIFI=C+"WifiConstraint;->X("+CTX+")Z", HOT=C+"WifiHotSpotConstraint;->X("+CTX+")Z", SUN=C+"SunsetSunriseConstraint;->X("+CTX+")Z";
 static final String CONTAINS="Lyih;->a(Ljava/lang/String;Z)Ljava/lang/String;", CONTAINS_SELECT="Lyih;->b(Ljava/lang/String;ZZ)Ljava/lang/String;", FULL="Lyih;->c(Ljava/lang/String;ZZ)Ljava/lang/String;", MATCH="Lyih;->d(Ljava/lang/String;Ljava/lang/String;ZZ)Z";
 static final String PARSE="Lg9f;->v1(Ljava/lang/String;)Ljava/lang/Long;", ROUND="Ln7b;->M(Ljava/math/BigDecimal;)Ljava/math/BigDecimal;", RAD="Ln7b;->z(Ljava/math/BigDecimal;)Ljava/math/BigDecimal;", CAL="Ln7b;->D(Ljava/math/BigDecimal;Ljava/util/Calendar;)Ljava/util/Calendar;", HOUR="Ln7b;->v(Lsrh;Ljava/util/Calendar;Z)Ljava/math/BigDecimal;";
 static final String GATE=CoreParityTests.CHECK, FORCED=CoreParityTests.FORCED, SIMPLE=CoreParityTests.SIMPLE;
 static BytecodeOracle original,rebuilt;
 static final Map<String,JsonObject> registry=new TreeMap<>();
 static final Set<String> expectedKeys=new TreeSet<>(),visited=new TreeSet<>();
 static final Map<String,Integer> groups=new TreeMap<>(),exceptions=new TreeMap<>();
 static final List<JsonObject> failures=new ArrayList<>();
 static int cases,failed,unsupported,expectedChecks,expectedFailures;
 static boolean normalizeVmMessage;
 static final String[] ZONES={"UTC","America/Halifax","America/New_York","Europe/Berlin","Asia/Kathmandu","Pacific/Chatham","Australia/Lord_Howe","Pacific/Apia"};
 static final long BASE=Instant.parse("2026-06-21T12:00:00Z").toEpochMilli();
 static final String[] NUMBERS={null,"","0","-0","+0","1","-1","2147483647","2147483648","-2147483648","-2147483649","9223372036854775807","9223372036854775808","-9223372036854775808","-9223372036854775809","+9223372036854775807","1.0","1e3"," 1","1 ","\t1","+","-","--1","++1","−1","١٢٣","１２３","१२३","00","0x10","1_000","\u00001","NaN","Infinity","1f"};
 static void reset(){EnvironmentControl.reset();Macro.sMacroDroidEnabled=true;rl9.a=new rl9();rl9.debugging=false;com.arlosoft.macrodroid.macro.b.k=new vq9();CoreTrace.reset();sr9.calls.clear();normalizeVmMessage=false;}
 static Calendar date(long epoch,String zone){Calendar c=Calendar.getInstance(TimeZone.getTimeZone(zone),Locale.ROOT);c.setTimeInMillis(epoch);return c;}
 static JsonElement canon(Object value){
  if(value==null)return JsonNull.INSTANCE;
  if(value instanceof BigDecimal){BigDecimal b=(BigDecimal)value;JsonObject o=new JsonObject();o.addProperty("decimal",b.toPlainString());o.addProperty("scale",b.scale());return o;}
  if(value instanceof Calendar){Calendar c=(Calendar)value;JsonObject o=new JsonObject();o.addProperty("millis",c.getTimeInMillis());o.addProperty("zone",c.getTimeZone().getID());o.addProperty("lenient",c.isLenient());o.addProperty("firstDay",c.getFirstDayOfWeek());return o;}
  if(value instanceof Double)return new JsonPrimitive("double:"+Long.toHexString(Double.doubleToLongBits((Double)value)));
  if(value instanceof Float)return new JsonPrimitive("float:"+Integer.toHexString(Float.floatToIntBits((Float)value)));
  return JSON.toJsonTree(value);
 }
 static Object javaCall(String key,Object[] args)throws Throwable{
  JsonObject e=registry.get(key);String signature=e.get("helper_method").getAsString()+"("+(e.get("instance").getAsBoolean()?e.get("target").getAsString():"")+e.get("method").getAsString().split("\\(",2)[1];
  List<String> descriptors=ParityTests.types(signature);Class<?>[] types=new Class<?>[descriptors.size()];for(int i=0;i<types.length;i++)types[i]=BytecodeOracle.type(descriptors.get(i));
  try{return BytecodeOracle.type(e.get("helper").getAsString()).getDeclaredMethod(e.get("helper_method").getAsString(),types).invoke(null,args);}catch(InvocationTargetException ex){throw ex.getCause();}
 }
 static JsonObject outcome(String key,String path,Supplier<Object[]> make){
  reset();Object[] args=make.get();Object oldList=args.length>0&&args[0] instanceof WifiConstraint?((WifiConstraint)args[0]).m_SSIDList:null;
  CoreTrace.reset();sr9.calls.clear();JsonObject o=new JsonObject();
  try{Object v=path.equals("original")?original.invoke(key,args):path.equals("rebuilt")?rebuilt.invoke(key,args):javaCall(key,args);o.add("value",canon(v));if(key.equals(CAL))o.addProperty("returnsBaseIdentity",v!=null&&v==args[1]);}
  catch(Throwable ex){
   o.addProperty("exception",ex.getClass().getName());if(path.equals("original"))exceptions.merge(ex.getClass().getName(),1,Integer::sum);
   if(ex instanceof BytecodeOracle.Unsupported || ex instanceof ReflectiveOperationException || ex instanceof LinkageError || ex instanceof java.lang.reflect.InaccessibleObjectException){unsupported++;o.addProperty("unsupported",ex.toString());}
  }
  List<String> trace=new ArrayList<>();for(String s:CoreTrace.calls){if(normalizeVmMessage&&s.contains("Error getting wifi AP State: "))s=s.substring(0,s.indexOf("Error getting wifi AP State: "))+"Error getting wifi AP State: <VM-generated message excluded>";trace.add(s);}o.add("boundaryOrder",JSON.toJsonTree(trace));
  o.add("expansionCalls",JSON.toJsonTree(sr9.calls));
  if(args.length>0&&args[0] instanceof WifiConstraint){WifiConstraint w=(WifiConstraint)args[0];o.add("ssidList",JSON.toJsonTree(w.m_SSIDList));o.addProperty("listIdentityRetained",oldList==w.m_SSIDList);}
  JsonArray calendars=new JsonArray();for(Object x:args)if(x instanceof Calendar)calendars.add(canon(x));if(calendars.size()>0)o.add("calendarArgumentsAfter",calendars);
  if(args.length>0&&args[0] instanceof Macro){Macro m=(Macro)args[0];JsonArray assigned=new JsonArray();for(Object c:m.m_constraintList)assigned.add(((Constraint)c).macro==m);o.add("macroAssigned",assigned);}
  return o;
 }
 static void check(String key,String label,Supplier<Object[]> make,Object expected){
  cases++;visited.add(key);groups.merge(key,1,Integer::sum);
  JsonObject a=outcome(key,"original",make),b=outcome(key,"java",make),c=rebuilt==null?null:outcome(key,"rebuilt",make);
  boolean bad=false;if(expected!=SKIP){expectedChecks++;bad=expected instanceof Class? !a.has("exception")||!a.get("exception").getAsString().equals(((Class<?>)expected).getName()):!a.has("value")||!a.get("value").equals(canon(expected));if(bad)expectedFailures++;}
  if(bad||!a.equals(b)||(c!=null&&!a.equals(c))||a.has("unsupported")||b.has("unsupported")||(c!=null&&c.has("unsupported"))){failed++;if(failures.size()<80){JsonObject f=new JsonObject();f.addProperty("method",key);f.addProperty("case",label);f.add("original",a);f.add("java",b);if(c!=null)f.add("rebuilt",c);if(expected!=SKIP)f.add("expected",expected instanceof Class?new JsonPrimitive(((Class<?>)expected).getName()):canon(expected));failures.add(f);}}
 }
 static SystemSettingConstraint setting(int type,int table,int operator,String wanted){SystemSettingConstraint s=new SystemSettingConstraint();s.valueType=type;s.tableOption=table;s.equalityCheckOption=operator;s.valueString=wanted;return s;}
 static Long parseExpected(String text){if(text==null||text.length()==0)return null;try{return Long.valueOf(text);}catch(NumberFormatException ex){return null;}}
 static boolean compare(long value,long threshold,int mode){return mode==0?value==threshold:mode==2?value<threshold:mode==3?value>threshold:value!=threshold;}
 static void integers(){
  for(String n:NUMBERS)check(PARSE,"parse "+n,()->new Object[]{n},n==null?NullPointerException.class:parseExpected(n));
  Random random=new Random(0x7a110cedL);for(int i=0;i<1200;i++){long n=random.nextLong();String s=Long.toString(n);check(PARSE,"generated "+i,()->new Object[]{s},n);String overflow=s+"9";check(PARSE,"overflow "+i,()->new Object[]{overflow},parseExpected(overflow));}
  long[] values={Long.MIN_VALUE,Long.MIN_VALUE+1,Integer.MIN_VALUE,-1,0,1,Integer.MAX_VALUE,Long.MAX_VALUE-1,Long.MAX_VALUE};
  for(String n:NUMBERS)for(long v:values)for(int mode:new int[]{-1,0,1,2,3,4})check(INTS,"integer "+n+" / "+v+" / "+mode,()->new Object[]{setting(2,0,mode,n),v,new TriggerContextInfo()},n==null?NullPointerException.class:compare(v,parseExpected(n)==null?0:parseExpected(n),mode));
 }
 static void settings(){
  for(int type:new int[]{-1,0,1,2,3,4})for(int table:new int[]{-1,0,1,2,3})for(int operator:new int[]{-1,0,1,2,3,4})for(String error:new String[]{null,"missing","security","illegal"}){
   Object expect=type<0||type>3?true:table<0||table>2?IllegalArgumentException.class:"illegal".equals(error)?IllegalStateException.class:error!=null?false:type==3?(operator==0||operator==2):compare(0,0,operator);
   check(SET,"provider "+type+"/"+table+"/"+operator+"/"+error,()->{SystemSettingConstraint s=setting(type,table,operator,"0");s.context.resolver.text="0";s.context.resolver.failure=error;return new Object[]{s,new TriggerContextInfo()};},expect);
  }
  float[] values={Float.NEGATIVE_INFINITY,-Float.MAX_VALUE,-1f,-0.0f,0f,Float.MIN_VALUE,1f,Math.nextUp(1f),Float.MAX_VALUE,Float.POSITIVE_INFINITY,Float.NaN};
  String[] thresholds={"-Infinity","-3.4028235E38","-1","-0","0","1.4E-45","1","1.0000001","3.4028235E38","Infinity","NaN","bad",null,""};
  for(float v:values)for(String threshold:thresholds)for(int mode:new int[]{-1,0,1,2,3,4})for(int table:new int[]{0,1,2}){
   float p=0;try{p=Float.parseFloat(threshold);}catch(Exception ignored){}final float t=p;
   Object expected=threshold==null?NullPointerException.class:mode==0?v==t:mode==2?v<t:mode==3?v>t:v!=t;
   check(SET,"float "+v+"/"+threshold+"/"+mode+"/"+table,()->{SystemSettingConstraint s=setting(1,table,mode,threshold);s.context.resolver.floating=v;return new Object[]{s,null};},expected);
  }
  for(int type:new int[]{0,2})for(String n:NUMBERS)for(int mode:new int[]{0,1,2,3})check(SET,"numeric provider "+type+"/"+n+"/"+mode,()->{SystemSettingConstraint s=setting(type,1,mode,n);s.context.resolver.integer=-17;s.context.resolver.longValue=Long.MIN_VALUE;return new Object[]{s,null};},n==null?NullPointerException.class:compare(type==0?-17:Long.MIN_VALUE,parseExpected(n)==null?0:parseExpected(n),mode));
  for(int type=0;type<4;type++){final int t=type;
   check(SET,"name expansion outside handler "+t,()->{SystemSettingConstraint s=setting(t,0,0,"0");s.expansionFailureInput=s.settingString;s.expansionFailure=new SecurityException("name expansion");return new Object[]{s,null};},SecurityException.class);
   check(SET,"value expansion inside handler "+t,()->{SystemSettingConstraint s=setting(t,0,0,"threshold");s.context.resolver.text="0";s.expansionFailureInput="threshold";s.expansionFailure=new SecurityException("value expansion");return new Object[]{s,null};},false);
   check(SET,"null context "+t,()->{SystemSettingConstraint s=setting(t,0,0,"0");s.context=null;return new Object[]{s,null};},NullPointerException.class);
   check(SET,"magic expansion "+t,()->{SystemSettingConstraint s=setting(t,2,0,"wanted");s.settingString="setting";s.expansions.put("setting","expanded setting");s.expansions.put("wanted","12");s.context.resolver.integer=12;s.context.resolver.longValue=12;s.context.resolver.floating=12;s.context.resolver.text="12";return new Object[]{s,null};},true);
  }
  check(SET,"string setting missing null",()->{SystemSettingConstraint s=setting(3,0,0,"x");return new Object[]{s,null};},false);
 }
 static void matching(){
  String[] texts={null,"","hello","HELLO","hello\nworld","Iİıi","Straße","[x]","(x)+","a.b","a*b","a?b","\\","$x","^$",".*","..*","a**b","a\u0000b","𝄞","x\r\ny"};
  Locale[] locales={Locale.ROOT,Locale.forLanguageTag("tr-TR"),Locale.GERMAN};
  for(Locale locale:locales){Locale.setDefault(locale);
   for(String text:texts)for(boolean ignoreCase:new boolean[]{false,true}){
    check(CONTAINS,"wildcard contains "+locale+"/"+text+"/"+ignoreCase,()->new Object[]{text,ignoreCase},text==null?NullPointerException.class:SKIP);
    for(boolean regex:new boolean[]{false,true}){check(CONTAINS_SELECT,"contains "+locale+"/"+text+"/"+regex+"/"+ignoreCase,()->new Object[]{text,regex,ignoreCase},text==null?NullPointerException.class:SKIP);check(FULL,"full "+locale+"/"+text+"/"+regex+"/"+ignoreCase,()->new Object[]{text,regex,ignoreCase},text==null?NullPointerException.class:SKIP);}
   }
   for(String text:texts)for(String pattern:new String[]{null,"","(?s).*hello.*","(?s)hello","I","[","*","\\","a.*b","(?i)hello","(?s).*"})for(boolean regex:new boolean[]{false,true})for(boolean ignoreCase:new boolean[]{false,true})check(MATCH,"matcher "+locale+"/"+text+"/"+pattern+"/"+regex+"/"+ignoreCase,()->new Object[]{text,pattern,regex,ignoreCase},SKIP);
   for(String text:texts)for(String pattern:new String[]{null,"","hello","he*","h?llo","[","I","(?i)hello",".*"})for(boolean regex:new boolean[]{false,true})for(int mode:new int[]{-1,0,1,2,3,4})check(TEXT,"text setting "+locale+"/"+text+"/"+pattern+"/"+regex+"/"+mode,()->{SystemSettingConstraint s=setting(3,0,mode,pattern);s.regexEnabled=regex;return new Object[]{s,text,null};},SKIP);
  }
  Locale.setDefault(Locale.ROOT);
  check(MATCH,"regular-expression find",()->new Object[]{"prefix needle suffix","needle",true,true},true);
  check(MATCH,"non-regex matches",()->new Object[]{"prefix needle suffix","needle",false,true},false);
  check(MATCH,"malformed regex",()->new Object[]{"abc","[",true,true},false);
  check(FULL,"literal dot escaping",()->new Object[]{"a.b",false,false},"(?s)a\\.b");
 }
 static WifiConstraint wifi(int api,int mode,int permission,int rawState,SupplicantState supplicant,String ssid,List list,String legacy){
  android.os.Build.VERSION.SDK_INT=api;EnvironmentControl.permission=permission;WifiConstraint w=new WifiConstraint();w.m_wifiState=mode;w.m_SSIDList=list==null?null:new ArrayList(list);w.m_SSID=legacy;WifiManager manager=(WifiManager)w.context.wifiService;manager.wifiState=rawState;manager.info.ssid=ssid;manager.info.state=supplicant;return w;
 }
 static void wifi(){
  int[] apis={26,27,28,29,36};String[] ssids={null,"","0x","<unknown ssid>","\"home\"","home","HOME","\"\"","\"","x\"","\"x"};
  for(int api:apis)for(int mode:new int[]{-1,0,1,2,3,4})for(int permission:new int[]{0,-1})for(int raw:new int[]{1,3,4})for(String ssid:ssids)check(WIFI,"wifi "+api+"/"+mode+"/"+permission+"/"+raw+"/"+ssid,()->new Object[]{wifi(api,mode,permission,raw,SupplicantState.COMPLETED,ssid,Arrays.asList("home"),"old"),null},SKIP);
  for(Object alias:htg.a)for(SupplicantState state:SupplicantState.values())for(int mode:new int[]{2,3})check(WIFI,"any-network alias "+alias+"/"+state+"/"+mode,()->new Object[]{wifi(28,mode,0,1,state,null,Arrays.asList(alias),"old"),null},mode==2?state==SupplicantState.COMPLETED:state!=SupplicantState.COMPLETED);
  for(int mode:new int[]{0,1,2,3})for(String ssid:new String[]{null,"home","\"home\""})for(boolean location:new boolean[]{false,true})check(WIFI,"legacy migration "+mode+"/"+ssid+"/"+location,()->{EnvironmentControl.locationEnabled=location;return new Object[]{wifi(28,mode,0,3,SupplicantState.DISCONNECTED,ssid,new ArrayList(),"home"),null};},SKIP);
  check(WIFI,"null SSID list",()->new Object[]{wifi(26,0,0,3,null,null,null,null),null},NullPointerException.class);
  check(WIFI,"null info any",()->{WifiConstraint w=wifi(26,2,0,3,null,null,Arrays.asList(htg.a.get(0)),null);((WifiManager)w.context.wifiService).info=null;return new Object[]{w,null};},false);
  check(WIFI,"permission stops service lookup",()->{WifiConstraint w=wifi(36,0,-1,3,null,null,null,null);w.context.wifiService=null;return new Object[]{w,null};},false);
  check(WIFI,"invalid mode original true",()->new Object[]{wifi(26,41,0,1,null,null,new ArrayList(),null),null},true);
  check(WIFI,"one quote throws",()->new Object[]{wifi(26,0,0,3,null,"\"",new ArrayList(),null),null},StringIndexOutOfBoundsException.class);
  check(WIFI,"null application context",()->{WifiConstraint w=wifi(26,0,0,3,null,null,new ArrayList(),null);w.context.nullApplicationContext=true;return new Object[]{w,null};},NullPointerException.class);
 }
 public static class InheritedManager extends WifiManager {} // getDeclaredMethod deliberately fails.
 static boolean hotExpected(int raw,int api,boolean enabled,boolean connections,int actual,int wanted,int mode){int state=raw>10?raw-10:raw;if(state==0||state==1||state==4)return !enabled;if(state==2||state==3){if(!connections||api>=29)return enabled;return mode==0?actual==wanted:mode==1?actual<wanted:mode==2?actual>wanted:true;}return true;}
 static WifiHotSpotConstraint hot(int raw,int api,boolean enabled,boolean connections,int actual,int wanted,int mode){android.os.Build.VERSION.SDK_INT=api;WifiHotSpotConstraint h=new WifiHotSpotConstraint();h.m_enabled=enabled;h.m_checkConnections=connections;h.m_connectedCount=wanted;h.m_comparisonValue=mode;((WifiManager)h.context.wifiService).apState=raw;WifiHotSpotConstraint.connected=actual;return h;}
 static void hotspot(){
  for(int raw:new int[]{-2,-1,0,1,2,3,4,5,10,11,12,13,14,15,23})for(int api:new int[]{26,28,29,36})for(boolean enabled:new boolean[]{false,true})for(boolean conn:new boolean[]{false,true})for(int count:new int[]{-1,0,1,2})for(int mode:new int[]{-1,0,1,2,3})check(HOT,"hotspot "+raw+"/"+api+"/"+enabled+"/"+conn+"/"+count+"/"+mode,()->new Object[]{hot(raw,api,enabled,conn,count,1,mode),null},hotExpected(raw,api,enabled,conn,count,1,mode));
  check(HOT,"reflection target exception",()->{WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);((WifiManager)h.context.wifiService).apFailure=new SecurityException("fixture AP");return new Object[]{h,null};},true);
  check(HOT,"reflection inherited method missing",()->{WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);h.context.wifiService=new InheritedManager();return new Object[]{h,null};},true);
  check(HOT,"null manager caught; VM message excluded",()->{normalizeVmMessage=true;WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);h.context.wifiService=null;return new Object[]{h,null};},true);
  check(HOT,"wrong service type outside catch",()->{WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);h.context.wifiService="not manager";return new Object[]{h,null};},ClassCastException.class);
  check(HOT,"client read exception caught",()->{WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);WifiHotSpotConstraint.connectedFailure=new IllegalStateException("fixture clients");return new Object[]{h,null};},true);
  check(HOT,"null context outside catch",()->{WifiHotSpotConstraint h=hot(13,28,true,true,0,0,0);h.context=null;return new Object[]{h,null};},NullPointerException.class);
 }
 static void solar(){
  String[] decimals={"0","0.0","-0.0","1","-1","1.23445","1.23455","-1.23445","-1.23455","0.00005","0.00015","90.8333","360","1E-10","9999999999.99995"};
  for(String v:decimals){check(ROUND,"round "+v,()->new Object[]{new BigDecimal(v)},new BigDecimal(v).setScale(4,RoundingMode.HALF_EVEN));check(RAD,"radians "+v,()->new Object[]{new BigDecimal(v)},new BigDecimal(v).multiply(BigDecimal.valueOf(0.017453292519943295d)).setScale(4,RoundingMode.HALF_EVEN));}
  check(ROUND,"round null",()->new Object[]{null},NullPointerException.class);check(RAD,"radians null",()->new Object[]{null},NullPointerException.class);
  for(String zone:ZONES)for(String v:new String[]{null,"0","1","24","0.0000","-0.0001","-1.0","-24.0","-25.0","0.5","1.0250","1.0750","23.9999","24.0000","25.5000","100.5000"})for(long epoch:new long[]{BASE,Instant.parse("2026-03-08T06:59:59Z").toEpochMilli(),Instant.parse("2026-11-01T05:59:59Z").toEpochMilli()})check(CAL,"calendar "+zone+"/"+v+"/"+epoch,()->new Object[]{v==null?null:new BigDecimal(v),date(epoch,zone)},v==null?null:SKIP);
  check(CAL,"null hour does not dereference base",()->new Object[]{null,null},null);check(CAL,"null base",()->new Object[]{new BigDecimal("1.0"),null},NullPointerException.class);
  double[][] coords={{46.2382,-63.1311},{0,0},{40.7128,-74.0060},{51.5074,-0.1278},{35.6892,51.3890},{27.7172,85.3240},{-33.8688,151.2093},{89.9,0},{-89.9,0},{90,180},{-90,-180},{66.56,25.83},{100,200}};
  String[] days={"2024-02-29T12:00:00Z","2026-03-08T06:59:59Z","2026-03-20T12:00:00Z","2026-06-21T12:00:00Z","2026-09-22T12:00:00Z","2026-11-01T05:59:59Z","2026-12-21T12:00:00Z"};
  for(double[] pos:coords)for(String zone:ZONES)for(String day:days)for(boolean rise:new boolean[]{false,true})check(HOUR,"solar "+Arrays.toString(pos)+"/"+zone+"/"+day+"/"+rise,()->new Object[]{new n7b(16,new g94(pos[0],pos[1]),TimeZone.getTimeZone(zone)),srh.b,date(Instant.parse(day).toEpochMilli(),"UTC"),rise},SKIP);
  check(HOUR,"null calendar",()->new Object[]{new n7b(16,new g94(0,0),TimeZone.getTimeZone("UTC")),srh.b,null,true},NullPointerException.class);
  check(HOUR,"null coordinates",()->new Object[]{new n7b(16,null,TimeZone.getTimeZone("UTC")),srh.b,date(BASE,"UTC"),true},NullPointerException.class);
  check(HOUR,"null zenith",()->new Object[]{new n7b(16,new g94(0,0),TimeZone.getTimeZone("UTC")),null,date(BASE,"UTC"),true},NullPointerException.class);
  String[] locations={null,"",",",",,","1","1,","1,,","bad,0","0,bad","NaN,0","0,Infinity","0,0","0,0,,","46.2382,-63.1311","89.9,0","-89.9,0","90,180","-90,-180","100,200"," 40.71 , -74.00 ","١,٢","1,2,3"};
  if(!TestClock.agentInstalled)throw new AssertionError("Sunrise test requires the explicit clock agent");
  for(String zone:ZONES){TimeZone.setDefault(TimeZone.getTimeZone(zone));for(String location:locations)for(int option:new int[]{-1,0,1,2,3,4})for(long epoch:new long[]{BASE,Instant.parse("2026-12-21T00:00:00Z").toEpochMilli()}){
   Object expected=(location==null||location.equals("")||location.equals(",")||location.equals(",,")||location.equals("1")||location.equals("1,")||location.equals("1,,")||location.startsWith("bad")||location.equals("0,bad")||location.equals("١,٢"))?false:location.contains("NaN")||location.contains("Infinity")?NumberFormatException.class:SKIP;
   check(SUN,"sunrise constraint "+zone+"/"+location+"/"+option+"/"+epoch,()->{TestClock.enabled=true;TestClock.epochMillis=epoch;com.arlosoft.macrodroid.settings.c.location=location;SunsetSunriseConstraint s=new SunsetSunriseConstraint();s.option=option;return new Object[]{s,null};},expected);
  }}TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
 }
 /** Event instants come from the original solar fixture; the strict before/after
  * expectations are separately specified, including exact equality and polar null.
  */
 static void solarBoundaries()throws Throwable{
  double[][] places={{0,0},{46.2382,-63.1311},{27.7172,85.3240},{-33.8688,151.2093}};
  String[] zones={"UTC","America/Halifax","Asia/Kathmandu","Australia/Sydney"};
  for(int place=0;place<places.length;place++){
   final double latitude=places[place][0],longitude=places[place][1];final String zone=zones[place];TimeZone.setDefault(TimeZone.getTimeZone(zone));
   for(String dateText:new String[]{"2026-03-20T12:00:00Z","2026-06-21T12:00:00Z","2026-12-21T12:00:00Z"})for(boolean sunrise:new boolean[]{false,true}){
    reset();Calendar day=date(Instant.parse(dateText).toEpochMilli(),zone);n7b calculator=new n7b(16,new g94(latitude,longitude),TimeZone.getTimeZone(zone));
    BigDecimal hour=(BigDecimal)original.invoke(HOUR,calculator,srh.b,day,sunrise);
    Calendar event=(Calendar)original.invoke(CAL,hour,day);if(event==null)throw new AssertionError("Expected a bounded nonpolar fixture event");
    final long at=event.getTimeInMillis();
    for(long delta:new long[]{-60000L,-1L,0L,1L,60000L})for(boolean before:new boolean[]{false,true}){
     final int option=sunrise?(before?0:1):(before?2:3);
     check(SUN,"strict solar boundary "+zone+"/"+dateText+"/"+option+"/"+delta,()->{
      TestClock.enabled=true;TestClock.epochMillis=at+delta;com.arlosoft.macrodroid.settings.c.location=latitude+","+longitude;SunsetSunriseConstraint constraint=new SunsetSunriseConstraint();constraint.option=option;return new Object[]{constraint,null};
     },before?delta<0:delta>=0);
    }
   }
  }
  TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
  for(long at:new long[]{BASE,Instant.parse("2026-12-21T12:00:00Z").toEpochMilli()})for(int option:new int[]{0,1,2,3,4})check(SUN,"polar missing event "+at+"/"+option,()->{TestClock.enabled=true;TestClock.epochMillis=at;com.arlosoft.macrodroid.settings.c.location="89.9,0";SunsetSunriseConstraint c=new SunsetSunriseConstraint();c.option=option;return new Object[]{c,null};},option!=0&&option!=2);
 }
 static void integration(){
  for(int pattern=0;pattern<32;pattern++)for(boolean or:new boolean[]{false,true})for(boolean disabled:new boolean[]{false,true})for(String key:new String[]{GATE,FORCED,SIMPLE}){
   final int p=pattern;check(key,"nested real constraints "+pattern+"/"+or+"/"+disabled+"/"+key,()->{
    Macro m=new Macro();m.orMode=or;m.categoryDisabled=false;m.isActionBlock=false;m.detailExcluded=false;
    SystemSettingConstraint s=setting(0,0,0,"10");s.context.resolver.integer=(p&1)!=0?10:0;s.testId="settings";
    WifiConstraint w=wifi(28,2,0,3,SupplicantState.COMPLETED,(p&2)!=0?"home":"away",Arrays.asList("home"),null);w.testId="wifi";
    WifiHotSpotConstraint h=hot((p&4)!=0?13:11,28,true,true,1,1,0);h.testId="hotspot";
    SunsetSunriseConstraint sun=new SunsetSunriseConstraint();sun.testId="sun";sun.option=(p&8)!=0?0:1;TestClock.enabled=true;TestClock.epochMillis=BASE;com.arlosoft.macrodroid.settings.c.location=(p&16)!=0?"89.9,0":"0,0";
    for(Constraint c:new Constraint[]{s,w,h,sun}){c.enabled=!disabled;m.m_constraintList.add(c);}
    TriggerContextInfo ctx=new TriggerContextInfo();return key.equals(SIMPLE)?new Object[]{m,ctx}:key.equals(FORCED)?new Object[]{m,ctx,false}:new Object[]{m,ctx,false,false};
   },disabled?true:SKIP);
  }
 }
 public static void main(String[] args)throws Throwable{
  Path root=Paths.get(args[0]);for(JsonElement x:JsonParser.parseString(Files.readString(root.resolve("source/java-method-map.json"))).getAsJsonArray()){JsonObject e=x.getAsJsonObject();registry.put(e.get("target").getAsString()+"->"+e.get("method").getAsString(),e);}
  for(JsonElement x:JsonParser.parseString(Files.readString(root.resolve("source/environment-methods.json"))).getAsJsonArray()){JsonObject e=x.getAsJsonObject();expectedKeys.add(e.get("target").getAsString()+"->"+e.get("method").getAsString());}
  Set<String> selected=new TreeSet<>(expectedKeys);selected.add(GATE);selected.add(FORCED);selected.add(SIMPLE);original=new BytecodeOracle(root.resolve("tests/fixtures/original-methods.dex"),selected);
  if(args.length>1){rebuilt=new BytecodeOracle();try(var stream=Files.list(Paths.get(args[1]))){for(Path p:(Iterable<Path>)stream.filter(x->x.toString().endsWith(".dex"))::iterator)rebuilt.add(p,selected);}}
  if(original.methods.size()!=selected.size()||(rebuilt!=null&&rebuilt.methods.size()!=selected.size()))throw new AssertionError("Missing selected methods");
  Locale priorLocale=Locale.getDefault();TimeZone priorZone=TimeZone.getDefault();Locale.setDefault(Locale.ROOT);TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
  try{integers();System.out.println("integer cases "+cases+" failed "+failed);settings();System.out.println("settings cases "+cases+" failed "+failed);matching();System.out.println("matching cases "+cases+" failed "+failed);wifi();System.out.println("wifi cases "+cases+" failed "+failed);hotspot();System.out.println("hotspot cases "+cases+" failed "+failed);solar();System.out.println("solar cases "+cases+" failed "+failed);solarBoundaries();integration();}
  finally{Locale.setDefault(priorLocale);TimeZone.setDefault(priorZone);TestClock.enabled=false;}
  Set<String> covered=new TreeSet<>(visited);covered.retainAll(expectedKeys);JsonObject r=new JsonObject();boolean pass=failed==0&&unsupported==0&&covered.equals(expectedKeys);r.addProperty("passed",pass);r.addProperty("cases",cases);r.addProperty("methodsCovered",covered.size());r.add("methodKeys",JSON.toJsonTree(covered));r.addProperty("methodsExpected",expectedKeys.size());r.addProperty("integrationMethodsCovered",visited.size()-covered.size());r.addProperty("failedCases",failed);r.addProperty("unsupportedExecutions",unsupported);r.addProperty("explicitExpectedChecks",expectedChecks);r.addProperty("expectedFailures",expectedFailures);r.addProperty("paths",rebuilt==null?2:3);r.addProperty("androidRuntime",false);r.add("families",JSON.toJsonTree(groups));r.add("exceptionTypes",JSON.toJsonTree(exceptions));r.add("failures",JSON.toJsonTree(failures));r.add("clockAgentTransformedHostClasses",JSON.toJsonTree(TestClockAgent.changed));
  JsonObject coverage=new JsonObject();for(String key:expectedKeys){int total=0,pc=0;Set<Integer> offsets=new TreeSet<>();for(var i:original.methods.get(key).getImplementation().getInstructions()){String name=i.getOpcode().name();if(!name.endsWith("PAYLOAD")){offsets.add(pc);total++;}pc+=i.getCodeUnits();}Set<Integer> seen=original.executed.getOrDefault(key,Collections.emptySet());JsonObject c=new JsonObject();c.addProperty("instructions",total);c.addProperty("visited",seen.size());offsets.removeAll(seen);c.add("notVisited",JSON.toJsonTree(offsets));coverage.add(key,c);}r.add("originalInstructionCoverage",coverage);
  r.addProperty("limitations","Host JVM and limited instruction interpreter, not Android/ART. Settings/radio/permission/location/float parser and constructor boundaries are controlled doubles. Clock agent modifies only host-loaded recovered code, not APKs. VM-generated NPE message text in one hotspot case is excluded; exception types and ordered log prefixes are compared. Concurrency, Android library differences and lifecycle not covered.");
  Files.writeString(root.resolve("reports/java-environment-"+(rebuilt==null?"two":"three")+"-path-parity.json"),JSON.toJson(r));System.out.println("environment cases="+cases+" methods="+covered.size()+" failed="+failed+" unsupported="+unsupported+" pass="+pass);if(!pass)throw new AssertionError("Environment parity failed; see report");
 }
}
