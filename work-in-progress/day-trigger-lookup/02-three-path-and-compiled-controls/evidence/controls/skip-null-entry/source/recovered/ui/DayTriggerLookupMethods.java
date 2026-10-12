package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;

/** Private candidate for the original DayTrigger.p0 body; not registered. */
public final class DayTriggerLookupMethods {
    private DayTriggerLookupMethods() {}

    public static DictionaryEntry findEntry(Dictionary dictionary, String key) {
        for (DictionaryEntry entry : dictionary.getEntries()) {
            if (entry == null) continue;
            if (key.equalsIgnoreCase(entry.getKey())) return entry;
        }
        return null;
    }
}
