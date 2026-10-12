import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Read-only original DEX metadata; counts do not claim execution coverage. */
public final class OriginalMethodInventory {
    static final Gson G = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create();
    static String signature(MethodReference method) {
        return method.getName() + "(" + String.join("", method.getParameterTypes()) + ")" + method.getReturnType();
    }
    public static void main(String[] args) throws Exception {
        JsonArray requested = JsonParser.parseString(Files.readString(Path.of(args[1]))).getAsJsonArray();
        Map<String,JsonObject> selected = new TreeMap<>();
        for (JsonElement element : requested) {
            JsonObject row = element.getAsJsonObject();
            String key = row.get("target").getAsString() + "->" + row.get("method").getAsString();
            if (selected.put(key, row) != null) throw new IllegalArgumentException("Duplicate selected method");
        }
        Set<String> found = new TreeSet<>();
        JsonArray methods = new JsonArray();
        var container = DexFileFactory.loadDexContainer(Path.of(args[0]).toFile(), Opcodes.forApi(23));
        for (String name : container.getDexEntryNames()) {
            for (ClassDef owner : container.getEntry(name).getDexFile().getClasses()) {
                for (Method method : owner.getMethods()) {
                    String key = owner.getType() + "->" + signature(method);
                    if (!selected.containsKey(key)) continue;
                    if (!found.add(key)) throw new IllegalStateException("Duplicate DEX definition");
                    MethodImplementation implementation = Objects.requireNonNull(method.getImplementation());
                    JsonObject row = selected.get(key).deepCopy();
                    row.addProperty("dex_entry", name);
                    row.addProperty("scope", "Original DEX metadata only; no execution or coverage claim");
                    Map<String,Integer> opcodes = new TreeMap<>();
                    Set<String> invokes = new TreeSet<>(), fields = new TreeSet<>(), types = new TreeSet<>();
                    JsonArray edges = new JsonArray(), tries = new JsonArray();
                    int offset = 0, count = 0;
                    for (Instruction instruction : implementation.getInstructions()) {
                        String opcode = instruction.getOpcode().name();
                        opcodes.merge(opcode, 1, Integer::sum);
                        if (opcode.startsWith("IF_")) {
                            for (int to : new int[]{offset + instruction.getCodeUnits(),
                                    offset + ((OffsetInstruction)instruction).getCodeOffset()}) {
                                edges.add(offset + ":" + to);
                            }
                        }
                        if (instruction instanceof ReferenceInstruction referenced) {
                            Reference reference = referenced.getReference();
                            if (reference instanceof MethodReference methodRef)
                                invokes.add(methodRef.getDefiningClass() + "->" + signature(methodRef));
                            else if (reference instanceof FieldReference fieldRef)
                                fields.add(fieldRef.getDefiningClass() + "->" + fieldRef.getName() + ":" + fieldRef.getType());
                            else if (reference instanceof TypeReference typeRef) types.add(typeRef.getType());
                        }
                        offset += instruction.getCodeUnits();
                        count++;
                    }
                    for (TryBlock<? extends ExceptionHandler> region : implementation.getTryBlocks()) {
                        JsonObject item = new JsonObject();
                        item.addProperty("start", region.getStartCodeAddress());
                        item.addProperty("end", region.getStartCodeAddress() + region.getCodeUnitCount());
                        JsonArray handlers = new JsonArray();
                        for (ExceptionHandler handler : region.getExceptionHandlers()) {
                            JsonObject target = new JsonObject();
                            target.addProperty("type", handler.getExceptionType());
                            target.addProperty("offset", handler.getHandlerCodeAddress());
                            handlers.add(target);
                        }
                        item.add("handlers", handlers); tries.add(item);
                    }
                    row.addProperty("instructions", count);
                    row.addProperty("code_units", offset);
                    row.addProperty("registers", implementation.getRegisterCount());
                    row.addProperty("conditional_edges", edges.size());
                    row.add("conditional_edge_identities", edges);
                    row.add("opcodes", G.toJsonTree(opcodes));
                    row.add("method_references", G.toJsonTree(invokes));
                    row.add("field_references", G.toJsonTree(fields));
                    row.add("type_references", G.toJsonTree(types));
                    row.add("exception_regions", tries);
                    methods.add(row);
                    if (key.equals("Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;")) {
                        ClassDef fixture = new ImmutableClassDef(owner.getType(), owner.getAccessFlags(),
                            owner.getSuperclass(), owner.getInterfaces(), owner.getSourceFile(),
                            owner.getAnnotations(), owner.getFields(), List.of(method));
                        DexPool.writeTo(args[3], new ImmutableDexFile(Opcodes.forApi(23), List.of(fixture)));
                    }
                }
            }
        }
        if (!found.equals(selected.keySet())) throw new IllegalStateException("Missing selected original methods");
        JsonObject result = new JsonObject();
        result.addProperty("scope", "Exact original APK instruction and conditional-edge metadata; no app method execution");
        result.addProperty("selected_methods", selected.size());
        result.addProperty("android_executed", false);
        result.add("methods", methods);
        Files.writeString(Path.of(args[2]), G.toJson(result) + "\n");
        System.out.println("Original metadata methods=" + found.size() + "; test-only video fixture methods=1");
    }
}
