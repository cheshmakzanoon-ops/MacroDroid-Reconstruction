.method public final a(Lm73;)Ljava/lang/Object;
    .locals 11

    .line 1
    const-string v10, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    const-string v0, "ProDeviceCheckWorker: server says device is deallocated (reason="

    .line 3
    const/4 v10, 0x2

    instance-of v1, p1, Lcom/arlosoft/macrodroid/upgrade/b;

    .line 5
    const/4 v10, 0x6

    if-eqz v1, :cond_1c

    .line 7
    move-object v1, p1

    .line 8
    check-cast v1, Lcom/arlosoft/macrodroid/upgrade/b;

    .line 10
    iget v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->label:I

    .line 12
    const/4 v10, 0x7

    const/high16 v3, -0x80000000

    .line 14
    and-int v4, v2, v3

    .line 16
    if-eqz v4, :cond_1c

    .line 18
    sub-int/2addr v2, v3

    .line 19
    const/4 v10, 0x4

    iput v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->label:I

    .line 21
    const/4 v10, 0x1

    goto :goto_23

    .line 22
    :cond_1c
    new-instance v1, Lcom/arlosoft/macrodroid/upgrade/b;

    .line 24
    check-cast p1, Lo73;

    .line 26
    invoke-direct {v1, p0, p1}, Lcom/arlosoft/macrodroid/upgrade/b;-><init>(Lcom/arlosoft/macrodroid/upgrade/ProDeviceCheckWorker;Lo73;)V

    .line 29
    :goto_23
    iget-object p1, v1, Lcom/arlosoft/macrodroid/upgrade/b;->result:Ljava/lang/Object;

    .line 31
    sget-object v2, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 33
    iget v3, v1, Lcom/arlosoft/macrodroid/upgrade/b;->label:I

    .line 35
    const/4 v10, 0x1

    const/4 v4, 0x2

    .line 36
    const/4 v10, 0x7

    const/4 v5, 0x1

    .line 37
    iget-object p0, p0, Lcom/arlosoft/macrodroid/upgrade/ProDeviceCheckWorker;->g:Landroid/content/Context;

    .line 39
    const/4 v6, 0x0

    .line 40
    if-eqz v3, :cond_7b

    .line 42
    const/4 v10, 0x6

    if-eq v3, v5, :cond_60

    .line 44
    if-ne v3, v4, :cond_5a

    .line 46
    const/4 v10, 0x5

    iget-object v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$5:Ljava/lang/Object;

    .line 48
    const/4 v10, 0x5

    check-cast v2, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceRequest;

    .line 50
    const/4 v10, 0x4

    iget-object v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$4:Ljava/lang/Object;

    .line 52
    const/4 v10, 0x1

    check-cast v2, Ljava/lang/String;

    .line 54
    const/4 v10, 0x7

    iget-object v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$3:Ljava/lang/Object;

    .line 56
    check-cast v2, Ljava/lang/String;

    .line 58
    iget-object v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$2:Ljava/lang/Object;

    .line 60
    check-cast v2, Ljava/lang/String;

    .line 62
    iget-object v2, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$1:Ljava/lang/Object;

    .line 64
    check-cast v2, Ljava/lang/String;

    .line 66
    iget-object v1, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$0:Ljava/lang/Object;

    .line 68
    const/4 v10, 0x4

    check-cast v1, Ljava/lang/String;

    .line 70
    :try_start_55
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_58
    .catch Lretrofit2/HttpException; {:try_start_55 .. :try_end_58} :catch_1c0
    .catch Ljava/lang/Exception; {:try_start_55 .. :try_end_58} :catch_193

    .line 73
    goto/16 :goto_15b

    .line 75
    :cond_5a
    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 77
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 80
    return-object v6

    .line 81
    :cond_60
    iget-object v3, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$3:Ljava/lang/Object;

    .line 83
    const/4 v10, 0x1

    check-cast v3, Lcom/arlosoft/macrodroid/upgrade/ProDeviceCheckWorker;

    .line 85
    iget-object v3, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$2:Ljava/lang/Object;

    .line 87
    check-cast v3, Ljava/lang/String;

    .line 89
    const/4 v10, 0x3

    iget-object v5, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$1:Ljava/lang/Object;

    .line 91
    check-cast v5, Ljava/lang/String;

    .line 93
    iget-object v7, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$0:Ljava/lang/Object;

    .line 95
    check-cast v7, Ljava/lang/String;

    .line 97
    :try_start_72
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_75
    .catchall {:try_start_72 .. :try_end_75} :catchall_78

    .line 100
    const/4 v10, 0x5

    goto/16 :goto_f7

    .line 102
    :catchall_78
    move-exception p1

    .line 103
    goto/16 :goto_101

    .line 105
    :cond_7b
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 108
    sget-object p1, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 110
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 113
    move-result-object p1

    .line 114
    const-string v3, "pro_via_device_cap"

    .line 116
    const/4 v7, 0x0

    .line 117
    invoke-interface {p1, v3, v7}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 120
    move-result p1

    .line 121
    if-nez p1, :cond_97

    .line 123
    const-string p0, "ProDeviceCheckWorker: not on device-cap model, skipping"

    .line 125
    invoke-static {p0}, Lkjf;->f(Ljava/lang/String;)V

    .line 128
    invoke-static {}, Lsa9;->a()Lra9;

    .line 131
    move-result-object p0

    .line 132
    return-object p0

    .line 133
    :cond_97
    const/4 v10, 0x0

    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 136
    move-result-object p1

    .line 137
    const-string v3, "pro_email"

    .line 139
    invoke-interface {p1, v3, v6}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 142
    move-result-object p1

    .line 143
    const/4 v10, 0x0

    invoke-static {p0}, Lcom/arlosoft/macrodroid/settings/c;->s0(Landroid/content/Context;)Ljava/lang/String;

    .line 146
    move-result-object v3

    .line 147
    const/4 v10, 0x4

    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 150
    move-result-object v8

    .line 151
    const/4 v10, 0x3

    const-string v9, "pro_device_fingerprint"

    .line 153
    invoke-interface {v8, v9, v6}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 156
    move-result-object v8

    .line 157
    if-eqz p1, :cond_1e8

    .line 159
    const/4 v10, 0x1

    invoke-static {p1}, Lz8f;->K1(Ljava/lang/CharSequence;)Z

    .line 162
    move-result v9

    .line 163
    if-eqz v9, :cond_be

    .line 165
    goto/16 :goto_1e8

    .line 167
    :cond_be
    if-eqz v3, :cond_1e8

    .line 169
    invoke-static {v3}, Lz8f;->K1(Ljava/lang/CharSequence;)Z

    .line 172
    move-result v9

    .line 173
    const/4 v10, 0x7

    if-eqz v9, :cond_c9

    .line 175
    goto/16 :goto_1e8

    .line 177
    :cond_c9
    if-eqz v8, :cond_1e8

    .line 179
    invoke-static {v8}, Lz8f;->K1(Ljava/lang/CharSequence;)Z

    .line 182
    move-result v9

    .line 183
    if-eqz v9, :cond_d3

    .line 185
    goto/16 :goto_1e8

    .line 187
    :cond_d3
    :try_start_d3
    invoke-static {}, Lcom/google/firebase/messaging/FirebaseMessaging;->d()Lcom/google/firebase/messaging/FirebaseMessaging;

    .line 190
    move-result-object v9

    .line 191
    const/4 v10, 0x5

    invoke-virtual {v9}, Lcom/google/firebase/messaging/FirebaseMessaging;->g()Lcom/google/android/gms/tasks/Task;

    .line 194
    move-result-object v9

    .line 195
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 198
    iput-object p1, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$0:Ljava/lang/Object;

    .line 200
    iput-object v3, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$1:Ljava/lang/Object;

    .line 202
    iput-object v8, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$2:Ljava/lang/Object;

    .line 204
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$3:Ljava/lang/Object;

    .line 206
    iput v7, v1, Lcom/arlosoft/macrodroid/upgrade/b;->I$0:I

    .line 208
    iput v5, v1, Lcom/arlosoft/macrodroid/upgrade/b;->label:I

    .line 210
    invoke-static {v9, v1}, Luy6;->i(Lcom/google/android/gms/tasks/Task;Lo73;)Ljava/lang/Object;

    .line 213
    move-result-object v5
    :try_end_ef
    .catchall {:try_start_d3 .. :try_end_ef} :catchall_fa

    .line 214
    if-ne v5, v2, :cond_f2

    .line 216
    goto :goto_159

    .line 217
    :cond_f2
    move-object v7, p1

    .line 218
    move-object p1, v5

    move-object p1, v5

    .line 219
    move-object v5, v3

    .line 220
    move-object v3, v8

    .line 221
    :goto_f7
    :try_start_f7
    check-cast p1, Ljava/lang/String;
    :try_end_f9
    .catchall {:try_start_f7 .. :try_end_f9} :catchall_78

    .line 223
    goto :goto_108

    .line 224
    :catchall_fa
    move-exception v5

    .line 225
    move-object v7, p1

    move-object v7, p1

    .line 226
    move-object p1, v5

    .line 227
    move-object v5, v3

    .line 228
    move-object v3, v8

    move-object v3, v8

    .line 229
    :goto_101
    const/4 v10, 0x2

    new-instance v8, Lg3d;

    .line 231
    invoke-direct {v8, p1}, Lg3d;-><init>(Ljava/lang/Throwable;)V

    .line 234
    move-object p1, v8

    .line 235
    :goto_108
    nop

    .line 236
    const/4 v10, 0x1

    instance-of v8, p1, Lg3d;

    .line 238
    if-eqz v8, :cond_10f

    .line 240
    move-object p1, v6

    .line 241
    :cond_10f
    const/4 v10, 0x4

    check-cast p1, Ljava/lang/String;

    .line 243
    const/4 v10, 0x6

    new-instance v8, Ljava/lang/StringBuilder;

    .line 245
    const/4 v10, 0x6

    const-string v9, "adb97ac6-f780-4a41-8475-ce661b574999"

    .line 247
    const/4 v10, 0x6

    invoke-direct {v8, v9}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 250
    invoke-virtual {v8, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 253
    const/4 v10, 0x2

    invoke-virtual {v8, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 256
    invoke-virtual {v8, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 259
    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 262
    move-result-object v8

    .line 263
    invoke-static {v8}, Lvdg;->m0(Ljava/lang/String;)Ljava/lang/String;

    .line 266
    move-result-object v8

    .line 267
    const/4 v10, 0x7

    new-instance v9, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceRequest;

    .line 269
    invoke-direct {v9, v7, v5, v3, p1}, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceRequest;-><init>(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 272
    :try_start_134
    sget-object p1, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->E:Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;

    .line 274
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 277
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;->a()Lxg0;

    .line 280
    move-result-object p1

    .line 281
    check-cast p1, Lru3;

    .line 283
    invoke-virtual {p1}, Lru3;->j()Lcom/arlosoft/macrodroid/action/email/api/UpgradeApi;

    .line 286
    move-result-object p1

    .line 287
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$0:Ljava/lang/Object;

    .line 289
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$1:Ljava/lang/Object;

    .line 291
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$2:Ljava/lang/Object;

    .line 293
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$3:Ljava/lang/Object;

    .line 295
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$4:Ljava/lang/Object;

    .line 297
    iput-object v6, v1, Lcom/arlosoft/macrodroid/upgrade/b;->L$5:Ljava/lang/Object;

    .line 299
    const/4 v10, 0x2

    iput v4, v1, Lcom/arlosoft/macrodroid/upgrade/b;->label:I

    .line 301
    const/4 v10, 0x2

    invoke-interface {p1, v8, v9, v1}, Lcom/arlosoft/macrodroid/action/email/api/UpgradeApi;->checkDevice(Ljava/lang/String;Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceRequest;Lm73;)Ljava/lang/Object;

    .line 304
    move-result-object p1

    .line 305
    if-ne p1, v2, :cond_15b

    .line 307
    :goto_159
    const/4 v10, 0x0

    return-object v2

    .line 308
    :cond_15b
    :goto_15b
    check-cast p1, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceResponse;

    .line 310
    const/4 v10, 0x6

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceResponse;->getActive()Z

    .line 313
    move-result v1

    .line 314
    if-nez v1, :cond_18d

    .line 316
    const/4 v10, 0x4

    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/upgrade/model/V2CheckDeviceResponse;->getReason()Ljava/lang/String;

    .line 319
    move-result-object p1

    .line 320
    const/4 v10, 0x6

    new-instance v1, Ljava/lang/StringBuilder;

    .line 322
    invoke-direct {v1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 325
    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 328
    const/4 v10, 0x1

    const-string p1, ")"

    .line 330
    const/4 v10, 0x5

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 333
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 336
    move-result-object p1

    .line 337
    const/4 v10, 0x4

    invoke-static {p1}, Lkjf;->u(Ljava/lang/String;)V

    .line 340
    sget-object p1, Lcom/arlosoft/macrodroid/upgrade/a;->a:Lcom/arlosoft/macrodroid/upgrade/a;

    .line 342
    const/4 v10, 0x7

    const-string v0, "poll"

    .line 344
    const/4 v10, 0x1

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 347
    invoke-static {p0, v0}, Lcom/arlosoft/macrodroid/upgrade/a;->a(Landroid/content/Context;Ljava/lang/String;)V

    .line 350
    :cond_18d
    const/4 v10, 0x0

    invoke-static {}, Lsa9;->a()Lra9;

    .line 353
    move-result-object p0
    :try_end_192
    .catch Lretrofit2/HttpException; {:try_start_134 .. :try_end_192} :catch_1c0
    .catch Ljava/lang/Exception; {:try_start_134 .. :try_end_192} :catch_193

    .line 354
    goto :goto_1e7

    .line 355
    :catch_193
    move-exception p0

    .line 356
    const/4 v10, 0x7

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 359
    move-result-object p0

    .line 360
    const/4 v10, 0x1

    invoke-virtual {p0}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    .line 363
    move-result-object p0

    .line 364
    const/4 v10, 0x2

    new-instance p1, Ljava/lang/StringBuilder;

    .line 366
    const-string v0, "ProDeviceCheckWorker: transient failure ("

    .line 368
    const/4 v10, 0x2

    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 371
    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 374
    const/4 v10, 0x7

    const-string p0, "); will retry"

    .line 376
    const/4 v10, 0x1

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 379
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 382
    move-result-object p0

    .line 383
    invoke-static {p0}, Lkjf;->u(Ljava/lang/String;)V

    .line 386
    new-instance p0, Lqa9;

    .line 388
    const/4 v10, 0x0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 391
    const/4 v10, 0x2

    goto :goto_1e7

    .line 392
    :catch_1c0
    move-exception p0

    .line 393
    const/4 v10, 0x3

    invoke-virtual {p0}, Lretrofit2/HttpException;->a()I

    .line 396
    move-result p0

    .line 397
    const/4 v10, 0x1

    new-instance p1, Ljava/lang/StringBuilder;

    .line 399
    const-string v0, "ProDeviceCheckWorker: HTTP "

    .line 401
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 404
    const/4 v10, 0x5

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 407
    const-string/jumbo p0, "twsyirr l; l"

    const-string p0, "; will retry"

    .line 409
    const/4 v10, 0x6

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 412
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 415
    move-result-object p0

    .line 416
    invoke-static {p0}, Lkjf;->u(Ljava/lang/String;)V

    .line 419
    new-instance p0, Lqa9;

    .line 421
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 424
    :goto_1e7
    return-object p0

    .line 425
    :cond_1e8
    :goto_1e8
    const/4 v10, 0x0

    const-string p1, "grimrdencnkvcetrlaCceicD:sae eriePclehersmnokg, rokos nwlW i"

    const-string p1, "ProDeviceCheckWorker: missing credentials, cancelling worker"

    .line 427
    invoke-static {p1}, Lkjf;->u(Ljava/lang/String;)V

    .line 430
    sget-object p1, Lcom/arlosoft/macrodroid/upgrade/ProDeviceCheckWorker;->h:Lcom/arlosoft/macrodroid/upgrade/ProDeviceCheckWorker$a;

    .line 432
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 435
    const/4 v10, 0x3

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 438
    invoke-static {p0}, Lnnh;->g(Landroid/content/Context;)Lnnh;

    .line 441
    move-result-object p0

    .line 442
    const/4 v10, 0x7

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 445
    const-string p1, "ccpeoei_vorehkcd"

    const-string p1, "pro_device_check"

    .line 447
    invoke-virtual {p0, p1}, Lnnh;->b(Ljava/lang/String;)Lzra;

    .line 450
    invoke-static {}, Lsa9;->a()Lra9;

    .line 453
    move-result-object p0

    .line 454
    return-object p0
.end method
