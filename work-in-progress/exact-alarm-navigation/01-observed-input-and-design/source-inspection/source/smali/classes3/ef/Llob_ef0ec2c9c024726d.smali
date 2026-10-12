.class public Llob;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# static fields
.field public static final a:Ljava/util/HashMap;

.field public static final b:Ljava/util/HashMap;

.field public static final c:[Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 15

    .line 1
    new-instance v0, Ljava/util/HashMap;

    .line 3
    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    .line 6
    sput-object v0, Llob;->a:Ljava/util/HashMap;

    .line 8
    new-instance v1, Ljava/util/HashMap;

    .line 10
    invoke-direct {v1}, Ljava/util/HashMap;-><init>()V

    .line 13
    sput-object v1, Llob;->b:Ljava/util/HashMap;

    .line 15
    const-string v13, "he"

    const-string v13, "he"

    .line 17
    const-string/jumbo v14, "vi"

    .line 19
    const-string/jumbo v2, "tp"

    const-string v2, "pt"

    .line 21
    const-string v3, "es"

    .line 23
    const-string v4, "fr"

    .line 25
    const-string v5, "ru"

    .line 27
    const-string v6, "aj"

    const-string v6, "ja"

    .line 29
    const-string v7, "ko"

    .line 31
    const-string v8, "de"

    .line 33
    const-string/jumbo v9, "tr"

    .line 35
    const-string v10, "di"

    const-string v10, "id"

    .line 37
    const-string v11, "it"

    .line 39
    const-string v12, "hu"

    .line 41
    filled-new-array/range {v2 .. v14}, [Ljava/lang/String;

    .line 44
    move-result-object v2

    .line 45
    sput-object v2, Llob;->c:[Ljava/lang/String;

    .line 47
    const-string v2, "TnsLWrAE.ArmsaNiCsiERo.onIRepD_di"

    const-string v2, "android.permission.WRITE_CALENDAR"

    .line 49
    const v3, 0x7a1dba

    .line 52
    const v4, 0x7a1db9

    .line 55
    const-string v5, "android.permission.READ_CALENDAR"

    .line 57
    invoke-static {v4, v0, v5, v3, v2}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 60
    const-string v2, "android.permission.READ_CONTACTS"

    .line 62
    const v3, 0x7a1dbc

    .line 65
    const v4, 0x7a1dbb

    .line 68
    const-string v5, "iidmamRCd.rsiMpoEr.AsnnAe"

    const-string v5, "android.permission.CAMERA"

    .line 70
    invoke-static {v4, v0, v5, v3, v2}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 73
    const-string v2, "android.permission.GET_ACCOUNTS"

    .line 75
    const v3, 0x7a1dbe

    .line 78
    const v4, 0x7a1dbd

    .line 81
    const-string v5, "android.permission.WRITE_CONTACTS"

    .line 83
    invoke-static {v4, v0, v5, v3, v2}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 86
    const-string v2, "android.permission.ACCESS_COARSE_LOCATION"

    .line 88
    const v3, 0x7a1dc0

    .line 91
    const v4, 0x7a1dbf

    .line 94
    const-string v5, "android.permission.ACCESS_FINE_LOCATION"

    .line 96
    invoke-static {v4, v0, v5, v3, v2}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 99
    const-string v2, "android.permission.READ_PHONE_STATE"

    .line 101
    const v3, 0x7a1dc2

    .line 104
    const v4, 0x7a1dc1

    .line 107
    const-string v5, "android.permission.RECORD_AUDIO"

    .line 109
    invoke-static {v4, v0, v5, v3, v2}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 112
    const v2, 0x7a1dc3

    .line 115
    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 118
    move-result-object v2

    .line 119
    const-string v3, "android.permission.CALL_PHONE"

    .line 121
    invoke-virtual {v0, v3, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 124
    const v2, 0x7a1dc4

    .line 127
    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 130
    move-result-object v2

    .line 131
    const-string v3, "O.pdo_LLi_mEAonDCssRGnLo.aeAdiir"

    const-string v3, "android.permission.READ_CALL_LOG"

    .line 133
    invoke-virtual {v0, v3, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 136
    const v3, 0x7a1dc5

    .line 139
    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 142
    move-result-object v3

    .line 143
    const-string v4, "android.permission.WRITE_CALL_LOG"

    .line 145
    invoke-virtual {v0, v4, v3}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 148
    const v4, 0x7a1dc6

    .line 151
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 154
    move-result-object v4

    .line 155
    const-string v5, "android.permission.USE_SIP"

    .line 157
    invoke-virtual {v0, v5, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 160
    const-string v4, "android.permission.BODY_SENSORS"

    .line 162
    const v5, 0x7a1dc8

    .line 165
    const v6, 0x7a1dc7

    .line 168
    const-string v7, "android.permission.PROCESS_OUTGOING_CALLS"

    .line 170
    invoke-static {v6, v0, v7, v5, v4}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 173
    const-string v4, "dCn.ibrRMisE._nsVemEdipSIEroSa"

    const-string v4, "android.permission.RECEIVE_SMS"

    .line 175
    const v5, 0x7a1dca

    .line 178
    const v6, 0x7a1dc9

    .line 181
    const-string v7, "android.permission.SEND_SMS"

    .line 183
    invoke-static {v6, v0, v7, v5, v4}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 186
    const-string v4, "android.permission.RECEIVE_WAP_PUSH"

    .line 188
    const v5, 0x7a1dcc

    .line 191
    const v6, 0x7a1dcb

    .line 194
    const-string v7, "android.permission.READ_SMS"

    .line 196
    invoke-static {v6, v0, v7, v5, v4}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 199
    const-string v4, "XEpORNurAAnS_.dRaoeEiisAEGTm._EsrnTDioRL"

    const-string v4, "android.permission.READ_EXTERNAL_STORAGE"

    .line 201
    const v5, 0x7a1dce

    .line 204
    const v6, 0x7a1dcd

    .line 207
    const-string v7, "android.permission.RECEIVE_MMS"

    .line 209
    invoke-static {v6, v0, v7, v5, v4}, Lku1;->x(ILjava/util/HashMap;Ljava/lang/String;ILjava/lang/String;)V

    .line 212
    const v4, 0x7a1dcf

    .line 215
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 218
    move-result-object v4

    .line 219
    const-string v5, "pGeOidTpRLEsiWSA.EREarrEnIs_mn_dTRA.XiNTo"

    const-string v5, "android.permission.WRITE_EXTERNAL_STORAGE"

    .line 221
    invoke-virtual {v0, v5, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 224
    const/4 v0, 0x1

    .line 225
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 228
    move-result-object v0

    .line 229
    const v4, 0x7a21a1

    .line 232
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 235
    move-result-object v4

    .line 236
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 239
    const/4 v0, 0x2

    .line 240
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 243
    move-result-object v0

    .line 244
    const v4, 0x7a21a2

    .line 247
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 250
    move-result-object v4

    .line 251
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 254
    const/4 v0, 0x3

    .line 255
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 258
    move-result-object v0

    .line 259
    const v4, 0x7a21a3

    .line 262
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 265
    move-result-object v4

    .line 266
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 269
    const/4 v0, 0x4

    .line 270
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 273
    move-result-object v0

    .line 274
    const v4, 0x7a21a4

    .line 277
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 280
    move-result-object v4

    .line 281
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 284
    const/4 v0, 0x5

    .line 285
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 288
    move-result-object v0

    .line 289
    const v4, 0x7a21a5

    .line 292
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 295
    move-result-object v4

    .line 296
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 299
    const/4 v0, 0x6

    .line 300
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 303
    move-result-object v0

    .line 304
    const v4, 0x7a21a6

    .line 307
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 310
    move-result-object v4

    .line 311
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 314
    const/4 v0, 0x7

    .line 315
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 318
    move-result-object v0

    .line 319
    const v4, 0x7a21a7

    .line 322
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 325
    move-result-object v4

    .line 326
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 329
    const/16 v0, 0x8

    .line 331
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 334
    move-result-object v0

    .line 335
    const v4, 0x7a21a8

    .line 338
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 341
    move-result-object v4

    .line 342
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 345
    const/16 v0, 0x9

    .line 347
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 350
    move-result-object v0

    .line 351
    const v4, 0x7a21a9

    .line 354
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 357
    move-result-object v4

    .line 358
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 361
    const/16 v0, 0xa

    .line 363
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 366
    move-result-object v0

    .line 367
    const v4, 0x7a21aa

    .line 370
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 373
    move-result-object v4

    .line 374
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 377
    const/16 v0, 0xb

    .line 379
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 382
    move-result-object v0

    .line 383
    const v4, 0x7a21ab

    .line 386
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 389
    move-result-object v4

    .line 390
    invoke-virtual {v1, v0, v4}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 393
    const/16 v0, 0xc

    .line 395
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 398
    move-result-object v0

    .line 399
    invoke-virtual {v1, v0, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 402
    const/16 v0, 0xf

    .line 404
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 407
    move-result-object v0

    .line 408
    invoke-virtual {v1, v0, v3}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 411
    return-void
.end method

.method public constructor <init>()V
    .locals 1

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 4
    const/4 v0, 0x2

    return-void
.end method

.method public static a(Landroid/content/Context;)Z
    .locals 7

    .line 1
    const-string v6, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    invoke-static {p0}, Landroid/provider/Settings;->canDrawOverlays(Landroid/content/Context;)Z

    .line 4
    move-result v0

    .line 5
    const/4 v6, 0x1

    const/4 v1, 0x1

    .line 6
    if-eqz v0, :cond_b

    .line 8
    return v1

    .line 9
    :cond_b
    const/4 v0, 0x0

    .line 10
    :try_start_c
    const-string v2, "appops"

    .line 12
    invoke-virtual {p0, v2}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 15
    move-result-object v2

    .line 16
    const/4 v6, 0x5

    check-cast v2, Landroid/app/AppOpsManager;

    .line 18
    if-nez v2, :cond_19

    .line 20
    const/4 v6, 0x1

    return v0

    .line 21
    :cond_19
    sget v3, Landroid/os/Build$VERSION;->SDK_INT:I
    :try_end_1b
    .catch Ljava/lang/Exception; {:try_start_c .. :try_end_1b} :catch_54

    .line 23
    const/4 v6, 0x0

    const/16 v4, 0x1d

    .line 25
    const-string v5, "android:system_alert_window"

    .line 27
    const/4 v6, 0x1

    if-lt v3, v4, :cond_33

    .line 29
    :try_start_23
    const/4 v6, 0x5

    invoke-static {}, Landroid/os/Process;->myUid()I

    .line 32
    move-result v3

    .line 33
    const/4 v6, 0x3

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 36
    move-result-object v4

    .line 37
    invoke-virtual {v2, v5, v3, v4}, Landroid/app/AppOpsManager;->unsafeCheckOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 40
    move-result v2

    .line 41
    const/4 v6, 0x5

    goto :goto_41

    .line 42
    :cond_33
    const/4 v6, 0x0

    invoke-static {}, Landroid/os/Process;->myUid()I

    .line 45
    move-result v3

    .line 46
    const/4 v6, 0x6

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 49
    move-result-object v4

    .line 50
    invoke-virtual {v2, v5, v3, v4}, Landroid/app/AppOpsManager;->checkOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 53
    move-result v2

    .line 54
    :goto_41
    const/4 v3, 0x3

    move v6, v3

    .line 55
    if-ne v2, v3, :cond_50

    .line 57
    const-string v2, "android.permission.SYSTEM_ALERT_WINDOW"

    .line 59
    invoke-static {p0, v2}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 62
    move-result p0
    :try_end_4b
    .catch Ljava/lang/Exception; {:try_start_23 .. :try_end_4b} :catch_54

    .line 63
    if-nez p0, :cond_4e

    .line 65
    return v1

    .line 66
    :cond_4e
    const/4 v6, 0x3

    return v0

    .line 67
    :cond_50
    const/4 v6, 0x1

    if-nez v2, :cond_54

    .line 69
    return v1

    .line 70
    :catch_54
    :cond_54
    const/4 v6, 0x7

    return v0
.end method

.method public static b(Landroid/content/Context;Lcom/arlosoft/macrodroid/common/SelectableItem;Z)Z
    .locals 3

    .line 1
    if-eqz p2, :cond_7

    .line 3
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissionsOnImport()[Ljava/lang/String;

    .line 6
    move-result-object p1

    .line 7
    goto :goto_c

    .line 8
    :cond_7
    const/4 v2, 0x0

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getRequiredPermissions()[Ljava/lang/String;

    .line 11
    move-result-object p1

    .line 12
    :goto_c
    if-eqz p1, :cond_26

    .line 14
    array-length p2, p1

    .line 15
    if-nez p2, :cond_13

    .line 17
    const/4 v2, 0x6

    goto :goto_26

    .line 18
    :cond_13
    const/4 p2, 0x0

    .line 19
    move v0, p2

    .line 20
    :goto_15
    const/4 v2, 0x2

    array-length v1, p1

    .line 21
    if-ge v0, v1, :cond_26

    .line 23
    aget-object v1, p1, v0

    .line 25
    invoke-static {p0, v1}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 28
    move-result v1

    .line 29
    if-eqz v1, :cond_22

    .line 31
    return p2

    .line 32
    :cond_22
    add-int/lit8 v0, v0, 0x1

    .line 34
    const/4 v2, 0x2

    goto :goto_15

    .line 35
    :cond_26
    :goto_26
    const/4 p0, 0x1

    .line 36
    return p0
.end method

.method public static c(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;ZZ)Z
    .locals 12

    .line 1
    const-string v0, "File acccess issue with: "

    .line 3
    const/4 v1, 0x1

    .line 4
    if-nez p0, :cond_7

    .line 6
    goto/16 :goto_343

    .line 8
    :cond_7
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 10
    const/16 v3, 0x1e

    .line 12
    const v4, 0x7f141190

    .line 15
    const/high16 v5, 0x1040000

    .line 17
    const v6, 0x104000a

    .line 20
    const v7, 0x7f150337

    .line 23
    const/4 v8, 0x0

    .line 24
    if-lt v2, v3, :cond_4c

    .line 26
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAllFilesAccess()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_4c

    .line 32
    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    .line 35
    move-result v2

    .line 36
    if-nez v2, :cond_4c

    .line 38
    const p1, 0x7f14118c

    .line 41
    invoke-static {p0, v7, v4, p1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 44
    move-result-object p1

    .line 45
    new-instance p2, Lzh;

    .line 47
    const/16 v0, 0xd

    .line 49
    invoke-direct {p2, v0, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 52
    invoke-virtual {p1, v6, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 55
    new-instance p2, Leob;

    .line 57
    const/16 v0, 0x9

    .line 59
    invoke-direct {p2, p3, p0, v0}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 62
    invoke-virtual {p1, v5, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 65
    iget-object p0, p1, Lyo;->a:Lvo;

    .line 67
    iput-boolean v8, p0, Lvo;->n:Z

    .line 69
    invoke-virtual {p1}, Lyo;->a()Lzo;

    .line 72
    move-result-object p0

    .line 73
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 76
    return v8

    .line 77
    :cond_4c
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresWriteSettings()Z

    .line 80
    move-result v2

    .line 81
    if-eqz v2, :cond_5e

    .line 83
    invoke-static {p0}, Landroid/provider/Settings$System;->canWrite(Landroid/content/Context;)Z

    .line 86
    move-result v2

    .line 87
    if-nez v2, :cond_5e

    .line 89
    if-eqz p2, :cond_23e

    .line 91
    invoke-static {p0, p3}, Llob;->r(Landroid/app/Activity;Z)V

    .line 94
    return v8

    .line 95
    :cond_5e
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanDrawOverlays()Z

    .line 98
    move-result v2

    .line 99
    if-eqz v2, :cond_70

    .line 101
    invoke-static {p0}, Llob;->a(Landroid/content/Context;)Z

    .line 104
    move-result v2

    .line 105
    if-nez v2, :cond_70

    .line 107
    if-eqz p2, :cond_23e

    .line 109
    invoke-static {p0, p3}, Llob;->l(Landroid/app/Activity;Z)V

    .line 112
    return v8

    .line 113
    :cond_70
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresLegacyHelperFile()Z

    .line 116
    move-result v2

    .line 117
    const-string v3, "com.arlosoft.macrodroid.helper"

    .line 119
    if-eqz v2, :cond_8f

    .line 121
    const-string v2, "com.arlosoft.macrodroid.settingshelper"

    .line 123
    invoke-static {v2}, Lgi0;->c(Ljava/lang/String;)Z

    .line 126
    move-result v2

    .line 127
    if-nez v2, :cond_8f

    .line 129
    invoke-static {v3}, Lgi0;->c(Ljava/lang/String;)Z

    .line 132
    move-result v2

    .line 133
    if-eqz v2, :cond_87

    .line 135
    goto :goto_8f

    .line 136
    :cond_87
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 139
    move-result-object p1

    .line 140
    invoke-static {p0, p1, p3}, Llob;->s(Landroid/app/Activity;Ljava/lang/String;Z)V

    .line 143
    return v8

    .line 144
    :cond_8f
    :goto_8f
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessNotificationPolicy()Z

    .line 147
    move-result v2

    .line 148
    if-eqz v2, :cond_d5

    .line 150
    const-string v2, "notification"

    .line 152
    invoke-virtual {p0, v2}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 155
    move-result-object v2

    .line 156
    check-cast v2, Landroid/app/NotificationManager;

    .line 158
    invoke-virtual {v2}, Landroid/app/NotificationManager;->isNotificationPolicyAccessGranted()Z

    .line 161
    move-result v2

    .line 162
    if-nez v2, :cond_d5

    .line 164
    const p1, 0x7f140940

    .line 167
    invoke-static {p0, v7, v4, p1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 170
    move-result-object p1

    .line 171
    new-instance p2, Lzh;

    .line 173
    const/16 v0, 0x8

    .line 175
    invoke-direct {p2, v0, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 178
    invoke-virtual {p1, v6, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 181
    new-instance p2, Leob;

    .line 183
    const/4 v0, 0x2

    .line 184
    invoke-direct {p2, p3, p0, v0}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 187
    invoke-virtual {p1, v5, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 190
    new-instance p2, Leob;

    .line 192
    const/4 v0, 0x3

    .line 193
    invoke-direct {p2, p0, p3, v0}, Leob;-><init>(Landroid/app/Activity;ZI)V

    .line 196
    const p0, 0x7f140d7a

    .line 199
    invoke-virtual {p1, p0, p2}, Lyo;->f(ILandroid/content/DialogInterface$OnClickListener;)V

    .line 202
    iget-object p0, p1, Lyo;->a:Lvo;

    .line 204
    iput-boolean v8, p0, Lvo;->n:Z

    .line 206
    invoke-virtual {p1}, Lyo;->a()Lzo;

    .line 209
    move-result-object p0

    .line 210
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 213
    return v8

    .line 214
    :cond_d5
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUsageAccess()Z

    .line 217
    move-result v2

    .line 218
    if-eqz v2, :cond_126

    .line 220
    :try_start_db
    invoke-virtual {p0}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 223
    move-result-object v2

    .line 224
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 227
    move-result-object v9

    .line 228
    invoke-virtual {v2, v9, v8}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;I)Landroid/content/pm/ApplicationInfo;

    .line 231
    move-result-object v2

    .line 232
    const-string v9, "appops"

    .line 234
    invoke-virtual {p0, v9}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 237
    move-result-object v9

    .line 238
    check-cast v9, Landroid/app/AppOpsManager;

    .line 240
    const-string v10, "android:get_usage_stats"

    .line 242
    iget v11, v2, Landroid/content/pm/ApplicationInfo;->uid:I

    .line 244
    iget-object v2, v2, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    .line 246
    invoke-virtual {v9, v10, v11, v2}, Landroid/app/AppOpsManager;->checkOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 249
    move-result v2
    :try_end_f9
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_db .. :try_end_f9} :catch_fc

    .line 250
    if-nez v2, :cond_fc

    .line 252
    goto :goto_126

    .line 253
    :catch_fc
    :cond_fc
    if-eqz p2, :cond_23e

    .line 255
    const p1, 0x7f1418f2

    .line 258
    const p2, 0x7f1418f3

    .line 261
    invoke-static {p0, v7, p1, p2}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 264
    move-result-object p1

    .line 265
    new-instance p2, Lzh;

    .line 267
    const/4 v0, 0x7

    .line 268
    invoke-direct {p2, v0, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 271
    invoke-virtual {p1, v6, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 274
    new-instance p2, Leob;

    .line 276
    invoke-direct {p2, p3, p0, v1}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 279
    invoke-virtual {p1, v5, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 282
    iget-object p0, p1, Lyo;->a:Lvo;

    .line 284
    iput-boolean v8, p0, Lvo;->n:Z

    .line 286
    invoke-virtual {p1}, Lyo;->a()Lzo;

    .line 289
    move-result-object p0

    .line 290
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 293
    goto/16 :goto_23e

    .line 295
    :cond_126
    :goto_126
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessibility()Z

    .line 298
    move-result v2

    .line 299
    if-eqz v2, :cond_138

    .line 301
    invoke-static {p0}, Lhtg;->I(Landroid/content/Context;)Z

    .line 304
    move-result v2

    .line 305
    if-nez v2, :cond_138

    .line 307
    if-eqz p2, :cond_23e

    .line 309
    invoke-static {p0, v8, v8, p3}, Llob;->i(Landroid/app/Activity;ZZZ)V

    .line 312
    return v8

    .line 313
    :cond_138
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUIInteractionAccessibility()Z

    .line 316
    move-result v2

    .line 317
    if-eqz v2, :cond_14a

    .line 319
    invoke-static {p0}, Lhtg;->J(Landroid/content/Context;)Z

    .line 322
    move-result v2

    .line 323
    if-nez v2, :cond_14a

    .line 325
    if-eqz p2, :cond_23e

    .line 327
    invoke-static {p0, v8, v1, p3}, Llob;->i(Landroid/app/Activity;ZZZ)V

    .line 330
    return v8

    .line 331
    :cond_14a
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDeviceAdmin()Z

    .line 334
    move-result v2

    .line 335
    if-eqz v2, :cond_16d

    .line 337
    new-instance v2, Landroid/content/ComponentName;

    .line 339
    const-class v9, Lcom/arlosoft/macrodroid/triggers/receivers/MacroDroidDeviceAdminReceiver;

    .line 341
    invoke-direct {v2, p0, v9}, Landroid/content/ComponentName;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 344
    const-string v9, "eycpld_iqvioe"

    const-string v9, "device_policy"

    .line 346
    invoke-virtual {p0, v9}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 349
    move-result-object v9

    .line 350
    check-cast v9, Landroid/app/admin/DevicePolicyManager;

    .line 352
    invoke-virtual {v9, v2}, Landroid/app/admin/DevicePolicyManager;->isAdminActive(Landroid/content/ComponentName;)Z

    .line 355
    move-result v9

    .line 356
    if-nez v9, :cond_16d

    .line 358
    if-eqz p2, :cond_23e

    .line 360
    invoke-static {p0, v2, v8, p3}, Llob;->n(Landroid/app/Activity;Landroid/content/ComponentName;ZZ)V

    .line 363
    return v8

    .line 364
    :cond_16d
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNotificationAccess()Z

    .line 367
    move-result v2

    .line 368
    if-eqz v2, :cond_1b9

    .line 370
    invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 373
    move-result-object v2

    .line 374
    const-string v9, "enabled_notification_listeners"

    .line 376
    invoke-static {v2, v9}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    .line 379
    move-result-object v2

    .line 380
    if-eqz v2, :cond_18d

    .line 382
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 385
    move-result-object v9

    .line 386
    invoke-virtual {v9}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 389
    move-result-object v9

    .line 390
    invoke-virtual {v2, v9}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 393
    move-result v2

    .line 394
    if-nez v2, :cond_1b9

    .line 396
    :cond_18d
    if-eqz p2, :cond_23e

    .line 398
    const p1, 0x7f1410ed

    .line 401
    const p2, 0x7f1410ec

    .line 404
    invoke-static {p0, v7, p1, p2}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 407
    move-result-object p1

    .line 408
    new-instance p2, Lzh;

    .line 410
    const/16 v0, 0x11

    .line 412
    invoke-direct {p2, v0, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 415
    invoke-virtual {p1, v6, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 418
    new-instance p2, Leob;

    .line 420
    const/16 v0, 0xc

    .line 422
    invoke-direct {p2, p3, p0, v0}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 425
    invoke-virtual {p1, v5, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 428
    iget-object p0, p1, Lyo;->a:Lvo;

    .line 430
    iput-boolean v8, p0, Lvo;->n:Z

    .line 432
    invoke-virtual {p1}, Lyo;->a()Lzo;

    .line 435
    move-result-object p0

    .line 436
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 439
    return v8

    .line 440
    :cond_1b9
    instance-of v2, p1, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;

    .line 442
    const/4 v9, 0x0

    .line 443
    if-eqz v2, :cond_21f

    .line 445
    :try_start_1be
    move-object v2, p1

    .line 446
    check-cast v2, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;

    .line 448
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;->h0()Ljava/lang/String;

    .line 451
    move-result-object v2

    .line 452
    move-object v10, p1

    .line 453
    check-cast v10, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;

    .line 455
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;->j0()Ljava/lang/String;

    .line 458
    move-result-object v10

    .line 459
    if-eqz v2, :cond_1d9

    .line 461
    invoke-static {v2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 464
    move-result-object v2

    .line 465
    invoke-static {p0, v2}, Lzr4;->j(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 468
    move-result-object v2

    .line 469
    goto :goto_1db

    .line 470
    :catch_1d7
    move-exception v0

    .line 471
    goto :goto_21a

    .line 472
    :cond_1d9
    move-object v2, v9

    move-object v2, v9

    .line 473
    :goto_1db
    if-eqz v10, :cond_1e6

    .line 475
    invoke-static {v10}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 478
    move-result-object v10

    .line 479
    invoke-static {p0, v10}, Lzr4;->j(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 482
    move-result-object v10

    .line 483
    goto :goto_1e7

    .line 484
    :cond_1e6
    move-object v10, v9

    .line 485
    :goto_1e7
    if-eqz v2, :cond_1f5

    .line 487
    invoke-virtual {v2}, Lzr4;->a()Z

    .line 490
    move-result v11

    .line 491
    if-eqz v11, :cond_1fd

    .line 493
    invoke-virtual {v2}, Lzr4;->b()Z

    .line 496
    move-result v2

    .line 497
    if-eqz v2, :cond_1fd

    .line 499
    :cond_1f5
    if-eqz v10, :cond_21f

    .line 501
    invoke-virtual {v10}, Lzr4;->b()Z

    .line 504
    move-result v2

    .line 505
    if-nez v2, :cond_21f

    .line 507
    :cond_1fd
    new-instance v2, Ljava/lang/StringBuilder;

    .line 509
    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 512
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 515
    move-result-object v0

    .line 516
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 519
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 522
    move-result-object v0

    .line 523
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 526
    move-result-object v2

    .line 527
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/macro/Macro;->getId()I

    .line 530
    move-result v2

    .line 531
    int-to-long v10, v2

    .line 532
    invoke-static {v10, v11, v0}, Lkjf;->g(JLjava/lang/String;)V
    :try_end_219
    .catch Ljava/lang/Exception; {:try_start_1be .. :try_end_219} :catch_1d7

    .line 535
    goto :goto_21f

    .line 536
    :goto_21a
    const-string v2, "Error checking for file access requirement: "

    .line 538
    invoke-static {v2, v0}, Lku1;->A(Ljava/lang/String;Ljava/lang/Exception;)V

    .line 541
    :cond_21f
    :goto_21f
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDefaultAssist()Z

    .line 544
    move-result v0

    .line 545
    if-eqz v0, :cond_23f

    .line 547
    sget-object v0, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 549
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 552
    move-result-object v0

    .line 553
    const-string v2, "ignore_default_assist_warning"

    .line 555
    invoke-interface {v0, v2, v8}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 558
    move-result v0

    .line 559
    if-nez v0, :cond_23f

    .line 561
    invoke-static {p0}, Lgi0;->d(Landroid/content/Context;)Z

    .line 564
    move-result v0

    .line 565
    if-nez v0, :cond_23f

    .line 567
    if-eqz p2, :cond_23e

    .line 569
    invoke-static {p0, p3}, Llob;->m(Landroid/app/Activity;Z)V

    .line 572
    :cond_23e
    :goto_23e
    return v8

    .line 573
    :cond_23f
    invoke-static {v3}, Lgi0;->b(Ljava/lang/String;)I

    .line 576
    move-result p2

    .line 577
    const-string v0, "odscamslaomitvrioe.nnrceprlioechdttoo..rcy"

    const-string v0, "com.arlosoft.macrodroid.connectivityhelper"

    .line 579
    invoke-static {v0}, Lgi0;->b(Ljava/lang/String;)I

    .line 582
    move-result v0

    .line 583
    invoke-virtual {p1, p2, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFile(II)Z

    .line 586
    move-result p2

    .line 587
    if-eqz p2, :cond_263

    .line 589
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->allowConfigurationWithoutHelperFile()Z

    .line 592
    move-result p2

    .line 593
    if-nez p2, :cond_263

    .line 595
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 598
    move-result-object p2

    .line 599
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseShizukuAsHelperAlternative()Z

    .line 602
    move-result p1

    .line 603
    invoke-static {p0, p3, p2, v9, p1}, Llob;->t(Landroid/app/Activity;ZLjava/lang/String;Ljava/lang/String;Z)V

    .line 606
    return v8

    .line 607
    :cond_263
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresFineLocationPermission()Z

    .line 610
    move-result p2

    .line 611
    if-eqz p2, :cond_277

    .line 613
    const-string p2, "p_omNCe.O_NImSdSsAEaCFTAinI.sdiLrCOEoin"

    const-string p2, "android.permission.ACCESS_FINE_LOCATION"

    .line 615
    invoke-static {p0, p2}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 618
    move-result p2

    .line 619
    if-eqz p2, :cond_277

    .line 621
    invoke-static {p0, p1}, Llob;->p(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 624
    return v8

    .line 625
    :cond_277
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresFineLocationPermission()Z

    .line 628
    move-result p2

    .line 629
    if-eqz p2, :cond_28b

    .line 631
    const-string p2, "AsSroCOiCNoSaAni.OnsEmI_idp.Ce_OoLEACTSRd"

    const-string p2, "android.permission.ACCESS_COARSE_LOCATION"

    .line 633
    invoke-static {p0, p2}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 636
    move-result p2

    .line 637
    if-eqz p2, :cond_28b

    .line 639
    invoke-static {p0, p1}, Llob;->p(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 642
    return v8

    .line 643
    :cond_28b
    const-string p2, "alarm"

    .line 645
    invoke-virtual {p0, p2}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 648
    move-result-object p2

    .line 649
    check-cast p2, Landroid/app/AlarmManager;

    .line 651
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresScheduleExactAlarm()Z

    .line 654
    move-result v0

    .line 655
    if-eqz v0, :cond_2cc

    .line 657
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 659
    const/16 v2, 0x1f

    .line 661
    if-lt v0, v2, :cond_2cc

    .line 663
    invoke-virtual {p2}, Landroid/app/AlarmManager;->canScheduleExactAlarms()Z

    .line 666
    move-result p2

    .line 667
    if-nez p2, :cond_2cc

    .line 669
    const p1, 0x7f141194

    .line 672
    invoke-static {p0, v7, v4, p1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 675
    move-result-object p1

    .line 676
    new-instance p2, Lzh;

    .line 678
    const/16 v0, 0x10

    .line 680
    invoke-direct {p2, v0, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 683
    invoke-virtual {p1, v6, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 686
    new-instance p2, Leob;

    .line 688
    const/16 v0, 0xb

    .line 690
    invoke-direct {p2, p3, p0, v0}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 693
    invoke-virtual {p1, v5, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 696
    iget-object p0, p1, Lyo;->a:Lvo;

    .line 698
    iput-boolean v8, p0, Lvo;->n:Z

    .line 700
    invoke-virtual {p1}, Lyo;->a()Lzo;

    .line 703
    move-result-object p0

    .line 704
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 707
    return v8

    .line 708
    :cond_2cc
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanShowBubbles()Z

    .line 711
    move-result p2

    .line 712
    if-eqz p2, :cond_2fd

    .line 714
    sget p2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 716
    const/16 v0, 0x1d

    .line 718
    if-lt p2, v0, :cond_2fd

    .line 720
    :try_start_2d8
    invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 723
    move-result-object p2

    .line 724
    const-string v0, "notification_bubbles"

    .line 726
    invoke-static {p2, v0}, Landroid/provider/Settings$Global;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 729
    move-result p2
    :try_end_2e2
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_2d8 .. :try_end_2e2} :catch_2e7

    .line 730
    if-ne p2, v1, :cond_2e5

    .line 732
    goto :goto_2e7

    .line 733
    :cond_2e5
    move p2, v8

    .line 734
    goto :goto_2e8

    .line 735
    :catch_2e7
    :goto_2e7
    move p2, v1

    .line 736
    :goto_2e8
    const-class v0, Landroid/app/NotificationManager;

    .line 738
    invoke-virtual {p0, v0}, Landroid/content/Context;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    .line 741
    move-result-object v0

    .line 742
    check-cast v0, Landroid/app/NotificationManager;

    .line 744
    if-eqz p2, :cond_2f9

    .line 746
    invoke-virtual {v0}, Landroid/app/NotificationManager;->areBubblesAllowed()Z

    .line 749
    move-result p2

    .line 750
    if-eqz p2, :cond_2f9

    .line 752
    goto :goto_2fd

    .line 753
    :cond_2f9
    invoke-static {p0, p3}, Llob;->k(Landroid/app/Activity;Z)V

    .line 756
    return v8

    .line 757
    :cond_2fd
    :goto_2fd
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresShizuku()Z

    .line 760
    move-result p1

    .line 761
    if-eqz p1, :cond_343

    .line 763
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 766
    move-result-object p1

    .line 767
    iget-object p1, p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->n:Ldje;

    .line 769
    invoke-virtual {p1, v8}, Ldje;->c(Z)Ljje;

    .line 772
    move-result-object p1

    .line 773
    sget-object p2, Ljje;->GRANTED:Ljje;

    .line 775
    if-eq p1, p2, :cond_343

    .line 777
    sget-object p2, Ljje;->VERSION_NOT_SUPPORTED:Ljje;

    .line 779
    if-ne p1, p2, :cond_31d

    .line 781
    const p1, 0x7f14141b

    .line 784
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 787
    move-result-object p1

    .line 788
    goto :goto_33c

    .line 789
    :cond_31d
    sget-object p2, Ljje;->NOT_INSTALLED:Ljje;

    .line 791
    if-ne p1, p2, :cond_329

    .line 793
    const p1, 0x7f141417

    .line 796
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 799
    move-result-object p1

    .line 800
    goto :goto_33c

    .line 801
    :cond_329
    sget-object p2, Ljje;->NOT_RUNNING:Ljje;

    .line 803
    if-ne p1, p2, :cond_335

    .line 805
    const p1, 0x7f141418

    .line 808
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 811
    move-result-object p1

    .line 812
    goto :goto_33c

    .line 813
    :cond_335
    const p1, 0x7f141416

    .line 816
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 819
    move-result-object p1

    .line 820
    :goto_33c
    invoke-static {p0, p1, v1}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 823
    move-result-object p0

    .line 824
    invoke-virtual {p0}, Le3g;->show()V

    .line 827
    :cond_343
    :goto_343
    return v1
.end method

.method public static d()Ljava/lang/String;
    .locals 6

    .line 1
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 4
    move-result-object v0

    .line 5
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->getResources()Landroid/content/res/Resources;

    .line 8
    move-result-object v0

    .line 9
    invoke-virtual {v0}, Landroid/content/res/Resources;->getConfiguration()Landroid/content/res/Configuration;

    .line 12
    move-result-object v0

    .line 13
    const/4 v5, 0x3

    iget-object v0, v0, Landroid/content/res/Configuration;->locale:Ljava/util/Locale;

    .line 15
    const/4 v5, 0x1

    invoke-virtual {v0}, Ljava/util/Locale;->getLanguage()Ljava/lang/String;

    .line 18
    move-result-object v0

    .line 19
    const/4 v5, 0x1

    sget-object v1, Llob;->c:[Ljava/lang/String;

    .line 21
    array-length v2, v1

    .line 22
    const/4 v5, 0x4

    const/4 v3, 0x0

    .line 23
    :goto_1a
    if-ge v3, v2, :cond_31

    .line 25
    aget-object v4, v1, v3

    .line 27
    invoke-virtual {v4, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 30
    move-result v4

    .line 31
    const/4 v5, 0x4

    if-eqz v4, :cond_2e

    .line 33
    const-string v1, "https://wiki.macrodroid.com/wiki/index.php/Helper_App_("

    .line 35
    const-string v2, ")"

    .line 37
    invoke-static {v1, v0, v2}, Lbl5;->t(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 40
    move-result-object v0

    .line 41
    return-object v0

    .line 42
    :cond_2e
    add-int/lit8 v3, v3, 0x1

    .line 44
    goto :goto_1a

    .line 45
    :cond_31
    const/4 v5, 0x6

    const-string v0, "https://wiki.macrodroid.com/wiki/index.php/Helper_App"

    .line 47
    return-object v0
.end method

.method public static e(Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .line 1
    const-string v0, "."

    .line 3
    const/4 v2, 0x2

    invoke-virtual {p0, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 6
    move-result v1

    .line 7
    if-eqz v1, :cond_14

    .line 9
    invoke-virtual {p0, v0}, Ljava/lang/String;->lastIndexOf(Ljava/lang/String;)I

    .line 12
    move-result v0

    .line 13
    const/4 v2, 0x5

    add-int/lit8 v0, v0, 0x1

    .line 15
    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    .line 18
    move-result-object p0

    .line 19
    :cond_14
    return-object p0
.end method

.method public static f(Landroid/content/Context;Lcom/arlosoft/macrodroid/common/SelectableItem;)Z
    .locals 8

    .line 1
    const/4 v0, 0x0

    .line 2
    if-eqz p0, :cond_1c5

    .line 4
    if-nez p1, :cond_7

    .line 6
    goto/16 :goto_1c5

    .line 8
    :cond_7
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getRequiredPermissions()[Ljava/lang/String;

    .line 11
    move-result-object v1

    .line 12
    const/4 v2, 0x1

    .line 13
    const/4 v7, 0x3

    if-eqz v1, :cond_22

    .line 15
    array-length v3, v1

    .line 16
    move v4, v0

    .line 17
    :goto_11
    if-ge v4, v3, :cond_22

    .line 19
    aget-object v5, v1, v4

    .line 21
    const/4 v7, 0x1

    invoke-static {p0, v5}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 24
    move-result v5

    .line 25
    if-eqz v5, :cond_1f

    .line 27
    const/4 v7, 0x3

    goto/16 :goto_1c3

    .line 29
    :cond_1f
    add-int/lit8 v4, v4, 0x1

    .line 31
    goto :goto_11

    .line 32
    :cond_22
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 34
    const/16 v3, 0x1e

    .line 36
    if-lt v1, v3, :cond_3a

    .line 38
    const/4 v7, 0x6

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAllFilesAccess()Z

    .line 41
    move-result v3

    .line 42
    const/4 v7, 0x4

    if-eqz v3, :cond_3a

    .line 44
    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    .line 47
    move-result v3

    .line 48
    const/4 v7, 0x2

    if-nez v3, :cond_3a

    .line 50
    const/4 v7, 0x7

    goto/16 :goto_1c3

    .line 52
    :cond_3a
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresWriteSettings()Z

    .line 55
    move-result v3

    .line 56
    if-eqz v3, :cond_48

    .line 58
    invoke-static {p0}, Landroid/provider/Settings$System;->canWrite(Landroid/content/Context;)Z

    .line 61
    move-result v3

    .line 62
    if-nez v3, :cond_48

    .line 64
    goto/16 :goto_1c3

    .line 66
    :cond_48
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanDrawOverlays()Z

    .line 69
    move-result v3

    .line 70
    if-eqz v3, :cond_57

    .line 72
    invoke-static {p0}, Llob;->a(Landroid/content/Context;)Z

    .line 75
    move-result v3

    .line 76
    const/4 v7, 0x6

    if-nez v3, :cond_57

    .line 78
    goto/16 :goto_1c3

    .line 80
    :cond_57
    const/4 v7, 0x4

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessNotificationPolicy()Z

    .line 83
    move-result v3

    .line 84
    const/4 v7, 0x4

    if-eqz v3, :cond_73

    .line 86
    const-string v3, "notification"

    .line 88
    const/4 v7, 0x4

    invoke-virtual {p0, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 91
    move-result-object v3

    .line 92
    check-cast v3, Landroid/app/NotificationManager;

    .line 94
    if-eqz v3, :cond_73

    .line 96
    invoke-virtual {v3}, Landroid/app/NotificationManager;->isNotificationPolicyAccessGranted()Z

    .line 99
    move-result v3

    .line 100
    const/4 v7, 0x3

    if-nez v3, :cond_73

    .line 102
    goto/16 :goto_1c3

    .line 104
    :cond_73
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNotificationsEnabled()Z

    .line 107
    move-result v3

    .line 108
    const/4 v7, 0x5

    if-eqz v3, :cond_89

    .line 110
    const/4 v7, 0x2

    new-instance v3, Liwa;

    .line 112
    invoke-direct {v3, p0}, Liwa;-><init>(Landroid/content/Context;)V

    .line 115
    invoke-virtual {v3}, Liwa;->a()Z

    .line 118
    move-result v3

    .line 119
    const/4 v7, 0x7

    if-nez v3, :cond_89

    .line 121
    goto/16 :goto_1c3

    .line 123
    :cond_89
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUsageAccess()Z

    .line 126
    move-result v3

    .line 127
    const/4 v7, 0x3

    if-eqz v3, :cond_b9

    .line 129
    :try_start_90
    const/4 v7, 0x7

    invoke-virtual {p0}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 132
    move-result-object v3

    .line 133
    const/4 v7, 0x1

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 136
    move-result-object v4

    .line 137
    const/4 v7, 0x0

    invoke-virtual {v3, v4, v0}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;I)Landroid/content/pm/ApplicationInfo;

    .line 140
    move-result-object v3

    .line 141
    const/4 v7, 0x2

    const-string v4, "appops"

    .line 143
    invoke-virtual {p0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 146
    move-result-object v4

    .line 147
    check-cast v4, Landroid/app/AppOpsManager;

    .line 149
    const-string v5, "android:get_usage_stats"

    .line 151
    iget v6, v3, Landroid/content/pm/ApplicationInfo;->uid:I

    .line 153
    iget-object v3, v3, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    .line 155
    const/4 v7, 0x3

    invoke-virtual {v4, v5, v6, v3}, Landroid/app/AppOpsManager;->checkOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 158
    move-result v3
    :try_end_b3
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_90 .. :try_end_b3} :catch_1c3

    .line 159
    const/4 v7, 0x7

    if-eqz v3, :cond_b9

    .line 161
    const/4 v7, 0x2

    goto/16 :goto_1c3

    .line 163
    :cond_b9
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessibility()Z

    .line 166
    move-result v3

    .line 167
    const/4 v7, 0x3

    if-eqz v3, :cond_c9

    .line 169
    invoke-static {p0}, Lhtg;->I(Landroid/content/Context;)Z

    .line 172
    move-result v3

    .line 173
    if-nez v3, :cond_c9

    .line 175
    const/4 v7, 0x4

    goto/16 :goto_1c3

    .line 177
    :cond_c9
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUIInteractionAccessibility()Z

    .line 180
    move-result v3

    .line 181
    const/4 v7, 0x0

    if-eqz v3, :cond_d8

    .line 183
    invoke-static {p0}, Lhtg;->J(Landroid/content/Context;)Z

    .line 186
    move-result v3

    .line 187
    if-nez v3, :cond_d8

    .line 189
    goto/16 :goto_1c3

    .line 191
    :cond_d8
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDeviceAdmin()Z

    .line 194
    move-result v3

    .line 195
    if-eqz v3, :cond_f9

    .line 197
    new-instance v3, Landroid/content/ComponentName;

    .line 199
    const-class v4, Lcom/arlosoft/macrodroid/triggers/receivers/MacroDroidDeviceAdminReceiver;

    .line 201
    invoke-direct {v3, p0, v4}, Landroid/content/ComponentName;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 204
    const-string v4, "device_policy"

    .line 206
    invoke-virtual {p0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 209
    move-result-object v4

    .line 210
    const/4 v7, 0x4

    check-cast v4, Landroid/app/admin/DevicePolicyManager;

    .line 212
    if-eqz v4, :cond_f9

    .line 214
    invoke-virtual {v4, v3}, Landroid/app/admin/DevicePolicyManager;->isAdminActive(Landroid/content/ComponentName;)Z

    .line 217
    move-result v3

    .line 218
    if-nez v3, :cond_f9

    .line 220
    const/4 v7, 0x3

    goto/16 :goto_1c3

    .line 222
    :cond_f9
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNotificationAccess()Z

    .line 225
    move-result v3

    .line 226
    const/4 v7, 0x0

    if-eqz v3, :cond_11e

    .line 228
    invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 231
    move-result-object v3

    .line 232
    const-string v4, "enabled_notification_listeners"

    .line 234
    invoke-static {v3, v4}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    .line 237
    move-result-object v3

    .line 238
    const/4 v7, 0x5

    if-eqz v3, :cond_1c3

    .line 240
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 243
    move-result-object v4

    .line 244
    invoke-virtual {v4}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 247
    move-result-object v4

    .line 248
    invoke-virtual {v3, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 251
    move-result v3

    .line 252
    const/4 v7, 0x2

    if-nez v3, :cond_11e

    .line 254
    goto/16 :goto_1c3

    .line 256
    :cond_11e
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDefaultAssist()Z

    .line 259
    move-result v3

    .line 260
    if-eqz v3, :cond_13e

    .line 262
    sget-object v3, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 264
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 267
    move-result-object v3

    .line 268
    const/4 v7, 0x1

    const-string v4, "idaf_be_arstgulsrose_nngainwt"

    const-string v4, "ignore_default_assist_warning"

    .line 270
    invoke-interface {v3, v4, v0}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 273
    move-result v3

    .line 274
    if-nez v3, :cond_13e

    .line 276
    invoke-static {p0}, Lgi0;->d(Landroid/content/Context;)Z

    .line 279
    move-result v3

    .line 280
    if-nez v3, :cond_13e

    .line 282
    const/4 v7, 0x3

    goto/16 :goto_1c3

    .line 284
    :cond_13e
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresFineLocationPermission()Z

    .line 287
    move-result v3

    .line 288
    if-eqz v3, :cond_15a

    .line 290
    const-string v3, "F_nNSnuioiArSEATIoIEeCdOdmpLrCaC_s..iNs"

    const-string v3, "android.permission.ACCESS_FINE_LOCATION"

    .line 292
    const/4 v7, 0x2

    invoke-static {p0, v3}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 295
    move-result v3

    .line 296
    const/4 v7, 0x7

    if-eqz v3, :cond_15a

    .line 298
    const-string v3, "android.permission.ACCESS_COARSE_LOCATION"

    .line 300
    invoke-static {p0, v3}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 303
    move-result v3

    .line 304
    const/4 v7, 0x1

    if-eqz v3, :cond_15a

    .line 306
    goto :goto_1c3

    .line 307
    :cond_15a
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresScheduleExactAlarm()Z

    .line 310
    move-result v3

    .line 311
    const/4 v7, 0x2

    if-eqz v3, :cond_177

    .line 313
    const/16 v3, 0x1f

    .line 315
    if-lt v1, v3, :cond_177

    .line 317
    const-string v3, "alarm"

    .line 319
    invoke-virtual {p0, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 322
    move-result-object v3

    .line 323
    const/4 v7, 0x2

    check-cast v3, Landroid/app/AlarmManager;

    .line 325
    if-eqz v3, :cond_177

    .line 327
    invoke-virtual {v3}, Landroid/app/AlarmManager;->canScheduleExactAlarms()Z

    .line 330
    move-result v3

    .line 331
    if-nez v3, :cond_177

    .line 333
    goto :goto_1c3

    .line 334
    :cond_177
    const/4 v7, 0x5

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanShowBubbles()Z

    .line 337
    move-result v3

    .line 338
    const/4 v7, 0x2

    if-eqz v3, :cond_1ad

    .line 340
    const/16 v3, 0x1d

    .line 342
    const/4 v7, 0x5

    if-lt v1, v3, :cond_1ad

    .line 344
    :try_start_184
    invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 347
    move-result-object v1

    .line 348
    const/4 v7, 0x6

    const-string v3, "_seultnpfibanbbtcoii"

    const-string v3, "notification_bubbles"

    .line 350
    invoke-static {v1, v3}, Landroid/provider/Settings$Global;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 353
    move-result v1
    :try_end_191
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_184 .. :try_end_191} :catch_197

    .line 354
    if-ne v1, v2, :cond_195

    .line 356
    const/4 v7, 0x2

    goto :goto_197

    .line 357
    :cond_195
    move v1, v0

    .line 358
    goto :goto_198

    .line 359
    :catch_197
    :goto_197
    move v1, v2

    .line 360
    :goto_198
    const-class v3, Landroid/app/NotificationManager;

    .line 362
    invoke-virtual {p0, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    .line 365
    move-result-object p0

    .line 366
    const/4 v7, 0x6

    check-cast p0, Landroid/app/NotificationManager;

    .line 368
    if-eqz v1, :cond_1c3

    .line 370
    if-eqz p0, :cond_1c3

    .line 372
    const/4 v7, 0x3

    invoke-virtual {p0}, Landroid/app/NotificationManager;->areBubblesAllowed()Z

    .line 375
    move-result p0

    .line 376
    const/4 v7, 0x7

    if-eqz p0, :cond_1c3

    .line 378
    :cond_1ad
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresShizuku()Z

    .line 381
    move-result p0

    .line 382
    const/4 v7, 0x6

    if-eqz p0, :cond_1c5

    .line 384
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 387
    move-result-object p0

    .line 388
    iget-object p0, p0, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->n:Ldje;

    .line 390
    invoke-virtual {p0, v0}, Ldje;->c(Z)Ljje;

    .line 393
    move-result-object p0

    .line 394
    const/4 v7, 0x2

    sget-object p1, Ljje;->GRANTED:Ljje;

    .line 396
    if-eq p0, p1, :cond_1c5

    .line 398
    :catch_1c3
    :cond_1c3
    :goto_1c3
    const/4 v7, 0x6

    return v2

    .line 399
    :cond_1c5
    :goto_1c5
    return v0
.end method

.method public static g(Landroid/app/Activity;)V
    .locals 4

    .line 1
    :try_start_0
    new-instance v0, Landroid/content/Intent;

    .line 3
    const-string v1, "android.settings.APP_NOTIFICATION_SETTINGS"

    .line 5
    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 8
    const-string v1, "Adixidenq_PtKeoApPrardvrEoaC.rG.AP"

    const-string v1, "android.provider.extra.APP_PACKAGE"

    .line 10
    const/4 v3, 0x7

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 13
    move-result-object v2

    .line 14
    const/4 v3, 0x1

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 17
    move-result-object v0

    .line 18
    invoke-virtual {p0, v0}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_18
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_18} :catch_19

    .line 21
    return-void

    .line 22
    :catch_19
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 25
    move-result-object p0

    .line 26
    const/4 v3, 0x4

    const-string v0, "FSssoh_Ti.NCtsT EdAdINde AninToOetoivitsnoPcdpP u.STOp IeGetIgars rnt_N"

    const-string v0, "android.settings.APP_NOTIFICATION_SETTINGS not supported on this device"

    .line 28
    const/4 v3, 0x6

    const/4 v1, 0x1

    .line 29
    const/4 v3, 0x0

    invoke-static {p0, v0, v1}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 32
    move-result-object p0

    .line 33
    invoke-virtual {p0}, Le3g;->show()V

    .line 36
    return-void
.end method

.method public static h(Landroid/app/Activity;[Ljava/lang/String;Lqk5;)V
    .locals 4

    .line 1
    array-length v0, p1

    .line 2
    const/4 v1, 0x3

    const/4 v1, 0x0

    .line 3
    :goto_3
    if-ge v1, v0, :cond_23

    .line 5
    aget-object v2, p1, v1

    .line 7
    invoke-static {p0, v2}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 10
    move-result v2

    .line 11
    if-eqz v2, :cond_20

    .line 13
    const v0, 0x7f140e7f

    .line 16
    const/4 v3, 0x1

    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 19
    move-result-object v0

    .line 20
    new-instance v1, Lm16;

    .line 22
    const/16 v2, 0x12

    .line 24
    invoke-direct {v1, p0, p1, p2, v2}, Lm16;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 27
    invoke-static {p0, v0, v1}, Llob;->o(Landroid/app/Activity;Ljava/lang/String;Ljava/lang/Runnable;)V

    .line 30
    return-void

    .line 31
    :cond_20
    add-int/lit8 v1, v1, 0x1

    .line 33
    goto :goto_3

    .line 34
    :cond_23
    invoke-interface {p2}, Lqk5;->g0()V

    .line 37
    return-void
.end method

.method public static i(Landroid/app/Activity;ZZZ)V
    .locals 7

    .line 1
    invoke-static {p0}, Lai;->a(Landroid/content/Context;)Z

    .line 4
    move-result v0

    .line 5
    const/4 v6, 0x0

    new-instance v1, Lyo;

    .line 7
    const v2, 0x7f150337

    .line 10
    const/4 v6, 0x0

    invoke-direct {v1, p0, v2}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 13
    const v2, 0x7f140022

    .line 16
    invoke-virtual {v1, v2}, Lyo;->k(I)Lyo;

    .line 19
    iget-object v2, v1, Lyo;->a:Lvo;

    .line 21
    const/4 v6, 0x3

    if-eqz v0, :cond_20

    .line 23
    const p2, 0x7f140468

    .line 26
    invoke-virtual {v1, p2}, Lyo;->c(I)Lyo;

    .line 29
    goto :goto_88

    .line 30
    :cond_20
    const-string v3, "\n\n"

    .line 32
    if-eqz p2, :cond_62

    .line 34
    const p2, 0x7f14002a

    .line 37
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 40
    move-result-object p2

    .line 41
    invoke-static {p2, v3}, Lx9f;->I(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 44
    move-result-object p2

    .line 45
    const v4, 0x7f140024

    .line 48
    const/4 v6, 0x0

    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 51
    move-result-object v4

    .line 52
    const/4 v6, 0x5

    invoke-virtual {p2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 55
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 58
    move-result-object p2

    .line 59
    sget-object v4, Landroid/os/Build;->MANUFACTURER:Ljava/lang/String;

    .line 61
    const-string/jumbo v5, "xiaomi"

    .line 63
    invoke-virtual {v4, v5}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    .line 66
    move-result v4

    .line 67
    const/4 v6, 0x6

    if-eqz v4, :cond_5e

    .line 69
    invoke-static {p2, v3}, Lbl5;->x(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 72
    move-result-object p2

    .line 73
    const/4 v6, 0x0

    const v3, 0x7f141a2d

    .line 76
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 79
    move-result-object v3

    .line 80
    invoke-virtual {p2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 83
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 86
    move-result-object p2

    .line 87
    :cond_5e
    iput-object p2, v2, Lvo;->g:Ljava/lang/CharSequence;

    .line 89
    const/4 v6, 0x4

    goto :goto_88

    .line 90
    :cond_62
    new-instance p2, Ljava/lang/StringBuilder;

    .line 92
    const/4 v6, 0x2

    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    .line 95
    const/4 v6, 0x7

    const v4, 0x7f140021

    .line 98
    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 101
    move-result-object v4

    .line 102
    invoke-virtual {p2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 105
    invoke-virtual {p2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 108
    const v3, 0x7f140023

    .line 111
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 114
    move-result-object v3

    .line 115
    invoke-virtual {p2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 118
    const/4 v6, 0x6

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 121
    move-result-object p2

    .line 122
    const/4 v6, 0x6

    iput-object p2, v2, Lvo;->g:Ljava/lang/CharSequence;

    .line 124
    :goto_88
    new-instance p2, Lfob;

    .line 126
    invoke-direct {p2, p0, v0, p1}, Lfob;-><init>(Landroid/app/Activity;ZZ)V

    .line 129
    const/4 v6, 0x6

    const p1, 0x104000a

    .line 132
    invoke-virtual {v1, p1, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 135
    const/4 v6, 0x6

    new-instance p1, Leob;

    .line 137
    const/16 p2, 0x8

    .line 139
    const/4 v6, 0x5

    invoke-direct {p1, p3, p0, p2}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 142
    const/high16 p0, 0x1040000

    .line 144
    invoke-virtual {v1, p0, p1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 147
    const/4 p0, 0x0

    .line 148
    iput-boolean p0, v2, Lvo;->n:Z

    .line 150
    invoke-virtual {v1}, Lyo;->o()Lzo;

    .line 153
    move-result-object p0

    .line 154
    const/4 v6, 0x0

    new-instance p1, Landroid/view/WindowManager$LayoutParams;

    .line 156
    invoke-direct {p1}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 159
    invoke-virtual {p0}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    .line 162
    move-result-object p2

    .line 163
    invoke-virtual {p2}, Landroid/view/Window;->getAttributes()Landroid/view/WindowManager$LayoutParams;

    .line 166
    move-result-object p2

    .line 167
    invoke-virtual {p1, p2}, Landroid/view/WindowManager$LayoutParams;->copyFrom(Landroid/view/WindowManager$LayoutParams;)I

    .line 170
    const/4 p2, -0x1

    move v6, p2

    .line 171
    iput p2, p1, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 173
    const/4 v6, 0x0

    invoke-virtual {p0}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    .line 176
    move-result-object p0

    .line 177
    const/4 v6, 0x7

    invoke-virtual {p0, p1}, Landroid/view/Window;->setAttributes(Landroid/view/WindowManager$LayoutParams;)V

    .line 180
    return-void
.end method

.method public static j(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;)V
    .locals 4

    .line 1
    const-string v0, "package:"

    .line 3
    const-string v1, "android.permission.ACCESS_BACKGROUND_LOCATION"

    .line 5
    const/4 v3, 0x6

    invoke-static {p0, v1}, Lpd;->b(Landroid/app/Activity;Ljava/lang/String;)Z

    .line 8
    move-result v2

    .line 9
    const/4 v3, 0x1

    if-eqz v2, :cond_17

    .line 11
    new-instance v0, Ljm3;

    .line 13
    const/16 v2, 0x18

    .line 15
    invoke-direct {v0, p1, v2}, Ljm3;-><init>(Ljava/lang/Object;I)V

    .line 18
    invoke-static {p0, v1, v0}, Lrk5;->a(Landroid/app/Activity;Ljava/lang/String;Lqk5;)V

    .line 21
    return-void

    .line 22
    :cond_17
    const/4 p1, 0x1

    .line 23
    :try_start_18
    new-instance v1, Landroid/content/Intent;

    .line 25
    const/4 v3, 0x1

    const-string v2, "SAAm.LgSPNaiAtd.dGiIsIsSLtTPEIoT_nDCe_NTTrnEI"

    const-string v2, "android.settings.APPLICATION_DETAILS_SETTINGS"

    .line 27
    const/4 v3, 0x5

    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 30
    new-instance v2, Ljava/lang/StringBuilder;

    .line 32
    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 35
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 38
    move-result-object v0

    .line 39
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 42
    const/4 v3, 0x1

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 45
    move-result-object v0

    .line 46
    invoke-static {v0}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 49
    move-result-object v0

    .line 50
    invoke-virtual {v1, v0}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;

    .line 53
    invoke-virtual {p0, v1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    .line 56
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 59
    move-result-object v0

    .line 60
    const v1, 0x7f14108e

    .line 63
    const/4 v3, 0x0

    invoke-static {v0, v1, p1}, Le3g;->a(Landroid/content/Context;II)Le3g;

    .line 66
    move-result-object v0

    .line 67
    const/4 v3, 0x3

    invoke-virtual {v0}, Le3g;->show()V
    :try_end_4e
    .catch Landroid/content/ActivityNotFoundException; {:try_start_18 .. :try_end_4e} :catch_4f

    .line 70
    return-void

    .line 71
    :catch_4f
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 74
    move-result-object p0

    .line 75
    const-string v0, "android.settings.APPLICATION_DETAILS_SETTINGS not supported on this device"

    .line 77
    invoke-static {p0, v0, p1}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 80
    move-result-object p0

    .line 81
    invoke-virtual {p0}, Le3g;->show()V

    .line 84
    return-void
.end method

.method public static k(Landroid/app/Activity;Z)V
    .locals 4

    .line 1
    const v0, 0x7f140083

    .line 4
    const v1, 0x7f140084

    .line 7
    const/4 v3, 0x3

    const v2, 0x7f150337

    .line 10
    invoke-static {p0, v2, v0, v1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 13
    move-result-object v0

    .line 14
    new-instance v1, Lzh;

    .line 16
    const/4 v3, 0x6

    const/4 v2, 0x6

    .line 17
    invoke-direct {v1, v2, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 20
    const v2, 0x104000a

    .line 23
    invoke-virtual {v0, v2, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 26
    const/4 v3, 0x0

    new-instance v1, Leob;

    .line 28
    const/4 v2, 0x5

    .line 29
    const/4 v3, 0x7

    invoke-direct {v1, p1, p0, v2}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 32
    const/high16 p0, 0x1040000

    .line 34
    invoke-virtual {v0, p0, v1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 37
    const/4 p0, 0x0

    .line 38
    iget-object p1, v0, Lyo;->a:Lvo;

    .line 40
    iput-boolean p0, p1, Lvo;->n:Z

    .line 42
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 45
    move-result-object p0

    .line 46
    const/4 v3, 0x4

    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 49
    return-void
.end method

.method public static l(Landroid/app/Activity;Z)V
    .locals 5

    .line 1
    new-instance v0, Lyo;

    .line 3
    const/4 v4, 0x0

    const v1, 0x7f150337

    .line 6
    invoke-direct {v0, p0, v1}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 9
    const/4 v4, 0x1

    const v1, 0x7f141293

    .line 12
    invoke-virtual {v0, v1}, Lyo;->k(I)Lyo;

    .line 15
    const/4 v4, 0x0

    new-instance v1, Ljava/lang/StringBuilder;

    .line 17
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 20
    const v2, 0x7f141295

    .line 23
    const/4 v4, 0x0

    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 26
    move-result-object v2

    .line 27
    const/4 v4, 0x1

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 30
    const-string v2, "//nn"

    const-string v2, "\n\n"

    .line 32
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 35
    const v2, 0x7f141294

    .line 38
    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 41
    move-result-object v2

    .line 42
    const/4 v4, 0x4

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 45
    const/4 v4, 0x0

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 48
    move-result-object v1

    .line 49
    const/4 v4, 0x1

    iget-object v2, v0, Lyo;->a:Lvo;

    .line 51
    iput-object v1, v2, Lvo;->g:Ljava/lang/CharSequence;

    .line 53
    const/4 v4, 0x1

    new-instance v1, Lzh;

    .line 55
    const/16 v3, 0xc

    .line 57
    invoke-direct {v1, v3, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 60
    const/4 v4, 0x2

    const v3, 0x104000a

    .line 63
    invoke-virtual {v0, v3, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 66
    new-instance v1, Leob;

    .line 68
    const/4 v3, 0x7

    .line 69
    invoke-direct {v1, p1, p0, v3}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 72
    const/4 v4, 0x0

    const/high16 p0, 0x1040000

    .line 74
    invoke-virtual {v0, p0, v1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 77
    const/4 p0, 0x0

    .line 78
    const/4 v4, 0x4

    iput-boolean p0, v2, Lvo;->n:Z

    .line 80
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 83
    move-result-object p0

    .line 84
    const/4 v4, 0x2

    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 87
    const/4 v4, 0x5

    return-void
.end method

.method public static m(Landroid/app/Activity;Z)V
    .locals 6

    .line 1
    const v0, 0x7f0d0210

    .line 4
    const/4 v5, 0x4

    const v1, 0x7f141190

    .line 7
    const v2, 0x7f150337

    .line 10
    invoke-static {p0, v2, v0, v1}, Lhvb;->n(Landroid/app/Activity;III)Lvf0;

    .line 13
    move-result-object v0

    .line 14
    const/4 v5, 0x4

    new-instance v1, Landroid/view/WindowManager$LayoutParams;

    .line 16
    invoke-direct {v1}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 19
    invoke-static {v0, v1}, Lbl5;->A(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 22
    const/4 v2, -0x1

    move v5, v2

    .line 23
    iput v2, v1, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 25
    const v2, 0x7f0a0ca4

    .line 28
    const/4 v5, 0x3

    invoke-static {v0, v1, v2}, Liu1;->i(Lvf0;Landroid/view/WindowManager$LayoutParams;I)Landroid/view/View;

    .line 31
    move-result-object v1

    .line 32
    check-cast v1, Landroid/widget/Button;

    .line 34
    const v2, 0x7f0a0252

    .line 37
    invoke-virtual {v0, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 40
    move-result-object v2

    .line 41
    const/4 v5, 0x4

    check-cast v2, Landroid/widget/Button;

    .line 43
    const/4 v5, 0x2

    const v3, 0x7f0a00f5

    .line 46
    invoke-virtual {v0, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 49
    move-result-object v3

    .line 50
    check-cast v3, Landroid/widget/TextView;

    .line 52
    invoke-virtual {v3}, Landroid/widget/TextView;->getPaintFlags()I

    .line 55
    move-result v4

    .line 56
    or-int/lit8 v4, v4, 0x8

    .line 58
    invoke-virtual {v3, v4}, Landroid/widget/TextView;->setPaintFlags(I)V

    .line 61
    new-instance v4, Lhob;

    .line 63
    invoke-direct {v4, p0, p1, v0}, Lhob;-><init>(Landroid/app/Activity;ZLvf0;)V

    .line 66
    const/4 v5, 0x7

    invoke-virtual {v3, v4}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 69
    new-instance v3, Lzk2;

    .line 71
    const/4 v4, 0x4

    .line 72
    invoke-direct {v3, v4, p0, v0}, Lzk2;-><init>(ILandroid/app/Activity;Ljava/lang/Object;)V

    .line 75
    invoke-virtual {v1, v3}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 78
    const/4 v5, 0x3

    new-instance v1, Lhob;

    .line 80
    const/4 v3, 0x0

    .line 81
    const/4 v5, 0x5

    invoke-direct {v1, v0, p1, p0, v3}, Lhob;-><init>(Lvf0;ZLandroid/app/Activity;I)V

    .line 84
    invoke-virtual {v2, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 87
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 90
    return-void
.end method

.method public static n(Landroid/app/Activity;Landroid/content/ComponentName;ZZ)V
    .locals 11

    .line 1
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 3
    const/16 v1, 0x22

    .line 5
    const/4 v2, 0x1

    .line 6
    if-lt v0, v1, :cond_2a

    .line 8
    :try_start_7
    new-instance p3, Landroid/content/Intent;

    .line 10
    const-string v0, "android.app.action.ADD_DEVICE_ADMIN"

    .line 12
    invoke-direct {p3, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 15
    const-string v0, "android.app.extra.DEVICE_ADMIN"

    .line 17
    invoke-virtual {p3, v0, p1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 20
    invoke-virtual {p0, p3}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_16
    .catch Landroid/content/ActivityNotFoundException; {:try_start_7 .. :try_end_16} :catch_17

    .line 23
    goto :goto_24

    .line 24
    :catch_17
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 27
    move-result-object p1

    .line 28
    const-string p3, "DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN not supported on this device"

    .line 30
    invoke-static {p1, p3, v2}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 33
    move-result-object p1

    .line 34
    invoke-virtual {p1}, Le3g;->show()V

    .line 37
    :goto_24
    if-eqz p2, :cond_29

    .line 39
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 42
    :cond_29
    return-void

    .line 43
    :cond_2a
    const v0, 0x7f0d0211

    .line 46
    const v1, 0x7f14128e

    .line 49
    const v3, 0x7f150337

    .line 52
    invoke-static {p0, v3, v0, v1}, Lhvb;->n(Landroid/app/Activity;III)Lvf0;

    .line 55
    move-result-object v5

    .line 56
    new-instance v0, Landroid/view/WindowManager$LayoutParams;

    .line 58
    invoke-direct {v0}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 61
    invoke-static {v5, v0}, Lbl5;->A(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 64
    const/4 v1, -0x1

    .line 65
    iput v1, v0, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 67
    const v1, 0x7f0a0ca4

    .line 70
    invoke-static {v5, v0, v1}, Liu1;->i(Lvf0;Landroid/view/WindowManager$LayoutParams;I)Landroid/view/View;

    .line 73
    move-result-object v0

    .line 74
    check-cast v0, Landroid/widget/Button;

    .line 76
    const v1, 0x7f0a0252

    .line 79
    invoke-virtual {v5, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 82
    move-result-object v1

    .line 83
    check-cast v1, Landroid/widget/Button;

    .line 85
    const v3, 0x7f0a03cb

    .line 88
    invoke-virtual {v5, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 91
    move-result-object v3

    .line 92
    check-cast v3, Landroid/widget/CheckBox;

    .line 94
    const/4 v10, 0x0

    .line 95
    invoke-virtual {v0, v10}, Landroid/view/View;->setEnabled(Z)V

    .line 98
    new-instance v4, Liob;

    .line 100
    move-object v6, p0

    .line 101
    move-object v7, p1

    move-object v7, p1

    .line 102
    move v8, p2

    .line 103
    move v9, p3

    .line 104
    invoke-direct/range {v4 .. v9}, Liob;-><init>(Lvf0;Landroid/app/Activity;Landroid/content/ComponentName;ZZ)V

    .line 107
    invoke-virtual {v0, v4}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 110
    new-instance p0, Lhob;

    .line 112
    invoke-direct {p0, v5, v9, v6, v2}, Lhob;-><init>(Lvf0;ZLandroid/app/Activity;I)V

    .line 115
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 118
    new-instance p0, Ljob;

    .line 120
    invoke-direct {p0, v10, v0}, Ljob;-><init>(ILandroid/widget/Button;)V

    .line 123
    invoke-virtual {v3, p0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 126
    invoke-virtual {v5}, Landroid/app/Dialog;->show()V

    .line 129
    return-void
.end method

.method public static o(Landroid/app/Activity;Ljava/lang/String;Ljava/lang/Runnable;)V
    .locals 3

    .line 1
    new-instance v0, Lyo;

    .line 3
    const v1, 0x7f150337

    .line 6
    invoke-direct {v0, p0, v1}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 9
    const/4 v2, 0x0

    const p0, 0x7f140e82

    .line 12
    invoke-virtual {v0, p0}, Lyo;->k(I)Lyo;

    .line 15
    const/4 v2, 0x7

    iget-object p0, v0, Lyo;->a:Lvo;

    .line 17
    const/4 v2, 0x1

    iput-object p1, p0, Lvo;->g:Ljava/lang/CharSequence;

    .line 19
    new-instance p1, Lxv7;

    .line 21
    const/16 v1, 0xd

    .line 23
    const/4 v2, 0x3

    invoke-direct {p1, p2, v1}, Lxv7;-><init>(Ljava/lang/Object;I)V

    .line 26
    const p2, 0x104000a

    .line 29
    invoke-virtual {v0, p2, p1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 32
    const/4 v2, 0x6

    const/high16 p1, 0x1040000

    .line 34
    const/4 v2, 0x2

    const/4 p2, 0x0

    .line 35
    invoke-virtual {v0, p1, p2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 38
    const/4 p1, 0x0

    .line 39
    const/4 v2, 0x3

    iput-boolean p1, p0, Lvo;->n:Z

    .line 41
    const/4 v2, 0x0

    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 44
    move-result-object p0

    .line 45
    const/4 v2, 0x4

    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 48
    return-void
.end method

.method public static p(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;)V
    .locals 4

    .line 1
    const v0, 0x7f140e82

    .line 4
    const v1, 0x7f140e7f

    .line 7
    const/4 v3, 0x5

    const v2, 0x7f150337

    .line 10
    invoke-static {p0, v2, v0, v1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 13
    move-result-object v0

    .line 14
    const/4 v3, 0x3

    new-instance v1, Lgob;

    .line 16
    const/4 v2, 0x0

    move v3, v2

    .line 17
    invoke-direct {v1, v2, p1, p0}, Lgob;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 20
    const p1, 0x104000a

    .line 23
    invoke-virtual {v0, p1, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 26
    new-instance p1, Lzh;

    .line 28
    const/16 v1, 0x12

    .line 30
    invoke-direct {p1, v1, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 33
    const/high16 p0, 0x1040000

    .line 35
    invoke-virtual {v0, p0, p1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 38
    iget-object p0, v0, Lyo;->a:Lvo;

    .line 40
    iput-boolean v2, p0, Lvo;->n:Z

    .line 42
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 45
    move-result-object p0

    .line 46
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 49
    return-void
.end method

.method public static q(Landroid/app/Activity;ZZ)V
    .locals 4

    .line 1
    const v0, 0x7f140e84

    .line 4
    const v1, 0x7f140e83

    .line 7
    const v2, 0x7f150337

    .line 10
    invoke-static {p0, v2, v0, v1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 13
    move-result-object v0

    .line 14
    new-instance v1, Leob;

    .line 16
    const/16 v2, 0xd

    .line 18
    const/4 v3, 0x6

    invoke-direct {v1, p0, p1, v2}, Leob;-><init>(Landroid/app/Activity;ZI)V

    .line 21
    const/4 v3, 0x0

    const p1, 0x104000a

    .line 24
    const/4 v3, 0x5

    invoke-virtual {v0, p1, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 27
    new-instance p1, Leob;

    .line 29
    const/4 v1, 0x0

    .line 30
    invoke-direct {p1, p2, p0, v1}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 33
    const/high16 p0, 0x1040000

    .line 35
    invoke-virtual {v0, p0, p1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 38
    const/4 v3, 0x5

    iget-object p0, v0, Lyo;->a:Lvo;

    .line 40
    iput-boolean v1, p0, Lvo;->n:Z

    .line 42
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 45
    move-result-object p0

    .line 46
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 49
    return-void
.end method

.method public static r(Landroid/app/Activity;Z)V
    .locals 4

    .line 1
    const v0, 0x7f141298

    .line 4
    const v1, 0x7f141299

    .line 7
    const v2, 0x7f150337

    .line 10
    const/4 v3, 0x7

    invoke-static {p0, v2, v0, v1}, Lku1;->f(Landroid/app/Activity;III)Lyo;

    .line 13
    move-result-object v0

    .line 14
    const/4 v3, 0x0

    new-instance v1, Lzh;

    .line 16
    const/16 v2, 0x9

    .line 18
    invoke-direct {v1, v2, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 21
    const v2, 0x104000a

    .line 24
    invoke-virtual {v0, v2, v1}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 27
    new-instance v1, Leob;

    .line 29
    const/4 v3, 0x7

    const/4 v2, 0x4

    .line 30
    invoke-direct {v1, p1, p0, v2}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 33
    const/high16 p0, 0x1040000

    .line 35
    invoke-virtual {v0, p0, v1}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 38
    const/4 p0, 0x0

    .line 39
    const/4 v3, 0x6

    iget-object p1, v0, Lyo;->a:Lvo;

    .line 41
    iput-boolean p0, p1, Lvo;->n:Z

    .line 43
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 46
    move-result-object p0

    .line 47
    const/4 v3, 0x6

    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 50
    const/4 v3, 0x6

    return-void
.end method

.method public static s(Landroid/app/Activity;Ljava/lang/String;Z)V
    .locals 3

    .line 1
    const/4 v0, 0x0

    .line 2
    const/4 v1, 0x0

    .line 3
    invoke-static {p0, p2, p1, v0, v1}, Llob;->t(Landroid/app/Activity;ZLjava/lang/String;Ljava/lang/String;Z)V

    .line 6
    return-void
.end method

.method public static t(Landroid/app/Activity;ZLjava/lang/String;Ljava/lang/String;Z)V
    .locals 5

    .line 1
    if-nez p0, :cond_4

    .line 3
    const/4 v4, 0x0

    goto :goto_13

    .line 4
    :cond_4
    instance-of v0, p0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 6
    if-eqz v0, :cond_15

    .line 8
    move-object v0, p0

    move-object v0, p0

    .line 9
    check-cast v0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 11
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;->T0()Z

    .line 14
    move-result v0

    .line 15
    const/4 v4, 0x4

    if-eqz v0, :cond_15

    .line 17
    :goto_13
    const/4 v4, 0x5

    return-void

    .line 18
    :cond_15
    new-instance v0, Lyo;

    .line 20
    const v1, 0x7f150337

    .line 23
    const/4 v4, 0x1

    invoke-direct {v0, p0, v1}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 26
    iget-object v1, v0, Lyo;->a:Lvo;

    .line 28
    iput-object p2, v1, Lvo;->e:Ljava/lang/CharSequence;

    .line 30
    const/4 p2, 0x0

    shr-int/2addr v4, p2

    .line 31
    if-eqz p3, :cond_2a

    .line 33
    iput-object p3, v1, Lvo;->g:Ljava/lang/CharSequence;

    .line 35
    const/4 v4, 0x2

    goto :goto_5d

    .line 36
    :cond_2a
    const/4 p3, 0x1

    .line 37
    if-eqz p4, :cond_45

    .line 39
    const v2, 0x7f140bbf

    .line 42
    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 45
    move-result-object v2

    .line 46
    invoke-static {}, Llob;->d()Ljava/lang/String;

    .line 49
    move-result-object v3

    .line 50
    new-array p3, p3, [Ljava/lang/Object;

    .line 52
    const/4 v4, 0x3

    aput-object v3, p3, p2

    .line 54
    invoke-static {v2, p3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 57
    move-result-object p3

    .line 58
    iput-object p3, v1, Lvo;->g:Ljava/lang/CharSequence;

    .line 60
    const/4 v4, 0x5

    goto :goto_5d

    .line 61
    :cond_45
    const/4 v4, 0x5

    const v2, 0x7f140bbe

    .line 64
    const/4 v4, 0x4

    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 67
    move-result-object v2

    .line 68
    invoke-static {}, Llob;->d()Ljava/lang/String;

    .line 71
    move-result-object v3

    .line 72
    new-array p3, p3, [Ljava/lang/Object;

    .line 74
    const/4 v4, 0x2

    aput-object v3, p3, p2

    .line 76
    invoke-static {v2, p3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 79
    move-result-object p3

    .line 80
    iput-object p3, v1, Lvo;->g:Ljava/lang/CharSequence;

    .line 82
    :goto_5d
    const/4 v4, 0x2

    new-instance p3, Lzh;

    .line 84
    const/4 v4, 0x5

    const/16 v2, 0xa

    .line 86
    invoke-direct {p3, v2, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 89
    const/4 v4, 0x0

    const v2, 0x7f140ca4

    .line 92
    invoke-virtual {v0, v2, p3}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 95
    const/4 v4, 0x1

    if-eqz p4, :cond_7e

    .line 97
    new-instance p3, Lzh;

    .line 99
    const/16 p4, 0xb

    .line 101
    invoke-direct {p3, p4, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 104
    const/4 v4, 0x7

    const p4, 0x7f141916

    .line 107
    invoke-virtual {v0, p4, p3}, Lyo;->f(ILandroid/content/DialogInterface$OnClickListener;)V

    .line 110
    :cond_7e
    new-instance p3, Leob;

    .line 112
    const/4 p4, 0x6

    .line 113
    invoke-direct {p3, p1, p0, p4}, Leob;-><init>(ZLandroid/app/Activity;I)V

    .line 116
    const/high16 p0, 0x1040000

    .line 118
    invoke-virtual {v0, p0, p3}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 121
    iput-boolean p2, v1, Lvo;->n:Z

    .line 123
    const/4 v4, 0x1

    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 126
    move-result-object p0

    .line 127
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 130
    const/4 v4, 0x3

    invoke-static {p0, p2}, Lxje;->m(Landroid/app/Dialog;I)V

    .line 133
    const/4 v4, 0x2

    const p1, 0x102000b

    .line 136
    invoke-virtual {p0, p1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 139
    move-result-object p0

    .line 140
    const/4 v4, 0x1

    check-cast p0, Landroid/widget/TextView;

    .line 142
    const/16 p1, 0xf

    .line 144
    invoke-static {p0, p1}, Landroid/text/util/Linkify;->addLinks(Landroid/widget/TextView;I)Z

    .line 147
    invoke-static {}, Landroid/text/method/LinkMovementMethod;->getInstance()Landroid/text/method/MovementMethod;

    .line 150
    move-result-object p1

    .line 151
    const/4 v4, 0x6

    invoke-virtual {p0, p1}, Landroid/widget/TextView;->setMovementMethod(Landroid/text/method/MovementMethod;)V

    .line 154
    return-void
.end method

.method public static u(Landroid/app/Activity;Ljava/lang/String;Landroid/content/DialogInterface$OnClickListener;)V
    .locals 6

    .line 1
    if-nez p0, :cond_3

    .line 3
    goto :goto_13

    .line 4
    :cond_3
    const/4 v5, 0x0

    instance-of v0, p0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 6
    if-eqz v0, :cond_15

    .line 8
    move-object v0, p0

    move-object v0, p0

    .line 9
    check-cast v0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 11
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;->T0()Z

    .line 14
    move-result v0

    .line 15
    const/4 v5, 0x6

    if-eqz v0, :cond_15

    .line 17
    :goto_13
    const/4 v5, 0x7

    return-void

    .line 18
    :cond_15
    new-instance v0, Lyo;

    .line 20
    const/4 v5, 0x2

    const v1, 0x7f150337

    .line 23
    const/4 v5, 0x4

    invoke-direct {v0, p0, v1}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 26
    iget-object v1, v0, Lyo;->a:Lvo;

    .line 28
    iput-object p1, v1, Lvo;->e:Ljava/lang/CharSequence;

    .line 30
    const p1, 0x7f140bc0

    .line 33
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 36
    move-result-object p1

    .line 37
    const/4 v5, 0x0

    invoke-static {}, Llob;->d()Ljava/lang/String;

    .line 40
    move-result-object v2

    .line 41
    const/4 v3, 0x1

    .line 42
    const/4 v5, 0x0

    new-array v3, v3, [Ljava/lang/Object;

    .line 44
    const/4 v4, 0x0

    .line 45
    const/4 v5, 0x6

    aput-object v2, v3, v4

    .line 47
    const/4 v5, 0x6

    invoke-static {p1, v3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 50
    move-result-object p1

    .line 51
    const/4 v5, 0x2

    iput-object p1, v1, Lvo;->g:Ljava/lang/CharSequence;

    .line 53
    const p1, 0x7f141185

    .line 56
    const/4 v5, 0x4

    invoke-virtual {v0, p1, p2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 59
    new-instance p1, Lzh;

    .line 61
    const/16 p2, 0xe

    .line 63
    const/4 v5, 0x6

    invoke-direct {p1, p2, p0}, Lzh;-><init>(ILandroid/app/Activity;)V

    .line 66
    const p0, 0x7f140ca4

    .line 69
    invoke-virtual {v0, p0, p1}, Lyo;->f(ILandroid/content/DialogInterface$OnClickListener;)V

    .line 72
    const/4 v5, 0x0

    iput-boolean v4, v1, Lvo;->n:Z

    .line 74
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 77
    move-result-object p0

    .line 78
    const/4 v5, 0x0

    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 81
    const p1, 0x102000b

    .line 84
    invoke-virtual {p0, p1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 87
    move-result-object p0

    .line 88
    check-cast p0, Landroid/widget/TextView;

    .line 90
    const/16 p1, 0xf

    .line 92
    invoke-static {p0, p1}, Landroid/text/util/Linkify;->addLinks(Landroid/widget/TextView;I)Z

    .line 95
    invoke-static {}, Landroid/text/method/LinkMovementMethod;->getInstance()Landroid/text/method/MovementMethod;

    .line 98
    move-result-object p1

    .line 99
    invoke-virtual {p0, p1}, Landroid/widget/TextView;->setMovementMethod(Landroid/text/method/MovementMethod;)V

    .line 102
    return-void
.end method

.method public static v(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V
    .locals 6

    .line 1
    if-nez p0, :cond_3

    .line 3
    return-void

    .line 4
    :cond_3
    invoke-static {p1}, Llob;->e(Ljava/lang/String;)Ljava/lang/String;

    .line 7
    move-result-object v0

    .line 8
    const/4 v5, 0x4

    new-instance v1, Ljava/lang/StringBuilder;

    .line 10
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 13
    if-nez p2, :cond_19

    .line 15
    const/4 v5, 0x7

    const v2, 0x7f140f29

    .line 18
    const/4 v5, 0x3

    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 21
    move-result-object v2

    .line 22
    goto :goto_1a

    .line 23
    :cond_19
    move-object v2, p2

    .line 24
    :goto_1a
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 27
    const-string v2, " "

    .line 29
    const/4 v5, 0x0

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 32
    const v3, 0x7f14128f

    .line 35
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 38
    move-result-object v3

    .line 39
    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 42
    const/4 v5, 0x6

    invoke-static {v2, v0, v2, v1}, Liu1;->A(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 45
    const/4 v5, 0x6

    const v0, 0x7f14118b

    .line 48
    const/4 v5, 0x6

    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 51
    move-result-object v0

    .line 52
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 55
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 58
    move-result-object v0

    .line 59
    sget-object v1, Llob;->a:Ljava/util/HashMap;

    .line 61
    invoke-virtual {v1, p1}, Ljava/util/HashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    .line 64
    move-result-object v1

    .line 65
    const/4 v5, 0x4

    check-cast v1, Ljava/lang/Integer;

    .line 67
    if-nez v1, :cond_54

    .line 69
    const v1, 0x7a1db8

    .line 72
    const/4 v5, 0x5

    invoke-static {v1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 75
    move-result-object v1

    .line 76
    :cond_54
    new-instance v2, Landroid/content/Intent;

    .line 78
    const-class v3, Lcom/arlosoft/macrodroid/permissions/PermissionRequestActivity;

    .line 80
    invoke-direct {v2, p0, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 83
    const-string v3, "permission"

    .line 85
    invoke-virtual {v2, v3, p1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 88
    const-string p1, "lttio"

    const-string/jumbo p1, "title"

    .line 90
    invoke-virtual {v2, p1, p2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 93
    const/4 v5, 0x4

    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    .line 96
    move-result p1

    .line 97
    const/high16 p2, 0x8000000

    .line 99
    sget v3, Lsmb;->a:I

    .line 101
    or-int/2addr p2, v3

    .line 102
    const/4 v5, 0x6

    invoke-static {p0, p1, v2, p2}, Landroid/app/PendingIntent;->getActivity(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;

    .line 105
    move-result-object p1

    .line 106
    const/4 v5, 0x0

    new-instance p2, Lava;

    .line 108
    const/4 v2, 0x7

    const/4 v2, 0x0

    .line 109
    invoke-direct {p2, p0, v2}, Lava;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 112
    const v2, 0x7f140f46

    .line 115
    invoke-virtual {p0, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 118
    move-result-object v2

    .line 119
    const/4 v5, 0x2

    invoke-static {v2}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 122
    move-result-object v2

    .line 123
    const/4 v5, 0x0

    iput-object v2, p2, Lava;->e:Ljava/lang/CharSequence;

    .line 125
    const/4 v5, 0x2

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 128
    move-result-wide v2

    .line 129
    const/4 v5, 0x2

    iget-object v4, p2, Lava;->z:Landroid/app/Notification;

    .line 131
    iput-wide v2, v4, Landroid/app/Notification;->when:J

    .line 133
    invoke-static {v0}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 136
    move-result-object v2

    .line 137
    const/4 v5, 0x2

    iput-object v2, p2, Lava;->f:Ljava/lang/CharSequence;

    .line 139
    iput-object p1, p2, Lava;->h:Landroid/app/PendingIntent;

    .line 141
    const/4 v5, 0x3

    const p1, 0x7f080422

    .line 144
    iput p1, v4, Landroid/app/Notification;->icon:I

    .line 146
    const/4 p1, 0x1

    .line 147
    const/16 v2, 0x10

    .line 149
    const/4 v5, 0x1

    invoke-virtual {p2, v2, p1}, Lava;->g(IZ)V

    .line 152
    const p1, 0x7f06062e

    .line 155
    invoke-static {p0, p1}, Lw63;->getColor(Landroid/content/Context;I)I

    .line 158
    move-result p1

    .line 159
    iput p1, p2, Lava;->r:I

    .line 161
    new-instance p1, Lwua;

    .line 163
    const/16 v2, 0x9

    .line 165
    const/4 v3, 0x2

    const/4 v3, 0x0

    .line 166
    invoke-direct {p1, v2, v3}, La3;-><init>(IZ)V

    .line 169
    invoke-static {v0}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 172
    move-result-object v0

    .line 173
    const/4 v5, 0x3

    iput-object v0, p1, Lwua;->c:Ljava/lang/CharSequence;

    .line 175
    invoke-virtual {p2, p1}, Lava;->j(La3;)V

    .line 178
    const-string/jumbo p1, "vital_functionality"

    .line 180
    iput-object p1, p2, Lava;->t:Ljava/lang/String;

    .line 182
    invoke-virtual {p2}, Lava;->b()Landroid/app/Notification;

    .line 185
    move-result-object p1

    .line 186
    const/4 v5, 0x3

    const-string p2, "notification"

    .line 188
    const/4 v5, 0x6

    invoke-virtual {p0, p2}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 191
    move-result-object p0

    .line 192
    check-cast p0, Landroid/app/NotificationManager;

    .line 194
    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    .line 197
    move-result p2

    .line 198
    invoke-virtual {p0, p2, p1}, Landroid/app/NotificationManager;->notify(ILandroid/app/Notification;)V

    .line 201
    return-void
.end method

.method public static w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V
    .locals 9

    .line 1
    const/4 v8, 0x3

    if-nez p0, :cond_5

    .line 3
    goto/16 :goto_df

    .line 5
    :cond_5
    const v0, 0x7f140f46

    .line 8
    const/4 v8, 0x7

    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 11
    move-result-object v0

    .line 12
    const/4 v8, 0x7

    const-string v1, " - "

    .line 14
    invoke-static {p1, v1}, Lx9f;->I(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 17
    move-result-object v1

    .line 18
    const/4 v2, 0x1

    .line 19
    const v3, 0x7f141413

    .line 22
    const/4 v8, 0x6

    packed-switch p3, :pswitch_data_224

    .line 25
    goto/16 :goto_147

    .line 27
    :pswitch_1e
    const p2, 0x7f1404ef

    .line 30
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 33
    move-result-object p2

    .line 34
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 37
    const/4 v8, 0x2

    goto/16 :goto_147

    .line 39
    :pswitch_2b
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 42
    move-result-object v0

    .line 43
    const p2, 0x7f141416

    .line 46
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 49
    move-result-object p2

    .line 50
    const/4 v8, 0x2

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 53
    const/4 v8, 0x3

    goto/16 :goto_147

    .line 55
    :pswitch_3d
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 58
    move-result-object v0

    .line 59
    const p2, 0x7f141418

    .line 62
    const/4 v8, 0x2

    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 65
    move-result-object p2

    .line 66
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 69
    goto/16 :goto_147

    .line 71
    :pswitch_4e
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 74
    move-result-object v0

    .line 75
    const/4 v8, 0x6

    const p2, 0x7f141417

    .line 78
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 81
    move-result-object p2

    .line 82
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 85
    goto/16 :goto_147

    .line 87
    :pswitch_5f
    invoke-virtual {p0, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 90
    move-result-object v0

    .line 91
    const/4 v8, 0x3

    const p2, 0x7f14141b

    .line 94
    const/4 v8, 0x1

    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 97
    move-result-object p2

    .line 98
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 101
    const/4 v8, 0x1

    goto/16 :goto_147

    .line 103
    :pswitch_72
    const p2, 0x7f140083

    .line 106
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 109
    move-result-object p2

    .line 110
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 113
    goto/16 :goto_147

    .line 115
    :pswitch_7e
    const p2, 0x7f14059d

    .line 118
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 121
    move-result-object p2

    .line 122
    const/4 v8, 0x4

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 125
    const p2, 0x7f14059e

    .line 128
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 131
    move-result-object v0

    .line 132
    goto/16 :goto_147

    .line 134
    :pswitch_92
    const v0, 0x7f140ce9

    .line 137
    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 140
    move-result-object v3

    .line 141
    const/4 v8, 0x6

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 144
    new-instance v3, Ljava/lang/StringBuilder;

    .line 146
    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    .line 149
    const/4 v8, 0x1

    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 152
    move-result-object v0

    .line 153
    const/4 v8, 0x1

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 156
    const-string v0, " ("

    const-string v0, " ("

    .line 158
    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 161
    const/4 v8, 0x7

    invoke-virtual {v3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 164
    const-string p2, "+)"

    .line 166
    const/4 v8, 0x3

    invoke-virtual {v3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 169
    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 172
    move-result-object v0

    .line 173
    const/4 v8, 0x7

    goto/16 :goto_147

    .line 175
    :pswitch_c3
    const p2, 0x7f141292

    .line 178
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 181
    move-result-object p2

    .line 182
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 185
    goto :goto_147

    .line 186
    :pswitch_ce
    const/4 v8, 0x6

    sget-object p2, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 188
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 191
    move-result-object p2

    .line 192
    const/4 v8, 0x1

    const-string v0, "preferences:show_location_services_warning"

    .line 194
    const/4 v8, 0x1

    invoke-interface {p2, v0, v2}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 197
    move-result p2

    .line 198
    if-nez p2, :cond_e1

    .line 200
    :goto_df
    const/4 v8, 0x4

    return-void

    .line 201
    :cond_e1
    const p2, 0x7f140e84

    .line 204
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 207
    move-result-object v0

    .line 208
    const p2, 0x7f140e83

    .line 211
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 214
    move-result-object p2

    .line 215
    const/4 v8, 0x5

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 218
    goto :goto_147

    .line 219
    :pswitch_f4
    const p2, 0x7f140940

    .line 222
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 225
    move-result-object p2

    .line 226
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 229
    const/4 v8, 0x6

    goto :goto_147

    .line 230
    :pswitch_100
    const p2, 0x7f1410ed

    .line 233
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 236
    move-result-object p2

    .line 237
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 240
    goto :goto_147

    .line 241
    :pswitch_10b
    const p2, 0x7f14128e

    .line 244
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 247
    move-result-object p2

    .line 248
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 251
    goto :goto_147

    .line 252
    :pswitch_116
    const/4 v8, 0x6

    const p2, 0x7f140022

    .line 255
    const/4 v8, 0x5

    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 258
    move-result-object p2

    .line 259
    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 262
    goto :goto_147

    .line 263
    :pswitch_123
    const/4 v8, 0x5

    const p2, 0x7f1418f2

    .line 266
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 269
    move-result-object p2

    .line 270
    const/4 v8, 0x5

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 273
    goto :goto_147

    .line 274
    :pswitch_130
    const p2, 0x7f141293

    .line 277
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 280
    move-result-object p2

    .line 281
    const/4 v8, 0x1

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 284
    goto :goto_147

    .line 285
    :pswitch_13c
    const p2, 0x7f141298

    .line 288
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 291
    move-result-object p2

    .line 292
    const/4 v8, 0x2

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 295
    :goto_147
    sget-object p2, Llob;->b:Ljava/util/HashMap;

    .line 297
    const/4 v8, 0x0

    invoke-static {p3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 300
    move-result-object v3

    .line 301
    const/4 v8, 0x0

    invoke-virtual {p2, v3}, Ljava/util/HashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    .line 304
    move-result-object p2

    .line 305
    check-cast p2, Ljava/lang/Integer;

    .line 307
    if-nez p2, :cond_15f

    .line 309
    const p2, 0x7a1db8

    .line 312
    const/4 v8, 0x4

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 315
    move-result-object p2

    .line 316
    :cond_15f
    new-instance v3, Landroid/content/Intent;

    .line 318
    const/4 v8, 0x0

    const-class v4, Lcom/arlosoft/macrodroid/permissions/PermissionRequestActivity;

    .line 320
    invoke-direct {v3, p0, v4}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 323
    const-string/jumbo v4, "special_permission_id"

    .line 325
    invoke-virtual {v3, v4, p3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 328
    const-string/jumbo p3, "title"

    .line 330
    invoke-virtual {v3, p3, p1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 333
    invoke-virtual {p2}, Ljava/lang/Integer;->intValue()I

    .line 336
    move-result p1

    .line 337
    const/high16 p3, 0x8000000

    .line 339
    sget v4, Lsmb;->a:I

    .line 341
    or-int/2addr p3, v4

    .line 342
    invoke-static {p0, p1, v3, p3}, Landroid/app/PendingIntent;->getActivity(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;

    .line 345
    move-result-object p1

    .line 346
    const/4 v8, 0x0

    new-instance p3, Lava;

    .line 348
    const/4 v3, 0x0

    .line 349
    invoke-direct {p3, p0, v3}, Lava;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 352
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 355
    move-result-object v1

    .line 356
    invoke-static {v0}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 359
    move-result-object v4

    .line 360
    iput-object v4, p3, Lava;->e:Ljava/lang/CharSequence;

    .line 362
    const/4 v8, 0x6

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 365
    move-result-wide v4

    .line 366
    iget-object v6, p3, Lava;->z:Landroid/app/Notification;

    .line 368
    iput-wide v4, v6, Landroid/app/Notification;->when:J

    .line 370
    invoke-static {v1}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 373
    move-result-object v4

    .line 374
    iput-object v4, p3, Lava;->f:Ljava/lang/CharSequence;

    .line 376
    iput-object p1, p3, Lava;->h:Landroid/app/PendingIntent;

    .line 378
    const/4 v8, 0x3

    const p1, 0x7f080422

    .line 381
    iput p1, v6, Landroid/app/Notification;->icon:I

    .line 383
    const/16 v4, 0x10

    .line 385
    invoke-virtual {p3, v4, v2}, Lava;->g(IZ)V

    .line 388
    const/4 v8, 0x7

    const v4, 0x7f06062e

    .line 391
    invoke-static {p0, v4}, Lw63;->getColor(Landroid/content/Context;I)I

    .line 394
    move-result v4

    .line 395
    iput v4, p3, Lava;->r:I

    .line 397
    const/4 v8, 0x0

    const-string v4, "nrisibesomP"

    const-string v4, "Permissions"

    .line 399
    const/4 v8, 0x7

    iput-object v4, p3, Lava;->n:Ljava/lang/String;

    .line 401
    new-instance v5, Lwua;

    .line 403
    const/16 v6, 0x9

    .line 405
    const/4 v7, 0x0

    .line 406
    const/4 v8, 0x7

    invoke-direct {v5, v6, v7}, La3;-><init>(IZ)V

    .line 409
    invoke-static {v1}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 412
    move-result-object v6

    .line 413
    iput-object v6, v5, Lwua;->c:Ljava/lang/CharSequence;

    .line 415
    invoke-virtual {p3, v5}, Lava;->j(La3;)V

    .line 418
    const-string/jumbo v5, "yitoutuvlinfatnl_ia"

    const-string/jumbo v5, "vital_functionality"

    .line 420
    const/4 v8, 0x2

    iput-object v5, p3, Lava;->t:Ljava/lang/String;

    .line 422
    invoke-virtual {p3}, Lava;->b()Landroid/app/Notification;

    .line 425
    move-result-object p3

    .line 426
    const/4 v8, 0x4

    const-string v6, "notification"

    .line 428
    invoke-virtual {p0, v6}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 431
    move-result-object v6

    .line 432
    check-cast v6, Landroid/app/NotificationManager;

    .line 434
    new-instance v7, Lava;

    .line 436
    invoke-direct {v7, p0, v3}, Lava;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 439
    invoke-static {v0}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 442
    move-result-object p0

    .line 443
    iput-object p0, v7, Lava;->e:Ljava/lang/CharSequence;

    .line 445
    invoke-static {v1}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 448
    move-result-object p0

    .line 449
    const/4 v8, 0x6

    iput-object p0, v7, Lava;->f:Ljava/lang/CharSequence;

    .line 451
    iget-object p0, v7, Lava;->z:Landroid/app/Notification;

    .line 453
    const/4 v8, 0x1

    iput p1, p0, Landroid/app/Notification;->icon:I

    .line 455
    iput-object v4, v7, Lava;->n:Ljava/lang/String;

    .line 457
    const/16 p0, 0x8

    .line 459
    const/4 v8, 0x6

    invoke-virtual {v7, p0, v2}, Lava;->g(IZ)V

    .line 462
    const/4 v8, 0x0

    iput-boolean v2, v7, Lava;->o:Z

    .line 464
    iput-object v5, v7, Lava;->t:Ljava/lang/String;

    .line 466
    const p0, 0x3628883

    .line 469
    invoke-virtual {v7}, Lava;->b()Landroid/app/Notification;

    .line 472
    move-result-object p1

    .line 473
    const/4 v8, 0x3

    invoke-virtual {v6, p0, p1}, Landroid/app/NotificationManager;->notify(ILandroid/app/Notification;)V

    .line 476
    invoke-virtual {p2}, Ljava/lang/Integer;->intValue()I

    .line 479
    move-result p0

    .line 480
    const/4 v8, 0x7

    invoke-virtual {v6, p0, p3}, Landroid/app/NotificationManager;->notify(ILandroid/app/Notification;)V

    .line 483
    invoke-static {v1}, Lkjf;->l(Ljava/lang/String;)V

    .line 486
    const/4 v8, 0x4

    return-void

    nop

    .line 487
    :pswitch_data_224
    .packed-switch 0x1
        :pswitch_13c
        :pswitch_130
        :pswitch_123
        :pswitch_116
        :pswitch_10b
        :pswitch_100
        :pswitch_f4
        :pswitch_116
        :pswitch_116
        :pswitch_116
        :pswitch_ce
        :pswitch_c3
        :pswitch_92
        :pswitch_7e
        :pswitch_72
        :pswitch_5f
        :pswitch_4e
        :pswitch_3d
        :pswitch_2b
        :pswitch_1e
    .end packed-switch
.end method
