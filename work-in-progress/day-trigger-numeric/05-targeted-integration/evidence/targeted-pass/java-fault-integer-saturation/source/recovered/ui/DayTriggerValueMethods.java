package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue;

/** Recovered DayTrigger.r0 body; registration is pending independent proof. */
public final class DayTriggerValueMethods {
    public static int numericValue(VariableValue.DictionaryEntry entry) {
        VariableValue value = entry.getVariable();
        if (value instanceof VariableValue.IntegerValue) {
            long n = ((VariableValue.IntegerValue) value).getIntValue(); return n > Integer.MAX_VALUE ? Integer.MAX_VALUE : n < Integer.MIN_VALUE ? Integer.MIN_VALUE : (int) n;
        }
        if (value instanceof VariableValue.DecimalValue) {
            return (int) ((VariableValue.DecimalValue) value).getDecimalValue();
        }
        return 0;
    }
}
