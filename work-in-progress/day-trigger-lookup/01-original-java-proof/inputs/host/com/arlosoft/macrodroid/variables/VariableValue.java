package com.arlosoft.macrodroid.variables;

import java.util.List;

/** Private host field boundary; these classes are not packaged into an APK. */
public abstract class VariableValue {
    public static final class Dictionary extends VariableValue {
        private final List<DictionaryEntry> entries;
        public Dictionary(List<DictionaryEntry> entries) { this.entries = entries; }
        public List<DictionaryEntry> getEntries() { return entries; }
    }

    public static final class DictionaryEntry extends VariableValue {
        private final String key;
        public DictionaryEntry(String key) { this.key = key; }
        public String getKey() { return key; }
    }
}
