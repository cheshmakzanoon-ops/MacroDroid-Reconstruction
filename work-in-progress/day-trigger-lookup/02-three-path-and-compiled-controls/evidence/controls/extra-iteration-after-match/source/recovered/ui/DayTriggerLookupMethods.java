package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue.Dictionary;
import com.arlosoft.macrodroid.variables.VariableValue.DictionaryEntry;

/** Private candidate for the original DayTrigger.p0 body; not registered. */
public final class DayTriggerLookupMethods {
    private DayTriggerLookupMethods() {}

    public static DictionaryEntry findEntry(Dictionary dictionary, String key) {
        java.util.Iterator<DictionaryEntry> entries = dictionary.getEntries().iterator();
        while (entries.hasNext()) {
            DictionaryEntry entry = entries.next();
            if (key.equalsIgnoreCase(entry.getKey())) { entries.hasNext(); return entry; }
        }
        return null;
    }
}
