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
public final class TextManipulationMethods {
    private TextManipulationMethods() {}

    public static String apply(TextManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        return str;
    }

    public static VariableValue.Dictionary applyArray(TextManipulation self, String str, Macro macro, TriggerContextInfo triggerContextInfo) {
        return null;
    }

    public static List<TextManipulation> getAllTextManipulations() {
        ArrayList arrayList = new ArrayList();
        arrayList.add(new SubstringManipulation());
        arrayList.add(new ReplaceAllManipulation());
        arrayList.add(new ExtractTextManipulation());
        arrayList.add(new UpperCaseManipulation());
        arrayList.add(new LowerCaseManipulation());
        arrayList.add(new TrimManipulation());
        arrayList.add(new SplitManipulation());
        arrayList.add(new RemoveTextManipulation());
        return arrayList;
    }

    public static String getDefaultValue(TextManipulation self, int i) {
        return null;
    }

    public static int[] getEnumNames(TextManipulation self, int i) {
        return new int[0];
    }

    public static boolean getLeaveNewLines(TextManipulation self) {
        return false;
    }

    public static List<String> getParams(TextManipulation self) {
        return self.params;
    }

    public static String getString(TextManipulation self, int i) {
        return ((android.content.Context) MacroDroidApplication.i()).getString(i);
    }

    public static boolean getTestLeaveNewLines(TextManipulation self) {
        return self.getLeaveNewLines();
    }

    public static boolean isArray(TextManipulation self) {
        return false;
    }

    public static void setParams(TextManipulation self, List<String> list) {
        self.params = list;
    }

    public static void writeToParcel(TextManipulation self, Parcel parcel, int i) {
        parcel.writeStringList(self.params);
    }
}
