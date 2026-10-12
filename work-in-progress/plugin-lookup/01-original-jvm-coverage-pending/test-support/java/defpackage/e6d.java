package defpackage;
public final class e6d {
    public static void r(String message) {
        PluginControl.hit("coroutine.invalid:" + message);
        if (!PluginControl.invalidLabelReturns) throw new IllegalStateException(message);
    }
}
