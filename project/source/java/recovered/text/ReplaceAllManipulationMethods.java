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
public final class ReplaceAllManipulationMethods {
    private ReplaceAllManipulationMethods() {}

    public static String apply(ReplaceAllManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        boolean zEqualsIgnoreCase = self.params.size() > 2 ? self.params.get(2).equalsIgnoreCase("true") : true;
        String strN = sr9.n(MacroDroidApplication.i(), self.params.get(0), triggerContextInfo, macro, zEqualsIgnoreCase);
        if (zEqualsIgnoreCase) {
            strN = vdg.h0(strN);
        }
        String strN2 = sr9.n(MacroDroidApplication.i(), self.params.get(1), triggerContextInfo, macro, zEqualsIgnoreCase);
        if (zEqualsIgnoreCase) {
            strN2 = vdg.h0(strN2);
        }
        if (zEqualsIgnoreCase) {
            str = vdg.h0(str);
        }
        return sr9.n(MacroDroidApplication.i(), str.replaceAll(strN, strN2), triggerContextInfo, macro, zEqualsIgnoreCase);
    }

    public static int describeContents(ReplaceAllManipulation self) {
        return 0;
    }

    public static String getDefaultValue(ReplaceAllManipulation self, int i) {
        if (i == 2) {
            return "true";
        }
        return null;
    }

    public static int getDescription(ReplaceAllManipulation self) {
        return R.string.text_manipulation_replace_all_description;
    }

    public static String getExtendedInfo(ReplaceAllManipulation self, String str) {
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

    public static boolean getLeaveNewLines(ReplaceAllManipulation self) {
        return self.params.size() > 2 && !self.params.get(2).equalsIgnoreCase("true");
    }

    public static int getName(ReplaceAllManipulation self) {
        return R.string.text_manipulation_replace_all;
    }

    public static int[] getParamNames(ReplaceAllManipulation self) {
        return new int[]{R.string.text_manipulation_text_to_replace_regex, R.string.text_manipulation_new_text, R.string.text_manipulation_convert_slashn_to_newline};
    }

    public static TextManipulation.a[] getParamTypes(ReplaceAllManipulation self) {
        return new TextManipulation.a[]{TextManipulation.a.STRING, TextManipulation.a.STRING_OPTIONAL, TextManipulation.a.BOOLEAN};
    }

    public static boolean getTestLeaveNewLines(ReplaceAllManipulation self) {
        return true;
    }
}
