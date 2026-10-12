package android.content;

import defpackage.TouchControl;
import java.util.LinkedHashMap;

/** Typed, ordered host Intent tokens, not Android marshalling or service delivery. */
public class Intent {
    public final Context context;
    public final Class<?> target;
    public final int id;
    public String action;
    public final LinkedHashMap<String,Object> extras = new LinkedHashMap<String,Object>();
    public Intent(Context context, Class<?> target) {
        this.context = context; this.target = target; this.id = TouchControl.intents.size();
        TouchControl.intents.add(this);
        TouchControl.hit("intent.new:"+id+":"+(context == null ? "null" : context.testContextId)+":"+(target == null ? "null" : target.getName()));
        context.getClass(); target.getClass();
    }
    public Intent setAction(String action) {
        TouchControl.hit("intent.action:"+id+":"+action); this.action = action; return this;
    }
    public Intent putExtra(String key, int value) {
        TouchControl.hit("intent.int:"+id+":"+key+":"+value); extras.put(key, value); return this;
    }
    public Intent putExtra(String key, float value) {
        TouchControl.hit("intent.float:"+id+":"+key+":"+Integer.toHexString(Float.floatToRawIntBits(value)));
        extras.put(key, value); return this;
    }
}
