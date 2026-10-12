.class public final Lcom/arlosoft/macrodroid/intro/IntroActivity;
.super Lagency/tango/materialintroscreen/MaterialIntroActivity;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/arlosoft/macrodroid/intro/IntroActivity$a;
    }
.end annotation

.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000\u000c\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0004\u0008\u0007\u0018\u00002\u00020\u0001:\u0001\u0004B\u0007\u00a2\u0006\u0004\u0008\u0002\u0010\u0003\u00a8\u0006\u0005"
    }
    d2 = {
        "Lcom/arlosoft/macrodroid/intro/IntroActivity;",
        "Lagency/tango/materialintroscreen/MaterialIntroActivity;",
        "<init>",
        "()V",
        "a",
        "app_standardRelease"
    }
    k = 0x1
    mv = {
        0x2,
        0x2,
        0x0
    }
    xi = 0x30
.end annotation


# static fields
.field public static final synthetic C:I


# instance fields
.field public B:Z


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .line 1
    new-instance v0, Lcom/arlosoft/macrodroid/intro/IntroActivity$a;

    .line 3
    const/4 v1, 0x0

    .line 4
    const/4 v2, 0x3

    invoke-direct {v0, v1}, Lcom/arlosoft/macrodroid/intro/IntroActivity$a;-><init>(I)V

    .line 7
    const/4 v2, 0x4

    return-void
.end method

.method public constructor <init>()V
    .locals 1

    .line 1
    invoke-direct {p0}, Lagency/tango/materialintroscreen/MaterialIntroActivity;-><init>()V

    .line 4
    return-void
.end method


