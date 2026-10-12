import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Recreate the frozen numeric fixture from the new lookup selection, byte exactly. */
public final class CompareOriginalFixture {
    static String signature(Method m) { return m.getName() + "(" + String.join("", m.getParameterTypes()) + ")" + m.getReturnType(); }
    public static void main(String[] args) throws Exception {
        if (args.length != 4) throw new IllegalArgumentException("baseline.dex new.dex recreated-baseline.dex report.json");
        var old = DexFileFactory.loadDexFile(args[0], Opcodes.forApi(23));
        var fresh = DexFileFactory.loadDexFile(args[1], Opcodes.forApi(23));
        Map<String, ClassDef> byType = new TreeMap<>(); for (ClassDef c : fresh.getClasses()) if (byType.put(c.getType(), c) != null) throw new AssertionError("Duplicate new class");
        List<ClassDef> selected = new ArrayList<>(); int oldCount = 0, newCount = 0;
        Set<String> oldKeys = new TreeSet<>(), newKeys = new TreeSet<>();
        for (ClassDef c : fresh.getClasses()) for (Method m : c.getMethods()) { newCount++; if (!newKeys.add(c.getType() + "->" + signature(m))) throw new AssertionError("Duplicate new method"); }
        for (ClassDef c : old.getClasses()) {
            ClassDef n = byType.get(c.getType()); if (n == null) throw new AssertionError("Old class missing");
            Set<String> methods = new TreeSet<>(); for (Method m : c.getMethods()) { oldCount++; methods.add(signature(m)); if (!oldKeys.add(c.getType() + "->" + signature(m))) throw new AssertionError("Duplicate old method"); }
            List<Method> chosen = new ArrayList<>(); for (Method m : n.getMethods()) if (methods.contains(signature(m))) chosen.add(m);
            if (chosen.size() != methods.size()) throw new AssertionError("Old method missing");
            selected.add(new ImmutableClassDef(n.getType(), n.getAccessFlags(), n.getSuperclass(), n.getInterfaces(), n.getSourceFile(), n.getAnnotations(), n.getFields(), chosen));
        }
        DexPool.writeTo(args[2], new ImmutableDexFile(Opcodes.forApi(23), selected));
        boolean same = Arrays.equals(Files.readAllBytes(Path.of(args[0])), Files.readAllBytes(Path.of(args[2])));
        Set<String> additions = new TreeSet<>(newKeys); additions.removeAll(oldKeys);
        Set<String> expectedAdditions = Set.of(
            "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;",
            "Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;",
            "Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;");
        JsonObject result = new JsonObject(); result.addProperty("priorFixtureRecreatedByteExactly", same);
        result.addProperty("priorMethods", oldCount); result.addProperty("priorClasses", old.getClasses().size());
        result.addProperty("newMethods", newCount); result.addProperty("newClasses", fresh.getClasses().size());
        result.add("addedMethodKeys", new Gson().toJsonTree(additions));
        Files.writeString(Path.of(args[3]), new GsonBuilder().setPrettyPrinting().create().toJson(result) + "\n");
        if (!same || oldCount != 1246 || newCount != 1249 || old.getClasses().size() != 607 || fresh.getClasses().size() != 607
                || oldKeys.size() != oldCount || newKeys.size() != newCount || !additions.equals(expectedAdditions))
            throw new AssertionError("Original fixture invariance or exact lookup addition failed");
        System.out.println("ORIGINAL_FIXTURE old=1246/607 new=1249/607 prior-bytes-exact=true added=exact-lookup-and-two-getters");
    }
}
