package recovered.environment;

import android.provider.Settings;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.SystemSettingConstraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.f9f;
import defpackage.g9f;
import defpackage.kjf;
import defpackage.yih;

/** Source reconstruction of the setting read, integer comparison and text comparison.
 * Table order, magic-text calls, null defaults, unknown selectors, and catch boundaries
 * follow the uploaded DEX. In particular, an unknown value type returns true.
 */
public final class SystemSettingMethods {
    public static boolean evaluate(SystemSettingConstraint self, TriggerContextInfo context) {
        String missing = ") does not exist on this device: ";
        String prefix = "Constraint check failed. The setting (";
        String name = ((SelectableItem) self).applyMagicText(self.settingString, context);
        try {
            int type = self.valueType;
            if (type == 0) {
                int table = self.tableOption;
                int value;
                if (table == SystemSettingConstraint.TABLE_OPTION_SYSTEM) {
                    value = Settings.System.getInt(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_SECURE) {
                    value = Settings.Secure.getInt(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_GLOBAL) {
                    value = Settings.Global.getInt(((SelectableItem) self).getContext().getContentResolver(), name);
                } else {
                    throw new IllegalArgumentException();
                }
                return self.r0((long) value, context);
            }
            if (type == 1) {
                int table = self.tableOption;
                float value;
                if (table == SystemSettingConstraint.TABLE_OPTION_SYSTEM) {
                    value = Settings.System.getFloat(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_SECURE) {
                    value = Settings.Secure.getFloat(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_GLOBAL) {
                    value = Settings.Global.getFloat(((SelectableItem) self).getContext().getContentResolver(), name);
                } else {
                    throw new IllegalArgumentException();
                }
                String expanded = ((SelectableItem) self).applyMagicText(self.valueString, context);
                expanded.getClass();
                Float parsed = f9f.e1(expanded);
                float threshold = parsed == null ? 0.0f : parsed.floatValue();
                int operator = self.equalityCheckOption;
                if (operator == 2) return value < threshold;
                if (operator == 3) return value > threshold;
                if (operator == 0) return threshold == value;
                return threshold != value;
            }
            if (type == 2) {
                int table = self.tableOption;
                long value;
                if (table == SystemSettingConstraint.TABLE_OPTION_SYSTEM) {
                    value = Settings.System.getLong(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_SECURE) {
                    value = Settings.Secure.getLong(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_GLOBAL) {
                    value = Settings.Global.getLong(((SelectableItem) self).getContext().getContentResolver(), name);
                } else {
                    throw new IllegalArgumentException();
                }
                return self.r0(value, context);
            }
            if (type == 3) {
                int table = self.tableOption;
                String value;
                if (table == SystemSettingConstraint.TABLE_OPTION_SYSTEM) {
                    value = Settings.System.getString(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_SECURE) {
                    value = Settings.Secure.getString(((SelectableItem) self).getContext().getContentResolver(), name);
                } else if (table == SystemSettingConstraint.TABLE_OPTION_GLOBAL) {
                    value = Settings.Global.getString(((SelectableItem) self).getContext().getContentResolver(), name);
                } else {
                    throw new IllegalArgumentException();
                }
                if (value != null) return self.t0(value, context);
                StringBuilder message = new StringBuilder(prefix);
                message.append(name).append(missing).append(name);
                kjf.h(message.toString());
                return false;
            }
            return true;
        } catch (Settings.SettingNotFoundException missingSetting) {
            StringBuilder message = new StringBuilder(prefix);
            message.append(name).append(missing).append(name);
            kjf.h(message.toString());
            return false;
        } catch (SecurityException denied) {
            StringBuilder message = new StringBuilder(prefix);
            message.append(name).append(") cannot be read: ").append(denied);
            kjf.h(message.toString());
            return false;
        }
    }

    public static boolean compareInteger(SystemSettingConstraint self, long value, TriggerContextInfo context) {
        String expanded = ((SelectableItem) self).applyMagicText(self.valueString, context);
        expanded.getClass();
        Long parsed = g9f.v1(expanded);
        long threshold = parsed == null ? 0L : parsed.longValue();
        int operator = self.equalityCheckOption;
        if (operator == 2) return value < threshold;
        if (operator == 3) return value > threshold;
        if (operator == 0) return threshold == value;
        return threshold != value;
    }

    public static boolean compareText(SystemSettingConstraint self, String value, TriggerContextInfo context) {
        String expanded = ((SelectableItem) self).applyMagicText(self.valueString, context);
        String full = yih.c(expanded, self.regexEnabled, true);
        String contains = yih.b(expanded, self.regexEnabled, true);
        int operator = self.equalityCheckOption;
        boolean regex = self.regexEnabled;
        if (operator == 2) return yih.d(value, contains, regex, true);
        if (operator == 3) return !yih.d(value, contains, regex, true);
        boolean matched = yih.d(value, full, regex, true);
        return self.equalityCheckOption == 0 ? matched : !matched;
    }
}
