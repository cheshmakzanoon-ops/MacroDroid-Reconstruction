package com.arlosoft.macrodroid.variables;

/** Minimal host field containers; Android constructors/Parcel are outside this study. */
public abstract class VariableValue {
    public static final class DictionaryEntry extends VariableValue {
        private VariableValue variable;
        public DictionaryEntry(VariableValue value) { variable = value; }
        public VariableValue getVariable() { return variable; }
    }

    public static final class IntegerValue extends VariableValue {
        private final long intValue;
        public IntegerValue(long value) { intValue = value; }
        public long getIntValue() { return intValue; }
    }

    public static final class DecimalValue extends VariableValue {
        private final double decimalValue;
        public DecimalValue(double value) { decimalValue = value; }
        public double getDecimalValue() { return decimalValue; }
    }

    public static final class StringValue extends VariableValue {
        public final String text;
        public StringValue(String value) { text = value; }
    }

    public static final class BooleanValue extends VariableValue {
        public final boolean value;
        public BooleanValue(boolean value) { this.value = value; }
    }

    public static final class Dictionary extends VariableValue {
        public Dictionary() {}
    }
}
