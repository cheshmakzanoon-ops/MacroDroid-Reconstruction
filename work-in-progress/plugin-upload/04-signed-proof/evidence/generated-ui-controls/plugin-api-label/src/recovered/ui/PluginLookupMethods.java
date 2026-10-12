package recovered.ui;

import android.os.BaseBundle;
import android.os.Bundle;
import com.arlosoft.macrodroid.plugins.b;
import com.arlosoft.macrodroid.plugins.b$b$a;
import com.arlosoft.macrodroid.plugins.b$b$b;
import com.arlosoft.macrodroid.plugins.b$c;
import com.arlosoft.macrodroid.plugins.c;
import com.arlosoft.macrodroid.plugins.d;
import com.arlosoft.macrodroid.plugins.g;
import com.arlosoft.macrodroid.plugins.j;
import com.arlosoft.macrodroid.plugins.data.AppBrainPackageInfo;
import defpackage.blg;
import defpackage.cne;
import defpackage.e6d;
import defpackage.hb9;
import defpackage.sz5;
import defpackage.u2f;
import defpackage.v93;
import retrofit2.HttpException;

/** Replacement body for the original plugin-lookup coroutine.
 * Dependency bodies and continuation scheduling remain the original implementations.
 */
public final class PluginLookupMethods {
    public static Object lookup(j self, Object result) {
        Object suspended = v93.COROUTINE_SUSPENDED;
        int label = self.label;
        int retryFlag = 0;
        int errorIndex = 0;
        Throwable pendingFailure = null;
        boolean resumedApi = false;

        if (label == 0) {
            u2f.P(result);
            b owner = self.this$0;
            if (owner.i) {
                cne sink = owner.j;
                ((hb9) sink).i(new g(b$c.USER_NOT_ALLOWED));
                return blg.a;
            }
            boolean known = owner.g.contains(self.$packageName);
            owner = self.this$0;
            if (known) {
                cne sink = owner.j;
                ((hb9) sink).i(new c(self.$packageName));
                return blg.a;
            }
            if (owner.h >= 5) {
                cne sink = owner.j;
                ((hb9) sink).i(b$b$b.a);
                return blg.a;
            }
            String packageName = self.$packageName;
            self.label = 1;
            result = owner.a(packageName, self);
            if (result == suspended) return suspended;
        } else if (label == 1) {
            u2f.P(result);
        } else if (label == 2) {
            errorIndex = self.I$1;
            retryFlag = self.I$0;
            try {
                u2f.P(result);
            } catch (Exception resumeFailure) {
                pendingFailure = resumeFailure;
            }
            resumedApi = true;
        } else {
            e6d.r("call to 'resume' before 'invoke' with coroutine");
            return null;
        }

        if (!resumedApi) {
            Boolean permitted = (Boolean) result;
            if (!permitted.booleanValue()) return blg.a;
            b owner = self.this$0;
            owner.h = owner.h + 1;
        }

        for (;;) {
            if (!resumedApi) {
                try {
                    sz5 ignored = sz5.a;
                    Bundle data = new Bundle();
                    ((BaseBundle) data).putInt("key_index", 0);
                    sz5.b.a(data, "app_brain_api_call_made");
                    b owner = self.this$0;
                    b.k.getClass();
                    String key = (String) b.l.get(0);
                    String packageName = self.$packageName;
                    self.I$0 = 0;
                    self.I$1 = 0;
                    self.label = 1;
                    result = owner.c.getApp(key, packageName, self);
                } catch (Exception apiFailure) {
                    pendingFailure = apiFailure;
                }
                if (pendingFailure == null && result == suspended) return suspended;
                errorIndex = 0;
                retryFlag = 0;
            } else {
                resumedApi = false;
            }

            if (pendingFailure == null) {
                try {
                    AppBrainPackageInfo info = (AppBrainPackageInfo) result;
                    cne sink = self.this$0.j;
                    ((hb9) sink).i(new d(info));
                    self.this$0.h = 0;
                } catch (Exception publicationFailure) {
                    pendingFailure = publicationFailure;
                }
                if (pendingFailure == null) retryFlag = 0;
            }

            if (pendingFailure != null) {
                Throwable failure = pendingFailure;
                pendingFailure = null;
                boolean http = failure instanceof HttpException;
                boolean badRequest = http && ((HttpException) failure).a() == 400;
                boolean rateLimited = http && ((HttpException) failure).a() == 429;
                if (badRequest) {
                    self.this$0.g.add(self.$packageName);
                    cne sink = self.this$0.j;
                    ((hb9) sink).i(new c(self.$packageName));
                } else if (rateLimited) {
                    errorIndex = errorIndex + 1;
                    b.k.getClass();
                    if (errorIndex < b.l.size()) {
                        retryFlag = 1;
                    } else {
                        sz5.b.a(null, "app_brain_calls_exceeded");
                    }
                } else {
                    cne sink = self.this$0.j;
                    ((hb9) sink).i(b$b$a.a);
                }
            }
            // Preserve the uploaded loop's repeated index-0 request and restored retry flag.
            if (retryFlag == 0) return blg.a;
        }
    }
}
