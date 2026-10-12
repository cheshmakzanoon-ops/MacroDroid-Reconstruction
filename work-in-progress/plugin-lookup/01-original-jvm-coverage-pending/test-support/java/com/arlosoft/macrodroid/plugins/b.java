package com.arlosoft.macrodroid.plugins;
import com.arlosoft.macrodroid.plugins.api.AppBrainApi;
import defpackage.PluginControl;
import defpackage.cne;
import defpackage.o73;
import java.util.ArrayList;
import java.util.List;
public final class b {
    public static b$a k = new b$a();
    public static List l;
    public AppBrainApi c;
    public ArrayList g = new ArrayList();
    public int h;
    public boolean i;
    public cne j = new cne();
    public Object[] precheckResults = new Object[]{Boolean.TRUE};
    public int precheckReads;
    public String lastPackage;
    public o73 lastContinuation;
    public Object a(String packageName, o73 continuation) {
        lastPackage = packageName; lastContinuation = continuation;
        int index = precheckReads++;
        PluginControl.hit("precheck:" + PluginControl.id(this) + ":" + PluginControl.id(packageName) + ":" + PluginControl.id(continuation));
        Object value = index < precheckResults.length ? precheckResults[index] : Boolean.TRUE;
        if (value instanceof Throwable) PluginControl.raise((Throwable) value);
        return value;
    }
}
