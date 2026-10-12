package recovered.ui;

import android.graphics.Bitmap;
import android.graphics.Bitmap$CompressFormat;
import android.graphics.drawable.Drawable;
import com.arlosoft.macrodroid.plugins.b;
import com.arlosoft.macrodroid.plugins.b$c;
import com.arlosoft.macrodroid.plugins.f;
import com.arlosoft.macrodroid.plugins.g;
import com.arlosoft.macrodroid.plugins.k;
import com.arlosoft.macrodroid.plugins.api.PluginListApi;
import com.arlosoft.macrodroid.plugins.api.UploadPluginBody;
import defpackage.agd;
import defpackage.blg;
import defpackage.cne;
import defpackage.e6d;
import defpackage.hb9;
import defpackage.l1g;
import defpackage.nx4;
import defpackage.u2f;
import defpackage.v93;
import java.io.ByteArrayOutputStream;
import okhttp3.MediaType;
import okhttp3.MediaType$Companion;
import okhttp3.MultipartBody$Part;
import okhttp3.MultipartBody$Part$Companion;
import okhttp3.RequestBody;
import okhttp3.RequestBody$Companion;
import okhttp3.RequestBody$Companion$toRequestBody$2;
import retrofit2.HttpException;

/** Selected body of the original plugin-upload coroutine; dependencies stay original. */
public final class PluginUploadMethods {
    public static Object upload(k self, Object result) {
        Object suspended = v93.COROUTINE_SUSPENDED;
        int label = self.label;

        if (label == 2) {
            UploadPluginBody ignoredBody = (UploadPluginBody) self.L$1;
            String ignoredIcon = (String) self.L$0;
        } else if (label == 1) {
            MultipartBody$Part ignoredPart = (MultipartBody$Part) self.L$4;
            RequestBody ignoredRequest = (RequestBody) self.L$3;
            byte[] ignoredBytes = (byte[]) self.L$2;
            ByteArrayOutputStream ignoredStream = (ByteArrayOutputStream) self.L$1;
            Bitmap ignoredBitmap = (Bitmap) self.L$0;
        } else if (label == 0) {
            u2f.P(result);
        } else {
            e6d.r("call to 'resume' before 'invoke' with coroutine");
            return null;
        }

        try {
            if (label == 2) {
                u2f.P(result);
            } else {
                String uploadedIcon;
                if (label == 1) {
                    u2f.P(result);
                    uploadedIcon = (String) result;
                } else {
                    Drawable drawable = self.$drawable;
                    if (drawable != null) {
                        Bitmap bitmap = nx4.a(drawable);
                        ByteArrayOutputStream stream = new ByteArrayOutputStream();
                        bitmap.compress(Bitmap$CompressFormat.PNG, 100, stream);
                        byte[] bytes = stream.toByteArray();
                        RequestBody$Companion requestCompanion = RequestBody.Companion;
                        MediaType$Companion mediaCompanion = MediaType.d;
                        mediaCompanion.getClass();
                        MediaType mediaType;
                        try {
                            mediaType = MediaType$Companion.a("image/*");
                        } catch (NullPointerException invalidType) {
                            mediaType = null;
                        }
                        bytes.getClass();
                        RequestBody$Companion$toRequestBody$2 request =
                                RequestBody$Companion.d(requestCompanion, mediaType, bytes, 0, 12);
                        MultipartBody$Part$Companion partCompanion = MultipartBody$Part.c;
                        partCompanion.getClass();
                        MultipartBody$Part part = MultipartBody$Part$Companion.b("icon", request);
                        PluginListApi api = self.this$0.b;
                        self.L$0 = null;
                        self.L$1 = null;
                        self.L$2 = null;
                        self.L$3 = null;
                        self.L$4 = null;
                        self.label = 1;
                        Object iconResult = api.uploadNonPlayStoreAppIcon(part, self);
                        if (iconResult == suspended) return suspended;
                        uploadedIcon = (String) iconResult;
                    } else {
                        uploadedIcon = null;
                    }
                }

                UploadPluginBody body = new UploadPluginBody(
                        self.this$0.d.a().getUserId(),
                        self.$name,
                        self.$developerName,
                        self.$shortDescription,
                        self.$packageName,
                        self.$downloadLink,
                        uploadedIcon == null ? self.$iconUrl : uploadedIcon,
                        self.$website,
                        "en");
                PluginListApi api = self.this$0.b;
                String hash = self.$hash;
                self.L$0 = null;
                self.L$1 = null;
                self.L$2 = null;
                self.L$3 = null;
                self.L$4 = null;
                self.label = 2;
                Object uploadResult = api.uploadPlayStorePlugin(hash, body, self);
                if (uploadResult == suspended) return suspended;
            }

            cne sink = self.this$0.j;
            ((hb9) sink).i(new f(self.$name));
        } catch (Exception failure) {
            boolean alreadyExists = failure instanceof HttpException
                    && ((HttpException) failure).a() == 409;
            boolean userNotAllowed = failure instanceof HttpException
                    && ((HttpException) failure).a() == 403;
            b owner = self.this$0;
            if (alreadyExists) {
                cne sink = owner.j;
                ((hb9) sink).i(new g(b$c.ALREADY_EXISTS));
            } else if (userNotAllowed) {
                owner.i = true;
                cne sink = owner.j;
                ((hb9) sink).i(new g(b$c.USER_NOT_ALLOWED));
            } else {
                cne sink = owner.j;
                ((hb9) sink).i(new g(b$c.CONNECTION_ERROR));
                l1g.b.getClass();
                agd.j();
            }
        }
        return blg.a;
    }
}
