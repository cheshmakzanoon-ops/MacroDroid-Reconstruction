package defpackage;
public final class e6d {
    public static void r(String message) {
        PluginControl.hit("coroutine.invalid:" + message);
        WidgetControl.hit("coroutine.invalid:" + message);
        VideoControl.hit("coroutine.invalid:" + message);
        if (!(VideoControl.active ? VideoControl.invalidLabelReturns :
                WidgetControl.active ? WidgetControl.invalidLabelReturns : PluginControl.invalidLabelReturns))
            throw new IllegalStateException(message);
    }
}
