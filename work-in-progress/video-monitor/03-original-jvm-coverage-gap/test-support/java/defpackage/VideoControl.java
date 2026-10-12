package defpackage;

import com.arlosoft.macrodroid.action.services.BaseVideoRecordingService;
import com.arlosoft.macrodroid.action.services.BaseVideoRecordingService$a;
import com.arlosoft.macrodroid.action.services.a;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Controlled host boundaries only; no filesystem, scheduler, dispatcher or Android service runs. */
public final class VideoControl {
    public static boolean active, invalidLabelReturns;
    public static int boundaryCalls, failAt, mutateAt, delayReads, dispatchReads;
    public static Throwable failure, escaped;
    public static Object returned;
    public static Runnable mutation;
    public static a current;
    public static final List<String> boundaries = new ArrayList<String>();
    public static final List<String> states = new ArrayList<String>();
    public static final List<BaseVideoRecordingService> owners = new ArrayList<BaseVideoRecordingService>();
    public static final List<VideoFile> files = new ArrayList<VideoFile>();
    public static final List<d31> callbacks = new ArrayList<d31>();
    public static final List<DelayCall> delays = new ArrayList<DelayCall>();
    public static final List<DispatchCall> dispatches = new ArrayList<DispatchCall>();
    public static final List<Object> delayResults = new ArrayList<Object>();
    public static final List<Object> dispatchResults = new ArrayList<Object>();
    public static final Map<Integer,Throwable> failures = new LinkedHashMap<Integer,Throwable>();
    public static final Map<Integer,Runnable> mutations = new LinkedHashMap<Integer,Runnable>();
    public static final IdentityHashMap<Object,String> identities = new IdentityHashMap<Object,String>();

    public static void reset() {
        active = false; invalidLabelReturns = false; boundaryCalls = 0;
        failAt = -1; mutateAt = -1; delayReads = 0; dispatchReads = 0;
        failure = null; escaped = null; returned = null; mutation = null; current = null;
        boundaries.clear(); states.clear(); owners.clear(); files.clear(); callbacks.clear();
        delays.clear(); dispatches.clear(); delayResults.clear(); dispatchResults.clear();
        failures.clear(); mutations.clear(); identities.clear();
        BaseVideoRecordingService.A = new BaseVideoRecordingService$a();
        BaseVideoRecordingService.B = false;
        android.os.Environment.DIRECTORY_MOVIES = "Movies";
        at9.a = new m47(); zp4.a = new ad4();
        name(blg.a, "unit"); name(v93.COROUTINE_SUSPENDED, "suspended");
        name(BaseVideoRecordingService.A, "recordingCompanion");
        name(at9.a, "mainDispatcher"); name(zp4.a, "discardedDispatcher");
    }

    public static void name(Object value, String name) { if (value != null) identities.put(value, name); }
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

    public static String state(a continuation) {
        if (continuation == null) return "null";
        StringBuilder out = new StringBuilder().append(continuation.label).append(':')
                .append(id(continuation.L$0)).append(':').append(id(continuation.L$1)).append(':')
                .append(id(continuation.this$0)).append(':').append(BaseVideoRecordingService.B)
                .append(':').append(id(BaseVideoRecordingService.A));
        for (BaseVideoRecordingService owner : owners) {
            out.append('|').append(id(owner)).append(':').append(owner.s).append(':').append(id(owner.t))
                    .append(':').append(id(owner.u)).append(':').append(owner.v).append(':').append(owner.w)
                    .append(':').append(owner.x).append(':').append(owner.availableReads)
                    .append(':').append(owner.videoDirectoryReads);
        }
        return out.toString();
    }

    public static void hit(String call) {
        if (!active) return;
        if (boundaryCalls >= 400) throw new BoundExceeded();
        boundaries.add(call); states.add(state(current));
        int index = boundaryCalls++;
        if (index == mutateAt && mutation != null) mutation.run();
        Runnable next = mutations.get(index); if (next != null) next.run();
        if (index == failAt && failure != null) raise(failure);
        Throwable planned = failures.get(index); if (planned != null) raise(planned);
    }

    public static Object result(List<Object> plan, int index, Object fallback) {
        Object value = index < plan.size() ? plan.get(index) : fallback;
        if (value instanceof g3d) raise(((g3d) value).exception);
        return value;
    }
    public static void raise(Throwable error) { VideoControl.<RuntimeException>raiseAs(error); }
    @SuppressWarnings("unchecked") private static <T extends Throwable> void raiseAs(Throwable error) throws T { throw (T) error; }

    public static final class BoundExceeded extends AssertionError {
        public BoundExceeded() { super("Controlled video boundary limit exceeded"); }
    }
    public static final class DelayCall {
        public final long milliseconds;
        public final m73 continuation;
        public final String state;
        public DelayCall(long milliseconds, m73 continuation) {
            this.milliseconds = milliseconds; this.continuation = continuation;
            this.state = VideoControl.state(current);
        }
    }
    public static final class DispatchCall {
        public final i93 dispatcher;
        public final jn6 callback;
        public final m73 continuation;
        public final String state;
        public DispatchCall(i93 dispatcher, jn6 callback, m73 continuation) {
            this.dispatcher = dispatcher; this.callback = callback; this.continuation = continuation;
            this.state = VideoControl.state(current);
        }
    }
}
