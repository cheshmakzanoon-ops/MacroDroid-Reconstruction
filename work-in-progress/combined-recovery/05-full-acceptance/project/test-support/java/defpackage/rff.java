package defpackage;
public abstract class rff extends o73 {
    public int widgetArity;
    public m73 widgetCompletion;
    public rff() {}
    public rff(int arity, m73 completion) {
        widgetArity = arity; widgetCompletion = completion;
        WidgetControl.name(this, "factory" + WidgetControl.factories.size());
        WidgetControl.factories.add(this);
        WidgetControl.hit("factory.new:" + WidgetControl.id(this) + ":" + arity + ":" + WidgetControl.id(completion));
    }
}
