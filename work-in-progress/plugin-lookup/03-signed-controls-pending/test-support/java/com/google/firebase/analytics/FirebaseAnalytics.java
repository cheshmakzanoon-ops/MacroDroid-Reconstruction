package com.google.firebase.analytics;
import android.os.Bundle;
import defpackage.PluginControl;
public class FirebaseAnalytics {
    public void a(Bundle bundle, String event) {
        PluginControl.Analytics call = new PluginControl.Analytics(this, bundle, event);
        PluginControl.analyticsAttempts.add(call);
        PluginControl.hit("analytics:" + PluginControl.id(this) + ":" + PluginControl.id(bundle) + ":" + event);
        PluginControl.analytics.add(call);
    }
}
