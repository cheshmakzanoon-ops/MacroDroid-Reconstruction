.class public final synthetic Lzh;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# instance fields
.field public final synthetic a:I

.field public final synthetic b:Landroid/app/Activity;


# direct methods
.method public synthetic constructor <init>(ILandroid/app/Activity;)V
    .locals 1

    .line 1
    const/4 v0, 0x6

    iput p1, p0, Lzh;->a:I

    .line 3
    iput-object p2, p0, Lzh;->b:Landroid/app/Activity;

    .line 5
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 8
    return-void
.end method

.method public synthetic constructor <init>(ILandroid/app/Activity;Ljava/lang/Object;)V
    .locals 1

    .line 9
    iput p1, p0, Lzh;->a:I

    iput-object p2, p0, Lzh;->b:Landroid/app/Activity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final onClick(Landroid/content/DialogInterface;I)V
    .locals 12

    .line 1
    const-string v11, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget p2, p0, Lzh;->a:I

    .line 3
    const/high16 v0, 0x10000000

    .line 5
    const/16 v1, 0x16

    .line 7
    const/4 v11, 0x6

    const/4 v2, 0x0

    .line 8
    const/4 v11, 0x0

    const-string v3, "gisesomdp:tarorfccldao.ocrakoam"

    const-string v3, "package:com.arlosoft.macrodroid"

    .line 10
    const/4 v4, 0x0

    .line 11
    const v5, 0x7f140622

    .line 14
    const v6, 0x7f140623

    .line 17
    const-string v7, "naEmodWn.rtaIoit.Vnidnciet"

    const-string v7, "android.intent.action.VIEW"

    .line 19
    const-string v8, ".CSsoedMIOModARtsS_APFEAPIIE.LSiN_NiagLES_CnE_nALAGtPS_"

    const-string v8, "android.settings.MANAGE_APP_ALL_FILES_ACCESS_PERMISSION"

    .line 21
    const/4 v11, 0x6

    const/4 v9, 0x1

    .line 22
    const-string v10, "package:"

    .line 24
    const/4 v11, 0x4

    iget-object p0, p0, Lzh;->b:Landroid/app/Activity;

    .line 26
    packed-switch p2, :pswitch_data_39e

    .line 29
    sget-object p1, Lcom/arlosoft/macrodroid/action/WriteToFileAction;->CREATOR:Landroid/os/Parcelable$Creator;

    .line 31
    const/4 v11, 0x3

    new-instance p1, Landroid/content/Intent;

    .line 33
    new-instance p2, Ljava/lang/StringBuilder;

    .line 35
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 38
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 41
    move-result-object v0

    .line 42
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 45
    const/4 v11, 0x2

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 48
    move-result-object p2

    .line 49
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 52
    move-result-object p2

    .line 53
    const/4 v11, 0x3

    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 56
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 59
    const/4 v11, 0x6

    return-void

    .line 60
    :pswitch_4b
    :try_start_4b
    new-instance p1, Landroid/content/Intent;

    .line 62
    const/4 v11, 0x7

    const-string p2, "cs/robearitmr:iap../coomdhdlt"

    const-string p2, "https://serial.macrodroid.com"

    .line 64
    const/4 v11, 0x0

    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 67
    move-result-object p2

    .line 68
    const/4 v11, 0x0

    invoke-direct {p1, v7, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 71
    const/4 v11, 0x7

    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_5f
    .catch Landroid/content/ActivityNotFoundException; {:try_start_4b .. :try_end_5f} :catch_61

    .line 74
    const/4 v11, 0x2

    goto :goto_66

    .line 75
    :catch_61
    const-string p0, "No browser available to open serial.macrodroid.com"

    .line 77
    invoke-static {p0}, Lkjf;->h(Ljava/lang/String;)V

    .line 80
    :goto_66
    return-void

    .line 81
    :pswitch_67
    invoke-interface {p1}, Landroid/content/DialogInterface;->dismiss()V

    .line 84
    const/4 v11, 0x0

    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 87
    const/4 v11, 0x6

    return-void

    .line 88
    :pswitch_70
    sget p1, Lcom/arlosoft/macrodroid/action/TakeScreenshotAction;->SAVE_TO_DEVICE:I

    .line 90
    new-instance p1, Landroid/content/Intent;

    .line 92
    new-instance p2, Ljava/lang/StringBuilder;

    .line 94
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 97
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 100
    move-result-object v0

    .line 101
    const/4 v11, 0x1

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 104
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 107
    move-result-object p2

    .line 108
    const/4 v11, 0x4

    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 111
    move-result-object p2

    .line 112
    const/4 v11, 0x4

    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 115
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 118
    return-void

    .line 119
    :pswitch_92
    const/4 v11, 0x6

    sget-object p1, Lcom/arlosoft/macrodroid/action/TakePictureAction;->CAMERA_ID_EXTRA:Ljava/lang/String;

    .line 121
    new-instance p1, Landroid/content/Intent;

    .line 123
    new-instance p2, Ljava/lang/StringBuilder;

    .line 125
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 128
    const/4 v11, 0x6

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 131
    move-result-object v0

    .line 132
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 135
    const/4 v11, 0x6

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 138
    move-result-object p2

    .line 139
    const/4 v11, 0x2

    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 142
    move-result-object p2

    .line 143
    const/4 v11, 0x0

    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 146
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 149
    return-void

    .line 150
    :pswitch_b6
    const/4 v11, 0x7

    invoke-static {p0}, Ldje;->e(Landroid/app/Activity;)V

    .line 153
    return-void

    .line 154
    :pswitch_bb
    invoke-static {p0}, Ldje;->f(Landroid/app/Activity;)V

    .line 157
    return-void

    .line 158
    :pswitch_bf
    const/4 v11, 0x2

    sget-object p1, Lcom/arlosoft/macrodroid/triggers/ShareFileTrigger;->Companion:Lcom/arlosoft/macrodroid/triggers/ShareFileTrigger$b;

    .line 160
    const/4 v11, 0x7

    new-instance p1, Landroid/content/Intent;

    .line 162
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 165
    move-result-object p2

    .line 166
    const/4 v11, 0x4

    new-instance v0, Ljava/lang/StringBuilder;

    .line 168
    const/4 v11, 0x5

    invoke-direct {v0, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 171
    const/4 v11, 0x7

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 174
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 177
    move-result-object p2

    .line 178
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 181
    move-result-object p2

    .line 182
    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 185
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 188
    return-void

    .line 189
    :pswitch_e3
    sget-object p1, Lcom/arlosoft/macrodroid/action/RecordMicrophoneAction;->RECORDINGS_DIRECTORY:Ljava/lang/String;

    .line 191
    new-instance p1, Landroid/content/Intent;

    .line 193
    new-instance p2, Ljava/lang/StringBuilder;

    .line 195
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 198
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 201
    move-result-object v0

    .line 202
    const/4 v11, 0x7

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 205
    const/4 v11, 0x0

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 208
    move-result-object p2

    .line 209
    const/4 v11, 0x4

    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 212
    move-result-object p2

    .line 213
    const/4 v11, 0x3

    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 216
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 219
    return-void

    .line 220
    :pswitch_106
    const/4 v11, 0x0

    sget-object p1, Lcom/arlosoft/macrodroid/action/PlaySoundAction;->CREATOR:Landroid/os/Parcelable$Creator;

    .line 222
    new-instance p1, Landroid/content/Intent;

    .line 224
    new-instance p2, Ljava/lang/StringBuilder;

    .line 226
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 229
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 232
    move-result-object v0

    .line 233
    const/4 v11, 0x1

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 236
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 239
    move-result-object p2

    .line 240
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 243
    move-result-object p2

    .line 244
    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 247
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 250
    const/4 v11, 0x5

    return-void

    .line 251
    :pswitch_128
    sget-object p0, Llob;->a:Ljava/util/HashMap;

    .line 253
    const/4 v11, 0x4

    return-void

    .line 254
    :pswitch_12c
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 256
    new-instance p1, Landroid/content/Intent;

    .line 258
    const-string p2, "android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"

    .line 260
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 263
    :try_start_135
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_138
    .catch Ljava/lang/Exception; {:try_start_135 .. :try_end_138} :catch_13a

    .line 266
    const/4 v11, 0x3

    goto :goto_142

    .line 267
    :catch_13a
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 270
    move-result-object p1

    .line 271
    const/4 v11, 0x0

    invoke-static {p0, v5, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 274
    :goto_142
    const/4 v11, 0x7

    return-void

    .line 275
    :pswitch_144
    const/4 v11, 0x6

    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 277
    new-instance p1, Landroid/content/Intent;

    .line 279
    new-instance p2, Ljava/lang/StringBuilder;

    .line 281
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 284
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 287
    move-result-object v0

    .line 288
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 291
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 294
    move-result-object p2

    .line 295
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 298
    move-result-object p2

    .line 299
    const/4 v11, 0x1

    const-string v0, "oTC_DiuRSnHCEtMAdnRT_SEEdAE.aetLULrsAgsX.iU_Q"

    const-string v0, "android.settings.REQUEST_SCHEDULE_EXACT_ALARM"

    .line 301
    invoke-direct {p1, v0, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 304
    const/4 v11, 0x7

    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 307
    return-void

    .line 308
    :pswitch_16a
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 310
    sget-object p1, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 312
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 315
    move-result-object p0

    .line 316
    const/4 v11, 0x4

    invoke-interface {p0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    .line 319
    move-result-object p0

    .line 320
    const/4 v11, 0x6

    const-string p1, "ignore_default_assist_warning"

    .line 322
    invoke-interface {p0, p1, v9}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    .line 325
    move-result-object p0

    .line 326
    invoke-interface {p0}, Landroid/content/SharedPreferences$Editor;->apply()V

    .line 329
    invoke-static {}, Lcj5;->a()Laj5;

    .line 332
    move-result-object p0

    .line 333
    const/4 v11, 0x2

    new-instance p1, Lcom/arlosoft/macrodroid/events/RefreshEditMacroPageEvent;

    .line 335
    invoke-direct {p1, v4}, Lcom/arlosoft/macrodroid/events/RefreshEditMacroPageEvent;-><init>(Ljava/lang/Long;)V

    .line 338
    const/4 v11, 0x4

    invoke-virtual {p0, p1}, Laj5;->e(Ljava/lang/Object;)V

    .line 341
    const/4 v11, 0x0

    return-void

    .line 342
    :pswitch_191
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 344
    :try_start_193
    new-instance p1, Landroid/content/Intent;

    .line 346
    invoke-static {}, Llob;->d()Ljava/lang/String;

    .line 349
    move-result-object p2

    .line 350
    const/4 v11, 0x3

    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 353
    move-result-object p2

    .line 354
    invoke-direct {p1, v7, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 357
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_1a4
    .catch Landroid/content/ActivityNotFoundException; {:try_start_193 .. :try_end_1a4} :catch_1a4

    .line 360
    :catch_1a4
    const/4 v11, 0x6

    return-void

    .line 361
    :pswitch_1a6
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 363
    new-instance p1, Landroid/content/Intent;

    .line 365
    new-instance p2, Ljava/lang/StringBuilder;

    .line 367
    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 370
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 373
    move-result-object v0

    .line 374
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 377
    const/4 v11, 0x2

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 380
    move-result-object p2

    .line 381
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 384
    move-result-object p2

    .line 385
    const/4 v11, 0x6

    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 388
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 391
    return-void

    .line 392
    :pswitch_1c7
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 394
    new-instance p1, Landroid/content/Intent;

    .line 396
    const-string p2, "android.settings.action.MANAGE_OVERLAY_PERMISSION"

    .line 398
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 401
    invoke-static {v3}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 404
    move-result-object p2

    .line 405
    const/4 v11, 0x5

    invoke-virtual {p1, p2}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;

    .line 408
    :try_start_1d8
    invoke-virtual {p0, p1, v9}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_1db
    .catch Ljava/lang/Exception; {:try_start_1d8 .. :try_end_1db} :catch_1dc

    .line 411
    goto :goto_1e4

    .line 412
    :catch_1dc
    const/4 v11, 0x3

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 415
    move-result-object p1

    .line 416
    invoke-static {p0, v6, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 419
    :goto_1e4
    return-void

    .line 420
    :pswitch_1e5
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 422
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 425
    move-result-object p1

    .line 426
    iget-object p1, p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->n:Ldje;

    .line 428
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 431
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 434
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 437
    move-result-object p2

    .line 438
    :try_start_1f7
    invoke-virtual {p2}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 441
    move-result-object p2

    .line 442
    const-string v0, "moe.shizuku.manager.permission.API_V23"

    .line 444
    invoke-virtual {p2, v0, v2}, Landroid/content/pm/PackageManager;->getPermissionInfo(Ljava/lang/String;I)Landroid/content/pm/PermissionInfo;

    .line 447
    move-result-object p2
    :try_end_201
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_1f7 .. :try_end_201} :catch_202

    .line 448
    goto :goto_203

    .line 449
    :catch_202
    move-object p2, v4

    .line 450
    :goto_203
    const/4 v11, 0x5

    const/high16 v0, 0x1040000

    .line 452
    const/4 v11, 0x3

    const v2, 0x7f141413

    .line 455
    const/4 v11, 0x5

    const v3, 0x7f150337

    .line 458
    if-eqz p2, :cond_252

    .line 460
    invoke-virtual {p1, v9}, Ldje;->c(Z)Ljje;

    .line 463
    move-result-object p2

    .line 464
    const/4 v11, 0x5

    sget-object v1, Laje;->a:[I

    .line 466
    invoke-virtual {p2}, Ljava/lang/Enum;->ordinal()I

    .line 469
    move-result p2

    .line 470
    aget p2, v1, p2

    .line 472
    const/4 v1, 0x2

    .line 473
    const/4 v11, 0x5

    if-eq p2, v1, :cond_24e

    .line 475
    const/4 v1, 0x3

    .line 476
    if-eq p2, v1, :cond_230

    .line 478
    new-instance p2, Lu4e;

    .line 480
    const/16 v0, 0x8

    .line 482
    invoke-direct {p2, v0, p0, p1}, Lu4e;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 485
    const/4 v11, 0x2

    invoke-virtual {p1, p2}, Ldje;->g(Lwm6;)V

    .line 488
    goto :goto_26d

    .line 489
    :cond_230
    const/4 v11, 0x0

    const p2, 0x7f141418

    .line 492
    invoke-static {p0, v3, v2, p2}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 495
    move-result-object p2

    .line 496
    const/4 v11, 0x6

    new-instance v1, Lzh;

    .line 498
    const/16 v2, 0x17

    .line 500
    invoke-direct {v1, v2, p0, p1}, Lzh;-><init>(ILandroid/app/Activity;Ljava/lang/Object;)V

    .line 503
    const p0, 0x7f14114f

    .line 506
    invoke-virtual {p2, p0, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 509
    invoke-virtual {p2, v0, v4}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 512
    invoke-virtual {p2}, Lyo;->o()Lzo;

    .line 515
    const/4 v11, 0x1

    goto :goto_26d

    .line 516
    :cond_24e
    invoke-static {p0}, Ldje;->j(Landroid/app/Activity;)V

    .line 519
    goto :goto_26d

    .line 520
    :cond_252
    const/4 v11, 0x3

    const p2, 0x7f14141a

    .line 523
    const/4 v11, 0x1

    invoke-static {p0, v3, v2, p2}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 526
    move-result-object p2

    .line 527
    new-instance v2, Lzh;

    .line 529
    const/4 v11, 0x2

    invoke-direct {v2, v1, p0, p1}, Lzh;-><init>(ILandroid/app/Activity;Ljava/lang/Object;)V

    .line 532
    const p0, 0x7f140dd2

    .line 535
    invoke-virtual {p2, p0, v2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 538
    invoke-virtual {p2, v0, v4}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 541
    invoke-virtual {p2}, Lyo;->o()Lzo;

    .line 544
    :goto_26d
    const/4 v11, 0x4

    return-void

    .line 545
    :pswitch_26f
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 547
    :try_start_271
    new-instance p1, Landroid/content/Intent;

    .line 549
    invoke-static {}, Llob;->d()Ljava/lang/String;

    .line 552
    move-result-object p2

    .line 553
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 556
    move-result-object p2

    .line 557
    invoke-direct {p1, v7, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 560
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_281
    .catch Landroid/content/ActivityNotFoundException; {:try_start_271 .. :try_end_281} :catch_281

    .line 563
    :catch_281
    const/4 v11, 0x3

    return-void

    .line 564
    :pswitch_283
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 566
    const/4 v11, 0x6

    new-instance p1, Landroid/content/Intent;

    .line 568
    const-string p2, "android.settings.action.MANAGE_WRITE_SETTINGS"

    .line 570
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 573
    const/4 v11, 0x5

    invoke-static {v3}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 576
    move-result-object p2

    .line 577
    const/4 v11, 0x1

    invoke-virtual {p1, p2}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;

    .line 580
    const/4 v11, 0x7

    invoke-virtual {p1, v0}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 583
    :try_start_29a
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_29d
    .catch Ljava/lang/Exception; {:try_start_29a .. :try_end_29d} :catch_29f

    .line 586
    const/4 v11, 0x6

    goto :goto_2a6

    .line 587
    :catch_29f
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 590
    move-result-object p1

    .line 591
    invoke-static {p0, v6, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 594
    :goto_2a6
    return-void

    .line 595
    :pswitch_2a7
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 597
    new-instance p1, Landroid/content/Intent;

    .line 599
    const/4 v11, 0x6

    const-string p2, "android.settings.NOTIFICATION_POLICY_ACCESS_SETTINGS"

    .line 601
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 604
    :try_start_2b1
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_2b4
    .catch Ljava/lang/Exception; {:try_start_2b1 .. :try_end_2b4} :catch_2b5

    .line 607
    goto :goto_2bd

    .line 608
    :catch_2b5
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 611
    move-result-object p1

    .line 612
    const/4 v11, 0x6

    invoke-static {p0, v5, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 615
    :goto_2bd
    const/4 v11, 0x1

    return-void

    .line 616
    :pswitch_2bf
    const/4 v11, 0x1

    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 618
    const/4 v11, 0x7

    new-instance p1, Landroid/content/Intent;

    .line 620
    const-string p2, "android.settings.USAGE_ACCESS_SETTINGS"

    .line 622
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 625
    const/4 v11, 0x3

    invoke-virtual {p1, v0}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 628
    :try_start_2ce
    const/4 v11, 0x5

    invoke-virtual {p0, p1, v2}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_2d2
    .catch Ljava/lang/Exception; {:try_start_2ce .. :try_end_2d2} :catch_2d3

    .line 631
    goto :goto_2df

    .line 632
    :catch_2d3
    const/4 v11, 0x0

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 635
    move-result-object p1

    .line 636
    const/4 v11, 0x3

    const p2, 0x7f140621

    .line 639
    invoke-static {p0, p2, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 642
    :goto_2df
    const/4 v11, 0x3

    return-void

    .line 643
    :pswitch_2e1
    sget-object p1, Llob;->a:Ljava/util/HashMap;

    .line 645
    :try_start_2e3
    new-instance p1, Liwa;

    .line 647
    const/4 v11, 0x0

    invoke-direct {p1, p0}, Liwa;-><init>(Landroid/content/Context;)V

    .line 650
    invoke-virtual {p1}, Liwa;->a()Z

    .line 653
    move-result p1
    :try_end_2ed
    .catch Landroid/content/ActivityNotFoundException; {:try_start_2e3 .. :try_end_2ed} :catch_320

    .line 654
    const/4 v11, 0x2

    const-string p2, "dp.EaePpGvAKi_roPCenPrtrodiarA.xAd"

    const-string p2, "android.provider.extra.APP_PACKAGE"

    .line 656
    if-nez p1, :cond_309

    .line 658
    :try_start_2f4
    new-instance p1, Landroid/content/Intent;

    .line 660
    const/4 v11, 0x2

    const-string v0, "android.settings.APP_NOTIFICATION_SETTINGS"

    .line 662
    const/4 v11, 0x0

    invoke-direct {p1, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 665
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 668
    move-result-object v0

    .line 669
    invoke-virtual {p1, p2, v0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 672
    move-result-object p1

    .line 673
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 676
    goto :goto_330

    .line 677
    :cond_309
    const/4 v11, 0x1

    new-instance p1, Landroid/content/Intent;

    .line 679
    const-string v0, "SiOABdgEqisnnETIFSNICatGAr__seNTTPLBdt.PTOIN.Uo_B"

    const-string v0, "android.settings.APP_NOTIFICATION_BUBBLE_SETTINGS"

    .line 681
    invoke-direct {p1, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 684
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 687
    move-result-object v0

    .line 688
    const/4 v11, 0x1

    invoke-virtual {p1, p2, v0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 691
    move-result-object p1

    .line 692
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_31f
    .catch Landroid/content/ActivityNotFoundException; {:try_start_2f4 .. :try_end_31f} :catch_320

    .line 695
    goto :goto_330

    .line 696
    :catch_320
    const/4 v11, 0x5

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 699
    move-result-object p0

    .line 700
    const-string p1, "hNsC tI_nU_rpBNSePTcitBT_ienIgs rT tIOnIouevsdOptoES  sGP.BodLiaTdAnAEdiFeosN."

    const-string p1, "android.settings.APP_NOTIFICATION_BUBBLE_SETTINGS not supported on this device"

    .line 702
    invoke-static {p0, p1, v9}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 705
    move-result-object p0

    .line 706
    invoke-virtual {p0}, Le3g;->show()V

    .line 709
    :goto_330
    const/4 v11, 0x0

    return-void

    .line 710
    :pswitch_332
    sget p1, Lcom/arlosoft/macrodroid/permissions/PermissionRequestActivity;->j:I

    .line 712
    new-instance p1, Lmm3;

    .line 714
    invoke-direct {p1, p0, v1}, Lmm3;-><init>(Ljava/lang/Object;I)V

    .line 717
    const/4 v11, 0x3

    const-string p2, "nIDmrDsdiodpAEsRRO_.nCeia.oUiOr"

    const-string p2, "android.permission.RECORD_AUDIO"

    .line 719
    const/4 v11, 0x3

    invoke-static {p0, p2, p1}, Lrk5;->a(Landroid/app/Activity;Ljava/lang/String;Lqk5;)V

    .line 722
    return-void

    .line 723
    :pswitch_343
    sget p1, Lcom/arlosoft/macrodroid/permissions/PermissionRequestActivity;->j:I

    .line 725
    :try_start_345
    const/4 v11, 0x7

    new-instance p1, Landroid/content/Intent;

    .line 727
    const/4 v11, 0x2

    const-string p2, "android.settings.SETTINGS"

    .line 729
    invoke-direct {p1, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 732
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 735
    const/4 v11, 0x4

    instance-of p1, p0, Lcom/arlosoft/macrodroid/permissions/PermissionRequestActivity;

    .line 737
    const/4 v11, 0x4

    if-eqz p1, :cond_363

    .line 739
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V
    :try_end_35a
    .catch Ljava/lang/Exception; {:try_start_345 .. :try_end_35a} :catch_35b

    .line 742
    goto :goto_363

    .line 743
    :catch_35b
    const/4 v11, 0x3

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 746
    move-result-object p1

    .line 747
    invoke-static {p0, v6, p1, v9}, Lni9;->B(Landroid/app/Activity;ILandroid/content/Context;I)V

    .line 750
    :cond_363
    :goto_363
    return-void

    .line 751
    :pswitch_364
    invoke-static {p0}, Llmb;->b(Landroid/content/Context;)V

    .line 754
    return-void

    .line 755
    :pswitch_368
    sget-object p1, Lcom/arlosoft/macrodroid/triggers/NotificationButtonTrigger;->CREATOR:Landroid/os/Parcelable$Creator;

    .line 757
    const/4 v11, 0x7

    new-instance p1, Landroid/content/Intent;

    .line 759
    const-class p2, Lcom/arlosoft/macrodroid/ConfigureNotificationBarActivity;

    .line 761
    invoke-direct {p1, p0, p2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 764
    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 767
    return-void

    .line 768
    :pswitch_376
    sget-object p1, Lcom/arlosoft/macrodroid/action/ExportMacrosAction;->CREATOR:Landroid/os/Parcelable$Creator;

    .line 770
    new-instance p1, Landroid/content/Intent;

    .line 772
    const/4 v11, 0x0

    new-instance p2, Ljava/lang/StringBuilder;

    .line 774
    const/4 v11, 0x0

    invoke-direct {p2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 777
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 780
    move-result-object v0

    .line 781
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 784
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 787
    move-result-object p2

    .line 788
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 791
    move-result-object p2

    .line 792
    invoke-direct {p1, v8, p2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 795
    const/4 v11, 0x6

    invoke-virtual {p0, p1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 798
    const/4 v11, 0x3

    return-void

    .line 799
    :pswitch_399
    invoke-static {p0}, Lai;->b(Landroid/content/Context;)V

    .line 802
    return-void

    nop

    .line 803
    :pswitch_data_39e
    .packed-switch 0x0
        :pswitch_399
        :pswitch_376
        :pswitch_368
        :pswitch_364
        :pswitch_343
        :pswitch_332
        :pswitch_2e1
        :pswitch_2bf
        :pswitch_2a7
        :pswitch_283
        :pswitch_26f
        :pswitch_1e5
        :pswitch_1c7
        :pswitch_1a6
        :pswitch_191
        :pswitch_16a
        :pswitch_144
        :pswitch_12c
        :pswitch_128
        :pswitch_106
        :pswitch_e3
        :pswitch_bf
        :pswitch_bb
        :pswitch_b6
        :pswitch_92
        :pswitch_70
        :pswitch_67
        :pswitch_4b
    .end packed-switch
.end method
