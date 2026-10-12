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
public final class TrimManipulationMethods {
    private TrimManipulationMethods() {}

    public static String apply(TrimManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        return vdg.u0(str.trim());
    }

    public static int describeContents(TrimManipulation self) {
        return 0;
    }

    public static int getDescription(TrimManipulation self) {
        return R.string.text_manipulation_trim_whitespace_description;
    }

    public static String getExtendedInfo(TrimManipulation self, String str) {
        if (str.length() > 28) {
            str = str.substring(0, 28).concat("..");
        }
        return self.getString(self.getName()) + " (" + str + ")";
    }

    public static int getName(TrimManipulation self) {
        return R.string.text_manipulation_trim_whitespace;
    }

    public static int[] getParamNames(TrimManipulation self) {
        return new int[0];
    }

    public static TextManipulation.a[] getParamTypes(TrimManipulation self) {
        return new TextManipulation.a[0];
    }
}
