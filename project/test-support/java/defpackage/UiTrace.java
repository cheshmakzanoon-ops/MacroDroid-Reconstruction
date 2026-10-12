package defpackage;
import java.util.*;
/** Controlled host observations, not Android services. */
public final class UiTrace {
    public static final List<String> calls = new ArrayList<String>();
    public static String resource = "[Localized stop]";
    public static Throwable resourceFailure;
    public static void add(String call) { calls.add(call); }
    public static void reset() { calls.clear(); resource = "[Localized stop]"; resourceFailure = null; }
    public static void raise(Throwable failure) { if (failure instanceof Error) throw (Error)failure; if (failure instanceof RuntimeException) throw (RuntimeException)failure; }
}
