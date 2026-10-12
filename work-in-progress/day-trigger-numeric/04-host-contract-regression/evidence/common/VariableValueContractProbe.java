import com.arlosoft.macrodroid.variables.VariableValue;
import com.arlosoft.macrodroid.variables.s0;
import com.google.gson.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.Supplier;

/** Integration-only regression: invoke the unchanged legacy encoders and recorder. */
public final class VariableValueContractProbe {
    static final Gson JSON = new GsonBuilder().serializeNulls().setPrettyPrinting().create();
    static JsonObject observation(Supplier<JsonElement> encode) {
        JsonObject row = new JsonObject();
        try { row.add("value", encode.get()); }
        catch (Throwable error) {
            row.addProperty("exception", error.getClass().getName());
            row.addProperty("message", error.getMessage());
        }
        return row;
    }
    static void require(boolean value, String message) { if (!value) throw new AssertionError(message); }
    public static void main(String[] args) throws Exception {
        require(args.length == 4, "contract.json aliases.json expected-class-directory check-aliases");
        Path expected = Path.of(args[2]).toRealPath();
        for (Class<?> type : List.of(VariableValue.class, VariableValue.Dictionary.class,
                VariableValue.DictionaryEntry.class, VariableValue.IntegerValue.class,
                VariableValue.DecimalValue.class, VariableValue.StringValue.class, VariableValue.BooleanValue.class)) {
            Path loaded = Path.of(type.getResource("/" + type.getName().replace('.', '/') + ".class").toURI()).toRealPath();
            require(loaded.equals(expected.resolve(type.getName().replace('.', '/') + ".class")), "Unexpected class origin: " + type);
        }
        List<String> keys = new ArrayList<>(Arrays.asList("outer", null, "<>&"));
        List<VariableValue> values = new ArrayList<>();
        values.add(null); values.add(new VariableValue());
        for (long value : new long[]{0, 1, -1, Long.MIN_VALUE, Long.MAX_VALUE, 9007199254740993L}) values.add(new VariableValue.IntegerValue(value, keys));
        for (long bits : new long[]{0, Long.MIN_VALUE, 0x3ffe666666666666L, 0xbffe666666666666L,
                1, 0x7fefffffffffffffL, 0x7ff0000000000000L, 0xfff0000000000000L, 0x7ff0000000000001L, 0xfff8000000000001L})
            values.add(new VariableValue.DecimalValue(Double.longBitsToDouble(bits), keys));
        for (String value : Arrays.asList(null, "", "27", "<>&\n")) values.add(new VariableValue.StringValue(value, keys));
        values.add(new VariableValue.BooleanValue(false, keys)); values.add(new VariableValue.BooleanValue(true, keys));
        VariableValue.IntegerValue stored = new VariableValue.IntegerValue(71, keys);
        VariableValue.DictionaryEntry entry = new VariableValue.DictionaryEntry("key", stored, keys);
        VariableValue.DictionaryEntry twin = new VariableValue.DictionaryEntry("key", stored, keys);
        List<VariableValue.DictionaryEntry> entries = new ArrayList<>(Arrays.asList(entry, null));
        values.add(entry); values.add(new VariableValue.DictionaryEntry(null, null, null));
        values.add(new VariableValue.Dictionary(entries, false, keys)); values.add(new VariableValue.Dictionary(null, true, null));
        JsonObject report = new JsonObject(); JsonArray rows = new JsonArray(); int number = 0;
        Gson defaults = new Gson(), nulls = new GsonBuilder().serializeNulls().create();
        for (VariableValue value : values) {
            JsonObject row = new JsonObject(); row.addProperty("index", number++);
            row.addProperty("class", value == null ? null : value.getClass().getName());
            row.add("legacyCanonical", observation(() -> ParityTests.canon(value)));
            row.add("coreCanonical", observation(() -> CoreParityTests.canon(value)));
            row.add("uiCanonical", observation(() -> UiParityTests.canonical(value)));
            row.add("gsonDefault", observation(() -> defaults.toJsonTree(value)));
            row.add("gsonSerializeNulls", observation(() -> nulls.toJsonTree(value)));
            rows.add(row);
        }
        report.add("values", rows);
        JsonObject identity = new JsonObject();
        identity.addProperty("entryKeyIdentity", entry.key == "key");
        identity.addProperty("entryValueIdentity", entry.value == stored);
        identity.addProperty("entryKeysIdentity", entry.keys == keys);
        identity.addProperty("dictionaryEntriesIdentity", ((VariableValue.Dictionary) values.get(values.size() - 2)).entries == entries);
        identity.addProperty("dictionaryKeysIdentity", ((VariableValue.Dictionary) values.get(values.size() - 2)).keys == keys);
        identity.addProperty("selfEquals", entry.equals(entry)); identity.addProperty("equalFieldsAreDistinct", !entry.equals(twin));
        identity.addProperty("nullNotEqual", !entry.equals(null)); identity.addProperty("otherClassNotEqual", !entry.equals(stored));
        report.add("existingIdentityContracts", identity);
        s0 event = new s0(); event.a = entry; event.b = "variable-event"; event.c = 19;
        report.add("variableRecordCoreEncoding", observation(() -> CoreParityTests.canon(event)));
        defpackage.EngineRuntime.active = false; defpackage.SceneControl.active = false;
        defpackage.CoreTrace.reset(); defpackage.aj5 bus = defpackage.cj5.a(); bus.e(event); bus.e(entry);
        report.add("existingEventRecorder", JSON.toJsonTree(defpackage.CoreTrace.calls));
        JsonObject publicApi = new JsonObject();
        for (Class<?> type : List.of(VariableValue.class, VariableValue.Dictionary.class, VariableValue.DictionaryEntry.class,
                VariableValue.IntegerValue.class, VariableValue.DecimalValue.class, VariableValue.StringValue.class, VariableValue.BooleanValue.class)) {
            JsonObject api = new JsonObject(); List<String> fields = new ArrayList<>(), constructors = new ArrayList<>();
            for (Field field : type.getFields()) fields.add(field.getName() + ":" + field.getType().getName() + ":" + field.getModifiers());
            for (Constructor<?> ctor : type.getConstructors()) constructors.add(ctor.toString());
            Collections.sort(fields); Collections.sort(constructors); api.add("publicFields", JSON.toJsonTree(fields));
            api.add("publicConstructors", JSON.toJsonTree(constructors)); publicApi.add(type.getName(), api);
        }
        report.add("existingPublicApi", publicApi); report.addProperty("valueCases", values.size());
        report.addProperty("encoderObservations", values.size() * 5 + 1);
        Files.writeString(Path.of(args[0]), JSON.toJson(report) + "\n");
        JsonObject aliases = new JsonObject(); int aliasChecks = 0;
        if (Boolean.parseBoolean(args[3])) {
            for (Class<?> type : List.of(VariableValue.DictionaryEntry.class, VariableValue.IntegerValue.class, VariableValue.DecimalValue.class)) {
                String fieldName = type == VariableValue.DictionaryEntry.class ? "variable" : type == VariableValue.IntegerValue.class ? "intValue" : "decimalValue";
                Field field = type.getDeclaredField(fieldName); int flags = field.getModifiers();
                require(Modifier.isPrivate(flags) && Modifier.isFinal(flags) && Modifier.isTransient(flags), "Alias must be private final transient: " + fieldName);
                aliasChecks++;
            }
            for (VariableValue value : values) {
                if (value instanceof VariableValue.IntegerValue integer) {
                    long observed = (Long) integer.getClass().getMethod("getIntValue").invoke(integer);
                    require(observed == integer.value, "Integer alias value drift"); aliasChecks++;
                } else if (value instanceof VariableValue.DecimalValue decimal) {
                    double observed = (Double) decimal.getClass().getMethod("getDecimalValue").invoke(decimal);
                    require(Double.doubleToRawLongBits(observed) == Double.doubleToRawLongBits(decimal.value), "Decimal alias raw-bit drift"); aliasChecks++;
                } else if (value instanceof VariableValue.DictionaryEntry item) {
                    require(item.getClass().getMethod("getVariable").invoke(item) == item.value, "Entry alias identity drift"); aliasChecks++;
                }
            }
        }
        aliases.addProperty("requested", Boolean.parseBoolean(args[3])); aliases.addProperty("checks", aliasChecks); aliases.addProperty("passed", true);
        Files.writeString(Path.of(args[1]), JSON.toJson(aliases) + "\n");
        System.out.println("VARIABLE_HOST_CONTRACT values=" + values.size() + " encodings=" + (values.size() * 5 + 1) + " aliasChecks=" + aliasChecks);
    }
}
