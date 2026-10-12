package defpackage;

import android.graphics.Bitmap;
import android.graphics.Bitmap$CompressFormat;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import okhttp3.*;

/** Host-only icon and upload boundaries. Never transplanted into the application. */
public final class PluginUploadControl {
    public static Throwable parseFailure;
    public static MediaType mediaType;
    public static RequestBody$Companion$toRequestBody$2 requestBody;
    public static MultipartBody$Part part;
    public static int logAttempts, logCompletions;
    public static final List<String> parseInputs = new ArrayList<String>();
    public static final List<Compression> compressions = new ArrayList<Compression>();
    public static final List<Request> requests = new ArrayList<Request>();
    public static final List<Part> parts = new ArrayList<Part>();
    public static void reset() {
        parseFailure = null; logAttempts = 0; logCompletions = 0;
        parseInputs.clear(); compressions.clear(); requests.clear(); parts.clear();
        mediaType = new MediaType(); mediaType.value = "image/*";
        requestBody = new RequestBody$Companion$toRequestBody$2(); part = new MultipartBody$Part();
        MediaType.d = new MediaType$Companion(); RequestBody.Companion = new RequestBody$Companion();
        MultipartBody$Part.c = new MultipartBody$Part$Companion(); l1g.b = new agd();
    }
    public static final class Compression {
        public final Bitmap bitmap; public final Bitmap$CompressFormat format;
        public final int quality; public final OutputStream stream; public boolean completed;
        public Compression(Bitmap bitmap, Bitmap$CompressFormat format, int quality, OutputStream stream) {
            this.bitmap = bitmap; this.format = format; this.quality = quality; this.stream = stream;
        }
    }
    public static final class Request {
        public final RequestBody$Companion companion; public final MediaType mediaType;
        public final byte[] bytes; public final int offset, mask; public boolean completed;
        public Request(RequestBody$Companion companion, MediaType mediaType, byte[] bytes, int offset, int mask) {
            this.companion = companion; this.mediaType = mediaType; this.bytes = bytes; this.offset = offset; this.mask = mask;
        }
    }
    public static final class Part {
        public final String name; public final RequestBody body; public boolean completed;
        public Part(String name, RequestBody body) { this.name = name; this.body = body; }
    }
}
