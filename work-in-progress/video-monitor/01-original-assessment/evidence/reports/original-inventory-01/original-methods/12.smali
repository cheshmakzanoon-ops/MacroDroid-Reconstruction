.method public checkAllPermissions(Z)Z
    .locals 9

    .line 1
    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 3
    const/4 v1, 0x1

    .line 4
    const/4 v8, 0x4

    if-eqz v0, :cond_8

    .line 6
    goto/16 :goto_43e

    .line 8
    :cond_8
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresWriteSettings()Z

    .line 11
    move-result v0

    .line 12
    const/4 v8, 0x4

    const/4 v2, 0x0

    .line 13
    const/4 v3, 0x6

    const/4 v3, 0x0

    .line 14
    if-eqz v0, :cond_30

    .line 16
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 19
    move-result-object v0

    .line 20
    invoke-static {v0}, Landroid/provider/Settings$System;->canWrite(Landroid/content/Context;)Z

    .line 23
    move-result v0

    .line 24
    if-nez v0, :cond_30

    .line 26
    const-string p1, "Missing write settings permission"

    .line 28
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 31
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 34
    move-result-object p1

    .line 35
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 38
    move-result-object p0

    .line 39
    invoke-static {p1, p0, v2, v1}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 42
    const/4 v8, 0x6

    return v3

    .line 43
    :cond_30
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanDrawOverlays()Z

    .line 46
    move-result v0

    .line 47
    const/4 v4, 0x2

    .line 48
    if-eqz v0, :cond_77

    .line 50
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 53
    move-result-object v0

    .line 54
    invoke-static {v0}, Llob;->a(Landroid/content/Context;)Z

    .line 57
    move-result v0

    .line 58
    const/4 v8, 0x3

    if-nez v0, :cond_77

    .line 60
    const/4 v8, 0x5

    new-instance p1, Ljava/lang/StringBuilder;

    .line 62
    const-string v0, "Cannot run "

    .line 64
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 67
    const/4 v8, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 70
    move-result-object v0

    .line 71
    const/4 v8, 0x2

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 74
    const-string v0, " - the display over other apps permission is not enabled"

    .line 76
    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 79
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 82
    move-result-object p1

    .line 83
    const/4 v8, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 86
    move-result-object v0

    .line 87
    const/4 v8, 0x0

    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 90
    move-result-wide v0

    .line 91
    const/4 v8, 0x0

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 94
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 97
    move-result-object p1

    .line 98
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 101
    move-result-object p0

    .line 102
    invoke-static {p1, p0, v2, v4}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 105
    return v3

    .line 106
    :cond_77
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanShowBubbles()Z

    .line 109
    move-result v0

    .line 110
    const/4 v8, 0x4

    if-eqz v0, :cond_cc

    .line 112
    const/4 v8, 0x3

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 114
    const/16 v5, 0x1d

    .line 116
    const/4 v8, 0x1

    if-ge v0, v5, :cond_88

    .line 118
    goto/16 :goto_43e

    .line 120
    :cond_88
    :try_start_88
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 123
    move-result-object v0

    .line 124
    invoke-virtual {v0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 127
    move-result-object v0

    .line 128
    const/4 v8, 0x1

    const-string v5, "notification_bubbles"

    .line 130
    const/4 v8, 0x3

    invoke-static {v0, v5}, Landroid/provider/Settings$Global;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 133
    move-result v0
    :try_end_99
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_88 .. :try_end_99} :catch_9f

    .line 134
    const/4 v8, 0x5

    if-ne v0, v1, :cond_9d

    .line 136
    goto :goto_9f

    .line 137
    :cond_9d
    move v0, v3

    .line 138
    goto :goto_a0

    .line 139
    :catch_9f
    :goto_9f
    move v0, v1

    .line 140
    :goto_a0
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 143
    move-result-object v5

    .line 144
    const/4 v8, 0x7

    const-class v6, Landroid/app/NotificationManager;

    .line 146
    invoke-virtual {v5, v6}, Landroid/content/Context;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    .line 149
    move-result-object v5

    .line 150
    check-cast v5, Landroid/app/NotificationManager;

    .line 152
    if-eqz v0, :cond_b8

    .line 154
    invoke-virtual {v5}, Landroid/app/NotificationManager;->areBubblesAllowed()Z

    .line 157
    move-result v0

    .line 158
    const/4 v8, 0x4

    if-eqz v0, :cond_b8

    .line 160
    const/4 v8, 0x3

    goto :goto_cc

    .line 161
    :cond_b8
    const-string p1, "Missing show bubbles permission"

    .line 163
    const/4 v8, 0x0

    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 166
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 169
    move-result-object p1

    .line 170
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 173
    move-result-object p0

    .line 174
    const/16 v0, 0xf

    .line 176
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 179
    return v3

    .line 180
    :cond_cc
    :goto_cc
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresLocationServicesEnabled()Z

    .line 183
    move-result v0

    .line 184
    if-eqz v0, :cond_f4

    .line 186
    :try_start_d3
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 189
    move-result-object v0

    .line 190
    invoke-virtual {v0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 193
    move-result-object v0

    .line 194
    const-string v5, "ldscaon_mioet"

    const-string v5, "location_mode"

    .line 196
    invoke-static {v0, v5}, Landroid/provider/Settings$Secure;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 199
    move-result v0
    :try_end_e3
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_d3 .. :try_end_e3} :catch_f4

    .line 200
    if-eqz v0, :cond_e6

    .line 202
    goto :goto_f4

    .line 203
    :cond_e6
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 206
    move-result-object p1

    .line 207
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 210
    move-result-object p0

    .line 211
    const/16 v0, 0xb

    .line 213
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 216
    return v3

    .line 217
    :catch_f4
    :cond_f4
    :goto_f4
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUsageAccess()Z

    .line 220
    move-result v0

    .line 221
    if-eqz v0, :cond_13b

    .line 223
    :try_start_fa
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 226
    move-result-object v0

    .line 227
    invoke-virtual {v0}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 230
    move-result-object v0

    .line 231
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 234
    move-result-object v5

    .line 235
    invoke-virtual {v5}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 238
    move-result-object v5

    .line 239
    invoke-virtual {v0, v5, v3}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;I)Landroid/content/pm/ApplicationInfo;

    .line 242
    move-result-object v0

    .line 243
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 246
    move-result-object v5

    .line 247
    const-string v6, "aopmps"

    const-string v6, "appops"

    .line 249
    invoke-virtual {v5, v6}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 252
    move-result-object v5

    .line 253
    const/4 v8, 0x0

    check-cast v5, Landroid/app/AppOpsManager;

    .line 255
    const-string v6, "android:get_usage_stats"

    .line 257
    iget v7, v0, Landroid/content/pm/ApplicationInfo;->uid:I

    .line 259
    iget-object v0, v0, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    .line 261
    invoke-virtual {v5, v6, v7, v0}, Landroid/app/AppOpsManager;->checkOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 264
    move-result v0
    :try_end_129
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_fa .. :try_end_129} :catch_12d

    .line 265
    const/4 v8, 0x1

    if-nez v0, :cond_12d

    .line 267
    goto :goto_13b

    .line 268
    :catch_12d
    :cond_12d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 271
    move-result-object p1

    .line 272
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 275
    move-result-object p0

    .line 276
    const/4 v0, 0x3

    .line 277
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 280
    const/4 v8, 0x5

    return v3

    .line 281
    :cond_13b
    :goto_13b
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessibility()Z

    .line 284
    move-result v0

    .line 285
    const-wide/16 v5, 0x7d0

    .line 287
    const/4 v8, 0x3

    if-eqz v0, :cond_179

    .line 289
    const/4 v8, 0x7

    if-eqz p1, :cond_15a

    .line 291
    new-instance v0, Landroid/os/Handler;

    .line 293
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 296
    move-result-object v7

    .line 297
    invoke-direct {v0, v7}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 300
    new-instance v7, Lsl9;

    .line 302
    const/4 v8, 0x1

    invoke-direct {v7, v1, p0}, Lsl9;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 305
    invoke-virtual {v0, v7, v5, v6}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 308
    goto :goto_179

    .line 309
    :cond_15a
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 312
    move-result-object v0

    .line 313
    const/4 v8, 0x2

    invoke-static {v0}, Lhtg;->I(Landroid/content/Context;)Z

    .line 316
    move-result v0

    .line 317
    if-nez v0, :cond_179

    .line 319
    const-string p1, "Accessibility service is not enabled"

    .line 321
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 324
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 327
    move-result-object p1

    .line 328
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 331
    move-result-object p0

    .line 332
    const/4 v8, 0x7

    const/4 v0, 0x4

    .line 333
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 336
    const/4 v8, 0x7

    return v3

    .line 337
    :cond_179
    :goto_179
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUIInteractionAccessibility()Z

    .line 340
    move-result v0

    .line 341
    if-eqz v0, :cond_1b9

    .line 343
    if-eqz p1, :cond_196

    .line 345
    const/4 v8, 0x4

    new-instance p1, Landroid/os/Handler;

    .line 347
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 350
    move-result-object v0

    .line 351
    const/4 v8, 0x2

    invoke-direct {p1, v0}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 354
    new-instance v0, Lsl9;

    .line 356
    invoke-direct {v0, v4, p0}, Lsl9;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 359
    invoke-virtual {p1, v0, v5, v6}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 362
    goto :goto_1b9

    .line 363
    :cond_196
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 366
    move-result-object p1

    .line 367
    const/4 v8, 0x6

    invoke-static {p1}, Lhtg;->J(Landroid/content/Context;)Z

    .line 370
    move-result p1

    .line 371
    const/4 v8, 0x5

    if-nez p1, :cond_1b9

    .line 373
    const-string p1, "UI interaction accessibility service is not enabled"

    .line 375
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 378
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 381
    move-result-object p1

    .line 382
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 385
    move-result-object p0

    .line 386
    const/4 v8, 0x7

    const/16 v0, 0xa

    .line 388
    const/4 v8, 0x4

    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 391
    const/4 v8, 0x3

    return v3

    .line 392
    :cond_1b9
    :goto_1b9
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDeviceAdmin()Z

    .line 395
    move-result p1

    .line 396
    if-eqz p1, :cond_1f6

    .line 398
    const/4 v8, 0x0

    new-instance p1, Landroid/content/ComponentName;

    .line 400
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 403
    move-result-object v0

    .line 404
    const-class v4, Lcom/arlosoft/macrodroid/triggers/receivers/MacroDroidDeviceAdminReceiver;

    .line 406
    invoke-direct {p1, v0, v4}, Landroid/content/ComponentName;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 409
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 412
    move-result-object v0

    .line 413
    const-string v4, "device_policy"

    .line 415
    invoke-virtual {v0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 418
    move-result-object v0

    .line 419
    const/4 v8, 0x3

    check-cast v0, Landroid/app/admin/DevicePolicyManager;

    .line 421
    invoke-virtual {v0, p1}, Landroid/app/admin/DevicePolicyManager;->isAdminActive(Landroid/content/ComponentName;)Z

    .line 424
    move-result p1

    .line 425
    if-nez p1, :cond_1f6

    .line 427
    const/4 v8, 0x0

    const-string p1, "Device admin access for MacroDroid is not enabled"

    .line 429
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 432
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 435
    move-result-object p1

    .line 436
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 439
    move-result-object p0

    .line 440
    const/4 v8, 0x1

    const/4 v0, 0x5

    .line 441
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 444
    const/4 v8, 0x0

    return v3

    .line 445
    :cond_1f6
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNotificationAccess()Z

    .line 448
    move-result p1

    .line 449
    if-eqz p1, :cond_247

    .line 451
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 454
    move-result-object p1

    .line 455
    const/4 v8, 0x2

    invoke-virtual {p1}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 458
    move-result-object p1

    .line 459
    const/4 v8, 0x2

    const-string v0, "enabled_notification_listeners"

    .line 461
    invoke-static {p1, v0}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    .line 464
    move-result-object p1

    .line 465
    const/4 v8, 0x3

    if-eqz p1, :cond_234

    .line 467
    const/4 v8, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 470
    move-result-object v0

    .line 471
    invoke-virtual {v0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 474
    move-result-object v0

    .line 475
    const/4 v8, 0x1

    invoke-virtual {p1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 478
    move-result v0

    .line 479
    const/4 v8, 0x4

    if-eqz v0, :cond_234

    .line 481
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 483
    const/16 v4, 0x1a

    .line 485
    if-lt v0, v4, :cond_247

    .line 487
    const/4 v8, 0x4

    const-class v0, Lcom/arlosoft/macrodroid/triggers/services/NotificationServiceOreo;

    .line 489
    invoke-virtual {v0}, Ljava/lang/Class;->getName()Ljava/lang/String;

    .line 492
    move-result-object v0

    .line 493
    const/4 v8, 0x6

    invoke-virtual {p1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 496
    move-result p1

    .line 497
    if-nez p1, :cond_247

    .line 499
    :cond_234
    const-string p1, "Notification access for MacroDroid is not enabled"

    .line 501
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 504
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 507
    move-result-object p1

    .line 508
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 511
    move-result-object p0

    .line 512
    const/4 v8, 0x6

    const/4 v0, 0x6

    .line 513
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 516
    return v3

    .line 517
    :cond_247
    const/4 v8, 0x7

    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 519
    const/16 v0, 0x18

    .line 521
    const/4 v8, 0x4

    if-lt p1, v0, :cond_27f

    .line 523
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessNotificationPolicy()Z

    .line 526
    move-result v0

    .line 527
    const/4 v8, 0x6

    if-eqz v0, :cond_27f

    .line 529
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 532
    move-result-object v0

    .line 533
    const-string v4, "aincontiifoo"

    const-string v4, "notification"

    .line 535
    const/4 v8, 0x7

    invoke-virtual {v0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 538
    move-result-object v0

    .line 539
    check-cast v0, Landroid/app/NotificationManager;

    .line 541
    invoke-virtual {v0}, Landroid/app/NotificationManager;->isNotificationPolicyAccessGranted()Z

    .line 544
    move-result v0

    .line 545
    if-nez v0, :cond_27f

    .line 547
    const/4 v8, 0x1

    const-string p1, "Notification policy access for MacroDroid is not enabled"

    .line 549
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 552
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 555
    move-result-object p1

    .line 556
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 559
    move-result-object p0

    .line 560
    const/4 v0, 0x7

    .line 561
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 564
    return v3

    .line 565
    :cond_27f
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDefaultAssist()Z

    .line 568
    move-result v0

    .line 569
    const/4 v8, 0x1

    if-eqz v0, :cond_2a7

    .line 571
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 574
    move-result-object v0

    .line 575
    invoke-static {v0}, Lgi0;->d(Landroid/content/Context;)Z

    .line 578
    move-result v0

    .line 579
    const/4 v8, 0x6

    if-nez v0, :cond_2a7

    .line 581
    const-string p1, "Default app permission for MacroDroid is not enabled"

    .line 583
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 586
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 589
    move-result-object p1

    .line 590
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 593
    move-result-object p0

    .line 594
    const/16 v0, 0xc

    .line 596
    const/4 v8, 0x3

    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 599
    return v3

    .line 600
    :cond_2a7
    const/4 v8, 0x4

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    .line 603
    move-result-wide v4

    .line 604
    const/4 v8, 0x2

    sget-object v0, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->E:Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;

    .line 606
    const/4 v8, 0x2

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 609
    sget-wide v6, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->G:J

    .line 611
    sub-long/2addr v4, v6

    .line 612
    const-wide/16 v6, 0x3e8

    const-wide/16 v6, 0x3e8

    .line 614
    div-long/2addr v4, v6

    .line 615
    const/4 v8, 0x1

    const-wide/16 v6, 0x3c

    .line 617
    cmp-long v0, v4, v6

    .line 619
    const/4 v8, 0x7

    if-lez v0, :cond_33a

    .line 621
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresShizuku()Z

    .line 624
    move-result v0

    .line 625
    if-eqz v0, :cond_33a

    .line 627
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 630
    move-result-object v0

    .line 631
    const/4 v8, 0x4

    iget-object v0, v0, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->n:Ldje;

    .line 633
    invoke-virtual {v0, v3}, Ldje;->c(Z)Ljje;

    .line 636
    move-result-object v0

    .line 637
    sget-object v4, Ljje;->GRANTED:Ljje;

    .line 639
    if-eq v0, v4, :cond_33a

    .line 641
    sget-object p1, Ljje;->VERSION_NOT_SUPPORTED:Ljje;

    .line 643
    if-ne v0, p1, :cond_2ef

    .line 645
    const p1, 0x7f14141b

    .line 648
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 651
    move-result-object p1

    .line 652
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 655
    move-result-wide v0

    .line 656
    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 659
    const/16 p1, 0x10

    .line 661
    const/4 v8, 0x1

    goto :goto_32d

    .line 662
    :cond_2ef
    sget-object p1, Ljje;->NOT_INSTALLED:Ljje;

    .line 664
    if-ne v0, p1, :cond_306

    .line 666
    const p1, 0x7f141417

    .line 669
    const/4 v8, 0x5

    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 672
    move-result-object p1

    .line 673
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 676
    move-result-wide v0

    .line 677
    const/4 v8, 0x5

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 680
    const/16 p1, 0x11

    .line 682
    goto :goto_32d

    .line 683
    :cond_306
    sget-object p1, Ljje;->NOT_RUNNING:Ljje;

    .line 685
    if-ne v0, p1, :cond_31c

    .line 687
    const p1, 0x7f141418

    .line 690
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 693
    move-result-object p1

    .line 694
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 697
    move-result-wide v0

    .line 698
    const/4 v8, 0x2

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 701
    const/16 p1, 0x12

    .line 703
    goto :goto_32d

    .line 704
    :cond_31c
    const p1, 0x7f141416

    .line 707
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 710
    move-result-object p1

    .line 711
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 714
    move-result-wide v0

    .line 715
    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 718
    const/16 p1, 0x13

    .line 720
    :goto_32d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 723
    move-result-object v0

    .line 724
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 727
    move-result-object p0

    .line 728
    const/4 v8, 0x3

    invoke-static {v0, p0, v2, p1}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 731
    return v3

    .line 732
    :cond_33a
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAllFilesAccess()Z

    .line 735
    move-result v0

    .line 736
    const/4 v8, 0x1

    if-eqz v0, :cond_35d

    .line 738
    const/16 v0, 0x1e

    .line 740
    const/4 v8, 0x6

    if-lt p1, v0, :cond_35d

    .line 742
    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    .line 745
    move-result p1

    .line 746
    const/4 v8, 0x0

    if-nez p1, :cond_35d

    .line 748
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 751
    move-result-object p1

    .line 752
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 755
    move-result-object v0

    .line 756
    const/4 v8, 0x3

    const/16 v4, 0x14

    .line 758
    const/4 v8, 0x4

    invoke-static {p1, v0, v2, v4}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 761
    :cond_35d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFileVersion()Landroid/util/Pair;

    .line 764
    move-result-object p1

    .line 765
    if-eqz p1, :cond_3f9

    .line 767
    iget-object v0, p1, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 769
    const/4 v8, 0x0

    check-cast v0, Ljava/lang/Integer;

    .line 771
    invoke-virtual {v0}, Ljava/lang/Integer;->intValue()I

    .line 774
    move-result v0

    .line 775
    const-string v2, "em.adbopa.crrrmor.tohcdfseolli"

    const-string v2, "com.arlosoft.macrodroid.helper"

    .line 777
    const/4 v8, 0x1

    invoke-static {v2}, Lgi0;->b(Ljava/lang/String;)I

    .line 780
    move-result v2

    .line 781
    const/4 v8, 0x6

    if-le v0, v2, :cond_3f9

    .line 783
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseConnectivityHelperApp()Landroid/util/Pair;

    .line 786
    move-result-object v0

    .line 787
    const/16 v2, 0xd

    .line 789
    const/4 v8, 0x2

    const-string v4, "+) must be installed to use this feature."

    .line 791
    const/4 v8, 0x1

    const-string v5, "(rocnMuvdo UsKrD  rPaeeviaHrle lAi"

    const-string v5, "MacroDroid Universal Helper APK (v"

    .line 793
    if-nez v0, :cond_3b3

    .line 795
    new-instance v0, Ljava/lang/StringBuilder;

    .line 797
    invoke-direct {v0, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 800
    iget-object v5, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 802
    const/4 v8, 0x4

    check-cast v5, Ljava/lang/String;

    .line 804
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 807
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 810
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 813
    move-result-object v0

    .line 814
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 817
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 820
    move-result-object v0

    .line 821
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 824
    move-result-object v4

    .line 825
    const/4 v8, 0x2

    iget-object p1, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 827
    const/4 v8, 0x3

    check-cast p1, Ljava/lang/String;

    .line 829
    invoke-static {v0, v4, p1, v2}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 832
    goto :goto_3f9

    .line 833
    :cond_3b3
    iget-object v6, v0, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 835
    check-cast v6, Ljava/lang/Integer;

    .line 837
    invoke-virtual {v6}, Ljava/lang/Integer;->intValue()I

    .line 840
    move-result v6

    .line 841
    const-string v7, "com.arlosoft.macrodroid.connectivityhelper"

    .line 843
    const/4 v8, 0x4

    invoke-static {v7}, Lgi0;->b(Ljava/lang/String;)I

    .line 846
    move-result v7

    .line 847
    if-le v6, v7, :cond_3f9

    .line 849
    new-instance v6, Ljava/lang/StringBuilder;

    .line 851
    invoke-direct {v6, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 854
    iget-object v5, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 856
    const/4 v8, 0x7

    check-cast v5, Ljava/lang/String;

    .line 858
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 861
    const-string v5, "+) or Connectivity Helper APK (v"

    .line 863
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 866
    iget-object v0, v0, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 868
    check-cast v0, Ljava/lang/String;

    .line 870
    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 873
    invoke-virtual {v6, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 876
    const/4 v8, 0x0

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 879
    move-result-object v0

    .line 880
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 883
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 886
    move-result-object v0

    .line 887
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 890
    move-result-object v4

    .line 891
    const/4 v8, 0x7

    iget-object p1, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 893
    check-cast p1, Ljava/lang/String;

    .line 895
    const/4 v8, 0x0

    invoke-static {v0, v4, p1, v2}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 898
    :cond_3f9
    :goto_3f9
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 901
    move-result-object p1

    .line 902
    const/4 v8, 0x5

    if-eqz p1, :cond_43e

    .line 904
    array-length v0, p1

    .line 905
    move v2, v3

    .line 906
    :goto_402
    if-ge v2, v0, :cond_43e

    .line 908
    const/4 v8, 0x7

    aget-object v4, p1, v2

    .line 910
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 913
    move-result-object v5

    .line 914
    const/4 v8, 0x3

    invoke-static {v5, v4}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 917
    move-result v5

    .line 918
    if-eqz v5, :cond_439

    .line 920
    new-instance p1, Ljava/lang/StringBuilder;

    .line 922
    const/4 v8, 0x2

    const-string v0, "Permission "

    .line 924
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 927
    invoke-virtual {p1, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 930
    const/4 v8, 0x5

    const-string v0, "n ner cpdMb a rrldoesDtfo ooai"

    const-string v0, " for MacroDroid is not enabled"

    .line 932
    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 935
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 938
    move-result-object p1

    .line 939
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 942
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 945
    move-result-object p1

    .line 946
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 949
    move-result-object p0

    .line 950
    invoke-static {p1, v4, p0}, Llob;->v(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V

    .line 953
    const/4 v8, 0x2

    return v3

    .line 954
    :cond_439
    const/4 v8, 0x4

    add-int/lit8 v2, v2, 0x1

    .line 956
    const/4 v8, 0x7

    goto :goto_402

    .line 957
    :cond_43e
    :goto_43e
    return v1
.end method
