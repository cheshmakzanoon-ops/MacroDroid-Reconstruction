package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue;

/** Recovered DayTrigger.r0 body; registration is pending independent proof. */
public final class DayTriggerValueMethods {
    public static int numericValue(VariableValue.DictionaryEntry entry) {
        VariableValue value = entry.getVariable();
        if (value instanceof VariableValue.IntegerValue) {
            return (byte) ((VariableValue.IntegerValue) value).getIntValue();
        }
        if (value instanceof VariableValue.DecimalValue) {
            return (int) ((VariableValue.DecimalValue) value).getDecimalValue();
        }
        return 0;
    }
}
