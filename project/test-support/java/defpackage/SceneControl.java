package defpackage;

import android.content.Intent;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.scene.display.*;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;

/** Host-only scene boundaries; no activity, scene rendering, or Runnable body is executed. */
public final class SceneControl {
    public static boolean active, overlayPermission, nullGuardReturns;
    public static Throwable escaped;
    public static aj5 eventBus;
    public static int permissionReads, permissionWarnings, nullGuards, runCalls;
    public static final List<Intent> activityStarts = new ArrayList<Intent>();
    public static final List<Object> createdEvents = new ArrayList<Object>();
    public static final List<Object> postedEvents = new ArrayList<Object>();
    public static final List<eld> tasks = new ArrayList<eld>();
    public static final List<Runnable> queuedTasks = new ArrayList<Runnable>();
    public static final IdentityHashMap<Object,String> identities = new IdentityHashMap<Object,String>();
    public static void reset() {
        active = false; overlayPermission = true; nullGuardReturns = false; escaped = null;
        permissionReads = 0; permissionWarnings = 0; nullGuards = 0; runCalls = 0;
        activityStarts.clear(); createdEvents.clear(); postedEvents.clear(); tasks.clear(); queuedTasks.clear(); identities.clear();
        MacroDroidApplication.E = new MacroDroidApplication.a();
        MacroDroidApplication.F = new MacroDroidApplication(); MacroDroidApplication.F.u = true;
        SceneOverlayDisplayService.d = new SceneOverlayDisplayService.a();
        SceneDialogActivity.R = new SceneDialogActivity.a();
        SceneDisplayActivity.P = new SceneDisplayActivity.a();
        SceneDisplayActivity.Q = new j$.util.concurrent.ConcurrentHashMap();
        SceneBaseActivity.D = new SceneBaseActivity.a(); SceneBaseActivity.E = "scene_description";
        eventBus = new aj5();
    }
    public static void name(Object object, String name) { if (object != null) identities.put(object, name); }
    public static String id(Object object) {
        if (object == null) return "null";
        if (object instanceof String || object instanceof Number || object instanceof Boolean) return String.valueOf(object);
        String id = identities.get(object);
        if (id == null) { id = object.getClass().getName()+"#"+identities.size(); identities.put(object, id); }
        return id;
    }
}
