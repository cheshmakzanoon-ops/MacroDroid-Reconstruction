package defpackage;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
public class nx4 {
    public static Bitmap a(Drawable drawable) {
        PluginControl.hit("drawable.bitmap:" + PluginControl.id(drawable));
        return drawable.bitmap;
    }
}
