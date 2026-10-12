package defpackage;
import android.content.Context; import com.arlosoft.macrodroid.macro.Macro; import com.arlosoft.macrodroid.triggers.TriggerContextInfo; import java.util.*;
/** Controlled magic-text boundary; deliberately NOT the real Android implementation. */
public class sr9 {
 public static final List<String> calls=new ArrayList<>();
 public static String l(Context c,Macro m,TriggerContextInfo t,String s){calls.add("l:"+s);CoreTrace.add("expand:"+s);return s;}
 public static String n(Context c,String s,TriggerContextInfo t,Macro m,boolean flag){calls.add("n:"+flag+":"+s);return s;}
}
