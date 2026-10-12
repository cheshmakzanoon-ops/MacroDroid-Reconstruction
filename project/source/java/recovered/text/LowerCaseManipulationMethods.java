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
public final class LowerCaseManipulationMethods {
    private LowerCaseManipulationMethods() {}

    public static String apply(LowerCaseManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        return str.toLowerCase();
    }

    public static int describeContents(LowerCaseManipulation self) {
        return 0;
    }

    public static int getDescription(LowerCaseManipulation self) {
        return R.string.text_manipulation_lowercase_description;
    }

    public static String getExtendedInfo(LowerCaseManipulation self, String str) {
        if (str.length() > 28) {
            str = str.substring(0, 28).concat("..");
        }
        return self.getString(self.getName()) + " (" + str + ")";
    }

    public static int getName(LowerCaseManipulation self) {
        return R.string.text_manipulation_lowercase;
    }

    public static int[] getParamNames(LowerCaseManipulation self) {
        return new int[0];
    }

    public static TextManipulation.a[] getParamTypes(LowerCaseManipulation self) {
        return new TextManipulation.a[0];
    }
}
