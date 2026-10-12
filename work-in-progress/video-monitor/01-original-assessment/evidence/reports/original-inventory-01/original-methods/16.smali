.method public final secondaryItemConfirmed()V
    .locals 50

    .line 1
    move-object/from16 v1, p0

    .line 3
    iget-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_packageName:Ljava/lang/String;

    .line 5
    if-eqz v0, :cond_16

    .line 7
    iget-object v2, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_applicationName:Ljava/lang/String;

    .line 9
    if-eqz v2, :cond_16

    .line 11
    iget-object v2, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_packageNameList:Ljava/util/ArrayList;

    .line 13
    invoke-virtual {v2, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 16
    iget-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_applicationNameList:Ljava/util/ArrayList;

    .line 18
    iget-object v2, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_applicationName:Ljava/lang/String;

    .line 20
    invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 23
    :cond_16
    const/4 v0, 0x0

    .line 24
    iput-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_packageName:Ljava/lang/String;

    .line 26
    iput-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_applicationName:Ljava/lang/String;

    .line 28
    new-instance v2, Ljava/util/ArrayList;

    .line 30
    iget-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_packageNameList:Ljava/util/ArrayList;

    .line 32
    invoke-direct {v2, v0}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 35
    new-instance v5, Ljava/util/ArrayList;

    .line 37
    iget-object v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_applicationNameList:Ljava/util/ArrayList;

    .line 39
    invoke-direct {v5, v0}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 42
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_excludeApps:Z

    .line 44
    const/4 v9, 0x1

    .line 45
    new-array v8, v9, [Z

    .line 47
    const/4 v10, 0x0

    .line 48
    aput-boolean v0, v8, v10

    .line 50
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 53
    move-result-object v0

    .line 54
    const v3, 0x7f150360

    .line 57
    const v4, 0x7f0d0561

    .line 60
    invoke-static {v0, v3, v4}, Lbl5;->h(Landroid/app/Activity;II)Lvf0;

    .line 63
    move-result-object v11

    .line 64
    const v3, 0x7f1416af

    .line 67
    invoke-static {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 70
    move-result-object v3

    .line 71
    const v4, 0x7f1416a9

    .line 74
    invoke-static {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 77
    move-result-object v4

    .line 78
    filled-new-array {v3, v4}, [Ljava/lang/String;

    .line 81
    move-result-object v3

    .line 82
    iget v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_option:I

    .line 84
    aget-object v3, v3, v4

    .line 86
    invoke-virtual {v11, v3}, Lvf0;->setTitle(Ljava/lang/CharSequence;)V

    .line 89
    new-instance v3, Landroid/view/WindowManager$LayoutParams;

    .line 91
    invoke-direct {v3}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 94
    invoke-static {v11, v3}, Lbl5;->A(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 97
    const/4 v4, -0x1

    .line 98
    iput v4, v3, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 100
    const v4, 0x7f0a0ca4

    .line 103
    invoke-static {v11, v3, v4}, Liu1;->i(Lvf0;Landroid/view/WindowManager$LayoutParams;I)Landroid/view/View;

    .line 106
    move-result-object v3

    .line 107
    move-object v14, v3

    .line 108
    check-cast v14, Landroid/widget/Button;

    .line 110
    const v3, 0x7f0a0252

    .line 113
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 116
    move-result-object v3

    .line 117
    move-object v12, v3

    move-object v12, v3

    .line 118
    check-cast v12, Landroid/widget/Button;

    .line 120
    const v3, 0x7f0a00fe

    .line 123
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 126
    move-result-object v3

    .line 127
    check-cast v3, Landroid/widget/TextView;

    .line 129
    const v4, 0x7f0a0c84

    .line 132
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 135
    move-result-object v4

    .line 136
    move-object/from16 v16, v4

    .line 138
    check-cast v16, Landroid/widget/EditText;

    .line 140
    const v4, 0x7f0a0c7e

    .line 143
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 146
    move-result-object v4

    .line 147
    move-object v15, v4

    .line 148
    check-cast v15, Landroid/widget/RadioButton;

    .line 150
    const v4, 0x7f0a0c82

    .line 153
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 156
    move-result-object v4

    .line 157
    move-object/from16 v22, v4

    move-object/from16 v22, v4

    .line 159
    check-cast v22, Landroid/widget/RadioButton;

    .line 161
    const v4, 0x7f0a0c7f

    .line 164
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 167
    move-result-object v4

    .line 168
    move-object/from16 v23, v4

    .line 170
    check-cast v23, Landroid/widget/RadioButton;

    .line 172
    const v4, 0x7f0a0c81

    .line 175
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 178
    move-result-object v4

    .line 179
    move-object/from16 v24, v4

    .line 181
    check-cast v24, Landroid/widget/RadioButton;

    .line 183
    const v4, 0x7f0a05db

    .line 186
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 189
    move-result-object v4

    .line 190
    move-object v13, v4

    move-object v13, v4

    .line 191
    check-cast v13, Landroid/widget/CheckBox;

    .line 193
    const v4, 0x7f0a09cd

    .line 196
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 199
    move-result-object v4

    .line 200
    check-cast v4, Landroid/widget/CheckBox;

    .line 202
    const v6, 0x7f0a0c80

    .line 205
    invoke-virtual {v11, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 208
    move-result-object v6

    .line 209
    check-cast v6, Landroid/widget/CheckBox;

    .line 211
    const v7, 0x7f0a0c83

    .line 214
    invoke-virtual {v11, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 217
    move-result-object v7

    .line 218
    check-cast v7, Landroid/widget/CheckBox;

    .line 220
    const v9, 0x7f0a0fe2

    .line 223
    invoke-virtual {v11, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 226
    move-result-object v9

    .line 227
    check-cast v9, Landroid/view/ViewGroup;

    .line 229
    const v10, 0x7f0a0fe1

    .line 232
    invoke-virtual {v11, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 235
    move-result-object v10

    .line 236
    check-cast v10, Landroidx/appcompat/widget/AppCompatSpinner;

    .line 238
    move-object/from16 v17, v0

    .line 240
    const v0, 0x7f0a0b02

    .line 243
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 246
    move-result-object v0

    .line 247
    check-cast v0, Landroid/widget/Button;

    .line 249
    move-object/from16 v18, v0

    .line 251
    const v0, 0x7f0a0136

    .line 254
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 257
    move-result-object v0

    .line 258
    check-cast v0, Landroid/widget/RadioGroup;

    .line 260
    const v1, 0x7f0a0130

    .line 263
    invoke-virtual {v11, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 266
    move-result-object v1

    .line 267
    check-cast v1, Landroid/view/ViewGroup;

    .line 269
    move-object/from16 v19, v2

    .line 271
    const v2, 0x7f0a0f49

    .line 274
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 277
    move-result-object v2

    .line 278
    check-cast v2, Landroid/widget/CheckBox;

    .line 280
    move-object/from16 v20, v2

    move-object/from16 v20, v2

    .line 282
    const v2, 0x7f0a0fb8

    .line 285
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 288
    move-result-object v2

    .line 289
    check-cast v2, Landroid/view/ViewGroup;

    .line 291
    move-object/from16 v21, v2

    .line 293
    const v2, 0x7f0a0c27

    .line 296
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 299
    move-result-object v2

    .line 300
    check-cast v2, Landroid/view/ViewGroup;

    .line 302
    move-object/from16 v25, v2

    .line 304
    const v2, 0x7f0a0c8b

    .line 307
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 310
    move-result-object v2

    .line 311
    move-object/from16 v31, v2

    .line 313
    check-cast v31, Landroid/widget/EditText;

    .line 315
    const v2, 0x7f0a0c6a

    .line 318
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 321
    move-result-object v2

    .line 322
    move-object/from16 v37, v2

    .line 324
    check-cast v37, Landroid/widget/EditText;

    .line 326
    const v2, 0x7f0a1127

    .line 329
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 332
    move-result-object v2

    .line 333
    check-cast v2, Landroid/widget/Button;

    .line 335
    move-object/from16 v26, v2

    .line 337
    const v2, 0x7f0a0bdf

    .line 340
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 343
    move-result-object v2

    .line 344
    check-cast v2, Landroid/widget/Button;

    .line 346
    move-object/from16 v27, v2

    .line 348
    const v2, 0x7f0a0c87

    .line 351
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 354
    move-result-object v2

    .line 355
    move-object/from16 v28, v2

    .line 357
    check-cast v28, Landroid/widget/RadioButton;

    .line 359
    const v2, 0x7f0a0c8a

    .line 362
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 365
    move-result-object v2

    .line 366
    move-object/from16 v29, v2

    .line 368
    check-cast v29, Landroid/widget/RadioButton;

    .line 370
    const v2, 0x7f0a0c88

    .line 373
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 376
    move-result-object v2

    .line 377
    move-object/from16 v30, v2

    move-object/from16 v30, v2

    .line 379
    check-cast v30, Landroid/widget/RadioButton;

    .line 381
    const v2, 0x7f0a0c89

    .line 384
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 387
    move-result-object v2

    .line 388
    move-object/from16 v32, v2

    .line 390
    check-cast v32, Landroid/widget/RadioButton;

    .line 392
    const v2, 0x7f0a0c79

    .line 395
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 398
    move-result-object v2

    .line 399
    move-object/from16 v33, v2

    move-object/from16 v33, v2

    .line 401
    check-cast v33, Landroid/widget/RadioButton;

    .line 403
    const v2, 0x7f0a0c7c

    .line 406
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 409
    move-result-object v2

    .line 410
    move-object/from16 v34, v2

    .line 412
    check-cast v34, Landroid/widget/RadioButton;

    .line 414
    const v2, 0x7f0a0c7a

    .line 417
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 420
    move-result-object v2

    .line 421
    move-object/from16 v35, v2

    move-object/from16 v35, v2

    .line 423
    check-cast v35, Landroid/widget/RadioButton;

    .line 425
    const v2, 0x7f0a0c7b

    .line 428
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 431
    move-result-object v2

    .line 432
    move-object/from16 v36, v2

    .line 434
    check-cast v36, Landroid/widget/RadioButton;

    .line 436
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 438
    move-object/from16 v38, v4

    .line 440
    const/16 v4, 0x23

    .line 442
    if-lt v2, v4, :cond_1cb

    .line 444
    const/4 v2, 0x0

    .line 445
    invoke-virtual {v3, v2}, Landroid/view/View;->setVisibility(I)V

    .line 448
    :cond_1cb
    const/16 v2, 0x8

    .line 450
    invoke-virtual {v0, v2}, Landroid/view/View;->setVisibility(I)V

    .line 453
    invoke-virtual {v1, v2}, Landroid/view/View;->setVisibility(I)V

    .line 456
    const v0, 0x7f0a0143

    .line 459
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 462
    move-result-object v0

    .line 463
    check-cast v0, Landroid/view/ViewGroup;

    .line 465
    const v1, 0x7f0a0140

    .line 468
    invoke-virtual {v11, v1}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 471
    move-result-object v1

    .line 472
    check-cast v1, Landroid/widget/TextView;

    .line 474
    const v3, 0x7f0a0141

    .line 477
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 480
    move-result-object v3

    .line 481
    check-cast v3, Landroid/widget/TextView;

    .line 483
    const v4, 0x7f0a0f15

    .line 486
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 489
    move-result-object v4

    .line 490
    check-cast v4, Landroid/widget/ImageButton;

    .line 492
    const v2, 0x7f0a00d3

    .line 495
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 498
    move-result-object v2

    .line 499
    check-cast v2, Landroid/widget/TextView;

    .line 501
    move-object/from16 v40, v1

    .line 503
    const/4 v1, 0x0

    .line 504
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 507
    move-object v0, v7

    .line 508
    aget-boolean v7, v8, v1

    .line 510
    move-object v1, v0

    .line 511
    move-object v0, v6

    .line 512
    move-object/from16 v39, v10

    .line 514
    move-object/from16 v10, v21

    .line 516
    move-object/from16 v41, v26

    .line 518
    move-object/from16 v42, v27

    .line 520
    move-object v6, v5

    .line 521
    move-object/from16 v26, v9

    move-object/from16 v26, v9

    .line 523
    move-object/from16 v21, v15

    .line 525
    move-object/from16 v5, v19

    .line 527
    move-object/from16 v9, v25

    .line 529
    move-object v15, v4

    .line 530
    move-object/from16 v25, v11

    move-object/from16 v25, v11

    .line 532
    move-object/from16 v19, v12

    .line 534
    move-object/from16 v11, v20

    move-object/from16 v11, v20

    .line 536
    move-object/from16 v12, v31

    .line 538
    move-object v4, v2

    .line 539
    move-object/from16 v20, v14

    .line 541
    move-object/from16 v2, v40

    .line 543
    const/16 v14, 0x8

    .line 545
    invoke-static/range {v2 .. v7}, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->I0(Landroid/widget/TextView;Landroid/widget/TextView;Landroid/widget/TextView;Ljava/util/ArrayList;Ljava/util/ArrayList;Z)V

    .line 548
    move-object v7, v6

    .line 549
    move-object v6, v2

    .line 550
    move-object v2, v5

    .line 551
    move-object v5, v7

    .line 552
    move-object v7, v0

    move-object v7, v0

    .line 553
    new-instance v0, Lof2;

    .line 555
    move-object v14, v8

    .line 556
    move-object v8, v4

    move-object v8, v4

    .line 557
    move-object v4, v14

    .line 558
    move-object/from16 v31, v9

    .line 560
    move-object/from16 v43, v18

    .line 562
    move-object/from16 v14, v38

    .line 564
    move-object v9, v1

    .line 565
    move-object/from16 v18, v12

    .line 567
    move-object/from16 v1, p0

    .line 569
    move-object v12, v7

    move-object v12, v7

    .line 570
    move-object v7, v3

    move-object v7, v3

    .line 571
    move-object/from16 v3, v17

    move-object/from16 v3, v17

    .line 573
    invoke-direct/range {v0 .. v8}, Lof2;-><init>(Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;Ljava/util/ArrayList;Landroid/app/Activity;[ZLjava/util/ArrayList;Landroid/widget/TextView;Landroid/widget/TextView;Landroid/widget/TextView;)V

    .line 576
    move-object/from16 v49, v3

    .line 578
    move-object v3, v0

    move-object v3, v0

    .line 579
    move-object/from16 v0, v49

    .line 581
    invoke-virtual {v15, v3}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 584
    iget v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_option:I

    .line 586
    if-nez v3, :cond_266

    .line 588
    const/4 v3, 0x0

    .line 589
    goto :goto_268

    .line 590
    :cond_266
    const/16 v3, 0x8

    .line 592
    :goto_268
    invoke-virtual {v12, v3}, Landroid/view/View;->setVisibility(I)V

    .line 595
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_ignoreOngoing:Z

    .line 597
    invoke-virtual {v12, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 600
    iget v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_option:I

    .line 602
    const/4 v6, 0x1

    .line 603
    if-eqz v3, :cond_27b

    .line 605
    if-ne v3, v6, :cond_278

    .line 607
    goto :goto_27b

    .line 608
    :cond_278
    const/16 v3, 0x8

    .line 610
    goto :goto_27c

    .line 611
    :cond_27b
    :goto_27b
    const/4 v3, 0x0

    .line 612
    :goto_27c
    invoke-virtual {v9, v3}, Landroid/view/View;->setVisibility(I)V

    .line 615
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_supressMultiples:Z

    .line 617
    invoke-virtual {v9, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 620
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->enableRegex:Z

    .line 622
    xor-int/2addr v3, v6

    .line 623
    invoke-virtual {v14, v3}, Landroid/view/View;->setEnabled(Z)V

    .line 626
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->ignoreCase:Z

    .line 628
    invoke-virtual {v14, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 631
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->enableRegex:Z

    .line 633
    invoke-virtual {v13, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 636
    new-instance v3, Lfc0;

    .line 638
    const/4 v7, 0x4

    .line 639
    invoke-direct {v3, v14, v7}, Lfc0;-><init>(Landroid/widget/CheckBox;I)V

    .line 642
    invoke-virtual {v13, v3}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 645
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->separateTitleAndMessage:Z

    .line 647
    invoke-virtual {v11, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 650
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->separateTitleAndMessage:Z

    .line 652
    const-string v7, ""

    .line 654
    if-eqz v3, :cond_2ce

    .line 656
    const/16 v3, 0x8

    .line 658
    invoke-virtual {v10, v3}, Landroid/view/View;->setVisibility(I)V

    .line 661
    move-object/from16 v3, v31

    .line 663
    const/4 v8, 0x0

    .line 664
    invoke-virtual {v3, v8}, Landroid/view/View;->setVisibility(I)V

    .line 667
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->titleContent:Ljava/lang/String;

    .line 669
    if-eqz v8, :cond_2ba

    .line 671
    :goto_2b7
    move-object/from16 v15, v18

    .line 673
    goto :goto_2bc

    .line 674
    :cond_2ba
    move-object v8, v7

    .line 675
    goto :goto_2b7

    .line 676
    :goto_2bc
    invoke-virtual {v15, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 679
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->messageContent:Ljava/lang/String;

    .line 681
    if-eqz v8, :cond_2c6

    .line 683
    :goto_2c3
    move-object/from16 v6, v37

    .line 685
    goto :goto_2c8

    .line 686
    :cond_2c6
    move-object v8, v7

    .line 687
    goto :goto_2c3

    .line 688
    :goto_2c8
    invoke-virtual {v6, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 691
    const/16 v8, 0x8

    .line 693
    goto :goto_2e1

    .line 694
    :cond_2ce
    move-object/from16 v15, v18

    move-object/from16 v15, v18

    .line 696
    move-object/from16 v3, v31

    .line 698
    move-object/from16 v6, v37

    move-object/from16 v6, v37

    .line 700
    const/4 v8, 0x0

    .line 701
    invoke-virtual {v10, v8}, Landroid/view/View;->setVisibility(I)V

    .line 704
    const/16 v8, 0x8

    .line 706
    invoke-virtual {v3, v8}, Landroid/view/View;->setVisibility(I)V

    .line 709
    :goto_2e1
    new-instance v38, Ltwa;

    .line 711
    move-object/from16 v18, v15

    .line 713
    move-object/from16 v15, v21

    .line 715
    const/16 v21, 0x1

    .line 717
    move-object/from16 v27, v10

    .line 719
    move-object v10, v12

    .line 720
    move-object/from16 v17, v28

    .line 722
    move-object/from16 v12, v38

    .line 724
    move/from16 v28, v8

    .line 726
    move-object v8, v13

    .line 727
    move-object v13, v11

    .line 728
    move-object v11, v14

    .line 729
    move-object/from16 v14, v20

    .line 731
    move-object/from16 v20, v6

    .line 733
    move-object/from16 v6, v19

    .line 735
    move-object/from16 v19, v33

    .line 737
    invoke-direct/range {v12 .. v21}, Ltwa;-><init>(Landroid/widget/CheckBox;Landroid/widget/Button;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;I)V

    .line 740
    move-object/from16 v21, v15

    move-object/from16 v21, v15

    .line 742
    move-object/from16 v37, v20

    move-object/from16 v37, v20

    .line 744
    move-object/from16 v31, v26

    .line 746
    move-object/from16 v20, v12

    move-object/from16 v20, v12

    .line 748
    move-object/from16 v26, v17

    .line 750
    move-object/from16 v12, v18

    .line 752
    new-instance v15, Lbxa;

    .line 754
    move-object/from16 v17, v3

    .line 756
    move-object/from16 v19, v16

    .line 758
    move-object/from16 v16, v27

    .line 760
    move-object/from16 v18, v37

    .line 762
    invoke-direct/range {v15 .. v20}, Lbxa;-><init>(Landroid/view/ViewGroup;Landroid/view/ViewGroup;Landroid/widget/EditText;Landroid/widget/EditText;Ltwa;)V

    .line 765
    move-object/from16 v40, v2

    .line 767
    move-object v2, v15

    .line 768
    move-object/from16 v15, v18

    .line 770
    move-object/from16 v3, v19

    .line 772
    invoke-virtual {v13, v2}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 775
    iget v2, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_option:I

    .line 777
    if-nez v2, :cond_333

    .line 779
    const/4 v2, 0x0

    .line 780
    :goto_32e
    move-object/from16 v44, v4

    .line 782
    move-object/from16 v4, v31

    .line 784
    goto :goto_336

    .line 785
    :cond_333
    move/from16 v2, v28

    .line 787
    goto :goto_32e

    .line 788
    :goto_336
    invoke-virtual {v4, v2}, Landroid/view/View;->setVisibility(I)V

    .line 791
    const v2, 0x7f141115

    .line 794
    invoke-static {v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 797
    move-result-object v2

    .line 798
    const v4, 0x7f140ce3

    .line 801
    invoke-static {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 804
    move-result-object v4

    .line 805
    const v16, 0x7f140ce2

    .line 808
    move-object/from16 v45, v5

    move-object/from16 v45, v5

    .line 810
    invoke-static/range {v16 .. v16}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 813
    move-result-object v5

    .line 814
    filled-new-array {v2, v4, v5}, [Ljava/lang/String;

    .line 817
    move-result-object v2

    .line 818
    new-instance v4, Landroid/widget/ArrayAdapter;

    .line 820
    const v5, 0x1090008

    .line 823
    invoke-direct {v4, v0, v5, v2}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;I[Ljava/lang/Object;)V

    .line 826
    const v2, 0x7f0d07d2

    .line 829
    invoke-virtual {v4, v2}, Landroid/widget/ArrayAdapter;->setDropDownViewResource(I)V

    .line 832
    move-object/from16 v2, v39

    move-object/from16 v2, v39

    .line 834
    invoke-virtual {v2, v4}, Landroidx/appcompat/widget/AppCompatSpinner;->setAdapter(Landroid/widget/SpinnerAdapter;)V

    .line 837
    iget v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_soundOption:I

    .line 839
    const/4 v5, 0x0

    .line 840
    invoke-virtual {v2, v4, v5}, Landroid/widget/AbsSpinner;->setSelection(IZ)V

    .line 843
    invoke-virtual {v3, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 846
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_textContent:Ljava/lang/String;

    .line 848
    if-eqz v4, :cond_379

    .line 850
    goto :goto_37a

    .line 851
    :cond_379
    move-object v4, v7

    .line 852
    :goto_37a
    invoke-virtual {v3, v4}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 855
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->titleContent:Ljava/lang/String;

    .line 857
    if-eqz v4, :cond_382

    .line 859
    goto :goto_383

    .line 860
    :cond_382
    move-object v4, v7

    .line 861
    :goto_383
    invoke-virtual {v12, v4}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 864
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->messageContent:Ljava/lang/String;

    .line 866
    if-eqz v4, :cond_38b

    .line 868
    move-object v7, v4

    .line 869
    :cond_38b
    invoke-virtual {v15, v7}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 872
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_textContent:Ljava/lang/String;

    .line 874
    if-eqz v4, :cond_3ce

    .line 876
    invoke-virtual {v4}, Ljava/lang/String;->length()I

    .line 879
    move-result v4

    .line 880
    if-nez v4, :cond_399

    .line 882
    goto :goto_3ce

    .line 883
    :cond_399
    iget-boolean v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_excludes:Z

    .line 885
    if-eqz v4, :cond_3b5

    .line 887
    const/4 v4, 0x3

    .line 888
    :goto_39e
    move/from16 v19, v4

    .line 890
    :goto_3a0
    move-object/from16 v37, v15

    .line 892
    move-object/from16 v15, v21

    move-object/from16 v15, v21

    .line 894
    move-object/from16 v16, v22

    .line 896
    move-object/from16 v17, v23

    move-object/from16 v17, v23

    .line 898
    move-object/from16 v18, v24

    .line 900
    :goto_3ae
    move-object/from16 v21, v20

    .line 902
    move-object/from16 v20, v3

    move-object/from16 v20, v3

    .line 904
    goto :goto_3d1

    .line 905
    :cond_3b5
    iget-boolean v4, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->m_exactMatch:Z

    .line 907
    if-eqz v4, :cond_3cc

    .line 909
    move-object/from16 v37, v15

    move-object/from16 v37, v15

    .line 911
    move-object/from16 v15, v21

    move-object/from16 v15, v21

    .line 913
    move-object/from16 v16, v22

    move-object/from16 v16, v22

    .line 915
    move-object/from16 v17, v23

    .line 917
    move-object/from16 v18, v24

    .line 919
    const/16 v19, 0x1

    .line 921
    goto :goto_3ae

    .line 922
    :cond_3cc
    const/4 v4, 0x2

    .line 923
    goto :goto_39e

    .line 924
    :cond_3ce
    :goto_3ce
    move/from16 v19, v5

    .line 926
    goto :goto_3a0

    .line 927
    :goto_3d1
    invoke-static/range {v15 .. v21}, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->n0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 930
    move-object/from16 v5, v16

    .line 932
    move-object/from16 v16, v20

    move-object/from16 v16, v20

    .line 934
    move-object/from16 v20, v21

    move-object/from16 v20, v21

    .line 936
    iget v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->matchOptionTitle:I

    .line 938
    move-object/from16 v31, v12

    move-object/from16 v31, v12

    .line 940
    move-object/from16 v27, v29

    .line 942
    move-object/from16 v28, v30

    .line 944
    move-object/from16 v29, v32

    .line 946
    move/from16 v30, v3

    .line 948
    move-object/from16 v32, v20

    .line 950
    invoke-static/range {v26 .. v32}, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->n0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 953
    move-object/from16 v17, v26

    .line 955
    move-object/from16 v19, v28

    move-object/from16 v19, v28

    .line 957
    iget v3, v1, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->matchOptionMessage:I

    .line 959
    move-object/from16 v38, v20

    .line 961
    move-object/from16 v32, v33

    .line 963
    move-object/from16 v33, v34

    .line 965
    move-object/from16 v34, v35

    .line 967
    move-object/from16 v35, v36

    move-object/from16 v35, v36

    .line 969
    move/from16 v36, v3

    .line 971
    invoke-static/range {v32 .. v38}, Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;->n0(Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;ILandroid/widget/EditText;Ltwa;)V

    .line 974
    move-object v3, v0

    .line 975
    new-instance v0, Laxa;

    .line 977
    move-object/from16 v46, v3

    .line 979
    move-object/from16 v48, v6

    move-object/from16 v48, v6

    .line 981
    move-object v6, v9

    .line 982
    move-object/from16 v47, v14

    .line 984
    move-object/from16 v3, v16

    move-object/from16 v3, v16

    .line 986
    move-object/from16 v4, v18

    .line 988
    move-object/from16 v23, v25

    .line 990
    move-object/from16 v18, v27

    .line 992
    move-object/from16 v20, v32

    move-object/from16 v20, v32

    .line 994
    move-object/from16 v21, v33

    .line 996
    move-object/from16 v22, v34

    move-object/from16 v22, v34

    .line 998
    move-object/from16 v7, v44

    .line 1000
    move-object/from16 v9, v45

    .line 1002
    move-object v14, v2

    move-object v14, v2

    .line 1003
    move-object/from16 v16, v11

    .line 1005
    move-object v11, v13

    .line 1006
    move-object v2, v15

    .line 1007
    move-object/from16 v13, v37

    .line 1009
    move-object v15, v8

    .line 1010
    move-object/from16 v8, v40

    .line 1012
    invoke-direct/range {v0 .. v23}, Laxa;-><init>(Lcom/arlosoft/macrodroid/triggers/NotificationTrigger;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/CheckBox;[ZLjava/util/ArrayList;Ljava/util/ArrayList;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Landroid/widget/EditText;Landroid/widget/EditText;Landroidx/appcompat/widget/AppCompatSpinner;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Lvf0;)V

    .line 1015
    move-object v2, v0

    .line 1016
    move-object v15, v13

    .line 1017
    move-object/from16 v0, v23

    .line 1019
    move-object/from16 v14, v47

    .line 1021
    invoke-virtual {v14, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1024
    new-instance v2, Lxr9;

    .line 1026
    const/4 v4, 0x7

    .line 1027
    invoke-direct {v2, v0, v4}, Lxr9;-><init>(Lvf0;I)V

    .line 1030
    move-object/from16 v6, v48

    .line 1032
    invoke-virtual {v6, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1035
    new-instance v2, Loo9;

    .line 1037
    const/16 v4, 0x12

    .line 1039
    invoke-direct {v2, v3, v4}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1042
    new-instance v3, Lft9;

    .line 1044
    move-object/from16 v5, v46

    move-object/from16 v5, v46

    .line 1046
    invoke-direct {v3, v1, v5, v2, v4}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1049
    move-object/from16 v2, v43

    .line 1051
    invoke-virtual {v2, v3}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1054
    new-instance v2, Loo9;

    .line 1056
    const/16 v3, 0x13

    .line 1058
    invoke-direct {v2, v12, v3}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1061
    new-instance v4, Loo9;

    .line 1063
    const/16 v6, 0x14

    .line 1065
    invoke-direct {v4, v15, v6}, Loo9;-><init>(Landroid/widget/EditText;I)V

    .line 1068
    new-instance v7, Lft9;

    .line 1070
    invoke-direct {v7, v1, v5, v2, v3}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1073
    move-object/from16 v2, v41

    .line 1075
    invoke-virtual {v2, v7}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1078
    new-instance v2, Lft9;

    .line 1080
    invoke-direct {v2, v1, v5, v4, v6}, Lft9;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1083
    move-object/from16 v1, v42

    .line 1085
    invoke-virtual {v1, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1088
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    .line 1091
    return-void
.end method
