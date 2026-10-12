package com.arlosoft.macrodroid.intro;

import agency.tango.materialintroscreen.MaterialIntroActivity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.View;
import android.widget.ImageButton;
import com.arlosoft.macrodroid.R;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.homescreen.NewHomeScreenActivity;
import com.arlosoft.macrodroid.settings.c;
import com.google.android.gms.ads.internal.client.zzeu;
import defpackage.c71;
import defpackage.dvd;
import defpackage.e3h;
import defpackage.f10;
import defpackage.f13;
import defpackage.fd6;
import defpackage.g0b;
import defpackage.g9f;
import defpackage.i0b;
import defpackage.ibg;
import defpackage.jc;
import defpackage.n2c;
import defpackage.n3h;
import defpackage.ok5;
import defpackage.oke;
import defpackage.pk5;
import defpackage.pm6;
import defpackage.q68;
import defpackage.q8;
import defpackage.r68;
import defpackage.rif;
import defpackage.rt8;
import defpackage.s35;
import defpackage.sud;
import defpackage.sz5;
import defpackage.t6;
import defpackage.vf3;
import defpackage.w63;
import defpackage.x47;
import defpackage.xdh;
import java.util.Locale;
import java.util.WeakHashMap;
import java.util.concurrent.TimeUnit;
import kotlin.Metadata;

/* JADX INFO: compiled from: r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f */
/* JADX INFO: loaded from: classes3.dex */
@Metadata(d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\b\u0007\u0018\u00002\u00020\u0001:\u0001\u0004B\u0007¢\u0006\u0004\b\u0002\u0010\u0003¨\u0006\u0005"}, d2 = {"Lcom/arlosoft/macrodroid/intro/IntroActivity;", "Lagency/tango/materialintroscreen/MaterialIntroActivity;", "<init>", "()V", "a", "app_standardRelease"}, k = 1, mv = {2, 2, 0}, xi = 48)
public final class IntroActivity extends MaterialIntroActivity {
    public static final /* synthetic */ int C = 0;
    public boolean B;

    static {
        new a(0);
    }

    @Override // agency.tango.materialintroscreen.MaterialIntroActivity
    public final void O0() {
        if (Build.VERSION.SDK_INT < 33 || w63.checkSelfPermission(this, "android.permission.POST_NOTIFICATIONS") == 0) {
            P0();
        } else {
            pk5.f.a(this);
            ok5.b(new String[]{"android.permission.POST_NOTIFICATIONS"}, new r68(this, 1));
        }
    }

    public final void P0() {
        Locale[] localeArr = c.a;
        SharedPreferences.Editor editorEdit = PreferenceManager.getDefaultSharedPreferences(this).edit();
        editorEdit.putBoolean("preferences:shown_intro", true);
        editorEdit.apply();
        startActivity(new Intent(this, (Class<?>) NewHomeScreenActivity.class));
        sz5.b.a(null, "funnel_onboarding_complete");
        finish();
    }

    public final void Q0(boolean z) {
        Locale[] localeArr = c.a;
        if (PreferenceManager.getDefaultSharedPreferences(this).getInt("preferences:last_run_version", 0) == 0 && !PreferenceManager.getDefaultSharedPreferences(this).getBoolean("preferences:shown_intro", false)) {
            View viewFindViewById = findViewById(R.id.coordinator_layout_slide);
            viewFindViewById.getClass();
            viewFindViewById.setVisibility(0);
            return;
        }
        Intent intent = new Intent(this, (Class<?>) NewHomeScreenActivity.class);
        if (this.B) {
            intent.addFlags(32768);
        }
        startActivity(intent);
        finish();
        if (z) {
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        } else {
            overridePendingTransition(0, 0);
        }
    }

    @Override // agency.tango.materialintroscreen.MaterialIntroActivity, androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    public final void onCreate(Bundle bundle) {
        String str;
        int i = 0;
        int i2 = 2;
        s35.b(this, new rif(0, 0, 2, new oke(18)), 2);
        super.onCreate(bundle);
        View viewFindViewById = findViewById(R.id.navigation_view);
        x47 x47Var = new x47(19);
        WeakHashMap weakHashMap = n3h.a;
        e3h.c(viewFindViewById, x47Var);
        viewFindViewById.requestApplyInsets();
        if (!getResources().getBoolean(R.bool.is_tablet)) {
            try {
                setRequestedOrientation(1);
            } catch (IllegalStateException unused) {
            }
        }
        this.B = getIntent().getBooleanExtra("force_clear_task", false);
        ((ImageButton) findViewById(R.id.button_next)).setContentDescription(getString(R.string.action_control_media_next));
        findViewById(R.id.coordinator_layout_slide).setBackgroundColor(-1);
        View viewFindViewById2 = findViewById(R.id.coordinator_layout_slide);
        viewFindViewById2.getClass();
        viewFindViewById2.setVisibility(8);
        M0(new xdh());
        M0(new ibg());
        M0(new jc());
        M0(new f13());
        String str2 = Build.MANUFACTURER;
        String str3 = "xiaomi";
        if (g9f.l1(str2, "xiaomi", true)) {
            str = "Xiaomi";
        } else {
            str3 = "huawei";
            if (g9f.l1(str2, "huawei", true)) {
                str = "Huawei";
            } else {
                str3 = null;
                str = null;
            }
        }
        if (str != null && str3 != null) {
            com.arlosoft.macrodroid.intro.a.n.getClass();
            Bundle bundle2 = new Bundle();
            bundle2.putString("device_type", str);
            bundle2.putString("web_link", str3);
            com.arlosoft.macrodroid.intro.a aVar = new com.arlosoft.macrodroid.intro.a();
            aVar.setArguments(bundle2);
            M0(aVar);
        }
        sz5.a.getClass();
        sz5.g("funnel_onboarding_start");
        this.m.setVisibility(8);
        this.n.setVisibility(0);
        this.n.setOnClickListener(new t6(this, 7));
        this.n.setOnClickListener(new q8(this, 28));
        try {
            MacroDroidApplication.E.getClass();
            MacroDroidApplication macroDroidApplication = MacroDroidApplication.F;
            macroDroidApplication.getClass();
            n2c n2cVarA = macroDroidApplication.j().a();
            n2cVarA.getClass();
            if (!(n2cVarA instanceof n2c.c)) {
                try {
                    zzeu.d().e(getApplicationContext(), new q68(i));
                } catch (Exception e) {
                    sz5.e(e);
                }
            }
        } catch (Exception unused2) {
        }
        long jCurrentTimeMillis = System.currentTimeMillis();
        MacroDroidApplication.E.getClass();
        MacroDroidApplication macroDroidApplication2 = MacroDroidApplication.F;
        macroDroidApplication2.getClass();
        c71 c71Var = macroDroidApplication2.z;
        c71Var.getClass();
        sud sudVar = dvd.a;
        pm6.N(TimeUnit.SECONDS, "timeUnit is null");
        pm6.N(sudVar, "scheduler is null");
        new g0b(new i0b(c71Var, 5L, sudVar)).e(dvd.b).a(f10.a()).c(new rt8(new fd6(new vf3(this, jCurrentTimeMillis, i2), 4), new fd6(new r68(this, i), 5)));
    }

    /* JADX INFO: compiled from: r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f */
    public static final class a {
        public /* synthetic */ a(int i) {
            this();
        }

        private a() {
        }
    }
}
