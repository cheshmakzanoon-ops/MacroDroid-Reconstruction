import com.android.tools.smali.dexlib2.iface.instruction.Instruction;
import com.android.tools.smali.dexlib2.iface.instruction.OffsetInstruction;
import com.arlosoft.macrodroid.variables.VariableValue;
import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;
import com.google.gson.*;
import recovered.ui.DayTriggerLookupMethods;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Private typed-list lookup study. The original interpreter is not Android/ART. */
public final class DayLookupStudy {
    static final String BASE = "Lcom/arlosoft/macrodroid/variables/VariableValue";
    static final String PRIMARY = "Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(" + BASE + "$Dictionary;Ljava/lang/String;)" + BASE + "$DictionaryEntry;";
    static final Set<String> GETTERS = Set.of(BASE + "$Dictionary;->getEntries()Ljava/util/List;",
        BASE + "$DictionaryEntry;->getKey()Ljava/lang/String;");
    static final Set<String> ALL;
    static { TreeSet<String> keys = new TreeSet<>(GETTERS); keys.add(PRIMARY); ALL = Collections.unmodifiableSet(keys); }
    record Input(String name, String[] keys, String query, String mode, int nullEntry,
                 String faultAt, String faultType, Integer expectedIndex, String expectedException,
                 List<String> expectedEvents) {}
    record Observed(Integer returnIndex, String exceptionClass, String rawMessage,
                    boolean injectedExceptionIdentity, List<String> events, boolean unsupported) {}
    interface Throwing { Object get() throws Throwable; }

    static String sha(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }
    static String fileSha(Path path) throws Exception { return sha(Files.readAllBytes(path)); }
    static void require(boolean condition, String message) { if (!condition) throw new IllegalStateException(message); }
    static void bindClass(Class<?> type, Path expected, String hash, JsonObject bindings) throws Exception {
        var url = type.getResource("/" + type.getName().replace('.', '/') + ".class");
        require(url != null && url.getProtocol().equals("file"), "Class is not loaded from a file: " + type.getName());
        Path actual = Paths.get(url.toURI()).toRealPath();
        require(actual.equals(expected.toRealPath()), "Wrong loaded class origin: " + type.getName());
        require(fileSha(actual).equals(hash), "Wrong loaded class hash: " + type.getName());
        JsonObject item = new JsonObject(); item.addProperty("path", actual.toString()); item.addProperty("sha256", hash);
        bindings.add(type.getName(), item);
    }


    public static final class State {
        final Input input;
        final List<String> events = new ArrayList<>();
        final List<DictionaryEntry> entries = new ArrayList<>();
        final RuntimeException fault;
        final Dictionary dictionary;
        State(Input input) {
            this.input = input;
            String message = "EXACT_INJECTED_LOOKUP_FAULT:" + input.name();
            fault = switch (input.faultType()) {
                case "npe" -> new NullPointerException(message);
                case "cast" -> new ClassCastException(message);
                default -> new IllegalStateException(message);
            };
            for (int i = 0; i < input.keys().length; i++)
                entries.add(i == input.nullEntry() ? null : new DictionaryEntry(input.keys()[i]));
            dictionary = input.mode().equals("dictionary-null") ? null :
                new Dictionary(input.mode().equals("entries-null") ? null : new TraceList(this));
        }
        void event(String name) {
            events.add(name);
            if (name.equals(input.faultAt())) throw fault;
        }
        int identityIndex(Object value) {
            if (value == null) return -1;
            for (int i = 0; i < entries.size(); i++) if (entries.get(i) == value) return i;
            return -2;
        }
    }
    public static final class TraceList extends AbstractList<DictionaryEntry> {
        final State state;
        TraceList(State state) { this.state = state; }
        public int size() { state.event("size"); return state.entries.size(); }
        public DictionaryEntry get(int index) { state.event("get@" + index); return state.entries.get(index); }
        public Iterator<DictionaryEntry> iterator() {
            state.event("iterator");
            return state.input.mode().equals("iterator-null") ? null : new TraceIterator(state);
        }
    }
    public static final class TraceIterator implements Iterator<DictionaryEntry> {
        final State state;
        int index;
        TraceIterator(State state) { this.state = state; }
        public boolean hasNext() { state.event("hasNext@" + index); return index < state.entries.size(); }
        public DictionaryEntry next() {
            state.event("next@" + index);
            if (index >= state.entries.size()) throw new NoSuchElementException("EXHAUSTED_LOOKUP_ITERATOR");
            return state.entries.get(index++);
        }
        public void remove() { state.event("remove"); throw new UnsupportedOperationException("REMOVE"); }
    }

