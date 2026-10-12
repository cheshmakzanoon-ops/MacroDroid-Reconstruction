package defpackage;
/** Host-only widget identifier construction. */
public class mh0 implements gy6 {
    public int id;
    public mh0(int id) {
        this.id = id;
        WidgetControl.name(this, "identifier" + WidgetControl.identifiers.size());
        WidgetControl.identifiers.add(this);
        WidgetControl.hit("identifier.new:" + WidgetControl.id(this) + ":" + id);
    }
}
