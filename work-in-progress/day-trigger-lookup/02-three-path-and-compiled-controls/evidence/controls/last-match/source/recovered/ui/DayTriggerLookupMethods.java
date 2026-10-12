package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;

/** Private candidate for the original DayTrigger.p0 body; not registered. */
public final class DayTriggerLookupMethods {
    private DayTriggerLookupMethods() {}

    public static DictionaryEntry findEntry(Dictionary dictionary, String key) {
        DictionaryEntry match = null;
        for (DictionaryEntry entry : dictionary.getEntries()) {
            if (key.equalsIgnoreCase(entry.getKey())) match = entry;
        }
        return match;
    }
}
