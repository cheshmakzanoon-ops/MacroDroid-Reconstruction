package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;

/** Exact recovery of the original DayTrigger.p0 method body. */
public final class DayTriggerLookupMethods {
    private DayTriggerLookupMethods() {}

    public static DictionaryEntry findEntry(Dictionary dictionary, String key) {
        for (DictionaryEntry entry : dictionary.getEntries()) {
            if (key.equalsIgnoreCase(entry.getKey())) return entry;
        }
        return null;
    }
}
