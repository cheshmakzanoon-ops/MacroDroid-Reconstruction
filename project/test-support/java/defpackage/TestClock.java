package defpackage;
import java.util.*;
/** Deterministic host boundary, installed only by the test agent/interpreter. */
public final class TestClock {
 public static boolean enabled;public static boolean agentInstalled;public static long epochMillis;
 public static Calendar calendar(){if(!enabled)return Calendar.getInstance();Calendar c=Calendar.getInstance(TimeZone.getDefault(),Locale.ROOT);c.setTimeInMillis(epochMillis);return c;}
}
