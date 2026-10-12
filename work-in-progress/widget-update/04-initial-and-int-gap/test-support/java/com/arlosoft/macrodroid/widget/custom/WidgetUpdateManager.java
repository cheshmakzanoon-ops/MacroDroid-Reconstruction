package com.arlosoft.macrodroid.widget.custom;

import android.content.Context;
import defpackage.WidgetControl;
import java.util.ArrayList;
import java.util.List;

/** Only the boundary called by the recovered method is implemented for host tests. */
public class WidgetUpdateManager {
    public final List<Context> initializationContexts = new ArrayList<Context>();
    public void a(Context context) {
        initializationContexts.add(context);
        WidgetControl.hit("widget.initialize:" + WidgetControl.id(this) + ":" + WidgetControl.id(context));
    }
}
