package android.graphics;
import defpackage.PluginControl;
import defpackage.PluginUploadControl;
import java.io.OutputStream;
import java.io.IOException;
/** Scripted compression boundary; does not encode Android image data. */
public class Bitmap {
    public byte[] bytes = new byte[]{0, 1, -1, 127};
    public boolean compressResult = true;
    public boolean compress(Bitmap$CompressFormat format, int quality, OutputStream stream) {
        PluginUploadControl.Compression call = new PluginUploadControl.Compression(this, format, quality, stream);
        PluginUploadControl.compressions.add(call);
        PluginControl.hit("bitmap.compress:" + PluginControl.id(this) + ":" + PluginControl.id(format)
                + ":" + quality + ":" + PluginControl.id(stream));
        try { stream.write(bytes); } catch (IOException failure) { PluginControl.raise(failure); }
        call.completed = true;
        return compressResult;
    }
}
