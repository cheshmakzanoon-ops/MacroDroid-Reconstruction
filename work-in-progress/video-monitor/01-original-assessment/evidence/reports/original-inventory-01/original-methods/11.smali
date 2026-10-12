.method public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;
    .locals 24

    .line 1
    move-object/from16 v1, p0

    .line 3
    sget-object v0, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 5
    iget v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->label:I

    .line 7
    sget-object v3, Lnc5;->a:Lnc5;

    .line 9
    const/4 v4, 0x3

    .line 10
    const/4 v5, 0x2

    .line 11
    sget-object v6, Lblg;->a:Lblg;

    .line 13
    const/4 v7, 0x1

    .line 14
    const/4 v8, 0x0

    .line 15
    const/4 v9, 0x0

    .line 16
    if-eqz v2, :cond_5e

    .line 18
    if-eq v2, v7, :cond_50

    .line 20
    if-eq v2, v5, :cond_2d

    .line 22
    if-ne v2, v4, :cond_25

    .line 24
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 26
    check-cast v0, Ljava/util/List;

    .line 28
    :try_start_1b
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_1e
    .catchall {:try_start_1b .. :try_end_1e} :catchall_22

    .line 31
    move-object/from16 v23, v6

    .line 33
    goto/16 :goto_33b

    .line 35
    :catchall_22
    move-exception v0

    .line 36
    goto/16 :goto_356

    .line 38
    :cond_25
    const-string v0, "o susr aec//n/rt/ovownoeetlek/hlu/f  ecirtb ei/i o/"

    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 40
    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    .line 43
    return-object v9

    .line 44
    :cond_2d
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$4:Ljava/lang/Object;

    .line 46
    check-cast v2, Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 48
    iget-object v5, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$3:Ljava/lang/Object;

    .line 50
    check-cast v5, Ljava/lang/String;

    .line 52
    iget-object v5, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$2:Ljava/lang/Object;

    .line 54
    check-cast v5, Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 56
    iget-object v10, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$1:Ljava/lang/Object;

    .line 58
    check-cast v10, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 60
    iget-object v11, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 62
    check-cast v11, Lvia;

    .line 64
    :try_start_41
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_44
    .catch Ljava/lang/Exception; {:try_start_41 .. :try_end_44} :catch_4d
    .catchall {:try_start_41 .. :try_end_44} :catchall_49

    .line 67
    move-object/from16 v4, p1

    .line 69
    move-object v13, v2

    .line 70
    goto/16 :goto_fd

    .line 72
    :catchall_49
    move-exception v0

    .line 73
    :goto_4a
    move-object v6, v9

    .line 74
    goto/16 :goto_352

    .line 76
    :catch_4d
    move-object v13, v2

    .line 77
    goto/16 :goto_103

    .line 79
    :cond_50
    iget v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->I$0:I

    .line 81
    iget-object v10, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$1:Ljava/lang/Object;

    .line 83
    check-cast v10, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 85
    iget-object v11, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 87
    check-cast v11, Lvia;

    .line 89
    :try_start_5a
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_5d
    .catchall {:try_start_5a .. :try_end_5d} :catchall_22

    .line 92
    goto :goto_79

    .line 93
    :cond_5e
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 96
    :try_start_61
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->this$0:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 98
    iget-object v10, v2, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->q:Lxia;

    .line 100
    iput-object v10, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 102
    iput-object v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$1:Ljava/lang/Object;

    .line 104
    iput v8, v1, Lcom/arlosoft/macrodroid/action/services/k;->I$0:I

    .line 106
    iput v7, v1, Lcom/arlosoft/macrodroid/action/services/k;->label:I

    .line 108
    invoke-virtual {v10, v1}, Lxia;->a(Lm73;)Ljava/lang/Object;

    .line 111
    move-result-object v11
    :try_end_71
    .catchall {:try_start_61 .. :try_end_71} :catchall_22

    .line 112
    if-ne v11, v0, :cond_75

    .line 114
    goto/16 :goto_33a

    .line 116
    :cond_75
    move-object v11, v10

    .line 117
    move-object v10, v2

    move-object v10, v2

    .line 118
    move v2, v8

    .line 119
    :goto_79
    :try_start_79
    sget-object v12, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->z:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService$a;

    .line 121
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->v()Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 124
    move-result-object v12
    :try_end_7f
    .catchall {:try_start_79 .. :try_end_7f} :catchall_34f

    .line 125
    if-eqz v12, :cond_8c

    .line 127
    :try_start_81
    invoke-virtual {v12}, Landroid/view/accessibility/AccessibilityNodeInfo;->getPackageName()Ljava/lang/CharSequence;

    .line 130
    move-result-object v13

    .line 131
    if-eqz v13, :cond_8c

    .line 133
    invoke-virtual {v13}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 136
    move-result-object v13
    :try_end_8b
    .catchall {:try_start_81 .. :try_end_8b} :catchall_49

    .line 137
    goto :goto_8d

    .line 138
    :cond_8c
    move-object v13, v9

    .line 139
    :goto_8d
    :try_start_8d
    sput-object v13, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->L:Ljava/lang/String;
    :try_end_8f
    .catchall {:try_start_8d .. :try_end_8f} :catchall_34f

    .line 141
    if-nez v12, :cond_9c

    .line 143
    :try_start_91
    invoke-interface {v11, v9}, Lvia;->c(Ljava/lang/Object;)V
    :try_end_94
    .catchall {:try_start_91 .. :try_end_94} :catchall_22

    .line 146
    :goto_94
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/k;->this$0:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 148
    iget-object v0, v0, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->r:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 150
    invoke-virtual {v0, v8}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 153
    return-object v6

    .line 154
    :cond_9c
    :try_start_9c
    invoke-virtual {v12}, Landroid/view/accessibility/AccessibilityNodeInfo;->getPackageName()Ljava/lang/CharSequence;

    .line 157
    move-result-object v13
    :try_end_a0
    .catchall {:try_start_9c .. :try_end_a0} :catchall_34f

    .line 158
    if-eqz v13, :cond_a7

    .line 160
    :try_start_a2
    invoke-virtual {v13}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 163
    move-result-object v13

    .line 164
    goto :goto_a8

    .line 165
    :cond_a7
    move-object v13, v9

    .line 166
    :goto_a8
    if-eqz v13, :cond_d8

    .line 168
    sget-object v14, Lcom/arlosoft/macrodroid/triggers/services/MacroDroidAccessibilityServiceJellyBean;->A:Ljava/lang/String;

    .line 170
    invoke-virtual {v13, v14}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    .line 173
    move-result v14

    .line 174
    if-nez v14, :cond_d8

    .line 176
    const-string v14, "oosm.ctmfiarmdodlc.oorr"

    const-string v14, "com.arlosoft.macrodroid"

    .line 178
    invoke-virtual {v13, v14}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    .line 181
    move-result v14

    .line 182
    if-eqz v14, :cond_d0

    .line 184
    sget-object v14, Lcom/arlosoft/macrodroid/common/NonAppActivity;->j:Lcom/arlosoft/macrodroid/common/NonAppActivity$a;

    .line 186
    invoke-virtual {v14}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 189
    sget-object v14, Lcom/arlosoft/macrodroid/common/NonAppActivity;->k:Ljava/util/concurrent/atomic/AtomicInteger;

    .line 191
    invoke-virtual {v14}, Ljava/util/concurrent/atomic/AtomicInteger;->get()I

    .line 194
    move-result v14

    .line 195
    if-lez v14, :cond_cc

    .line 197
    move v14, v7

    move v14, v7

    .line 198
    goto :goto_ce

    .line 199
    :cond_cc
    move v14, v8

    move v14, v8

    .line 200
    :goto_ce
    if-nez v14, :cond_d8

    .line 202
    :cond_d0
    invoke-static {v13}, Lhtg;->O(Ljava/lang/String;)Z

    .line 205
    move-result v14

    .line 206
    if-nez v14, :cond_d8

    .line 208
    sput-object v13, Lcom/arlosoft/macrodroid/triggers/services/MacroDroidAccessibilityServiceJellyBean;->A:Ljava/lang/String;
    :try_end_d8
    .catchall {:try_start_a2 .. :try_end_d8} :catchall_49

    .line 210
    :cond_d8
    :try_start_d8
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->v()Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 213
    move-result-object v13
    :try_end_dc
    .catchall {:try_start_d8 .. :try_end_dc} :catchall_34f

    .line 214
    :try_start_dc
    new-instance v14, Lygg;

    .line 216
    invoke-direct {v14, v10, v9}, Lygg;-><init>(Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;Lm73;)V

    .line 219
    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 221
    iput-object v10, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$1:Ljava/lang/Object;

    .line 223
    iput-object v12, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$2:Ljava/lang/Object;

    .line 225
    iput-object v9, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$3:Ljava/lang/Object;

    .line 227
    iput-object v13, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$4:Ljava/lang/Object;

    .line 229
    iput v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->I$0:I

    .line 231
    iput v8, v1, Lcom/arlosoft/macrodroid/action/services/k;->I$1:I

    .line 233
    iput v5, v1, Lcom/arlosoft/macrodroid/action/services/k;->label:I

    .line 235
    const-wide/16 v4, 0xc8

    .line 237
    invoke-static {v4, v5, v14, v1}, Lpnh;->T(JLjn6;Lm73;)Ljava/lang/Object;

    .line 240
    move-result-object v4
    :try_end_f7
    .catch Ljava/lang/Exception; {:try_start_dc .. :try_end_f7} :catch_106
    .catchall {:try_start_dc .. :try_end_f7} :catchall_49

    .line 241
    if-ne v4, v0, :cond_fb

    .line 243
    goto/16 :goto_33a

    .line 245
    :cond_fb
    move-object v5, v12

    move-object v5, v12

    .line 246
    :goto_fd
    :try_start_fd
    check-cast v4, Ljava/util/List;
    :try_end_ff
    .catch Ljava/lang/Exception; {:try_start_fd .. :try_end_ff} :catch_103
    .catchall {:try_start_fd .. :try_end_ff} :catchall_49

    .line 248
    if-nez v4, :cond_102

    .line 250
    goto :goto_103

    .line 251
    :cond_102
    move-object v3, v4

    .line 252
    :catch_103
    :goto_103
    move-object v4, v11

    .line 253
    move-object v11, v13

    .line 254
    goto :goto_108

    .line 255
    :catch_106
    move-object v5, v12

    .line 256
    goto :goto_103

    .line 257
    :goto_108
    :try_start_108
    invoke-interface {v3}, Ljava/util/List;->isEmpty()Z

    .line 260
    move-result v12
    :try_end_10c
    .catchall {:try_start_108 .. :try_end_10c} :catchall_1f8

    .line 261
    if-eqz v12, :cond_112

    .line 263
    :try_start_10e
    invoke-interface {v4, v9}, Lvia;->c(Ljava/lang/Object;)V
    :try_end_111
    .catchall {:try_start_10e .. :try_end_111} :catchall_22

    .line 266
    goto :goto_94

    .line 267
    :cond_112
    :try_start_112
    sget-object v12, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->z:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService$a;

    .line 269
    invoke-virtual {v12}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 272
    sget-boolean v12, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->I:Z
    :try_end_119
    .catchall {:try_start_112 .. :try_end_119} :catchall_1f8

    .line 274
    if-eqz v12, :cond_152

    .line 276
    :try_start_11b
    new-instance v12, Ljava/util/ArrayList;

    .line 278
    invoke-direct {v12}, Ljava/util/ArrayList;-><init>()V

    .line 281
    new-instance v13, Ljava/util/HashSet;

    .line 283
    invoke-direct {v13}, Ljava/util/HashSet;-><init>()V

    .line 286
    iput v8, v10, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->o:I

    .line 288
    invoke-interface {v3}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 291
    move-result-object v3

    .line 292
    :cond_12b
    :goto_12b
    invoke-interface {v3}, Ljava/util/Iterator;->hasNext()Z

    .line 295
    move-result v14

    .line 296
    if-eqz v14, :cond_178

    .line 298
    invoke-interface {v3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 301
    move-result-object v14

    .line 302
    check-cast v14, Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 304
    if-eqz v14, :cond_12b

    .line 306
    move-object v15, v14

    move-object v15, v14

    .line 307
    invoke-virtual {v15, v11}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    .line 310
    move-result v14

    .line 311
    move-object/from16 v16, v11

    move-object/from16 v16, v11

    .line 313
    move-object v11, v15

    move-object v11, v15

    .line 314
    const/4 v15, 0x0

    .line 315
    move-object/from16 v2, v16

    .line 317
    invoke-virtual/range {v10 .. v15}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->c(Landroid/view/accessibility/AccessibilityNodeInfo;Ljava/util/ArrayList;Ljava/util/HashSet;ZI)V
    :try_end_14b
    .catchall {:try_start_11b .. :try_end_14b} :catchall_14e

    .line 320
    move-object v11, v2

    move-object v11, v2

    .line 321
    goto :goto_12b

    .line 322
    :catchall_14e
    move-exception v0

    .line 323
    move-object v11, v4

    .line 324
    goto/16 :goto_4a

    .line 326
    :cond_152
    move-object v2, v11

    move-object v2, v11

    .line 327
    :try_start_154
    new-instance v12, Ljava/util/ArrayList;

    .line 329
    invoke-direct {v12}, Ljava/util/ArrayList;-><init>()V

    .line 332
    sget-object v13, Lvc5;->a:Lvc5;

    .line 334
    invoke-interface {v3}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 337
    move-result-object v3

    .line 338
    :cond_15f
    :goto_15f
    invoke-interface {v3}, Ljava/util/Iterator;->hasNext()Z

    .line 341
    move-result v11
    :try_end_163
    .catchall {:try_start_154 .. :try_end_163} :catchall_1f8

    .line 342
    if-eqz v11, :cond_178

    .line 344
    :try_start_165
    invoke-interface {v3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 347
    move-result-object v11

    .line 348
    check-cast v11, Landroid/view/accessibility/AccessibilityNodeInfo;

    .line 350
    if-eqz v11, :cond_15f

    .line 352
    invoke-virtual {v11, v2}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    .line 355
    move-result v14

    .line 356
    invoke-virtual {v10}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 359
    invoke-static {v8, v11, v12, v14}, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->a(ILandroid/view/accessibility/AccessibilityNodeInfo;Ljava/util/ArrayList;Z)V
    :try_end_177
    .catchall {:try_start_165 .. :try_end_177} :catchall_14e

    .line 362
    goto :goto_15f

    .line 363
    :cond_178
    :try_start_178
    new-instance v2, Ljava/util/ArrayList;

    .line 365
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 368
    iget-object v3, v10, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->l:Lt2c;

    .line 370
    if-eqz v3, :cond_344

    .line 372
    invoke-virtual {v3}, Lt2c;->a()Ln2c;

    .line 375
    move-result-object v3

    .line 376
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 379
    instance-of v3, v3, Ln2c$c;

    .line 381
    sget-object v11, Lcom/arlosoft/macrodroid/macro/b;->k:Lvq9;

    .line 383
    invoke-virtual {v11}, Lvq9;->a()Lcom/arlosoft/macrodroid/macro/b;

    .line 386
    move-result-object v11

    .line 387
    invoke-virtual {v11}, Lcom/arlosoft/macrodroid/macro/b;->D()Ljava/util/List;

    .line 390
    move-result-object v11

    .line 391
    check-cast v11, Ljava/util/ArrayList;

    .line 393
    invoke-virtual {v11}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 396
    move-result-object v11

    .line 397
    move v14, v8

    move v14, v8

    .line 398
    :cond_19c
    :goto_19c
    invoke-interface {v11}, Ljava/util/Iterator;->hasNext()Z

    .line 401
    move-result v15

    .line 402
    if-eqz v15, :cond_30b

    .line 404
    invoke-interface {v11}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 407
    move-result-object v15

    .line 408
    check-cast v15, Lcom/arlosoft/macrodroid/macro/Macro;

    .line 410
    invoke-virtual {v15}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerListWithAwaitingActions()Ljava/util/ArrayList;

    .line 413
    move-result-object v16

    .line 414
    invoke-virtual/range {v16 .. v16}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 417
    move-result-object v16

    .line 418
    invoke-virtual/range {v16 .. v16}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 421
    :goto_1b3
    invoke-interface/range {v16 .. v16}, Ljava/util/Iterator;->hasNext()Z

    .line 424
    move-result v17

    .line 425
    if-eqz v17, :cond_19c

    .line 427
    invoke-interface/range {v16 .. v16}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 430
    move-result-object v17

    .line 431
    move-object/from16 v9, v17

    .line 433
    check-cast v9, Lcom/arlosoft/macrodroid/triggers/Trigger;

    .line 435
    instance-of v8, v9, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 437
    if-eqz v8, :cond_307

    .line 439
    move-object v8, v9

    .line 440
    check-cast v8, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 442
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->q0()I

    .line 445
    move-result v8

    .line 446
    if-ne v8, v7, :cond_1cf

    .line 448
    move v14, v7

    .line 449
    :cond_1cf
    move-object v8, v9

    .line 450
    check-cast v8, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 452
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->r0()Ljava/util/ArrayList;

    .line 455
    move-result-object v8

    .line 456
    invoke-virtual {v8}, Ljava/util/ArrayList;->isEmpty()Z

    .line 459
    move-result v8

    .line 460
    if-nez v8, :cond_1fd

    .line 462
    move-object v8, v9

    .line 463
    check-cast v8, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 465
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->r0()Ljava/util/ArrayList;

    .line 468
    move-result-object v8

    .line 469
    invoke-virtual {v5}, Landroid/view/accessibility/AccessibilityNodeInfo;->getPackageName()Ljava/lang/CharSequence;

    .line 472
    move-result-object v7

    .line 473
    invoke-static {v8, v7}, Lxj2;->v0(Ljava/lang/Iterable;Ljava/lang/Object;)Z

    .line 476
    move-result v7

    .line 477
    if-eqz v7, :cond_1ee

    .line 479
    goto :goto_1fd

    .line 480
    :cond_1ee
    move/from16 v19, v3

    .line 482
    move-object/from16 v20, v5

    .line 484
    :cond_1f2
    move-object/from16 v23, v6

    move-object/from16 v23, v6

    .line 486
    goto/16 :goto_2f6

    .line 488
    :catchall_1f8
    move-exception v0

    .line 489
    move-object v11, v4

    .line 490
    :goto_1fa
    const/4 v6, 0x0

    .line 491
    goto/16 :goto_352

    .line 493
    :cond_1fd
    :goto_1fd
    move-object v7, v9

    .line 494
    check-cast v7, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 496
    invoke-virtual {v10}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 499
    move-result-object v8

    .line 500
    invoke-static {v8}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 503
    move-result-object v8

    .line 504
    move/from16 v19, v3

    .line 506
    const-string/jumbo v3, "tr_eovgftrinciatyuc"

    const-string v3, "current_fg_activity"

    .line 508
    move-object/from16 v20, v5

    .line 510
    const-string v5, "none"

    .line 512
    invoke-interface {v8, v3, v5}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 515
    move-result-object v3

    .line 516
    invoke-virtual {v7, v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->z0(Ljava/lang/String;)Z

    .line 519
    move-result v3

    .line 520
    if-eqz v3, :cond_1f2

    .line 522
    move-object v3, v9

    .line 523
    check-cast v3, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 525
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->t0()Ljava/lang/String;

    .line 528
    move-result-object v3

    .line 529
    if-eqz v3, :cond_22c

    .line 531
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    .line 534
    move-result v5

    .line 535
    if-nez v5, :cond_232

    .line 537
    :cond_22c
    move-object/from16 v23, v6

    move-object/from16 v23, v6

    .line 539
    goto/16 :goto_2ed

    .line 541
    :cond_232
    move-object v5, v9

    .line 542
    check-cast v5, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 544
    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->y0()Z

    .line 547
    move-result v5

    .line 548
    move-object v7, v9

    move-object v7, v9

    .line 549
    check-cast v7, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 551
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->x0()Z

    .line 554
    move-result v7

    .line 555
    invoke-static {v3, v5, v7}, Lyih;->b(Ljava/lang/String;ZZ)Ljava/lang/String;

    .line 558
    move-result-object v3

    .line 559
    move-object v5, v9

    .line 560
    check-cast v5, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 562
    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->q0()I

    .line 565
    move-result v5

    .line 566
    if-nez v5, :cond_250

    .line 568
    move-object v5, v12

    .line 569
    goto :goto_253

    .line 570
    :cond_250
    move-object v5, v13

    .line 571
    check-cast v5, Ljava/util/Collection;

    .line 573
    :goto_253
    check-cast v5, Ljava/lang/Iterable;

    .line 575
    invoke-interface {v5}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 578
    move-result-object v5

    .line 579
    :goto_259
    invoke-interface {v5}, Ljava/util/Iterator;->hasNext()Z

    .line 582
    move-result v7

    .line 583
    if-eqz v7, :cond_2a0

    .line 585
    invoke-interface {v5}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 588
    move-result-object v7

    .line 589
    move-object v8, v7

    .line 590
    check-cast v8, Lszf;

    .line 592
    move-object/from16 v21, v5

    move-object/from16 v21, v5

    .line 594
    iget-boolean v5, v8, Lszf;->b:Z

    .line 596
    if-nez v5, :cond_27f

    .line 598
    if-eqz v19, :cond_27a

    .line 600
    move-object v5, v9

    .line 601
    check-cast v5, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 603
    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->o0()Z

    .line 606
    move-result v5

    .line 607
    if-eqz v5, :cond_27a

    .line 609
    goto :goto_27f

    .line 610
    :cond_27a
    move-object/from16 v23, v6

    move-object/from16 v23, v6

    .line 612
    goto :goto_299

    .line 613
    :cond_27f
    :goto_27f
    iget-object v5, v8, Lszf;->a:Ljava/lang/String;

    .line 615
    move-object v8, v9

    .line 616
    check-cast v8, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 618
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->y0()Z

    .line 621
    move-result v8

    .line 622
    move-object/from16 v22, v9

    .line 624
    check-cast v22, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 626
    move-object/from16 v23, v6

    .line 628
    invoke-virtual/range {v22 .. v22}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->x0()Z

    .line 631
    move-result v6

    .line 632
    invoke-static {v5, v3, v8, v6}, Lyih;->d(Ljava/lang/String;Ljava/lang/String;ZZ)Z

    .line 635
    move-result v5

    .line 636
    if-eqz v5, :cond_299

    .line 638
    goto :goto_2a3

    .line 639
    :cond_299
    :goto_299
    move-object/from16 v5, v21

    .line 641
    move-object/from16 v6, v23

    move-object/from16 v6, v23

    .line 643
    goto :goto_259

    .line 644
    :cond_2a0
    move-object/from16 v23, v6

    .line 646
    const/4 v7, 0x0

    .line 647
    :goto_2a3
    check-cast v7, Lszf;

    .line 649
    move-object v3, v9

    .line 650
    check-cast v3, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 652
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->p0()Z

    .line 655
    move-result v3

    .line 656
    if-eqz v3, :cond_2b1

    .line 658
    if-nez v7, :cond_2ef

    .line 660
    goto :goto_2b3

    .line 661
    :cond_2b1
    if-eqz v7, :cond_2ef

    .line 663
    :goto_2b3
    move-object v3, v9

    .line 664
    check-cast v3, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 666
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->n0()Z

    .line 669
    move-result v3

    .line 670
    if-eqz v3, :cond_2ed

    .line 672
    move-object v3, v9

    move-object v3, v9

    .line 673
    check-cast v3, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 675
    const/4 v5, 0x0

    .line 676
    invoke-virtual {v3, v5}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->B0(Z)V

    .line 679
    new-instance v3, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 681
    invoke-direct {v3, v9}, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;-><init>(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 684
    invoke-virtual {v15, v3}, Lcom/arlosoft/macrodroid/macro/Macro;->canInvoke(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z

    .line 687
    move-result v5

    .line 688
    if-eqz v5, :cond_2e2

    .line 690
    move-object v5, v9

    .line 691
    check-cast v5, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 693
    const/4 v6, 0x0

    .line 694
    invoke-virtual {v5, v6}, Lcom/arlosoft/macrodroid/common/SelectableItem;->constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z

    .line 697
    move-result v5

    .line 698
    if-eqz v5, :cond_2e2

    .line 700
    invoke-virtual {v15, v3}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerContextInfo(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)V

    .line 703
    invoke-virtual {v15, v9}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerThatInvoked(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 706
    invoke-virtual {v2, v15}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 709
    :cond_2e2
    move/from16 v3, v19

    .line 711
    move-object/from16 v5, v20

    .line 713
    move-object/from16 v6, v23

    .line 715
    const/4 v7, 0x1

    .line 716
    const/4 v8, 0x0

    .line 717
    const/4 v9, 0x0

    .line 718
    goto/16 :goto_19c

    .line 720
    :cond_2ed
    :goto_2ed
    const/4 v3, 0x1

    .line 721
    goto :goto_2fc

    .line 722
    :cond_2ef
    check-cast v9, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 724
    const/4 v3, 0x1

    .line 725
    invoke-virtual {v9, v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->B0(Z)V

    .line 728
    goto :goto_2ed

    .line 729
    :goto_2f6
    check-cast v9, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;

    .line 731
    const/4 v3, 0x1

    .line 732
    invoke-virtual {v9, v3}, Lcom/arlosoft/macrodroid/triggers/ScreenContentTrigger;->B0(Z)V

    .line 735
    :goto_2fc
    move v7, v3

    .line 736
    move/from16 v3, v19

    .line 738
    move-object/from16 v5, v20

    move-object/from16 v5, v20

    .line 740
    move-object/from16 v6, v23

    move-object/from16 v6, v23

    .line 742
    :cond_307
    const/4 v8, 0x0

    .line 743
    const/4 v9, 0x0

    .line 744
    goto/16 :goto_1b3

    .line 746
    :cond_30b
    move-object/from16 v23, v6

    .line 748
    sget-object v3, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->z:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService$a;

    .line 750
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 753
    sput-boolean v14, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->I:Z
    :try_end_314
    .catchall {:try_start_178 .. :try_end_314} :catchall_1f8

    .line 755
    const/4 v6, 0x0

    .line 756
    :try_start_315
    invoke-interface {v4, v6}, Lvia;->c(Ljava/lang/Object;)V

    .line 759
    invoke-virtual {v2}, Ljava/util/ArrayList;->isEmpty()Z

    .line 762
    move-result v3

    .line 763
    if-nez v3, :cond_33b

    .line 765
    sget-object v3, Lzp4;->a:Lad4;

    .line 767
    sget-object v3, Lat9;->a:Lm47;

    .line 769
    new-instance v4, Lxgg;

    .line 771
    invoke-direct {v4, v2, v6}, Lxgg;-><init>(Ljava/util/List;Lm73;)V

    .line 774
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$0:Ljava/lang/Object;

    .line 776
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$1:Ljava/lang/Object;

    .line 778
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$2:Ljava/lang/Object;

    .line 780
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$3:Ljava/lang/Object;

    .line 782
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/k;->L$4:Ljava/lang/Object;

    .line 784
    const/4 v2, 0x3

    .line 785
    iput v2, v1, Lcom/arlosoft/macrodroid/action/services/k;->label:I

    .line 787
    invoke-static {v3, v4, v1}, Ldt9;->e0(Li93;Ljn6;Lm73;)Ljava/lang/Object;

    .line 790
    move-result-object v2
    :try_end_338
    .catchall {:try_start_315 .. :try_end_338} :catchall_22

    .line 791
    if-ne v2, v0, :cond_33b

    .line 793
    :goto_33a
    return-object v0

    .line 794
    :cond_33b
    :goto_33b
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/k;->this$0:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 796
    iget-object v0, v0, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->r:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 798
    const/4 v5, 0x0

    .line 799
    invoke-virtual {v0, v5}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 802
    return-object v23

    .line 803
    :cond_344
    :try_start_344
    const-string/jumbo v0, "upaltbSHarertumeisdm"

    const-string v0, "premiumStatusHandler"

    .line 805
    invoke-static {v0}, Lj68;->h0(Ljava/lang/String;)V

    .line 808
    const/16 v18, 0x0

    .line 810
    throw v18
    :try_end_34f
    .catchall {:try_start_344 .. :try_end_34f} :catchall_1f8

    .line 811
    :catchall_34f
    move-exception v0

    .line 812
    goto/16 :goto_1fa

    .line 814
    :goto_352
    :try_start_352
    invoke-interface {v11, v6}, Lvia;->c(Ljava/lang/Object;)V

    .line 817
    throw v0
    :try_end_356
    .catchall {:try_start_352 .. :try_end_356} :catchall_22

    .line 818
    :goto_356
    iget-object v1, v1, Lcom/arlosoft/macrodroid/action/services/k;->this$0:Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 820
    iget-object v1, v1, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;->r:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 822
    const/4 v5, 0x0

    .line 823
    invoke-virtual {v1, v5}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 826
    throw v0
.end method
