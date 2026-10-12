package recovered.environment;

import android.text.TextUtils;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.SunsetSunriseConstraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.settings.c;
import defpackage.aqc;
import defpackage.g94;
import defpackage.kjf;
import defpackage.n7b;
import defpackage.nc5;
import defpackage.srh;
import defpackage.xj2;
import java.util.Calendar;
import java.util.List;
import java.util.ListIterator;
import java.util.TimeZone;

/** Restores the failed sunrise/sunset constraint decompilation. The numeric-parse
 * catch deliberately excludes coordinate construction and astronomical calculations.
 */
public final class SolarConstraintMethods {
    public static boolean evaluate(SunsetSunriseConstraint self, TriggerContextInfo ignored) {
        String location = c.l0(((SelectableItem) self).getContext());
        if (TextUtils.isEmpty(location)) {
            Long guid = ((SelectableItem) self).getMacroGuid();
            guid.getClass();
            kjf.g(guid.longValue(), "Failed to evaluate sunset/sunrise constraint - no location set");
            return false;
        }
        location.getClass();
        List parts = new aqc(",").h(0, location);
        List retained = nc5.a;
        if (!parts.isEmpty()) {
            ListIterator iterator = parts.listIterator(parts.size());
            while (iterator.hasPrevious()) {
                if (((String) iterator.previous()).length() != 0) {
                    retained = xj2.c1(parts, iterator.nextIndex() + 1);
                    break;
                }
            }
        }
        String[] values = (String[]) ((java.util.Collection) retained).toArray(new String[0]);
        if (values.length < 2) {
            String message = "Failed to evaluate sunset/sunrise constraint - malformed location: ".concat(location);
            Long guid = ((SelectableItem) self).getMacroGuid();
            guid.getClass();
            kjf.g(guid.longValue(), message);
            return false;
        }
        double latitude;
        double longitude;
        try {
            Double first = Double.valueOf(values[0]);
            first.getClass();
            latitude = first.doubleValue();
            Double second = Double.valueOf(values[1]);
            second.getClass();
            longitude = second.doubleValue();
        } catch (NumberFormatException invalidCoordinate) {
            String message = "Failed to evaluate sunset/sunrise constraint - invalid location values: ".concat(location);
            Long guid = ((SelectableItem) self).getMacroGuid();
            guid.getClass();
            kjf.g(guid.longValue(), message);
            return false;
        }
        g94 coordinates = new g94(latitude, longitude);
        TimeZone zone = TimeZone.getDefault();
        n7b calculator = new n7b(16, coordinates, zone);
        Calendar now = Calendar.getInstance();
        int option = self.option;
        if (option == 0 || option == 1) {
            Calendar event = n7b.D(calculator.v(srh.b, now, true), now);
            boolean before = now.before(event);
            return self.option == 0 ? before : !before;
        }
        Calendar event = n7b.D(calculator.v(srh.b, now, false), now);
        boolean before = now.before(event);
        return self.option == 2 ? before : !before;
    }
}
