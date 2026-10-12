import com.google.gson.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import com.arlosoft.macrodroid.action.textmanipulation.TextManipulation;
import com.arlosoft.macrodroid.variables.VariableValue;

/** Differential host tests. Android resources, macros, expressions, constructors and
 * Parcel remain explicitly controlled boundaries. No device or ART result is implied. */
public final class ParityTests {
 static final Gson GSON=new GsonBuilder().setPrettyPrinting().serializeNulls().disableHtmlEscaping().create();
 static BytecodeOracle original, rebuilt;static int cases,failures,unsupported;static Set<String> visited=new TreeSet<>();static List<JsonObject> errors=new ArrayList<>();static Map<String,Integer> families=new TreeMap<>();
 static List<String> types(String sig){String s=sig.substring(sig.indexOf('(')+1,sig.indexOf(')'));List<String> out=new ArrayList<>();for(int i=0;i<s.length();){int st=i;while(s.charAt(i)=='[')i++;if(s.charAt(i)=='L')i=s.indexOf(';',i)+1;else i++;out.add(s.substring(st,i));}return out;}
 static JsonElement canon(Object x){
  if(x==null)return JsonNull.INSTANCE;
  if(x instanceof String)return new JsonPrimitive((String)x);
  if(x instanceof Character)return new JsonPrimitive((int)(Character)x);
  if(x instanceof Boolean)return new JsonPrimitive((Boolean)x);
  if(x instanceof Double){JsonObject o=new JsonObject();o.addProperty("double_bits",Long.toUnsignedString(Double.doubleToRawLongBits((Double)x),16));return o;}
  if(x instanceof Float){JsonObject o=new JsonObject();o.addProperty("float_bits",Integer.toUnsignedString(Float.floatToRawIntBits((Float)x),16));return o;}
  if(x instanceof Number)return new JsonPrimitive((Number)x);
  if(x instanceof Enum<?>){JsonObject o=new JsonObject();o.addProperty("enum",x.getClass().getName());o.addProperty("name",((Enum<?>)x).name());return o;}
  if(x instanceof StringBuilder)return new JsonPrimitive(x.toString());
  if(x.getClass().isArray()){JsonArray a=new JsonArray();for(int i=0;i<Array.getLength(x);i++)a.add(canon(Array.get(x,i)));return a;}
  if(x instanceof List<?>){JsonArray a=new JsonArray();for(Object v:(List<?>)x)a.add(canon(v));return a;}
  JsonObject o=new JsonObject();o.addProperty("class",x.getClass().getName());
  if(x instanceof TextManipulation){o.add("params",canon(((TextManipulation)x).params));return o;}
  if(x instanceof android.os.Parcel){o.add("written",canon(((android.os.Parcel)x).written));return o;}
  if(x instanceof VariableValue){for(Field f:x.getClass().getFields())if(!Modifier.isStatic(f.getModifiers()))try{o.add(f.getName(),canon(f.get(x)));}catch(IllegalAccessException e){throw new AssertionError(e);}return o;}
  return o;
 }
 static Object dummy(String type,int variant) {
  switch(type){case "Z":return variant%2!=0;case "B":return (byte)(variant==0?0:-19);case "S":return (short)(variant==0?0:-219);case "C":return (char)(variant==0?0:65535);case "I":return variant==0?0:variant==1?-17:Integer.MAX_VALUE;case "J":return variant==0?0L:variant==1?-9999999999L:Long.MAX_VALUE;case "F":return variant==0?0.0f:Float.NaN;case "D":return variant==0?0.0d:Double.NEGATIVE_INFINITY;default:return variant==0?null: "unused";}
 }
 static Object[] arguments(JsonObject e,List<String> params,String input,int number,int variant) throws Exception {
  String target=e.get("target").getAsString(),sig=e.get("method").getAsString();boolean instance=e.get("instance").getAsBoolean();boolean constant=e.has("proof_family")&&e.get("proof_family").getAsString().equals("constant");List<Object> args=new ArrayList<>();
  if(instance){Object self=constant?new Object():BytecodeOracle.type(target).getDeclaredConstructor().newInstance();if(self instanceof TextManipulation)((TextManipulation)self).params=params==null?null:new ArrayList<>(params);args.add(self);}
  int strNo=0;
  for(String t:types(sig)){
   if(constant){args.add(dummy(t,variant));continue;}
   switch(t){
    case "Ljava/lang/String;":args.add(strNo++==0?input:(variant%2==0?":suffix":null));break;
    case "I":args.add(number);break;
    case "Ljava/util/List;":args.add(params==null?null:new ArrayList<>(params));break;
    case "Ljava/lang/StringBuilder;":args.add(variant%3==0?null:new StringBuilder("prefix:"));break;
    case "Landroid/os/Parcel;":args.add(new android.os.Parcel());break;
    case "Lcom/arlosoft/macrodroid/macro/Macro;":case "Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;":args.add(null);break;
    default:throw new IllegalArgumentException("Unhandled test argument "+t+" in "+sig);
   }
  }
  return args.toArray();
 }
 static JsonObject outcome(JsonObject entry,String path,List<String> params,String input,int number,int variant) {
  JsonObject out=new JsonObject();Object[] args=null;Object result=null;defpackage.sr9.calls.clear();
  try{
   args=arguments(entry,params,input,number,variant);
   String key=entry.get("target").getAsString()+"->"+entry.get("method").getAsString();
   if(path.equals("original"))result=original.invoke(key,args);
   else if(path.equals("rebuilt"))result=rebuilt.invoke(key,args);
   else{
    String hd=entry.has("helper_descriptor")?entry.get("helper_descriptor").getAsString():entry.get("helper_method").getAsString()+"("+(entry.get("instance").getAsBoolean()?entry.get("target").getAsString():"")+entry.get("method").getAsString().split("\\(",2)[1];
    List<String> ptypes=types(hd);Class<?>[] cls=new Class<?>[ptypes.size()];for(int i=0;i<cls.length;i++)cls[i]=BytecodeOracle.type(ptypes.get(i));
    var method=BytecodeOracle.type(entry.get("helper").getAsString()).getDeclaredMethod(entry.get("helper_method").getAsString(),cls);
    try{result=method.invoke(null,args);}catch(InvocationTargetException ex){throw ex.getCause();}
   }
   out.add("value",canon(result));
  }catch(Throwable ex){out.addProperty("exception",ex.getClass().getName());if(ex instanceof BytecodeOracle.Unsupported){unsupported++;out.addProperty("unsupported",ex.getMessage());}}
  out.add("boundary_calls",canon(defpackage.sr9.calls));
  if(args!=null){JsonArray effects=new JsonArray();for(Object arg:args)if(arg instanceof TextManipulation||arg instanceof StringBuilder||arg instanceof android.os.Parcel)effects.add(canon(arg));out.add("effects",effects);if(args.length>0&&args[0] instanceof TextManipulation)out.addProperty("returned_params_identity",result!=null&&result==((TextManipulation)args[0]).params);}
  return out;
 }
 static void test(JsonObject entry,List<String> params,String input,int number,int variant){
  String key=entry.get("target").getAsString()+"->"+entry.get("method").getAsString();visited.add(key);cases++;String family=entry.has("proof_family")?entry.get("proof_family").getAsString():"v4-text-and-strings";families.merge(family,1,Integer::sum);
  JsonObject a=outcome(entry,"original",params,input,number,variant),b=outcome(entry,"java",params,input,number,variant),c=rebuilt==null?null:outcome(entry,"rebuilt",params,input,number,variant);
  if(!a.equals(b)||(c!=null&&!a.equals(c))||a.has("unsupported")||b.has("unsupported")||(c!=null&&c.has("unsupported"))){failures++;if(errors.size()<80){JsonObject e=new JsonObject();e.addProperty("target",key);e.addProperty("locale",Locale.getDefault().toLanguageTag());e.add("input",canon(input));e.add("params",canon(params));e.addProperty("index",number);e.addProperty("variant",variant);e.add("original",a);e.add("java",b);if(c!=null)e.add("rebuilt",c);errors.add(e);}}
 }
 static List<String> strings(){List<String> s=new ArrayList<>(Arrays.asList(null,"","a","ABC abc","Iıİi","Straße","éÉ\t ","سلام دنیا","日本語", "\u200E\u202A\u202C x \u200E","\\n","\\\\n","\\\\\\n","a\\nb\\\\nc","a\nb\rc","a,b,,c,","\uFEFF\u200B1,2,3","true,FALSE,TRUE,1, false","2147483647,2147483648,-2147483648,-2147483649","1e309,NaN,-Infinity,-0.0", " ","\t\r\n","😀,😃","\uD800","\uDC00","x".repeat(28),"x".repeat(29),"x".repeat(100)));
  Random random=new Random(5820195);String alphabet="abAZIıİi09\\nrt ,.-[]()\u200E\uFEFF\n\t";for(int i=0;i<60;i++){StringBuilder b=new StringBuilder();for(int n=random.nextInt(70);n>0;n--)b.append(alphabet.charAt(random.nextInt(alphabet.length())));s.add(b.toString());}return s;}
 static List<List<String>> configurations(String target){List<List<String>> out=new ArrayList<>();out.add(null);out.add(new ArrayList<>());out.add(Arrays.asList((String)null));
  if(target.endsWith("SubstringManipulation;")){for(String a:List.of("-1","0","1","5","100","2147483647","x"))for(String b:List.of("-1","0","2","99","x"))out.add(Arrays.asList(a,b));}
  else if(target.endsWith("SplitManipulation;")){for(String d:Arrays.asList(",","","|",".","\\n","\\r","\\\\n",null))for(String t:List.of("0","1","2","3","4","-1","bad"))out.add(Arrays.asList(d,t));}
  else if(target.endsWith("ReplaceAllManipulation;")){for(String p:List.of("a","(.)","[","\\n","$"))for(String b:List.of("x","$1","$9","\\n"))for(String f:Arrays.asList("true","false","TRUE",null))out.add(Arrays.asList(p,b,f));out.add(Arrays.asList("a","b"));}
  else if(target.endsWith("ExtractTextManipulation;")||target.endsWith("RemoveTextManipulation;")){for(String p:Arrays.asList("a","(.)","(a)?","[","\\n",".",null))for(String t:List.of("0","1","2","-1","bad"))out.add(Arrays.asList(p,t));}
  else{out.add(Arrays.asList("0","3"));out.add(Arrays.asList("a","x","false"));}
  return out;
 }
 public static void main(String[] args) throws Exception {
  Path root=Paths.get(args[0]);JsonArray all=JsonParser.parseString(Files.readString(root.resolve("source/java-method-map.json"))).getAsJsonArray();JsonArray registry=new JsonArray();for(JsonElement entry:all)if(!entry.getAsJsonObject().has("proof_family")||(!entry.getAsJsonObject().get("proof_family").getAsString().equals("v6-core")&&!entry.getAsJsonObject().get("proof_family").getAsString().equals("v7-environment")&&!entry.getAsJsonObject().get("proof_family").getAsString().equals("v8-engine")&&!entry.getAsJsonObject().get("proof_family").getAsString().equals("v9-ui")))registry.add(entry);Set<String> selected=new HashSet<>();for(JsonElement x:registry){var e=x.getAsJsonObject();selected.add(e.get("target").getAsString()+"->"+e.get("method").getAsString());}
  original=new BytecodeOracle(root.resolve("tests/fixtures/original-methods.dex"),selected);
  if(args.length>1){rebuilt=new BytecodeOracle();try(var files=Files.list(Paths.get(args[1]))){for(Path p:files.filter(x->x.toString().endsWith(".dex")).toList())rebuilt.add(p,selected);}if(rebuilt.methods.size()!=selected.size())throw new IllegalStateException("Incomplete rebuilt method coverage "+rebuilt.methods.size());}
  List<String> inputs=strings();Locale saved=Locale.getDefault();
  try{for(JsonElement x:registry){JsonObject e=x.getAsJsonObject();String target=e.get("target").getAsString(),sig=e.get("method").getAsString();
    if(e.has("proof_family")&&e.get("proof_family").getAsString().equals("constant")){for(int v=0;v<3;v++)test(e,List.of(),"unused",v,v);continue;}
    List<List<String>> configs=configurations(target);boolean apply=sig.startsWith("apply(")||sig.startsWith("applyArray(");boolean stringArg=types(sig).contains("Ljava/lang/String;");boolean integerArg=types(sig).contains("I");
    for(Locale locale:List.of(Locale.ROOT,Locale.forLanguageTag("tr-TR"),Locale.forLanguageTag("de-DE"))){Locale.setDefault(locale);
      if(apply){for(List<String> config:configs)for(int v=0;v<inputs.size();v++)test(e,config,inputs.get(v),v%7-2,v);}
      else if(stringArg){for(List<String> config:configs.subList(0,Math.min(configs.size(),6)))for(int v=0;v<inputs.size();v++)test(e,config,inputs.get(v),v%7-2,v);}
      else{for(List<String> config:configs.subList(0,Math.min(configs.size(),7)))for(int v=0;v<(integerArg?7:1);v++)test(e,config,"Abc",v-2,v);}
    }
  }}finally{Locale.setDefault(saved);}
  JsonObject report=new JsonObject();report.addProperty("passed",failures==0&&unsupported==0&&visited.size()==registry.size());report.addProperty("cases",cases);report.addProperty("failedCases",failures);report.addProperty("unsupportedExecutions",unsupported);report.addProperty("methodsCovered",visited.size());report.add("methodKeys",GSON.toJsonTree(visited));report.addProperty("methodsExpected",registry.size());report.addProperty("paths",rebuilt==null?2:3);report.addProperty("androidRuntime",false);report.addProperty("boundaries","Controlled Android resources, macro expansion, expression/Parcel behavior, constructors and enums; JDK libraries, not Android libraries.");report.add("families",GSON.toJsonTree(families));report.add("failures",GSON.toJsonTree(errors));
  Files.createDirectories(root.resolve("reports"));Files.writeString(root.resolve("reports/"+(rebuilt==null?"java-two-path-parity.json":"java-three-path-parity.json")),GSON.toJson(report));
  System.out.println("cases="+cases+" methods="+visited.size()+" failures="+failures+" unsupported="+unsupported);if(!report.get("passed").getAsBoolean())System.exit(2);
 }
}
