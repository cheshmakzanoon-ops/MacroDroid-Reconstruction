package android.os;
import defpackage.PluginControl;
import java.util.LinkedHashMap;
public class BaseBundle {
    public final LinkedHashMap<String,Integer> values = new LinkedHashMap<String,Integer>();
    public void putInt(String key, int value) {
        PluginControl.hit("bundle.putInt:" + PluginControl.id(this) + ":" + key + ":" + value);
        values.put(key, value);
    }
}
