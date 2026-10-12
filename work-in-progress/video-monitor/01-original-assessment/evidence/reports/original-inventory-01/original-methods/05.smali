.method public final secondaryItemConfirmed()V
    .locals 55

    .line 1
    move-object/from16 v1, p0

    .line 3
    iget v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->action:I

    .line 5
    const-string v7, "250"

    .line 7
    const-string v8, "500"

    .line 9
    const v15, 0x7f0a0d75

    .line 12
    const v6, 0x7f0a0d74

    .line 15
    const v12, 0x7f0a0d71

    .line 18
    const v13, 0x7f0a0d70

    .line 21
    const-string v2, ", "

    const-string v2, ", "

    .line 23
    const-string v3, ": "

    .line 25
    const v21, 0x7f141341

    .line 28
    const v22, 0x7f141003

    .line 31
    const v14, 0x7f0a0e5a

    .line 34
    const v4, 0x7f0a0252

    .line 37
    const v5, 0x7f0a0ca4

    .line 40
    const v9, 0x7f0a0f96

    .line 43
    const-string v34, "0"

    const-string v34, "0"

    .line 45
    move-object/from16 v36, v7

    .line 47
    const/4 v10, 0x0

    .line 48
    packed-switch v0, :pswitch_data_104e

    .line 51
    return-void

    .line 52
    :pswitch_37
    new-instance v0, Lvf0;

    .line 54
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 57
    move-result-object v7

    .line 58
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 61
    move-result v11

    .line 62
    invoke-direct {v0, v7, v11}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 65
    const v7, 0x7f0d02c8

    .line 68
    const v11, 0x7f1418a7

    .line 71
    invoke-static {v0, v7, v11, v0, v10}, Liu1;->x(Lvf0;IILvf0;I)V

    .line 74
    invoke-static {v0}, Lxje;->l(Lvf0;)V

    .line 77
    iget-object v7, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 79
    instance-of v11, v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;

    .line 81
    if-eqz v11, :cond_59

    .line 83
    check-cast v7, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;

    .line 85
    goto :goto_5a

    .line 86
    :cond_59
    const/4 v7, 0x0

    .line 87
    :goto_5a
    invoke-virtual {v0, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 90
    move-result-object v9

    .line 91
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 94
    check-cast v9, Landroid/widget/Button;

    .line 96
    invoke-virtual {v0, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 99
    move-result-object v5

    .line 100
    move-object v11, v5

    .line 101
    check-cast v11, Landroid/widget/Button;

    .line 103
    invoke-virtual {v0, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 106
    move-result-object v4

    .line 107
    check-cast v4, Landroid/widget/Button;

    .line 109
    invoke-virtual {v0, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 112
    move-result-object v5

    .line 113
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 116
    check-cast v5, Landroid/widget/EditText;

    .line 118
    invoke-virtual {v0, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 121
    move-result-object v12

    .line 122
    invoke-virtual {v12}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 125
    check-cast v12, Landroid/widget/EditText;

    .line 127
    invoke-virtual {v0, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 130
    move-result-object v6

    .line 131
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 134
    check-cast v6, Landroid/widget/EditText;

    .line 136
    invoke-virtual {v0, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 139
    move-result-object v13

    .line 140
    invoke-virtual {v13}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 143
    check-cast v13, Landroid/widget/EditText;

    .line 145
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 148
    move-result-object v14

    .line 149
    check-cast v14, Landroid/widget/TextView;

    .line 151
    const v15, 0x7f0a0589

    .line 154
    invoke-virtual {v0, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 157
    move-result-object v15

    .line 158
    check-cast v15, Landroid/widget/EditText;

    .line 160
    const v10, 0x7f0a1296

    .line 163
    invoke-virtual {v0, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 166
    move-result-object v10

    .line 167
    check-cast v10, Landroid/widget/CheckBox;

    .line 169
    move-object/from16 v16, v4

    move-object/from16 v16, v4

    .line 171
    const v4, 0x7f0a0c08

    .line 174
    invoke-virtual {v0, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 177
    move-result-object v4

    .line 178
    check-cast v4, Landroid/widget/TextView;

    .line 180
    move-object/from16 v17, v7

    .line 182
    const v7, 0x7f0a0e88

    .line 185
    invoke-virtual {v0, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 188
    move-result-object v7

    .line 189
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 192
    check-cast v7, Landroid/widget/EditText;

    .line 194
    move-object/from16 v40, v8

    .line 196
    const v8, 0x7f0a0dd6

    .line 199
    invoke-virtual {v0, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 202
    move-result-object v8

    .line 203
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 206
    check-cast v8, Landroid/widget/RadioButton;

    .line 208
    move-object/from16 v18, v11

    .line 210
    const v11, 0x7f0a0dd5

    .line 213
    invoke-virtual {v0, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 216
    move-result-object v11

    .line 217
    invoke-virtual {v11}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 220
    check-cast v11, Landroid/widget/RadioButton;

    .line 222
    move-object/from16 v19, v14

    move-object/from16 v19, v14

    .line 224
    const v14, 0x7f0a0d6e

    .line 227
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 230
    move-result-object v14

    .line 231
    check-cast v14, Landroid/widget/Button;

    .line 233
    move-object/from16 v20, v14

    .line 235
    const v14, 0x7f0a0d6f

    .line 238
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 241
    move-result-object v14

    .line 242
    check-cast v14, Landroid/widget/Button;

    .line 244
    move-object/from16 v23, v14

    move-object/from16 v23, v14

    .line 246
    const v14, 0x7f0a0d72

    .line 249
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 252
    move-result-object v14

    .line 253
    check-cast v14, Landroid/widget/Button;

    .line 255
    move-object/from16 v24, v14

    move-object/from16 v24, v14

    .line 257
    const v14, 0x7f0a0d73

    .line 260
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 263
    move-result-object v14

    .line 264
    check-cast v14, Landroid/widget/Button;

    .line 266
    move-object/from16 v27, v14

    .line 268
    const v14, 0x7f0a0e89

    .line 271
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 274
    move-result-object v14

    .line 275
    check-cast v14, Landroid/widget/Button;

    .line 277
    move-object/from16 v28, v14

    .line 279
    const v14, 0x7f0a0c09

    .line 282
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 285
    move-result-object v14

    .line 286
    check-cast v14, Landroid/widget/Button;

    .line 288
    move-object/from16 v26, v14

    move-object/from16 v26, v14

    .line 290
    const v14, 0x7f0a0f95

    .line 293
    invoke-virtual {v0, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 296
    move-result-object v14

    .line 297
    invoke-virtual {v14}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 300
    check-cast v14, Landroid/widget/CheckBox;

    .line 302
    if-eqz v17, :cond_148

    .line 304
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getShowTouchLocation()Z

    .line 307
    move-result v25

    .line 308
    move/from16 v54, v25

    .line 310
    move-object/from16 v25, v0

    .line 312
    move/from16 v0, v54

    .line 314
    goto :goto_14b

    .line 315
    :cond_148
    move-object/from16 v25, v0

    .line 317
    const/4 v0, 0x0

    .line 318
    :goto_14b
    invoke-virtual {v14, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 321
    if-nez v17, :cond_157

    .line 323
    const/4 v0, 0x1

    .line 324
    invoke-virtual {v8, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 327
    move/from16 v37, v0

    .line 329
    goto :goto_16c

    .line 330
    :cond_157
    const/4 v0, 0x1

    .line 331
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getXyPercentages()Z

    .line 334
    move-result v29

    .line 335
    move/from16 v37, v0

    move/from16 v37, v0

    .line 337
    xor-int/lit8 v0, v29, 0x1

    .line 339
    invoke-virtual {v8, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 342
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getXyPercentages()Z

    .line 345
    move-result v0

    .line 346
    invoke-virtual {v11, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 349
    :goto_16c
    new-instance v0, Lfig;

    .line 351
    const/4 v8, 0x0

    .line 352
    invoke-direct {v0, v1, v8}, Lfig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Lm73;)V

    .line 355
    invoke-static {v9, v0}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 358
    if-eqz v4, :cond_18a

    .line 360
    invoke-static/range {v22 .. v22}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 363
    move-result-object v0

    .line 364
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 367
    sget-object v8, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    .line 369
    invoke-virtual {v0, v8}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    .line 372
    move-result-object v0

    .line 373
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 376
    invoke-virtual {v4, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 379
    :cond_18a
    if-eqz v10, :cond_198

    .line 381
    if-eqz v17, :cond_193

    .line 383
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getWaitBeforeNext()Z

    .line 386
    move-result v0

    .line 387
    goto :goto_195

    .line 388
    :cond_193
    move/from16 v0, v37

    .line 390
    :goto_195
    invoke-virtual {v10, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 393
    :cond_198
    if-eqz v17, :cond_19f

    .line 395
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1XVarName()Ljava/lang/String;

    .line 398
    move-result-object v0

    .line 399
    goto :goto_1a0

    .line 400
    :cond_19f
    const/4 v0, 0x0

    .line 401
    :goto_1a0
    if-eqz v0, :cond_1aa

    .line 403
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1XVarName()Ljava/lang/String;

    .line 406
    move-result-object v0

    .line 407
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 410
    goto :goto_1bd

    .line 411
    :cond_1aa
    if-eqz v17, :cond_1b6

    .line 413
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1X()I

    .line 416
    move-result v0

    .line 417
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 420
    move-result-object v0

    .line 421
    if-nez v0, :cond_1ba

    .line 423
    :cond_1b6
    move-object/from16 v0, v34

    move-object/from16 v0, v34

    .line 425
    :cond_1ba
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 428
    :goto_1bd
    if-eqz v17, :cond_1c4

    .line 430
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1YVarName()Ljava/lang/String;

    .line 433
    move-result-object v0

    .line 434
    goto :goto_1c5

    .line 435
    :cond_1c4
    const/4 v0, 0x0

    .line 436
    :goto_1c5
    if-eqz v0, :cond_1cf

    .line 438
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1YVarName()Ljava/lang/String;

    .line 441
    move-result-object v0

    .line 442
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 445
    goto :goto_1e2

    .line 446
    :cond_1cf
    if-eqz v17, :cond_1db

    .line 448
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint1Y()I

    .line 451
    move-result v0

    .line 452
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 455
    move-result-object v0

    .line 456
    if-nez v0, :cond_1df

    .line 458
    :cond_1db
    move-object/from16 v0, v34

    move-object/from16 v0, v34

    .line 460
    :cond_1df
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 463
    :goto_1e2
    if-eqz v17, :cond_1e9

    .line 465
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2XVarName()Ljava/lang/String;

    .line 468
    move-result-object v0

    .line 469
    goto :goto_1ea

    .line 470
    :cond_1e9
    const/4 v0, 0x0

    .line 471
    :goto_1ea
    if-eqz v0, :cond_1f4

    .line 473
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2XVarName()Ljava/lang/String;

    .line 476
    move-result-object v0

    .line 477
    invoke-virtual {v6, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 480
    goto :goto_205

    .line 481
    :cond_1f4
    if-eqz v17, :cond_200

    .line 483
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2X()I

    .line 486
    move-result v0

    .line 487
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 490
    move-result-object v0

    .line 491
    if-nez v0, :cond_202

    .line 493
    :cond_200
    move-object/from16 v0, v34

    .line 495
    :cond_202
    invoke-virtual {v6, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 498
    :goto_205
    if-eqz v17, :cond_20c

    .line 500
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2YVarName()Ljava/lang/String;

    .line 503
    move-result-object v0

    .line 504
    goto :goto_20d

    .line 505
    :cond_20c
    const/4 v0, 0x0

    .line 506
    :goto_20d
    if-eqz v0, :cond_217

    .line 508
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2YVarName()Ljava/lang/String;

    .line 511
    move-result-object v0

    .line 512
    invoke-virtual {v13, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 515
    goto :goto_228

    .line 516
    :cond_217
    if-eqz v17, :cond_223

    .line 518
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getPoint2Y()I

    .line 521
    move-result v0

    .line 522
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 525
    move-result-object v0

    .line 526
    if-nez v0, :cond_225

    .line 528
    :cond_223
    move-object/from16 v0, v34

    .line 530
    :cond_225
    invoke-virtual {v13, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 533
    :goto_228
    if-eqz v17, :cond_22f

    .line 535
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getRotateDegreesVarName()Ljava/lang/String;

    .line 538
    move-result-object v0

    .line 539
    goto :goto_230

    .line 540
    :cond_22f
    const/4 v0, 0x0

    .line 541
    :goto_230
    if-eqz v0, :cond_23a

    .line 543
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getRotateDegreesVarName()Ljava/lang/String;

    .line 546
    move-result-object v0

    .line 547
    invoke-virtual {v7, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 550
    goto :goto_24d

    .line 551
    :cond_23a
    if-eqz v17, :cond_246

    .line 553
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getRotateDegrees()I

    .line 556
    move-result v0

    .line 557
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 560
    move-result-object v0

    .line 561
    if-nez v0, :cond_24a

    .line 563
    :cond_246
    const-string v0, "90"

    const-string v0, "90"

    .line 565
    :cond_24a
    invoke-virtual {v7, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 568
    :goto_24d
    if-eqz v17, :cond_254

    .line 570
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getDurationVarName()Ljava/lang/String;

    .line 573
    move-result-object v0

    .line 574
    goto :goto_255

    .line 575
    :cond_254
    const/4 v0, 0x0

    .line 576
    :goto_255
    if-eqz v0, :cond_261

    .line 578
    if-eqz v15, :cond_279

    .line 580
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getDurationVarName()Ljava/lang/String;

    .line 583
    move-result-object v0

    .line 584
    invoke-virtual {v15, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 587
    goto :goto_279

    .line 588
    :cond_261
    if-eqz v15, :cond_279

    .line 590
    if-eqz v17, :cond_272

    .line 592
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$TwoFingerRotate;->getDurationMs()I

    .line 595
    move-result v0

    .line 596
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 599
    move-result-object v0

    .line 600
    if-nez v0, :cond_270

    .line 602
    goto :goto_272

    .line 603
    :cond_270
    move-object v8, v0

    .line 604
    goto :goto_276

    .line 605
    :cond_272
    :goto_272
    move-object/from16 v8, v40

    move-object/from16 v8, v40

    .line 607
    :goto_276
    invoke-virtual {v15, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 610
    :cond_279
    :goto_279
    new-instance v0, Landroid/graphics/Point;

    .line 612
    invoke-direct {v0}, Landroid/graphics/Point;-><init>()V

    .line 615
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 618
    move-result-object v4

    .line 619
    invoke-virtual {v4}, Landroid/app/Activity;->getWindowManager()Landroid/view/WindowManager;

    .line 622
    move-result-object v4

    .line 623
    invoke-interface {v4}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 626
    move-result-object v4

    .line 627
    invoke-virtual {v4, v0}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 630
    if-eqz v19, :cond_2b4

    .line 632
    invoke-static/range {v21 .. v21}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 635
    move-result-object v4

    .line 636
    iget v8, v0, Landroid/graphics/Point;->x:I

    .line 638
    iget v9, v0, Landroid/graphics/Point;->y:I

    .line 640
    new-instance v1, Ljava/lang/StringBuilder;

    .line 642
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 645
    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 648
    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 651
    invoke-virtual {v1, v8}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 654
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 657
    invoke-virtual {v1, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 660
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 663
    move-result-object v1

    .line 664
    move-object/from16 v2, v19

    .line 666
    invoke-virtual {v2, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 669
    :cond_2b4
    iget v1, v0, Landroid/graphics/Point;->x:I

    .line 671
    iget v2, v0, Landroid/graphics/Point;->y:I

    .line 673
    invoke-static {v1, v2}, Ljava/lang/Math;->max(II)I

    .line 676
    move-result v8

    .line 677
    move-object v3, v0

    .line 678
    new-instance v0, Lgig;

    .line 680
    move-object v1, v7

    .line 681
    const/4 v7, 0x0

    .line 682
    move-object v9, v1

    .line 683
    move-object v2, v5

    .line 684
    move-object v5, v6

    .line 685
    move-object v4, v12

    move-object v4, v12

    .line 686
    move-object v6, v13

    .line 687
    move/from16 v13, v37

    move/from16 v13, v37

    .line 689
    move-object/from16 v1, p0

    .line 691
    invoke-direct/range {v0 .. v7}, Lgig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/graphics/Point;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Lm73;)V

    .line 694
    move-object v3, v5

    move-object v3, v5

    .line 695
    invoke-static {v11, v0}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 698
    move-object/from16 v0, v20

    .line 700
    invoke-static {v1, v2, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 703
    move-object/from16 v0, v23

    .line 705
    invoke-static {v1, v4, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 708
    move-object/from16 v0, v24

    move-object/from16 v0, v24

    .line 710
    invoke-static {v1, v3, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 713
    move-object/from16 v0, v27

    .line 715
    invoke-static {v1, v6, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 718
    move-object/from16 v0, v28

    move-object/from16 v0, v28

    .line 720
    invoke-static {v1, v9, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 723
    if-eqz v15, :cond_2f9

    .line 725
    move-object/from16 v0, v26

    .line 727
    invoke-static {v1, v15, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->p0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 730
    :cond_2f9
    if-eqz v18, :cond_319

    .line 732
    new-instance v0, Ljhg;

    .line 734
    move-object v5, v9

    .line 735
    move-object v7, v11

    .line 736
    move-object v11, v14

    .line 737
    move-object/from16 v14, v18

    .line 739
    move-object/from16 v12, v25

    move-object/from16 v12, v25

    .line 741
    move-object v9, v1

    .line 742
    move-object v1, v2

    .line 743
    move-object v2, v4

    .line 744
    move-object v4, v6

    move-object v4, v6

    .line 745
    move-object v6, v15

    .line 746
    move-object/from16 v15, v16

    move-object/from16 v15, v16

    .line 748
    invoke-direct/range {v0 .. v12}, Ljhg;-><init>(Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;ILcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Lvf0;)V

    .line 751
    move-object v1, v9

    move-object v1, v9

    .line 752
    invoke-virtual {v14, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 755
    goto :goto_31d

    .line 756
    :cond_319
    move-object/from16 v15, v16

    .line 758
    move-object/from16 v12, v25

    .line 760
    :goto_31d
    if-eqz v15, :cond_329

    .line 762
    new-instance v0, Ltkf;

    .line 764
    const/16 v2, 0xc

    .line 766
    invoke-direct {v0, v12, v2}, Ltkf;-><init>(Lvf0;I)V

    .line 769
    invoke-virtual {v15, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 772
    :cond_329
    new-instance v0, Lihg;

    .line 774
    invoke-direct {v0, v1, v13}, Lihg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;I)V

    .line 777
    invoke-virtual {v12, v0}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 780
    invoke-virtual {v12}, Landroid/app/Dialog;->show()V

    .line 783
    return-void

    .line 784
    :pswitch_335
    move-object/from16 v40, v8

    move-object/from16 v40, v8

    .line 786
    const/4 v7, 0x1

    .line 787
    new-instance v8, Lvf0;

    .line 789
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 792
    move-result-object v0

    .line 793
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 796
    move-result v10

    .line 797
    invoke-direct {v8, v0, v10}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 800
    const v0, 0x7f0d02c6

    .line 803
    const v10, 0x7f1418a1

    .line 806
    const/4 v11, 0x0

    .line 807
    invoke-static {v8, v0, v10, v8, v11}, Liu1;->x(Lvf0;IILvf0;I)V

    .line 810
    invoke-static {v8}, Lxje;->l(Lvf0;)V

    .line 813
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 815
    instance-of v10, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;

    .line 817
    if-eqz v10, :cond_35d

    .line 819
    check-cast v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;

    .line 821
    goto :goto_35e

    .line 822
    :cond_35d
    const/4 v0, 0x0

    .line 823
    :goto_35e
    invoke-virtual {v8, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 826
    move-result-object v9

    .line 827
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 830
    check-cast v9, Landroid/widget/Button;

    .line 832
    invoke-virtual {v8, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 835
    move-result-object v5

    .line 836
    move-object v10, v5

    .line 837
    check-cast v10, Landroid/widget/Button;

    .line 839
    invoke-virtual {v8, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 842
    move-result-object v4

    .line 843
    check-cast v4, Landroid/widget/Button;

    .line 845
    invoke-virtual {v8, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 848
    move-result-object v5

    .line 849
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 852
    check-cast v5, Landroid/widget/EditText;

    .line 854
    invoke-virtual {v8, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 857
    move-result-object v12

    .line 858
    invoke-virtual {v12}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 861
    check-cast v12, Landroid/widget/EditText;

    .line 863
    invoke-virtual {v8, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 866
    move-result-object v6

    .line 867
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 870
    check-cast v6, Landroid/widget/EditText;

    .line 872
    invoke-virtual {v8, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 875
    move-result-object v13

    .line 876
    invoke-virtual {v13}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 879
    check-cast v13, Landroid/widget/EditText;

    .line 881
    invoke-virtual {v8, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 884
    move-result-object v14

    .line 885
    check-cast v14, Landroid/widget/TextView;

    .line 887
    const v15, 0x7f0a0589

    .line 890
    invoke-virtual {v8, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 893
    move-result-object v15

    .line 894
    check-cast v15, Landroid/widget/EditText;

    .line 896
    const v11, 0x7f0a1296

    .line 899
    invoke-virtual {v8, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 902
    move-result-object v11

    .line 903
    check-cast v11, Landroid/widget/CheckBox;

    .line 905
    const v7, 0x7f0a0c08

    .line 908
    invoke-virtual {v8, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 911
    move-result-object v7

    .line 912
    check-cast v7, Landroid/widget/TextView;

    .line 914
    move-object/from16 v16, v0

    .line 916
    const v0, 0x7f0a12ff

    .line 919
    invoke-virtual {v8, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 922
    move-result-object v0

    .line 923
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 926
    check-cast v0, Landroid/widget/EditText;

    .line 928
    move-object/from16 v17, v4

    .line 930
    const v4, 0x7f0a0dde

    .line 933
    invoke-virtual {v8, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 936
    move-result-object v4

    .line 937
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 940
    check-cast v4, Landroid/widget/RadioButton;

    .line 942
    move-object/from16 v18, v10

    .line 944
    const v10, 0x7f0a0ddf

    .line 947
    invoke-virtual {v8, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 950
    move-result-object v10

    .line 951
    invoke-virtual {v10}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 954
    check-cast v10, Landroid/widget/RadioButton;

    .line 956
    move-object/from16 v19, v14

    .line 958
    const v14, 0x7f0a0dd6

    .line 961
    invoke-virtual {v8, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 964
    move-result-object v14

    .line 965
    invoke-virtual {v14}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 968
    check-cast v14, Landroid/widget/RadioButton;

    .line 970
    move-object/from16 v41, v2

    .line 972
    const v2, 0x7f0a0dd5

    .line 975
    invoke-virtual {v8, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 978
    move-result-object v2

    .line 979
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 982
    check-cast v2, Landroid/widget/RadioButton;

    .line 984
    move-object/from16 v42, v3

    .line 986
    const v3, 0x7f0a0d6e

    .line 989
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 992
    move-result-object v3

    .line 993
    check-cast v3, Landroid/widget/Button;

    .line 995
    move-object/from16 v20, v3

    move-object/from16 v20, v3

    .line 997
    const v3, 0x7f0a0d6f

    .line 1000
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1003
    move-result-object v3

    .line 1004
    check-cast v3, Landroid/widget/Button;

    .line 1006
    move-object/from16 v23, v3

    .line 1008
    const v3, 0x7f0a0d72

    .line 1011
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1014
    move-result-object v3

    .line 1015
    check-cast v3, Landroid/widget/Button;

    .line 1017
    move-object/from16 v24, v3

    .line 1019
    const v3, 0x7f0a0d73

    .line 1022
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1025
    move-result-object v3

    .line 1026
    check-cast v3, Landroid/widget/Button;

    .line 1028
    move-object/from16 v27, v3

    .line 1030
    const v3, 0x7f0a1300

    .line 1033
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1036
    move-result-object v3

    .line 1037
    check-cast v3, Landroid/widget/Button;

    .line 1039
    move-object/from16 v28, v3

    move-object/from16 v28, v3

    .line 1041
    const v3, 0x7f0a0c09

    .line 1044
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1047
    move-result-object v3

    .line 1048
    check-cast v3, Landroid/widget/Button;

    .line 1050
    move-object/from16 v26, v3

    .line 1052
    const v3, 0x7f0a0f95

    .line 1055
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1058
    move-result-object v3

    .line 1059
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1062
    check-cast v3, Landroid/widget/CheckBox;

    .line 1064
    if-eqz v16, :cond_464

    .line 1066
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getShowTouchLocation()Z

    .line 1069
    move-result v25

    .line 1070
    move/from16 v54, v25

    move/from16 v54, v25

    .line 1072
    move-object/from16 v25, v8

    .line 1074
    move/from16 v8, v54

    move/from16 v8, v54

    .line 1076
    goto :goto_469

    .line 1077
    :cond_464
    move-object/from16 v25, v8

    move-object/from16 v25, v8

    .line 1079
    const/4 v8, 0x0

    .line 1080
    :goto_469
    invoke-virtual {v3, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1083
    if-nez v16, :cond_473

    .line 1085
    const/4 v8, 0x1

    .line 1086
    invoke-virtual {v14, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1089
    goto :goto_486

    .line 1090
    :cond_473
    const/4 v8, 0x1

    .line 1091
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getXyPercentages()Z

    .line 1094
    move-result v29

    .line 1095
    move/from16 v37, v8

    .line 1097
    xor-int/lit8 v8, v29, 0x1

    .line 1099
    invoke-virtual {v14, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1102
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getXyPercentages()Z

    .line 1105
    move-result v8

    .line 1106
    invoke-virtual {v2, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1109
    :goto_486
    if-eqz v16, :cond_48d

    .line 1111
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomIn()Z

    .line 1114
    move-result v8

    .line 1115
    goto :goto_48e

    .line 1116
    :cond_48d
    const/4 v8, 0x1

    .line 1117
    :goto_48e
    invoke-virtual {v4, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1120
    if-eqz v16, :cond_49b

    .line 1122
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomIn()Z

    .line 1125
    move-result v8

    .line 1126
    if-nez v8, :cond_49b

    .line 1128
    const/4 v8, 0x1

    .line 1129
    goto :goto_49c

    .line 1130
    :cond_49b
    const/4 v8, 0x0

    .line 1131
    :goto_49c
    invoke-virtual {v10, v8}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1134
    new-instance v8, Ldig;

    .line 1136
    const/4 v10, 0x0

    .line 1137
    invoke-direct {v8, v1, v10}, Ldig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Lm73;)V

    .line 1140
    invoke-static {v9, v8}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 1143
    if-eqz v7, :cond_4bd

    .line 1145
    invoke-static/range {v22 .. v22}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 1148
    move-result-object v8

    .line 1149
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1152
    sget-object v9, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    .line 1154
    invoke-virtual {v8, v9}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    .line 1157
    move-result-object v8

    .line 1158
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1161
    invoke-virtual {v7, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1164
    :cond_4bd
    if-eqz v11, :cond_4ca

    .line 1166
    if-eqz v16, :cond_4c6

    .line 1168
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getWaitBeforeNext()Z

    .line 1171
    move-result v7

    .line 1172
    goto :goto_4c7

    .line 1173
    :cond_4c6
    const/4 v7, 0x1

    .line 1174
    :goto_4c7
    invoke-virtual {v11, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1177
    :cond_4ca
    if-eqz v16, :cond_4d1

    .line 1179
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1XVarName()Ljava/lang/String;

    .line 1182
    move-result-object v7

    .line 1183
    goto :goto_4d2

    .line 1184
    :cond_4d1
    const/4 v7, 0x0

    .line 1185
    :goto_4d2
    if-eqz v7, :cond_4dc

    .line 1187
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1XVarName()Ljava/lang/String;

    .line 1190
    move-result-object v7

    .line 1191
    invoke-virtual {v5, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1194
    goto :goto_4ed

    .line 1195
    :cond_4dc
    if-eqz v16, :cond_4e8

    .line 1197
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1X()I

    .line 1200
    move-result v7

    .line 1201
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1204
    move-result-object v7

    .line 1205
    if-nez v7, :cond_4ea

    .line 1207
    :cond_4e8
    move-object/from16 v7, v34

    .line 1209
    :cond_4ea
    invoke-virtual {v5, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1212
    :goto_4ed
    if-eqz v16, :cond_4f4

    .line 1214
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1YVarName()Ljava/lang/String;

    .line 1217
    move-result-object v7

    .line 1218
    goto :goto_4f5

    .line 1219
    :cond_4f4
    const/4 v7, 0x0

    .line 1220
    :goto_4f5
    if-eqz v7, :cond_4ff

    .line 1222
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1YVarName()Ljava/lang/String;

    .line 1225
    move-result-object v7

    .line 1226
    invoke-virtual {v12, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1229
    goto :goto_510

    .line 1230
    :cond_4ff
    if-eqz v16, :cond_50b

    .line 1232
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint1Y()I

    .line 1235
    move-result v7

    .line 1236
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1239
    move-result-object v7

    .line 1240
    if-nez v7, :cond_50d

    .line 1242
    :cond_50b
    move-object/from16 v7, v34

    .line 1244
    :cond_50d
    invoke-virtual {v12, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1247
    :goto_510
    if-eqz v16, :cond_517

    .line 1249
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2XVarName()Ljava/lang/String;

    .line 1252
    move-result-object v7

    .line 1253
    goto :goto_518

    .line 1254
    :cond_517
    const/4 v7, 0x0

    .line 1255
    :goto_518
    if-eqz v7, :cond_522

    .line 1257
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2XVarName()Ljava/lang/String;

    .line 1260
    move-result-object v7

    .line 1261
    invoke-virtual {v6, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1264
    goto :goto_533

    .line 1265
    :cond_522
    if-eqz v16, :cond_52e

    .line 1267
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2X()I

    .line 1270
    move-result v7

    .line 1271
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1274
    move-result-object v7

    .line 1275
    if-nez v7, :cond_530

    .line 1277
    :cond_52e
    move-object/from16 v7, v34

    .line 1279
    :cond_530
    invoke-virtual {v6, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1282
    :goto_533
    if-eqz v16, :cond_53a

    .line 1284
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2YVarName()Ljava/lang/String;

    .line 1287
    move-result-object v7

    .line 1288
    goto :goto_53b

    .line 1289
    :cond_53a
    const/4 v7, 0x0

    .line 1290
    :goto_53b
    if-eqz v7, :cond_545

    .line 1292
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2YVarName()Ljava/lang/String;

    .line 1295
    move-result-object v7

    .line 1296
    invoke-virtual {v13, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1299
    goto :goto_556

    .line 1300
    :cond_545
    if-eqz v16, :cond_551

    .line 1302
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getPoint2Y()I

    .line 1305
    move-result v7

    .line 1306
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1309
    move-result-object v7

    .line 1310
    if-nez v7, :cond_553

    .line 1312
    :cond_551
    move-object/from16 v7, v34

    .line 1314
    :cond_553
    invoke-virtual {v13, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1317
    :goto_556
    if-eqz v16, :cond_55d

    .line 1319
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomPercentVarName()Ljava/lang/String;

    .line 1322
    move-result-object v7

    .line 1323
    goto :goto_55e

    .line 1324
    :cond_55d
    const/4 v7, 0x0

    .line 1325
    :goto_55e
    if-eqz v7, :cond_568

    .line 1327
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomPercentVarName()Ljava/lang/String;

    .line 1330
    move-result-object v7

    .line 1331
    invoke-virtual {v0, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1334
    goto :goto_579

    .line 1335
    :cond_568
    if-eqz v16, :cond_574

    .line 1337
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getZoomPercent()I

    .line 1340
    move-result v7

    .line 1341
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1344
    move-result-object v7

    .line 1345
    if-nez v7, :cond_576

    .line 1347
    :cond_574
    const-string v7, "50"

    .line 1349
    :cond_576
    invoke-virtual {v0, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1352
    :goto_579
    if-eqz v16, :cond_580

    .line 1354
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getDurationVarName()Ljava/lang/String;

    .line 1357
    move-result-object v10

    .line 1358
    goto :goto_581

    .line 1359
    :cond_580
    const/4 v10, 0x0

    .line 1360
    :goto_581
    if-eqz v10, :cond_58e

    .line 1362
    if-eqz v15, :cond_58c

    .line 1364
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getDurationVarName()Ljava/lang/String;

    .line 1367
    move-result-object v7

    .line 1368
    invoke-virtual {v15, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1371
    :cond_58c
    :goto_58c
    move-object v7, v3

    .line 1372
    goto :goto_5a6

    .line 1373
    :cond_58e
    if-eqz v15, :cond_58c

    .line 1375
    if-eqz v16, :cond_5a0

    .line 1377
    invoke-virtual/range {v16 .. v16}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PinchZoom;->getDurationMs()I

    .line 1380
    move-result v7

    .line 1381
    invoke-static {v7}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1384
    move-result-object v7

    .line 1385
    if-nez v7, :cond_59d

    .line 1387
    goto :goto_5a0

    .line 1388
    :cond_59d
    move-object v8, v7

    move-object v8, v7

    .line 1389
    goto :goto_5a2

    .line 1390
    :cond_5a0
    :goto_5a0
    move-object/from16 v8, v40

    .line 1392
    :goto_5a2
    invoke-virtual {v15, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1395
    goto :goto_58c

    .line 1396
    :goto_5a6
    new-instance v3, Landroid/graphics/Point;

    .line 1398
    invoke-direct {v3}, Landroid/graphics/Point;-><init>()V

    .line 1401
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 1404
    move-result-object v8

    .line 1405
    invoke-virtual {v8}, Landroid/app/Activity;->getWindowManager()Landroid/view/WindowManager;

    .line 1408
    move-result-object v8

    .line 1409
    invoke-interface {v8}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 1412
    move-result-object v8

    .line 1413
    invoke-virtual {v8, v3}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 1416
    if-eqz v19, :cond_5e5

    .line 1418
    invoke-static/range {v21 .. v21}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 1421
    move-result-object v8

    .line 1422
    iget v9, v3, Landroid/graphics/Point;->x:I

    .line 1424
    iget v10, v3, Landroid/graphics/Point;->y:I

    .line 1426
    new-instance v14, Ljava/lang/StringBuilder;

    .line 1428
    invoke-direct {v14}, Ljava/lang/StringBuilder;-><init>()V

    .line 1431
    invoke-virtual {v14, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1434
    move-object/from16 v8, v42

    .line 1436
    invoke-virtual {v14, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1439
    invoke-virtual {v14, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 1442
    move-object/from16 v8, v41

    .line 1444
    invoke-virtual {v14, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1447
    invoke-virtual {v14, v10}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 1450
    invoke-virtual {v14}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1453
    move-result-object v8

    .line 1454
    move-object/from16 v14, v19

    .line 1456
    invoke-virtual {v14, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1459
    :cond_5e5
    iget v8, v3, Landroid/graphics/Point;->x:I

    .line 1461
    iget v9, v3, Landroid/graphics/Point;->y:I

    .line 1463
    invoke-static {v8, v9}, Ljava/lang/Math;->max(II)I

    .line 1466
    move-result v8

    .line 1467
    move-object v9, v0

    move-object v9, v0

    .line 1468
    new-instance v0, Leig;

    .line 1470
    move-object v10, v7

    .line 1471
    const/4 v7, 0x0

    .line 1472
    move-object v14, v12

    move-object v14, v12

    .line 1473
    move-object v12, v2

    move-object v12, v2

    .line 1474
    move-object v2, v5

    move-object v2, v5

    .line 1475
    move-object v5, v6

    .line 1476
    move-object v6, v13

    .line 1477
    move-object/from16 v13, v20

    move-object/from16 v13, v20

    .line 1479
    move-object/from16 v20, v17

    .line 1481
    move-object/from16 v17, v4

    .line 1483
    move-object v4, v14

    .line 1484
    move/from16 v16, v8

    .line 1486
    move-object/from16 v21, v10

    move-object/from16 v21, v10

    .line 1488
    move-object/from16 v19, v11

    .line 1490
    move-object/from16 v8, v23

    .line 1492
    move-object/from16 v10, v24

    .line 1494
    move-object/from16 v43, v26

    .line 1496
    move-object/from16 v11, v27

    move-object/from16 v11, v27

    .line 1498
    move-object/from16 v14, v28

    .line 1500
    invoke-direct/range {v0 .. v7}, Leig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/graphics/Point;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Lm73;)V

    .line 1503
    move-object v3, v5

    .line 1504
    invoke-static {v12, v0}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 1507
    invoke-static {v1, v2, v13}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1510
    invoke-static {v1, v4, v8}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1513
    invoke-static {v1, v3, v10}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1516
    invoke-static {v1, v6, v11}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1519
    invoke-static {v1, v9, v14}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1522
    if-eqz v15, :cond_635

    .line 1524
    move-object/from16 v0, v43

    .line 1526
    invoke-static {v1, v15, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->m0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 1529
    :cond_635
    if-eqz v18, :cond_659

    .line 1531
    new-instance v0, Lnhg;

    .line 1533
    move-object v5, v9

    .line 1534
    move-object v7, v12

    .line 1535
    move/from16 v8, v16

    .line 1537
    move-object/from16 v10, v17

    .line 1539
    move-object/from16 v14, v18

    move-object/from16 v14, v18

    .line 1541
    move-object/from16 v11, v19

    .line 1543
    move-object/from16 v12, v21

    move-object/from16 v12, v21

    .line 1545
    move-object/from16 v13, v25

    .line 1547
    move-object v9, v1

    .line 1548
    move-object v1, v2

    .line 1549
    move-object v2, v4

    .line 1550
    move-object v4, v6

    .line 1551
    move-object v6, v15

    .line 1552
    const/4 v15, 0x0

    .line 1553
    invoke-direct/range {v0 .. v13}, Lnhg;-><init>(Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;ILcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Lvf0;)V

    .line 1556
    move-object v1, v9

    .line 1557
    invoke-virtual {v14, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1560
    goto :goto_65c

    .line 1561
    :cond_659
    move-object/from16 v13, v25

    .line 1563
    const/4 v15, 0x0

    .line 1564
    :goto_65c
    if-eqz v20, :cond_66a

    .line 1566
    new-instance v0, Ltkf;

    .line 1568
    const/16 v2, 0x12

    .line 1570
    invoke-direct {v0, v13, v2}, Ltkf;-><init>(Lvf0;I)V

    .line 1573
    move-object/from16 v4, v20

    .line 1575
    invoke-virtual {v4, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1578
    :cond_66a
    new-instance v0, Lihg;

    .line 1580
    invoke-direct {v0, v1, v15}, Lihg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;I)V

    .line 1583
    invoke-virtual {v13, v0}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 1586
    invoke-virtual {v13}, Landroid/app/Dialog;->show()V

    .line 1589
    return-void

    .line 1590
    :pswitch_676
    sget-object v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PressEnter;->INSTANCE:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$PressEnter;

    .line 1592
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 1594
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->itemComplete()V

    .line 1597
    return-void

    .line 1598
    :pswitch_67e
    move-object v0, v2

    .line 1599
    move-object v8, v3

    move-object v8, v3

    .line 1600
    move v15, v10

    .line 1601
    new-instance v2, Lvf0;

    .line 1603
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 1606
    move-result-object v3

    .line 1607
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 1610
    move-result v6

    .line 1611
    invoke-direct {v2, v3, v6}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 1614
    const v3, 0x7f0d02c4

    .line 1617
    const v6, 0x7f14189f

    .line 1620
    invoke-static {v2, v3, v6, v2, v15}, Liu1;->x(Lvf0;IILvf0;I)V

    .line 1623
    invoke-static {v2}, Lxje;->l(Lvf0;)V

    .line 1626
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 1628
    instance-of v6, v3, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;

    .line 1630
    if-eqz v6, :cond_6a5

    .line 1632
    check-cast v3, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;

    .line 1634
    move-object v6, v3

    .line 1635
    goto :goto_6a6

    .line 1636
    :cond_6a5
    const/4 v6, 0x0

    .line 1637
    :goto_6a6
    const v3, 0x7f0a1148

    .line 1640
    invoke-virtual {v2, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1643
    move-result-object v3

    .line 1644
    check-cast v3, Landroid/view/ViewGroup;

    .line 1646
    invoke-virtual {v2, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1649
    move-result-object v7

    .line 1650
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1653
    check-cast v7, Landroid/widget/Button;

    .line 1655
    invoke-virtual {v2, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1658
    move-result-object v5

    .line 1659
    move-object v12, v5

    .line 1660
    check-cast v12, Landroid/widget/Button;

    .line 1662
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1665
    move-result-object v4

    .line 1666
    move-object v13, v4

    move-object v13, v4

    .line 1667
    check-cast v13, Landroid/widget/Button;

    .line 1669
    const v4, 0x7f0a1021

    .line 1672
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1675
    move-result-object v4

    .line 1676
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1679
    move-object v9, v4

    .line 1680
    check-cast v9, Landroid/widget/EditText;

    .line 1682
    const v4, 0x7f0a1023

    .line 1685
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1688
    move-result-object v4

    .line 1689
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1692
    move-object v10, v4

    .line 1693
    check-cast v10, Landroid/widget/EditText;

    .line 1695
    const v4, 0x7f0a0589

    .line 1698
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1701
    move-result-object v4

    .line 1702
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1705
    move-object v11, v4

    .line 1706
    check-cast v11, Landroid/widget/EditText;

    .line 1708
    const v4, 0x7f0a0c09

    .line 1711
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1714
    move-result-object v4

    .line 1715
    check-cast v4, Landroid/widget/Button;

    .line 1717
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1720
    move-result-object v5

    .line 1721
    check-cast v5, Landroid/widget/TextView;

    .line 1723
    const v14, 0x7f0a1296

    .line 1726
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1729
    move-result-object v14

    .line 1730
    check-cast v14, Landroid/widget/CheckBox;

    .line 1732
    const v15, 0x7f0a0c08

    .line 1735
    invoke-virtual {v2, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1738
    move-result-object v15

    .line 1739
    check-cast v15, Landroid/widget/TextView;

    .line 1741
    move-object/from16 v17, v3

    .line 1743
    const v3, 0x7f0a1016

    .line 1746
    invoke-virtual {v2, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1749
    move-result-object v3

    .line 1750
    check-cast v3, Landroid/widget/Button;

    .line 1752
    move-object/from16 v20, v4

    .line 1754
    const v4, 0x7f0a1019

    .line 1757
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1760
    move-result-object v4

    .line 1761
    check-cast v4, Landroid/widget/Button;

    .line 1763
    move-object/from16 v19, v6

    .line 1765
    const v6, 0x7f0a060e

    .line 1768
    invoke-virtual {v2, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1771
    move-result-object v6

    .line 1772
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1775
    check-cast v6, Landroid/widget/LinearLayout;

    .line 1777
    move-object/from16 v23, v13

    .line 1779
    const v13, 0x7f0a0090

    .line 1782
    invoke-virtual {v2, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1785
    move-result-object v13

    .line 1786
    check-cast v13, Landroid/widget/Button;

    .line 1788
    move-object/from16 v24, v12

    .line 1790
    const v12, 0x7f0a0e46

    .line 1793
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1796
    move-result-object v12

    .line 1797
    check-cast v12, Landroid/widget/Button;

    .line 1799
    move-object/from16 v26, v11

    .line 1801
    const v11, 0x7f0a0dd6

    .line 1804
    invoke-virtual {v2, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1807
    move-result-object v11

    .line 1808
    invoke-virtual {v11}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1811
    check-cast v11, Landroid/widget/RadioButton;

    .line 1813
    move-object/from16 v27, v13

    .line 1815
    const v13, 0x7f0a0dd5

    .line 1818
    invoke-virtual {v2, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1821
    move-result-object v13

    .line 1822
    invoke-virtual {v13}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1825
    check-cast v13, Landroid/widget/RadioButton;

    .line 1827
    invoke-virtual/range {v17 .. v17}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1830
    move-object/from16 v28, v6

    .line 1832
    invoke-virtual/range {v17 .. v17}, Landroid/view/ViewGroup;->getLayoutTransition()Landroid/animation/LayoutTransition;

    .line 1835
    move-result-object v6

    .line 1836
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1839
    move-object/from16 v17, v12

    move-object/from16 v17, v12

    .line 1841
    const/4 v12, 0x4

    .line 1842
    invoke-virtual {v6, v12}, Landroid/animation/LayoutTransition;->enableTransitionType(I)V

    .line 1845
    if-eqz v15, :cond_78e

    .line 1847
    invoke-static/range {v22 .. v22}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 1850
    move-result-object v6

    .line 1851
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1854
    sget-object v12, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    .line 1856
    invoke-virtual {v6, v12}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    .line 1859
    move-result-object v6

    .line 1860
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1863
    invoke-virtual {v15, v6}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1866
    :cond_78e
    if-eqz v14, :cond_79b

    .line 1868
    if-eqz v19, :cond_797

    .line 1870
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getWaitBeforeNext()Z

    .line 1873
    move-result v6

    .line 1874
    goto :goto_798

    .line 1875
    :cond_797
    const/4 v6, 0x1

    .line 1876
    :goto_798
    invoke-virtual {v14, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1879
    :cond_79b
    const v6, 0x7f0a0f95

    .line 1882
    invoke-virtual {v2, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 1885
    move-result-object v6

    .line 1886
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1889
    move-object v12, v6

    move-object v12, v6

    .line 1890
    check-cast v12, Landroid/widget/CheckBox;

    .line 1892
    if-eqz v19, :cond_7b0

    .line 1894
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getShowTouchLocation()Z

    .line 1897
    move-result v6

    .line 1898
    goto :goto_7b1

    .line 1899
    :cond_7b0
    const/4 v6, 0x0

    .line 1900
    :goto_7b1
    invoke-virtual {v12, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1903
    if-nez v19, :cond_7bb

    .line 1905
    const/4 v6, 0x1

    .line 1906
    invoke-virtual {v11, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1909
    goto :goto_7cb

    .line 1910
    :cond_7bb
    const/4 v6, 0x1

    .line 1911
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1914
    move-result v15

    .line 1915
    xor-int/2addr v15, v6

    .line 1916
    invoke-virtual {v11, v15}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1919
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXyPercentages()Z

    .line 1922
    move-result v6

    .line 1923
    invoke-virtual {v13, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1926
    :goto_7cb
    new-instance v6, Lwhg;

    .line 1928
    const/4 v11, 0x0

    .line 1929
    invoke-direct {v6, v1, v11}, Lwhg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Lm73;)V

    .line 1932
    invoke-static {v7, v6}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 1935
    if-eqz v19, :cond_7db

    .line 1937
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXStartVarName()Ljava/lang/String;

    .line 1940
    move-result-object v6

    .line 1941
    goto :goto_7dc

    .line 1942
    :cond_7db
    const/4 v6, 0x0

    .line 1943
    :goto_7dc
    if-eqz v6, :cond_7e6

    .line 1945
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getXStartVarName()Ljava/lang/String;

    .line 1948
    move-result-object v6

    .line 1949
    invoke-virtual {v9, v6}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1952
    goto :goto_7f7

    .line 1953
    :cond_7e6
    if-eqz v19, :cond_7f2

    .line 1955
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getStartX()I

    .line 1958
    move-result v6

    .line 1959
    invoke-static {v6}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1962
    move-result-object v6

    .line 1963
    if-nez v6, :cond_7f4

    .line 1965
    :cond_7f2
    move-object/from16 v6, v34

    .line 1967
    :cond_7f4
    invoke-virtual {v9, v6}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1970
    :goto_7f7
    if-eqz v19, :cond_7fe

    .line 1972
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getYStartVarName()Ljava/lang/String;

    .line 1975
    move-result-object v6

    .line 1976
    goto :goto_7ff

    .line 1977
    :cond_7fe
    const/4 v6, 0x0

    .line 1978
    :goto_7ff
    if-eqz v6, :cond_809

    .line 1980
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getYStartVarName()Ljava/lang/String;

    .line 1983
    move-result-object v6

    .line 1984
    invoke-virtual {v10, v6}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1987
    goto :goto_81a

    .line 1988
    :cond_809
    if-eqz v19, :cond_815

    .line 1990
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getStartY()I

    .line 1993
    move-result v6

    .line 1994
    invoke-static {v6}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1997
    move-result-object v6

    .line 1998
    if-nez v6, :cond_817

    .line 2000
    :cond_815
    move-object/from16 v6, v34

    .line 2002
    :cond_817
    invoke-virtual {v10, v6}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2005
    :goto_81a
    new-instance v6, Landroid/graphics/Point;

    .line 2007
    invoke-direct {v6}, Landroid/graphics/Point;-><init>()V

    .line 2010
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 2013
    move-result-object v7

    .line 2014
    invoke-virtual {v7}, Landroid/app/Activity;->getWindowManager()Landroid/view/WindowManager;

    .line 2017
    move-result-object v7

    .line 2018
    invoke-interface {v7}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 2021
    move-result-object v7

    .line 2022
    invoke-virtual {v7, v6}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 2025
    if-eqz v5, :cond_856

    .line 2027
    invoke-static/range {v21 .. v21}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 2030
    move-result-object v7

    .line 2031
    iget v11, v6, Landroid/graphics/Point;->x:I

    .line 2033
    iget v15, v6, Landroid/graphics/Point;->y:I

    .line 2035
    move-object/from16 v25, v2

    .line 2037
    new-instance v2, Ljava/lang/StringBuilder;

    .line 2039
    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    .line 2042
    invoke-virtual {v2, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 2045
    invoke-virtual {v2, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 2048
    invoke-virtual {v2, v11}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 2051
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 2054
    invoke-virtual {v2, v15}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 2057
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 2060
    move-result-object v0

    .line 2061
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2064
    goto :goto_858

    .line 2065
    :cond_856
    move-object/from16 v25, v2

    .line 2067
    :goto_858
    iget v0, v6, Landroid/graphics/Point;->x:I

    .line 2069
    iget v2, v6, Landroid/graphics/Point;->y:I

    .line 2071
    invoke-static {v0, v2}, Ljava/lang/Math;->max(II)I

    .line 2074
    move-result v7

    .line 2075
    new-instance v0, Lkhg;

    .line 2077
    const/4 v8, 0x1

    .line 2078
    invoke-direct {v0, v9, v8}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 2081
    if-eqz v3, :cond_872

    .line 2083
    new-instance v2, Lxhg;

    .line 2085
    const/4 v8, 0x0

    .line 2086
    invoke-direct {v2, v1, v0, v8}, Lxhg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Ltr9;Lm73;)V

    .line 2089
    invoke-static {v3, v2}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2092
    goto :goto_873

    .line 2093
    :cond_872
    const/4 v8, 0x0

    .line 2094
    :goto_873
    new-instance v0, Lkhg;

    .line 2096
    const/4 v2, 0x2

    .line 2097
    invoke-direct {v0, v10, v2}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 2100
    if-eqz v4, :cond_883

    .line 2102
    new-instance v2, Lyhg;

    .line 2104
    invoke-direct {v2, v1, v0, v8}, Lyhg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Ltr9;Lm73;)V

    .line 2107
    invoke-static {v4, v2}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2110
    :cond_883
    if-eqz v17, :cond_894

    .line 2112
    new-instance v0, Lzhg;

    .line 2114
    move-object/from16 v4, v17

    .line 2116
    move-object/from16 v3, v28

    move-object/from16 v3, v28

    .line 2118
    invoke-direct {v0, v3, v4, v8}, Lzhg;-><init>(Landroid/widget/LinearLayout;Landroid/widget/Button;Lm73;)V

    .line 2121
    invoke-static {v4, v0}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2124
    goto :goto_898

    .line 2125
    :cond_894
    move-object/from16 v4, v17

    .line 2127
    move-object/from16 v3, v28

    .line 2129
    :goto_898
    if-eqz v27, :cond_8ab

    .line 2131
    new-instance v0, Lcom/arlosoft/macrodroid/action/z;

    .line 2133
    const/4 v5, 0x0

    .line 2134
    move-object/from16 v8, v20

    .line 2136
    move-object/from16 v2, v25

    .line 2138
    invoke-direct/range {v0 .. v5}, Lcom/arlosoft/macrodroid/action/z;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Lvf0;Landroid/widget/LinearLayout;Landroid/widget/Button;Lm73;)V

    .line 2141
    move-object v2, v0

    .line 2142
    move-object/from16 v0, v27

    .line 2144
    invoke-static {v0, v2}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2147
    goto :goto_8af

    .line 2148
    :cond_8ab
    move-object/from16 v8, v20

    move-object/from16 v8, v20

    .line 2150
    :goto_8af
    if-eqz v19, :cond_8d2

    .line 2152
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getGestures()Ljava/util/List;

    .line 2155
    move-result-object v0

    .line 2156
    if-eqz v0, :cond_8d2

    .line 2158
    invoke-interface {v0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 2161
    move-result-object v0

    .line 2162
    :goto_8bb
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 2165
    move-result v2

    .line 2166
    if-eqz v2, :cond_8d2

    .line 2168
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 2171
    move-result-object v2

    .line 2172
    check-cast v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureEntry;

    .line 2174
    invoke-virtual/range {v25 .. v25}, Landroid/app/Dialog;->getLayoutInflater()Landroid/view/LayoutInflater;

    .line 2177
    move-result-object v5

    .line 2178
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2181
    invoke-virtual {v1, v5, v3, v2}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->U(Landroid/view/LayoutInflater;Landroid/widget/LinearLayout;Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureEntry;)V

    .line 2184
    goto :goto_8bb

    .line 2185
    :cond_8d2
    if-eqz v19, :cond_8d9

    .line 2187
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getDurationVarName()Ljava/lang/String;

    .line 2190
    move-result-object v0

    .line 2191
    goto :goto_8da

    .line 2192
    :cond_8d9
    const/4 v0, 0x0

    .line 2193
    :goto_8da
    if-eqz v0, :cond_8e6

    .line 2195
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getDurationVarName()Ljava/lang/String;

    .line 2198
    move-result-object v0

    .line 2199
    move-object/from16 v11, v26

    .line 2201
    invoke-virtual {v11, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2204
    goto :goto_8fb

    .line 2205
    :cond_8e6
    move-object/from16 v11, v26

    move-object/from16 v11, v26

    .line 2207
    if-eqz v19, :cond_8f6

    .line 2209
    invoke-virtual/range {v19 .. v19}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$GestureSequence;->getDurationMs()I

    .line 2212
    move-result v0

    .line 2213
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 2216
    move-result-object v0

    .line 2217
    if-nez v0, :cond_8f8

    .line 2219
    :cond_8f6
    move-object/from16 v0, v36

    .line 2221
    :cond_8f8
    invoke-virtual {v11, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2224
    :goto_8fb
    new-instance v0, Lkhg;

    .line 2226
    const/4 v2, 0x3

    .line 2227
    invoke-direct {v0, v11, v2}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 2230
    if-eqz v8, :cond_90c

    .line 2232
    new-instance v2, Laig;

    .line 2234
    const/4 v5, 0x0

    .line 2235
    invoke-direct {v2, v1, v0, v5}, Laig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Ltr9;Lm73;)V

    .line 2238
    invoke-static {v8, v2}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2241
    :cond_90c
    if-eqz v4, :cond_91b

    .line 2243
    invoke-virtual {v3}, Landroid/view/ViewGroup;->getChildCount()I

    .line 2246
    move-result v0

    .line 2247
    if-lez v0, :cond_916

    .line 2249
    const/4 v0, 0x0

    .line 2250
    goto :goto_918

    .line 2251
    :cond_916
    const/16 v0, 0x8

    .line 2253
    :goto_918
    invoke-virtual {v4, v0}, Landroid/view/View;->setVisibility(I)V

    .line 2256
    :cond_91b
    new-instance v0, Lbig;

    .line 2258
    move-object v5, v3

    move-object v5, v3

    .line 2259
    move-object v3, v6

    .line 2260
    const/4 v6, 0x0

    .line 2261
    move-object v2, v9

    .line 2262
    move-object v4, v10

    .line 2263
    invoke-direct/range {v0 .. v6}, Lbig;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/graphics/Point;Landroid/widget/EditText;Landroid/widget/LinearLayout;Lm73;)V

    .line 2266
    move-object v3, v5

    .line 2267
    invoke-static {v13, v0}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 2270
    if-eqz v24, :cond_94c

    .line 2272
    new-instance v0, Lcom/arlosoft/macrodroid/action/a0;

    .line 2274
    move-object v5, v11

    move-object v5, v11

    .line 2275
    const/4 v11, 0x0

    .line 2276
    move-object v1, v3

    .line 2277
    move v6, v7

    .line 2278
    move-object v9, v12

    move-object v9, v12

    .line 2279
    move-object v7, v13

    .line 2280
    move-object v8, v14

    .line 2281
    move-object/from16 v10, v25

    .line 2283
    move-object v3, v2

    .line 2284
    move-object/from16 v2, p0

    move-object/from16 v2, p0

    .line 2286
    invoke-direct/range {v0 .. v11}, Lcom/arlosoft/macrodroid/action/a0;-><init>(Landroid/widget/LinearLayout;Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;ILandroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Lvf0;Lm73;)V

    .line 2289
    move-object v1, v2

    move-object v1, v2

    .line 2290
    move-object v2, v10

    .line 2291
    move-object/from16 v5, v24

    move-object/from16 v5, v24

    .line 2293
    invoke-static {v5, v0}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2296
    goto :goto_950

    .line 2297
    :cond_94c
    move-object/from16 v1, p0

    .line 2299
    move-object/from16 v2, v25

    .line 2301
    :goto_950
    if-eqz v23, :cond_95e

    .line 2303
    new-instance v0, Ltkf;

    .line 2305
    const/16 v3, 0xe

    .line 2307
    invoke-direct {v0, v2, v3}, Ltkf;-><init>(Lvf0;I)V

    .line 2310
    move-object/from16 v4, v23

    .line 2312
    invoke-virtual {v4, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 2315
    :cond_95e
    new-instance v0, Lihg;

    .line 2317
    const/4 v3, 0x2

    .line 2318
    invoke-direct {v0, v1, v3}, Lihg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;I)V

    .line 2321
    invoke-virtual {v2, v0}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 2324
    invoke-virtual {v2}, Landroid/app/Dialog;->show()V

    .line 2327
    return-void

    .line 2328
    :pswitch_96b
    move-object v0, v2

    move-object v0, v2

    .line 2329
    move-object v8, v3

    .line 2330
    new-instance v12, Lvf0;

    .line 2332
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 2335
    move-result-object v2

    .line 2336
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 2339
    move-result v3

    .line 2340
    invoke-direct {v12, v2, v3}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 2343
    const v2, 0x7f0d02c3

    .line 2346
    const v3, 0x7f14189e

    .line 2349
    const/4 v15, 0x0

    .line 2350
    invoke-static {v12, v2, v3, v12, v15}, Liu1;->x(Lvf0;IILvf0;I)V

    .line 2353
    invoke-static {v12}, Lxje;->l(Lvf0;)V

    .line 2356
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 2358
    instance-of v3, v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 2360
    if-eqz v3, :cond_991

    .line 2362
    check-cast v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 2364
    goto :goto_992

    .line 2365
    :cond_991
    const/4 v2, 0x0

    .line 2366
    :goto_992
    invoke-virtual {v12, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2369
    move-result-object v3

    .line 2370
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2373
    check-cast v3, Landroid/widget/Button;

    .line 2375
    invoke-virtual {v12, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2378
    move-result-object v5

    .line 2379
    move-object v13, v5

    move-object v13, v5

    .line 2380
    check-cast v13, Landroid/widget/Button;

    .line 2382
    invoke-virtual {v12, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2385
    move-result-object v4

    .line 2386
    move-object v15, v4

    .line 2387
    check-cast v15, Landroid/widget/Button;

    .line 2389
    const v4, 0x7f0a1021

    .line 2392
    invoke-virtual {v12, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2395
    move-result-object v4

    .line 2396
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2399
    check-cast v4, Landroid/widget/EditText;

    .line 2401
    const v5, 0x7f0a1023

    .line 2404
    invoke-virtual {v12, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2407
    move-result-object v5

    .line 2408
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2411
    check-cast v5, Landroid/widget/EditText;

    .line 2413
    const v6, 0x7f0a05f1

    .line 2416
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2419
    move-result-object v6

    .line 2420
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2423
    check-cast v6, Landroid/widget/EditText;

    .line 2425
    const v7, 0x7f0a05f3

    .line 2428
    invoke-virtual {v12, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2431
    move-result-object v7

    .line 2432
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2435
    check-cast v7, Landroid/widget/EditText;

    .line 2437
    invoke-virtual {v12, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2440
    move-result-object v9

    .line 2441
    check-cast v9, Landroid/widget/TextView;

    .line 2443
    const v10, 0x7f0a0589

    .line 2446
    invoke-virtual {v12, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2449
    move-result-object v10

    .line 2450
    move-object v14, v10

    .line 2451
    check-cast v14, Landroid/widget/EditText;

    .line 2453
    const v10, 0x7f0a1296

    .line 2456
    invoke-virtual {v12, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2459
    move-result-object v10

    .line 2460
    check-cast v10, Landroid/widget/CheckBox;

    .line 2462
    const v11, 0x7f0a0c08

    .line 2465
    invoke-virtual {v12, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2468
    move-result-object v11

    .line 2469
    check-cast v11, Landroid/widget/TextView;

    .line 2471
    move-object/from16 v23, v2

    .line 2473
    const v2, 0x7f0a1016

    .line 2476
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2479
    move-result-object v2

    .line 2480
    check-cast v2, Landroid/widget/Button;

    .line 2482
    move-object/from16 v20, v2

    .line 2484
    const v2, 0x7f0a1019

    .line 2487
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2490
    move-result-object v2

    .line 2491
    check-cast v2, Landroid/widget/Button;

    .line 2493
    move-object/from16 v19, v2

    .line 2495
    const v2, 0x7f0a05eb

    .line 2498
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2501
    move-result-object v2

    .line 2502
    check-cast v2, Landroid/widget/Button;

    .line 2504
    move-object/from16 v24, v2

    .line 2506
    const v2, 0x7f0a05ed

    .line 2509
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2512
    move-result-object v2

    .line 2513
    check-cast v2, Landroid/widget/Button;

    .line 2515
    move-object/from16 v27, v2

    .line 2517
    const v2, 0x7f0a0c09

    .line 2520
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2523
    move-result-object v2

    .line 2524
    check-cast v2, Landroid/widget/Button;

    .line 2526
    move-object/from16 v26, v2

    .line 2528
    const v2, 0x7f0a0dd6

    .line 2531
    invoke-virtual {v12, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2534
    move-result-object v2

    .line 2535
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2538
    check-cast v2, Landroid/widget/RadioButton;

    .line 2540
    move-object/from16 v28, v13

    move-object/from16 v28, v13

    .line 2542
    const v13, 0x7f0a0dd5

    .line 2545
    invoke-virtual {v12, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2548
    move-result-object v13

    .line 2549
    invoke-virtual {v13}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2552
    check-cast v13, Landroid/widget/RadioButton;

    .line 2554
    move-object/from16 v29, v15

    move-object/from16 v29, v15

    .line 2556
    const v15, 0x7f0a0dd4

    .line 2559
    invoke-virtual {v12, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2562
    move-result-object v15

    .line 2563
    invoke-virtual {v15}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2566
    check-cast v15, Landroid/widget/RadioButton;

    .line 2568
    move-object/from16 v30, v9

    .line 2570
    const v9, 0x7f0a0ddd

    .line 2573
    invoke-virtual {v12, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2576
    move-result-object v9

    .line 2577
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2580
    check-cast v9, Landroid/widget/RadioButton;

    .line 2582
    move-object/from16 v41, v0

    move-object/from16 v41, v0

    .line 2584
    const v0, 0x7f0a0694

    .line 2587
    invoke-virtual {v12, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2590
    move-result-object v0

    .line 2591
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2594
    check-cast v0, Landroid/widget/TextView;

    .line 2596
    move-object/from16 v42, v8

    .line 2598
    const v8, 0x7f0a0695

    .line 2601
    invoke-virtual {v12, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2604
    move-result-object v8

    .line 2605
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2608
    check-cast v8, Landroid/widget/TextView;

    .line 2610
    move-object/from16 v31, v14

    move-object/from16 v31, v14

    .line 2612
    const v14, 0x7f0a0696

    .line 2615
    invoke-virtual {v12, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2618
    move-result-object v14

    .line 2619
    invoke-virtual {v14}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2622
    check-cast v14, Landroid/widget/LinearLayout;

    .line 2624
    const v32, 0x7f140c9e

    .line 2627
    move-object/from16 v33, v7

    .line 2629
    invoke-static/range {v32 .. v32}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 2632
    move-result-object v7

    .line 2633
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2636
    const/16 v35, 0x1

    .line 2638
    invoke-static/range {v35 .. v35}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 2641
    move-result-object v37

    .line 2642
    move-object/from16 v38, v6

    move-object/from16 v38, v6

    .line 2644
    move/from16 v6, v35

    move/from16 v6, v35

    .line 2646
    move-object/from16 v35, v5

    move-object/from16 v35, v5

    .line 2648
    new-array v5, v6, [Ljava/lang/Object;

    .line 2650
    const/16 v39, 0x0

    .line 2652
    aput-object v37, v5, v39

    .line 2654
    invoke-static {v5, v6}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    .line 2657
    move-result-object v5

    .line 2658
    invoke-static {v7, v5}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 2661
    move-result-object v5

    .line 2662
    invoke-virtual {v0, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2665
    invoke-static/range {v32 .. v32}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 2668
    move-result-object v5

    .line 2669
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2672
    const/16 v18, 0x2

    .line 2674
    invoke-static/range {v18 .. v18}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 2677
    move-result-object v7

    .line 2678
    move-object/from16 v18, v7

    move-object/from16 v18, v7

    .line 2680
    new-array v7, v6, [Ljava/lang/Object;

    .line 2682
    aput-object v18, v7, v39

    .line 2684
    invoke-static {v7, v6, v5, v8}, Lku1;->C([Ljava/lang/Object;ILjava/lang/String;Landroid/widget/TextView;)V

    .line 2687
    const v5, 0x7f0a1020

    .line 2690
    invoke-virtual {v12, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2693
    move-result-object v5

    .line 2694
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2697
    move-object v7, v5

    .line 2698
    check-cast v7, Landroid/widget/EditText;

    .line 2700
    const v5, 0x7f0a1022

    .line 2703
    invoke-virtual {v12, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2706
    move-result-object v5

    .line 2707
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2710
    move-object v8, v5

    move-object v8, v5

    .line 2711
    check-cast v8, Landroid/widget/EditText;

    .line 2713
    const v5, 0x7f0a05f0

    .line 2716
    invoke-virtual {v12, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2719
    move-result-object v5

    .line 2720
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2723
    check-cast v5, Landroid/widget/EditText;

    .line 2725
    const v6, 0x7f0a05f2

    .line 2728
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2731
    move-result-object v6

    .line 2732
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2735
    check-cast v6, Landroid/widget/EditText;

    .line 2737
    move-object/from16 v18, v6

    move-object/from16 v18, v6

    .line 2739
    const v6, 0x7f0a1014

    .line 2742
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2745
    move-result-object v6

    .line 2746
    check-cast v6, Landroid/widget/Button;

    .line 2748
    move-object/from16 v32, v6

    .line 2750
    const v6, 0x7f0a1017

    .line 2753
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2756
    move-result-object v6

    .line 2757
    check-cast v6, Landroid/widget/Button;

    .line 2759
    move-object/from16 v40, v6

    move-object/from16 v40, v6

    .line 2761
    const v6, 0x7f0a05ea

    .line 2764
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2767
    move-result-object v6

    .line 2768
    check-cast v6, Landroid/widget/Button;

    .line 2770
    move-object/from16 v43, v6

    move-object/from16 v43, v6

    .line 2772
    const v6, 0x7f0a05ec

    .line 2775
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2778
    move-result-object v6

    .line 2779
    check-cast v6, Landroid/widget/Button;

    .line 2781
    move-object/from16 v44, v6

    move-object/from16 v44, v6

    .line 2783
    const v6, 0x7f0a0f95

    .line 2786
    invoke-virtual {v12, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 2789
    move-result-object v6

    .line 2790
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2793
    check-cast v6, Landroid/widget/CheckBox;

    .line 2795
    if-eqz v23, :cond_b68

    .line 2797
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getShowTouchLocation()Z

    .line 2800
    move-result v25

    .line 2801
    move/from16 v54, v25

    move/from16 v54, v25

    .line 2803
    move-object/from16 v25, v12

    .line 2805
    move/from16 v12, v54

    .line 2807
    goto :goto_b6b

    .line 2808
    :cond_b68
    move-object/from16 v25, v12

    .line 2810
    const/4 v12, 0x0

    .line 2811
    :goto_b6b
    invoke-virtual {v6, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2814
    if-nez v23, :cond_b75

    .line 2816
    const/4 v12, 0x1

    .line 2817
    invoke-virtual {v2, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2820
    goto :goto_b8a

    .line 2821
    :cond_b75
    const/4 v12, 0x1

    .line 2822
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 2825
    move-result v37

    .line 2826
    move/from16 v45, v12

    move/from16 v45, v12

    .line 2828
    xor-int/lit8 v12, v37, 0x1

    .line 2830
    invoke-virtual {v2, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2833
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXyPercentages()Z

    .line 2836
    move-result v2

    .line 2837
    invoke-virtual {v13, v2}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2840
    :goto_b8a
    if-eqz v23, :cond_b91

    .line 2842
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getAdditionalFingers()I

    .line 2845
    move-result v2

    .line 2846
    goto :goto_b92

    .line 2847
    :cond_b91
    const/4 v2, 0x0

    .line 2848
    :goto_b92
    if-lez v2, :cond_b96

    .line 2850
    const/4 v2, 0x1

    .line 2851
    goto :goto_b97

    .line 2852
    :cond_b96
    const/4 v2, 0x0

    .line 2853
    :goto_b97
    xor-int/lit8 v12, v2, 0x1

    .line 2855
    invoke-virtual {v15, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2858
    invoke-virtual {v9, v2}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2861
    if-eqz v2, :cond_ba3

    .line 2863
    const/4 v12, 0x0

    .line 2864
    goto :goto_ba5

    .line 2865
    :cond_ba3
    const/16 v12, 0x8

    .line 2867
    :goto_ba5
    invoke-virtual {v0, v12}, Landroid/view/View;->setVisibility(I)V

    .line 2870
    if-eqz v2, :cond_bac

    .line 2872
    const/4 v2, 0x0

    .line 2873
    goto :goto_bae

    .line 2874
    :cond_bac
    const/16 v2, 0x8

    .line 2876
    :goto_bae
    invoke-virtual {v14, v2}, Landroid/view/View;->setVisibility(I)V

    .line 2879
    new-instance v2, Lthg;

    .line 2881
    const/4 v12, 0x0

    .line 2882
    invoke-direct {v2, v0, v14, v12}, Lthg;-><init>(Landroid/widget/TextView;Landroid/widget/LinearLayout;Lm73;)V

    .line 2885
    invoke-static {v9, v2}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 2888
    new-instance v0, Luhg;

    .line 2890
    invoke-direct {v0, v1, v12}, Luhg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Lm73;)V

    .line 2893
    invoke-static {v3, v0}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 2896
    if-eqz v11, :cond_bd7

    .line 2898
    invoke-static/range {v22 .. v22}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 2901
    move-result-object v0

    .line 2902
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2905
    sget-object v2, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    .line 2907
    invoke-virtual {v0, v2}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    .line 2910
    move-result-object v0

    .line 2911
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2914
    invoke-virtual {v11, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2917
    :cond_bd7
    if-eqz v10, :cond_be4

    .line 2919
    if-eqz v23, :cond_be0

    .line 2921
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getWaitBeforeNext()Z

    .line 2924
    move-result v0

    .line 2925
    goto :goto_be1

    .line 2926
    :cond_be0
    const/4 v0, 0x1

    .line 2927
    :goto_be1
    invoke-virtual {v10, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 2930
    :cond_be4
    if-eqz v23, :cond_beb

    .line 2932
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXStartVarName()Ljava/lang/String;

    .line 2935
    move-result-object v0

    .line 2936
    goto :goto_bec

    .line 2937
    :cond_beb
    const/4 v0, 0x0

    .line 2938
    :goto_bec
    if-eqz v0, :cond_bf6

    .line 2940
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXStartVarName()Ljava/lang/String;

    .line 2943
    move-result-object v0

    .line 2944
    invoke-virtual {v4, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2947
    goto :goto_c07

    .line 2948
    :cond_bf6
    if-eqz v23, :cond_c02

    .line 2950
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getStartX()I

    .line 2953
    move-result v0

    .line 2954
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 2957
    move-result-object v0

    .line 2958
    if-nez v0, :cond_c04

    .line 2960
    :cond_c02
    move-object/from16 v0, v34

    .line 2962
    :cond_c04
    invoke-virtual {v4, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2965
    :goto_c07
    if-eqz v23, :cond_c0e

    .line 2967
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYStartVarName()Ljava/lang/String;

    .line 2970
    move-result-object v0

    .line 2971
    goto :goto_c0f

    .line 2972
    :cond_c0e
    const/4 v0, 0x0

    .line 2973
    :goto_c0f
    if-eqz v0, :cond_c1d

    .line 2975
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYStartVarName()Ljava/lang/String;

    .line 2978
    move-result-object v0

    .line 2979
    move-object/from16 v2, v35

    move-object/from16 v2, v35

    .line 2981
    invoke-virtual {v2, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 2984
    goto :goto_c30

    .line 2985
    :cond_c1d
    move-object/from16 v2, v35

    .line 2987
    if-eqz v23, :cond_c2b

    .line 2989
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getStartY()I

    .line 2992
    move-result v0

    .line 2993
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 2996
    move-result-object v0

    .line 2997
    if-nez v0, :cond_c2d

    .line 2999
    :cond_c2b
    move-object/from16 v0, v34

    .line 3001
    :cond_c2d
    invoke-virtual {v2, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3004
    :goto_c30
    if-eqz v23, :cond_c37

    .line 3006
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXEndVarName()Ljava/lang/String;

    .line 3009
    move-result-object v0

    .line 3010
    goto :goto_c38

    .line 3011
    :cond_c37
    const/4 v0, 0x0

    .line 3012
    :goto_c38
    if-eqz v0, :cond_c44

    .line 3014
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXEndVarName()Ljava/lang/String;

    .line 3017
    move-result-object v0

    .line 3018
    move-object/from16 v3, v38

    .line 3020
    invoke-virtual {v3, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3023
    goto :goto_c59

    .line 3024
    :cond_c44
    move-object/from16 v3, v38

    .line 3026
    if-eqz v23, :cond_c52

    .line 3028
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getEndX()I

    .line 3031
    move-result v0

    .line 3032
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3035
    move-result-object v0

    .line 3036
    if-nez v0, :cond_c56

    .line 3038
    :cond_c52
    move-object/from16 v0, v34

    move-object/from16 v0, v34

    .line 3040
    :cond_c56
    invoke-virtual {v3, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3043
    :goto_c59
    if-eqz v23, :cond_c60

    .line 3045
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYEndVarName()Ljava/lang/String;

    .line 3048
    move-result-object v0

    .line 3049
    goto :goto_c61

    .line 3050
    :cond_c60
    const/4 v0, 0x0

    .line 3051
    :goto_c61
    if-eqz v0, :cond_c6d

    .line 3053
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYEndVarName()Ljava/lang/String;

    .line 3056
    move-result-object v0

    .line 3057
    move-object/from16 v11, v33

    .line 3059
    invoke-virtual {v11, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3062
    goto :goto_c80

    .line 3063
    :cond_c6d
    move-object/from16 v11, v33

    .line 3065
    if-eqz v23, :cond_c7b

    .line 3067
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getEndY()I

    .line 3070
    move-result v0

    .line 3071
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3074
    move-result-object v0

    .line 3075
    if-nez v0, :cond_c7d

    .line 3077
    :cond_c7b
    move-object/from16 v0, v34

    .line 3079
    :cond_c7d
    invoke-virtual {v11, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3082
    :goto_c80
    if-eqz v23, :cond_c87

    .line 3084
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getDurationVarName()Ljava/lang/String;

    .line 3087
    move-result-object v0

    .line 3088
    goto :goto_c88

    .line 3089
    :cond_c87
    const/4 v0, 0x0

    .line 3090
    :goto_c88
    if-eqz v0, :cond_c99

    .line 3092
    if-eqz v31, :cond_c96

    .line 3094
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getDurationVarName()Ljava/lang/String;

    .line 3097
    move-result-object v0

    .line 3098
    move-object/from16 v12, v31

    .line 3100
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3103
    goto :goto_cb2

    .line 3104
    :cond_c96
    move-object/from16 v12, v31

    .line 3106
    goto :goto_cb2

    .line 3107
    :cond_c99
    move-object/from16 v12, v31

    move-object/from16 v12, v31

    .line 3109
    if-eqz v12, :cond_cb2

    .line 3111
    if-eqz v23, :cond_cab

    .line 3113
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getDurationMs()I

    .line 3116
    move-result v0

    .line 3117
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3120
    move-result-object v0

    .line 3121
    if-nez v0, :cond_caf

    .line 3123
    :cond_cab
    move-object/from16 v0, v36

    move-object/from16 v0, v36

    .line 3125
    :cond_caf
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3128
    :cond_cb2
    :goto_cb2
    if-eqz v23, :cond_cb9

    .line 3130
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXStartVarName2()Ljava/lang/String;

    .line 3133
    move-result-object v0

    .line 3134
    goto :goto_cba

    .line 3135
    :cond_cb9
    const/4 v0, 0x0

    .line 3136
    :goto_cba
    if-eqz v0, :cond_cc4

    .line 3138
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXStartVarName2()Ljava/lang/String;

    .line 3141
    move-result-object v0

    .line 3142
    invoke-virtual {v7, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3145
    goto :goto_cd5

    .line 3146
    :cond_cc4
    if-eqz v23, :cond_cd0

    .line 3148
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getStartX2()I

    .line 3151
    move-result v0

    .line 3152
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3155
    move-result-object v0

    .line 3156
    if-nez v0, :cond_cd2

    .line 3158
    :cond_cd0
    move-object/from16 v0, v34

    .line 3160
    :cond_cd2
    invoke-virtual {v7, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3163
    :goto_cd5
    if-eqz v23, :cond_cdc

    .line 3165
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYStartVarName2()Ljava/lang/String;

    .line 3168
    move-result-object v0

    .line 3169
    goto :goto_cdd

    .line 3170
    :cond_cdc
    const/4 v0, 0x0

    .line 3171
    :goto_cdd
    if-eqz v0, :cond_ce7

    .line 3173
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYStartVarName2()Ljava/lang/String;

    .line 3176
    move-result-object v0

    .line 3177
    invoke-virtual {v8, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3180
    goto :goto_cf8

    .line 3181
    :cond_ce7
    if-eqz v23, :cond_cf3

    .line 3183
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getStartY2()I

    .line 3186
    move-result v0

    .line 3187
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3190
    move-result-object v0

    .line 3191
    if-nez v0, :cond_cf5

    .line 3193
    :cond_cf3
    move-object/from16 v0, v34

    .line 3195
    :cond_cf5
    invoke-virtual {v8, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3198
    :goto_cf8
    if-eqz v23, :cond_cff

    .line 3200
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXEndVarName2()Ljava/lang/String;

    .line 3203
    move-result-object v0

    .line 3204
    goto :goto_d00

    .line 3205
    :cond_cff
    const/4 v0, 0x0

    .line 3206
    :goto_d00
    if-eqz v0, :cond_d0a

    .line 3208
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getXEndVarName2()Ljava/lang/String;

    .line 3211
    move-result-object v0

    .line 3212
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3215
    goto :goto_d1b

    .line 3216
    :cond_d0a
    if-eqz v23, :cond_d16

    .line 3218
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getEndX2()I

    .line 3221
    move-result v0

    .line 3222
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3225
    move-result-object v0

    .line 3226
    if-nez v0, :cond_d18

    .line 3228
    :cond_d16
    move-object/from16 v0, v34

    .line 3230
    :cond_d18
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3233
    :goto_d1b
    if-eqz v23, :cond_d22

    .line 3235
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYEndVarName2()Ljava/lang/String;

    .line 3238
    move-result-object v0

    .line 3239
    goto :goto_d23

    .line 3240
    :cond_d22
    const/4 v0, 0x0

    .line 3241
    :goto_d23
    if-eqz v0, :cond_d31

    .line 3243
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getYEndVarName2()Ljava/lang/String;

    .line 3246
    move-result-object v0

    .line 3247
    move-object/from16 v14, v18

    .line 3249
    invoke-virtual {v14, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3252
    :goto_d2e
    move-object/from16 v38, v3

    .line 3254
    goto :goto_d47

    .line 3255
    :cond_d31
    move-object/from16 v14, v18

    move-object/from16 v14, v18

    .line 3257
    if-eqz v23, :cond_d41

    .line 3259
    invoke-virtual/range {v23 .. v23}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;->getEndY2()I

    .line 3262
    move-result v0

    .line 3263
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 3266
    move-result-object v0

    .line 3267
    if-nez v0, :cond_d43

    .line 3269
    :cond_d41
    move-object/from16 v0, v34

    .line 3271
    :cond_d43
    invoke-virtual {v14, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3274
    goto :goto_d2e

    .line 3275
    :goto_d47
    new-instance v3, Landroid/graphics/Point;

    .line 3277
    invoke-direct {v3}, Landroid/graphics/Point;-><init>()V

    .line 3280
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 3283
    move-result-object v0

    .line 3284
    invoke-virtual {v0}, Landroid/app/Activity;->getWindowManager()Landroid/view/WindowManager;

    .line 3287
    move-result-object v0

    .line 3288
    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    .line 3291
    move-result-object v0

    .line 3292
    invoke-virtual {v0, v3}, Landroid/view/Display;->getRealSize(Landroid/graphics/Point;)V

    .line 3295
    if-eqz v30, :cond_d89

    .line 3297
    invoke-static/range {v21 .. v21}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 3300
    move-result-object v0

    .line 3301
    iget v15, v3, Landroid/graphics/Point;->x:I

    .line 3303
    iget v1, v3, Landroid/graphics/Point;->y:I

    .line 3305
    move-object/from16 v35, v2

    .line 3307
    new-instance v2, Ljava/lang/StringBuilder;

    .line 3309
    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    .line 3312
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 3315
    move-object/from16 v0, v42

    .line 3317
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 3320
    invoke-virtual {v2, v15}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 3323
    move-object/from16 v0, v41

    .line 3325
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 3328
    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 3331
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 3334
    move-result-object v0

    .line 3335
    move-object/from16 v1, v30

    .line 3337
    invoke-virtual {v1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3340
    goto :goto_d8b

    .line 3341
    :cond_d89
    move-object/from16 v35, v2

    .line 3343
    :goto_d8b
    iget v0, v3, Landroid/graphics/Point;->x:I

    .line 3345
    iget v1, v3, Landroid/graphics/Point;->y:I

    .line 3347
    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    .line 3350
    move-result v15

    .line 3351
    new-instance v0, Lvhg;

    .line 3353
    move-object/from16 v33, v11

    move-object/from16 v33, v11

    .line 3355
    const/4 v11, 0x0

    .line 3356
    move-object/from16 v1, p0

    .line 3358
    move-object v2, v4

    .line 3359
    move-object/from16 v16, v10

    .line 3361
    move-object/from16 v31, v12

    move-object/from16 v31, v12

    .line 3363
    move-object v10, v14

    .line 3364
    move/from16 v18, v15

    .line 3366
    move-object/from16 v15, v19

    .line 3368
    move-object/from16 v14, v20

    .line 3370
    move-object/from16 v12, v24

    .line 3372
    move-object/from16 v47, v26

    .line 3374
    move-object/from16 v46, v27

    .line 3376
    move-object/from16 v48, v32

    .line 3378
    move-object/from16 v4, v35

    move-object/from16 v4, v35

    .line 3380
    move-object/from16 v49, v40

    .line 3382
    move-object/from16 v50, v43

    .line 3384
    move-object/from16 v51, v44

    .line 3386
    move-object/from16 v20, v6

    move-object/from16 v20, v6

    .line 3388
    move-object/from16 v19, v9

    .line 3390
    move-object/from16 v6, v33

    .line 3392
    move-object v9, v5

    .line 3393
    move-object/from16 v5, v38

    .line 3395
    invoke-direct/range {v0 .. v11}, Lvhg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/graphics/Point;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Lm73;)V

    .line 3398
    move-object v3, v5

    .line 3399
    invoke-static {v13, v0}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 3402
    invoke-static {v1, v2, v14}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3405
    invoke-static {v1, v4, v15}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3408
    invoke-static {v1, v3, v12}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3411
    move-object/from16 v0, v46

    .line 3413
    invoke-static {v1, v6, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3416
    move-object/from16 v0, v48

    .line 3418
    invoke-static {v1, v7, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3421
    move-object/from16 v0, v49

    .line 3423
    invoke-static {v1, v8, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3426
    move-object/from16 v0, v50

    move-object/from16 v0, v50

    .line 3428
    invoke-static {v1, v9, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3431
    move-object/from16 v0, v51

    .line 3433
    invoke-static {v1, v10, v0}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->j0(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/EditText;Landroid/widget/Button;)V

    .line 3436
    if-eqz v31, :cond_e0c

    .line 3438
    new-instance v0, Lkhg;

    .line 3440
    const/16 v5, 0xa

    .line 3442
    move-object/from16 v12, v31

    .line 3444
    invoke-direct {v0, v12, v5}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 3447
    move-object/from16 v5, v47

    .line 3449
    if-eqz v5, :cond_e0e

    .line 3451
    new-instance v11, Lxnf;

    .line 3453
    const/16 v14, 0xf

    .line 3455
    invoke-direct {v11, v14, v1, v0}, Lxnf;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 3458
    invoke-virtual {v5, v11}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3461
    goto :goto_e0e

    .line 3462
    :cond_e0c
    move-object/from16 v12, v31

    .line 3464
    :cond_e0e
    :goto_e0e
    if-eqz v28, :cond_e3c

    .line 3466
    new-instance v0, Lmhg;

    .line 3468
    move-object v5, v12

    move-object v5, v12

    .line 3469
    move-object v11, v13

    .line 3470
    move-object/from16 v14, v16

    .line 3472
    move/from16 v12, v18

    .line 3474
    move-object/from16 v15, v20

    .line 3476
    move-object/from16 v16, v25

    .line 3478
    move-object/from16 v52, v28

    move-object/from16 v52, v28

    .line 3480
    move-object/from16 v53, v29

    .line 3482
    move-object v13, v1

    .line 3483
    move-object v1, v2

    .line 3484
    move-object v2, v4

    move-object v2, v4

    .line 3485
    move-object v4, v6

    .line 3486
    move-object/from16 v6, v19

    move-object/from16 v6, v19

    .line 3488
    invoke-direct/range {v0 .. v16}, Lmhg;-><init>(Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;ILcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Lvf0;)V

    .line 3491
    move-object v2, v0

    .line 3492
    move-object v1, v13

    move-object v1, v13

    .line 3493
    move-object/from16 v0, v16

    .line 3495
    move-object/from16 v5, v52

    .line 3497
    invoke-virtual {v5, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3500
    move-object/from16 v4, v53

    .line 3502
    goto :goto_e40

    .line 3503
    :cond_e3c
    move-object/from16 v0, v25

    .line 3505
    move-object/from16 v4, v29

    .line 3507
    :goto_e40
    if-eqz v4, :cond_e4c

    .line 3509
    new-instance v2, Ltkf;

    .line 3511
    const/16 v3, 0x11

    .line 3513
    invoke-direct {v2, v0, v3}, Ltkf;-><init>(Lvf0;I)V

    .line 3516
    invoke-virtual {v4, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3519
    :cond_e4c
    new-instance v2, Lihg;

    .line 3521
    const/4 v3, 0x6

    .line 3522
    invoke-direct {v2, v1, v3}, Lihg;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;I)V

    .line 3525
    invoke-virtual {v0, v2}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 3528
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 3531
    return-void

    .line 3532
    :pswitch_e59
    sget-object v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$ClearSelection;->INSTANCE:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$ClearSelection;

    .line 3534
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 3536
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->itemComplete()V

    .line 3539
    return-void

    .line 3540
    :pswitch_e61
    const/4 v3, 0x6

    .line 3541
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkActivityAlive()Z

    .line 3544
    move-result v0

    .line 3545
    if-nez v0, :cond_e6a

    .line 3547
    goto/16 :goto_fad

    .line 3549
    :cond_e6a
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 3551
    instance-of v2, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 3553
    if-eqz v2, :cond_e74

    .line 3555
    move-object v2, v0

    .line 3556
    check-cast v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 3558
    goto :goto_e75

    .line 3559
    :cond_e74
    const/4 v2, 0x0

    .line 3560
    :goto_e75
    instance-of v6, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 3562
    if-eqz v6, :cond_e80

    .line 3564
    check-cast v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;

    .line 3566
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getForceClear()Z

    .line 3569
    move-result v10

    .line 3570
    goto :goto_e81

    .line 3571
    :cond_e80
    const/4 v10, 0x0

    .line 3572
    :goto_e81
    if-eqz v2, :cond_e88

    .line 3574
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getUseClipboard()Z

    .line 3577
    move-result v7

    .line 3578
    goto :goto_e89

    .line 3579
    :cond_e88
    const/4 v7, 0x1

    .line 3580
    :goto_e89
    if-eqz v2, :cond_e94

    .line 3582
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getUseNewClipboardPasteMechanism()Z

    .line 3585
    move-result v0

    .line 3586
    const/4 v6, 0x1

    .line 3587
    if-ne v0, v6, :cond_e94

    .line 3589
    const/4 v0, 0x1

    .line 3590
    goto :goto_e95

    .line 3591
    :cond_e94
    const/4 v0, 0x0

    .line 3592
    :goto_e95
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 3595
    move-result-object v6

    .line 3596
    new-instance v8, Lvf0;

    .line 3598
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 3601
    move-result v9

    .line 3602
    invoke-direct {v8, v6, v9}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 3605
    const v9, 0x7f0d02c5

    .line 3608
    const v11, 0x7f141899

    .line 3611
    const/4 v15, 0x0

    .line 3612
    invoke-static {v8, v9, v11, v8, v15}, Liu1;->x(Lvf0;IILvf0;I)V

    .line 3615
    invoke-static {v8}, Lxje;->l(Lvf0;)V

    .line 3618
    invoke-virtual {v8, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3621
    move-result-object v5

    .line 3622
    move-object v9, v5

    move-object v9, v5

    .line 3623
    check-cast v9, Landroid/widget/Button;

    .line 3625
    invoke-virtual {v8, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3628
    move-result-object v4

    .line 3629
    move-object v11, v4

    move-object v11, v4

    .line 3630
    check-cast v11, Landroid/widget/Button;

    .line 3632
    const v4, 0x7f0a10cb

    .line 3635
    invoke-virtual {v8, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3638
    move-result-object v4

    .line 3639
    check-cast v4, Landroid/widget/EditText;

    .line 3641
    const v5, 0x7f0a0aff

    .line 3644
    invoke-virtual {v8, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3647
    move-result-object v5

    .line 3648
    check-cast v5, Landroid/widget/Button;

    .line 3650
    const v12, 0x7f0a11b9

    .line 3653
    invoke-virtual {v8, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3656
    move-result-object v12

    .line 3657
    check-cast v12, Landroid/widget/RadioButton;

    .line 3659
    const v13, 0x7f0a05f8

    .line 3662
    invoke-virtual {v8, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3665
    move-result-object v13

    .line 3666
    check-cast v13, Landroid/widget/RadioButton;

    .line 3668
    const v14, 0x7f0a05f7

    .line 3671
    invoke-virtual {v8, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3674
    move-result-object v14

    .line 3675
    check-cast v14, Landroid/view/ViewGroup;

    .line 3677
    const v15, 0x7f0a0316

    .line 3680
    invoke-virtual {v8, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3683
    move-result-object v15

    .line 3684
    check-cast v15, Landroid/widget/CheckBox;

    .line 3686
    const v3, 0x7f0a11bf

    .line 3689
    invoke-virtual {v8, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3692
    move-result-object v3

    .line 3693
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3696
    check-cast v3, Landroid/widget/RadioButton;

    .line 3698
    move-object/from16 v18, v2

    move-object/from16 v18, v2

    .line 3700
    const v2, 0x7f0a0f5c

    .line 3703
    invoke-virtual {v8, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3706
    move-result-object v2

    .line 3707
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3710
    check-cast v2, Landroid/widget/RadioButton;

    .line 3712
    move-object/from16 v19, v11

    move-object/from16 v19, v11

    .line 3714
    const v11, 0x7f0a0447

    .line 3717
    invoke-virtual {v8, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 3720
    move-result-object v11

    .line 3721
    invoke-virtual {v11}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3724
    check-cast v11, Landroid/widget/RadioGroup;

    .line 3726
    if-eqz v12, :cond_f26

    .line 3728
    invoke-virtual {v12, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3731
    :cond_f26
    if-eqz v13, :cond_f30

    .line 3733
    move/from16 v20, v7

    .line 3735
    xor-int/lit8 v7, v20, 0x1

    .line 3737
    invoke-virtual {v13, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3740
    goto :goto_f34

    .line 3741
    :cond_f30
    move/from16 v20, v7

    move/from16 v20, v7

    .line 3743
    :goto_f34
    if-eqz v15, :cond_f39

    .line 3745
    invoke-virtual {v15, v10}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3748
    :cond_f39
    xor-int/lit8 v7, v20, 0x1

    .line 3750
    invoke-virtual {v3, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3753
    if-nez v20, :cond_f42

    .line 3755
    const/4 v10, 0x0

    .line 3756
    goto :goto_f44

    .line 3757
    :cond_f42
    const/16 v10, 0x8

    .line 3759
    :goto_f44
    invoke-virtual {v11, v10}, Landroid/view/View;->setVisibility(I)V

    .line 3762
    xor-int/lit8 v7, v0, 0x1

    .line 3764
    invoke-virtual {v2, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3767
    invoke-virtual {v3, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 3770
    if-eqz v14, :cond_f5a

    .line 3772
    if-nez v20, :cond_f55

    .line 3774
    const/4 v0, 0x0

    .line 3775
    goto :goto_f57

    .line 3776
    :cond_f55
    const/16 v0, 0x8

    .line 3778
    :goto_f57
    invoke-virtual {v14, v0}, Landroid/view/View;->setVisibility(I)V

    .line 3781
    :cond_f5a
    if-eqz v13, :cond_f65

    .line 3783
    new-instance v0, Lcig;

    .line 3785
    const/4 v10, 0x0

    .line 3786
    invoke-direct {v0, v14, v11, v10}, Lcig;-><init>(Landroid/view/ViewGroup;Landroid/widget/RadioGroup;Lm73;)V

    .line 3789
    invoke-static {v13, v0}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 3792
    :cond_f65
    if-eqz v4, :cond_f74

    .line 3794
    if-eqz v18, :cond_f6f

    .line 3796
    invoke-virtual/range {v18 .. v18}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Paste;->getText()Ljava/lang/String;

    .line 3799
    move-result-object v0

    .line 3800
    if-nez v0, :cond_f71

    .line 3802
    :cond_f6f
    const-string v0, ""

    .line 3804
    :cond_f71
    invoke-virtual {v4, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 3807
    :cond_f74
    if-eqz v4, :cond_f79

    .line 3809
    invoke-static {v4}, Ldt9;->a0(Landroid/widget/EditText;)V

    .line 3812
    :cond_f79
    if-eqz v4, :cond_f8c

    .line 3814
    new-instance v0, Lkhg;

    .line 3816
    const/4 v11, 0x0

    .line 3817
    invoke-direct {v0, v4, v11}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 3820
    if-eqz v5, :cond_f8c

    .line 3822
    new-instance v2, Lfrf;

    .line 3824
    const/4 v7, 0x6

    .line 3825
    invoke-direct {v2, v6, v0, v1, v7}, Lfrf;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 3828
    invoke-virtual {v5, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3831
    :cond_f8c
    if-eqz v9, :cond_f9b

    .line 3833
    new-instance v0, Lfh1;

    .line 3835
    move-object v5, v3

    .line 3836
    move-object v6, v8

    .line 3837
    move-object v2, v12

    .line 3838
    move-object v3, v15

    .line 3839
    invoke-direct/range {v0 .. v6}, Lfh1;-><init>(Lcom/arlosoft/macrodroid/action/UIInteractionAction;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/EditText;Landroid/widget/RadioButton;Lvf0;)V

    .line 3842
    invoke-virtual {v9, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3845
    goto :goto_f9c

    .line 3846
    :cond_f9b
    move-object v6, v8

    .line 3847
    :goto_f9c
    if-eqz v19, :cond_faa

    .line 3849
    new-instance v0, Ltkf;

    .line 3851
    const/16 v1, 0xd

    .line 3853
    invoke-direct {v0, v6, v1}, Ltkf;-><init>(Lvf0;I)V

    .line 3856
    move-object/from16 v4, v19

    .line 3858
    invoke-virtual {v4, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 3861
    :cond_faa
    invoke-virtual {v6}, Landroid/app/Dialog;->show()V

    .line 3864
    :goto_fad
    return-void

    .line 3865
    :pswitch_fae
    sget-object v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Cut;->INSTANCE:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Cut;

    .line 3867
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 3869
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->itemComplete()V

    .line 3872
    return-void

    .line 3873
    :pswitch_fb6
    sget-object v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Copy;->INSTANCE:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Copy;

    .line 3875
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 3877
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->itemComplete()V

    .line 3880
    return-void

    .line 3881
    :pswitch_fbe
    move v11, v10

    .line 3882
    const/4 v6, 0x1

    .line 3883
    if-ne v0, v6, :cond_fc4

    .line 3885
    move v7, v6

    .line 3886
    goto :goto_fc6

    .line 3887
    :cond_fc4
    move v7, v11

    move v7, v11

    .line 3888
    :goto_fc6
    iput-boolean v7, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->transientLongClick:Z

    .line 3890
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->uiInteractionConfiguration:Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration;

    .line 3892
    instance-of v2, v0, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 3894
    if-eqz v2, :cond_fd2

    .line 3896
    move-object v8, v0

    .line 3897
    check-cast v8, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 3899
    goto :goto_fd3

    .line 3900
    :cond_fd2
    const/4 v8, 0x0

    .line 3901
    :goto_fd3
    if-eqz v8, :cond_fda

    .line 3903
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;->getClickOption()I

    .line 3906
    move-result v10

    .line 3907
    goto :goto_fdb

    .line 3908
    :cond_fda
    move v10, v11

    .line 3909
    :goto_fdb
    iput v10, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->transientClickOption:I

    .line 3911
    new-instance v0, Lyo;

    .line 3913
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 3916
    move-result-object v2

    .line 3917
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3920
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getAlertDialogTheme()I

    .line 3923
    move-result v3

    .line 3924
    invoke-direct {v0, v2, v3}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 3927
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptionsTitle()Ljava/lang/String;

    .line 3930
    move-result-object v2

    .line 3931
    iget-object v3, v0, Lyo;->a:Lvo;

    .line 3933
    iput-object v2, v3, Lvo;->e:Ljava/lang/CharSequence;

    .line 3935
    sget-object v2, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->Companion:Lcom/arlosoft/macrodroid/action/UIInteractionAction$b;

    .line 3937
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3940
    const v2, 0x7f141890

    .line 3943
    invoke-static {v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 3946
    move-result-object v2

    .line 3947
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 3950
    const v3, 0x7f141888

    .line 3953
    invoke-static {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 3956
    move-result-object v3

    .line 3957
    const v4, 0x7f141889

    .line 3960
    invoke-static {v4, v3}, Lku1;->k(ILjava/lang/String;)Ljava/lang/String;

    .line 3963
    move-result-object v4

    .line 3964
    const v5, 0x7f1418a4

    .line 3967
    invoke-static {v5}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 3970
    move-result-object v5

    .line 3971
    const v6, 0x7f1418a8

    .line 3974
    invoke-static {v6, v5}, Lku1;->k(ILjava/lang/String;)Ljava/lang/String;

    .line 3977
    move-result-object v6

    .line 3978
    filled-new-array {v2, v3, v4, v5, v6}, [Ljava/lang/String;

    .line 3981
    move-result-object v2

    .line 3982
    check-cast v2, [Ljava/lang/CharSequence;

    .line 3984
    iget v3, v1, Lcom/arlosoft/macrodroid/action/UIInteractionAction;->transientClickOption:I

    .line 3986
    new-instance v4, Ldee;

    .line 3988
    const/16 v5, 0x9

    .line 3990
    invoke-direct {v4, v1, v5}, Ldee;-><init>(Ljava/lang/Object;I)V

    .line 3993
    invoke-virtual {v0, v2, v3, v4}, Lyo;->j([Ljava/lang/CharSequence;ILandroid/content/DialogInterface$OnClickListener;)V

    .line 3996
    const/high16 v2, 0x1040000

    .line 3998
    const/4 v10, 0x0

    .line 3999
    invoke-virtual {v0, v2, v10}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 4002
    new-instance v2, Lgob;

    .line 4004
    const/16 v3, 0x1a

    .line 4006
    invoke-direct {v2, v3, v1, v8}, Lgob;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 4009
    const v1, 0x104000a

    .line 4012
    invoke-virtual {v0, v1, v2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 4015
    invoke-virtual {v0}, Lyo;->a()Lzo;

    .line 4018
    move-result-object v0

    .line 4019
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 4022
    return-void

    nop

    .line 4023
    :pswitch_data_104e
    .packed-switch 0x0
        :pswitch_fbe
        :pswitch_fbe
        :pswitch_fb6
        :pswitch_fae
        :pswitch_e61
        :pswitch_e59
        :pswitch_96b
        :pswitch_67e
        :pswitch_676
        :pswitch_335
        :pswitch_37
    .end packed-switch
.end method
