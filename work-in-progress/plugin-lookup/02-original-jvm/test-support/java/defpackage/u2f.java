package defpackage;
public final class u2f {
    public static void P(Object result) {
        PluginControl.hit("coroutine.result:" + PluginControl.id(result));
        if (result instanceof g3d) PluginControl.raise(((g3d) result).exception);
    }
}
