package defpackage;
import com.arlosoft.macrodroid.templatestore.model.User;
public final class jsg {
    public User user;
    public int reads;
    public User a() {
        reads++;
        PluginControl.hit("user.current:" + PluginControl.id(this));
        return user;
    }
}
