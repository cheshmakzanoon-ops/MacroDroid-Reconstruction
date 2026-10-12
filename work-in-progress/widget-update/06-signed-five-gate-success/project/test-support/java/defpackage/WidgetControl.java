package defpackage;

import android.content.Context;
import android.appwidget.AppWidgetManager;
import com.arlosoft.macrodroid.widget.custom.b;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;

/** Host-only observable widget boundaries; no Android service or scheduler runs. */
public final class WidgetControl {
    public static boolean active, invalidLabelReturns;
    public static int boundaryCalls, failAt, mutateAt, firstReads, secondReads;
    public static Throwable failure, escaped;
    public static Object returned;
    public static Runnable mutation;
    public static b current;
    public static AppWidgetManager backend;
    public static final List<String> boundaries = new ArrayList<String>();
    public static final List<String> states = new ArrayList<String>();
    public static final List<b> continuations = new ArrayList<b>();
    public static final List<wx6> managers = new ArrayList<wx6>();
    public static final List<hn9> renderers = new ArrayList<hn9>();
    public static final List<mh0> identifiers = new ArrayList<mh0>();
    public static final List<rff> factories = new ArrayList<rff>();
    public static final List<Call> firstCalls = new ArrayList<Call>();
    public static final List<Call> secondCalls = new ArrayList<Call>();
    public static final List<Object> firstResults = new ArrayList<Object>();
    public static final List<Object> secondResults = new ArrayList<Object>();
    public static final IdentityHashMap<Object,String> identities = new IdentityHashMap<Object,String>();

    public static void reset() {
        active = false; invalidLabelReturns = false; boundaryCalls = 0;
        failAt = -1; mutateAt = -1; firstReads = 0; secondReads = 0;
        failure = null; escaped = null; returned = null; mutation = null; current = null;
        boundaries.clear(); states.clear(); continuations.clear(); managers.clear(); renderers.clear();
        identifiers.clear(); factories.clear(); firstCalls.clear(); secondCalls.clear();
        firstResults.clear(); secondResults.clear(); identities.clear();
        backend = new AppWidgetManager();
        name(backend, "backend"); name(blg.a, "unit"); name(v93.COROUTINE_SUSPENDED, "suspended");
    }

    public static void name(Object value, String name) {
        if (value != null) identities.put(value, name);
    }

    public static String id(Object value) {
        if (value == null) return "null";
        String known = identities.get(value);
        if (known != null) return known;
        if (value instanceof String || value instanceof Number || value instanceof Boolean || value instanceof Enum)
            return String.valueOf(value);
        String name = value.getClass().getName() + "#" + identities.size();
        identities.put(value, name);
        return name;
    }

    public static String state(b value) {
        if (value == null) return "null";
        return value.label + ":" + value.I$0 + ":" + value.I$1 + ":" + value.I$2
            + ":" + id(value.L$0) + ":" + id(value.L$1) + ":" + id(value.L$2) + ":" + id(value.L$3)
            + ":" + id(value.L$4) + ":" + id(value.L$5) + ":" + id(value.L$6) + ":" + id(value.L$7)
            + ":" + id(value.result) + ":" + id(value.this$0) + ":" + id(value.completion);
    }

    public static void hit(String call) {
        if (!active) return;
        boundaries.add(call); states.add(state(current));
        int index = boundaryCalls++;
        if (index == mutateAt && mutation != null) mutation.run();
        if (index == failAt && failure != null) raise(failure);
    }

    public static void raise(Throwable error) { WidgetControl.<RuntimeException>raiseAs(error); }
    @SuppressWarnings("unchecked") private static <T extends Throwable> void raiseAs(Throwable error) throws T { throw (T) error; }

    public static Object result(List<Object> plan, int index, Object fallback) {
        Object value = index < plan.size() ? plan.get(index) : fallback;
        if (value instanceof g3d) raise(((g3d) value).exception);
        return value;
    }

    public static final class Call {
        public final Object receiver, identifier, factory, continuation;
        public final Context context;
        public final String state;
        public Call(Object receiver, Context context, gy6 identifier, jn6 factory, o73 continuation) {
            this.receiver = receiver; this.context = context; this.identifier = identifier;
            this.factory = factory; this.continuation = continuation;
            this.state = WidgetControl.state(continuation instanceof b ? (b) continuation : null);
        }
    }
}
