package defpackage;
import java.util.*;
/** Host-only ordered boundary trace. Never packaged. */
public final class CoreTrace {
 public static final List<String> calls = new ArrayList<String>();
 public static void add(String value) { calls.add(value); EngineRuntime.onCall(value); }
 public static void reset() { calls.clear(); }
}
