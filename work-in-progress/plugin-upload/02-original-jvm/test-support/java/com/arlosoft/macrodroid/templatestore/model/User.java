package com.arlosoft.macrodroid.templatestore.model;
import defpackage.PluginControl;
public final class User {
    public int userId, reads;
    public int getUserId() {
        reads++;
        PluginControl.hit("user.id:" + PluginControl.id(this));
        return userId;
    }
}
