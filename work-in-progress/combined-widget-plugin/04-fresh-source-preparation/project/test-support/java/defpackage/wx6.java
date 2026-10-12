package defpackage;
import android.content.Context;
import android.appwidget.AppWidgetManager;
/** Host-only manager creation and field identity. */
public class wx6 {
    public AppWidgetManager b;
    public Context context;
    public wx6(Context context) {
        this.context = context; this.b = WidgetControl.backend;
        WidgetControl.name(this, "manager" + WidgetControl.managers.size());
        WidgetControl.managers.add(this);
        WidgetControl.hit("manager.new:" + WidgetControl.id(this) + ":" + WidgetControl.id(context));
    }
}