    static Observed observe(State state, Throwing body) {
        try {
            Object value = body.get();
            int index = state.identityIndex(value);
            return new Observed(index, null, null, false, List.copyOf(state.events), index == -2);
        } catch (Throwable error) {
            return new Observed(null, error.getClass().getName(), error.getMessage(), error == state.fault,
                List.copyOf(state.events), error instanceof BytecodeOracle.Unsupported);
        }
    }
    static boolean matchesExpected(Input input, Observed output) {
        if (output.unsupported() || !output.events().equals(input.expectedEvents())) return false;
        if (input.expectedException() == null)
            return output.exceptionClass() == null && Objects.equals(output.returnIndex(), input.expectedIndex())
                && !output.injectedExceptionIdentity() && output.rawMessage() == null;
        if (output.returnIndex() != null || !input.expectedException().equals(output.exceptionClass())) return false;
        if (input.faultAt() != null)
            return output.injectedExceptionIdentity() && ("EXACT_INJECTED_LOOKUP_FAULT:" + input.name()).equals(output.rawMessage());
        return !output.injectedExceptionIdentity() && input.expectedException().equals("java.lang.NullPointerException");
    }
    static boolean sameScopedOutcome(Input input, Observed left, Observed right) {
        // Only explicitly authored VM-null cases exclude host-generated NPE diagnostics.
        // Injected NPE/ClassCastException messages and identities are still compared exactly.
        if (input.faultAt() == null && "java.lang.NullPointerException".equals(input.expectedException()))
            return matchesExpected(input, left) && matchesExpected(input, right);
        return left.equals(right);
    }
    static List<String> trace(int inspected, boolean exhausted) {
        List<String> events = new ArrayList<>(); events.add("iterator");
        for (int i = 0; i < inspected; i++) { events.add("hasNext@" + i); events.add("next@" + i); }
        if (exhausted) events.add("hasNext@" + inspected);
        return List.copyOf(events);
    }
    static void normal(List<Input> out, String name, String query, int matched, String... keys) {
        out.add(new Input(name, keys, query, "normal", -1, null, "state", matched, null,
            trace(matched < 0 ? keys.length : matched + 1, matched < 0)));
    }
    static List<Input> cases() {
        List<Input> out = new ArrayList<>();
        normal(out, "empty", "day", -1);
        normal(out, "empty-with-null-query", null, -1);
        normal(out, "empty-string-match", "", 0, "", "");
        normal(out, "null-entry-key-is-not-a-match", "day", 1, null, "DAY");
        normal(out, "all-null-entry-keys", "day", -1, null, null);
        normal(out, "first-duplicate-entry-identity", "day", 0, "DAY", "day", "Day");
        normal(out, "last-distinct-entry-identity", "day", 3, "month", "year", "hour", "DAY");
        normal(out, "whitespace-is-significant", "day", -1, " day", "day ", " day ");
        normal(out, "query-whitespace-is-significant", " day ", -1, "day", "DAY");
        normal(out, "punctuation-is-significant", "day", -1, "day!", "!day", "d-ay");
        for (int letter = 0; letter < 26; letter++) {
            String upper = String.valueOf((char)('A' + letter));
            String lower = String.valueOf((char)('a' + letter));
            String other = String.valueOf((char)('a' + (letter + 1) % 26));
            for (int form = 0; form < 4; form++) {
                String query = (form & 1) == 0 ? upper : lower;
                String key = (form & 2) == 0 ? upper : lower;
                normal(out, "ascii-first-" + letter + "-" + form, query, 0, key, other);
                normal(out, "ascii-middle-" + letter + "-" + form, query, 1, "#", key, query);
                normal(out, "ascii-absent-" + letter + "-" + form, query, -1, other, "#");
            }
        }
        String[][] equal = {{"İ", "i"}, {"ı", "I"}, {"ſ", "S"}, {"K", "k"}, {"Σ", "σ"},
            {"Σ", "ς"}, {"Д", "д"}, {"É", "é"}, {"\uD801\uDC00", "\uD801\uDC28"}};
        for (int i = 0; i < equal.length; i++) {
            normal(out, "declared-unicode-forward-" + i, equal[i][0], 0, equal[i][1], equal[i][0]);
            normal(out, "declared-unicode-reverse-" + i, equal[i][1], 1, "#", equal[i][0]);
        }
        normal(out, "no-multi-character-sharp-s-fold", "SS", -1, "ß");
        normal(out, "no-composed-decomposed-fold", "é", -1, "e\u0301");
        normal(out, "literal-surrogate-identity", "\uD800", 0, "\uD800");
        normal(out, "different-surrogates", "\uD800", -1, "\uD801");
        for (String mode : List.of("dictionary-null", "entries-null", "iterator-null"))
            out.add(new Input(mode, new String[]{"day"}, "day", mode, -1, null, "state", null,
                "java.lang.NullPointerException", mode.equals("iterator-null") ? List.of("iterator") : List.of()));
        out.add(new Input("null-query-nonempty", new String[]{"day"}, null, "normal", -1, null, "state", null,
            "java.lang.NullPointerException", trace(1, false)));
        out.add(new Input("null-query-and-null-key", new String[]{null}, null, "normal", -1, null, "state", null,
            "java.lang.NullPointerException", trace(1, false)));
        out.add(new Input("null-first-entry", new String[]{"ignored"}, "day", "normal", 0, null, "state", null,
            "java.lang.NullPointerException", trace(1, false)));
        out.add(new Input("null-second-entry", new String[]{"month", "ignored"}, "day", "normal", 1, null, "state", null,
            "java.lang.NullPointerException", trace(2, false)));
        out.add(new Input("return-before-null-second-entry", new String[]{"DAY", "ignored"}, "day", "normal", 1, null, "state", 0,
            null, trace(1, false)));
        List<String> exhaustive = trace(2, true);
        for (String event : exhaustive) for (String kind : List.of("state", "npe", "cast")) {
            String exception = switch (kind) {
                case "npe" -> "java.lang.NullPointerException";
                case "cast" -> "java.lang.ClassCastException";
                default -> "java.lang.IllegalStateException";
            };
            out.add(new Input("injected-" + event + "-" + kind, new String[]{"month", "year"}, "day", "normal", -1,
                event, kind, null, exception, List.copyOf(exhaustive.subList(0, exhaustive.indexOf(event) + 1))));
        }
        out.add(new Input("match-before-later-iterator-fault", new String[]{"day", "month"}, "DAY", "normal", -1,
            "hasNext@1", "state", 0, null, trace(1, false)));
        require(out.stream().map(Input::name).distinct().count() == out.size(), "Duplicate case identifiers");
        return out;
    }

