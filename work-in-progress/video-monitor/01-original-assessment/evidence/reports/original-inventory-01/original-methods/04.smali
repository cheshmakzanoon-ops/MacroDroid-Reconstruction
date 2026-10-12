.method public final handleItemSelected()V
    .locals 47

    .line 1
    move-object/from16 v2, p0

    .line 3
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 6
    move-result-object v0

    .line 7
    new-instance v1, Lvf0;

    .line 9
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 12
    move-result v3

    .line 13
    invoke-direct {v1, v0, v3}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 16
    const v3, 0x7f0d0561

    .line 19
    invoke-virtual {v1, v3}, Lvf0;->setContentView(I)V

    .line 22
    const v3, 0x7f140261

    .line 25
    invoke-virtual {v1, v3}, Lvf0;->setTitle(I)V

    .line 28
    iget-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->packageName:Ljava/lang/String;

    .line 30
    iput-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->workingPackageName:Ljava/lang/String;

    .line 32
    iget-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->applicationName:Ljava/lang/String;

    .line 34
    iput-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->workingApplicationName:Ljava/lang/String;

    .line 36
    new-instance v3, Landroid/view/WindowManager$LayoutParams;

    .line 38
    invoke-direct {v3}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 41
    invoke-virtual {v1}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    .line 44
    move-result-object v4

    .line 45
    if-eqz v4, :cond_33

    .line 47
    invoke-virtual {v4}, Landroid/view/Window;->getAttributes()Landroid/view/WindowManager$LayoutParams;

    .line 50
    move-result-object v4

    .line 51
    goto :goto_34

    .line 52
    :cond_33
    const/4 v4, 0x0

    .line 53
    :goto_34
    invoke-virtual {v3, v4}, Landroid/view/WindowManager$LayoutParams;->copyFrom(Landroid/view/WindowManager$LayoutParams;)I

    .line 56
    const/4 v4, -0x1

    .line 57
    iput v4, v3, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 59
    invoke-virtual {v1}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    .line 62
    move-result-object v4

    .line 63
    if-eqz v4, :cond_43

    .line 65
    invoke-virtual {v4, v3}, Landroid/view/Window;->setAttributes(Landroid/view/WindowManager$LayoutParams;)V

    .line 68
    :cond_43
    const v3, 0x7f0a0ca4

    .line 71
    invoke-virtual {v1, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 74
    move-result-object v3

    .line 75
    move-object v8, v3

    .line 76
    check-cast v8, Landroid/widget/Button;

    .line 78
    const v3, 0x7f0a0252

    .line 81
    invoke-virtual {v1, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 84
    move-result-object v3

    .line 85
    check-cast v3, Landroid/widget/Button;

    .line 87
    const v4, 0x7f0a11cc

    .line 90
    invoke-virtual {v1, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 93
    move-result-object v4

    .line 94
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 97
    check-cast v4, Landroid/widget/RadioButton;

    .line 99
    const v6, 0x7f0a048e

    .line 102
    invoke-virtual {v1, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 105
    move-result-object v6

    .line 106
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 109
    check-cast v6, Landroid/view/ViewGroup;

    .line 111
    const v7, 0x7f0a048f

    .line 114
    invoke-virtual {v1, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 117
    move-result-object v7

    .line 118
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 121
    check-cast v7, Landroid/widget/RadioButton;

    .line 123
    const v9, 0x7f0a0f14

    .line 126
    invoke-virtual {v1, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 129
    move-result-object v9

    .line 130
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 133
    check-cast v9, Landroid/widget/ImageButton;

    .line 135
    const v10, 0x7f0a0139

    .line 138
    invoke-virtual {v1, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 141
    move-result-object v10

    .line 142
    invoke-virtual {v10}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 145
    check-cast v10, Landroid/widget/TextView;

    .line 147
    iput-object v10, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->applicationNameText:Landroid/widget/TextView;

    .line 149
    const v10, 0x7f0a0c84

    .line 152
    invoke-virtual {v1, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 155
    move-result-object v10

    .line 156
    move-object v15, v10

    .line 157
    check-cast v15, Landroid/widget/EditText;

    .line 159
    const v10, 0x7f0a0c7e

    .line 162
    invoke-virtual {v1, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 165
    move-result-object v10

    .line 166
    check-cast v10, Landroid/widget/RadioButton;

    .line 168
    const v11, 0x7f0a0c82

    .line 171
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 174
    move-result-object v11

    .line 175
    check-cast v11, Landroid/widget/RadioButton;

    .line 177
    const v12, 0x7f0a0c7f

    .line 180
    invoke-virtual {v1, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 183
    move-result-object v12

    .line 184
    check-cast v12, Landroid/widget/RadioButton;

    .line 186
    const v13, 0x7f0a0c81

    .line 189
    invoke-virtual {v1, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 192
    move-result-object v13

    .line 193
    check-cast v13, Landroid/widget/RadioButton;

    .line 195
    const v14, 0x7f0a09cd

    .line 198
    invoke-virtual {v1, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 201
    move-result-object v14

    .line 202
    invoke-virtual {v14}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 205
    check-cast v14, Landroid/widget/CheckBox;

    .line 207
    const v5, 0x7f0a05db

    .line 210
    invoke-virtual {v1, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 213
    move-result-object v5

    .line 214
    check-cast v5, Landroid/widget/CheckBox;

    .line 216
    move-object/from16 v18, v3

    .line 218
    const v3, 0x7f0a0c80

    .line 221
    invoke-virtual {v1, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 224
    move-result-object v3

    .line 225
    check-cast v3, Landroid/widget/CheckBox;

    .line 227
    move-object/from16 v17, v8

    .line 229
    const v8, 0x7f0a0b02

    .line 232
    invoke-virtual {v1, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 235
    move-result-object v8

    .line 236
    check-cast v8, Landroid/widget/Button;

    .line 238
    move-object/from16 v19, v8

    .line 240
    const v8, 0x7f0a0c83

    .line 243
    invoke-virtual {v1, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 246
    move-result-object v8

    .line 247
    check-cast v8, Landroid/widget/CheckBox;

    .line 249
    move-object/from16 v20, v10

    .line 251
    const/16 v10, 0x8

    .line 253
    if-eqz v8, :cond_101

    .line 255
    invoke-virtual {v8, v10}, Landroid/view/View;->setVisibility(I)V

    .line 258
    :cond_101
    const v8, 0x7f0a006c

    .line 261
    invoke-virtual {v1, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 264
    move-result-object v8

    .line 265
    check-cast v8, Landroid/view/ViewGroup;

    .line 267
    const/4 v10, 0x0

    .line 268
    if-eqz v8, :cond_110

    .line 270
    invoke-virtual {v8, v10}, Landroid/view/View;->setVisibility(I)V

    .line 273
    :cond_110
    const v8, 0x7f0a0c64

    .line 276
    invoke-virtual {v1, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 279
    move-result-object v8

    .line 280
    check-cast v8, Landroid/widget/Spinner;

    .line 282
    move/from16 v22, v10

    .line 284
    const v10, 0x7f0a0f49

    .line 287
    invoke-virtual {v1, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 290
    move-result-object v10

    .line 291
    check-cast v10, Landroid/widget/CheckBox;

    .line 293
    move-object/from16 v23, v11

    .line 295
    const v11, 0x7f0a0fb8

    .line 298
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 301
    move-result-object v11

    .line 302
    check-cast v11, Landroid/view/ViewGroup;

    .line 304
    move-object/from16 v24, v12

    move-object/from16 v24, v12

    .line 306
    const v12, 0x7f0a0c27

    .line 309
    invoke-virtual {v1, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 312
    move-result-object v12

    .line 313
    check-cast v12, Landroid/view/ViewGroup;

    .line 315
    move-object/from16 v25, v13

    move-object/from16 v25, v13

    .line 317
    const v13, 0x7f0a0c8b

    .line 320
    invoke-virtual {v1, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 323
    move-result-object v13

    .line 324
    check-cast v13, Landroid/widget/EditText;

    .line 326
    move-object/from16 v26, v12

    .line 328
    const v12, 0x7f0a0c6a

    .line 331
    invoke-virtual {v1, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 334
    move-result-object v12

    .line 335
    check-cast v12, Landroid/widget/EditText;

    .line 337
    move-object/from16 v27, v11

    .line 339
    const v11, 0x7f0a1127

    .line 342
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 345
    move-result-object v11

    .line 346
    check-cast v11, Landroid/widget/Button;

    .line 348
    move-object/from16 v28, v11

    move-object/from16 v28, v11

    .line 350
    const v11, 0x7f0a0bdf

    .line 353
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 356
    move-result-object v11

    .line 357
    check-cast v11, Landroid/widget/Button;

    .line 359
    move-object/from16 v29, v11

    .line 361
    const v11, 0x7f0a0c87

    .line 364
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 367
    move-result-object v11

    .line 368
    check-cast v11, Landroid/widget/RadioButton;

    .line 370
    move-object/from16 v30, v11

    .line 372
    const v11, 0x7f0a0c8a

    .line 375
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 378
    move-result-object v11

    .line 379
    move-object/from16 v31, v11

    .line 381
    check-cast v31, Landroid/widget/RadioButton;

    .line 383
    const v11, 0x7f0a0c88

    .line 386
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 389
    move-result-object v11

    .line 390
    move-object/from16 v32, v11

    move-object/from16 v32, v11

    .line 392
    check-cast v32, Landroid/widget/RadioButton;

    .line 394
    const v11, 0x7f0a0c89

    .line 397
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 400
    move-result-object v11

    .line 401
    move-object/from16 v33, v11

    .line 403
    check-cast v33, Landroid/widget/RadioButton;

    .line 405
    const v11, 0x7f0a0c79

    .line 408
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 411
    move-result-object v11

    .line 412
    check-cast v11, Landroid/widget/RadioButton;

    .line 414
    move-object/from16 v34, v11

    move-object/from16 v34, v11

    .line 416
    const v11, 0x7f0a0c7c

    .line 419
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 422
    move-result-object v11

    .line 423
    move-object/from16 v35, v11

    .line 425
    check-cast v35, Landroid/widget/RadioButton;

    .line 427
    const v11, 0x7f0a0c7a

    .line 430
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 433
    move-result-object v11

    .line 434
    move-object/from16 v36, v11

    .line 436
    check-cast v36, Landroid/widget/RadioButton;

    .line 438
    const v11, 0x7f0a0c7b

    .line 441
    invoke-virtual {v1, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 444
    move-result-object v11

    .line 445
    move-object/from16 v37, v11

    .line 447
    check-cast v37, Landroid/widget/RadioButton;

    .line 449
    iget-object v11, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->workingPackageName:Ljava/lang/String;

    .line 451
    invoke-virtual {v11}, Ljava/lang/String;->length()I

    .line 454
    move-result v11

    .line 455
    move-object/from16 v38, v1

    .line 457
    const/4 v1, 0x1

    .line 458
    if-nez v11, :cond_1d7

    .line 460
    iput-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->useNotificationTrigger:Z

    .line 462
    :cond_1d7
    iget-object v11, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->applicationNameText:Landroid/widget/TextView;

    .line 464
    move/from16 v39, v1

    move/from16 v39, v1

    .line 466
    if-eqz v11, :cond_1f4

    .line 468
    iget-object v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->applicationName:Ljava/lang/String;

    .line 470
    invoke-virtual {v1}, Ljava/lang/String;->length()I

    .line 473
    move-result v40

    .line 474
    if-nez v40, :cond_1f1

    .line 476
    const v1, 0x7f1410dc

    .line 479
    invoke-static {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 482
    move-result-object v1

    .line 483
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 486
    :cond_1f1
    invoke-virtual {v11, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 489
    :cond_1f4
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->useNotificationTrigger:Z

    .line 491
    invoke-virtual {v4, v1}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 494
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->useNotificationTrigger:Z

    .line 496
    xor-int/lit8 v1, v1, 0x1

    .line 498
    invoke-virtual {v7, v1}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 501
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->useNotificationTrigger:Z

    .line 503
    if-nez v1, :cond_207

    .line 505
    move/from16 v1, v22

    .line 507
    goto :goto_209

    .line 508
    :cond_207
    const/16 v1, 0x8

    .line 510
    :goto_209
    invoke-virtual {v6, v1}, Landroid/view/View;->setVisibility(I)V

    .line 513
    new-instance v1, Luva;

    .line 515
    const/4 v7, 0x0

    .line 516
    invoke-direct {v1, v6, v7}, Luva;-><init>(Landroid/view/ViewGroup;Lm73;)V

    .line 519
    invoke-static {v4, v1}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 522
    const v1, 0x7f140263

    .line 525
    invoke-static {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 528
    move-result-object v1

    .line 529
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 532
    filled-new-array {v1}, [Ljava/lang/String;

    .line 535
    move-result-object v1

    .line 536
    invoke-static {v1}, Lmx2;->I([Ljava/lang/Object;)Ljava/util/ArrayList;

    .line 539
    move-result-object v1

    .line 540
    move/from16 v6, v39

    .line 542
    :goto_229
    const/4 v7, 0x6

    .line 543
    if-ge v6, v7, :cond_258

    .line 545
    const v7, 0x7f140262

    .line 548
    invoke-static {v7}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 551
    move-result-object v7

    .line 552
    invoke-virtual {v7}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 555
    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 558
    move-result-object v11

    .line 559
    move-object/from16 v40, v4

    .line 561
    move/from16 v41, v6

    move/from16 v41, v6

    .line 563
    move/from16 v4, v39

    .line 565
    new-array v6, v4, [Ljava/lang/Object;

    .line 567
    aput-object v11, v6, v22

    .line 569
    invoke-static {v6, v4}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    .line 572
    move-result-object v6

    .line 573
    invoke-static {v7, v6}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 576
    move-result-object v4

    .line 577
    invoke-virtual {v1, v4}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 580
    add-int/lit8 v6, v41, 0x1

    .line 582
    move-object/from16 v4, v40

    .line 584
    const/16 v39, 0x1

    .line 586
    goto :goto_229

    .line 587
    :cond_258
    move-object/from16 v40, v4

    .line 589
    new-instance v4, Landroid/widget/ArrayAdapter;

    .line 591
    const v6, 0x1090008

    .line 594
    invoke-direct {v4, v0, v6, v1}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;ILjava/util/List;)V

    .line 597
    const v1, 0x7f0d07d2

    .line 600
    invoke-virtual {v4, v1}, Landroid/widget/ArrayAdapter;->setDropDownViewResource(I)V

    .line 603
    if-eqz v8, :cond_26d

    .line 605
    invoke-virtual {v8, v4}, Landroid/widget/Spinner;->setAdapter(Landroid/widget/SpinnerAdapter;)V

    .line 608
    :cond_26d
    if-eqz v8, :cond_276

    .line 610
    iget v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->actionsOption:I

    .line 612
    move/from16 v4, v22

    .line 614
    invoke-virtual {v8, v1, v4}, Landroid/widget/AbsSpinner;->setSelection(IZ)V

    .line 617
    :cond_276
    new-instance v1, Lvva;

    .line 619
    const/4 v7, 0x0

    .line 620
    invoke-direct {v1, v2, v7}, Lvva;-><init>(Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;Lm73;)V

    .line 623
    invoke-static {v9, v1}, Ldt9;->Q(Landroid/view/View;Lln6;)V

    .line 626
    if-eqz v3, :cond_286

    .line 628
    const/16 v1, 0x8

    .line 630
    invoke-virtual {v3, v1}, Landroid/view/View;->setVisibility(I)V

    .line 633
    :cond_286
    if-eqz v15, :cond_28d

    .line 635
    iget-object v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->matchText:Ljava/lang/String;

    .line 637
    invoke-virtual {v15, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 640
    :cond_28d
    const-string v1, ""

    .line 642
    if-eqz v13, :cond_299

    .line 644
    iget-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->titleContent:Ljava/lang/String;

    .line 646
    if-nez v3, :cond_296

    .line 648
    move-object v3, v1

    .line 649
    :cond_296
    invoke-virtual {v13, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 652
    :cond_299
    if-eqz v12, :cond_2a4

    .line 654
    iget-object v3, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->messageContent:Ljava/lang/String;

    .line 656
    if-nez v3, :cond_2a0

    .line 658
    goto :goto_2a1

    .line 659
    :cond_2a0
    move-object v1, v3

    .line 660
    :goto_2a1
    invoke-virtual {v12, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 663
    :cond_2a4
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->enableRegex:Z

    .line 665
    const/16 v39, 0x1

    .line 667
    xor-int/lit8 v1, v1, 0x1

    .line 669
    invoke-virtual {v14, v1}, Landroid/view/View;->setEnabled(Z)V

    .line 672
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->ignoreCase:Z

    .line 674
    invoke-virtual {v14, v1}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 677
    if-eqz v5, :cond_2b9

    .line 679
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->enableRegex:Z

    .line 681
    invoke-virtual {v5, v1}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 684
    :cond_2b9
    if-eqz v5, :cond_2c4

    .line 686
    new-instance v1, Lwva;

    .line 688
    const/4 v7, 0x0

    .line 689
    invoke-direct {v1, v14, v7}, Lwva;-><init>(Landroid/widget/CheckBox;Lm73;)V

    .line 692
    invoke-static {v5, v1}, Lnug;->e0(Landroid/widget/CompoundButton;Lnn6;)V

    .line 695
    :cond_2c4
    if-eqz v10, :cond_2cb

    .line 697
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->separateTitleAndMessage:Z

    .line 699
    invoke-virtual {v10, v1}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 702
    :cond_2cb
    iget-boolean v1, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->separateTitleAndMessage:Z

    .line 704
    if-eqz v1, :cond_2e5

    .line 706
    move-object/from16 v11, v27

    move-object/from16 v11, v27

    .line 708
    if-eqz v27, :cond_2da

    .line 710
    const/16 v1, 0x8

    .line 712
    invoke-virtual {v11, v1}, Landroid/view/View;->setVisibility(I)V

    .line 715
    :cond_2da
    move-object/from16 v1, v26

    move-object/from16 v1, v26

    .line 717
    const/4 v4, 0x0

    .line 718
    if-eqz v26, :cond_2f8

    .line 720
    invoke-virtual {v1, v4}, Landroid/view/View;->setVisibility(I)V

    .line 723
    goto :goto_2f8

    .line 724
    :cond_2e5
    move-object/from16 v1, v26

    .line 726
    move-object/from16 v11, v27

    move-object/from16 v11, v27

    .line 728
    const/4 v4, 0x0

    .line 729
    if-eqz v11, :cond_2f1

    .line 731
    invoke-virtual {v11, v4}, Landroid/view/View;->setVisibility(I)V

    .line 734
    :cond_2f1
    if-eqz v1, :cond_2f8

    .line 736
    const/16 v3, 0x8

    .line 738
    invoke-virtual {v1, v3}, Landroid/view/View;->setVisibility(I)V

    .line 741
    :cond_2f8
    :goto_2f8
    new-instance v16, Lu56;

    .line 743
    move-object/from16 v21, v0

    move-object/from16 v21, v0

    .line 745
    move-object/from16 v26, v1

    .line 747
    move v0, v4

    .line 748
    move-object v7, v10

    move-object v7, v10

    .line 749
    move-object/from16 v27, v11

    .line 751
    move-object v10, v15

    .line 752
    move-object/from16 v6, v16

    .line 754
    move-object/from16 v15, v19

    .line 756
    move-object/from16 v9, v20

    .line 758
    move-object/from16 v4, v23

    .line 760
    move-object/from16 v1, v24

    move-object/from16 v1, v24

    .line 762
    move-object/from16 v3, v25

    .line 764
    move-object/from16 v42, v28

    move-object/from16 v42, v28

    .line 766
    move-object/from16 v43, v29

    .line 768
    move-object/from16 v11, v30

    .line 770
    move-object/from16 v20, v8

    .line 772
    move-object/from16 v19, v14

    .line 774
    move-object/from16 v8, v17

    move-object/from16 v8, v17

    .line 776
    move-object v14, v12

    .line 777
    move-object v12, v13

    .line 778
    move-object/from16 v13, v34

    .line 780
    invoke-direct/range {v6 .. v14}, Lu56;-><init>(Landroid/widget/CheckBox;Landroid/widget/Button;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;)V

    .line 783
    move-object v6, v9

    .line 784
    move-object/from16 v17, v10

    move-object/from16 v17, v10

    .line 786
    move-object v10, v11

    .line 787
    move-object/from16 v11, v27

    .line 789
    move-object/from16 v27, v31

    .line 791
    move-object/from16 v31, v12

    .line 793
    if-eqz v7, :cond_34a

    .line 795
    move-object v12, v11

    .line 796
    new-instance v11, Ljf2;

    .line 798
    move-object v9, v15

    .line 799
    move-object/from16 v15, v17

    .line 801
    const/16 v17, 0x3

    .line 803
    move-object/from16 v13, v26

    .line 805
    invoke-direct/range {v11 .. v17}, Ljf2;-><init>(Ljava/lang/Object;Landroid/view/KeyEvent$Callback;Landroid/widget/TextView;Landroid/view/View;Ljava/lang/Object;I)V

    .line 808
    invoke-virtual {v7, v11}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 811
    goto :goto_34d

    .line 812
    :cond_34a
    move-object v9, v15

    .line 813
    move-object/from16 v15, v17

    .line 815
    :goto_34d
    if-eqz v4, :cond_352

    .line 817
    invoke-virtual {v4, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 820
    :cond_352
    if-eqz v1, :cond_357

    .line 822
    invoke-virtual {v1, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 825
    :cond_357
    if-eqz v3, :cond_35c

    .line 827
    invoke-virtual {v3, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 830
    :cond_35c
    if-eqz v6, :cond_361

    .line 832
    invoke-virtual {v6, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 835
    :cond_361
    iget v11, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->matchOption:I

    .line 837
    if-eqz v11, :cond_390

    .line 839
    const/4 v12, 0x1

    .line 840
    if-eq v11, v12, :cond_385

    .line 842
    const/4 v0, 0x2

    .line 843
    if-eq v11, v0, :cond_37a

    .line 845
    const/4 v0, 0x3

    .line 846
    if-eq v11, v0, :cond_36f

    .line 848
    goto :goto_39b

    .line 849
    :cond_36f
    if-eqz v3, :cond_374

    .line 851
    invoke-virtual {v3, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 854
    :cond_374
    if-eqz v15, :cond_39b

    .line 856
    invoke-virtual {v15, v12}, Landroid/view/View;->setEnabled(Z)V

    .line 859
    goto :goto_39b

    .line 860
    :cond_37a
    if-eqz v1, :cond_37f

    .line 862
    invoke-virtual {v1, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 865
    :cond_37f
    if-eqz v15, :cond_39b

    .line 867
    invoke-virtual {v15, v12}, Landroid/view/View;->setEnabled(Z)V

    .line 870
    goto :goto_39b

    .line 871
    :cond_385
    if-eqz v4, :cond_38a

    .line 873
    invoke-virtual {v4, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 876
    :cond_38a
    if-eqz v15, :cond_39b

    .line 878
    invoke-virtual {v15, v12}, Landroid/view/View;->setEnabled(Z)V

    .line 881
    goto :goto_39b

    .line 882
    :cond_390
    const/4 v12, 0x1

    .line 883
    if-eqz v6, :cond_396

    .line 885
    invoke-virtual {v6, v12}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 888
    :cond_396
    if-eqz v15, :cond_39b

    .line 890
    invoke-virtual {v15, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 893
    :cond_39b
    :goto_39b
    iget v0, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->matchOptionTitle:I

    .line 895
    move/from16 v30, v0

    move/from16 v30, v0

    .line 897
    move-object/from16 v26, v10

    .line 899
    move-object/from16 v28, v32

    move-object/from16 v28, v32

    .line 901
    move-object/from16 v29, v33

    .line 903
    move-object/from16 v32, v16

    .line 905
    invoke-static/range {v26 .. v32}, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->T(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Lu56;)V

    .line 908
    move-object/from16 v0, v27

    .line 910
    move-object/from16 v16, v28

    .line 912
    move-object/from16 v13, v31

    .line 914
    iget v10, v2, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->matchOptionMessage:I

    .line 916
    move/from16 v31, v10

    .line 918
    move-object/from16 v33, v32

    .line 920
    move-object/from16 v27, v34

    .line 922
    move-object/from16 v28, v35

    .line 924
    move-object/from16 v29, v36

    .line 926
    move-object/from16 v30, v37

    .line 928
    move-object/from16 v32, v14

    move-object/from16 v32, v14

    .line 930
    invoke-static/range {v27 .. v33}, Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;->T(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Lu56;)V

    .line 933
    move-object/from16 v32, v33

    .line 935
    if-eqz v6, :cond_3ec

    .line 937
    move-object v10, v6

    .line 938
    new-instance v6, Luw7;

    .line 940
    move-object v11, v1

    move-object v11, v1

    .line 941
    move-object v12, v3

    .line 942
    move-object v1, v7

    .line 943
    move-object v3, v10

    .line 944
    move-object v7, v15

    .line 945
    move-object v10, v4

    move-object v10, v4

    .line 946
    move-object v15, v9

    move-object v15, v9

    .line 947
    move-object v9, v8

    .line 948
    move-object/from16 v8, v32

    move-object/from16 v8, v32

    .line 950
    invoke-direct/range {v6 .. v12}, Luw7;-><init>(Landroid/widget/EditText;Lu56;Landroid/widget/Button;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;)V

    .line 953
    move-object v4, v9

    .line 954
    move-object v9, v8

    .line 955
    move-object v8, v4

    .line 956
    move-object v4, v10

    .line 957
    move-object v10, v6

    .line 958
    move-object v6, v12

    .line 959
    invoke-virtual {v3, v10}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 962
    goto :goto_3f7

    .line 963
    :cond_3ec
    move-object v11, v6

    .line 964
    move-object v6, v3

    move-object v6, v3

    .line 965
    move-object v3, v11

    .line 966
    move-object v11, v1

    .line 967
    move-object v1, v7

    .line 968
    move-object v7, v15

    move-object v7, v15

    .line 969
    move-object v15, v9

    .line 970
    move-object/from16 v9, v32

    .line 972
    :goto_3f7
    if-eqz v4, :cond_403

    .line 974
    new-instance v10, Lmf2;

    .line 976
    const/16 v12, 0x9

    .line 978
    invoke-direct {v10, v3, v11, v6, v12}, Lmf2;-><init>(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;I)V

    .line 981
    invoke-virtual {v4, v10}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 984
    :cond_403
    const/16 v10, 0xa

    .line 986
    if-eqz v11, :cond_40f

    .line 988
    new-instance v12, Lmf2;

    .line 990
    invoke-direct {v12, v4, v3, v6, v10}, Lmf2;-><init>(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;I)V

    .line 993
    invoke-virtual {v11, v12}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 996
    :cond_40f
    const/16 v12, 0xb

    .line 998
    if-eqz v6, :cond_41b

    .line 1000
    new-instance v10, Lmf2;

    .line 1002
    invoke-direct {v10, v4, v11, v3, v12}, Lmf2;-><init>(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;I)V

    .line 1005
    invoke-virtual {v6, v10}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1008
    :cond_41b
    if-eqz v7, :cond_426

    .line 1010
    new-instance v10, Ltva;

    .line 1012
    const/4 v12, 0x1

    .line 1013
    invoke-direct {v10, v9, v12}, Ltva;-><init>(Lu56;I)V

    .line 1016
    invoke-virtual {v7, v10}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 1019
    :cond_426
    if-eqz v8, :cond_471

    .line 1021
    move-object/from16 v27, v0

    move-object/from16 v27, v0

    .line 1023
    new-instance v0, Lsva;

    .line 1025
    move-object/from16 v17, v7

    move-object/from16 v17, v7

    .line 1027
    move-object/from16 v45, v8

    move-object/from16 v45, v8

    .line 1029
    move-object/from16 v32, v9

    .line 1031
    move-object v8, v13

    move-object v8, v13

    .line 1032
    move-object v9, v14

    .line 1033
    move-object/from16 v12, v16

    .line 1035
    move-object/from16 v46, v18

    move-object/from16 v46, v18

    .line 1037
    move-object/from16 v16, v20

    .line 1039
    move-object/from16 v44, v21

    move-object/from16 v44, v21

    .line 1041
    move-object/from16 v10, v26

    move-object/from16 v10, v26

    .line 1043
    move-object/from16 v14, v28

    .line 1045
    move-object/from16 v13, v34

    move-object/from16 v13, v34

    .line 1047
    move-object/from16 v20, v38

    .line 1049
    move-object v7, v1

    .line 1050
    move-object/from16 v18, v5

    .line 1052
    move-object v5, v11

    .line 1053
    move-object/from16 v21, v15

    .line 1055
    move-object/from16 v11, v27

    .line 1057
    move-object/from16 v15, v29

    .line 1059
    move-object/from16 v1, v40

    move-object/from16 v1, v40

    .line 1061
    invoke-direct/range {v0 .. v20}, Lsva;-><init>(Landroid/widget/RadioButton;Lcom/arlosoft/macrodroid/action/NotificationInteractionAction;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/Spinner;Landroid/widget/EditText;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Lvf0;)V

    .line 1064
    move-object v1, v0

    .line 1065
    move-object v12, v8

    .line 1066
    move-object v14, v9

    .line 1067
    move-object/from16 v15, v17

    .line 1069
    move-object/from16 v0, v20

    .line 1071
    move-object/from16 v8, v45

    .line 1073
    invoke-virtual {v8, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1076
    goto :goto_481

    .line 1077
    :cond_471
    move-object/from16 v32, v9

    move-object/from16 v32, v9

    .line 1079
    move-object v12, v13

    .line 1080
    move-object/from16 v46, v18

    move-object/from16 v46, v18

    .line 1082
    move-object/from16 v44, v21

    .line 1084
    move-object/from16 v0, v38

    .line 1086
    move-object/from16 v21, v15

    .line 1088
    move-object v15, v7

    .line 1089
    :goto_481
    invoke-virtual/range {v32 .. v32}, Lu56;->invoke()Ljava/lang/Object;

    .line 1092
    move-object/from16 v3, v46

    move-object/from16 v3, v46

    .line 1094
    if-eqz v3, :cond_493

    .line 1096
    new-instance v1, Lwo9;

    .line 1098
    const/4 v4, 0x5

    .line 1099
    invoke-direct {v1, v4, v0, v2}, Lwo9;-><init>(ILvf0;Lcom/arlosoft/macrodroid/action/Action;)V

    .line 1102
    invoke-virtual {v3, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1105
    :cond_493
    new-instance v1, Loo9;

    .line 1107
    const/16 v3, 0xa

    .line 1109
    invoke-direct {v1, v15, v3}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1112
    invoke-virtual/range {v21 .. v21}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 1115
    new-instance v4, Lft9;

    .line 1117
    move-object/from16 v5, v44

    .line 1119
    invoke-direct {v4, v5, v1, v2, v3}, Lft9;-><init>(Landroid/app/Activity;Ljava/lang/Object;Lcom/arlosoft/macrodroid/action/Action;I)V

    .line 1122
    move-object/from16 v15, v21

    .line 1124
    invoke-virtual {v15, v4}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1127
    new-instance v1, Loo9;

    .line 1129
    const/16 v3, 0xb

    .line 1131
    invoke-direct {v1, v12, v3}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1134
    new-instance v4, Loo9;

    .line 1136
    const/16 v6, 0xc

    .line 1138
    invoke-direct {v4, v14, v6}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1141
    move-object/from16 v11, v42

    .line 1143
    if-eqz v11, :cond_4c3

    .line 1145
    new-instance v7, Lft9;

    .line 1147
    invoke-direct {v7, v5, v1, v2, v3}, Lft9;-><init>(Landroid/app/Activity;Ljava/lang/Object;Lcom/arlosoft/macrodroid/action/Action;I)V

    .line 1150
    invoke-virtual {v11, v7}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1153
    :cond_4c3
    move-object/from16 v11, v43

    .line 1155
    if-eqz v11, :cond_4cf

    .line 1157
    new-instance v1, Lft9;

    .line 1159
    invoke-direct {v1, v5, v4, v2, v6}, Lft9;-><init>(Landroid/app/Activity;Ljava/lang/Object;Lcom/arlosoft/macrodroid/action/Action;I)V

    .line 1162
    invoke-virtual {v11, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1165
    :cond_4cf
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 1168
    return-void
.end method
