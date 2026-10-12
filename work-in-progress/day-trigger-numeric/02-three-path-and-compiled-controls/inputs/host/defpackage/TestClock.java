package defpackage;

import java.util.Calendar;

/** Inactive host hook; a calendar call in this numeric study is an error. */
public final class TestClock {
    public static boolean enabled = false;
    public static Calendar calendar() { throw new AssertionError("Unexpected calendar boundary in numeric study"); }
}
