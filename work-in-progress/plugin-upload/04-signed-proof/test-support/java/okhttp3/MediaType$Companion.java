package okhttp3;
import defpackage.PluginControl;
import defpackage.PluginUploadControl;
public final class MediaType$Companion {
    public static MediaType a(String value) {
        PluginUploadControl.parseInputs.add(value);
        PluginControl.hit("media.parse:" + value);
        if (PluginUploadControl.parseFailure != null) PluginControl.raise(PluginUploadControl.parseFailure);
        return PluginUploadControl.mediaType;
    }
}
