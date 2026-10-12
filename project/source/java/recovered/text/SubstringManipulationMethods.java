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
public final class SubstringManipulationMethods {
    private SubstringManipulationMethods() {}

    public static String apply(SubstringManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        int intValue = self.getIntValue(0, macro, triggerContextInfo);
        int intValue2 = self.getIntValue(1, macro, triggerContextInfo);
        if (intValue > str.length()) {
            return "";
        }
        if (intValue2 > str.length()) {
            intValue2 = str.length();
        }
        return str.substring(intValue, intValue2);
    }

    public static int describeContents(SubstringManipulation self) {
        return 0;
    }

    public static int getDescription(SubstringManipulation self) {
        return R.string.text_manipulation_substring_description;
    }

    public static String getExtendedInfo(SubstringManipulation self, String str) {
        if (str.length() > 28) {
            str = str.substring(0, 28).concat("..");
        }
        StringBuilder sb = new StringBuilder();
        sb.append(self.getString(self.getName()));
        sb.append(" (");
        sb.append(str);
        sb.append(", ");
        sb.append(self.params.get(0));
        sb.append(", ");
        return q77.B(self.params.get(1), ")", sb);
    }

    public static int getName(SubstringManipulation self) {
        return R.string.text_manipulation_substring;
    }

    public static int[] getParamNames(SubstringManipulation self) {
        return new int[]{R.string.text_manipulation_start_index, R.string.text_manipulation_end_index};
    }

    public static TextManipulation.a[] getParamTypes(SubstringManipulation self) {
        TextManipulation.a aVar = TextManipulation.a.INTEGER;
        return new TextManipulation.a[]{aVar, aVar};
    }
}
