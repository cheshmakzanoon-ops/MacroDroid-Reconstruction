package defpackage;
import android.content.Context;
/** Host-only first suspending call; controlled results never run Android work. */
public final class rjb {
    public static Object M(Context context, gy6 identifier, jn6 factory, o73 continuation) {
        WidgetControl.firstCalls.add(new WidgetControl.Call(null, context, identifier, factory, continuation));
        int index = WidgetControl.firstReads++;
        WidgetControl.hit("widget.first:" + WidgetControl.id(context) + ":" + WidgetControl.id(identifier)
            + ":" + WidgetControl.id(factory) + ":" + WidgetControl.id(continuation));
        return WidgetControl.result(WidgetControl.firstResults, index, "first-ok");
    }
}
