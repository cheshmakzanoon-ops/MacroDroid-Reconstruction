package defpackage;
/** Host-only renderer construction. */
public class hn9 extends rx6 {
    public hn9() {
        WidgetControl.name(this, "renderer" + WidgetControl.renderers.size());
        WidgetControl.renderers.add(this);
        WidgetControl.hit("renderer.new:" + WidgetControl.id(this));
    }
}
