package defpackage;
public class hb9 {
    public void i(Object value) {
        PluginControl.Publication call = new PluginControl.Publication(this, value);
        PluginControl.publicationAttempts.add(call);
        PluginControl.hit("publish:" + PluginControl.id(this) + ":" + PluginControl.id(value));
        PluginControl.publications.add(call);
    }
}
