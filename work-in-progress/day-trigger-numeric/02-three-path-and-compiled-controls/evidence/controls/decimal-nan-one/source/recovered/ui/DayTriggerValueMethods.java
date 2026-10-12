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
            double n = ((VariableValue.DecimalValue) value).getDecimalValue(); return Double.isNaN(n) ? 1 : (int) n;
        }
        return 0;
    }
}
