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
public final class RemoveTextManipulationMethods {
    private RemoveTextManipulationMethods() {}

    public static String apply(RemoveTextManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        int i = 4 & 0;
        String strH0 = vdg.h0(sr9.l(MacroDroidApplication.i(), macro, triggerContextInfo, self.params.get(0)));
        return Integer.valueOf(self.params.get(1)).intValue() == 0 ? str.replaceAll(Pattern.quote(strH0), "") : str.replaceAll(strH0, "");
    }

    public static int describeContents(RemoveTextManipulation self) {
        return 0;
    }

    public static int getDescription(RemoveTextManipulation self) {
        return R.string.text_manipulation_remove_text_description;
    }

    public static String getExtendedInfo(RemoveTextManipulation self, String str) {
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

    public static int getName(RemoveTextManipulation self) {
        return R.string.text_manipulation_remove_text;
    }

    public static int[] getParamNames(RemoveTextManipulation self) {
        return new int[]{R.string.text_to_match, 0};
    }

    public static TextManipulation.a[] getParamTypes(RemoveTextManipulation self) {
        return new TextManipulation.a[]{TextManipulation.a.STRING, TextManipulation.a.ENUM};
    }
}
