package defpackage;
import android.content.Context;
/** Host-only second suspending call. */
public class rx6 {
    public Object d(Context context, gy6 identifier, o73 continuation) {
        WidgetControl.secondCalls.add(new WidgetControl.Call(this, context, identifier, null, continuation));
        int index = WidgetControl.secondReads++;
        WidgetControl.hit("widget.second:" + WidgetControl.id(this) + ":" + WidgetControl.id(context)
            + ":" + WidgetControl.id(identifier) + ":" + WidgetControl.id(continuation));
        return WidgetControl.result(WidgetControl.secondResults, index, "second-ok");
    }
}
