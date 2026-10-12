package com.arlosoft.macrodroid.triggers.services;
import android.content.Context;
import defpackage.TouchControl;
/** Host-only service state; never grants or exercises accessibility permission. */
public class MacroDroidAccessibilityServiceJellyBean {
    public static a u = new a();
    public static boolean v;
    public static class a {
        public static void b(Context context) {
            TouchControl.hit("accessibility.unblock:"+context.testContextId);
            TouchControl.unblockCalls++; v = false;
        }
    }
}
