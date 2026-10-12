package com.arlosoft.macrodroid.intro;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import com.arlosoft.macrodroid.R;
import defpackage.ku1;
import defpackage.xpe;
import kotlin.Metadata;

/* JADX INFO: compiled from: r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f */
/* JADX INFO: loaded from: classes3.dex */
@Metadata(d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\b\u0007\u0018\u00002\u00020\u0001:\u0001\u0004B\u0007¢\u0006\u0004\b\u0002\u0010\u0003¨\u0006\u0005"}, d2 = {"Lcom/arlosoft/macrodroid/intro/a;", "Lxpe;", "<init>", "()V", "a", "app_standardRelease"}, k = 1, mv = {2, 2, 0}, xi = 48)
public final class a extends xpe {
    public static final C0023a n = new C0023a(0);

    @Override // defpackage.xpe
    public final int n() {
        return R.color.design_default_color_primary;
    }

    @Override // defpackage.xpe
    public final int o() {
        return R.color.white_very_transparent;
    }

    @Override // defpackage.xpe, androidx.fragment.app.n
    public final View onCreateView(LayoutInflater layoutInflater, ViewGroup viewGroup, Bundle bundle) {
        String string;
        String string2;
        layoutInflater.getClass();
        View viewInflate = layoutInflater.inflate(R.layout.fragment_warning_onboard, viewGroup, false);
        viewInflate.getClass();
        View viewFindViewById = viewInflate.findViewById(R.id.badDeviceText);
        viewFindViewById.getClass();
        TextView textView = (TextView) viewFindViewById;
        String string3 = getString(R.string.bad_device_brand_device_detected);
        string3.getClass();
        Bundle arguments = getArguments();
        String str = "";
        if (arguments == null || (string = arguments.getString("device_type")) == null) {
            string = "";
        }
        ku1.C(new Object[]{string}, 1, string3, textView);
        View viewFindViewById2 = viewInflate.findViewById(R.id.warningText);
        viewFindViewById2.getClass();
        TextView textView2 = (TextView) viewFindViewById2;
        String string4 = getString(R.string.bad_device_brand_short_warning);
        string4.getClass();
        Bundle arguments2 = getArguments();
        if (arguments2 != null && (string2 = arguments2.getString("web_link")) != null) {
            str = string2;
        }
        ku1.C(new Object[]{str}, 1, string4, textView2);
        return viewInflate;
    }

    @Override // defpackage.xpe
    public final int p() {
        return R.color.white_very_transparent;
    }

    /* JADX INFO: renamed from: com.arlosoft.macrodroid.intro.a$a, reason: collision with other inner class name */
    /* JADX INFO: compiled from: r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f */
    public static final class C0023a {
        public /* synthetic */ C0023a(int i) {
            this();
        }

        private C0023a() {
        }
    }
}
