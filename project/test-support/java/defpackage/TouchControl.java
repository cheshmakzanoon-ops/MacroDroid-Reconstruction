package defpackage;

import android.content.Intent;
import com.arlosoft.macrodroid.action.services.BlockTouchesService;
import com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean;
import java.util.ArrayList;
import java.util.List;

/** Host-only controlled service boundaries. This is neither Android nor an overlay implementation. */
public final class TouchControl {
    public static final List<Intent> intents = new ArrayList<Intent>();
    public static final List<Intent> starts = new ArrayList<Intent>();
    public static final List<Intent> stops = new ArrayList<Intent>();
    public static final List<String> boundaries = new ArrayList<String>();
    public static int boundaryCalls, failAt, mutateAt, unblockCalls;
    public static int resolvedColor;
    public static boolean resolveColor, stopResult, startReturnsNull;
    public static Throwable failure;
    public static Exception loggedFailure;
    public static String loggedPrefix;
    public static int logCalls;
    public static Runnable mutation;
    public static void reset() {
        intents.clear(); starts.clear(); stops.clear(); boundaries.clear();
        boundaryCalls = 0; failAt = -1; mutateAt = -1; unblockCalls = 0;
        resolvedColor = 0xff102030; resolveColor = true; stopResult = true;
        startReturnsNull = false; failure = null; mutation = null;
        loggedFailure = null; loggedPrefix = null; logCalls = 0;
        BlockTouchesService.i = new BlockTouchesService.a(); BlockTouchesService.j = false;
        MacroDroidAccessibilityServiceJellyBean.u = new MacroDroidAccessibilityServiceJellyBean.a();
        MacroDroidAccessibilityServiceJellyBean.v = false;
        com.arlosoft.macrodroid.variables.a.lastMacro = null;
        com.arlosoft.macrodroid.variables.a.lastVariable = null;
        com.arlosoft.macrodroid.variables.a.lastInfo = null;
        com.arlosoft.macrodroid.variables.a.lastBaseColor = 0;
        com.arlosoft.macrodroid.variables.a.colorCalls = 0;
    }
    public static void hit(String call) {
        CoreTrace.add(call); boundaries.add(call);
        int index = boundaryCalls++;
        if (index == mutateAt && mutation != null) mutation.run();
        if (index == failAt && failure != null) TouchControl.<RuntimeException>raise(failure);
    }
    @SuppressWarnings("unchecked") private static <T extends Throwable> void raise(Throwable error) throws T { throw (T)error; }
}
