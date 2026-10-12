package android.os;
import defpackage.PluginControl;
public class Bundle extends BaseBundle {
    public Bundle() {
        PluginControl.name(this, "bundle" + PluginControl.bundles.size());
        PluginControl.bundles.add(this);
        PluginControl.hit("bundle.new:" + PluginControl.id(this));
    }
}
