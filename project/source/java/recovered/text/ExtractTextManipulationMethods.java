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
public final class ExtractTextManipulationMethods {
    private ExtractTextManipulationMethods() {}

    public static String apply(ExtractTextManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        Matcher matcher = Pattern.compile(sr9.l(MacroDroidApplication.i(), macro, triggerContextInfo, self.params.get(0))).matcher(str);
        if (Integer.valueOf(self.params.get(1)).intValue() == 1) {
            if (matcher.find()) {
                try {
                    return matcher.group(1);
                } catch (Exception unused) {
                }
            }
            return "";
        }
        if (Integer.valueOf(self.params.get(1)).intValue() == 0) {
            return matcher.find() ? str.substring(matcher.start(), matcher.end()) : "";
        }
        StringBuilder sb = new StringBuilder();
        while (matcher.find()) {
            sb.append(matcher.group(0));
        }
        return sb.toString();
    }

    public static int describeContents(ExtractTextManipulation self) {
        return 0;
    }

    public static int getDescription(ExtractTextManipulation self) {
        return R.string.text_manipulation_extract_text_description;
    }

    public static String getExtendedInfo(ExtractTextManipulation self, String str) {
        if (str.length() > 28) {
            str = str.substring(0, 28).concat("..");
        }
        StringBuilder sb = new StringBuilder();
        sb.append(self.getString(self.getName()));
        sb.append(" (");
        sb.append(str);
        sb.append(", ");
        return q77.B(self.params.get(0), ")", sb);
    }

    public static int getName(ExtractTextManipulation self) {
        return R.string.text_manipulation_extract_text;
    }

    public static int[] getParamNames(ExtractTextManipulation self) {
        return new int[]{R.string.text_manipulation_text_to_match_regex, 0};
    }

    public static TextManipulation.a[] getParamTypes(ExtractTextManipulation self) {
        return new TextManipulation.a[]{TextManipulation.a.STRING, TextManipulation.a.ENUM};
    }
}
