package okhttp3;
import defpackage.PluginControl;
import defpackage.PluginUploadControl;
public final class MultipartBody$Part$Companion {
    public static MultipartBody$Part b(String name, RequestBody body) {
        PluginUploadControl.Part call = new PluginUploadControl.Part(name, body);
        PluginUploadControl.parts.add(call);
        PluginControl.hit("multipart.create:" + name + ":" + PluginControl.id(body));
        call.completed = true;
        return PluginUploadControl.part;
    }
}
