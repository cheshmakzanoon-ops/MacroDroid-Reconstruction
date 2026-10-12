package defpackage;

import android.os.Bundle;
import com.arlosoft.macrodroid.plugins.b;
import com.arlosoft.macrodroid.plugins.b$a;
import com.arlosoft.macrodroid.plugins.b$b$a;
import com.arlosoft.macrodroid.plugins.b$b$b;
import com.arlosoft.macrodroid.plugins.j;
import com.google.firebase.analytics.FirebaseAnalytics;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;

/** Controlled plugin dependencies, never included in the APK. No network/scheduler is run. */
public final class PluginControl {
    public static boolean active, invalidLabelReturns;
    public static int boundaryCalls, failAt, mutateAt;
    public static Throwable failure, escaped;
    public static Object returned;
    public static Runnable mutation;
    public static j self;
    public static final List<String> boundaries = new ArrayList<String>();
    public static final List<String> states = new ArrayList<String>();
    public static final List<Bundle> bundles = new ArrayList<Bundle>();
    public static final List<Constructed> created = new ArrayList<Constructed>();
    public static final List<Publication> publicationAttempts = new ArrayList<Publication>();
    public static final List<Publication> publications = new ArrayList<Publication>();
    public static final List<Analytics> analyticsAttempts = new ArrayList<Analytics>();
    public static final List<Analytics> analytics = new ArrayList<Analytics>();
    public static final IdentityHashMap<Object,String> identities = new IdentityHashMap<Object,String>();
    public static void reset() {
        active = false; invalidLabelReturns = false; boundaryCalls = 0; failAt = -1; mutateAt = -1;
        failure = null; escaped = null; returned = null; mutation = null; self = null;
        boundaries.clear(); states.clear(); bundles.clear(); created.clear();
        publicationAttempts.clear(); publications.clear(); analyticsAttempts.clear(); analytics.clear(); identities.clear();
        b.k = new b$a(); b.l = new ArrayList();
        b$b$a.a = new b$b$a(); b$b$b.a = new b$b$b();
        sz5.a = new sz5(); sz5.b = new FirebaseAnalytics();
        name(blg.a, "unit"); name(v93.COROUTINE_SUSPENDED, "suspended");
        name(b$b$a.a, "connectionError"); name(b$b$b.a, "attemptLimit");
    }
    public static void name(Object value, String name) { if (value != null) identities.put(value, name); }
    public static String id(Object value) {
        if (value == null) return "null";
        String known = identities.get(value); if (known != null) return known;
        if (value instanceof String || value instanceof Number || value instanceof Boolean || value instanceof Enum) return String.valueOf(value);
        String name = value.getClass().getName() + "#" + identities.size(); identities.put(value, name); return name;
    }
    public static void hit(String call) {
        if (!active) return;
        boundaries.add(call);
        states.add(self == null ? "null" : self.label + ":" + self.I$0 + ":" + self.I$1 + ":" + id(self.this$0) + ":" + (self.this$0 == null ? "null" : self.this$0.h));
        int index = boundaryCalls++;
        if (index == mutateAt && mutation != null) mutation.run();
        if (index == failAt && failure != null) raise(failure);
    }
    public static void raise(Throwable error) { PluginControl.<RuntimeException>raiseAs(error); }
    @SuppressWarnings("unchecked") private static <T extends Throwable> void raiseAs(Throwable error) throws T { throw (T) error; }
    public static void constructed(Object object, String kind, Object value) {
        name(object, "payload" + created.size());
        created.add(new Constructed(object, kind, value));
        hit("payload.new:" + id(object) + ":" + kind + ":" + id(value));
    }
    public static final class Constructed {
        public final Object object, value; public final String kind;
        public Constructed(Object object, String kind, Object value) { this.object = object; this.kind = kind; this.value = value; }
    }
    public static final class Publication {
        public final Object receiver, value;
        public Publication(Object receiver, Object value) { this.receiver = receiver; this.value = value; }
    }
    public static final class Analytics {
        public final Object receiver; public final Bundle bundle; public final String event;
        public final LinkedHashMap<String,Integer> values;
        public Analytics(Object receiver, Bundle bundle, String event) {
            this.receiver = receiver; this.bundle = bundle; this.event = event;
            values = bundle == null ? null : new LinkedHashMap<String,Integer>(bundle.values);
        }
    }
}
