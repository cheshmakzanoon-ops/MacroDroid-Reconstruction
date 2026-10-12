package defpackage;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Inactive host hooks needed by the unchanged interpreter; none belongs to this method. */
public final class EngineRuntime {
    public static boolean active = false;
    private static AssertionError unexpected() { return new AssertionError("Unexpected engine boundary in numeric study"); }
    public static long now() { throw unexpected(); }
    public static long nanoTime() { throw unexpected(); }
    public static void sleep(long value) { throw unexpected(); }
    public static boolean await(CountDownLatch latch, long value, TimeUnit unit) { throw unexpected(); }
    public static void start(Thread thread) { throw unexpected(); }
}
