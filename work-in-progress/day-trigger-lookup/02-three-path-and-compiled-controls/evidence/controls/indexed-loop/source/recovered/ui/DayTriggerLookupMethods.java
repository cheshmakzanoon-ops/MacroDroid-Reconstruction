package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;

/** Private candidate for the original DayTrigger.p0 body; not registered. */
public final class DayTriggerLookupMethods {
    private DayTriggerLookupMethods() {}

    public static DictionaryEntry findEntry(Dictionary dictionary, String key) {
        java.util.List<DictionaryEntry> entries = dictionary.getEntries();
        for (int i = 0; i < entries.size(); i++) {
            DictionaryEntry entry = entries.get(i);
            if (key.equalsIgnoreCase(entry.getKey())) return entry;
        }
        return null;
    }
}
