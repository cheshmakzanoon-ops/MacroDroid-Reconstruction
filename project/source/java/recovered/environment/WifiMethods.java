package recovered.environment;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.net.wifi.SupplicantState;
import android.os.Build;
import android.text.TextUtils;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.WifiConstraint;
import com.arlosoft.macrodroid.constraint.WifiHotSpotConstraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.cg9;
import defpackage.htg;
import defpackage.jb3;
import defpackage.kjf;
import defpackage.lob;
import defpackage.q77;
import defpackage.sz5;
import defpackage.w63;
import java.lang.reflect.Method;
import java.util.List;

/** Recovered Wi-Fi state/SSID and hotspot decisions. No permission checks are removed.
 * These reproduce the uploaded implementation, including its legacy fall-throughs.
 */
public final class WifiMethods {
    public static boolean evaluate(WifiConstraint self, TriggerContextInfo ignored) {
        int api = Build.VERSION.SDK_INT;
        if (api >= 27 && w63.checkSelfPermission(((SelectableItem) self).getContext(),
                "android.permission.ACCESS_FINE_LOCATION") != 0) {
            kjf.g(((SelectableItem) self).getMacroGuid().longValue(),
                    "Could not get Wifi SSID, location access/permission is required on Android 8.1+");
            Context context = ((SelectableItem) self).getContext();
            String name = self.getConfiguredName();
            lob.v(context, "android.permission.ACCESS_FINE_LOCATION", name);
            return false;
        }
        WifiManager manager = (WifiManager) ((SelectableItem) self).getContext()
                .getApplicationContext().getSystemService("wifi");
        boolean enabled = manager.getWifiState() == 3;
        WifiInfo info = manager.getConnectionInfo();
        SupplicantState state = info == null ? null : info.getSupplicantState();
        String current = null;
        if (info != null) {
            String ssid = info.getSSID();
            if (ssid != null) {
                if (ssid.startsWith("\"") && ssid.endsWith("\"")) ssid = q77.x(1, 1, ssid);
                if (ssid.equals("0x") || ssid.length() == 0 || ssid.equals("<unknown ssid>")) ssid = null;
            }
            current = ssid;
        }
        // The legacy one-SSID field is migrated even in enable/disable query modes.
        if (self.m_SSIDList.isEmpty()) self.m_SSIDList.add(self.m_SSID);
        int wanted = self.m_wifiState;
        if (wanted == 0) return enabled;
        if (wanted == 1) return !enabled;
        if (wanted != 2 && wanted != 3) {
            jb3.J("WifiConstraint: Invalid Wifi State");
            return true;
        }
        List selected = self.m_SSIDList;
        List initializationRead = htg.a;
        if (selected != null) {
            for (Object raw : selected) {
                String ssid = (String) raw;
                if (htg.a.contains(ssid)) {
                    return wanted == 2 ? state == SupplicantState.COMPLETED : state != SupplicantState.COMPLETED;
                }
            }
        }
        if (!TextUtils.isEmpty(current) && !current.equals("0x")) {
            boolean found = self.m_SSIDList.contains(current);
            return wanted == 2 ? found : !found;
        }
        if (api >= 27 && !cg9.a(((SelectableItem) self).getContext())) {
            kjf.g(((SelectableItem) self).getMacroGuid().longValue(),
                    "Wifi Constraint could not get current SSID, location services must be enabled on Android 8.1+");
        }
        return wanted == 3;
    }

    public static boolean hotspot(WifiHotSpotConstraint self, TriggerContextInfo ignored) {
        WifiManager manager = (WifiManager) ((SelectableItem) self).getContext()
                .getApplicationContext().getSystemService("wifi");
        try {
            Method method = manager.getClass().getDeclaredMethod("getWifiApState", (Class<?>[]) null);
            ((java.lang.reflect.AccessibleObject) method).setAccessible(true);
            int state = ((Integer) method.invoke(manager, (Object[]) null)).intValue();
            if (state > 10) state -= 10;
            if (state == 0 || state == 1 || state == 4) return !self.m_enabled;
            if (state == 2 || state == 3) {
                if (!self.m_checkConnections || Build.VERSION.SDK_INT >= 29) return self.m_enabled;
                int connected = WifiHotSpotConstraint.l0();
                int comparison = self.m_comparisonValue;
                if (comparison == 0) return connected == self.m_connectedCount;
                if (comparison == 1) return connected < self.m_connectedCount;
                if (comparison == 2) return connected > self.m_connectedCount;
            }
            return true;
        } catch (Exception failure) {
            String message = q77.z(failure, new StringBuilder("Error getting wifi AP State: "));
            kjf.g(((SelectableItem) self).getMacroGuid().longValue(), message);
            String crashMessage = q77.z(failure, new StringBuilder("Error getting wifi AP State: "));
            sz5.e(new RuntimeException(crashMessage));
            return true;
        }
    }
}
