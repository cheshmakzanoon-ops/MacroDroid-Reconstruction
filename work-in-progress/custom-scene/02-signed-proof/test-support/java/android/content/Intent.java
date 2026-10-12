package android.content;

import defpackage.TouchControl;
import java.util.LinkedHashMap;

/** Typed, ordered host Intent tokens, not Android marshalling or service delivery. */
public class Intent {
    public final Context context;
    public final Class<?> target;
    public final int id;
    public String action;
    public int flags;
    public final LinkedHashMap<String,Object> extras = new LinkedHashMap<String,Object>();
    public final LinkedHashMap<String,String> extraTypes = new LinkedHashMap<String,String>();
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
        TouchControl.hit("intent.int:"+id+":"+key+":"+value); extras.put(key, value); extraTypes.put(key,"int"); return this;
    }
    public Intent putExtra(String key, float value) {
        TouchControl.hit("intent.float:"+id+":"+key+":"+Integer.toHexString(Float.floatToRawIntBits(value)));
        extras.put(key, value); extraTypes.put(key,"float"); return this;
    }
    public Intent putExtra(String key, long value) {
        TouchControl.hit("intent.long:"+id+":"+key+":"+value); extras.put(key,value); extraTypes.put(key,"long"); return this;
    }
    public Intent putExtra(String key, boolean value) {
        TouchControl.hit("intent.boolean:"+id+":"+key+":"+value); extras.put(key,value); extraTypes.put(key,"boolean"); return this;
    }
    public Intent putExtra(String key, android.os.Parcelable value) {
        TouchControl.hit("intent.parcelable:"+id+":"+key+":"+defpackage.SceneControl.id(value));
        extras.put(key,value); extraTypes.put(key,"parcelable"); return this;
    }
    public Intent putExtra(String key, java.io.Serializable value) {
        TouchControl.hit("intent.serializable:"+id+":"+key+":"+defpackage.SceneControl.id(value));
        extras.put(key,value); extraTypes.put(key,"serializable"); return this;
    }
    public Intent addFlags(int flags) {
        TouchControl.hit("intent.flags:"+id+":"+flags); this.flags |= flags; return this;
    }
}
