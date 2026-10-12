package android.appwidget;

import defpackage.WidgetControl;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Explicit host boundary, with no connection to the Android widget service. */
public class AppWidgetManager {
    public final Map<Integer,AppWidgetProviderInfo> providers = new HashMap<Integer,AppWidgetProviderInfo>();
    public final List<Integer> reads = new ArrayList<Integer>();
    public AppWidgetProviderInfo getAppWidgetInfo(int id) {
        reads.add(id);
        WidgetControl.hit("widget.info:" + WidgetControl.id(this) + ":" + id);
        return providers.get(id);
    }
}
