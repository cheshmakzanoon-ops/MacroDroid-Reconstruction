package recovered.text;

import com.arlosoft.macrodroid.R;
import com.arlosoft.macrodroid.action.textmanipulation.*;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.variables.VariableValue;
import android.os.Parcel;
import defpackage.q77;
import defpackage.vdg;
import defpackage.sr9;
import java.util.*;
import java.util.regex.*;

/** Executable recovered method bodies. Remaining class structure is retained in smali. */
public final class SplitManipulationMethods {
    private SplitManipulationMethods() {}

    public static int describeContents(SplitManipulation self) {
        return 0;
    }

    public static int getDescription(SplitManipulation self) {
        return R.string.text_manipulation_split_to_array_description;
    }

    public static String getExtendedInfo(SplitManipulation self, String str) {
        if (str.length() > 28) {
            str = str.substring(0, 28).concat("..");
        }
        return self.getString(self.getName()) + " (" + str + ")";
    }

    public static int getName(SplitManipulation self) {
        return R.string.text_manipulation_split_to_array;
    }

    public static int[] getParamNames(SplitManipulation self) {
        return new int[]{R.string.text_manipulation_string_delimiter, R.string.text_manipulation_split_to_variable_type};
    }

    public static TextManipulation.a[] getParamTypes(SplitManipulation self) {
        return new TextManipulation.a[]{TextManipulation.a.STRING_OPTIONAL, TextManipulation.a.ENUM};
    }

    public static boolean isArray(SplitManipulation self) {
        return true;
    }

    /** Original split semantics: strip leading direction/zero-width markers, use a
     * literal delimiter, discard trailing empty fields, and default failed numeric
     * conversions to zero. Integer parsing is intentionally 32-bit before widening.
     */
    public static VariableValue.Dictionary applyArray(SplitManipulation self, String input, Macro macro, TriggerContextInfo context) {
        ArrayList<VariableValue.DictionaryEntry> entries = new ArrayList<>();
        if (android.text.TextUtils.isEmpty(input)) {
            return new VariableValue.Dictionary(entries, true, null);
        }
        String delimiter = sr9.l(MacroDroidApplication.i(), macro, context, self.params.get(0));
        delimiter = vdg.h0(delimiter.replace("\\r", "\r"));
        String[] parts = input.replaceFirst("^[\\uFEFF\\uFFFE\\u200B\\u200C\\u200D\\u2060]+", "")
                .split(Pattern.quote(delimiter));
        for (int index = 0; index < parts.length; index++) {
            // Re-read the configuration for every element, as the original does.
            int type = Integer.valueOf(self.params.get(1)).intValue();
            switch (type) {
                case 0:
                    entries.add(new VariableValue.DictionaryEntry(String.valueOf(index),
                            new VariableValue.StringValue(parts[index], null), null));
                    break;
                case 1:
                    int integer;
                    try { integer = Integer.valueOf(parts[index]).intValue(); }
                    catch (Exception failure) { integer = 0; }
                    entries.add(new VariableValue.DictionaryEntry(String.valueOf(index),
                            new VariableValue.IntegerValue((long) integer, null), null));
                    break;
                case 2:
                    double decimal;
                    try { decimal = Double.valueOf(parts[index]).doubleValue(); }
                    catch (Exception failure) { decimal = 0.0d; }
                    entries.add(new VariableValue.DictionaryEntry(String.valueOf(index),
                            new VariableValue.DecimalValue(decimal, null), null));
                    break;
                case 3:
                    entries.add(new VariableValue.DictionaryEntry(String.valueOf(index),
                            new VariableValue.BooleanValue(parts[index].equalsIgnoreCase("true"), null), null));
                    break;
                default:
                    // Unsupported types produce no entry, rather than a string fallback.
                    break;
            }
        }
        return new VariableValue.Dictionary(entries, true, null);
    }

    public static int[] getEnumNames(SplitManipulation self, int index) {
        if (index == 1) {
            return new int[]{R.string.string, R.string.integer, R.string.decimal, R.string.bool};
        }
        // The original invokes TextManipulation.getEnumNames directly, which returns
        // a fresh empty array; it does not dispatch to an override on self.
        return new int[0];
    }
}
