package okhttp3;
import defpackage.PluginControl;
import defpackage.PluginUploadControl;
public final class RequestBody$Companion {
    public static RequestBody$Companion$toRequestBody$2 d(RequestBody$Companion companion,
            MediaType mediaType, byte[] bytes, int offset, int mask) {
        PluginUploadControl.Request call = new PluginUploadControl.Request(companion, mediaType, bytes, offset, mask);
        PluginUploadControl.requests.add(call);
        PluginControl.hit("request.create:" + PluginControl.id(companion) + ":" + PluginControl.id(mediaType)
                + ":" + PluginControl.id(bytes) + ":" + offset + ":" + mask);
        call.completed = true;
        return PluginUploadControl.requestBody;
    }
}