# virtual methods
.method public final O0()V
    .locals 4

    .line 1
    const-string v3, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 3
    const/4 v3, 0x0

    const/16 v1, 0x21

    .line 5
    if-lt v0, v1, :cond_29

    .line 7
    const-string v0, "I.sSSoAiI.PpOonTrIrisesOOaFNNC_mTiTdd"

    const-string v0, "android.permission.POST_NOTIFICATIONS"

    .line 9
    invoke-static {p0, v0}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 12
    move-result v1

    .line 13
    const/4 v3, 0x7

    if-nez v1, :cond_15

    .line 15
    goto :goto_29

    .line 16
    :cond_15
    sget-object v1, Lpk5;->f:Lok5;

    .line 18
    const/4 v3, 0x4

    invoke-virtual {v1, p0}, Lok5;->a(Landroid/app/Activity;)V

    .line 21
    filled-new-array {v0}, [Ljava/lang/String;

    .line 24
    move-result-object v0

    .line 25
    new-instance v1, Lr68;

    .line 27
    const/4 v2, 0x1

    .line 28
    invoke-direct {v1, p0, v2}, Lr68;-><init>(Lcom/arlosoft/macrodroid/intro/IntroActivity;I)V

    .line 31
    invoke-static {v0, v1}, Lok5;->b([Ljava/lang/String;Lwm6;)V

    .line 34
    return-void

    .line 35
    :cond_29
    :goto_29
    const/4 v3, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/intro/IntroActivity;->P0()V

    .line 38
    return-void
.end method

.method public final P0()V
    .locals 4

    .line 1
    const/4 v3, 0x1

    sget-object v0, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 3
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 6
    move-result-object v0

    .line 7
    const/4 v3, 0x3

    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    .line 10
    move-result-object v0

    .line 11
    const/4 v3, 0x4

    const-string v1, "preferences:shown_intro"

    .line 13
    const/4 v2, 0x1

    .line 14
    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    .line 17
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V

    .line 20
    const/4 v3, 0x5

    new-instance v0, Landroid/content/Intent;

    .line 22
    const-class v1, Lcom/arlosoft/macrodroid/homescreen/NewHomeScreenActivity;

    const-class v1, Lcom/arlosoft/macrodroid/homescreen/NewHomeScreenActivity;

    .line 24
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 27
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 30
    const/4 v3, 0x2

    sget-object v0, Lsz5;->b:Lcom/google/firebase/analytics/FirebaseAnalytics;

    .line 32
    const/4 v3, 0x7

    const-string v1, "funnel_onboarding_complete"

    .line 34
    const/4 v3, 0x3

    const/4 v2, 0x0

    .line 35
    const/4 v3, 0x4

    invoke-virtual {v0, v2, v1}, Lcom/google/firebase/analytics/FirebaseAnalytics;->a(Landroid/os/Bundle;Ljava/lang/String;)V

    .line 38
    const/4 v3, 0x0

    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 41
    return-void
.end method

.method public final Q0(Z)V
    .locals 4

    .line 1
    const/4 v3, 0x1

    sget-object v0, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 3
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 6
    move-result-object v0

    .line 7
    const-string v1, "_tpmrur_oaerencs:nrvseefinle"

    const-string v1, "preferences:last_run_version"

    .line 9
    const/4 v2, 0x0

    .line 10
    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    .line 13
    move-result v0

    .line 14
    const/4 v3, 0x5

    if-nez v0, :cond_33

    .line 16
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 19
    move-result-object v0

    .line 20
    const-string/jumbo v1, "w:n_ornrntofeeishesocer"

    const-string v1, "preferences:shown_intro"

    .line 22
    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 25
    move-result v0

    .line 26
    if-eqz v0, :cond_24

    .line 28
    const/4 v3, 0x0

    goto :goto_33

    .line 29
    :cond_24
    const p1, 0x7f0a0406

    .line 32
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 35
    move-result-object p0

    .line 36
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 39
    invoke-virtual {p0, v2}, Landroid/view/View;->setVisibility(I)V

    .line 42
    const/4 v3, 0x4

    return-void

    .line 43
    :cond_33
    :goto_33
    new-instance v0, Landroid/content/Intent;

    .line 45
    const-class v1, Lcom/arlosoft/macrodroid/homescreen/NewHomeScreenActivity;

    .line 47
    const/4 v3, 0x3

    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 50
    iget-boolean v1, p0, Lcom/arlosoft/macrodroid/intro/IntroActivity;->B:Z

    .line 52
    if-eqz v1, :cond_45

    .line 54
    const v1, 0x8000

    .line 57
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 60
    :cond_45
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 63
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 66
    if-eqz p1, :cond_57

    .line 68
    const/high16 p1, 0x10a0000

    .line 70
    const v0, 0x10a0001

    .line 73
    invoke-virtual {p0, p1, v0}, Landroid/app/Activity;->overridePendingTransition(II)V

    .line 76
    const/4 v3, 0x0

    return-void

    .line 77
    :cond_57
    invoke-virtual {p0, v2, v2}, Landroid/app/Activity;->overridePendingTransition(II)V

    .line 80
    const/4 v3, 0x5

    return-void
.end method

.method public final onCreate(Landroid/os/Bundle;)V
    .locals 9

    .line 1
    const/4 v8, 0x4

    new-instance v0, Lrif;

    .line 3
    new-instance v1, Loke;

    .line 5
    const/4 v8, 0x4

    const/16 v2, 0x12

    .line 7
    invoke-direct {v1, v2}, Loke;-><init>(I)V

    .line 10
    const/4 v2, 0x0

    .line 11
    const/4 v3, 0x2

    move v8, v3

    .line 12
    invoke-direct {v0, v2, v2, v3, v1}, Lrif;-><init>(IIILwm6;)V

    .line 15
    invoke-static {p0, v0, v3}, Ls35;->b(Landroidx/activity/ComponentActivity;Lrif;I)V

    .line 18
    invoke-super {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->onCreate(Landroid/os/Bundle;)V

    .line 21
    const p1, 0x7f0a0c42

    .line 24
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 27
    move-result-object p1

    .line 28
    new-instance v0, Lx47;

    .line 30
    const/16 v1, 0x13

    .line 32
    invoke-direct {v0, v1}, Lx47;-><init>(I)V

    .line 35
    sget-object v1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 37
    invoke-static {p1, v0}, Le3h;->c(Landroid/view/View;Li3b;)V

    .line 40
    invoke-virtual {p1}, Landroid/view/View;->requestApplyInsets()V

    .line 43
    invoke-virtual {p0}, Landroidx/appcompat/app/AppCompatActivity;->getResources()Landroid/content/res/Resources;

    .line 46
    move-result-object p1

    .line 47
    const/4 v8, 0x7

    const v0, 0x7f050012

    .line 50
    invoke-virtual {p1, v0}, Landroid/content/res/Resources;->getBoolean(I)Z

    .line 53
    move-result p1

    .line 54
    const/4 v8, 0x1

    const/4 v0, 0x1

    .line 55
    if-nez p1, :cond_41

    .line 57
    :try_start_3d
    const/4 v8, 0x1

    invoke-virtual {p0, v0}, Landroid/app/Activity;->setRequestedOrientation(I)V
    :try_end_41
    .catch Ljava/lang/IllegalStateException; {:try_start_3d .. :try_end_41} :catch_41

    .line 60
    :catch_41
    :cond_41
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 63
    move-result-object p1

    .line 64
    const/4 v8, 0x3

    const-string v1, "force_clear_task"

    .line 66
    const/4 v8, 0x7

    invoke-virtual {p1, v1, v2}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 69
    move-result p1

    .line 70
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/intro/IntroActivity;->B:Z

    .line 72
    const p1, 0x7f0a0219

    .line 75
    const/4 v8, 0x7

    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 78
    move-result-object p1

    .line 79
    check-cast p1, Landroid/widget/ImageButton;

    .line 81
    const p1, 0x7f0a022d

    .line 84
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 87
    move-result-object p1

    .line 88
    check-cast p1, Landroid/widget/ImageButton;

    .line 90
    const/4 v8, 0x6

    const v1, 0x7f14011c

    .line 93
    invoke-virtual {p0, v1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 96
    move-result-object v1

    .line 97
    invoke-virtual {p1, v1}, Landroid/view/View;->setContentDescription(Ljava/lang/CharSequence;)V

    .line 100
    const p1, 0x7f0a0406

    .line 103
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 106
    move-result-object v1

    .line 107
    const/4 v4, -0x1

    .line 108
    invoke-virtual {v1, v4}, Landroid/view/View;->setBackgroundColor(I)V

    .line 111
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 114
    move-result-object p1

    .line 115
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 118
    const/16 v1, 0x8

    .line 120
    invoke-virtual {p1, v1}, Landroid/view/View;->setVisibility(I)V

    .line 123
    new-instance p1, Lxdh;

    .line 125
    invoke-direct {p1}, Lxdh;-><init>()V

    .line 128
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->M0(Lxpe;)V

    .line 131
    new-instance p1, Libg;

    .line 133
    invoke-direct {p1}, Libg;-><init>()V

    .line 136
    const/4 v8, 0x6

    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->M0(Lxpe;)V

    .line 139
    new-instance p1, Ljc;

    .line 141
    invoke-direct {p1}, Ljc;-><init>()V

    .line 144
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->M0(Lxpe;)V

    .line 147
    new-instance p1, Lf13;

    .line 149
    const/4 v8, 0x5

    invoke-direct {p1}, Lf13;-><init>()V

    .line 152
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->M0(Lxpe;)V

    .line 155
    const/4 v8, 0x1

    sget-object p1, Landroid/os/Build;->MANUFACTURER:Ljava/lang/String;

    .line 157
    const-string v4, "iaxmob"

    const-string/jumbo v4, "xiaomi"

    .line 159
    invoke-static {p1, v4, v0}, Lg9f;->l1(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 162
    move-result v5

    .line 163
    if-eqz v5, :cond_b8

    .line 165
    const/4 v8, 0x7

    const-string p1, "Xiaomi"

    .line 167
    goto :goto_c7

    .line 168
    :cond_b8
    const/4 v8, 0x4

    const-string v4, "huawei"

    .line 170
    invoke-static {p1, v4, v0}, Lg9f;->l1(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 173
    move-result p1

    .line 174
    if-eqz p1, :cond_c4

    .line 176
    const-string p1, "Huawei"

    .line 178
    goto :goto_c7

    .line 179
    :cond_c4
    const/4 v8, 0x4

    const/4 v4, 0x0

    .line 180
    move-object p1, v4

    .line 181
    :goto_c7
    const/4 v8, 0x5

    if-eqz p1, :cond_ec

    .line 183
    if-eqz v4, :cond_ec

    .line 185
    sget-object v0, Lcom/arlosoft/macrodroid/intro/a;->n:Lcom/arlosoft/macrodroid/intro/a$a;

    .line 187
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 190
    new-instance v0, Landroid/os/Bundle;

    .line 192
    invoke-direct {v0}, Landroid/os/Bundle;-><init>()V

    .line 195
    const-string v5, "device_type"

    .line 197
    invoke-virtual {v0, v5, p1}, Landroid/os/BaseBundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 200
    const-string/jumbo p1, "web_link"

    .line 202
    invoke-virtual {v0, p1, v4}, Landroid/os/BaseBundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 205
    new-instance p1, Lcom/arlosoft/macrodroid/intro/a;

    .line 207
    invoke-direct {p1}, Lcom/arlosoft/macrodroid/intro/a;-><init>()V

    .line 210
    invoke-virtual {p1, v0}, Landroidx/fragment/app/n;->setArguments(Landroid/os/Bundle;)V

    .line 213
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->M0(Lxpe;)V

    .line 216
    :cond_ec
    const/4 v8, 0x3

    sget-object p1, Lsz5;->a:Lsz5;

    .line 218
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 221
    const/4 v8, 0x5

    const-string p1, "nudsnlugarrbtatoeonn_i_"

    const-string p1, "funnel_onboarding_start"

    .line 223
    invoke-static {p1}, Lsz5;->g(Ljava/lang/String;)V

    .line 226
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->m:Landroid/widget/ImageButton;

    .line 228
    invoke-virtual {p1, v1}, Landroid/view/View;->setVisibility(I)V

    .line 231
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->n:Landroid/widget/ImageButton;

    .line 233
    invoke-virtual {p1, v2}, Landroid/view/View;->setVisibility(I)V

    .line 236
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->n:Landroid/widget/ImageButton;

    .line 238
    new-instance v0, Lt6;

    .line 240
    const/4 v8, 0x1

    const/4 v1, 0x7

    .line 241
    invoke-direct {v0, p0, v1}, Lt6;-><init>(Ljava/lang/Object;I)V

    .line 244
    invoke-virtual {p1, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 247
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->n:Landroid/widget/ImageButton;

    .line 249
    new-instance v0, Lq8;

    .line 251
    const/4 v8, 0x6

    const/16 v1, 0x1c

    .line 253
    invoke-direct {v0, p0, v1}, Lq8;-><init>(Ljava/lang/Object;I)V

    .line 256
    invoke-virtual {p1, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 259
    :try_start_11d
    const/4 v8, 0x5

    sget-object p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->E:Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;

    .line 261
    const/4 v8, 0x2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 264
    sget-object p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->F:Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 266
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 269
    const/4 v8, 0x5

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->j()Lt2c;

    .line 272
    move-result-object p1

    .line 273
    invoke-virtual {p1}, Lt2c;->a()Ln2c;

    .line 276
    move-result-object p1

    .line 277
    const/4 v8, 0x2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 280
    instance-of p1, p1, Ln2c$c;
    :try_end_138
    .catch Ljava/lang/Exception; {:try_start_11d .. :try_end_138} :catch_152

    .line 282
    const/4 v8, 0x5

    if-nez p1, :cond_152

    .line 284
    :try_start_13b
    const/4 v8, 0x5

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 287
    move-result-object p1

    .line 288
    new-instance v0, Lq68;

    .line 290
    invoke-direct {v0, v2}, Lq68;-><init>(I)V

    .line 293
    const/4 v8, 0x3

    invoke-static {}, Lcom/google/android/gms/ads/internal/client/zzeu;->d()Lcom/google/android/gms/ads/internal/client/zzeu;

    .line 296
    move-result-object v1

    .line 297
    invoke-virtual {v1, p1, v0}, Lcom/google/android/gms/ads/internal/client/zzeu;->e(Landroid/content/Context;Lcom/google/android/gms/ads/initialization/OnInitializationCompleteListener;)V
    :try_end_14d
    .catch Ljava/lang/Exception; {:try_start_13b .. :try_end_14d} :catch_14e

    .line 300
    goto :goto_152

    .line 301
    :catch_14e
    move-exception p1

    .line 302
    :try_start_14f
    invoke-static {p1}, Lsz5;->e(Ljava/lang/Throwable;)V
    :try_end_152
    .catch Ljava/lang/Exception; {:try_start_14f .. :try_end_152} :catch_152

    .line 305
    :catch_152
    :cond_152
    :goto_152
    const/4 v8, 0x4

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 308
    move-result-wide v0

    .line 309
    const/4 v8, 0x5

    sget-object p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->E:Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;

    .line 311
    const/4 v8, 0x2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 314
    sget-object p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->F:Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 316
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 319
    iget-object p1, p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->z:Lc71;

    .line 321
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 324
    const/4 v8, 0x1

    sget-object v4, Ldvd;->a:Lsud;

    .line 326
    const-string/jumbo v5, "timeUnit is null"

    .line 328
    const/4 v8, 0x1

    sget-object v6, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 330
    invoke-static {v6, v5}, Lpm6;->N(Ljava/lang/Object;Ljava/lang/String;)V

    .line 333
    const-string v5, "scheduler is null"

    .line 335
    invoke-static {v4, v5}, Lpm6;->N(Ljava/lang/Object;Ljava/lang/String;)V

    .line 338
    new-instance v5, Li0b;

    .line 340
    const/4 v8, 0x2

    const-wide/16 v6, 0x5

    .line 342
    invoke-direct {v5, p1, v6, v7, v4}, Li0b;-><init>(Lgza;JLsud;)V

    .line 345
    new-instance p1, Lg0b;

    .line 347
    invoke-direct {p1, v5}, Lp2;-><init>(Lgza;)V

    .line 350
    sget-object v4, Ldvd;->b:Lsud;

    .line 352
    invoke-virtual {p1, v4}, Lgza;->e(Lsud;)Llza;

    .line 355
    move-result-object p1

    .line 356
    invoke-static {}, Lf10;->a()Lt47;

    .line 359
    move-result-object v4

    .line 360
    const/4 v8, 0x3

    invoke-virtual {p1, v4}, Lgza;->a(Lt47;)Lqza;

    .line 363
    move-result-object p1

    .line 364
    const/4 v8, 0x5

    new-instance v4, Lvf3;

    .line 366
    invoke-direct {v4, p0, v0, v1, v3}, Lvf3;-><init>(Ljava/lang/Object;JI)V

    .line 369
    new-instance v0, Lfd6;

    .line 371
    const/4 v1, 0x4

    .line 372
    invoke-direct {v0, v4, v1}, Lfd6;-><init>(Ljava/lang/Object;I)V

    .line 375
    const/4 v8, 0x7

    new-instance v1, Lr68;

    .line 377
    invoke-direct {v1, p0, v2}, Lr68;-><init>(Lcom/arlosoft/macrodroid/intro/IntroActivity;I)V

    .line 380
    new-instance p0, Lfd6;

    .line 382
    const/4 v8, 0x2

    const/4 v2, 0x5

    .line 383
    invoke-direct {p0, v1, v2}, Lfd6;-><init>(Ljava/lang/Object;I)V

    .line 386
    const/4 v8, 0x3

    new-instance v1, Lrt8;

    .line 388
    invoke-direct {v1, v0, p0}, Lrt8;-><init>(Lg33;Lg33;)V

    .line 391
    const/4 v8, 0x0

    invoke-virtual {p1, v1}, Lgza;->c(Lo0b;)V

    .line 394
    return-void
.end method
