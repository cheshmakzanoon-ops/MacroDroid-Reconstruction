import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Extract actual original method bodies and their two original field getters. */
public final class ExtractDayLookupFixture {
    static String signature(Method method) {
        return method.getName() + "(" + String.join("", method.getParameterTypes()) + ")" + method.getReturnType();
    }

    public static void main(String[] args) throws Exception {
        String variables = "Lcom/arlosoft/macrodroid/variables/VariableValue";
        Map<String, String> wanted = Map.of(
            "Lcom/arlosoft/macrodroid/triggers/DayTrigger;", "p0(" + variables + "$Dictionary;Ljava/lang/String;)" + variables + "$DictionaryEntry;",
            variables + "$Dictionary;", "getEntries()Ljava/util/List;",
            variables + "$DictionaryEntry;", "getKey()Ljava/lang/String;");
        var container = DexFileFactory.loadDexContainer(new java.io.File(args[0]), Opcodes.forApi(23));
        List<ClassDef> classes = new ArrayList<>();
        Set<String> found = new TreeSet<>();
        JsonArray inventory = new JsonArray();
        for (String partition : container.getDexEntryNames()) {
            for (ClassDef original : container.getEntry(partition).getDexFile().getClasses()) {
                if (!wanted.containsKey(original.getType())) continue;
                List<Method> selected = new ArrayList<>();
                for (Method method : original.getMethods()) {
                    if (!signature(method).equals(wanted.get(original.getType()))) continue;
                    if (!found.add(original.getType())) throw new IllegalStateException("Duplicate original selected method");
                    selected.add(method);
                    JsonObject row = new JsonObject();
                    row.addProperty("partition", partition);
                    row.addProperty("key", original.getType() + "->" + signature(method));
                    row.addProperty("accessFlags", method.getAccessFlags());
                    int position = 0;
                    JsonArray instructions = new JsonArray();
                    for (var instruction : method.getImplementation().getInstructions()) {
                        JsonObject item = new JsonObject();
                        item.addProperty("offset", position);
                        item.addProperty("opcode", instruction.getOpcode().name());
                        item.addProperty("codeUnits", instruction.getCodeUnits());
                        instructions.add(item);
                        position += instruction.getCodeUnits();
                    }
                    row.add("instructions", instructions);
                    row.addProperty("exceptionRegions", method.getImplementation().getTryBlocks().size());
                    inventory.add(row);
                }
                if (selected.size() != 1) throw new IllegalStateException("Missing original selected method");
                classes.add(new ImmutableClassDef(original.getType(), original.getAccessFlags(), original.getSuperclass(),
                    original.getInterfaces(), original.getSourceFile(), original.getAnnotations(), original.getFields(), selected));
            }
        }
        if (!found.equals(wanted.keySet())) throw new IllegalStateException("Incomplete original fixture");
        DexPool.writeTo(args[1], new ImmutableDexFile(Opcodes.forApi(23), classes));
        Files.writeString(Paths.get(args[2]), new GsonBuilder().setPrettyPrinting().create().toJson(inventory) + "\n");
        System.out.println("Extracted three exact original methods into a test-only fixture");
    }
}
