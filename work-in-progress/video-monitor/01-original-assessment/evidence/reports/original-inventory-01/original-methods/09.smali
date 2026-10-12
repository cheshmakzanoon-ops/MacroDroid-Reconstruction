.method public final onStartCommand(Landroid/content/Intent;II)I
    .locals 60

    .line 1
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 3
    move-object/from16 v0, p1

    .line 5
    const/4 v13, 0x0

    .line 6
    if-eqz v0, :cond_e

    .line 8
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 11
    move-result-object v2

    .line 12
    goto :goto_f

    .line 13
    :cond_e
    move-object v2, v13

    .line 14
    :goto_f
    const-string v3, "scanQuickTiles"

    .line 16
    invoke-static {v2, v3}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 19
    move-result v2

    .line 20
    sget-object v14, Lvz6;->a:Lvz6;

    .line 22
    const/4 v15, 0x2

    .line 23
    if-eqz v2, :cond_27

    .line 25
    sget-object v0, Lzp4;->a:Lad4;

    .line 27
    sget-object v0, Lat9;->a:Lm47;

    .line 29
    new-instance v2, Lcom/arlosoft/macrodroid/action/services/m;

    .line 31
    invoke-direct {v2, v1, v13}, Lcom/arlosoft/macrodroid/action/services/m;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;Lm73;)V

    .line 34
    invoke-static {v14, v0, v13, v2, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 37
    return v15

    .line 38
    :cond_27
    if-eqz v0, :cond_2e

    .line 40
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 43
    move-result-object v2

    .line 44
    goto :goto_2f

    .line 45
    :cond_2e
    move-object v2, v13

    .line 46
    :goto_2f
    const-string/jumbo v3, "showCaptureClickOverlay"

    .line 48
    invoke-static {v2, v3}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 51
    move-result v2

    .line 52
    const-string/jumbo v3, "window"

    .line 54
    const/4 v4, 0x1

    .line 55
    const/4 v5, 0x0

    .line 56
    if-eqz v2, :cond_c4

    .line 58
    const-string v2, "captureClickReplay"

    .line 60
    invoke-virtual {v0, v2, v5}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 63
    move-result v2

    .line 64
    const-string v6, "captureClickTimeoutMs"

    .line 66
    const-wide/16 v7, 0x7530

    .line 68
    invoke-virtual {v0, v6, v7, v8}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 71
    move-result-wide v6

    .line 72
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->C()V

    .line 75
    iput-boolean v2, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->w:Z

    .line 77
    new-instance v0, Landroid/widget/FrameLayout;

    .line 79
    invoke-direct {v0, v1}, Landroid/widget/FrameLayout;-><init>(Landroid/content/Context;)V

    .line 82
    invoke-static {v4, v5, v5, v5}, Landroid/graphics/Color;->argb(IIII)I

    .line 85
    move-result v2

    .line 86
    invoke-virtual {v0, v2}, Landroid/view/View;->setBackgroundColor(I)V

    .line 89
    new-instance v2, Lao2;

    .line 91
    const/4 v4, 0x6

    .line 92
    invoke-direct {v2, v1, v4}, Lao2;-><init>(Ljava/lang/Object;I)V

    .line 95
    invoke-virtual {v0, v2}, Landroid/view/View;->setOnTouchListener(Landroid/view/View$OnTouchListener;)V

    .line 98
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->v:Landroid/widget/FrameLayout;

    .line 100
    new-instance v16, Landroid/view/WindowManager$LayoutParams;

    .line 102
    const/16 v20, 0x308

    .line 104
    const/16 v21, -0x3

    .line 106
    const/16 v17, -0x1

    .line 108
    const/16 v18, -0x1

    .line 110
    const/16 v19, 0x7f0

    .line 112
    invoke-direct/range {v16 .. v21}, Landroid/view/WindowManager$LayoutParams;-><init>(IIIII)V

    .line 115
    move-object/from16 v0, v16

    .line 117
    const v2, 0x800033

    .line 120
    iput v2, v0, Landroid/view/WindowManager$LayoutParams;->gravity:I

    .line 122
    invoke-static {v0}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->d(Landroid/view/WindowManager$LayoutParams;)V

    .line 125
    :try_start_80
    invoke-virtual {v1, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 128
    move-result-object v2

    .line 129
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 132
    check-cast v2, Landroid/view/WindowManager;

    .line 134
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->v:Landroid/widget/FrameLayout;

    .line 136
    invoke-interface {v2, v3, v0}, Landroid/view/ViewManager;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 139
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y:Lw52;

    .line 141
    if-eqz v0, :cond_99

    .line 143
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->x:Landroid/os/Handler;

    .line 145
    if-eqz v2, :cond_99

    .line 147
    invoke-virtual {v2, v0}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V

    .line 150
    :cond_99
    iput-object v13, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->x:Landroid/os/Handler;

    .line 152
    iput-object v13, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y:Lw52;

    .line 154
    new-instance v0, Landroid/os/Handler;

    .line 156
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 159
    move-result-object v2

    .line 160
    invoke-direct {v0, v2}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 163
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->x:Landroid/os/Handler;

    .line 165
    new-instance v2, Lw52;

    .line 167
    const/4 v3, 0x5

    .line 168
    invoke-direct {v2, v6, v7, v1, v3}, Lw52;-><init>(JLjava/lang/Object;I)V

    .line 171
    iput-object v2, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y:Lw52;

    .line 173
    invoke-virtual {v0, v2, v6, v7}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 176
    invoke-static {v5, v1}, Lj0h;->b(ILandroid/content/Context;)V
    :try_end_b6
    .catch Ljava/lang/Exception; {:try_start_80 .. :try_end_b6} :catch_b7

    .line 179
    return v15

    .line 180
    :catch_b7
    move-exception v0

    .line 181
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 184
    move-result-object v0

    .line 185
    const-string v2, "Failed to show capture click overlay: "

    .line 187
    invoke-static {v2, v0}, Lbl5;->D(Ljava/lang/String;Ljava/lang/String;)V

    .line 190
    iput-object v13, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->v:Landroid/widget/FrameLayout;

    .line 192
    return v15

    .line 193
    :cond_c4
    if-eqz v0, :cond_cb

    .line 195
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 198
    move-result-object v2

    .line 199
    goto :goto_cd

    .line 200
    :cond_cb
    move-object v2, v13

    move-object v2, v13

    .line 201
    :goto_cd
    const-string v6, "hideCaptureClickOverlay"

    .line 203
    invoke-static {v2, v6}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 206
    move-result v2

    .line 207
    if-eqz v2, :cond_d9

    .line 209
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->C()V

    .line 212
    return v15

    .line 213
    :cond_d9
    if-eqz v0, :cond_e0

    .line 215
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 218
    move-result-object v2

    .line 219
    goto :goto_e1

    .line 220
    :cond_e0
    move-object v2, v13

    .line 221
    :goto_e1
    const-string v6, "findNodeByText"

    .line 223
    invoke-static {v2, v6}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 226
    move-result v2

    .line 227
    const-string v6, ""

    .line 229
    if-eqz v2, :cond_108

    .line 231
    const-string v2, "findNodeText"

    .line 233
    invoke-virtual {v0, v2}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 236
    move-result-object v2

    .line 237
    if-nez v2, :cond_f4

    .line 239
    goto :goto_f5

    .line 240
    :cond_f4
    move-object v6, v2

    .line 241
    :goto_f5
    const-string v2, "findNodeMatchAny"

    .line 243
    invoke-virtual {v0, v2, v4}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 246
    move-result v0

    .line 247
    sget-object v2, Lzp4;->a:Lad4;

    .line 249
    sget-object v2, Lat9;->a:Lm47;

    .line 251
    new-instance v3, Lcom/arlosoft/macrodroid/action/services/i;

    .line 253
    invoke-direct {v3, v1, v6, v0, v13}, Lcom/arlosoft/macrodroid/action/services/i;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;Ljava/lang/String;ZLm73;)V

    .line 256
    invoke-static {v14, v2, v13, v3, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 259
    return v15

    .line 260
    :cond_108
    if-eqz v0, :cond_10f

    .line 262
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 265
    move-result-object v2

    .line 266
    goto :goto_111

    .line 267
    :cond_10f
    move-object v2, v13

    move-object v2, v13

    .line 268
    :goto_111
    const-string v7, "getNodeInfoAtLocation"

    .line 270
    invoke-static {v2, v7}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 273
    move-result v2

    .line 274
    if-eqz v2, :cond_134

    .line 276
    const-string v2, "itsonolaX"

    const-string v2, "locationX"

    .line 278
    invoke-virtual {v0, v2, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 281
    move-result v2

    .line 282
    const-string v3, "locationY"

    .line 284
    invoke-virtual {v0, v3, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 287
    move-result v0

    .line 288
    sget-object v3, Lzp4;->a:Lad4;

    .line 290
    sget-object v3, Lat9;->a:Lm47;

    .line 292
    new-instance v4, Lcom/arlosoft/macrodroid/action/services/j;

    .line 294
    invoke-direct {v4, v2, v0, v1, v13}, Lcom/arlosoft/macrodroid/action/services/j;-><init>(IILcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;Lm73;)V

    .line 297
    invoke-static {v14, v3, v13, v4, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 300
    return v15

    .line 301
    :cond_134
    if-eqz v0, :cond_13b

    .line 303
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 306
    move-result-object v2

    .line 307
    goto :goto_13d

    .line 308
    :cond_13b
    move-object v2, v13

    move-object v2, v13

    .line 309
    :goto_13d
    const-string v7, "captureScreenshotBitmap"

    .line 311
    invoke-static {v2, v7}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 314
    move-result v2

    .line 315
    const/16 v7, 0x1e

    .line 317
    if-eqz v2, :cond_16b

    .line 319
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 321
    if-lt v0, v7, :cond_15c

    .line 323
    invoke-virtual {v1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 326
    move-result-object v0

    .line 327
    invoke-virtual {v0}, Landroid/content/Context;->getMainExecutor()Ljava/util/concurrent/Executor;

    .line 330
    move-result-object v0

    .line 331
    new-instance v2, Lugg;

    .line 333
    invoke-direct {v2, v1}, Lugg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;)V

    .line 336
    invoke-virtual {v1, v5, v0, v2}, Landroid/accessibilityservice/AccessibilityService;->takeScreenshot(ILjava/util/concurrent/Executor;Landroid/accessibilityservice/AccessibilityService$TakeScreenshotCallback;)V

    .line 339
    return v15

    .line 340
    :cond_15c
    const-string v0, "Read QR from screen requires Android 11+"

    .line 342
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 345
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y()Lzvd;

    .line 348
    move-result-object v0

    .line 349
    iget-object v0, v0, Lzvd;->k:Lqge;

    .line 351
    invoke-virtual {v0, v13}, Lqge;->a(Ljava/lang/Object;)Z

    .line 354
    return v15

    .line 355
    :cond_16b
    if-eqz v0, :cond_34e

    .line 357
    invoke-virtual {v0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 360
    move-result-object v2

    .line 361
    if-eqz v2, :cond_34e

    .line 363
    const-string v8, "GlobalControlType"

    .line 365
    const/4 v9, -0x1

    .line 366
    invoke-virtual {v2, v8, v9}, Landroid/os/BaseBundle;->getInt(Ljava/lang/String;I)I

    .line 369
    move-result v8

    .line 370
    if-eq v8, v9, :cond_180

    .line 372
    invoke-virtual {v1, v8}, Landroid/accessibilityservice/AccessibilityService;->performGlobalAction(I)Z

    .line 375
    return v15

    .line 376
    :cond_180
    const-string v8, "service_request_id"

    .line 378
    invoke-virtual {v2, v8, v9}, Landroid/os/BaseBundle;->getInt(Ljava/lang/String;I)I

    .line 381
    move-result v8

    .line 382
    invoke-static {v8}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 385
    move-result-object v9

    .line 386
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 389
    move-result-wide v10

    .line 390
    invoke-static {v10, v11}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 393
    move-result-object v10

    .line 394
    iget-object v11, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->h:Lj$/util/concurrent/ConcurrentHashMap;

    .line 396
    invoke-virtual {v11, v9, v10}, Lj$/util/concurrent/ConcurrentHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 399
    const-string/jumbo v9, "wTtmedyItgeiVeB"

    const-string v9, "getTextByViewId"

    .line 401
    invoke-virtual {v2, v9}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;)Z

    .line 404
    move-result v9

    .line 405
    const-string v10, "captureScreen"

    .line 407
    invoke-virtual {v2, v10}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;)Z

    .line 410
    move-result v10

    .line 411
    const-string v11, "ieuuoyQ"

    const-string/jumbo v11, "uiQuery"

    .line 413
    invoke-virtual {v2, v11}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;)Z

    .line 416
    move-result v11

    .line 417
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 420
    move-result-object v12

    .line 421
    const-string v7, "inputKeyEvent"

    .line 423
    invoke-static {v12, v7}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 426
    move-result v7

    .line 427
    if-eqz v7, :cond_20b

    .line 429
    const-string v2, "keyCode"

    .line 431
    invoke-virtual {v0, v2, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 434
    move-result v2

    .line 435
    const-string v3, "OtoprbnesykPei"

    const-string v3, "keyPressOption"

    .line 437
    invoke-virtual {v0, v3, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 440
    move-result v3

    .line 441
    const-string v4, "keyModifierMask"

    .line 443
    invoke-virtual {v0, v4, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 446
    move-result v4

    .line 447
    new-instance v0, Ljava/lang/StringBuilder;

    .line 449
    const-string v5, "sendKey "

    .line 451
    invoke-direct {v0, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 454
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 457
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 460
    move-result-object v0

    .line 461
    invoke-static {v0}, Lsz5;->a(Ljava/lang/String;)V

    .line 464
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 466
    const/16 v5, 0x21

    .line 468
    if-ge v0, v5, :cond_1ef

    .line 470
    const-string v0, "onrrsiu1 ue Ti3Acr+tidshq  adeio"

    const-string v0, "This action requires Android 13+"

    .line 472
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 475
    goto/16 :goto_cc1

    .line 477
    :cond_1ef
    invoke-virtual {v1}, Landroid/accessibilityservice/AccessibilityService;->getServiceInfo()Landroid/accessibilityservice/AccessibilityServiceInfo;

    .line 480
    move-result-object v0

    .line 481
    if-eqz v0, :cond_204

    .line 483
    sget-object v0, Lzp4;->a:Lad4;

    .line 485
    sget-object v6, Lat9;->a:Lm47;

    .line 487
    new-instance v0, Lghg;

    .line 489
    const/4 v5, 0x0

    .line 490
    invoke-direct/range {v0 .. v5}, Lghg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;IIILm73;)V

    .line 493
    invoke-static {v14, v6, v13, v0, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 496
    goto/16 :goto_cc1

    .line 498
    :cond_204
    const-string v0, "Accessibility service not connected"

    .line 500
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 503
    goto/16 :goto_cc1

    .line 505
    :cond_20b
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 508
    move-result-object v7

    .line 509
    const-string/jumbo v12, "uiQueryScreenshot"

    .line 511
    invoke-static {v7, v12}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 514
    move-result v7

    .line 515
    const-string v12, "charset_option"

    .line 517
    if-eqz v7, :cond_255

    .line 519
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->m:Lkwd;

    .line 521
    if-eqz v2, :cond_24f

    .line 523
    invoke-virtual {v0, v12, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 526
    move-result v3

    .line 527
    sget-object v6, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->J:Ljava/lang/String;

    .line 529
    const-string v7, "pAepavgpaugpierkscoP"

    const-string v7, "previousFgAppPackage"

    .line 531
    invoke-virtual {v0, v7}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 534
    move-result-object v0

    .line 535
    iget-boolean v7, v2, Lkwd;->c:Z

    .line 537
    if-nez v7, :cond_239

    .line 539
    const-string v7, "nfntlineqstcgrcitorSne c inag eo rte"

    const-string v7, "Screen content trigger is functional"

    .line 541
    invoke-static {v7}, Lkjf;->f(Ljava/lang/String;)V

    .line 544
    iput-boolean v4, v2, Lkwd;->c:Z

    .line 546
    :cond_239
    sget v4, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 548
    const/16 v7, 0x1e

    .line 550
    if-lt v4, v7, :cond_cc1

    .line 552
    iget-object v4, v2, Lkwd;->a:Landroid/content/Context;

    .line 554
    invoke-virtual {v4}, Landroid/content/Context;->getMainExecutor()Ljava/util/concurrent/Executor;

    .line 557
    move-result-object v4

    .line 558
    new-instance v7, Ljwd;

    .line 560
    invoke-direct {v7, v2, v3, v6, v0}, Ljwd;-><init>(Lkwd;ILjava/lang/String;Ljava/lang/String;)V

    .line 563
    invoke-virtual {v1, v5, v4, v7}, Landroid/accessibilityservice/AccessibilityService;->takeScreenshot(ILjava/util/concurrent/Executor;Landroid/accessibilityservice/AccessibilityService$TakeScreenshotCallback;)V

    .line 566
    goto/16 :goto_cc1

    .line 568
    :cond_24f
    const-string v0, "screenShotTriggerHandler"

    .line 570
    invoke-static {v0}, Lj68;->h0(Ljava/lang/String;)V

    .line 573
    throw v13

    .line 574
    :cond_255
    invoke-virtual {v0}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 577
    move-result-object v7

    .line 578
    const-string v4, "captureScreenshotText"

    .line 580
    invoke-static {v7, v4}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 583
    move-result v4

    .line 584
    if-eqz v4, :cond_284

    .line 586
    invoke-virtual {v0, v12, v5}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 589
    move-result v0

    .line 590
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 592
    const/16 v7, 0x1e

    .line 594
    if-lt v2, v7, :cond_27d

    .line 596
    invoke-virtual {v1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 599
    move-result-object v2

    .line 600
    invoke-virtual {v2}, Landroid/content/Context;->getMainExecutor()Ljava/util/concurrent/Executor;

    .line 603
    move-result-object v2

    .line 604
    new-instance v3, Ltgg;

    .line 606
    invoke-direct {v3, v1, v0}, Ltgg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;I)V

    .line 609
    invoke-virtual {v1, v5, v2, v3}, Landroid/accessibilityservice/AccessibilityService;->takeScreenshot(ILjava/util/concurrent/Executor;Landroid/accessibilityservice/AccessibilityService$TakeScreenshotCallback;)V

    .line 612
    goto/16 :goto_cc1

    .line 614
    :cond_27d
    const-string v0, "This action requires Android 11+"

    .line 616
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 619
    goto/16 :goto_cc1

    .line 621
    :cond_284
    const-string v0, "forceScreenRefresh"

    .line 623
    const-string/jumbo v4, "ueslrlidvcsOyna"

    const-string v4, "includeOverlays"

    .line 625
    if-eqz v9, :cond_303

    .line 627
    iput v5, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p:I

    .line 629
    invoke-virtual {v2, v4, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 632
    move-result v3

    .line 633
    const-string/jumbo v4, "viewId"

    .line 635
    invoke-virtual {v2, v4, v6}, Landroid/os/BaseBundle;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 638
    move-result-object v4

    .line 639
    const-string v6, "eeemlxgaRbn"

    const-string v6, "enableRegex"

    .line 641
    invoke-virtual {v2, v6, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 644
    move-result v6

    .line 645
    const-string v7, "roeioansge"

    const-string v7, "ignoreCase"

    .line 647
    invoke-virtual {v2, v7, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 650
    move-result v7

    .line 651
    invoke-virtual {v2, v0, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 654
    move-result v0

    .line 655
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 658
    invoke-virtual {v1, v3}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->x(Z)Ljava/util/List;

    .line 661
    move-result-object v2

    .line 662
    new-instance v3, Ljava/util/HashSet;

    .line 664
    invoke-direct {v3}, Ljava/util/HashSet;-><init>()V

    .line 667
    invoke-static {v4, v6, v7}, Lyih;->c(Ljava/lang/String;ZZ)Ljava/lang/String;

    .line 670
    move-result-object v4

    .line 671
    invoke-interface {v2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 674
    move-result-object v10

    .line 675
    :goto_2c2
    invoke-interface {v10}, Ljava/util/Iterator;->hasNext()Z

    .line 678
    move-result v2

    .line 679
    if-eqz v2, :cond_2f8

    .line 681
    invoke-interface {v10}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 684
    move-result-object v2

    .line 685
    check-cast v2, Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 687
    if-eqz v2, :cond_2f1

    .line 689
    const/4 v8, 0x0

    .line 690
    const/4 v9, 0x0

    .line 691
    move v5, v6

    move v5, v6

    .line 692
    move v6, v7

    move v6, v7

    .line 693
    move v7, v0

    .line 694
    invoke-virtual/range {v1 .. v9}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->u(Landroid/view/accessibility/AccessibilityNodeInfo;Ljava/util/HashSet;Ljava/lang/String;ZZZILjava/util/Set;)Ljava/lang/String;

    .line 697
    move-result-object v0

    .line 698
    if-eqz v0, :cond_2e8

    .line 700
    invoke-virtual/range {p0 .. p0}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y()Lzvd;

    .line 703
    move-result-object v1

    .line 704
    iget-object v1, v1, Lzvd;->c:Lqge;

    .line 706
    invoke-virtual {v1, v0}, Lqge;->a(Ljava/lang/Object;)Z

    .line 709
    goto/16 :goto_cc1

    .line 711
    :cond_2e8
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 713
    move v0, v7

    .line 714
    move v7, v6

    move v7, v6

    .line 715
    :goto_2ef
    move v6, v5

    .line 716
    goto :goto_2c2

    .line 717
    :cond_2f1
    move v5, v6

    .line 718
    move v6, v7

    .line 719
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 721
    goto :goto_2ef

    .line 722
    :cond_2f8
    invoke-virtual/range {p0 .. p0}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->y()Lzvd;

    .line 725
    move-result-object v0

    .line 726
    iget-object v0, v0, Lzvd;->c:Lqge;

    .line 728
    invoke-virtual {v0, v13}, Lqge;->a(Ljava/lang/Object;)Z

    .line 731
    goto/16 :goto_cc1

    .line 733
    :cond_303
    const-string v1, "macroGuid"

    .line 735
    move-object/from16 v17, v14

    .line 737
    const-wide/16 v13, -0x1

    .line 739
    if-eqz v10, :cond_33d

    .line 741
    invoke-virtual {v2, v4, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 744
    move-result v3

    .line 745
    const-string v4, "includeWithoutText"

    .line 747
    invoke-virtual {v2, v4, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 750
    move-result v4

    .line 751
    const-string v6, "baeuabslIkclsF"

    const-string/jumbo v6, "useIdFallbacks"

    .line 753
    invoke-virtual {v2, v6, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 756
    move-result v6

    .line 757
    invoke-virtual {v2, v0, v5}, Landroid/os/BaseBundle;->getBoolean(Ljava/lang/String;Z)Z

    .line 760
    move-result v5

    .line 761
    move v0, v3

    move v0, v3

    .line 762
    move v3, v4

    .line 763
    move v4, v6

    .line 764
    invoke-virtual {v2, v1, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 767
    move-result-wide v6

    .line 768
    sget-object v9, Lzp4;->a:Lad4;

    .line 770
    move v2, v0

    .line 771
    new-instance v0, Lchg;

    .line 773
    const/4 v8, 0x0

    .line 774
    move-object/from16 v1, p0

    .line 776
    invoke-direct/range {v0 .. v8}, Lchg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;ZZZZJLm73;)V

    .line 779
    move-object/from16 v4, v17

    .line 781
    const/4 v7, 0x0

    .line 782
    invoke-static {v4, v9, v7, v0, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 785
    goto/16 :goto_cc1

    .line 787
    :cond_33d
    const/4 v7, 0x0

    .line 788
    move-object/from16 v9, p0

    .line 790
    move-object/from16 v4, v17

    .line 792
    if-eqz v11, :cond_352

    .line 794
    sget-object v0, Lzp4;->a:Lad4;

    .line 796
    new-instance v1, Ldhg;

    .line 798
    invoke-direct {v1, v9, v7}, Ldhg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;Lm73;)V

    .line 801
    invoke-static {v4, v0, v7, v1, v15}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 804
    :cond_34e
    move/from16 v34, v15

    .line 806
    goto/16 :goto_cc3

    .line 808
    :cond_352
    const-string v0, "iogtioutifrecnuanCI"

    const-string/jumbo v0, "uiInteractionConfig"

    .line 810
    invoke-virtual {v2, v0}, Landroid/os/Bundle;->getParcelable(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 813
    move-result-object v0

    .line 814
    move-object v7, v0

    .line 815
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 817
    const-string/jumbo v0, "xtiretoptgoCIgnenf"

    const-string/jumbo v0, "triggerContextInfo"

    .line 819
    invoke-virtual {v2, v0}, Landroid/os/Bundle;->getParcelable(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 822
    move-result-object v0

    .line 823
    check-cast v0, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 825
    const-string/jumbo v10, "xVariableValue"

    .line 827
    invoke-virtual {v2, v10, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 830
    move-result-wide v10

    .line 831
    const-string/jumbo v12, "yVariableValue"

    .line 833
    invoke-virtual {v2, v12, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 836
    move-result-wide v17

    .line 837
    invoke-virtual {v2, v1, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 840
    move-result-wide v19

    .line 841
    const-string/jumbo v1, "xStartVariableValue"

    .line 843
    move-object v12, v6

    move-object v12, v6

    .line 844
    invoke-virtual {v2, v1, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 847
    move-result-wide v5

    .line 848
    const-string/jumbo v1, "yStartVariableValue"

    .line 850
    move/from16 v21, v8

    .line 852
    invoke-virtual {v2, v1, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 855
    move-result-wide v8

    .line 856
    const-string v1, "nlledixVqaeVabruE"

    const-string/jumbo v1, "xEndVariableValue"

    .line 858
    move-object/from16 p1, v0

    .line 860
    invoke-virtual {v2, v1, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 863
    move-result-wide v0

    .line 864
    const-string v15, "aeslabVdVinElauey"

    const-string/jumbo v15, "yEndVariableValue"

    .line 866
    move-wide/from16 v22, v10

    .line 868
    invoke-virtual {v2, v15, v13, v14}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 871
    move-result-wide v10

    .line 872
    const-string v15, "sequenceXValues"

    .line 874
    invoke-virtual {v2, v15}, Landroid/os/BaseBundle;->getLongArray(Ljava/lang/String;)[J

    .line 877
    move-result-object v15

    .line 878
    const/4 v13, 0x0

    .line 879
    if-nez v15, :cond_3af

    .line 881
    new-array v15, v13, [J

    .line 883
    :cond_3af
    const-string v14, "euYmecVaenslqsu"

    const-string v14, "sequenceYValues"

    .line 885
    invoke-virtual {v2, v14}, Landroid/os/BaseBundle;->getLongArray(Ljava/lang/String;)[J

    .line 888
    move-result-object v14

    .line 889
    if-nez v14, :cond_3bb

    .line 891
    new-array v14, v13, [J

    .line 893
    :cond_3bb
    const-string v13, "aVueorbndaVaiertuaoil"

    const-string v13, "durationVariableValue"

    .line 895
    move-object/from16 v24, v12

    .line 897
    move-object/from16 v29, v14

    .line 899
    move-object/from16 v28, v15

    .line 901
    const-wide/16 v14, -0x1

    .line 903
    invoke-virtual {v2, v13, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 906
    move-result-wide v12

    .line 907
    move-object/from16 v25, v4

    .line 909
    const-string v4, "point1XVariableValue"

    .line 911
    move-wide/from16 v30, v12

    .line 913
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 916
    move-result-wide v12

    .line 917
    const-string v4, "point1YVariableValue"

    .line 919
    move-wide/from16 v32, v12

    .line 921
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 924
    move-result-wide v12

    .line 925
    const-string v4, "point2XVariableValue"

    .line 927
    move-wide/from16 v35, v12

    .line 929
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 932
    move-result-wide v12

    .line 933
    const-string v4, "point2YVariableValue"

    .line 935
    move-wide/from16 v37, v12

    .line 937
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 940
    move-result-wide v12

    .line 941
    const-string v4, "metuPbleicaeolaebVVonzrr"

    const-string/jumbo v4, "zoomPercentVariableValue"

    .line 943
    move-wide/from16 v39, v12

    .line 945
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 948
    move-result-wide v12

    .line 949
    const-string v4, "rotateDegreesVariableValue"

    .line 951
    move-wide/from16 v41, v12

    .line 953
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 956
    move-result-wide v12

    .line 957
    const-string/jumbo v4, "xStartVariableValue2"

    .line 959
    move-wide/from16 v43, v12

    .line 961
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 964
    move-result-wide v12

    .line 965
    const-string v4, "leartruiayeVSa2atVlb"

    const-string/jumbo v4, "yStartVariableValue2"

    .line 967
    move-wide/from16 v45, v12

    .line 969
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 972
    move-result-wide v12

    .line 973
    const-string/jumbo v4, "xEndVariableValue2"

    .line 975
    move-wide/from16 v47, v12

    .line 977
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 980
    move-result-wide v12

    .line 981
    const-string v4, "ndVeebypliEa2luraa"

    const-string/jumbo v4, "yEndVariableValue2"

    .line 983
    invoke-virtual {v2, v4, v14, v15}, Landroid/os/BaseBundle;->getLong(Ljava/lang/String;J)J

    .line 986
    move-result-wide v14

    .line 987
    instance-of v2, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 989
    if-eqz v2, :cond_449

    .line 991
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    .line 994
    move-result-wide v3

    .line 995
    new-instance v0, Lehg;

    .line 997
    const/4 v12, 0x0

    .line 998
    move-object/from16 v5, p0

    .line 1000
    move-wide/from16 v10, v17

    .line 1002
    move-wide/from16 v1, v19

    .line 1004
    move/from16 v6, v21

    .line 1006
    move-wide/from16 v8, v22

    .line 1008
    move-object/from16 v13, v25

    .line 1010
    invoke-direct/range {v0 .. v12}, Lehg;-><init>(JJLcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;ILcom/arlosoft/macrodroid/action/UiInteractionConfiguration;JJLm73;)V

    .line 1013
    sget-object v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->P:Lvk5;

    .line 1015
    const/4 v2, 0x2

    .line 1016
    const/4 v7, 0x0

    .line 1017
    invoke-static {v13, v1, v7, v0, v2}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 1020
    goto/16 :goto_cc1

    .line 1022
    :cond_449
    move-wide/from16 v17, v12

    .line 1024
    move-wide/from16 v49, v14

    .line 1026
    move-wide/from16 v14, v19

    .line 1028
    move-wide v12, v0

    .line 1029
    move-object/from16 v1, p0

    .line 1031
    instance-of v0, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Copy;

    .line 1033
    const-string/jumbo v2, "utucl)fpqdldsyiedo ore c e t nCct(oacn eIutUor "

    const-string v2, "Copy failed (could not detect current UI focus)"

    .line 1035
    if-eqz v0, :cond_46e

    .line 1037
    const/4 v4, 0x1

    .line 1038
    invoke-virtual {v1, v4}, Landroid/accessibilityservice/AccessibilityService;->findFocus(I)Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 1041
    move-result-object v0

    .line 1042
    if-eqz v0, :cond_469

    .line 1044
    const/16 v1, 0x4000

    .line 1046
    invoke-virtual {v0, v1}, Landroid/view/accessibility/AccessibilityNodeInfo;->performAction(I)Z

    .line 1049
    goto/16 :goto_cc1

    .line 1051
    :cond_469
    invoke-static {v14, v15, v2}, Lkjf;->g(JLjava/lang/String;)V

    .line 1054
    goto/16 :goto_cc1

    .line 1056
    :cond_46e
    const/4 v4, 0x1

    .line 1057
    instance-of v0, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Cut;

    .line 1059
    if-eqz v0, :cond_487

    .line 1061
    invoke-virtual {v1, v4}, Landroid/accessibilityservice/AccessibilityService;->findFocus(I)Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 1064
    move-result-object v0

    .line 1065
    if-eqz v0, :cond_480

    .line 1067
    const/high16 v1, 0x10000

    .line 1069
    invoke-virtual {v0, v1}, Landroid/view/accessibility/AccessibilityNodeInfo;->performAction(I)Z

    .line 1072
    goto/16 :goto_cc1

    .line 1074
    :cond_480
    const-string v0, "Cut failed (could not detect current UI focus)"

    .line 1076
    invoke-static {v14, v15, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1079
    goto/16 :goto_cc1

    .line 1081
    :cond_487
    instance-of v0, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$ClearSelection;

    .line 1083
    if-eqz v0, :cond_4a3

    .line 1085
    const/4 v4, 0x1

    .line 1086
    invoke-virtual {v1, v4}, Landroid/accessibilityservice/AccessibilityService;->findFocus(I)Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 1089
    move-result-object v1

    .line 1090
    if-eqz v1, :cond_499

    .line 1092
    const/16 v0, 0x8

    .line 1094
    invoke-virtual {v1, v0}, Landroid/view/accessibility/AccessibilityNodeInfo;->performAction(I)Z

    .line 1097
    goto/16 :goto_cc1

    .line 1099
    :cond_499
    const-string/jumbo v0, "tuse tticroledcdrt dusule   Iane i  retCanln)osUc(eoocfefc"

    const-string v0, "Clear selection failed (could not detect current UI focus)"

    .line 1101
    invoke-static {v14, v15, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1104
    goto/16 :goto_cc1

    .line 1106
    :cond_4a3
    instance-of v4, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 1108
    if-eqz v4, :cond_510

    .line 1110
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 1112
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getUseClipboard()Z

    .line 1115
    move-result v0

    .line 1116
    if-eqz v0, :cond_4f8

    .line 1118
    const-string v0, "clipboard"

    .line 1120
    invoke-virtual {v1, v0}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 1123
    move-result-object v0

    .line 1124
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1127
    check-cast v0, Landroid/content/ClipboardManager;

    .line 1129
    invoke-virtual {v0}, Landroid/content/ClipboardManager;->getPrimaryClip()Landroid/content/ClipData;

    .line 1132
    move-result-object v0

    .line 1133
    if-eqz v0, :cond_4c6

    .line 1135
    const/4 v13, 0x0

    .line 1136
    invoke-virtual {v0, v13}, Landroid/content/ClipData;->getItemAt(I)Landroid/content/ClipData$Item;

    .line 1139
    move-result-object v13

    .line 1140
    goto :goto_4c7

    .line 1141
    :cond_4c6
    const/4 v13, 0x0

    .line 1142
    :goto_4c7
    if-eqz v13, :cond_4e1

    .line 1144
    invoke-virtual {v13}, Landroid/content/ClipData$Item;->getText()Ljava/lang/CharSequence;

    .line 1147
    move-result-object v0

    .line 1148
    if-eqz v0, :cond_4e1

    .line 1150
    invoke-virtual {v13}, Landroid/content/ClipData$Item;->getText()Ljava/lang/CharSequence;

    .line 1153
    move-result-object v0

    .line 1154
    if-eqz v0, :cond_4de

    .line 1156
    invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 1159
    move-result-object v0

    .line 1160
    if-nez v0, :cond_4dc

    .line 1162
    goto :goto_4de

    .line 1163
    :cond_4dc
    move-object v2, v0

    .line 1164
    goto :goto_4e6

    .line 1165
    :cond_4de
    :goto_4de
    move-object/from16 v2, v24

    .line 1167
    goto :goto_4e6

    .line 1168
    :cond_4e1
    sget-object v0, Lch2;->a:Ljava/lang/String;

    .line 1170
    if-nez v0, :cond_4dc

    .line 1172
    goto :goto_4de

    .line 1173
    :goto_4e6
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getForceClear()Z

    .line 1176
    move-result v3

    .line 1177
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getUseNewClipboardPasteMechanism()Z

    .line 1180
    move-result v4

    .line 1181
    move-object/from16 v5, p1

    move-object/from16 v5, p1

    .line 1183
    move-wide v6, v14

    .line 1184
    invoke-virtual/range {v1 .. v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->F(Ljava/lang/String;ZZLcom/arlosoft/macrodroid/triggers/TriggerContextInfo;J)V

    .line 1187
    goto/16 :goto_cc1

    .line 1189
    :cond_4f8
    move-object/from16 v5, p1

    move-object/from16 v5, p1

    .line 1191
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getText()Ljava/lang/String;

    .line 1194
    move-result-object v2

    .line 1195
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getForceClear()Z

    .line 1198
    move-result v3

    .line 1199
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getUseNewClipboardPasteMechanism()Z

    .line 1202
    move-result v4

    .line 1203
    move-object/from16 v1, p0

    .line 1205
    move-wide v6, v14

    .line 1206
    invoke-virtual/range {v1 .. v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->F(Ljava/lang/String;ZZLcom/arlosoft/macrodroid/triggers/TriggerContextInfo;J)V

    .line 1209
    goto/16 :goto_cc1

    .line 1211
    :cond_510
    instance-of v4, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 1213
    const-string v0, " ham dFtseurecae ltsotdigp"

    const-string v0, "Failed to dispatch gesture"

    .line 1215
    move-wide/from16 v19, v14

    .line 1217
    const-wide/32 v21, 0xea60

    const-wide/32 v21, 0xea60

    .line 1220
    const-string v14, "noy or7nilo duua eedd rs ntter+rGpseo oAp"

    const-string v14, "Gestures are only supported on Android 7+"

    .line 1222
    move-object/from16 v23, v14

    .line 1224
    if-eqz v4, :cond_734

    .line 1226
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 1228
    new-instance v2, Landroid/graphics/Path;

    .line 1230
    invoke-direct {v2}, Landroid/graphics/Path;-><init>()V

    .line 1233
    invoke-virtual {v1, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 1236
    move-result-object v3

    .line 1237
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1240
    check-cast v3, Landroid/view/WindowManager;

    .line 1242
    invoke-interface {v3}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 1245
    move-result-object v3

    .line 1246
    new-instance v4, Landroid/graphics/Point;

    .line 1248
    invoke-direct {v4}, Landroid/graphics/Point;-><init>()V

    .line 1251
    invoke-virtual {v3, v4}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 1254
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1257
    move-result v3

    .line 1258
    if-eqz v3, :cond_583

    .line 1260
    move-object/from16 v53, v0

    .line 1262
    const-wide/16 v14, 0x0

    const-wide/16 v14, 0x0

    .line 1264
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 1267
    move-result-wide v0

    .line 1268
    iget v3, v4, Landroid/graphics/Point;->x:I

    .line 1270
    invoke-static {v3, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1273
    move-result-wide v0

    .line 1274
    long-to-float v0, v0

    .line 1275
    move-wide/from16 v54, v5

    .line 1277
    invoke-static {v14, v15, v8, v9}, Ljava/lang/Math;->max(JJ)J

    .line 1280
    move-result-wide v5

    .line 1281
    iget v1, v4, Landroid/graphics/Point;->y:I

    .line 1283
    invoke-static {v1, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1286
    move-result-wide v5

    .line 1287
    long-to-float v1, v5

    .line 1288
    invoke-virtual {v2, v0, v1}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1291
    invoke-static {v14, v15, v12, v13}, Ljava/lang/Math;->max(JJ)J

    .line 1294
    move-result-wide v0

    .line 1295
    iget v3, v4, Landroid/graphics/Point;->x:I

    .line 1297
    invoke-static {v3, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1300
    move-result-wide v0

    .line 1301
    long-to-float v0, v0

    .line 1302
    invoke-static {v14, v15, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 1305
    move-result-wide v5

    .line 1306
    iget v1, v4, Landroid/graphics/Point;->y:I

    .line 1308
    invoke-static {v1, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1311
    move-result-wide v5

    .line 1312
    long-to-float v1, v5

    .line 1313
    invoke-virtual {v2, v0, v1}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1316
    goto :goto_5a3

    .line 1317
    :cond_583
    move-object/from16 v53, v0

    .line 1319
    const-wide/16 v14, 0x0

    .line 1321
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 1324
    move-result-wide v0

    .line 1325
    long-to-float v0, v0

    .line 1326
    move-wide/from16 v54, v5

    .line 1328
    invoke-static {v14, v15, v8, v9}, Ljava/lang/Math;->max(JJ)J

    .line 1331
    move-result-wide v5

    .line 1332
    long-to-float v1, v5

    .line 1333
    invoke-virtual {v2, v0, v1}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1336
    invoke-static {v14, v15, v12, v13}, Ljava/lang/Math;->max(JJ)J

    .line 1339
    move-result-wide v0

    .line 1340
    long-to-float v0, v0

    .line 1341
    invoke-static {v14, v15, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 1344
    move-result-wide v5

    .line 1345
    long-to-float v1, v5

    .line 1346
    invoke-virtual {v2, v0, v1}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1349
    :goto_5a3
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 1351
    const/16 v1, 0x18

    .line 1353
    if-lt v0, v1, :cond_72b

    .line 1355
    invoke-static {}, Li2;->a()Landroid/accessibilityservice/GestureDescription$Builder;

    .line 1358
    move-result-object v0

    .line 1359
    cmp-long v1, v30, v21

    .line 1361
    if-lez v1, :cond_5bb

    .line 1363
    const-string v1, "Gesture duration exceeds maximum (60 seconds). Forcing to 60 seconds"

    .line 1365
    move-wide/from16 v14, v19

    .line 1367
    invoke-static {v14, v15, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 1370
    move-wide/from16 v5, v21

    .line 1372
    goto :goto_5bf

    .line 1373
    :cond_5bb
    move-wide/from16 v14, v19

    .line 1375
    move-wide/from16 v5, v30

    .line 1377
    :goto_5bf
    invoke-static {}, Lqgg;->a()V

    .line 1380
    move-object/from16 v36, v2

    move-object/from16 v36, v2

    .line 1382
    const-wide/16 v1, 0x1

    const-wide/16 v1, 0x1

    .line 1384
    invoke-static {v1, v2, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 1387
    move-result-wide v39

    .line 1388
    new-instance v35, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 1390
    const-wide/16 v37, 0x0

    .line 1392
    invoke-direct/range {v35 .. v40}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 1395
    move-object/from16 v1, v35

    .line 1397
    invoke-virtual {v0, v1}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 1400
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getAdditionalFingers()I

    .line 1403
    move-result v1

    .line 1404
    if-lez v1, :cond_689

    .line 1406
    const-wide/16 v1, 0x0

    .line 1408
    cmp-long v3, v45, v1

    .line 1410
    if-ltz v3, :cond_689

    .line 1412
    new-instance v3, Landroid/graphics/Path;

    .line 1414
    invoke-direct {v3}, Landroid/graphics/Path;-><init>()V

    .line 1417
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1420
    move-result v19

    .line 1421
    if-eqz v19, :cond_63c

    .line 1423
    move-object/from16 p1, v7

    .line 1425
    move-wide/from16 v56, v8

    .line 1427
    move-wide/from16 v7, v45

    .line 1429
    move-wide/from16 v45, v10

    .line 1431
    invoke-static {v1, v2, v7, v8}, Ljava/lang/Math;->max(JJ)J

    .line 1434
    move-result-wide v9

    .line 1435
    iget v11, v4, Landroid/graphics/Point;->x:I

    .line 1437
    invoke-static {v11, v9, v10}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1440
    move-result-wide v9

    .line 1441
    long-to-float v9, v9

    .line 1442
    move-wide/from16 v10, v47

    .line 1444
    move-wide/from16 v47, v12

    .line 1446
    invoke-static {v1, v2, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 1449
    move-result-wide v12

    .line 1450
    iget v1, v4, Landroid/graphics/Point;->y:I

    .line 1452
    invoke-static {v1, v12, v13}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1455
    move-result-wide v1

    .line 1456
    long-to-float v1, v1

    .line 1457
    invoke-virtual {v3, v9, v1}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1460
    move-wide/from16 v1, v17

    .line 1462
    const-wide/16 v12, 0x0

    .line 1464
    move-wide/from16 v17, v14

    .line 1466
    invoke-static {v12, v13, v1, v2}, Ljava/lang/Math;->max(JJ)J

    .line 1469
    move-result-wide v14

    .line 1470
    iget v9, v4, Landroid/graphics/Point;->x:I

    .line 1472
    invoke-static {v9, v14, v15}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1475
    move-result-wide v14

    .line 1476
    long-to-float v9, v14

    .line 1477
    move-wide/from16 v35, v5

    .line 1479
    move-wide/from16 v14, v49

    .line 1481
    invoke-static {v12, v13, v14, v15}, Ljava/lang/Math;->max(JJ)J

    .line 1484
    move-result-wide v5

    .line 1485
    iget v12, v4, Landroid/graphics/Point;->y:I

    .line 1487
    invoke-static {v12, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1490
    move-result-wide v5

    .line 1491
    long-to-float v5, v5

    .line 1492
    invoke-virtual {v3, v9, v5}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1495
    move-wide/from16 v43, v7

    .line 1497
    goto :goto_66d

    .line 1498
    :cond_63c
    move-wide/from16 v35, v5

    .line 1500
    move-object/from16 p1, v7

    .line 1502
    move-wide/from16 v56, v8

    .line 1504
    move-wide/from16 v7, v45

    .line 1506
    move-wide/from16 v45, v10

    .line 1508
    move-wide/from16 v10, v47

    .line 1510
    move-wide/from16 v47, v12

    .line 1512
    move-wide v12, v1

    .line 1513
    move-wide/from16 v1, v17

    .line 1515
    move-wide/from16 v17, v14

    .line 1517
    move-wide/from16 v14, v49

    .line 1519
    invoke-static {v12, v13, v7, v8}, Ljava/lang/Math;->max(JJ)J

    .line 1522
    move-result-wide v5

    .line 1523
    long-to-float v5, v5

    .line 1524
    move-wide/from16 v43, v7

    .line 1526
    invoke-static {v12, v13, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 1529
    move-result-wide v6

    .line 1530
    long-to-float v6, v6

    .line 1531
    invoke-virtual {v3, v5, v6}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1534
    invoke-static {v12, v13, v1, v2}, Ljava/lang/Math;->max(JJ)J

    .line 1537
    move-result-wide v5

    .line 1538
    long-to-float v5, v5

    .line 1539
    invoke-static {v12, v13, v14, v15}, Ljava/lang/Math;->max(JJ)J

    .line 1542
    move-result-wide v6

    .line 1543
    long-to-float v6, v6

    .line 1544
    invoke-virtual {v3, v5, v6}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1547
    :goto_66d
    invoke-static {}, Lqgg;->a()V

    .line 1550
    move-wide/from16 v5, v35

    .line 1552
    const-wide/16 v7, 0x1

    .line 1554
    invoke-static {v7, v8, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 1557
    move-result-wide v23

    .line 1558
    new-instance v19, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 1560
    const-wide/16 v21, 0x0

    .line 1562
    move-object/from16 v20, v3

    .line 1564
    invoke-direct/range {v19 .. v24}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 1567
    move-object/from16 v3, v19

    move-object/from16 v3, v19

    .line 1569
    invoke-virtual {v0, v3}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 1572
    goto :goto_69b

    .line 1573
    :cond_689
    move-object/from16 p1, v7

    .line 1575
    move-wide/from16 v56, v8

    .line 1577
    move-wide/from16 v1, v17

    .line 1579
    move-wide/from16 v43, v45

    .line 1581
    move-wide/from16 v45, v10

    .line 1583
    move-wide/from16 v17, v14

    .line 1585
    move-wide/from16 v10, v47

    .line 1587
    move-wide/from16 v14, v49

    .line 1589
    move-wide/from16 v47, v12

    .line 1591
    :goto_69b
    invoke-virtual {v0}, Landroid/accessibilityservice/GestureDescription$Builder;->build()Landroid/accessibilityservice/GestureDescription;

    .line 1594
    move-result-object v0

    .line 1595
    const/4 v7, 0x0

    .line 1596
    move-object/from16 v9, p0

    .line 1598
    invoke-virtual {v9, v0, v7, v7}, Landroid/accessibilityservice/AccessibilityService;->dispatchGesture(Landroid/accessibilityservice/GestureDescription;Landroid/accessibilityservice/AccessibilityService$GestureResultCallback;Landroid/os/Handler;)Z

    .line 1601
    move-result v0

    .line 1602
    if-nez v0, :cond_6af

    .line 1604
    move-wide/from16 v12, v17

    .line 1606
    move-object/from16 v0, v53

    .line 1608
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1611
    :cond_6af
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getShowTouchLocation()Z

    .line 1614
    move-result v0

    .line 1615
    if-eqz v0, :cond_cc1

    .line 1617
    new-instance v0, Ljava/util/ArrayList;

    .line 1619
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 1622
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1625
    move-result v26

    .line 1626
    move-object/from16 v25, v4

    .line 1628
    move-wide/from16 v21, v54

    .line 1630
    move-wide/from16 v23, v56

    .line 1632
    invoke-static/range {v21 .. v26}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 1635
    move-result-object v3

    .line 1636
    move-object/from16 v32, v25

    move-object/from16 v32, v25

    .line 1638
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1641
    move-result v33

    .line 1642
    move-wide/from16 v30, v45

    .line 1644
    move-wide/from16 v28, v47

    .line 1646
    invoke-static/range {v28 .. v33}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 1649
    move-result-object v4

    .line 1650
    const/4 v7, 0x2

    .line 1651
    new-array v8, v7, [Landroid/graphics/Point;

    .line 1653
    const/16 v27, 0x0

    .line 1655
    aput-object v3, v8, v27

    .line 1657
    const/4 v3, 0x1

    .line 1658
    aput-object v4, v8, v3

    .line 1660
    invoke-static {v8}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 1663
    move-result-object v3

    .line 1664
    invoke-virtual {v0, v3}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1667
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getAdditionalFingers()I

    .line 1670
    move-result v3

    .line 1671
    if-lez v3, :cond_722

    .line 1673
    const-wide/16 v51, 0x0

    .line 1675
    cmp-long v3, v43, v51

    .line 1677
    if-ltz v3, :cond_722

    .line 1679
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1682
    move-result v48

    .line 1683
    move-wide/from16 v45, v10

    .line 1685
    move-object/from16 v47, v32

    .line 1687
    invoke-static/range {v43 .. v48}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 1690
    move-result-object v3

    .line 1691
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 1694
    move-result v52

    .line 1695
    move-wide/from16 v47, v1

    .line 1697
    move-wide/from16 v49, v14

    .line 1699
    move-object/from16 v51, v32

    move-object/from16 v51, v32

    .line 1701
    invoke-static/range {v47 .. v52}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 1704
    move-result-object v1

    .line 1705
    const/4 v2, 0x2

    .line 1706
    new-array v4, v2, [Landroid/graphics/Point;

    .line 1708
    const/16 v27, 0x0

    .line 1710
    aput-object v3, v4, v27

    .line 1712
    const/4 v3, 0x1

    .line 1713
    aput-object v1, v4, v3

    .line 1715
    invoke-static {v4}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 1718
    move-result-object v1

    .line 1719
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1722
    :cond_722
    invoke-static {v0}, Lyj2;->k0(Ljava/lang/Iterable;)Ljava/util/ArrayList;

    .line 1725
    move-result-object v1

    .line 1726
    invoke-virtual {v9, v5, v6, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->N(JLjava/util/List;Ljava/util/List;)V

    .line 1729
    goto/16 :goto_cc1

    .line 1731
    :cond_72b
    move-wide/from16 v12, v19

    .line 1733
    move-object/from16 v1, v23

    .line 1735
    invoke-static {v12, v13, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 1738
    goto/16 :goto_cc1

    .line 1740
    :cond_734
    move-wide v10, v8

    .line 1741
    move-wide/from16 v12, v19

    .line 1743
    move-object v9, v1

    .line 1744
    move-object/from16 v1, v23

    move-object/from16 v1, v23

    .line 1746
    instance-of v4, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;

    .line 1748
    if-eqz v4, :cond_858

    .line 1750
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;

    .line 1752
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 1754
    const/16 v4, 0x18

    .line 1756
    if-ge v2, v4, :cond_74d

    .line 1758
    invoke-static {v12, v13, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 1761
    goto/16 :goto_cc1

    .line 1763
    :cond_74d
    invoke-virtual {v9, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 1766
    move-result-object v1

    .line 1767
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1770
    check-cast v1, Landroid/view/WindowManager;

    .line 1772
    invoke-interface {v1}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 1775
    move-result-object v1

    .line 1776
    new-instance v2, Landroid/graphics/Point;

    .line 1778
    invoke-direct {v2}, Landroid/graphics/Point;-><init>()V

    .line 1781
    invoke-virtual {v1, v2}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 1784
    new-instance v1, Landroid/graphics/Path;

    .line 1786
    invoke-direct {v1}, Landroid/graphics/Path;-><init>()V

    .line 1789
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1792
    move-result v3

    .line 1793
    if-eqz v3, :cond_77f

    .line 1795
    iget v3, v2, Landroid/graphics/Point;->x:I

    .line 1797
    invoke-static {v3, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1800
    move-result-wide v3

    .line 1801
    long-to-float v3, v3

    .line 1802
    iget v4, v2, Landroid/graphics/Point;->y:I

    .line 1804
    invoke-static {v4, v10, v11}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1807
    move-result-wide v14

    .line 1808
    long-to-float v4, v14

    .line 1809
    invoke-virtual {v1, v3, v4}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1812
    goto :goto_784

    .line 1813
    :cond_77f
    long-to-float v3, v5

    .line 1814
    long-to-float v4, v10

    .line 1815
    invoke-virtual {v1, v3, v4}, Landroid/graphics/Path;->moveTo(FF)V

    .line 1818
    :goto_784
    invoke-static {}, Li2;->a()Landroid/accessibilityservice/GestureDescription$Builder;

    .line 1821
    move-result-object v3

    .line 1822
    move-object/from16 v15, v28

    .line 1824
    array-length v4, v15

    .line 1825
    const/4 v8, 0x0

    .line 1826
    :goto_78c
    if-ge v8, v4, :cond_7c3

    .line 1828
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1831
    move-result v14

    .line 1832
    if-eqz v14, :cond_7af

    .line 1834
    move-wide/from16 v54, v5

    .line 1836
    move v6, v4

    .line 1837
    aget-wide v4, v15, v8

    .line 1839
    iget v14, v2, Landroid/graphics/Point;->x:I

    .line 1841
    invoke-static {v14, v4, v5}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1844
    move-result-wide v4

    .line 1845
    long-to-float v4, v4

    .line 1846
    move/from16 p1, v6

    .line 1848
    aget-wide v5, v29, v8

    .line 1850
    iget v14, v2, Landroid/graphics/Point;->y:I

    .line 1852
    invoke-static {v14, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 1855
    move-result-wide v5

    .line 1856
    long-to-float v5, v5

    .line 1857
    invoke-virtual {v1, v4, v5}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1860
    goto :goto_7bc

    .line 1861
    :cond_7af
    move/from16 p1, v4

    .line 1863
    move-wide/from16 v54, v5

    .line 1865
    aget-wide v4, v15, v8

    .line 1867
    long-to-float v4, v4

    .line 1868
    aget-wide v5, v29, v8

    .line 1870
    long-to-float v5, v5

    .line 1871
    invoke-virtual {v1, v4, v5}, Landroid/graphics/Path;->lineTo(FF)V

    .line 1874
    :goto_7bc
    add-int/lit8 v8, v8, 0x1

    .line 1876
    move/from16 v4, p1

    .line 1878
    move-wide/from16 v5, v54

    .line 1880
    goto :goto_78c

    .line 1881
    :cond_7c3
    move-wide/from16 v54, v5

    .line 1883
    const-wide/16 v4, 0x4e20

    .line 1885
    cmp-long v6, v30, v4

    .line 1887
    if-lez v6, :cond_7d3

    .line 1889
    const-string v6, "Gesture sequence element duration exceeds maximum (20 seconds). Forcing to 20 seconds"

    .line 1891
    invoke-static {v12, v13, v6}, Lkjf;->g(JLjava/lang/String;)V

    .line 1894
    move-wide/from16 v21, v4

    .line 1896
    goto :goto_7e0

    .line 1897
    :cond_7d3
    const-wide/16 v25, 0x1

    .line 1899
    cmp-long v4, v30, v25

    .line 1901
    if-gez v4, :cond_7de

    .line 1903
    const-wide/16 v21, 0x1

    const-wide/16 v21, 0x1

    .line 1905
    goto :goto_7e0

    .line 1906
    :cond_7de
    move-wide/from16 v21, v30

    .line 1908
    :goto_7e0
    new-instance v17, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 1910
    const-wide/16 v19, 0x0

    .line 1912
    move-object/from16 v18, v1

    move-object/from16 v18, v1

    .line 1914
    invoke-direct/range {v17 .. v22}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 1917
    move-object/from16 v1, v17

    .line 1919
    move-wide/from16 v4, v21

    .line 1921
    invoke-virtual {v3, v1}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 1924
    invoke-virtual {v3}, Landroid/accessibilityservice/GestureDescription$Builder;->build()Landroid/accessibilityservice/GestureDescription;

    .line 1927
    move-result-object v1

    .line 1928
    const/4 v3, 0x0

    .line 1929
    :try_start_7f7
    invoke-virtual {v9, v1, v3, v3}, Landroid/accessibilityservice/AccessibilityService;->dispatchGesture(Landroid/accessibilityservice/GestureDescription;Landroid/accessibilityservice/AccessibilityService$GestureResultCallback;Landroid/os/Handler;)Z

    .line 1932
    move-result v1

    .line 1933
    if-nez v1, :cond_815

    .line 1935
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V
    :try_end_800
    .catch Ljava/lang/Exception; {:try_start_7f7 .. :try_end_800} :catch_801

    .line 1938
    goto :goto_815

    .line 1939
    :catch_801
    move-exception v0

    .line 1940
    new-instance v1, Ljava/lang/StringBuilder;

    .line 1942
    const-string v3, "eef:ebuldqus eesi ar tnce"

    const-string v3, "Gesture sequence failed: "

    .line 1944
    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 1947
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 1950
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1953
    move-result-object v0

    .line 1954
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1957
    :cond_815
    :goto_815
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getShowTouchLocation()Z

    .line 1960
    move-result v0

    .line 1961
    if-eqz v0, :cond_cc1

    .line 1963
    new-instance v0, Ljava/util/ArrayList;

    .line 1965
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 1968
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1971
    move-result v26

    .line 1972
    move-object/from16 v25, v2

    move-object/from16 v25, v2

    .line 1974
    move-wide/from16 v23, v10

    .line 1976
    move-wide/from16 v21, v54

    .line 1978
    invoke-static/range {v21 .. v26}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 1981
    move-result-object v1

    .line 1982
    move-object/from16 v21, v25

    .line 1984
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1987
    array-length v1, v15

    .line 1988
    const/4 v2, 0x0

    .line 1989
    :goto_837
    if-ge v2, v1, :cond_84b

    .line 1991
    aget-wide v17, v15, v2

    .line 1993
    aget-wide v19, v29, v2

    .line 1995
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1998
    move-result v22

    .line 1999
    invoke-static/range {v17 .. v22}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->K(JJLandroid/graphics/Point;Z)Landroid/graphics/Point;

    .line 2002
    move-result-object v3

    .line 2003
    invoke-virtual {v0, v3}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 2006
    add-int/lit8 v2, v2, 0x1

    .line 2008
    goto :goto_837

    .line 2009
    :cond_84b
    invoke-static {v0}, Lmx2;->D(Ljava/lang/Object;)Ljava/util/List;

    .line 2012
    move-result-object v0

    .line 2013
    invoke-static {v0}, Lyj2;->k0(Ljava/lang/Iterable;)Ljava/util/ArrayList;

    .line 2016
    move-result-object v1

    .line 2017
    invoke-virtual {v9, v4, v5, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->N(JLjava/util/List;Ljava/util/List;)V

    .line 2020
    goto/16 :goto_cc1

    .line 2022
    :cond_858
    instance-of v0, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;

    .line 2024
    const/high16 v4, 0x40000000    # 2.0f

    .line 2026
    if-eqz v0, :cond_a6e

    .line 2028
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;

    .line 2030
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 2032
    const/16 v2, 0x18

    .line 2034
    if-ge v0, v2, :cond_86b

    .line 2036
    invoke-static {v12, v13, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 2039
    goto/16 :goto_cc1

    .line 2041
    :cond_86b
    invoke-virtual {v9, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 2044
    move-result-object v0

    .line 2045
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2048
    check-cast v0, Landroid/view/WindowManager;

    .line 2050
    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 2053
    move-result-object v0

    .line 2054
    new-instance v1, Landroid/graphics/Point;

    .line 2056
    invoke-direct {v1}, Landroid/graphics/Point;-><init>()V

    .line 2059
    invoke-virtual {v0, v1}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 2062
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getXyPercentages()Z

    .line 2065
    move-result v0

    .line 2066
    if-eqz v0, :cond_8c2

    .line 2068
    move-wide/from16 v5, v32

    .line 2070
    const-wide/16 v14, 0x0

    .line 2072
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2075
    move-result-wide v2

    .line 2076
    iget v0, v1, Landroid/graphics/Point;->x:I

    .line 2078
    invoke-static {v0, v2, v3}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2081
    move-result-wide v2

    .line 2082
    long-to-float v0, v2

    .line 2083
    move-wide/from16 v10, v35

    .line 2085
    invoke-static {v14, v15, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2088
    move-result-wide v2

    .line 2089
    iget v5, v1, Landroid/graphics/Point;->y:I

    .line 2091
    invoke-static {v5, v2, v3}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2094
    move-result-wide v2

    .line 2095
    long-to-float v2, v2

    .line 2096
    move-wide/from16 v5, v37

    .line 2098
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2101
    move-result-wide v5

    .line 2102
    iget v3, v1, Landroid/graphics/Point;->x:I

    .line 2104
    invoke-static {v3, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2107
    move-result-wide v5

    .line 2108
    long-to-float v3, v5

    .line 2109
    move-wide/from16 v5, v39

    .line 2111
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2114
    move-result-wide v5

    .line 2115
    iget v8, v1, Landroid/graphics/Point;->y:I

    .line 2117
    invoke-static {v8, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2120
    move-result-wide v5

    .line 2121
    long-to-float v5, v5

    .line 2122
    move v6, v5

    .line 2123
    move-object/from16 p1, v7

    .line 2125
    move v5, v2

    .line 2126
    :goto_8c0
    move v2, v0

    .line 2127
    goto :goto_8e6

    .line 2128
    :cond_8c2
    move-object/from16 p1, v7

    .line 2130
    move-wide/from16 v5, v32

    .line 2132
    move-wide/from16 v10, v35

    .line 2134
    move-wide/from16 v2, v37

    .line 2136
    move-wide/from16 v7, v39

    .line 2138
    const-wide/16 v14, 0x0

    const-wide/16 v14, 0x0

    .line 2140
    invoke-static {v14, v15, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2143
    move-result-wide v5

    .line 2144
    long-to-float v0, v5

    .line 2145
    invoke-static {v14, v15, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2148
    move-result-wide v5

    .line 2149
    long-to-float v5, v5

    .line 2150
    invoke-static {v14, v15, v2, v3}, Ljava/lang/Math;->max(JJ)J

    .line 2153
    move-result-wide v2

    .line 2154
    long-to-float v3, v2

    .line 2155
    invoke-static {v14, v15, v7, v8}, Ljava/lang/Math;->max(JJ)J

    .line 2158
    move-result-wide v6

    .line 2159
    long-to-float v2, v6

    .line 2160
    move v6, v2

    .line 2161
    goto :goto_8c0

    .line 2162
    :goto_8e6
    add-float v0, v2, v3

    .line 2164
    div-float/2addr v0, v4

    .line 2165
    add-float v7, v5, v6

    .line 2167
    div-float/2addr v7, v4

    .line 2168
    const-wide/16 v10, 0x64

    .line 2170
    move-wide/from16 v14, v41

    .line 2172
    invoke-static {v10, v11, v14, v15}, Ljava/lang/Math;->min(JJ)J

    .line 2175
    move-result-wide v10

    .line 2176
    const-wide/16 v14, 0x1

    .line 2178
    invoke-static {v14, v15, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2181
    move-result-wide v10

    .line 2182
    long-to-float v4, v10

    .line 2183
    const/high16 v8, 0x42c80000    # 100.0f

    .line 2185
    div-float/2addr v4, v8

    .line 2186
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomIn()Z

    .line 2189
    move-result v8

    .line 2190
    if-eqz v8, :cond_918

    .line 2192
    invoke-static {v0, v2, v4, v2}, Lq77;->t(FFFF)F

    .line 2195
    move-result v8

    .line 2196
    invoke-static {v7, v5, v4, v5}, Lq77;->t(FFFF)F

    .line 2199
    move-result v10

    .line 2200
    invoke-static {v0, v3, v4, v3}, Lq77;->t(FFFF)F

    .line 2203
    move-result v0

    .line 2204
    invoke-static {v7, v6, v4, v6}, Lq77;->t(FFFF)F

    .line 2207
    move-result v4

    .line 2208
    move v7, v4

    .line 2209
    move v4, v0

    move v4, v0

    .line 2210
    goto :goto_96c

    .line 2211
    :cond_918
    sub-float v37, v2, v0

    .line 2213
    sub-float v38, v5, v7

    .line 2215
    sub-float v8, v3, v0

    .line 2217
    sub-float v10, v6, v7

    .line 2219
    iget v11, v1, Landroid/graphics/Point;->x:I

    .line 2221
    int-to-float v11, v11

    .line 2222
    iget v14, v1, Landroid/graphics/Point;->y:I

    .line 2224
    int-to-float v14, v14

    .line 2225
    move/from16 v35, v0

    .line 2227
    move/from16 v36, v7

    move/from16 v36, v7

    .line 2229
    move/from16 v39, v11

    move/from16 v39, v11

    .line 2231
    move/from16 v40, v14

    move/from16 v40, v14

    .line 2233
    invoke-static/range {v35 .. v40}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->f(FFFFFF)F

    .line 2236
    move-result v0

    .line 2237
    move/from16 v7, v37

    move/from16 v7, v37

    .line 2239
    move/from16 v11, v38

    move/from16 v11, v38

    .line 2241
    iget v14, v1, Landroid/graphics/Point;->x:I

    .line 2243
    int-to-float v14, v14

    .line 2244
    iget v15, v1, Landroid/graphics/Point;->y:I

    .line 2246
    int-to-float v15, v15

    .line 2247
    move/from16 v37, v8

    .line 2249
    move/from16 v38, v10

    .line 2251
    move/from16 v39, v14

    .line 2253
    move/from16 v40, v15

    .line 2255
    invoke-static/range {v35 .. v40}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->f(FFFFFF)F

    .line 2258
    move-result v8

    .line 2259
    invoke-static {v0, v8}, Ljava/lang/Math;->min(FF)F

    .line 2262
    move-result v0

    .line 2263
    const/high16 v8, 0x3f800000    # 1.0f

    .line 2265
    sub-float/2addr v0, v8

    .line 2266
    mul-float/2addr v0, v4

    .line 2267
    add-float/2addr v0, v8

    .line 2268
    mul-float v4, v7, v0

    .line 2270
    add-float v8, v4, v35

    .line 2272
    mul-float v4, v11, v0

    .line 2274
    add-float v10, v4, v36

    .line 2276
    mul-float v4, v37, v0

    .line 2278
    add-float v4, v4, v35

    .line 2280
    mul-float v0, v0, v38

    .line 2282
    add-float v0, v0, v36

    .line 2284
    move v7, v0

    .line 2285
    :goto_96c
    new-instance v0, Landroid/graphics/Path;

    .line 2287
    invoke-direct {v0}, Landroid/graphics/Path;-><init>()V

    .line 2290
    invoke-virtual {v0, v2, v5}, Landroid/graphics/Path;->moveTo(FF)V

    .line 2293
    iget v11, v1, Landroid/graphics/Point;->x:I

    .line 2295
    int-to-float v11, v11

    .line 2296
    invoke-static {v8, v11}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2299
    move-result v11

    .line 2300
    iget v14, v1, Landroid/graphics/Point;->y:I

    .line 2302
    int-to-float v14, v14

    .line 2303
    invoke-static {v10, v14}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2306
    move-result v14

    .line 2307
    invoke-virtual {v0, v11, v14}, Landroid/graphics/Path;->lineTo(FF)V

    .line 2310
    new-instance v11, Landroid/graphics/Path;

    .line 2312
    invoke-direct {v11}, Landroid/graphics/Path;-><init>()V

    .line 2315
    invoke-virtual {v11, v3, v6}, Landroid/graphics/Path;->moveTo(FF)V

    .line 2318
    iget v14, v1, Landroid/graphics/Point;->x:I

    .line 2320
    int-to-float v14, v14

    .line 2321
    invoke-static {v4, v14}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2324
    move-result v14

    .line 2325
    iget v15, v1, Landroid/graphics/Point;->y:I

    .line 2327
    int-to-float v15, v15

    .line 2328
    invoke-static {v7, v15}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2331
    move-result v15

    .line 2332
    invoke-virtual {v11, v14, v15}, Landroid/graphics/Path;->lineTo(FF)V

    .line 2335
    move/from16 p2, v6

    move/from16 p2, v6

    .line 2337
    move/from16 v17, v7

    move/from16 v17, v7

    .line 2339
    move-wide/from16 v6, v21

    .line 2341
    move-wide/from16 v14, v30

    .line 2343
    invoke-static {v6, v7, v14, v15}, Ljava/lang/Math;->min(JJ)J

    .line 2346
    move-result-wide v6

    .line 2347
    const-wide/16 v14, 0x1

    const-wide/16 v14, 0x1

    .line 2349
    invoke-static {v14, v15, v6, v7}, Ljava/lang/Math;->max(JJ)J

    .line 2352
    move-result-wide v39

    .line 2353
    invoke-static {}, Li2;->a()Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2356
    move-result-object v6

    .line 2357
    new-instance v35, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 2359
    const-wide/16 v37, 0x0

    .line 2361
    move-object/from16 v36, v0

    .line 2363
    invoke-direct/range {v35 .. v40}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 2366
    move-object/from16 v0, v35

    .line 2368
    invoke-virtual {v6, v0}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2371
    new-instance v35, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 2373
    move-object/from16 v36, v11

    move-object/from16 v36, v11

    .line 2375
    invoke-direct/range {v35 .. v40}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 2378
    move-object/from16 v0, v35

    .line 2380
    move-wide/from16 v14, v39

    .line 2382
    invoke-virtual {v6, v0}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2385
    :try_start_9d8
    invoke-virtual {v6}, Landroid/accessibilityservice/GestureDescription$Builder;->build()Landroid/accessibilityservice/GestureDescription;

    .line 2388
    move-result-object v0

    .line 2389
    const/4 v7, 0x0

    .line 2390
    invoke-virtual {v9, v0, v7, v7}, Landroid/accessibilityservice/AccessibilityService;->dispatchGesture(Landroid/accessibilityservice/GestureDescription;Landroid/accessibilityservice/AccessibilityService$GestureResultCallback;Landroid/os/Handler;)Z

    .line 2393
    move-result v0

    .line 2394
    if-nez v0, :cond_9fd

    .line 2396
    const-string v0, "Failed to dispatch pinch zoom gesture"

    .line 2398
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V
    :try_end_9e8
    .catch Ljava/lang/Exception; {:try_start_9d8 .. :try_end_9e8} :catch_9e9

    .line 2401
    goto :goto_9fd

    .line 2402
    :catch_9e9
    move-exception v0

    .line 2403
    new-instance v6, Ljava/lang/StringBuilder;

    .line 2405
    const-string v7, "es dhnuolouP gc riem:te fzi"

    const-string v7, "Pinch zoom gesture failed: "

    .line 2407
    invoke-direct {v6, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 2410
    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 2413
    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 2416
    move-result-object v0

    .line 2417
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 2420
    :cond_9fd
    :goto_9fd
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getShowTouchLocation()Z

    .line 2423
    move-result v0

    .line 2424
    if-eqz v0, :cond_cc1

    .line 2426
    new-instance v0, Landroid/graphics/Point;

    .line 2428
    float-to-int v2, v2

    .line 2429
    float-to-int v5, v5

    .line 2430
    invoke-direct {v0, v2, v5}, Landroid/graphics/Point;-><init>(II)V

    .line 2433
    new-instance v2, Landroid/graphics/Point;

    .line 2435
    iget v5, v1, Landroid/graphics/Point;->x:I

    .line 2437
    int-to-float v5, v5

    .line 2438
    invoke-static {v8, v5}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2441
    move-result v5

    .line 2442
    float-to-int v5, v5

    .line 2443
    iget v6, v1, Landroid/graphics/Point;->y:I

    .line 2445
    int-to-float v6, v6

    .line 2446
    invoke-static {v10, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2449
    move-result v6

    .line 2450
    float-to-int v6, v6

    .line 2451
    invoke-direct {v2, v5, v6}, Landroid/graphics/Point;-><init>(II)V

    .line 2454
    const/4 v7, 0x2

    .line 2455
    new-array v5, v7, [Landroid/graphics/Point;

    .line 2457
    const/16 v27, 0x0

    .line 2459
    aput-object v0, v5, v27

    .line 2461
    const/4 v6, 0x1

    .line 2462
    aput-object v2, v5, v6

    .line 2464
    invoke-static {v5}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 2467
    move-result-object v0

    .line 2468
    new-instance v2, Landroid/graphics/Point;

    .line 2470
    float-to-int v3, v3

    .line 2471
    move/from16 v5, p2

    .line 2473
    float-to-int v5, v5

    .line 2474
    invoke-direct {v2, v3, v5}, Landroid/graphics/Point;-><init>(II)V

    .line 2477
    new-instance v3, Landroid/graphics/Point;

    .line 2479
    iget v5, v1, Landroid/graphics/Point;->x:I

    .line 2481
    int-to-float v5, v5

    .line 2482
    invoke-static {v4, v5}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2485
    move-result v4

    .line 2486
    float-to-int v4, v4

    .line 2487
    iget v1, v1, Landroid/graphics/Point;->y:I

    .line 2489
    int-to-float v1, v1

    .line 2490
    move/from16 v5, v17

    .line 2492
    invoke-static {v5, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2495
    move-result v1

    .line 2496
    float-to-int v1, v1

    .line 2497
    invoke-direct {v3, v4, v1}, Landroid/graphics/Point;-><init>(II)V

    .line 2500
    const/4 v7, 0x2

    .line 2501
    new-array v1, v7, [Landroid/graphics/Point;

    .line 2503
    const/16 v27, 0x0

    .line 2505
    aput-object v2, v1, v27

    .line 2507
    const/4 v4, 0x1

    .line 2508
    aput-object v3, v1, v4

    .line 2510
    invoke-static {v1}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 2513
    move-result-object v1

    .line 2514
    new-array v2, v7, [Ljava/util/List;

    .line 2516
    aput-object v0, v2, v27

    .line 2518
    aput-object v1, v2, v4

    .line 2520
    invoke-static {v2}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 2523
    move-result-object v0

    .line 2524
    invoke-static {v0}, Lyj2;->k0(Ljava/lang/Iterable;)Ljava/util/ArrayList;

    .line 2527
    move-result-object v1

    .line 2528
    invoke-virtual {v9, v14, v15, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->N(JLjava/util/List;Ljava/util/List;)V

    .line 2531
    goto/16 :goto_cc1

    .line 2533
    :cond_a6e
    move/from16 v17, v4

    .line 2535
    move-object v0, v7

    .line 2536
    move-wide/from16 v14, v30

    .line 2538
    move-wide/from16 v5, v32

    .line 2540
    move-wide/from16 v10, v35

    .line 2542
    move-wide/from16 v58, v37

    .line 2544
    move-wide/from16 v7, v39

    .line 2546
    instance-of v4, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;

    .line 2548
    if-eqz v4, :cond_c8f

    .line 2550
    move-object v2, v0

    .line 2551
    check-cast v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;

    .line 2553
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 2555
    const/16 v4, 0x18

    .line 2557
    if-ge v0, v4, :cond_a8d

    .line 2559
    invoke-static {v12, v13, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 2562
    goto/16 :goto_cc1

    .line 2564
    :cond_a8d
    invoke-virtual {v9, v3}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 2567
    move-result-object v0

    .line 2568
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2571
    check-cast v0, Landroid/view/WindowManager;

    .line 2573
    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 2576
    move-result-object v0

    .line 2577
    new-instance v1, Landroid/graphics/Point;

    .line 2579
    invoke-direct {v1}, Landroid/graphics/Point;-><init>()V

    .line 2582
    invoke-virtual {v0, v1}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 2585
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getXyPercentages()Z

    .line 2588
    move-result v0

    .line 2589
    if-eqz v0, :cond_adb

    .line 2591
    const-wide/16 v3, 0x0

    .line 2593
    invoke-static {v3, v4, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2596
    move-result-wide v5

    .line 2597
    iget v0, v1, Landroid/graphics/Point;->x:I

    .line 2599
    invoke-static {v0, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2602
    move-result-wide v5

    .line 2603
    long-to-float v0, v5

    .line 2604
    invoke-static {v3, v4, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2607
    move-result-wide v5

    .line 2608
    iget v10, v1, Landroid/graphics/Point;->y:I

    .line 2610
    invoke-static {v10, v5, v6}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2613
    move-result-wide v5

    .line 2614
    long-to-float v5, v5

    .line 2615
    move-wide/from16 v10, v58

    .line 2617
    invoke-static {v3, v4, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2620
    move-result-wide v10

    .line 2621
    iget v6, v1, Landroid/graphics/Point;->x:I

    .line 2623
    invoke-static {v6, v10, v11}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2626
    move-result-wide v10

    .line 2627
    long-to-float v6, v10

    .line 2628
    invoke-static {v3, v4, v7, v8}, Ljava/lang/Math;->max(JJ)J

    .line 2631
    move-result-wide v3

    .line 2632
    iget v7, v1, Landroid/graphics/Point;->y:I

    .line 2634
    invoke-static {v7, v3, v4}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->p(IJ)J

    .line 2637
    move-result-wide v3

    .line 2638
    long-to-float v3, v3

    .line 2639
    move-wide/from16 v19, v12

    .line 2641
    goto :goto_af5

    .line 2642
    :cond_adb
    move-wide/from16 v19, v12

    .line 2644
    move-wide/from16 v12, v58

    .line 2646
    const-wide/16 v3, 0x0

    .line 2648
    invoke-static {v3, v4, v5, v6}, Ljava/lang/Math;->max(JJ)J

    .line 2651
    move-result-wide v5

    .line 2652
    long-to-float v0, v5

    .line 2653
    invoke-static {v3, v4, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2656
    move-result-wide v5

    .line 2657
    long-to-float v5, v5

    .line 2658
    invoke-static {v3, v4, v12, v13}, Ljava/lang/Math;->max(JJ)J

    .line 2661
    move-result-wide v10

    .line 2662
    long-to-float v6, v10

    .line 2663
    invoke-static {v3, v4, v7, v8}, Ljava/lang/Math;->max(JJ)J

    .line 2666
    move-result-wide v3

    .line 2667
    long-to-float v3, v3

    .line 2668
    :goto_af5
    add-float v4, v0, v6

    .line 2670
    div-float v4, v4, v17

    .line 2672
    add-float v7, v5, v3

    .line 2674
    div-float v7, v7, v17

    .line 2676
    const-wide/16 v10, 0x168

    const-wide/16 v10, 0x168

    .line 2678
    move-wide/from16 v12, v43

    .line 2680
    invoke-static {v10, v11, v12, v13}, Ljava/lang/Math;->min(JJ)J

    .line 2683
    move-result-wide v10

    .line 2684
    const-wide/16 v12, -0x168

    .line 2686
    invoke-static {v12, v13, v10, v11}, Ljava/lang/Math;->max(JJ)J

    .line 2689
    move-result-wide v10

    .line 2690
    long-to-float v8, v10

    .line 2691
    float-to-double v10, v8

    .line 2692
    invoke-static {v10, v11}, Ljava/lang/Math;->toRadians(D)D

    .line 2695
    move-result-wide v10

    .line 2696
    invoke-static {v8}, Ljava/lang/Math;->abs(F)F

    .line 2699
    move-result v8

    .line 2700
    const/high16 v12, 0x40a00000    # 5.0f

    .line 2702
    div-float/2addr v8, v12

    .line 2703
    float-to-int v8, v8

    .line 2704
    const/16 v12, 0x8

    .line 2706
    invoke-static {v12, v8}, Ljava/lang/Math;->max(II)I

    .line 2709
    move-result v8

    .line 2710
    new-instance v12, Landroid/graphics/Path;

    .line 2712
    invoke-direct {v12}, Landroid/graphics/Path;-><init>()V

    .line 2715
    new-instance v13, Landroid/graphics/Path;

    .line 2717
    invoke-direct {v13}, Landroid/graphics/Path;-><init>()V

    .line 2720
    invoke-virtual {v12, v0, v5}, Landroid/graphics/Path;->moveTo(FF)V

    .line 2723
    invoke-virtual {v13, v6, v3}, Landroid/graphics/Path;->moveTo(FF)V

    .line 2726
    move-object/from16 p1, v2

    .line 2728
    new-instance v2, Landroid/graphics/Point;

    .line 2730
    move-wide/from16 v17, v10

    .line 2732
    float-to-int v10, v0

    .line 2733
    float-to-int v11, v5

    .line 2734
    invoke-direct {v2, v10, v11}, Landroid/graphics/Point;-><init>(II)V

    .line 2737
    const/4 v10, 0x1

    .line 2738
    new-array v11, v10, [Landroid/graphics/Point;

    .line 2740
    const/16 v27, 0x0

    .line 2742
    aput-object v2, v11, v27

    .line 2744
    invoke-static {v11}, Lmx2;->I([Ljava/lang/Object;)Ljava/util/ArrayList;

    .line 2747
    move-result-object v2

    .line 2748
    new-instance v11, Landroid/graphics/Point;

    .line 2750
    float-to-int v10, v6

    .line 2751
    move/from16 p2, v0

    .line 2753
    float-to-int v0, v3

    .line 2754
    invoke-direct {v11, v10, v0}, Landroid/graphics/Point;-><init>(II)V

    .line 2757
    const/4 v10, 0x1

    .line 2758
    new-array v0, v10, [Landroid/graphics/Point;

    .line 2760
    aput-object v11, v0, v27

    .line 2762
    invoke-static {v0}, Lmx2;->I([Ljava/lang/Object;)Ljava/util/ArrayList;

    .line 2765
    move-result-object v11

    .line 2766
    sub-float v0, p2, v4

    .line 2768
    move-object/from16 p2, v11

    .line 2770
    float-to-double v10, v0

    .line 2771
    sub-float/2addr v5, v7

    .line 2772
    move v0, v6

    .line 2773
    float-to-double v5, v5

    .line 2774
    sub-float/2addr v0, v4

    .line 2775
    move-wide/from16 v23, v5

    .line 2777
    float-to-double v5, v0

    .line 2778
    sub-float/2addr v3, v7

    .line 2779
    move-wide/from16 v28, v5

    .line 2781
    float-to-double v5, v3

    .line 2782
    const/4 v3, 0x1

    .line 2783
    if-gt v3, v8, :cond_bfb

    .line 2785
    move-wide/from16 v30, v5

    .line 2787
    const/4 v0, 0x1

    .line 2788
    :goto_b6f
    int-to-double v5, v0

    .line 2789
    mul-double v5, v5, v17

    .line 2791
    move-wide/from16 v32, v5

    .line 2793
    int-to-double v5, v8

    .line 2794
    div-double v5, v32, v5

    .line 2796
    invoke-static {v5, v6}, Ljava/lang/Math;->cos(D)D

    .line 2799
    move-result-wide v32

    .line 2800
    invoke-static {v5, v6}, Ljava/lang/Math;->sin(D)D

    .line 2803
    move-result-wide v5

    .line 2804
    move-wide/from16 v35, v5

    .line 2806
    float-to-double v5, v4

    .line 2807
    mul-double v37, v10, v32

    .line 2809
    add-double v37, v37, v5

    .line 2811
    mul-double v39, v23, v35

    .line 2813
    move/from16 v41, v4

    .line 2815
    sub-double v3, v37, v39

    .line 2817
    double-to-float v3, v3

    .line 2818
    move-wide/from16 v37, v5

    .line 2820
    float-to-double v4, v7

    .line 2821
    mul-double v39, v10, v35

    .line 2823
    add-double v39, v39, v4

    .line 2825
    mul-double v42, v23, v32

    .line 2827
    move-wide/from16 v44, v4

    .line 2829
    add-double v4, v42, v39

    .line 2831
    double-to-float v4, v4

    .line 2832
    mul-double v5, v28, v32

    .line 2834
    add-double v5, v5, v37

    .line 2836
    mul-double v37, v30, v35

    .line 2838
    sub-double v5, v5, v37

    .line 2840
    double-to-float v5, v5

    .line 2841
    mul-double v35, v35, v28

    .line 2843
    add-double v35, v35, v44

    .line 2845
    mul-double v32, v32, v30

    .line 2847
    move/from16 v37, v7

    .line 2849
    add-double v6, v32, v35

    .line 2851
    double-to-float v6, v6

    .line 2852
    iget v7, v1, Landroid/graphics/Point;->x:I

    .line 2854
    int-to-float v7, v7

    .line 2855
    invoke-static {v3, v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2858
    move-result v3

    .line 2859
    iget v7, v1, Landroid/graphics/Point;->y:I

    .line 2861
    int-to-float v7, v7

    .line 2862
    invoke-static {v4, v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2865
    move-result v4

    .line 2866
    iget v7, v1, Landroid/graphics/Point;->x:I

    .line 2868
    int-to-float v7, v7

    .line 2869
    invoke-static {v5, v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2872
    move-result v5

    .line 2873
    iget v7, v1, Landroid/graphics/Point;->y:I

    .line 2875
    int-to-float v7, v7

    .line 2876
    invoke-static {v6, v7}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->g(FF)F

    .line 2879
    move-result v6

    .line 2880
    invoke-virtual {v12, v3, v4}, Landroid/graphics/Path;->lineTo(FF)V

    .line 2883
    invoke-virtual {v13, v5, v6}, Landroid/graphics/Path;->lineTo(FF)V

    .line 2886
    new-instance v7, Landroid/graphics/Point;

    .line 2888
    float-to-int v3, v3

    .line 2889
    float-to-int v4, v4

    .line 2890
    invoke-direct {v7, v3, v4}, Landroid/graphics/Point;-><init>(II)V

    .line 2893
    invoke-virtual {v2, v7}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 2896
    new-instance v3, Landroid/graphics/Point;

    .line 2898
    float-to-int v4, v5

    .line 2899
    float-to-int v5, v6

    .line 2900
    invoke-direct {v3, v4, v5}, Landroid/graphics/Point;-><init>(II)V

    .line 2903
    move-object/from16 v4, p2

    .line 2905
    invoke-virtual {v4, v3}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 2908
    if-eq v0, v8, :cond_bf7

    .line 2910
    add-int/lit8 v0, v0, 0x1

    .line 2912
    move-object/from16 p2, v4

    move-object/from16 p2, v4

    .line 2914
    move/from16 v7, v37

    .line 2916
    move/from16 v4, v41

    move/from16 v4, v41

    .line 2918
    goto/16 :goto_b6f

    .line 2920
    :cond_bf7
    :goto_bf7
    const-wide/32 v6, 0xea60

    .line 2923
    goto :goto_bfe

    .line 2924
    :cond_bfb
    move-object/from16 v4, p2

    .line 2926
    goto :goto_bf7

    .line 2927
    :goto_bfe
    invoke-static {v6, v7, v14, v15}, Ljava/lang/Math;->min(JJ)J

    .line 2930
    move-result-wide v0

    .line 2931
    const-wide/16 v14, 0x1

    .line 2933
    invoke-static {v14, v15, v0, v1}, Ljava/lang/Math;->max(JJ)J

    .line 2936
    move-result-wide v32

    .line 2937
    invoke-static {}, Li2;->a()Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2940
    move-result-object v0

    .line 2941
    new-instance v28, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 2943
    const-wide/16 v30, 0x0

    .line 2945
    move-object/from16 v29, v12

    move-object/from16 v29, v12

    .line 2947
    invoke-direct/range {v28 .. v33}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 2950
    move-object/from16 v1, v28

    move-object/from16 v1, v28

    .line 2952
    invoke-virtual {v0, v1}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2955
    new-instance v28, Landroid/accessibilityservice/GestureDescription$StrokeDescription;

    .line 2957
    move-object/from16 v29, v13

    move-object/from16 v29, v13

    .line 2959
    invoke-direct/range {v28 .. v33}, Landroid/accessibilityservice/GestureDescription$StrokeDescription;-><init>(Landroid/graphics/Path;JJ)V

    .line 2962
    move-object/from16 v1, v28

    .line 2964
    move-wide/from16 v5, v32

    .line 2966
    invoke-virtual {v0, v1}, Landroid/accessibilityservice/GestureDescription$Builder;->addStroke(Landroid/accessibilityservice/GestureDescription$StrokeDescription;)Landroid/accessibilityservice/GestureDescription$Builder;

    .line 2969
    :try_start_c2e
    invoke-virtual {v0}, Landroid/accessibilityservice/GestureDescription$Builder;->build()Landroid/accessibilityservice/GestureDescription;

    .line 2972
    move-result-object v0

    .line 2973
    const/4 v7, 0x0

    .line 2974
    invoke-virtual {v9, v0, v7, v7}, Landroid/accessibilityservice/AccessibilityService;->dispatchGesture(Landroid/accessibilityservice/GestureDescription;Landroid/accessibilityservice/AccessibilityService$GestureResultCallback;Landroid/os/Handler;)Z

    .line 2977
    move-result v0

    .line 2978
    if-nez v0, :cond_c57

    .line 2980
    const-string v0, "Failed to dispatch two finger rotate gesture"
    :try_end_c3b
    .catch Ljava/lang/Exception; {:try_start_c2e .. :try_end_c3b} :catch_c43

    .line 2982
    move-wide/from16 v14, v19

    .line 2984
    :try_start_c3d
    invoke-static {v14, v15, v0}, Lkjf;->g(JLjava/lang/String;)V
    :try_end_c40
    .catch Ljava/lang/Exception; {:try_start_c3d .. :try_end_c40} :catch_c41

    .line 2987
    goto :goto_c57

    .line 2988
    :catch_c41
    move-exception v0

    .line 2989
    goto :goto_c46

    .line 2990
    :catch_c43
    move-exception v0

    .line 2991
    move-wide/from16 v14, v19

    .line 2993
    :goto_c46
    new-instance v1, Ljava/lang/StringBuilder;

    .line 2995
    const-string v3, "Two finger rotate gesture failed: "

    .line 2997
    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 3000
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 3003
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 3006
    move-result-object v0

    .line 3007
    invoke-static {v14, v15, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 3010
    :cond_c57
    :goto_c57
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getShowTouchLocation()Z

    .line 3013
    move-result v0

    .line 3014
    if-eqz v0, :cond_cc1

    .line 3016
    const/4 v7, 0x2

    .line 3017
    new-array v0, v7, [Ljava/util/List;

    .line 3019
    const/16 v27, 0x0

    .line 3021
    aput-object v2, v0, v27

    .line 3023
    const/4 v3, 0x1

    .line 3024
    aput-object v4, v0, v3

    .line 3026
    invoke-static {v0}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 3029
    move-result-object v0

    .line 3030
    const/4 v1, 0x4

    .line 3031
    new-array v1, v1, [Landroid/graphics/Point;

    .line 3033
    invoke-static {v2}, Lxj2;->B0(Ljava/util/List;)Ljava/lang/Object;

    .line 3036
    move-result-object v8

    .line 3037
    aput-object v8, v1, v27

    .line 3039
    invoke-static {v2}, Lxj2;->K0(Ljava/util/List;)Ljava/lang/Object;

    .line 3042
    move-result-object v2

    .line 3043
    aput-object v2, v1, v3

    .line 3045
    invoke-static {v4}, Lxj2;->B0(Ljava/util/List;)Ljava/lang/Object;

    .line 3048
    move-result-object v2

    .line 3049
    aput-object v2, v1, v7

    .line 3051
    const/4 v2, 0x3

    .line 3052
    invoke-static {v4}, Lxj2;->K0(Ljava/util/List;)Ljava/lang/Object;

    .line 3055
    move-result-object v3

    .line 3056
    aput-object v3, v1, v2

    .line 3058
    invoke-static {v1}, Lmx2;->E([Ljava/lang/Object;)Ljava/util/List;

    .line 3061
    move-result-object v1

    .line 3062
    invoke-virtual {v9, v5, v6, v0, v1}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->N(JLjava/util/List;Ljava/util/List;)V

    .line 3065
    goto :goto_cc1

    .line 3066
    :cond_c8f
    move-wide v14, v12

    .line 3067
    instance-of v1, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PressBack;

    .line 3069
    if-eqz v1, :cond_c99

    .line 3071
    const/4 v3, 0x1

    .line 3072
    invoke-virtual {v9, v3}, Landroid/accessibilityservice/AccessibilityService;->performGlobalAction(I)Z

    .line 3075
    goto :goto_cc1

    .line 3076
    :cond_c99
    const/4 v3, 0x1

    .line 3077
    instance-of v0, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PressEnter;

    .line 3079
    if-eqz v0, :cond_cc1

    .line 3081
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 3083
    const/16 v7, 0x1e

    .line 3085
    if-lt v0, v7, :cond_cba

    .line 3087
    invoke-virtual {v9, v3}, Landroid/accessibilityservice/AccessibilityService;->findFocus(I)Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 3090
    move-result-object v0

    .line 3091
    if-eqz v0, :cond_cb6

    .line 3093
    invoke-static {}, Lsq1;->q()Landroid/view/accessibility/AccessibilityNodeInfo$AccessibilityAction;

    .line 3096
    move-result-object v1

    .line 3097
    invoke-virtual {v1}, Landroid/view/accessibility/AccessibilityNodeInfo$AccessibilityAction;->getId()I

    .line 3100
    move-result v1

    .line 3101
    invoke-virtual {v0, v1}, Landroid/view/accessibility/AccessibilityNodeInfo;->performAction(I)Z

    .line 3104
    goto :goto_cc1

    .line 3105
    :cond_cb6
    invoke-static {v14, v15, v2}, Lkjf;->g(JLjava/lang/String;)V

    .line 3108
    goto :goto_cc1

    .line 3109
    :cond_cba
    const-string v0, "e ri oApdPieerdbonEor sta.eussq1vnr1 r  r"

    const-string v0, "Press Enter requires Android 11 or above."

    .line 3111
    invoke-static {v14, v15, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 3114
    :cond_cc1
    :goto_cc1
    const/16 v34, 0x2

    .line 3116
    :goto_cc3
    return v34
.end method
