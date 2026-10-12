.method public final m0(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/util/ArrayList;
    .locals 62

    .line 1
    move-object/from16 v1, p0

    .line 3
    move-object/from16 v0, p1

    .line 5
    const-string v2, ""

    .line 7
    const-string/jumbo v3, "yyyy-MM-dd\'T\'HH:mm:ssZ"

    .line 9
    const-string/jumbo v4, "title"

    .line 11
    const-string v5, "description"

    .line 13
    const-string/jumbo v6, "startTimestamp"

    .line 15
    const-string v7, "endTimestamp"

    .line 17
    const-string/jumbo v8, "startFormatted"

    .line 19
    const-string v9, "endFormatted"

    .line 21
    const-string v10, "durationMinutes"

    .line 23
    const-string v11, "organizer"

    .line 25
    const-string v12, "attendees"

    .line 27
    const-string v13, "location"

    .line 29
    const-string v14, "allDay"

    .line 31
    new-instance v15, Ljava/util/ArrayList;

    .line 33
    invoke-direct {v15}, Ljava/util/ArrayList;-><init>()V

    .line 36
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 39
    move-result-object v16

    .line 40
    invoke-virtual/range {v16 .. v16}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 43
    move-result-object v17

    .line 44
    invoke-virtual/range {v17 .. v17}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 47
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 50
    move-result-wide v18

    .line 51
    move-object/from16 v16, v2

    move-object/from16 v16, v2

    .line 53
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 56
    move-result-object v2

    .line 57
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 60
    move-object/from16 v23, v15

    move-object/from16 v23, v15

    .line 62
    iget-object v15, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->startOffsetValue:Ljava/lang/String;

    .line 64
    move-object/from16 v24, v11

    .line 66
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 69
    move-result-object v11

    .line 70
    invoke-static {v2, v11, v0, v15}, Lsr9;->l(Landroid/content/Context;Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Ljava/lang/String;)Ljava/lang/String;

    .line 73
    move-result-object v2

    .line 74
    :try_start_51
    invoke-static {v2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    .line 77
    move-result v2
    :try_end_55
    .catch Ljava/lang/NumberFormatException; {:try_start_51 .. :try_end_55} :catch_56

    .line 78
    goto :goto_57

    .line 79
    :catch_56
    const/4 v2, 0x0

    .line 80
    :goto_57
    iget v15, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->startOffsetUnit:I

    .line 82
    const v20, 0x15180

    .line 85
    const/4 v11, 0x1

    .line 86
    const-wide/16 v21, 0x3e8

    .line 88
    if-eqz v15, :cond_75

    .line 90
    if-eq v15, v11, :cond_71

    .line 92
    const/4 v11, 0x2

    .line 93
    if-eq v15, v11, :cond_6d

    .line 95
    mul-int/lit8 v2, v2, 0x3c

    .line 97
    move-object v15, v12

    .line 98
    :goto_69
    int-to-long v11, v2

    .line 99
    mul-long v11, v11, v21

    .line 101
    goto :goto_7a

    .line 102
    :cond_6d
    move-object v15, v12

    .line 103
    mul-int v2, v2, v20

    .line 105
    goto :goto_69

    .line 106
    :cond_71
    move-object v15, v12

    .line 107
    mul-int/lit16 v2, v2, 0xe10

    .line 109
    goto :goto_69

    .line 110
    :cond_75
    move-object v15, v12

    move-object v15, v12

    .line 111
    mul-int/lit8 v2, v2, 0x3c

    .line 113
    goto :goto_69

    .line 114
    :goto_7a
    add-long v11, v18, v11

    .line 116
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 119
    move-result-object v2

    .line 120
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 123
    move-object/from16 v28, v15

    .line 125
    iget-object v15, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->durationValue:Ljava/lang/String;

    .line 127
    move-object/from16 v29, v13

    .line 129
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 132
    move-result-object v13

    .line 133
    invoke-static {v2, v13, v0, v15}, Lsr9;->l(Landroid/content/Context;Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Ljava/lang/String;)Ljava/lang/String;

    .line 136
    move-result-object v0

    .line 137
    :try_start_91
    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    .line 140
    move-result v0
    :try_end_95
    .catch Ljava/lang/NumberFormatException; {:try_start_91 .. :try_end_95} :catch_a2

    .line 141
    const/4 v2, 0x1

    .line 142
    if-ge v0, v2, :cond_9d

    .line 144
    move/from16 v27, v2

    move/from16 v27, v2

    .line 146
    goto :goto_9f

    .line 147
    :cond_9d
    move/from16 v27, v0

    .line 149
    :goto_9f
    move/from16 v0, v27

    .line 151
    goto :goto_a4

    .line 152
    :catch_a2
    const/4 v2, 0x1

    .line 153
    move v0, v2

    .line 154
    :goto_a4
    iget v13, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->durationUnit:I

    .line 156
    if-eqz v13, :cond_bc

    .line 158
    if-eq v13, v2, :cond_b8

    .line 160
    const/4 v2, 0x2

    .line 161
    if-eq v13, v2, :cond_b4

    .line 163
    mul-int v0, v0, v20

    .line 165
    move-object v2, v14

    .line 166
    :goto_b0
    int-to-long v14, v0

    .line 167
    mul-long v14, v14, v21

    .line 169
    goto :goto_c1

    .line 170
    :cond_b4
    move-object v2, v14

    .line 171
    mul-int v0, v0, v20

    .line 173
    goto :goto_b0

    .line 174
    :cond_b8
    move-object v2, v14

    .line 175
    mul-int/lit16 v0, v0, 0xe10

    .line 177
    goto :goto_b0

    .line 178
    :cond_bc
    move-object v2, v14

    move-object v2, v14

    .line 179
    mul-int/lit8 v0, v0, 0x3c

    .line 181
    goto :goto_b0

    .line 182
    :goto_c1
    add-long/2addr v14, v11

    .line 183
    iget v0, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->startOffsetUnit:I

    .line 185
    move-object/from16 p1, v2

    move-object/from16 p1, v2

    .line 187
    const/4 v2, 0x2

    .line 188
    if-ne v0, v2, :cond_10a

    .line 190
    if-ne v13, v2, :cond_10a

    .line 192
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 195
    move-result-object v0

    .line 196
    invoke-virtual {v0, v11, v12}, Ljava/util/Calendar;->setTimeInMillis(J)V

    .line 199
    const/16 v2, 0xb

    .line 201
    const/4 v11, 0x0

    .line 202
    invoke-virtual {v0, v2, v11}, Ljava/util/Calendar;->set(II)V

    .line 205
    const/16 v12, 0xc

    .line 207
    invoke-virtual {v0, v12, v11}, Ljava/util/Calendar;->set(II)V

    .line 210
    const/16 v13, 0xd

    .line 212
    invoke-virtual {v0, v13, v11}, Ljava/util/Calendar;->set(II)V

    .line 215
    const/16 v13, 0xe

    .line 217
    invoke-virtual {v0, v13, v11}, Ljava/util/Calendar;->set(II)V

    .line 220
    invoke-virtual {v0}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 223
    move-result-wide v19

    .line 224
    invoke-virtual {v0, v14, v15}, Ljava/util/Calendar;->setTimeInMillis(J)V

    .line 227
    const/16 v11, 0x17

    .line 229
    invoke-virtual {v0, v2, v11}, Ljava/util/Calendar;->set(II)V

    .line 232
    const/16 v2, 0x3b

    .line 234
    invoke-virtual {v0, v12, v2}, Ljava/util/Calendar;->set(II)V

    .line 237
    const/16 v11, 0xd

    .line 239
    invoke-virtual {v0, v11, v2}, Ljava/util/Calendar;->set(II)V

    .line 242
    const/16 v2, 0x3e7

    .line 244
    invoke-virtual {v0, v13, v2}, Ljava/util/Calendar;->set(II)V

    .line 247
    invoke-virtual {v0}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 250
    move-result-wide v14

    .line 251
    move-wide/from16 v11, v19

    .line 253
    :cond_10a
    const-string v2, "0"

    .line 255
    const-string v13, "_=saledrdian"

    const-string v13, "calendar_id="

    .line 257
    const-string v0, "content://com.android.calendar/instances/when"

    .line 259
    invoke-static {v0}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 262
    move-result-object v0

    .line 263
    invoke-virtual {v0}, Landroid/net/Uri;->buildUpon()Landroid/net/Uri$Builder;

    .line 266
    move-result-object v0

    .line 267
    invoke-static {v0, v11, v12}, Landroid/content/ContentUris;->appendId(Landroid/net/Uri$Builder;J)Landroid/net/Uri$Builder;

    .line 270
    invoke-static {v0, v14, v15}, Landroid/content/ContentUris;->appendId(Landroid/net/Uri$Builder;J)Landroid/net/Uri$Builder;

    .line 273
    const/16 v30, 0xa

    .line 275
    move-wide/from16 v31, v11

    .line 277
    const-wide/32 v38, 0xea60

    .line 280
    const/16 v40, 0x0

    .line 282
    :try_start_129
    iget-object v11, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->calendarId:Ljava/lang/String;
    :try_end_12b
    .catch Ljava/lang/Exception; {:try_start_129 .. :try_end_12b} :catch_3f4
    .catchall {:try_start_129 .. :try_end_12b} :catchall_147

    .line 284
    if-eqz v11, :cond_16c

    .line 286
    :try_start_12d
    invoke-virtual {v11}, Ljava/lang/String;->length()I

    .line 289
    move-result v11

    .line 290
    if-nez v11, :cond_134

    .line 292
    goto :goto_16c

    .line 293
    :cond_134
    iget-object v11, v1, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->calendarId:Ljava/lang/String;

    .line 295
    new-instance v12, Ljava/lang/StringBuilder;

    .line 297
    invoke-direct {v12, v13}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 300
    invoke-virtual {v12, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 303
    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 306
    move-result-object v11
    :try_end_142
    .catch Ljava/lang/Exception; {:try_start_12d .. :try_end_142} :catch_14a
    .catchall {:try_start_12d .. :try_end_142} :catchall_147

    .line 307
    move-object/from16 v20, v11

    move-object/from16 v20, v11

    .line 309
    goto :goto_16e

    .line 310
    :catchall_147
    move-exception v0

    .line 311
    goto/16 :goto_928

    .line 313
    :catch_14a
    move-exception v0

    .line 314
    move-object/from16 v48, v2

    .line 316
    move-object/from16 v43, v3

    move-object/from16 v43, v3

    .line 318
    move-object v2, v9

    .line 319
    move-object v12, v10

    move-object v12, v10

    .line 320
    move-wide/from16 v44, v14

    .line 322
    move-object/from16 v51, v17

    .line 324
    move-object/from16 v1, v23

    move-object/from16 v1, v23

    .line 326
    move-object/from16 v10, v24

    .line 328
    move-object/from16 v3, v28

    .line 330
    move-object/from16 v11, v29

    .line 332
    move-object/from16 v50, v40

    .line 334
    move-object/from16 v15, p1

    move-object/from16 v15, p1

    .line 336
    move-object/from16 v17, v13

    .line 338
    goto/16 :goto_414

    .line 340
    :cond_16c
    :goto_16c
    move-object/from16 v20, v40

    .line 342
    :goto_16e
    :try_start_16e
    invoke-virtual {v0}, Landroid/net/Uri$Builder;->build()Landroid/net/Uri;

    .line 345
    move-result-object v18

    .line 346
    const-string/jumbo v43, "title"

    .line 348
    const-string v44, "cdimonistep"

    const-string v44, "description"

    .line 350
    const-string v45, "begin"

    .line 352
    const-string v46, "end"

    .line 354
    const-string v47, "allDay"

    .line 356
    const-string v48, "eventLocation"

    .line 358
    const-string v49, "indeovet"

    const-string v49, "event_id"

    .line 360
    const-string v50, "hasAlarm"

    .line 362
    const-string v51, "availability"

    .line 364
    const-string v52, "organizer"

    .line 366
    filled-new-array/range {v43 .. v52}, [Ljava/lang/String;

    .line 369
    move-result-object v19

    .line 370
    const-string v22, "begin ASC"

    .line 372
    const/16 v21, 0x0

    .line 374
    invoke-virtual/range {v17 .. v22}, Landroid/content/ContentResolver;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;

    .line 377
    move-result-object v11
    :try_end_197
    .catch Ljava/lang/Exception; {:try_start_16e .. :try_end_197} :catch_3f4
    .catchall {:try_start_16e .. :try_end_197} :catchall_147

    .line 378
    move-object/from16 v12, v17

    .line 380
    if-eqz v11, :cond_3eb

    .line 382
    :try_start_19b
    new-instance v0, Ljava/text/SimpleDateFormat;
    :try_end_19d
    .catch Ljava/lang/Exception; {:try_start_19b .. :try_end_19d} :catch_3dc
    .catchall {:try_start_19b .. :try_end_19d} :catchall_370

    .line 384
    move-object/from16 v17, v13

    .line 386
    :try_start_19f
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    .line 389
    move-result-object v13

    .line 390
    invoke-direct {v0, v3, v13}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    .line 393
    :goto_1a6
    invoke-interface {v11}, Landroid/database/Cursor;->moveToNext()Z

    .line 396
    move-result v13

    .line 397
    if-eqz v13, :cond_3c1

    .line 399
    const/4 v13, 0x0

    .line 400
    invoke-interface {v11, v13}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 403
    move-result-object v18
    :try_end_1b1
    .catch Ljava/lang/Exception; {:try_start_19f .. :try_end_1b1} :catch_3b9
    .catchall {:try_start_19f .. :try_end_1b1} :catchall_370

    .line 404
    if-nez v18, :cond_1bd

    .line 406
    move-object/from16 v13, v16

    move-object/from16 v13, v16

    .line 408
    :goto_1b7
    move-object/from16 v43, v3

    move-object/from16 v43, v3

    .line 410
    const/4 v3, 0x1

    .line 411
    goto :goto_1c2

    .line 412
    :cond_1bd
    move-object/from16 v13, v18

    move-object/from16 v13, v18

    .line 414
    goto :goto_1b7

    .line 415
    :goto_1c2
    :try_start_1c2
    invoke-interface {v11, v3}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 418
    move-result-object v18
    :try_end_1c6
    .catch Ljava/lang/Exception; {:try_start_1c2 .. :try_end_1c6} :catch_3a2
    .catchall {:try_start_1c2 .. :try_end_1c6} :catchall_370

    .line 419
    if-nez v18, :cond_1d0

    .line 421
    move-object/from16 v3, v16

    move-object/from16 v3, v16

    .line 423
    :goto_1cc
    move-wide/from16 v44, v14

    .line 425
    const/4 v1, 0x2

    .line 426
    goto :goto_1d5

    .line 427
    :cond_1d0
    move-object/from16 v3, v18

    move-object/from16 v3, v18

    .line 429
    goto :goto_1cc

    .line 430
    :goto_1d5
    :try_start_1d5
    invoke-interface {v11, v1}, Landroid/database/Cursor;->getLong(I)J

    .line 433
    move-result-wide v14
    :try_end_1d9
    .catch Ljava/lang/Exception; {:try_start_1d5 .. :try_end_1d9} :catch_388
    .catchall {:try_start_1d5 .. :try_end_1d9} :catchall_370

    .line 434
    move-object/from16 v46, v9

    .line 436
    move-object/from16 v47, v10

    .line 438
    const/4 v1, 0x3

    .line 439
    :try_start_1de
    invoke-interface {v11, v1}, Landroid/database/Cursor;->getLong(I)J

    .line 442
    move-result-wide v9

    .line 443
    move-wide/from16 v18, v9

    .line 445
    const/4 v1, 0x4

    .line 446
    invoke-interface {v11, v1}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 449
    move-result-object v9

    .line 450
    invoke-static {v9, v2}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 453
    move-result v1

    .line 454
    const/16 v27, 0x1

    .line 456
    xor-int/lit8 v1, v1, 0x1

    .line 458
    const/4 v9, 0x5

    .line 459
    invoke-interface {v11, v9}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 462
    move-result-object v10
    :try_end_1f6
    .catch Ljava/lang/Exception; {:try_start_1de .. :try_end_1f6} :catch_380
    .catchall {:try_start_1de .. :try_end_1f6} :catchall_370

    .line 463
    if-nez v10, :cond_1fa

    .line 465
    move-object/from16 v10, v16

    .line 467
    :cond_1fa
    move/from16 v20, v1

    move/from16 v20, v1

    .line 469
    move-object/from16 v48, v2

    .line 471
    const/4 v9, 0x6

    .line 472
    :try_start_201
    invoke-interface {v11, v9}, Landroid/database/Cursor;->getLong(I)J

    .line 475
    move-result-wide v1

    .line 476
    const/4 v9, 0x7

    .line 477
    invoke-interface {v11, v9}, Landroid/database/Cursor;->getInt(I)I

    .line 480
    const/16 v9, 0x8

    .line 482
    invoke-interface {v11, v9}, Landroid/database/Cursor;->getInt(I)I

    .line 485
    const/16 v9, 0x9

    .line 487
    invoke-interface {v11, v9}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 490
    move-result-object v21

    .line 491
    if-nez v21, :cond_21b

    .line 493
    move-object/from16 v9, v16

    move-object/from16 v9, v16

    .line 495
    goto :goto_21d

    .line 496
    :cond_21b
    move-object/from16 v9, v21

    .line 498
    :goto_21d
    invoke-static {v12, v1, v2}, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->l0(Landroid/content/ContentResolver;J)Ljava/lang/String;

    .line 501
    move-result-object v1

    .line 502
    new-instance v2, Ldib;

    .line 504
    invoke-direct {v2, v4, v13}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 507
    new-instance v13, Ldib;

    .line 509
    invoke-direct {v13, v5, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 512
    invoke-static {v14, v15}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 515
    move-result-object v3

    .line 516
    move-object/from16 v21, v2

    .line 518
    new-instance v2, Ldib;

    .line 520
    invoke-direct {v2, v6, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 523
    invoke-static/range {v18 .. v19}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 526
    move-result-object v3

    .line 527
    move-object/from16 v22, v2

    move-object/from16 v22, v2

    .line 529
    new-instance v2, Ldib;

    .line 531
    invoke-direct {v2, v7, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 534
    new-instance v3, Ljava/util/Date;

    .line 536
    invoke-direct {v3, v14, v15}, Ljava/util/Date;-><init>(J)V

    .line 539
    invoke-virtual {v0, v3}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 542
    move-result-object v3

    .line 543
    move-object/from16 v49, v2

    .line 545
    new-instance v2, Ldib;

    .line 547
    invoke-direct {v2, v8, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 550
    new-instance v3, Ljava/util/Date;
    :try_end_255
    .catch Ljava/lang/Exception; {:try_start_201 .. :try_end_255} :catch_376
    .catchall {:try_start_201 .. :try_end_255} :catchall_370

    .line 552
    move-object/from16 v50, v11

    move-object/from16 v50, v11

    .line 554
    move-object/from16 v51, v12

    .line 556
    move-wide/from16 v11, v18

    .line 558
    :try_start_25d
    invoke-direct {v3, v11, v12}, Ljava/util/Date;-><init>(J)V

    .line 561
    invoke-virtual {v0, v3}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 564
    move-result-object v3
    :try_end_264
    .catch Ljava/lang/Exception; {:try_start_25d .. :try_end_264} :catch_35c
    .catchall {:try_start_25d .. :try_end_264} :catchall_303

    .line 565
    move-object/from16 v18, v0

    .line 567
    :try_start_266
    new-instance v0, Ldib;
    :try_end_268
    .catch Ljava/lang/Exception; {:try_start_266 .. :try_end_268} :catch_358
    .catchall {:try_start_266 .. :try_end_268} :catchall_303

    .line 569
    move-object/from16 v19, v2

    .line 571
    move-object/from16 v2, v46

    .line 573
    :try_start_26c
    invoke-direct {v0, v2, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 576
    sub-long/2addr v11, v14

    .line 577
    div-long v11, v11, v38

    .line 579
    invoke-static {v11, v12}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 582
    move-result-object v3
    :try_end_276
    .catch Ljava/lang/Exception; {:try_start_26c .. :try_end_276} :catch_347
    .catchall {:try_start_26c .. :try_end_276} :catchall_303

    .line 583
    :try_start_276
    new-instance v11, Ldib;
    :try_end_278
    .catch Ljava/lang/Exception; {:try_start_276 .. :try_end_278} :catch_343
    .catchall {:try_start_276 .. :try_end_278} :catchall_303

    .line 585
    move-object/from16 v12, v47

    .line 587
    :try_start_27a
    invoke-direct {v11, v12, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 590
    invoke-static/range {v20 .. v20}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    .line 593
    move-result-object v3

    .line 594
    new-instance v14, Ldib;
    :try_end_283
    .catch Ljava/lang/Exception; {:try_start_27a .. :try_end_283} :catch_330
    .catchall {:try_start_27a .. :try_end_283} :catchall_303

    .line 596
    move-object/from16 v15, p1

    move-object/from16 v15, p1

    .line 598
    :try_start_287
    invoke-direct {v14, v15, v3}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_28a
    .catch Ljava/lang/Exception; {:try_start_287 .. :try_end_28a} :catch_32e
    .catchall {:try_start_287 .. :try_end_28a} :catchall_303

    .line 601
    :try_start_28a
    new-instance v3, Ldib;
    :try_end_28c
    .catch Ljava/lang/Exception; {:try_start_28a .. :try_end_28c} :catch_32a
    .catchall {:try_start_28a .. :try_end_28c} :catchall_303

    .line 603
    move-object/from16 p1, v11

    .line 605
    move-object/from16 v11, v29

    .line 607
    :try_start_290
    invoke-direct {v3, v11, v10}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_293
    .catch Ljava/lang/Exception; {:try_start_290 .. :try_end_293} :catch_31f
    .catchall {:try_start_290 .. :try_end_293} :catchall_303

    .line 610
    :try_start_293
    new-instance v10, Ldib;
    :try_end_295
    .catch Ljava/lang/Exception; {:try_start_293 .. :try_end_295} :catch_31b
    .catchall {:try_start_293 .. :try_end_295} :catchall_303

    .line 612
    move-object/from16 v20, v3

    move-object/from16 v20, v3

    .line 614
    move-object/from16 v3, v28

    .line 616
    :try_start_29b
    invoke-direct {v10, v3, v1}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_29e
    .catch Ljava/lang/Exception; {:try_start_29b .. :try_end_29e} :catch_316
    .catchall {:try_start_29b .. :try_end_29e} :catchall_303

    .line 619
    :try_start_29e
    new-instance v1, Ldib;
    :try_end_2a0
    .catch Ljava/lang/Exception; {:try_start_29e .. :try_end_2a0} :catch_310
    .catchall {:try_start_29e .. :try_end_2a0} :catchall_303

    .line 621
    move-object/from16 v28, v10

    move-object/from16 v28, v10

    .line 623
    move-object/from16 v10, v24

    .line 625
    :try_start_2a6
    invoke-direct {v1, v10, v9}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 628
    move-object/from16 v24, v0

    .line 630
    const/16 v9, 0xb

    .line 632
    new-array v0, v9, [Ldib;

    .line 634
    const/16 v25, 0x0

    .line 636
    aput-object v21, v0, v25

    .line 638
    const/16 v27, 0x1

    .line 640
    aput-object v13, v0, v27

    .line 642
    const/16 v26, 0x2

    .line 644
    aput-object v22, v0, v26

    .line 646
    const/16 v42, 0x3

    .line 648
    aput-object v49, v0, v42

    .line 650
    const/16 v41, 0x4

    .line 652
    aput-object v19, v0, v41

    .line 654
    const/16 v33, 0x5

    .line 656
    aput-object v24, v0, v33

    .line 658
    const/16 v34, 0x6

    .line 660
    aput-object p1, v0, v34

    .line 662
    const/16 v35, 0x7

    .line 664
    aput-object v14, v0, v35

    .line 666
    const/16 v36, 0x8

    .line 668
    aput-object v20, v0, v36

    .line 670
    const/16 v37, 0x9

    .line 672
    aput-object v28, v0, v37

    .line 674
    aput-object v1, v0, v30

    .line 676
    invoke-static {v0}, Lyw9;->U([Ldib;)Ljava/util/Map;

    .line 679
    move-result-object v0
    :try_end_2dd
    .catch Ljava/lang/Exception; {:try_start_2a6 .. :try_end_2dd} :catch_30b
    .catchall {:try_start_2a6 .. :try_end_2dd} :catchall_303

    .line 680
    move-object/from16 v1, v23

    .line 682
    :try_start_2df
    invoke-virtual {v1, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
    :try_end_2e2
    .catch Ljava/lang/Exception; {:try_start_2df .. :try_end_2e2} :catch_308
    .catchall {:try_start_2df .. :try_end_2e2} :catchall_303

    .line 685
    move-object/from16 v23, v1

    .line 687
    move-object v9, v2

    .line 688
    move-object/from16 v28, v3

    move-object/from16 v28, v3

    .line 690
    move-object/from16 v24, v10

    .line 692
    move-object/from16 v29, v11

    .line 694
    move-object v10, v12

    move-object v10, v12

    .line 695
    move-object/from16 p1, v15

    .line 697
    move-object/from16 v0, v18

    .line 699
    move-object/from16 v3, v43

    .line 701
    move-wide/from16 v14, v44

    .line 703
    move-object/from16 v2, v48

    .line 705
    move-object/from16 v11, v50

    move-object/from16 v11, v50

    .line 707
    move-object/from16 v12, v51

    .line 709
    move-object/from16 v1, p0

    .line 711
    goto/16 :goto_1a6

    .line 713
    :catchall_303
    move-exception v0

    .line 714
    :goto_304
    move-object/from16 v40, v50

    .line 716
    goto/16 :goto_928

    .line 718
    :catch_308
    move-exception v0

    .line 719
    goto/16 :goto_414

    .line 721
    :catch_30b
    move-exception v0

    .line 722
    :goto_30c
    move-object/from16 v1, v23

    .line 724
    goto/16 :goto_414

    .line 726
    :catch_310
    move-exception v0

    .line 727
    move-object/from16 v10, v24

    move-object/from16 v10, v24

    .line 729
    goto :goto_30c

    .line 730
    :catch_316
    move-exception v0

    .line 731
    :goto_317
    move-object/from16 v1, v23

    .line 733
    goto/16 :goto_39e

    .line 735
    :catch_31b
    move-exception v0

    .line 736
    move-object/from16 v3, v28

    .line 738
    goto :goto_317

    .line 739
    :catch_31f
    move-exception v0

    .line 740
    :goto_320
    move-object/from16 v1, v23

    move-object/from16 v1, v23

    .line 742
    move-object/from16 v10, v24

    .line 744
    move-object/from16 v3, v28

    .line 746
    goto/16 :goto_414

    .line 748
    :catch_32a
    move-exception v0

    .line 749
    move-object/from16 v11, v29

    .line 751
    goto :goto_320

    .line 752
    :catch_32e
    move-exception v0

    .line 753
    goto :goto_335

    .line 754
    :catch_330
    move-exception v0

    .line 755
    :goto_331
    move-object/from16 v15, p1

    move-object/from16 v15, p1

    .line 757
    :goto_335
    move-object/from16 v1, v23

    .line 759
    move-object/from16 v10, v24

    move-object/from16 v10, v24

    .line 761
    move-object/from16 v3, v28

    move-object/from16 v3, v28

    .line 763
    move-object/from16 v11, v29

    .line 765
    goto/16 :goto_414

    .line 767
    :catch_343
    move-exception v0

    .line 768
    move-object/from16 v12, v47

    .line 770
    goto :goto_331

    .line 771
    :catch_347
    move-exception v0

    .line 772
    :goto_348
    move-object/from16 v15, p1

    .line 774
    move-object/from16 v1, v23

    .line 776
    move-object/from16 v10, v24

    .line 778
    move-object/from16 v3, v28

    move-object/from16 v3, v28

    .line 780
    move-object/from16 v11, v29

    .line 782
    :goto_354
    move-object/from16 v12, v47

    .line 784
    goto/16 :goto_414

    .line 786
    :catch_358
    move-exception v0

    .line 787
    move-object/from16 v2, v46

    .line 789
    goto :goto_348

    .line 790
    :catch_35c
    move-exception v0

    .line 791
    move-object/from16 v15, p1

    .line 793
    :goto_35f
    move-object/from16 v1, v23

    .line 795
    move-object/from16 v10, v24

    .line 797
    move-object/from16 v3, v28

    move-object/from16 v3, v28

    .line 799
    move-object/from16 v11, v29

    move-object/from16 v11, v29

    .line 801
    move-object/from16 v2, v46

    move-object/from16 v2, v46

    .line 803
    goto :goto_354

    .line 804
    :catchall_370
    move-exception v0

    .line 805
    move-object/from16 v50, v11

    move-object/from16 v50, v11

    .line 807
    goto :goto_304

    .line 808
    :catch_376
    move-exception v0

    .line 809
    move-object/from16 v15, p1

    .line 811
    :goto_379
    move-object/from16 v50, v11

    .line 813
    move-object/from16 v51, v12

    move-object/from16 v51, v12

    .line 815
    goto :goto_35f

    .line 816
    :catch_380
    move-exception v0

    .line 817
    move-object/from16 v15, p1

    move-object/from16 v15, p1

    .line 819
    move-object/from16 v48, v2

    .line 821
    goto :goto_379

    .line 822
    :catch_388
    move-exception v0

    .line 823
    move-object/from16 v15, p1

    move-object/from16 v15, p1

    .line 825
    move-object/from16 v48, v2

    .line 827
    move-object v2, v9

    .line 828
    move-object/from16 v50, v11

    move-object/from16 v50, v11

    .line 830
    move-object/from16 v51, v12

    .line 832
    move-object/from16 v1, v23

    .line 834
    move-object/from16 v3, v28

    .line 836
    move-object/from16 v11, v29

    .line 838
    :goto_39c
    move-object v12, v10

    move-object v12, v10

    .line 839
    :goto_39e
    move-object/from16 v10, v24

    .line 841
    goto/16 :goto_414

    .line 843
    :catch_3a2
    move-exception v0

    .line 844
    move-object/from16 v48, v2

    move-object/from16 v48, v2

    .line 846
    :goto_3a7
    move-object v2, v9

    .line 847
    move-object/from16 v50, v11

    .line 849
    move-object/from16 v51, v12

    move-object/from16 v51, v12

    .line 851
    :goto_3ae
    move-wide/from16 v44, v14

    .line 853
    move-object/from16 v1, v23

    .line 855
    move-object/from16 v3, v28

    .line 857
    move-object/from16 v11, v29

    .line 859
    move-object/from16 v15, p1

    .line 861
    goto :goto_39c

    .line 862
    :catch_3b9
    move-exception v0

    .line 863
    move-object/from16 v48, v2

    move-object/from16 v48, v2

    .line 865
    move-object/from16 v43, v3

    .line 867
    goto :goto_3a7

    .line 868
    :cond_3c1
    :goto_3c1
    move-object/from16 v48, v2

    .line 870
    move-object/from16 v43, v3

    .line 872
    move-object v2, v9

    .line 873
    move-object/from16 v50, v11

    move-object/from16 v50, v11

    .line 875
    move-object/from16 v51, v12

    .line 877
    move-wide/from16 v44, v14

    .line 879
    move-object/from16 v1, v23

    move-object/from16 v1, v23

    .line 881
    move-object/from16 v3, v28

    .line 883
    move-object/from16 v11, v29

    .line 885
    move-object/from16 v15, p1

    .line 887
    move-object v12, v10

    .line 888
    move-object/from16 v10, v24

    .line 890
    goto :goto_3ee

    .line 891
    :catch_3dc
    move-exception v0

    .line 892
    move-object/from16 v48, v2

    .line 894
    move-object/from16 v43, v3

    .line 896
    move-object v2, v9

    .line 897
    move-object/from16 v50, v11

    move-object/from16 v50, v11

    .line 899
    move-object/from16 v51, v12

    .line 901
    move-object/from16 v17, v13

    .line 903
    goto :goto_3ae

    .line 904
    :cond_3eb
    move-object/from16 v17, v13

    .line 906
    goto :goto_3c1

    .line 907
    :goto_3ee
    if-eqz v50, :cond_42f

    .line 909
    :goto_3f0
    invoke-interface/range {v50 .. v50}, Landroid/database/Cursor;->close()V

    .line 912
    goto :goto_42f

    .line 913
    :catch_3f4
    move-exception v0

    .line 914
    move-object/from16 v48, v2

    .line 916
    move-object/from16 v43, v3

    .line 918
    move-object v2, v9

    move-object v2, v9

    .line 919
    move-object v12, v10

    .line 920
    move-wide/from16 v44, v14

    .line 922
    move-object/from16 v51, v17

    move-object/from16 v51, v17

    .line 924
    move-object/from16 v1, v23

    .line 926
    move-object/from16 v10, v24

    move-object/from16 v10, v24

    .line 928
    move-object/from16 v3, v28

    move-object/from16 v3, v28

    .line 930
    move-object/from16 v11, v29

    .line 932
    move-object/from16 v15, p1

    .line 934
    move-object/from16 v17, v13

    .line 936
    move-object/from16 v50, v40

    .line 938
    :goto_414
    :try_start_414
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 941
    move-result-object v0

    .line 942
    new-instance v9, Ljava/lang/StringBuilder;

    .line 944
    invoke-direct {v9}, Ljava/lang/StringBuilder;-><init>()V

    .line 947
    const-string v13, "Error fetching calendar events: "

    .line 949
    invoke-virtual {v9, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 952
    invoke-virtual {v9, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 955
    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 958
    move-result-object v0

    .line 959
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V
    :try_end_42c
    .catchall {:try_start_414 .. :try_end_42c} :catchall_303

    .line 962
    if-eqz v50, :cond_42f

    .line 964
    goto :goto_3f0

    .line 965
    :cond_42f
    :goto_42f
    invoke-virtual {v1}, Ljava/util/ArrayList;->isEmpty()Z

    .line 968
    move-result v0

    .line 969
    if-eqz v0, :cond_7c1

    .line 971
    :try_start_435
    new-instance v0, Ljava/lang/StringBuilder;

    .line 973
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 976
    const-string v9, "dtstart<="

    .line 978
    invoke-virtual {v0, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    :try_end_43f
    .catch Ljava/lang/Exception; {:try_start_435 .. :try_end_43f} :catch_48b
    .catchall {:try_start_435 .. :try_end_43f} :catchall_488

    .line 981
    move-wide/from16 v13, v44

    .line 983
    :try_start_441
    invoke-virtual {v0, v13, v14}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 986
    const-string v9, "= NAtbednd >"

    const-string v9, " AND dtend>="

    .line 988
    invoke-virtual {v0, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    :try_end_44b
    .catch Ljava/lang/Exception; {:try_start_441 .. :try_end_44b} :catch_795
    .catchall {:try_start_441 .. :try_end_44b} :catchall_488

    .line 991
    move-wide/from16 v44, v13

    .line 993
    move-wide/from16 v13, v31

    .line 995
    :try_start_44f
    invoke-virtual {v0, v13, v14}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 998
    const-string v9, " AND dtend>0 AND (rrule IS NULL OR rrule=\'\')"

    .line 1000
    invoke-virtual {v0, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1003
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1006
    move-result-object v0
    :try_end_45b
    .catch Ljava/lang/Exception; {:try_start_44f .. :try_end_45b} :catch_784
    .catchall {:try_start_44f .. :try_end_45b} :catchall_488

    .line 1007
    move-object/from16 v9, p0

    .line 1009
    move-wide/from16 v31, v13

    .line 1011
    :try_start_45f
    iget-object v13, v9, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->calendarId:Ljava/lang/String;

    .line 1013
    if-eqz v13, :cond_485

    .line 1015
    invoke-virtual {v13}, Ljava/lang/String;->length()I

    .line 1018
    move-result v13

    .line 1019
    if-nez v13, :cond_46a

    .line 1021
    goto :goto_485

    .line 1022
    :cond_46a
    iget-object v9, v9, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->calendarId:Ljava/lang/String;

    .line 1024
    new-instance v13, Ljava/lang/StringBuilder;

    .line 1026
    invoke-direct {v13}, Ljava/lang/StringBuilder;-><init>()V

    .line 1029
    move-object/from16 v14, v17

    .line 1031
    invoke-virtual {v13, v14}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1034
    invoke-virtual {v13, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1037
    const-string v9, " AND "

    .line 1039
    invoke-virtual {v13, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1042
    invoke-virtual {v13, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1045
    invoke-virtual {v13}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1048
    move-result-object v0

    .line 1049
    :cond_485
    :goto_485
    move-object/from16 v20, v0

    .line 1051
    goto :goto_497

    .line 1052
    :catchall_488
    move-exception v0

    .line 1053
    goto/16 :goto_7bb

    .line 1055
    :catch_48b
    move-exception v0

    .line 1056
    move-object v9, v2

    .line 1057
    move-object v2, v1

    .line 1058
    move-object v1, v9

    .line 1059
    move-object v9, v11

    .line 1060
    move-object v14, v12

    .line 1061
    move-object/from16 v13, v51

    .line 1063
    :goto_493
    move-object v11, v3

    .line 1064
    :goto_494
    move-object v3, v15

    .line 1065
    goto/16 :goto_79d

    .line 1067
    :goto_497
    sget-object v18, Landroid/provider/CalendarContract$Events;->CONTENT_URI:Landroid/net/Uri;

    .line 1069
    const-string v52, "luiet"

    const-string/jumbo v52, "title"

    .line 1071
    const-string v53, "description"

    .line 1073
    const-string v54, "dtstart"

    .line 1075
    const-string v55, "dtend"

    .line 1077
    const-string v56, "allDay"

    .line 1079
    const-string v57, "eventLocation"

    .line 1081
    const-string v58, "_id"

    .line 1083
    const-string v59, "hasAlarm"

    .line 1085
    const-string v60, "availability"

    .line 1087
    const-string v61, "organizer"

    .line 1089
    filled-new-array/range {v52 .. v61}, [Ljava/lang/String;

    .line 1092
    move-result-object v19

    .line 1093
    const-string v22, "rASdsa ptCt"

    const-string v22, "dtstart ASC"
    :try_end_4b8
    .catch Ljava/lang/Exception; {:try_start_45f .. :try_end_4b8} :catch_48b
    .catchall {:try_start_45f .. :try_end_4b8} :catchall_488

    .line 1095
    const/16 v21, 0x0

    .line 1097
    move-object/from16 v17, v51

    move-object/from16 v17, v51

    .line 1099
    :try_start_4be
    invoke-virtual/range {v17 .. v22}, Landroid/content/ContentResolver;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;

    .line 1102
    move-result-object v9
    :try_end_4c2
    .catch Ljava/lang/Exception; {:try_start_4be .. :try_end_4c2} :catch_779
    .catchall {:try_start_4be .. :try_end_4c2} :catchall_488

    .line 1103
    move-object/from16 v13, v17

    move-object/from16 v13, v17

    .line 1105
    if-eqz v9, :cond_765

    .line 1107
    :try_start_4c8
    invoke-interface {v9}, Landroid/database/Cursor;->getCount()I

    .line 1110
    move-result v0
    :try_end_4cc
    .catch Ljava/lang/Exception; {:try_start_4c8 .. :try_end_4cc} :catch_755
    .catchall {:try_start_4c8 .. :try_end_4cc} :catchall_6a7

    .line 1111
    if-lez v0, :cond_506

    .line 1113
    :try_start_4ce
    invoke-interface {v9}, Landroid/database/Cursor;->getCount()I

    .line 1116
    move-result v0

    .line 1117
    new-instance v14, Ljava/lang/StringBuilder;

    .line 1119
    invoke-direct {v14}, Ljava/lang/StringBuilder;-><init>()V
    :try_end_4d7
    .catch Ljava/lang/Exception; {:try_start_4ce .. :try_end_4d7} :catch_500
    .catchall {:try_start_4ce .. :try_end_4d7} :catchall_4f0

    .line 1122
    move-object/from16 v23, v1

    move-object/from16 v23, v1

    .line 1124
    :try_start_4db
    const-string v1, "Events table fallback found "

    .line 1126
    invoke-virtual {v14, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1129
    invoke-virtual {v14, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 1132
    const-string v0, " events for GetCalendarEvents"

    .line 1134
    invoke-virtual {v14, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1137
    invoke-virtual {v14}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1140
    move-result-object v0

    .line 1141
    invoke-static {v0}, Lkjf;->r(Ljava/lang/String;)V
    :try_end_4ef
    .catch Ljava/lang/Exception; {:try_start_4db .. :try_end_4ef} :catch_4f5
    .catchall {:try_start_4db .. :try_end_4ef} :catchall_4f0

    .line 1144
    goto :goto_508

    .line 1145
    :catchall_4f0
    move-exception v0

    .line 1146
    move-object/from16 v40, v9

    .line 1148
    goto/16 :goto_7bb

    .line 1150
    :catch_4f5
    move-exception v0

    .line 1151
    :goto_4f6
    move-object v1, v2

    .line 1152
    move-object/from16 v40, v9

    move-object/from16 v40, v9

    .line 1154
    move-object v9, v11

    .line 1155
    move-object v14, v12

    .line 1156
    move-object/from16 v2, v23

    .line 1158
    goto :goto_493

    .line 1159
    :catch_500
    move-exception v0

    .line 1160
    move-object/from16 v23, v1

    move-object/from16 v23, v1

    .line 1162
    goto :goto_4f6

    .line 1163
    :cond_506
    move-object/from16 v23, v1

    .line 1165
    :goto_508
    :try_start_508
    new-instance v0, Ljava/text/SimpleDateFormat;

    .line 1167
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    .line 1170
    move-result-object v1
    :try_end_50e
    .catch Ljava/lang/Exception; {:try_start_508 .. :try_end_50e} :catch_727
    .catchall {:try_start_508 .. :try_end_50e} :catchall_6a7

    .line 1171
    move-object/from16 v14, v43

    move-object/from16 v14, v43

    .line 1173
    :try_start_512
    invoke-direct {v0, v14, v1}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    .line 1176
    :goto_515
    invoke-interface {v9}, Landroid/database/Cursor;->moveToNext()Z

    .line 1179
    move-result v1

    .line 1180
    if-eqz v1, :cond_745

    .line 1182
    const/4 v1, 0x0

    .line 1183
    invoke-interface {v9, v1}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1186
    move-result-object v17
    :try_end_520
    .catch Ljava/lang/Exception; {:try_start_512 .. :try_end_520} :catch_735
    .catchall {:try_start_512 .. :try_end_520} :catchall_6a7

    .line 1187
    if-nez v17, :cond_528

    .line 1189
    move-object/from16 v1, v16

    .line 1191
    :goto_524
    move-object/from16 v43, v14

    .line 1193
    const/4 v14, 0x1

    .line 1194
    goto :goto_52d

    .line 1195
    :cond_528
    move-object/from16 v1, v17

    move-object/from16 v1, v17

    .line 1197
    goto :goto_524

    .line 1198
    :goto_52d
    :try_start_52d
    invoke-interface {v9, v14}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1201
    move-result-object v17
    :try_end_531
    .catch Ljava/lang/Exception; {:try_start_52d .. :try_end_531} :catch_727
    .catchall {:try_start_52d .. :try_end_531} :catchall_6a7

    .line 1202
    if-nez v17, :cond_53f

    .line 1204
    move-object/from16 v14, v16

    .line 1206
    :goto_535
    move-object/from16 v24, v10

    move-object/from16 v24, v10

    .line 1208
    move-object/from16 v29, v11

    .line 1210
    move-object/from16 v47, v12

    .line 1212
    const/4 v10, 0x2

    .line 1213
    goto :goto_542

    .line 1214
    :cond_53f
    move-object/from16 v14, v17

    .line 1216
    goto :goto_535

    .line 1217
    :goto_542
    :try_start_542
    invoke-interface {v9, v10}, Landroid/database/Cursor;->getLong(I)J

    .line 1220
    move-result-wide v11
    :try_end_546
    .catch Ljava/lang/Exception; {:try_start_542 .. :try_end_546} :catch_71c
    .catchall {:try_start_542 .. :try_end_546} :catchall_6a7

    .line 1221
    move-object/from16 v46, v2

    .line 1223
    move-object/from16 v28, v3

    move-object/from16 v28, v3

    .line 1225
    const/4 v10, 0x3

    .line 1226
    :try_start_54d
    invoke-interface {v9, v10}, Landroid/database/Cursor;->getLong(I)J

    .line 1229
    move-result-wide v2
    :try_end_551
    .catch Ljava/lang/Exception; {:try_start_54d .. :try_end_551} :catch_715
    .catchall {:try_start_54d .. :try_end_551} :catchall_6a7

    .line 1230
    move-object/from16 p1, v15

    .line 1232
    const/4 v10, 0x4

    .line 1233
    :try_start_554
    invoke-interface {v9, v10}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1236
    move-result-object v15

    .line 1237
    move-object/from16 v10, v48

    .line 1239
    invoke-static {v15, v10}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 1242
    move-result v15

    .line 1243
    const/16 v27, 0x1

    .line 1245
    xor-int/lit8 v15, v15, 0x1

    .line 1247
    move-object/from16 v48, v10

    .line 1249
    const/4 v10, 0x5

    .line 1250
    invoke-interface {v9, v10}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1253
    move-result-object v17

    .line 1254
    if-nez v17, :cond_573

    .line 1256
    move-object/from16 v10, v16

    .line 1258
    move-wide/from16 v17, v2

    .line 1260
    move/from16 p0, v15

    .line 1262
    const/4 v15, 0x6

    .line 1263
    goto :goto_57a

    .line 1264
    :cond_573
    move-object/from16 v10, v17

    .line 1266
    move/from16 p0, v15

    .line 1268
    const/4 v15, 0x6

    .line 1269
    move-wide/from16 v17, v2

    .line 1271
    :goto_57a
    invoke-interface {v9, v15}, Landroid/database/Cursor;->getLong(I)J

    .line 1274
    move-result-wide v2

    .line 1275
    const/4 v15, 0x7

    .line 1276
    invoke-interface {v9, v15}, Landroid/database/Cursor;->getInt(I)I

    .line 1279
    const/16 v15, 0x8

    .line 1281
    invoke-interface {v9, v15}, Landroid/database/Cursor;->getInt(I)I

    .line 1284
    const/16 v15, 0x9

    .line 1286
    invoke-interface {v9, v15}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1289
    move-result-object v19

    .line 1290
    if-nez v19, :cond_592

    .line 1292
    move-object/from16 v15, v16

    .line 1294
    goto :goto_594

    .line 1295
    :cond_592
    move-object/from16 v15, v19

    .line 1297
    :goto_594
    invoke-static {v13, v2, v3}, Lcom/arlosoft/macrodroid/action/GetCalendarEventsAction;->l0(Landroid/content/ContentResolver;J)Ljava/lang/String;

    .line 1300
    move-result-object v2
    :try_end_598
    .catch Ljava/lang/Exception; {:try_start_554 .. :try_end_598} :catch_6ed
    .catchall {:try_start_554 .. :try_end_598} :catchall_6a7

    .line 1301
    :try_start_598
    new-instance v3, Ldib;

    .line 1303
    invoke-direct {v3, v4, v1}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1306
    new-instance v1, Ldib;

    .line 1308
    invoke-direct {v1, v5, v14}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5a2
    .catch Ljava/lang/Exception; {:try_start_598 .. :try_end_5a2} :catch_703
    .catchall {:try_start_598 .. :try_end_5a2} :catchall_6a7

    .line 1311
    :try_start_5a2
    invoke-static {v11, v12}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1314
    move-result-object v14
    :try_end_5a6
    .catch Ljava/lang/Exception; {:try_start_5a2 .. :try_end_5a6} :catch_6ed
    .catchall {:try_start_5a2 .. :try_end_5a6} :catchall_6a7

    .line 1315
    move-object/from16 v19, v1

    .line 1317
    :try_start_5a8
    new-instance v1, Ldib;

    .line 1319
    invoke-direct {v1, v6, v14}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5ad
    .catch Ljava/lang/Exception; {:try_start_5a8 .. :try_end_5ad} :catch_703
    .catchall {:try_start_5a8 .. :try_end_5ad} :catchall_6a7

    .line 1322
    :try_start_5ad
    invoke-static/range {v17 .. v18}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1325
    move-result-object v14
    :try_end_5b1
    .catch Ljava/lang/Exception; {:try_start_5ad .. :try_end_5b1} :catch_6ed
    .catchall {:try_start_5ad .. :try_end_5b1} :catchall_6a7

    .line 1326
    move-object/from16 v20, v1

    .line 1328
    :try_start_5b3
    new-instance v1, Ldib;

    .line 1330
    invoke-direct {v1, v7, v14}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5b8
    .catch Ljava/lang/Exception; {:try_start_5b3 .. :try_end_5b8} :catch_703
    .catchall {:try_start_5b3 .. :try_end_5b8} :catchall_6a7

    .line 1333
    :try_start_5b8
    new-instance v14, Ljava/util/Date;

    .line 1335
    invoke-direct {v14, v11, v12}, Ljava/util/Date;-><init>(J)V

    .line 1338
    invoke-virtual {v0, v14}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 1341
    move-result-object v14
    :try_end_5c1
    .catch Ljava/lang/Exception; {:try_start_5b8 .. :try_end_5c1} :catch_6ed
    .catchall {:try_start_5b8 .. :try_end_5c1} :catchall_6a7

    .line 1342
    move-object/from16 v21, v1

    move-object/from16 v21, v1

    .line 1344
    :try_start_5c5
    new-instance v1, Ldib;

    .line 1346
    invoke-direct {v1, v8, v14}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5ca
    .catch Ljava/lang/Exception; {:try_start_5c5 .. :try_end_5ca} :catch_703
    .catchall {:try_start_5c5 .. :try_end_5ca} :catchall_6a7

    .line 1349
    :try_start_5ca
    new-instance v14, Ljava/util/Date;

    .line 1351
    move-wide/from16 v49, v11

    .line 1353
    move-wide/from16 v11, v17

    .line 1355
    invoke-direct {v14, v11, v12}, Ljava/util/Date;-><init>(J)V

    .line 1358
    invoke-virtual {v0, v14}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 1361
    move-result-object v14
    :try_end_5d7
    .catch Ljava/lang/Exception; {:try_start_5ca .. :try_end_5d7} :catch_6ed
    .catchall {:try_start_5ca .. :try_end_5d7} :catchall_6a7

    .line 1362
    move-object/from16 v17, v0

    .line 1364
    :try_start_5d9
    new-instance v0, Ldib;
    :try_end_5db
    .catch Ljava/lang/Exception; {:try_start_5d9 .. :try_end_5db} :catch_6e7
    .catchall {:try_start_5d9 .. :try_end_5db} :catchall_6a7

    .line 1366
    move-object/from16 v18, v1

    .line 1368
    move-object/from16 v1, v46

    .line 1370
    :try_start_5df
    invoke-direct {v0, v1, v14}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5e2
    .catch Ljava/lang/Exception; {:try_start_5df .. :try_end_5e2} :catch_6d3
    .catchall {:try_start_5df .. :try_end_5e2} :catchall_6a7

    .line 1373
    sub-long v11, v11, v49

    .line 1375
    :try_start_5e4
    div-long v11, v11, v38

    .line 1377
    invoke-static {v11, v12}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1380
    move-result-object v11
    :try_end_5ea
    .catch Ljava/lang/Exception; {:try_start_5e4 .. :try_end_5ea} :catch_6c1
    .catchall {:try_start_5e4 .. :try_end_5ea} :catchall_6a7

    .line 1381
    :try_start_5ea
    new-instance v12, Ldib;
    :try_end_5ec
    .catch Ljava/lang/Exception; {:try_start_5ea .. :try_end_5ec} :catch_6bd
    .catchall {:try_start_5ea .. :try_end_5ec} :catchall_6a7

    .line 1383
    move-object/from16 v14, v47

    .line 1385
    :try_start_5ee
    invoke-direct {v12, v14, v11}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_5f1
    .catch Ljava/lang/Exception; {:try_start_5ee .. :try_end_5f1} :catch_6bb
    .catchall {:try_start_5ee .. :try_end_5f1} :catchall_6a7

    .line 1388
    :try_start_5f1
    invoke-static/range {p0 .. p0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    .line 1391
    move-result-object v11
    :try_end_5f5
    .catch Ljava/lang/Exception; {:try_start_5f1 .. :try_end_5f5} :catch_6ab
    .catchall {:try_start_5f1 .. :try_end_5f5} :catchall_6a7

    .line 1392
    move-object/from16 p0, v0

    .line 1394
    :try_start_5f7
    new-instance v0, Ldib;
    :try_end_5f9
    .catch Ljava/lang/Exception; {:try_start_5f7 .. :try_end_5f9} :catch_6a3
    .catchall {:try_start_5f7 .. :try_end_5f9} :catchall_6a7

    .line 1396
    move-object/from16 v22, v3

    move-object/from16 v22, v3

    .line 1398
    move-object/from16 v3, p1

    .line 1400
    :try_start_5ff
    invoke-direct {v0, v3, v11}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_602
    .catch Ljava/lang/Exception; {:try_start_5ff .. :try_end_602} :catch_6a1
    .catchall {:try_start_5ff .. :try_end_602} :catchall_6a7

    .line 1403
    :try_start_602
    new-instance v11, Ldib;
    :try_end_604
    .catch Ljava/lang/Exception; {:try_start_602 .. :try_end_604} :catch_699
    .catchall {:try_start_602 .. :try_end_604} :catchall_6a7

    .line 1405
    move-object/from16 p1, v9

    .line 1407
    move-object/from16 v9, v29

    move-object/from16 v9, v29

    .line 1409
    :try_start_60a
    invoke-direct {v11, v9, v10}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_60d
    .catch Ljava/lang/Exception; {:try_start_60a .. :try_end_60d} :catch_691
    .catchall {:try_start_60a .. :try_end_60d} :catchall_66f

    .line 1412
    :try_start_60d
    new-instance v10, Ldib;
    :try_end_60f
    .catch Ljava/lang/Exception; {:try_start_60d .. :try_end_60f} :catch_68d
    .catchall {:try_start_60d .. :try_end_60f} :catchall_66f

    .line 1414
    move-object/from16 v29, v11

    .line 1416
    move-object/from16 v11, v28

    .line 1418
    :try_start_613
    invoke-direct {v10, v11, v2}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_616
    .catch Ljava/lang/Exception; {:try_start_613 .. :try_end_616} :catch_685
    .catchall {:try_start_613 .. :try_end_616} :catchall_66f

    .line 1421
    :try_start_616
    new-instance v2, Ldib;
    :try_end_618
    .catch Ljava/lang/Exception; {:try_start_616 .. :try_end_618} :catch_681
    .catchall {:try_start_616 .. :try_end_618} :catchall_66f

    .line 1423
    move-object/from16 v28, v10

    .line 1425
    move-object/from16 v10, v24

    move-object/from16 v10, v24

    .line 1427
    :try_start_61e
    invoke-direct {v2, v10, v15}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_621
    .catch Ljava/lang/Exception; {:try_start_61e .. :try_end_621} :catch_67f
    .catchall {:try_start_61e .. :try_end_621} :catchall_66f

    .line 1430
    move-object/from16 v24, v0

    .line 1432
    const/16 v15, 0xb

    .line 1434
    :try_start_625
    new-array v0, v15, [Ldib;

    .line 1436
    const/16 v25, 0x0

    .line 1438
    aput-object v22, v0, v25

    .line 1440
    const/16 v27, 0x1

    .line 1442
    aput-object v19, v0, v27

    .line 1444
    const/16 v26, 0x2

    .line 1446
    aput-object v20, v0, v26

    .line 1448
    const/16 v42, 0x3

    .line 1450
    aput-object v21, v0, v42

    .line 1452
    const/16 v41, 0x4

    .line 1454
    aput-object v18, v0, v41

    .line 1456
    const/16 v33, 0x5

    .line 1458
    aput-object p0, v0, v33

    .line 1460
    const/16 v34, 0x6

    .line 1462
    aput-object v12, v0, v34

    .line 1464
    const/16 v35, 0x7

    .line 1466
    aput-object v24, v0, v35

    .line 1468
    const/16 v36, 0x8

    .line 1470
    aput-object v29, v0, v36

    .line 1472
    const/16 v37, 0x9

    .line 1474
    aput-object v28, v0, v37

    .line 1476
    aput-object v2, v0, v30

    .line 1478
    invoke-static {v0}, Lyw9;->U([Ldib;)Ljava/util/Map;

    .line 1481
    move-result-object v0
    :try_end_655
    .catch Ljava/lang/Exception; {:try_start_625 .. :try_end_655} :catch_67b
    .catchall {:try_start_625 .. :try_end_655} :catchall_66f

    .line 1482
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1484
    :try_start_659
    invoke-virtual {v2, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
    :try_end_65c
    .catch Ljava/lang/Exception; {:try_start_659 .. :try_end_65c} :catch_674
    .catchall {:try_start_659 .. :try_end_65c} :catchall_66f

    .line 1487
    move-object/from16 v23, v2

    .line 1489
    move-object v15, v3

    .line 1490
    move-object v3, v11

    .line 1491
    move-object v12, v14

    .line 1492
    move-object/from16 v0, v17

    move-object/from16 v0, v17

    .line 1494
    move-object/from16 v14, v43

    move-object/from16 v14, v43

    .line 1496
    move-object v2, v1

    .line 1497
    move-object v11, v9

    .line 1498
    move-object/from16 v9, p1

    .line 1500
    goto/16 :goto_515

    .line 1502
    :catchall_66f
    move-exception v0

    .line 1503
    :goto_670
    move-object/from16 v40, p1

    .line 1505
    goto/16 :goto_7bb

    .line 1507
    :catch_674
    move-exception v0

    .line 1508
    :goto_675
    move-object/from16 v40, p1

    move-object/from16 v40, p1

    .line 1510
    goto/16 :goto_79d

    .line 1512
    :catch_67b
    move-exception v0

    .line 1513
    :goto_67c
    move-object/from16 v2, v23

    .line 1515
    goto :goto_675

    .line 1516
    :catch_67f
    move-exception v0

    .line 1517
    goto :goto_67c

    .line 1518
    :catch_681
    move-exception v0

    .line 1519
    move-object/from16 v10, v24

    .line 1521
    goto :goto_67c

    .line 1522
    :catch_685
    move-exception v0

    .line 1523
    :goto_686
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1525
    move-object/from16 v10, v24

    .line 1527
    goto :goto_675

    .line 1528
    :catch_68d
    move-exception v0

    .line 1529
    move-object/from16 v11, v28

    .line 1531
    goto :goto_686

    .line 1532
    :catch_691
    move-exception v0

    .line 1533
    :goto_692
    move-object/from16 v2, v23

    .line 1535
    move-object/from16 v10, v24

    .line 1537
    move-object/from16 v11, v28

    .line 1539
    goto :goto_675

    .line 1540
    :catch_699
    move-exception v0

    .line 1541
    move-object/from16 p1, v9

    move-object/from16 p1, v9

    .line 1543
    move-object/from16 v9, v29

    .line 1545
    goto :goto_692

    .line 1546
    :catch_6a1
    move-exception v0

    .line 1547
    goto :goto_6ae

    .line 1548
    :catch_6a3
    move-exception v0

    .line 1549
    move-object/from16 v3, p1

    .line 1551
    goto :goto_6ae

    .line 1552
    :catchall_6a7
    move-exception v0

    .line 1553
    move-object/from16 p1, v9

    .line 1555
    goto :goto_670

    .line 1556
    :catch_6ab
    move-exception v0

    .line 1557
    :goto_6ac
    move-object/from16 v3, p1

    .line 1559
    :goto_6ae
    move-object/from16 p1, v9

    .line 1561
    move-object/from16 v2, v23

    .line 1563
    move-object/from16 v10, v24

    move-object/from16 v10, v24

    .line 1565
    move-object/from16 v11, v28

    .line 1567
    move-object/from16 v9, v29

    .line 1569
    goto :goto_675

    .line 1570
    :catch_6bb
    move-exception v0

    .line 1571
    goto :goto_6ac

    .line 1572
    :catch_6bd
    move-exception v0

    .line 1573
    move-object/from16 v14, v47

    .line 1575
    goto :goto_6ac

    .line 1576
    :catch_6c1
    move-exception v0

    .line 1577
    move-object/from16 v3, p1

    .line 1579
    move-object/from16 p1, v9

    move-object/from16 p1, v9

    .line 1581
    move-object/from16 v2, v23

    .line 1583
    move-object/from16 v10, v24

    .line 1585
    move-object/from16 v11, v28

    .line 1587
    :goto_6ce
    move-object/from16 v9, v29

    .line 1589
    :goto_6d0
    move-object/from16 v14, v47

    .line 1591
    goto :goto_675

    .line 1592
    :catch_6d3
    move-exception v0

    .line 1593
    :goto_6d4
    move-object/from16 v3, p1

    move-object/from16 v3, p1

    .line 1595
    move-object/from16 p1, v9

    .line 1597
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1599
    move-object/from16 v10, v24

    .line 1601
    move-object/from16 v11, v28

    move-object/from16 v11, v28

    .line 1603
    move-object/from16 v9, v29

    .line 1605
    goto :goto_6d0

    .line 1606
    :catch_6e7
    move-exception v0

    .line 1607
    move-object/from16 v1, v46

    move-object/from16 v1, v46

    .line 1609
    goto :goto_6d4

    .line 1610
    :catch_6ed
    move-exception v0

    .line 1611
    move-object/from16 v3, p1

    .line 1613
    move-object/from16 p1, v9

    .line 1615
    :goto_6f2
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1617
    move-object/from16 v10, v24

    .line 1619
    move-object/from16 v11, v28

    move-object/from16 v11, v28

    .line 1621
    move-object/from16 v9, v29

    .line 1623
    move-object/from16 v1, v46

    move-object/from16 v1, v46

    .line 1625
    goto :goto_6d0

    .line 1626
    :catch_703
    move-exception v0

    .line 1627
    move-object/from16 v3, p1

    .line 1629
    move-object/from16 p1, v9

    .line 1631
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1633
    move-object/from16 v10, v24

    .line 1635
    move-object/from16 v11, v28

    .line 1637
    move-object/from16 v9, v29

    .line 1639
    move-object/from16 v1, v46

    .line 1641
    goto :goto_6d0

    .line 1642
    :catch_715
    move-exception v0

    .line 1643
    move-object/from16 p1, v9

    move-object/from16 p1, v9

    .line 1645
    move-object v3, v15

    .line 1646
    goto :goto_6f2

    .line 1647
    :catch_71c
    move-exception v0

    .line 1648
    move-object v1, v2

    .line 1649
    move-object v11, v3

    .line 1650
    move-object/from16 p1, v9

    .line 1652
    move-object v3, v15

    .line 1653
    move-object/from16 v2, v23

    .line 1655
    move-object/from16 v10, v24

    .line 1657
    goto :goto_6ce

    .line 1658
    :catch_727
    move-exception v0

    .line 1659
    move-object v1, v2

    .line 1660
    move-object/from16 p1, v9

    .line 1662
    move-object v9, v11

    .line 1663
    move-object v14, v12

    .line 1664
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1666
    :goto_731
    move-object v11, v3

    .line 1667
    :goto_732
    move-object v3, v15

    .line 1668
    goto/16 :goto_675

    .line 1670
    :catch_735
    move-exception v0

    .line 1671
    move-object v1, v2

    .line 1672
    move-object/from16 p1, v9

    move-object/from16 p1, v9

    .line 1674
    move-object v9, v11

    move-object v9, v11

    .line 1675
    move-object/from16 v43, v14

    .line 1677
    move-object/from16 v2, v23

    .line 1679
    move-object v11, v3

    move-object v11, v3

    .line 1680
    move-object v14, v12

    .line 1681
    goto :goto_732

    .line 1682
    :cond_745
    move-object v1, v2

    .line 1683
    move-object/from16 v43, v14

    .line 1685
    move-object/from16 v2, v23

    move-object/from16 v2, v23

    .line 1687
    move-object/from16 p1, v9

    .line 1689
    move-object v9, v11

    move-object v9, v11

    .line 1690
    move-object v11, v3

    .line 1691
    move-object v14, v12

    .line 1692
    :goto_752
    move-object v3, v15

    move-object v3, v15

    .line 1693
    goto :goto_772

    .line 1694
    :catch_755
    move-exception v0

    .line 1695
    move-object/from16 p1, v2

    .line 1697
    move-object v2, v1

    .line 1698
    move-object/from16 v1, p1

    move-object/from16 v1, p1

    .line 1700
    move-object/from16 p1, v9

    move-object/from16 p1, v9

    .line 1702
    move-object v9, v11

    move-object v9, v11

    .line 1703
    move-object v14, v12

    .line 1704
    goto :goto_731

    .line 1705
    :cond_765
    move-object/from16 p1, v2

    .line 1707
    move-object v2, v1

    .line 1708
    move-object/from16 v1, p1

    .line 1710
    move-object/from16 p1, v9

    .line 1712
    move-object v9, v11

    move-object v9, v11

    .line 1713
    move-object v14, v12

    move-object v14, v12

    .line 1714
    move-object v11, v3

    .line 1715
    goto :goto_752

    .line 1716
    :goto_772
    if-eqz p1, :cond_7cc

    .line 1718
    invoke-interface/range {p1 .. p1}, Landroid/database/Cursor;->close()V

    .line 1721
    goto/16 :goto_7cc

    .line 1723
    :catch_779
    move-exception v0

    .line 1724
    move-object v9, v2

    move-object v9, v2

    .line 1725
    move-object v2, v1

    .line 1726
    move-object v1, v9

    .line 1727
    move-object v9, v11

    .line 1728
    move-object v14, v12

    .line 1729
    move-object/from16 v13, v17

    .line 1731
    goto/16 :goto_493

    .line 1733
    :catch_784
    move-exception v0

    .line 1734
    move-object v9, v2

    .line 1735
    move-object v2, v1

    .line 1736
    move-object v1, v9

    .line 1737
    move-object v9, v11

    .line 1738
    move-wide/from16 v31, v13

    .line 1740
    :goto_78b
    move-object/from16 v13, v51

    move-object/from16 v13, v51

    .line 1742
    move-object v11, v3

    move-object v11, v3

    .line 1743
    move-object v14, v12

    move-object v14, v12

    .line 1744
    goto/16 :goto_494

    .line 1746
    :catch_795
    move-exception v0

    .line 1747
    move-object v9, v2

    .line 1748
    move-object v2, v1

    .line 1749
    move-object v1, v9

    .line 1750
    move-object v9, v11

    .line 1751
    move-wide/from16 v44, v13

    .line 1753
    goto :goto_78b

    .line 1754
    :goto_79d
    :try_start_79d
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 1757
    move-result-object v0

    .line 1758
    new-instance v12, Ljava/lang/StringBuilder;

    .line 1760
    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    .line 1763
    const-string v15, "Events table fallback query failed: "

    .line 1765
    invoke-virtual {v12, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1768
    invoke-virtual {v12, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1771
    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1774
    move-result-object v0

    .line 1775
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V
    :try_end_7b5
    .catchall {:try_start_79d .. :try_end_7b5} :catchall_488

    .line 1778
    if-eqz v40, :cond_7cc

    .line 1780
    invoke-interface/range {v40 .. v40}, Landroid/database/Cursor;->close()V

    .line 1783
    goto :goto_7cc

    .line 1784
    :goto_7bb
    if-eqz v40, :cond_7c0

    .line 1786
    invoke-interface/range {v40 .. v40}, Landroid/database/Cursor;->close()V

    .line 1789
    :cond_7c0
    throw v0

    .line 1790
    :cond_7c1
    move-object v9, v2

    .line 1791
    move-object v2, v1

    .line 1792
    move-object v1, v9

    .line 1793
    move-object v9, v11

    .line 1794
    move-object v14, v12

    .line 1795
    move-object/from16 v13, v51

    .line 1797
    move-object v11, v3

    move-object v11, v3

    .line 1798
    move-object v3, v15

    move-object v3, v15

    .line 1799
    :cond_7cc
    :goto_7cc
    :try_start_7cc
    const-string v0, "content://com.google.android.apps.tasks/tasks"

    .line 1801
    invoke-static {v0}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 1804
    move-result-object v18

    .line 1805
    const-string v0, "notes"

    .line 1807
    const-string/jumbo v12, "ued"

    const-string v12, "due"

    .line 1809
    const-string v15, "completed"

    .line 1811
    filled-new-array {v4, v0, v12, v15}, [Ljava/lang/String;

    .line 1814
    move-result-object v19

    .line 1815
    const-string v20, "? u d N qu e eAD>?=<d"

    const-string v20, "due >= ? AND due <= ?"

    .line 1817
    invoke-static/range {v31 .. v32}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;

    .line 1820
    move-result-object v0

    .line 1821
    invoke-static/range {v44 .. v45}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;

    .line 1824
    move-result-object v12

    .line 1825
    filled-new-array {v0, v12}, [Ljava/lang/String;

    .line 1828
    move-result-object v21

    .line 1829
    const-string v22, "due ASC"

    .line 1831
    move-object/from16 v17, v13

    .line 1833
    invoke-virtual/range {v17 .. v22}, Landroid/content/ContentResolver;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;

    .line 1836
    move-result-object v12
    :try_end_7f7
    .catch Ljava/lang/Exception; {:try_start_7cc .. :try_end_7f7} :catch_90f

    .line 1837
    if-eqz v12, :cond_90d

    .line 1839
    :try_start_7f9
    new-instance v0, Ljava/text/SimpleDateFormat;

    .line 1841
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    .line 1844
    move-result-object v13

    .line 1845
    move-object/from16 v15, v43

    .line 1847
    invoke-direct {v0, v15, v13}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    .line 1850
    :goto_804
    invoke-interface {v12}, Landroid/database/Cursor;->moveToNext()Z

    .line 1853
    move-result v13

    .line 1854
    if-eqz v13, :cond_8ff

    .line 1856
    const/4 v13, 0x0

    .line 1857
    invoke-interface {v12, v13}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1860
    move-result-object v15

    .line 1861
    if-nez v15, :cond_813

    .line 1863
    move-object/from16 v15, v16

    .line 1865
    :cond_813
    const/4 v13, 0x1

    .line 1866
    invoke-interface {v12, v13}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    .line 1869
    move-result-object v17
    :try_end_818
    .catchall {:try_start_7f9 .. :try_end_818} :catchall_8fc

    .line 1870
    if-nez v17, :cond_826

    .line 1872
    move-object/from16 v13, v16

    .line 1874
    :goto_81c
    move-object/from16 v23, v2

    move-object/from16 v23, v2

    .line 1876
    move-object/from16 v24, v10

    .line 1878
    move-object/from16 v28, v11

    .line 1880
    const/4 v2, 0x2

    .line 1881
    goto :goto_829

    .line 1882
    :cond_826
    move-object/from16 v13, v17

    .line 1884
    goto :goto_81c

    .line 1885
    :goto_829
    :try_start_829
    invoke-interface {v12, v2}, Landroid/database/Cursor;->getLong(I)J

    .line 1888
    move-result-wide v10

    .line 1889
    const/4 v2, 0x3

    .line 1890
    invoke-interface {v12, v2}, Landroid/database/Cursor;->getInt(I)I

    .line 1893
    new-instance v2, Ldib;

    .line 1895
    invoke-direct {v2, v4, v15}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1898
    new-instance v15, Ldib;

    .line 1900
    invoke-direct {v15, v5, v13}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1903
    invoke-static {v10, v11}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1906
    move-result-object v13

    .line 1907
    move-object/from16 p0, v2

    .line 1909
    new-instance v2, Ldib;

    .line 1911
    invoke-direct {v2, v6, v13}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1914
    invoke-static {v10, v11}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1917
    move-result-object v13

    .line 1918
    move-object/from16 p1, v2

    .line 1920
    new-instance v2, Ldib;

    .line 1922
    invoke-direct {v2, v7, v13}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1925
    new-instance v13, Ljava/util/Date;

    .line 1927
    invoke-direct {v13, v10, v11}, Ljava/util/Date;-><init>(J)V

    .line 1930
    invoke-virtual {v0, v13}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 1933
    move-result-object v13

    .line 1934
    move-object/from16 v17, v2

    .line 1936
    new-instance v2, Ldib;

    .line 1938
    invoke-direct {v2, v8, v13}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1941
    new-instance v13, Ljava/util/Date;

    .line 1943
    invoke-direct {v13, v10, v11}, Ljava/util/Date;-><init>(J)V

    .line 1946
    invoke-virtual {v0, v13}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 1949
    move-result-object v10

    .line 1950
    new-instance v11, Ldib;

    .line 1952
    invoke-direct {v11, v1, v10}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1955
    const-wide/16 v18, 0x0

    .line 1957
    invoke-static/range {v18 .. v19}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 1960
    move-result-object v10

    .line 1961
    new-instance v13, Ldib;

    .line 1963
    invoke-direct {v13, v14, v10}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1966
    sget-object v10, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    .line 1968
    move-object/from16 v18, v0

    .line 1970
    new-instance v0, Ldib;

    .line 1972
    invoke-direct {v0, v3, v10}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1975
    new-instance v10, Ldib;

    .line 1977
    move-object/from16 v46, v1

    .line 1979
    move-object/from16 v1, v16

    move-object/from16 v1, v16

    .line 1981
    invoke-direct {v10, v9, v1}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1984
    move-object/from16 v16, v0

    .line 1986
    new-instance v0, Ldib;

    .line 1988
    move-object/from16 v19, v2

    .line 1990
    move-object/from16 v2, v28

    .line 1992
    invoke-direct {v0, v2, v1}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 1995
    move-object/from16 v20, v0

    .line 1997
    new-instance v0, Ldib;

    .line 1999
    move-object/from16 v28, v2

    move-object/from16 v28, v2

    .line 2001
    move-object/from16 v2, v24

    move-object/from16 v2, v24

    .line 2003
    invoke-direct {v0, v2, v1}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 2006
    move-object/from16 v22, v0

    .line 2008
    move-object/from16 v21, v1

    .line 2010
    const/16 v1, 0xb

    .line 2012
    new-array v0, v1, [Ldib;

    .line 2014
    const/16 v25, 0x0

    .line 2016
    aput-object p0, v0, v25

    .line 2018
    const/16 v27, 0x1

    .line 2020
    aput-object v15, v0, v27

    .line 2022
    const/16 v26, 0x2

    .line 2024
    aput-object p1, v0, v26

    .line 2026
    const/16 v42, 0x3

    .line 2028
    aput-object v17, v0, v42

    .line 2030
    const/16 v41, 0x4

    .line 2032
    aput-object v19, v0, v41

    .line 2034
    const/16 v33, 0x5

    .line 2036
    aput-object v11, v0, v33

    .line 2038
    const/16 v34, 0x6

    .line 2040
    aput-object v13, v0, v34

    .line 2042
    const/16 v35, 0x7

    .line 2044
    aput-object v16, v0, v35

    .line 2046
    const/16 v36, 0x8

    .line 2048
    aput-object v10, v0, v36

    .line 2050
    const/16 v37, 0x9

    .line 2052
    aput-object v20, v0, v37

    .line 2054
    aput-object v22, v0, v30

    .line 2056
    invoke-static {v0}, Lyw9;->U([Ldib;)Ljava/util/Map;

    .line 2059
    move-result-object v0
    :try_end_8de
    .catchall {:try_start_829 .. :try_end_8de} :catchall_8f8

    .line 2060
    move-object/from16 v10, v23

    .line 2062
    :try_start_8e0
    invoke-virtual {v10, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
    :try_end_8e3
    .catchall {:try_start_8e0 .. :try_end_8e3} :catchall_8f4

    .line 2065
    move-object v0, v10

    .line 2066
    move-object v10, v2

    .line 2067
    move-object v2, v0

    .line 2068
    move-object/from16 v0, v18

    move-object/from16 v0, v18

    .line 2070
    move-object/from16 v16, v21

    .line 2072
    move-object/from16 v11, v28

    move-object/from16 v11, v28

    .line 2074
    move-object/from16 v1, v46

    .line 2076
    goto/16 :goto_804

    .line 2078
    :catchall_8f4
    move-exception v0

    .line 2079
    :goto_8f5
    move-object v1, v0

    move-object v1, v0

    .line 2080
    goto :goto_907

    .line 2081
    :catchall_8f8
    move-exception v0

    .line 2082
    move-object/from16 v10, v23

    .line 2084
    goto :goto_8f5

    .line 2085
    :catchall_8fc
    move-exception v0

    .line 2086
    move-object v10, v2

    .line 2087
    goto :goto_8f5

    .line 2088
    :cond_8ff
    move-object v10, v2

    move-object v10, v2

    .line 2089
    :try_start_901
    invoke-interface {v12}, Ljava/io/Closeable;->close()V
    :try_end_904
    .catch Ljava/lang/Exception; {:try_start_901 .. :try_end_904} :catch_905

    .line 2092
    goto :goto_927

    .line 2093
    :catch_905
    move-exception v0

    .line 2094
    goto :goto_912

    .line 2095
    :goto_907
    :try_start_907
    throw v1
    :try_end_908
    .catchall {:try_start_907 .. :try_end_908} :catchall_908

    .line 2096
    :catchall_908
    move-exception v0

    .line 2097
    :try_start_909
    invoke-static {v12, v1}, Lxt0;->n(Ljava/io/Closeable;Ljava/lang/Throwable;)V

    .line 2100
    throw v0
    :try_end_90d
    .catch Ljava/lang/Exception; {:try_start_909 .. :try_end_90d} :catch_905

    .line 2101
    :cond_90d
    move-object v10, v2

    .line 2102
    goto :goto_927

    .line 2103
    :catch_90f
    move-exception v0

    .line 2104
    move-object v10, v2

    move-object v10, v2

    .line 2105
    :goto_912
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 2108
    move-result-object v0

    .line 2109
    new-instance v1, Ljava/lang/StringBuilder;

    .line 2111
    const-string v2, "Tasks provider not accessible: "

    .line 2113
    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 2116
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 2119
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 2122
    move-result-object v0

    .line 2123
    invoke-static {v0}, Lkjf;->r(Ljava/lang/String;)V

    .line 2126
    :goto_927
    return-object v10

    .line 2127
    :goto_928
    if-eqz v40, :cond_92d

    .line 2129
    invoke-interface/range {v40 .. v40}, Landroid/database/Cursor;->close()V

    .line 2132
    :cond_92d
    throw v0
.end method
