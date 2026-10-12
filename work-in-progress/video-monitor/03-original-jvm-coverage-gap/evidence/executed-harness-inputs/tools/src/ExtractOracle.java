import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;
/** Copies only selected original methods into a test-only fixture. Never a build input. */
public final class ExtractOracle {
 static String signature(Method m){return m.getName()+"("+String.join("",m.getParameterTypes())+")"+m.getReturnType();}
 public static void main(String[] args) throws Exception {
  Path root=Paths.get(args[0]);JsonArray registry=JsonParser.parseString(Files.readString(root.resolve("source/java-method-map.json"))).getAsJsonArray();
  Map<String,Set<String>> selected=new TreeMap<>();
  for(JsonElement x:registry){JsonObject e=x.getAsJsonObject();selected.computeIfAbsent(e.get("target").getAsString(),k->new TreeSet<>()).add(e.get("method").getAsString());}
  var container=DexFileFactory.loadDexContainer(new java.io.File(args[1]),Opcodes.forApi(23));
  List<ClassDef> classes=new ArrayList<>();int count=0;
  for(String name:container.getDexEntryNames()){
   for(ClassDef c:container.getEntry(name).getDexFile().getClasses()){
    Set<String> wanted=selected.get(c.getType());if(wanted==null)continue;
    List<Method> methods=new ArrayList<>();for(Method m:c.getMethods())if(wanted.contains(signature(m)))methods.add(m);
    if(methods.size()!=wanted.size())throw new IllegalStateException("Missing original methods in "+c.getType());
    classes.add(new ImmutableClassDef(c.getType(),c.getAccessFlags(),c.getSuperclass(),c.getInterfaces(),c.getSourceFile(),c.getAnnotations(),c.getFields(),methods));count+=methods.size();
   }
  }
  if(classes.size()!=selected.size())throw new IllegalStateException("Incomplete fixture");
  Path out=root.resolve("tests/fixtures/original-methods.dex");Files.createDirectories(out.getParent());
  DexPool.writeTo(out.toString(),new ImmutableDexFile(Opcodes.forApi(23),classes));
  System.out.println("Test-only original fixture: classes="+classes.size()+" methods="+count);
 }
}