    static JsonObject coverage(BytecodeOracle oracle, Set<String> keys) {
        JsonObject output = new JsonObject(); JsonArray methods = new JsonArray();
        int total = 0, covered = 0, edgeTotal = 0, edgeCovered = 0;
        for (String key : new TreeSet<>(keys)) {
            var method = oracle.methods.get(key); require(method != null, "Coverage method missing: " + key);
            Set<Integer> required = new TreeSet<>(); Set<String> requiredEdges = new TreeSet<>(); int pc = 0;
            for (Instruction instruction : method.getImplementation().getInstructions()) {
                required.add(pc);
                if (instruction.getOpcode().name().startsWith("IF_")) {
                    requiredEdges.add(pc + ":" + (pc + instruction.getCodeUnits()));
                    requiredEdges.add(pc + ":" + (pc + ((OffsetInstruction) instruction).getCodeOffset()));
                }
                pc += instruction.getCodeUnits();
            }
            Set<Integer> actual = oracle.executed.getOrDefault(key, Set.of());
            Set<String> actualEdges = oracle.branchEdges.getOrDefault(key, Set.of());
            require(required.containsAll(actual) && requiredEdges.containsAll(actualEdges), "Unexpected coverage coordinates");
            Set<Integer> missing = new TreeSet<>(required); missing.removeAll(actual);
            Set<String> missingEdges = new TreeSet<>(requiredEdges); missingEdges.removeAll(actualEdges);
            JsonObject row = new JsonObject(); row.addProperty("key", key); row.addProperty("primaryRecovery", key.equals(PRIMARY));
            row.add("requiredOffsets", new Gson().toJsonTree(required)); row.add("executedOffsets", new Gson().toJsonTree(actual));
            row.add("missingOffsets", new Gson().toJsonTree(missing)); row.add("requiredEdges", new Gson().toJsonTree(requiredEdges));
            row.add("executedEdges", new Gson().toJsonTree(actualEdges)); row.add("missingEdges", new Gson().toJsonTree(missingEdges));
            row.addProperty("instructionCount", required.size()); row.addProperty("exceptionRegions", method.getImplementation().getTryBlocks().size());
            methods.add(row); total += required.size(); covered += actual.size(); edgeTotal += requiredEdges.size(); edgeCovered += actualEdges.size();
        }
        output.add("methods", methods); output.addProperty("instructionCount", total); output.addProperty("executedInstructionCount", covered);
        output.addProperty("requiredBranchEdges", edgeTotal); output.addProperty("executedBranchEdges", edgeCovered);
        output.addProperty("allInstructionsAndEdgesExecuted", total == covered && edgeTotal == edgeCovered);
        return output;
    }


