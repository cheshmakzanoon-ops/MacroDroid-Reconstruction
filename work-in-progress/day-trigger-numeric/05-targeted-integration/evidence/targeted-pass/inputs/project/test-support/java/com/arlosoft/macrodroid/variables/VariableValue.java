package com.arlosoft.macrodroid.variables;
import java.util.*;
/** Host boundary recorders, NOT recovered Android implementations and NOT packaged. */
public class VariableValue {
 public static class Dictionary extends VariableValue { public final List<DictionaryEntry> entries; public final boolean array; public final List<String> keys; public Dictionary(List<DictionaryEntry> e, boolean a, List<String> k){ entries=e;array=a;keys=k; } }
 public static class DictionaryEntry extends VariableValue { public boolean equals(Object other){ return super.equals(other); } public final String key; public final VariableValue value; public final List<String> keys; private transient final VariableValue variable; public DictionaryEntry(String k,VariableValue v,List<String> ks){key=k;value=v;keys=ks;variable=v;} public final VariableValue getVariable(){return variable;} }
 public static class StringValue extends VariableValue {public final String value;public StringValue(String v,List<String> k){value=v;} }
 public static class IntegerValue extends VariableValue {public final long value;private transient final long intValue;public IntegerValue(long v,List<String> k){value=v;intValue=v;} public final long getIntValue(){return intValue;} }
 public static class DecimalValue extends VariableValue {public final double value;private transient final double decimalValue;public DecimalValue(double v,List<String> k){value=v;decimalValue=v;} public final double getDecimalValue(){return decimalValue;} }
 public static class BooleanValue extends VariableValue {public final boolean value;public BooleanValue(boolean v,List<String> k){value=v;} }
}
