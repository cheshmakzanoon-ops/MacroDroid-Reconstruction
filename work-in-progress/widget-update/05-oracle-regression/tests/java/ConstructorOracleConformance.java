import com.android.tools.smali.dexlib2.immutable.reference.ImmutableMethodReference;
import com.google.gson.*;
import defpackage.*;
import java.nio.file.*;
import java.util.*;

/** Synthetic constructor boundary tests. These do not execute Android ART. */
public final class ConstructorOracleConformance {
    static final String PREFIX = "LConstructorOwnerFixture;->";
    static final String PARENT = PREFIX + "parent()Ljava/lang/Object;";
    static final String OTHER = PREFIX + "other()Ljava/lang/Object;";
    static final String SAME = PREFIX + "sameOwner()Ljava/lang/Object;";
    static final String VIRTUAL = PREFIX + "virtualConstructor()Ljava/lang/Object;";
    static final String SIGNATURE = "<init>(ILm73;)V";
    static final Set<String> KEYS = new TreeSet<>(Arrays.asList(PARENT, OTHER, SAME, VIRTUAL));
    static Path fixture;
    static final List<String> passed = new ArrayList<>();
    interface Attempt { void run() throws Throwable; }

    static BytecodeOracle oracle() throws Exception { return new BytecodeOracle(fixture, KEYS); }
    static void allow(BytecodeOracle value) throws Exception { value.allowParentConstructor(PARENT, "Lzhh;", "Lrff;", SIGNATURE, 1); }
    static void succeeds(String label, Attempt action) throws Throwable { action.run(); passed.add(label); }
    static void rejects(String label, Class<? extends Throwable> type, Attempt action) throws Throwable {
        try { action.run(); } catch (Throwable error) {
            if (!type.isInstance(error)) throw new AssertionError(label + " produced " + error, error);
            passed.add(label); return;
        }
        throw new AssertionError(label + " did not reject");
    }
    static void require(boolean condition, String message) { if (!condition) throw new AssertionError(message); }

    public static void main(String[] args) throws Throwable {
        fixture = Paths.get(args[0]); WidgetControl.reset();
        succeeds("ordinary same-owner constructor still executes", () -> {
            BytecodeOracle value = oracle(); Object result = value.invoke(SAME);
            require(result.getClass() == zhh.class && ((zhh) result).widgetArity == 2, "same-owner allocation identity/argument");
            require(value.parentConstructorAdapterCalls.isEmpty(), "ordinary call used an adapter");
        });
        rejects("unconfigured direct-parent owner is rejected", BytecodeOracle.Unsupported.class, () -> oracle().invoke(PARENT));
        succeeds("explicit method-scoped parent adapter executes", () -> {
            BytecodeOracle value = oracle(); allow(value); Object result = value.invoke(PARENT);
            require(result.getClass() == zhh.class && ((zhh) result).widgetArity == 2 && ((zhh) result).widgetCompletion == null, "parent-adapter allocation identity/arguments");
            require(value.parentConstructorAdapterCalls.size() == 1 && value.parentConstructorAdapterCalls.values().iterator().next() == 1, "adapter invocation accounting");
        });
        rejects("allowance cannot cross method boundaries", BytecodeOracle.Unsupported.class, () -> {
            BytecodeOracle value = oracle(); allow(value); value.invoke(OTHER);
        });
        rejects("constructor cannot use invoke-virtual", BytecodeOracle.Unsupported.class, () -> oracle().invoke(VIRTUAL));
        rejects("unselected target cannot obtain an adapter", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PREFIX + "absent()V", "Lzhh;", "Lrff;", SIGNATURE, 1));
        rejects("non-parent owner cannot obtain an adapter", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lzhh;", "Ljava/lang/Object;", SIGNATURE, 1));
        rejects("same-owner rules are not parent adapters", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lzhh;", "Lzhh;", SIGNATURE, 1));
        rejects("abstract allocated type is rejected", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lrff;", "Lo73;", SIGNATURE, 1));
        rejects("zero occurrence count is rejected", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lzhh;", "Lrff;", SIGNATURE, 0));
        rejects("wrong occurrence count is rejected", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lzhh;", "Lrff;", SIGNATURE, 2));
        rejects("wrong constructor descriptor is rejected", IllegalArgumentException.class,
            () -> oracle().allowParentConstructor(PARENT, "Lzhh;", "Lrff;", "<init>(I)V", 1));
        rejects("duplicate adapter is rejected", IllegalArgumentException.class, () -> {
            BytecodeOracle value = oracle(); allow(value); allow(value);
        });
        rejects("adapter cannot be added after execution", IllegalStateException.class, () -> {
            BytecodeOracle value = oracle(); value.invoke(SAME); allow(value);
        });
        rejects("allowance is bound to actual allocated type", BytecodeOracle.Unsupported.class, () -> {
            BytecodeOracle value = oracle(); allow(value);
            value.validateConstructorOwner(PARENT, new BytecodeOracle.Pending(StringBuilder.class),
                new ImmutableMethodReference("Lrff;", "<init>", Arrays.asList("I", "Lm73;"), "V"), "INVOKE_DIRECT");
        });
        rejects("allowance is bound to actual constructor parameters", BytecodeOracle.Unsupported.class, () -> {
            BytecodeOracle value = oracle(); allow(value);
            value.validateConstructorOwner(PARENT, new BytecodeOracle.Pending(zhh.class),
                new ImmutableMethodReference("Lrff;", "<init>", Arrays.asList("I"), "V"), "INVOKE_DIRECT");
        });
        JsonObject report = new JsonObject(); report.addProperty("passed", true); report.addProperty("cases", passed.size());
        report.addProperty("androidRuntime", false); report.addProperty("scope", "Synthetic host constructor-owner boundary only; compile-only child reflection adapter");
        report.add("checks", new Gson().toJsonTree(passed));
        Files.writeString(Paths.get(args[1]), new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        System.out.println("Constructor oracle controls passed=" + passed.size());
    }
}