    static JsonElement utf16(String value) {
        if (value == null) return JsonNull.INSTANCE;
        StringBuilder units = new StringBuilder();
        for (int i = 0; i < value.length(); i++)
            units.append(String.format(Locale.ROOT, "%04x", (int)value.charAt(i)));
        return new JsonPrimitive(units.toString());
    }
    static JsonObject inputEvidence(Input input) {
        JsonObject row = new JsonObject(); JsonArray keys = new JsonArray();
        for (String key : input.keys()) keys.add(utf16(key));
        row.addProperty("case", input.name()); row.add("keysUtf16Hex", keys);
        row.add("queryUtf16Hex", utf16(input.query())); row.addProperty("mode", input.mode());
        row.addProperty("nullEntryIndex", input.nullEntry()); row.addProperty("injectedFaultAt", input.faultAt());
        row.addProperty("injectedFaultType", input.faultType()); row.addProperty("expectedReturnIndex", input.expectedIndex());
        row.addProperty("expectedExceptionClass", input.expectedException());
        row.add("expectedEvents", new Gson().toJsonTree(input.expectedEvents()));
        row.addProperty("exceptionComparisonScope", input.faultAt() == null &&
            "java.lang.NullPointerException".equals(input.expectedException()) ?
            "Explicit VM-null case: exception class and complete event trace; raw messages retained" :
            "Complete observed record, including injected exception identity and exact message");
        return row;
    }
    static JsonObject observerControls(List<Input> cases) {
        Input input = cases.stream().filter(i -> i.name().equals("injected-iterator-npe")).findFirst().orElseThrow();
        Observed positive = new Observed(null, input.expectedException(), "EXACT_INJECTED_LOOKUP_FAULT:" + input.name(),
            true, input.expectedEvents(), false);
        require(matchesExpected(input, positive), "Observer control positive rejected");
        List<Observed> faults = List.of(
            new Observed(null, positive.exceptionClass(), "CHANGED_INJECTED_MESSAGE", true, positive.events(), false),
            new Observed(null, positive.exceptionClass(), positive.rawMessage(), false, positive.events(), false),
            new Observed(null, positive.exceptionClass(), positive.rawMessage(), true, List.of(), false),
            new Observed(0, positive.exceptionClass(), positive.rawMessage(), true, positive.events(), false),
            new Observed(null, positive.exceptionClass(), positive.rawMessage(), true, positive.events(), true));
        int rejected = 0;
        for (Observed fault : faults)
            if (!matchesExpected(input, fault) && !sameScopedOutcome(input, positive, fault)) rejected++;
        require(rejected == faults.size(), "Observer accepted a changed injected fault");
        JsonObject output = new JsonObject(); output.addProperty("case", input.name());
        output.addProperty("positiveAccepted", true); output.addProperty("changedRecordsRejected", rejected);
        output.addProperty("applicationExecutions", 0); output.addProperty("applicationCoverageCredit", 0);
        output.add("positive", new GsonBuilder().serializeNulls().create().toJsonTree(positive));
        output.add("rejectedRecords", new GsonBuilder().serializeNulls().create().toJsonTree(faults));
        return output;
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Expected config.json report.json");
        JsonObject config = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        Path original = Path.of(config.get("originalDex").getAsString());
        require(fileSha(original).equals(config.get("originalDexSha256").getAsString()), "Wrong original fixture identity");
        JsonObject origins = new JsonObject(); JsonObject pins = config.getAsJsonObject("classPins");
        for (Class<?> type : List.of(DayLookupStudy.class, BytecodeOracle.class, DayTriggerLookupMethods.class,
                VariableValue.class, Dictionary.class, DictionaryEntry.class, Input.class, Observed.class,
                Throwing.class, State.class, TraceList.class, TraceIterator.class,
                defpackage.EngineRuntime.class, defpackage.TestClock.class))
            require(pins.has(type.getName()), "Class pin missing: " + type.getName());
        for (String name : new TreeSet<>(pins.keySet())) {
            Class<?> type = Class.forName(name, false, DayLookupStudy.class.getClassLoader());
            JsonObject pin = pins.getAsJsonObject(name);
            bindClass(type, Path.of(pin.get("path").getAsString()), pin.get("sha256").getAsString(), origins);
        }
        require(!defpackage.EngineRuntime.active && !defpackage.TestClock.enabled, "Unexpected enabled host hook");
        BytecodeOracle reference = new BytecodeOracle(original, ALL);
        require(reference.methods.keySet().equals(ALL), "Original fixture membership mismatch");
        BytecodeOracle rebuilt = null;
        if (config.has("rebuiltDex")) {
            Path dex = Path.of(config.get("rebuiltDex").getAsString());
            require(fileSha(dex).equals(config.get("rebuiltDexSha256").getAsString()), "Wrong rebuilt fixture identity");
            require(!fileSha(dex).equals(fileSha(original)), "Original fixture cannot masquerade as rebuilt");
            rebuilt = new BytecodeOracle(original, GETTERS); rebuilt.add(dex, Set.of(PRIMARY));
            require(rebuilt.methods.keySet().equals(ALL), "Rebuilt fixture membership mismatch");
        }
        List<Input> cases = cases(); JsonArray rows = new JsonArray(); JsonArray mismatches = new JsonArray();
        JsonObject controls = observerControls(cases);
        Gson gson = new GsonBuilder().serializeNulls().create();
        int unsupported = 0, expectedFailures = 0;
        for (Input input : cases) {
            State oldState = new State(input), javaState = new State(input);
            Observed old = observe(oldState, () -> reference.invoke(PRIMARY, oldState.dictionary, input.query()));
            Observed java = observe(javaState, () -> DayTriggerLookupMethods.findEntry(javaState.dictionary, input.query()));
            Observed dex = null;
            if (rebuilt != null) {
                BytecodeOracle actualRebuilt = rebuilt; State dexState = new State(input);
                dex = observe(dexState, () -> actualRebuilt.invoke(PRIMARY, dexState.dictionary, input.query()));
            }
            JsonObject row = inputEvidence(input);
            row.add("original", gson.toJsonTree(old)); row.add("java", gson.toJsonTree(java));
            if (dex != null) row.add("rebuilt", gson.toJsonTree(dex));
            boolean same = sameScopedOutcome(input, old, java) && (dex == null || sameScopedOutcome(input, old, dex));
            boolean correct = matchesExpected(input, old) && matchesExpected(input, java) && (dex == null || matchesExpected(input, dex));
            row.addProperty("sameScopedOutcome", same); row.addProperty("allPathsMatchIndependentExpected", correct);
            if (!same || !correct) mismatches.add(input.name());
            for (Observed output : dex == null ? List.of(old, java) : List.of(old, java, dex))
                if (output.unsupported()) unsupported++;
            if (!correct) expectedFailures++;
            rows.add(row);
        }
        JsonObject report = new JsonObject();
        report.addProperty("scope", "One DayTrigger dictionary lookup with two original getter dependencies. Interpreter/JVM study over declared typed-list, null, UTF-16 and iterator-fault inputs; not ART, exhaustive Unicode, ill-typed erased lists, calendar or lifecycle coverage.");
        report.addProperty("inputEncoding", "Strings are exact concatenated four-hex-digit UTF-16 code units; JSON null is a null String. This preserves unpaired surrogates.");
        report.addProperty("exceptionComparisonScope", "Only explicitly authored VM-null cases compare the required NPE class and complete event trace; all raw messages are retained. Every other outcome compares the complete record, including injected exception message and reference identity.");
        report.addProperty("primaryMethod", PRIMARY); report.addProperty("primaryRecoveredMethods", 1); report.addProperty("originalDependencyMethods", 2);
        report.addProperty("cases", cases.size()); report.addProperty("executionPaths", rebuilt == null ? 2 : 3);
        report.addProperty("mismatchCount", mismatches.size()); report.addProperty("unsupportedCount", unsupported);
        report.addProperty("independentExpectedChecks", cases.size()); report.addProperty("independentExpectedFailures", expectedFailures);
        report.addProperty("originalDexSha256", fileSha(original)); report.add("loadedClassOrigins", origins);
        report.add("originalCoverage", coverage(reference, ALL)); report.add("observerRecordControls", controls);
        if (rebuilt != null) {
            report.add("rebuiltCoverage", coverage(rebuilt, ALL));
            report.addProperty("rebuiltDexSha256", config.get("rebuiltDexSha256").getAsString());
        }
        report.add("mismatches", mismatches); report.add("observations", rows);
        report.addProperty("passed", mismatches.size() == 0 && unsupported == 0 && expectedFailures == 0
            && report.getAsJsonObject("originalCoverage").get("allInstructionsAndEdgesExecuted").getAsBoolean()
            && (rebuilt == null || report.getAsJsonObject("rebuiltCoverage").get("allInstructionsAndEdgesExecuted").getAsBoolean()));
        Files.writeString(Path.of(args[1]), new GsonBuilder().setPrettyPrinting().serializeNulls().create().toJson(report) + "\n");
        System.out.println("DAY_LOOKUP_STUDY cases=" + cases.size() + " paths=" + (rebuilt == null ? 2 : 3)
            + " mismatches=" + mismatches.size() + " unsupported=" + unsupported + " expectedFailures=" + expectedFailures
            + " passed=" + report.get("passed"));
        if (!report.get("passed").getAsBoolean()) System.exit(3);
    }
}
