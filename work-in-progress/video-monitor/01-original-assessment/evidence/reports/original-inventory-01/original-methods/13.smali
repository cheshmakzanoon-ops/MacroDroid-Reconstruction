.method public final secondaryItemConfirmed()V
    .locals 50

    .line 1
    move-object/from16 v1, p0

    .line 3
    new-instance v2, Ljava/util/ArrayList;

    .line 5
    iget-object v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_packageNameList:Ljava/util/ArrayList;

    .line 7
    invoke-direct {v2, v0}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 10
    new-instance v5, Ljava/util/ArrayList;

    .line 12
    iget-object v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_applicationNameList:Ljava/util/ArrayList;

    .line 14
    invoke-direct {v5, v0}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 17
    iget v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_excludesApps:I

    .line 19
    filled-new-array {v0}, [I

    .line 22
    move-result-object v20

    .line 23
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 26
    move-result-object v0

    .line 27
    new-instance v9, Lvf0;

    .line 29
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/constraint/Constraint;->getDialogTheme()I

    .line 32
    move-result v3

    .line 33
    invoke-direct {v9, v0, v3}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 36
    const v3, 0x7f0d0561

    .line 39
    invoke-virtual {v9, v3}, Lvf0;->setContentView(I)V

    .line 42
    const v3, 0x7f1407e9

    .line 45
    invoke-static {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 48
    move-result-object v3

    .line 49
    const v4, 0x7f1407e8

    .line 52
    invoke-static {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 55
    move-result-object v4

    .line 56
    filled-new-array {v3, v4}, [Ljava/lang/String;

    .line 59
    move-result-object v3

    .line 60
    iget v4, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_option:I

    .line 62
    aget-object v3, v3, v4

    .line 64
    invoke-virtual {v9, v3}, Lvf0;->setTitle(Ljava/lang/CharSequence;)V

    .line 67
    new-instance v3, Landroid/view/WindowManager$LayoutParams;

    .line 69
    invoke-direct {v3}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 72
    invoke-static {v9, v3}, Lbl5;->A(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 75
    const/4 v4, -0x1

    .line 76
    iput v4, v3, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 78
    const v6, 0x7f0a0ca4

    .line 81
    invoke-static {v9, v3, v6}, Liu1;->i(Lvf0;Landroid/view/WindowManager$LayoutParams;I)Landroid/view/View;

    .line 84
    move-result-object v3

    .line 85
    move-object v12, v3

    .line 86
    check-cast v12, Landroid/widget/Button;

    .line 88
    const v3, 0x7f0a0252

    .line 91
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 94
    move-result-object v3

    .line 95
    move-object v10, v3

    .line 96
    check-cast v10, Landroid/widget/Button;

    .line 98
    const v3, 0x7f0a0c84

    .line 101
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 104
    move-result-object v3

    .line 105
    move-object v14, v3

    .line 106
    check-cast v14, Landroid/widget/EditText;

    .line 108
    const v3, 0x7f0a0c7e

    .line 111
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 114
    move-result-object v3

    .line 115
    move-object v13, v3

    move-object v13, v3

    .line 116
    check-cast v13, Landroid/widget/RadioButton;

    .line 118
    const v3, 0x7f0a0c82

    .line 121
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 124
    move-result-object v3

    .line 125
    move-object/from16 v21, v3

    .line 127
    check-cast v21, Landroid/widget/RadioButton;

    .line 129
    const v3, 0x7f0a0c7f

    .line 132
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 135
    move-result-object v3

    .line 136
    move-object/from16 v22, v3

    .line 138
    check-cast v22, Landroid/widget/RadioButton;

    .line 140
    const v3, 0x7f0a0c81

    .line 143
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 146
    move-result-object v3

    .line 147
    move-object v11, v3

    move-object v11, v3

    .line 148
    check-cast v11, Landroid/widget/RadioButton;

    .line 150
    const v3, 0x7f0a05db

    .line 153
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 156
    move-result-object v3

    .line 157
    move-object v15, v3

    move-object v15, v3

    .line 158
    check-cast v15, Landroid/widget/CheckBox;

    .line 160
    const v3, 0x7f0a09cd

    .line 163
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 166
    move-result-object v3

    .line 167
    move-object v8, v3

    move-object v8, v3

    .line 168
    check-cast v8, Landroid/widget/CheckBox;

    .line 170
    const v3, 0x7f0a0c80

    .line 173
    invoke-virtual {v9, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 176
    move-result-object v3

    .line 177
    check-cast v3, Landroid/widget/CheckBox;

    .line 179
    const v6, 0x7f0a0c83

    .line 182
    invoke-virtual {v9, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 185
    move-result-object v6

    .line 186
    check-cast v6, Landroid/widget/CheckBox;

    .line 188
    const v7, 0x7f0a0b02

    .line 191
    invoke-virtual {v9, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 194
    move-result-object v7

    .line 195
    check-cast v7, Landroid/widget/Button;

    .line 197
    const v4, 0x7f0a0136

    .line 200
    invoke-virtual {v9, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 203
    move-result-object v4

    .line 204
    check-cast v4, Landroid/widget/RadioGroup;

    .line 206
    move-object/from16 v17, v0

    .line 208
    const v0, 0x7f0a0130

    .line 211
    invoke-virtual {v9, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 214
    move-result-object v0

    .line 215
    check-cast v0, Landroid/view/ViewGroup;

    .line 217
    const v1, 0x7f0a0f49

    .line 220
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 223
    move-result-object v1

    .line 224
    check-cast v1, Landroid/widget/CheckBox;

    .line 226
    move-object/from16 v18, v1

    .line 228
    const v1, 0x7f0a0fb8

    .line 231
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 234
    move-result-object v1

    .line 235
    check-cast v1, Landroid/view/ViewGroup;

    .line 237
    move-object/from16 v19, v1

    move-object/from16 v19, v1

    .line 239
    const v1, 0x7f0a0c27

    .line 242
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 245
    move-result-object v1

    .line 246
    check-cast v1, Landroid/view/ViewGroup;

    .line 248
    move-object/from16 v23, v1

    .line 250
    const v1, 0x7f0a0c8b

    .line 253
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 256
    move-result-object v1

    .line 257
    move-object/from16 v29, v1

    .line 259
    check-cast v29, Landroid/widget/EditText;

    .line 261
    const v1, 0x7f0a0c6a

    .line 264
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 267
    move-result-object v1

    .line 268
    move-object/from16 v35, v1

    move-object/from16 v35, v1

    .line 270
    check-cast v35, Landroid/widget/EditText;

    .line 272
    const v1, 0x7f0a1127

    .line 275
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 278
    move-result-object v1

    .line 279
    check-cast v1, Landroid/widget/Button;

    .line 281
    move-object/from16 v24, v1

    .line 283
    const v1, 0x7f0a0bdf

    .line 286
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 289
    move-result-object v1

    .line 290
    check-cast v1, Landroid/widget/Button;

    .line 292
    move-object/from16 v25, v1

    .line 294
    const v1, 0x7f0a0c87

    .line 297
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 300
    move-result-object v1

    .line 301
    move-object/from16 v26, v1

    .line 303
    check-cast v26, Landroid/widget/RadioButton;

    .line 305
    const v1, 0x7f0a0c8a

    .line 308
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 311
    move-result-object v1

    .line 312
    move-object/from16 v27, v1

    .line 314
    check-cast v27, Landroid/widget/RadioButton;

    .line 316
    const v1, 0x7f0a0c88

    .line 319
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 322
    move-result-object v1

    .line 323
    move-object/from16 v28, v1

    .line 325
    check-cast v28, Landroid/widget/RadioButton;

    .line 327
    const v1, 0x7f0a0c89

    .line 330
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 333
    move-result-object v1

    .line 334
    move-object/from16 v30, v1

    .line 336
    check-cast v30, Landroid/widget/RadioButton;

    .line 338
    const v1, 0x7f0a0c79

    .line 341
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 344
    move-result-object v1

    .line 345
    move-object/from16 v31, v1

    move-object/from16 v31, v1

    .line 347
    check-cast v31, Landroid/widget/RadioButton;

    .line 349
    const v1, 0x7f0a0c7c

    .line 352
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 355
    move-result-object v1

    .line 356
    move-object/from16 v32, v1

    .line 358
    check-cast v32, Landroid/widget/RadioButton;

    .line 360
    const v1, 0x7f0a0c7a

    .line 363
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 366
    move-result-object v1

    .line 367
    move-object/from16 v33, v1

    .line 369
    check-cast v33, Landroid/widget/RadioButton;

    .line 371
    const v1, 0x7f0a0c7b

    .line 374
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 377
    move-result-object v1

    .line 378
    move-object/from16 v34, v1

    .line 380
    check-cast v34, Landroid/widget/RadioButton;

    .line 382
    const/16 v1, 0x8

    .line 384
    invoke-virtual {v4, v1}, Landroid/view/View;->setVisibility(I)V

    .line 387
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 390
    const v0, 0x7f0a0143

    .line 393
    invoke-virtual {v9, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 396
    move-result-object v0

    .line 397
    check-cast v0, Landroid/view/ViewGroup;

    .line 399
    const v4, 0x7f0a0140

    .line 402
    invoke-virtual {v9, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 405
    move-result-object v4

    .line 406
    check-cast v4, Landroid/widget/TextView;

    .line 408
    const v1, 0x7f0a0141

    .line 411
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 414
    move-result-object v1

    .line 415
    check-cast v1, Landroid/widget/TextView;

    .line 417
    move-object/from16 v37, v1

    move-object/from16 v37, v1

    .line 419
    const v1, 0x7f0a0f15

    .line 422
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 425
    move-result-object v1

    .line 426
    check-cast v1, Landroid/widget/ImageButton;

    .line 428
    move-object/from16 v38, v1

    .line 430
    const v1, 0x7f0a00d3

    .line 433
    invoke-virtual {v9, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 436
    move-result-object v1

    .line 437
    check-cast v1, Landroid/widget/TextView;

    .line 439
    move-object/from16 v39, v9

    .line 441
    const/4 v9, 0x0

    .line 442
    invoke-virtual {v0, v9}, Landroid/view/View;->setVisibility(I)V

    .line 445
    aget v0, v20, v9

    .line 447
    const/4 v9, 0x1

    .line 448
    if-eq v0, v9, :cond_1e5

    .line 450
    const/4 v9, -0x1

    .line 451
    if-ne v0, v9, :cond_1d7

    .line 453
    invoke-virtual/range {p0 .. p0}, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->l0()Z

    .line 456
    move-result v0

    .line 457
    if-eqz v0, :cond_1d7

    .line 459
    goto :goto_1e5

    .line 460
    :cond_1d7
    move-object v0, v6

    .line 461
    move-object v6, v5

    move-object v6, v5

    .line 462
    move-object v5, v2

    .line 463
    move-object v2, v4

    .line 464
    move-object v4, v1

    .line 465
    move-object v1, v7

    move-object v1, v7

    .line 466
    const/4 v7, 0x0

    .line 467
    :goto_1e0
    move-object v9, v3

    move-object v9, v3

    .line 468
    move-object/from16 v3, v37

    .line 470
    goto :goto_1f0

    .line 471
    :cond_1e5
    :goto_1e5
    move-object v0, v6

    move-object v0, v6

    .line 472
    move-object v6, v5

    move-object v6, v5

    .line 473
    move-object v5, v2

    .line 474
    move-object v2, v4

    move-object v2, v4

    .line 475
    move-object v4, v1

    .line 476
    move-object v1, v7

    .line 477
    const/4 v7, 0x1

    .line 478
    goto :goto_1e0

    .line 479
    :goto_1f0
    invoke-static/range {v2 .. v7}, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->n0(Landroid/widget/TextView;Landroid/widget/TextView;Landroid/widget/TextView;Ljava/util/ArrayList;Ljava/util/ArrayList;Z)V

    .line 482
    move-object v7, v6

    .line 483
    move-object v6, v2

    .line 484
    move-object v2, v5

    move-object v2, v5

    .line 485
    move-object v5, v7

    .line 486
    move-object v7, v0

    move-object v7, v0

    .line 487
    new-instance v0, Lof2;

    .line 489
    move-object/from16 v40, v1

    .line 491
    move-object/from16 v16, v10

    .line 493
    move-object/from16 v41, v19

    .line 495
    move-object/from16 v42, v23

    .line 497
    move-object/from16 v45, v24

    .line 499
    move-object/from16 v46, v25

    .line 501
    move-object/from16 v43, v29

    .line 503
    move-object/from16 v44, v35

    .line 505
    move-object/from16 v1, p0

    .line 507
    move-object v10, v8

    .line 508
    move-object/from16 v19, v18

    move-object/from16 v19, v18

    .line 510
    move-object v8, v4

    .line 511
    move-object/from16 v18, v13

    move-object/from16 v18, v13

    .line 513
    move-object/from16 v4, v17

    move-object/from16 v4, v17

    .line 515
    move-object/from16 v13, v38

    .line 517
    move-object/from16 v17, v12

    move-object/from16 v17, v12

    .line 519
    move-object v12, v7

    .line 520
    move-object v7, v3

    .line 521
    move-object/from16 v3, v20

    .line 523
    move-object/from16 v20, v9

    .line 525
    const/16 v9, 0x8

    .line 527
    invoke-direct/range {v0 .. v8}, Lof2;-><init>(Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;Ljava/util/ArrayList;[ILandroid/app/Activity;Ljava/util/ArrayList;Landroid/widget/TextView;Landroid/widget/TextView;Landroid/widget/TextView;)V

    .line 530
    invoke-virtual {v13, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 533
    iget v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_option:I

    .line 535
    const/4 v6, 0x1

    .line 536
    if-ne v0, v6, :cond_23f

    .line 538
    invoke-virtual {v11, v9}, Landroid/view/View;->setVisibility(I)V

    .line 541
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_excludes:Z

    .line 543
    if-eqz v0, :cond_23f

    .line 545
    const/4 v0, 0x0

    .line 546
    iput-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_excludes:Z

    .line 548
    :cond_23f
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->enableRegex:Z

    .line 550
    xor-int/2addr v0, v6

    .line 551
    invoke-virtual {v10, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 554
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->ignoreCase:Z

    .line 556
    invoke-virtual {v10, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 559
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->enableRegex:Z

    .line 561
    invoke-virtual {v15, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 564
    new-instance v0, Lwr1;

    .line 566
    const/4 v7, 0x5

    .line 567
    invoke-direct {v0, v10, v7}, Lwr1;-><init>(Landroid/widget/CheckBox;I)V

    .line 570
    invoke-virtual {v15, v0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 573
    invoke-virtual {v12, v9}, Landroid/view/View;->setVisibility(I)V

    .line 576
    const/4 v0, 0x0

    .line 577
    invoke-virtual {v14, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 580
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->ignoreOngoing:Z

    .line 582
    move-object/from16 v8, v20

    move-object/from16 v8, v20

    .line 584
    invoke-virtual {v8, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 587
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->separateTitleAndMessage:Z

    .line 589
    move-object/from16 v12, v19

    .line 591
    invoke-virtual {v12, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 594
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->separateTitleAndMessage:Z

    .line 596
    const-string v20, ""

    .line 598
    if-eqz v7, :cond_29f

    .line 600
    move-object/from16 v7, v41

    .line 602
    invoke-virtual {v7, v9}, Landroid/view/View;->setVisibility(I)V

    .line 605
    move-object/from16 v13, v42

    .line 607
    invoke-virtual {v13, v0}, Landroid/view/View;->setVisibility(I)V

    .line 610
    iget-object v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->titleContent:Ljava/lang/String;

    .line 612
    if-eqz v0, :cond_286

    .line 614
    :goto_283
    move-object/from16 v9, v43

    .line 616
    goto :goto_289

    .line 617
    :cond_286
    move-object/from16 v0, v20

    .line 619
    goto :goto_283

    .line 620
    :goto_289
    invoke-virtual {v9, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 623
    iget-object v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->messageContent:Ljava/lang/String;

    .line 625
    if-eqz v0, :cond_293

    .line 627
    :goto_290
    move-object/from16 v6, v44

    .line 629
    goto :goto_298

    .line 630
    :cond_293
    move-object/from16 v0, v20

    move-object/from16 v0, v20

    .line 632
    goto :goto_290

    .line 633
    :goto_298
    invoke-virtual {v6, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 636
    move-object/from16 v43, v9

    .line 638
    const/4 v0, 0x0

    .line 639
    goto :goto_2ad

    .line 640
    :cond_29f
    move-object/from16 v7, v41

    .line 642
    move-object/from16 v13, v42

    move-object/from16 v13, v42

    .line 644
    move-object/from16 v6, v44

    .line 646
    invoke-virtual {v7, v0}, Landroid/view/View;->setVisibility(I)V

    .line 649
    invoke-virtual {v13, v9}, Landroid/view/View;->setVisibility(I)V

    .line 652
    :goto_2ad
    new-instance v19, Ltwa;

    .line 654
    move-object/from16 v36, v19

    .line 656
    const/16 v19, 0x0

    .line 658
    move-object/from16 v37, v10

    .line 660
    move-object v9, v11

    move-object v9, v11

    .line 661
    move-object v11, v12

    .line 662
    move-object/from16 v42, v13

    move-object/from16 v42, v13

    .line 664
    move-object/from16 v23, v15

    .line 666
    move-object/from16 v12, v17

    .line 668
    move-object/from16 v13, v18

    move-object/from16 v13, v18

    .line 670
    move-object/from16 v15, v26

    .line 672
    move-object/from16 v17, v31

    move-object/from16 v17, v31

    .line 674
    move-object/from16 v10, v36

    .line 676
    move-object/from16 v18, v6

    .line 678
    move-object/from16 v6, v16

    .line 680
    move-object/from16 v16, v43

    move-object/from16 v16, v43

    .line 682
    invoke-direct/range {v10 .. v19}, Ltwa;-><init>(Landroid/widget/CheckBox;Landroid/widget/Button;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;I)V

    .line 685
    move-object v10, v13

    move-object v10, v13

    .line 686
    move-object/from16 v24, v15

    .line 688
    move-object/from16 v16, v18

    .line 690
    move-object/from16 v17, v14

    move-object/from16 v17, v14

    .line 692
    new-instance v13, Ljf2;

    .line 694
    const/16 v19, 0x5

    .line 696
    move-object v14, v7

    .line 697
    move-object/from16 v18, v36

    .line 699
    move-object/from16 v15, v42

    .line 701
    move-object/from16 v7, v43

    .line 703
    invoke-direct/range {v13 .. v19}, Ljf2;-><init>(Ljava/lang/Object;Landroid/view/KeyEvent$Callback;Landroid/widget/TextView;Landroid/view/View;Ljava/lang/Object;I)V

    .line 706
    move-object v15, v13

    .line 707
    move-object/from16 v13, v16

    .line 709
    move-object/from16 v14, v17

    .line 711
    invoke-virtual {v11, v15}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 714
    iget-object v15, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_textContent:Ljava/lang/String;

    .line 716
    if-eqz v15, :cond_2fc

    .line 718
    goto :goto_2fe

    .line 719
    :cond_2fc
    move-object/from16 v15, v20

    .line 721
    :goto_2fe
    invoke-virtual {v14, v15}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 724
    iget-object v15, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->titleContent:Ljava/lang/String;

    .line 726
    if-eqz v15, :cond_306

    .line 728
    goto :goto_308

    .line 729
    :cond_306
    move-object/from16 v15, v20

    .line 731
    :goto_308
    invoke-virtual {v7, v15}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 734
    iget-object v15, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->messageContent:Ljava/lang/String;

    .line 736
    if-eqz v15, :cond_310

    .line 738
    goto :goto_312

    .line 739
    :cond_310
    move-object/from16 v15, v20

    .line 741
    :goto_312
    invoke-virtual {v13, v15}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 744
    iget-object v15, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_textContent:Ljava/lang/String;

    .line 746
    if-eqz v15, :cond_325

    .line 748
    invoke-virtual {v15}, Ljava/lang/String;->length()I

    .line 751
    move-result v15

    .line 752
    if-nez v15, :cond_320

    .line 754
    goto :goto_325

    .line 755
    :cond_320
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_excludes:Z

    .line 757
    if-eqz v0, :cond_339

    .line 759
    const/4 v0, 0x3

    .line 760
    :cond_325
    :goto_325
    move/from16 v17, v0

    move/from16 v17, v0

    .line 762
    move-object/from16 v16, v9

    .line 764
    move-object/from16 v35, v13

    .line 766
    move-object/from16 v18, v14

    .line 768
    move-object/from16 v14, v21

    .line 770
    move-object/from16 v15, v22

    move-object/from16 v15, v22

    .line 772
    move-object/from16 v19, v36

    .line 774
    :goto_337
    move-object v13, v10

    .line 775
    goto :goto_354

    .line 776
    :cond_339
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->m_exactMatch:Z

    .line 778
    if-eqz v0, :cond_352

    .line 780
    move-object/from16 v16, v9

    move-object/from16 v16, v9

    .line 782
    move-object/from16 v35, v13

    .line 784
    move-object/from16 v18, v14

    move-object/from16 v18, v14

    .line 786
    move-object/from16 v14, v21

    .line 788
    move-object/from16 v15, v22

    move-object/from16 v15, v22

    .line 790
    move-object/from16 v19, v36

    .line 792
    const/16 v17, 0x1

    .line 794
    goto :goto_337

    .line 795
    :cond_352
    const/4 v0, 0x2

    .line 796
    goto :goto_325

    .line 797
    :goto_354
    invoke-static/range {v13 .. v19}, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->k0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 800
    move-object/from16 v17, v18

    .line 802
    move-object/from16 v36, v19

    .line 804
    iget v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->matchOptionTitle:I

    .line 806
    move-object/from16 v29, v7

    move-object/from16 v29, v7

    .line 808
    move-object/from16 v25, v27

    move-object/from16 v25, v27

    .line 810
    move-object/from16 v26, v28

    .line 812
    move-object/from16 v27, v30

    .line 814
    move-object/from16 v30, v36

    .line 816
    move/from16 v28, v0

    .line 818
    invoke-static/range {v24 .. v30}, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->k0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 821
    move-object/from16 v43, v29

    .line 823
    iget v0, v1, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->matchOptionMessage:I

    .line 825
    move-object/from16 v30, v31

    .line 827
    move-object/from16 v31, v32

    .line 829
    move-object/from16 v32, v33

    move-object/from16 v32, v33

    .line 831
    move-object/from16 v33, v34

    move-object/from16 v33, v34

    .line 833
    move/from16 v34, v0

    move/from16 v34, v0

    .line 835
    invoke-static/range {v30 .. v36}, Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;->k0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 838
    move-object/from16 v9, v16

    move-object/from16 v9, v16

    .line 840
    move-object/from16 v16, v31

    .line 842
    move-object/from16 v31, v30

    .line 844
    new-instance v0, Lk56;

    .line 846
    move-object/from16 v18, v2

    .line 848
    move-object/from16 v20, v3

    .line 850
    move-object/from16 v47, v4

    .line 852
    move-object/from16 v19, v5

    move-object/from16 v19, v5

    .line 854
    move-object/from16 v49, v6

    .line 856
    move-object v4, v9

    .line 857
    move-object v6, v11

    move-object v6, v11

    .line 858
    move-object/from16 v48, v12

    .line 860
    move-object v2, v13

    .line 861
    move-object v5, v14

    move-object v5, v14

    .line 862
    move-object/from16 v3, v17

    .line 864
    move-object/from16 v9, v23

    .line 866
    move-object/from16 v12, v24

    move-object/from16 v12, v24

    .line 868
    move-object/from16 v13, v25

    .line 870
    move-object/from16 v14, v26

    .line 872
    move-object/from16 v15, v31

    move-object/from16 v15, v31

    .line 874
    move-object/from16 v17, v32

    .line 876
    move-object/from16 v10, v37

    move-object/from16 v10, v37

    .line 878
    move-object/from16 v21, v39

    .line 880
    move-object/from16 v7, v43

    .line 882
    move-object v11, v8

    move-object v11, v8

    .line 883
    move-object/from16 v8, v35

    .line 885
    invoke-direct/range {v0 .. v21}, Lk56;-><init>(Lcom/arlosoft/macrodroid/constraint/NotificationPresentConstraint;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Ljava/util/ArrayList;Ljava/util/ArrayList;[ILvf0;)V

    .line 888
    move-object v2, v0

    .line 889
    move-object v14, v3

    .line 890
    move-object v6, v8

    move-object v6, v8

    .line 891
    move-object/from16 v0, v21

    move-object/from16 v0, v21

    .line 893
    move-object/from16 v12, v48

    .line 895
    invoke-virtual {v12, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 898
    new-instance v2, Lxr9;

    .line 900
    const/4 v3, 0x6

    .line 901
    invoke-direct {v2, v0, v3}, Lxr9;-><init>(Lvf0;I)V

    .line 904
    move-object/from16 v3, v49

    move-object/from16 v3, v49

    .line 906
    invoke-virtual {v3, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 909
    new-instance v2, Loo9;

    .line 911
    const/16 v3, 0xd

    .line 913
    invoke-direct {v2, v14, v3}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 916
    new-instance v4, Lft9;

    .line 918
    const/16 v5, 0xf

    .line 920
    move-object/from16 v8, v47

    .line 922
    invoke-direct {v4, v1, v8, v2, v5}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 925
    move-object/from16 v2, v40

    .line 927
    invoke-virtual {v2, v4}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 930
    new-instance v2, Loo9;

    .line 932
    const/16 v4, 0xe

    .line 934
    invoke-direct {v2, v7, v4}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 937
    new-instance v7, Loo9;

    .line 939
    invoke-direct {v7, v6, v5}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 942
    new-instance v5, Lft9;

    .line 944
    invoke-direct {v5, v1, v8, v2, v3}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 947
    move-object/from16 v2, v45

    .line 949
    invoke-virtual {v2, v5}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 952
    new-instance v2, Lft9;

    .line 954
    invoke-direct {v2, v1, v8, v7, v4}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 957
    move-object/from16 v1, v46

    .line 959
    invoke-virtual {v1, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 962
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 965
    return-void
.end method
