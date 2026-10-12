package defpackage;
/** Controls only host test doubles. This class must never be included in an APK. */
public final class EnvironmentControl {
 public static boolean recoveredMatching,locationEnabled=true; public static int permission;
 public static void reset(){recoveredMatching=true;locationEnabled=true;permission=0;android.os.Build.VERSION.SDK_INT=36;com.arlosoft.macrodroid.constraint.WifiHotSpotConstraint.connected=0;com.arlosoft.macrodroid.constraint.WifiHotSpotConstraint.connectedFailure=null;com.arlosoft.macrodroid.settings.c.location=null;TestClock.enabled=false;}
}
