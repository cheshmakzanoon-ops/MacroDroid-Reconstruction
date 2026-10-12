package recovered.ui;

import com.arlosoft.macrodroid.variables.VariableValue;

/** Recovered DayTrigger.r0 body; registration is pending independent proof. */
public final class DayTriggerValueMethods {
    public static int numericValue(VariableValue.DictionaryEntry entry) {
        VariableValue value = entry.getVariable();
        if (value instanceof VariableValue.IntegerValue) {
            return (int) ((VariableValue.IntegerValue) value).getIntValue();
        }
        if (value instanceof VariableValue.DecimalValue) {
            return (int) ((VariableValue.DecimalValue) value).getDecimalValue();
        }
        if (value instanceof VariableValue.StringValue) return Integer.parseInt(((VariableValue.StringValue) value).value);
        return 0;
    }
}
