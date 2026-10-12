.method public final X(Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;)V
    .locals 61

    .line 1
    move-object/from16 v1, p0

    .line 3
    const/16 v9, 0x8

    .line 5
    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 8
    move-result-object v0

    .line 9
    iget v2, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 11
    iput v2, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->workingIconType:I

    .line 13
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 16
    move-result-object v10

    .line 17
    new-instance v11, Lvf0;

    .line 19
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/action/Action;->getDialogTheme()I

    .line 22
    move-result v2

    .line 23
    invoke-direct {v11, v10, v2}, Lvf0;-><init>(Landroid/content/Context;I)V

    .line 26
    const v2, 0x7f0d0235

    .line 29
    invoke-virtual {v11, v2}, Lvf0;->setContentView(I)V

    .line 32
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 35
    move-result-object v2

    .line 36
    invoke-virtual {v11, v2}, Lvf0;->setTitle(Ljava/lang/CharSequence;)V

    .line 39
    new-instance v2, Landroid/view/WindowManager$LayoutParams;

    .line 41
    invoke-direct {v2}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 44
    invoke-static {v11, v2}, Lku1;->y(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 47
    const/4 v3, -0x1

    .line 48
    iput v3, v2, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 50
    const v3, 0x7f0a0ca4

    .line 53
    invoke-static {v11, v2, v3}, Lku1;->i(Lvf0;Landroid/view/WindowManager$LayoutParams;I)Landroid/view/View;

    .line 56
    move-result-object v2

    .line 57
    move-object v12, v2

    move-object v12, v2

    .line 58
    check-cast v12, Landroid/widget/Button;

    .line 60
    const v2, 0x7f0a0252

    .line 63
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 66
    move-result-object v2

    .line 67
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 70
    move-object v13, v2

    .line 71
    check-cast v13, Landroid/widget/Button;

    .line 73
    const v2, 0x7f0a06cd

    .line 76
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 79
    move-result-object v2

    .line 80
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 83
    move-object v14, v2

    .line 84
    check-cast v14, Landroid/widget/Button;

    .line 86
    const v2, 0x7f0a06ce

    .line 89
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 92
    move-result-object v2

    .line 93
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 96
    check-cast v2, Landroid/widget/Button;

    .line 98
    const v3, 0x7f0a06cc

    .line 101
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 104
    move-result-object v3

    .line 105
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 108
    move-object v15, v3

    .line 109
    check-cast v15, Landroid/widget/SeekBar;

    .line 111
    const v3, 0x7f0a0cf2

    .line 114
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 117
    move-result-object v3

    .line 118
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 121
    move-object v7, v3

    .line 122
    check-cast v7, Landroid/widget/SeekBar;

    .line 124
    const v3, 0x7f0a00f3

    .line 127
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 130
    move-result-object v3

    .line 131
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 134
    check-cast v3, Landroid/widget/TextView;

    .line 136
    const v4, 0x7f0a0cf3

    .line 139
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 142
    move-result-object v4

    .line 143
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 146
    check-cast v4, Landroid/widget/TextView;

    .line 148
    const v5, 0x7f0a0c5f

    .line 151
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 154
    move-result-object v5

    .line 155
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 158
    move-object v6, v5

    .line 159
    check-cast v6, Landroid/widget/RadioButton;

    .line 161
    const v5, 0x7f0a0bea

    .line 164
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 167
    move-result-object v5

    .line 168
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 171
    check-cast v5, Landroid/widget/RadioButton;

    .line 173
    const v8, 0x7f0a0f9f

    .line 176
    invoke-virtual {v11, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 179
    move-result-object v8

    .line 180
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 183
    check-cast v8, Landroid/widget/CheckBox;

    .line 185
    const v9, 0x7f0a06d1

    .line 188
    invoke-virtual {v11, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 191
    move-result-object v9

    .line 192
    invoke-virtual {v9}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 195
    check-cast v9, Landroid/widget/ImageView;

    .line 197
    move-object/from16 v17, v0

    move-object/from16 v17, v0

    .line 199
    const v0, 0x7f0a0654

    .line 202
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 205
    move-result-object v0

    .line 206
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 209
    check-cast v0, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    .line 211
    move-object/from16 v18, v0

    .line 213
    const v0, 0x7f0a116a

    .line 216
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 219
    move-result-object v0

    .line 220
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 223
    check-cast v0, Landroid/widget/CheckBox;

    .line 225
    move-object/from16 v19, v0

    .line 227
    const v0, 0x7f0a06e9

    .line 230
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 233
    move-result-object v0

    .line 234
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 237
    check-cast v0, Landroid/widget/CheckBox;

    .line 239
    move-object/from16 v20, v0

    .line 241
    const v0, 0x7f0a12e7    # 1.835316E38f

    .line 244
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 247
    move-result-object v0

    .line 248
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 251
    move-object/from16 v22, v0

    .line 253
    check-cast v22, Landroid/widget/EditText;

    .line 255
    const v0, 0x7f0a12f3

    .line 258
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 261
    move-result-object v0

    .line 262
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 265
    move-object/from16 v23, v0

    move-object/from16 v23, v0

    .line 267
    check-cast v23, Landroid/widget/EditText;

    .line 269
    const v0, 0x7f0a05b9

    .line 272
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 275
    move-result-object v0

    .line 276
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 279
    check-cast v0, Lcom/google/android/material/textfield/TextInputLayout;

    .line 281
    move-object/from16 v21, v0

    .line 283
    const v0, 0x7f0a102b

    .line 286
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 289
    move-result-object v0

    .line 290
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 293
    check-cast v0, Landroid/widget/TextView;

    .line 295
    move-object/from16 v24, v0

    .line 297
    const v0, 0x7f0a05e2

    .line 300
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 303
    move-result-object v0

    .line 304
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 307
    check-cast v0, Landroid/widget/Spinner;

    .line 309
    move-object/from16 v25, v0

    move-object/from16 v25, v0

    .line 311
    const v0, 0x7f0a0dd6

    .line 314
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 317
    move-result-object v0

    .line 318
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 321
    check-cast v0, Landroid/widget/RadioButton;

    .line 323
    move-object/from16 v26, v0

    .line 325
    const v0, 0x7f0a0dd5

    .line 328
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 331
    move-result-object v0

    .line 332
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 335
    check-cast v0, Landroid/widget/RadioButton;

    .line 337
    move-object/from16 v27, v0

    move-object/from16 v27, v0

    .line 339
    const v0, 0x7f0a0d95

    .line 342
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 345
    move-result-object v0

    .line 346
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 349
    check-cast v0, Landroid/widget/CheckBox;

    .line 351
    move-object/from16 v28, v0

    .line 353
    const v0, 0x7f0a12e8

    .line 356
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 359
    move-result-object v0

    .line 360
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 363
    move-object/from16 v29, v0

    .line 365
    check-cast v29, Landroid/widget/Button;

    .line 367
    const v0, 0x7f0a12f4

    .line 370
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 373
    move-result-object v0

    .line 374
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 377
    move-object/from16 v30, v0

    .line 379
    check-cast v30, Landroid/widget/Button;

    .line 381
    const v0, 0x7f0a0df4

    .line 384
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 387
    move-result-object v0

    .line 388
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 391
    check-cast v0, Landroid/widget/RadioButton;

    .line 393
    move-object/from16 v31, v2

    .line 395
    const v2, 0x7f0a0df5

    .line 398
    invoke-virtual {v11, v2}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 401
    move-result-object v2

    .line 402
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 405
    check-cast v2, Landroid/widget/RadioButton;

    .line 407
    move-object/from16 v32, v3

    move-object/from16 v32, v3

    .line 409
    const v3, 0x7f0a09b4

    .line 412
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 415
    move-result-object v3

    .line 416
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 419
    check-cast v3, Landroid/view/ViewGroup;

    .line 421
    const v3, 0x7f0a09bb

    .line 424
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 427
    move-result-object v3

    .line 428
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 431
    check-cast v3, Landroid/view/ViewGroup;

    .line 433
    move-object/from16 v33, v3

    move-object/from16 v33, v3

    .line 435
    const v3, 0x7f0a09ba

    .line 438
    invoke-virtual {v11, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 441
    move-result-object v3

    .line 442
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 445
    check-cast v3, Lcom/google/android/material/textfield/TextInputLayout;

    .line 447
    move-object/from16 v34, v4

    .line 449
    const v4, 0x7f0a09b9

    .line 452
    invoke-virtual {v11, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 455
    move-result-object v4

    .line 456
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 459
    check-cast v4, Landroid/widget/EditText;

    .line 461
    move-object/from16 v35, v5

    .line 463
    const v5, 0x7f0a06d0

    .line 466
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 469
    move-result-object v5

    .line 470
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 473
    check-cast v5, Landroid/widget/Button;

    .line 475
    move-object/from16 v36, v5

    .line 477
    const v5, 0x7f0a0c6f

    .line 480
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 483
    move-result-object v5

    .line 484
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 487
    check-cast v5, Landroid/widget/Button;

    .line 489
    move-object/from16 v37, v5

    .line 491
    const v5, 0x7f0a06ad

    .line 494
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 497
    move-result-object v5

    .line 498
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 501
    check-cast v5, Landroid/widget/CheckBox;

    .line 503
    move-object/from16 v38, v5

    .line 505
    const v5, 0x7f0a0560

    .line 508
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 511
    move-result-object v5

    .line 512
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 515
    check-cast v5, Landroid/widget/CheckBox;

    .line 517
    move-object/from16 v39, v5

    .line 519
    const v5, 0x7f0a0562

    .line 522
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 525
    move-result-object v5

    .line 526
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 529
    check-cast v5, Landroid/widget/TextView;

    .line 531
    const v5, 0x7f0a09bd

    .line 534
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 537
    move-result-object v5

    .line 538
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 541
    check-cast v5, Landroid/widget/CheckBox;

    .line 543
    move-object/from16 v40, v5

    move-object/from16 v40, v5

    .line 545
    const v5, 0x7f0a09bc

    .line 548
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 551
    move-result-object v5

    .line 552
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 555
    check-cast v5, Landroid/widget/ImageView;

    .line 557
    move-object/from16 v41, v5

    .line 559
    const v5, 0x7f0a09be

    .line 562
    invoke-virtual {v11, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 565
    move-result-object v5

    .line 566
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 569
    check-cast v5, Landroid/view/ViewGroup;

    .line 571
    move-object/from16 v42, v5

    .line 573
    iget v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 575
    move-object/from16 v43, v8

    .line 577
    const/16 v44, 0x0

    .line 579
    const/4 v8, 0x1

    .line 580
    if-nez v5, :cond_256

    .line 582
    move v5, v8

    .line 583
    goto :goto_258

    .line 584
    :cond_256
    move/from16 v5, v44

    .line 586
    :goto_258
    invoke-virtual {v0, v5}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 589
    iget v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 591
    if-ne v5, v8, :cond_262

    .line 593
    move v5, v8

    move v5, v8

    .line 594
    goto :goto_266

    .line 595
    :cond_262
    move/from16 v5, v44

    move/from16 v5, v44

    .line 597
    :goto_266
    invoke-virtual {v2, v5}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 600
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 603
    move-result-object v5

    .line 604
    const v8, 0x7f140d70

    .line 607
    invoke-virtual {v5, v8}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 610
    move-result-object v5

    .line 611
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 614
    move-object/from16 v45, v0

    .line 616
    const/4 v8, 0x1

    .line 617
    new-array v0, v8, [Ljava/lang/Object;

    .line 619
    aput-object v17, v0, v44

    .line 621
    invoke-static {v0, v8}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    .line 624
    move-result-object v0

    .line 625
    invoke-static {v5, v0}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 628
    move-result-object v0

    .line 629
    invoke-virtual {v4, v0}, Landroid/widget/TextView;->setHint(Ljava/lang/CharSequence;)V

    .line 632
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 635
    move-result-object v0

    .line 636
    const v5, 0x7f140d70

    .line 639
    invoke-virtual {v0, v5}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 642
    move-result-object v0

    .line 643
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 646
    new-array v5, v8, [Ljava/lang/Object;

    .line 648
    aput-object v17, v5, v44

    .line 650
    invoke-static {v5, v8}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    .line 653
    move-result-object v5

    .line 654
    invoke-static {v0, v5}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 657
    move-result-object v0

    .line 658
    invoke-virtual {v3, v0}, Lcom/google/android/material/textfield/TextInputLayout;->setHint(Ljava/lang/CharSequence;)V

    .line 661
    new-instance v0, Lw46;

    .line 663
    move v3, v8

    move v3, v8

    .line 664
    const/4 v8, 0x1

    .line 665
    move-object v5, v11

    .line 666
    move v11, v3

    .line 667
    move-object/from16 v3, v33

    .line 669
    move-object/from16 v33, v5

    .line 671
    move-object/from16 v48, v6

    .line 673
    move-object/from16 v17, v12

    .line 675
    move-object/from16 v6, v18

    move-object/from16 v6, v18

    .line 677
    move-object/from16 v51, v19

    .line 679
    move-object/from16 v52, v20

    .line 681
    move-object/from16 v53, v21

    .line 683
    move-object/from16 v54, v24

    move-object/from16 v54, v24

    .line 685
    move-object/from16 v12, v26

    .line 687
    move-object/from16 v46, v32

    .line 689
    move-object/from16 v47, v34

    move-object/from16 v47, v34

    .line 691
    move-object/from16 v49, v35

    .line 693
    move-object/from16 v55, v37

    .line 695
    move-object/from16 v56, v39

    .line 697
    move-object/from16 v57, v40

    .line 699
    move-object/from16 v58, v41

    .line 701
    move-object/from16 v5, v42

    .line 703
    move-object/from16 v50, v43

    move-object/from16 v50, v43

    .line 705
    move-object/from16 v34, v4

    .line 707
    move-object/from16 v20, v9

    .line 709
    move-object/from16 v19, v10

    .line 711
    move-object/from16 v18, v13

    .line 713
    move-object/from16 v32, v14

    .line 715
    move-object/from16 v13, v25

    .line 717
    move-object/from16 v10, v27

    move-object/from16 v10, v27

    .line 719
    move-object/from16 v9, v28

    .line 721
    move-object/from16 v4, v36

    .line 723
    move-object v14, v2

    .line 724
    move-object/from16 v2, v31

    .line 726
    move-object/from16 v31, v15

    .line 728
    move-object/from16 v15, v45

    .line 730
    invoke-direct/range {v0 .. v8}, Lw46;-><init>(Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;Landroid/widget/Button;Landroid/view/ViewGroup;Landroid/widget/Button;Landroid/view/ViewGroup;Lcom/google/android/material/floatingactionbutton/FloatingActionButton;Landroid/widget/SeekBar;I)V

    .line 733
    invoke-virtual {v15, v0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 736
    new-instance v0, Lw46;

    .line 738
    const/4 v8, 0x0

    .line 739
    move-object/from16 v1, p0

    .line 741
    invoke-direct/range {v0 .. v8}, Lw46;-><init>(Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;Landroid/widget/Button;Landroid/view/ViewGroup;Landroid/widget/Button;Landroid/view/ViewGroup;Lcom/google/android/material/floatingactionbutton/FloatingActionButton;Landroid/widget/SeekBar;I)V

    .line 744
    move-object v8, v6

    move-object v8, v6

    .line 745
    move-object v6, v2

    .line 746
    move-object v2, v8

    .line 747
    move-object v8, v4

    .line 748
    invoke-virtual {v14, v0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 751
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 753
    if-nez v0, :cond_312

    .line 755
    const/4 v0, 0x0

    .line 756
    goto :goto_314

    .line 757
    :cond_312
    const/16 v0, 0x8

    .line 759
    :goto_314
    invoke-virtual {v6, v0}, Landroid/view/View;->setVisibility(I)V

    .line 762
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 764
    if-ne v0, v11, :cond_31d

    .line 766
    const/4 v0, 0x0

    .line 767
    goto :goto_31f

    .line 768
    :cond_31d
    const/16 v0, 0x8

    .line 770
    :goto_31f
    invoke-virtual {v3, v0}, Landroid/view/View;->setVisibility(I)V

    .line 773
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 775
    if-ne v0, v11, :cond_328

    .line 777
    const/4 v0, 0x0

    .line 778
    goto :goto_32a

    .line 779
    :cond_328
    const/16 v0, 0x8

    .line 781
    :goto_32a
    invoke-virtual {v8, v0}, Landroid/view/View;->setVisibility(I)V

    .line 784
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconType:I

    .line 786
    if-nez v0, :cond_333

    .line 788
    const/4 v0, 0x0

    .line 789
    goto :goto_335

    .line 790
    :cond_333
    const/16 v0, 0x8

    .line 792
    :goto_335
    invoke-virtual {v5, v0}, Landroid/view/View;->setVisibility(I)V

    .line 795
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->usePercentForLocation:Z

    .line 797
    xor-int/2addr v0, v11

    .line 798
    invoke-virtual {v12, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 801
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->usePercentForLocation:Z

    .line 803
    invoke-virtual {v10, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 806
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->preventRemoveByDrag:Z

    .line 808
    invoke-virtual {v9, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 811
    const/4 v0, 0x0

    .line 812
    invoke-virtual {v13, v0}, Landroid/view/View;->setVisibility(I)V

    .line 815
    iget v3, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->enableOption:I

    .line 817
    invoke-virtual {v13, v3}, Landroid/widget/AdapterView;->setSelection(I)V

    .line 820
    move-object/from16 v3, v53

    .line 822
    const/16 v4, 0x8

    .line 824
    invoke-virtual {v3, v4}, Landroid/view/View;->setVisibility(I)V

    .line 827
    move-object/from16 v3, v54

    .line 829
    invoke-virtual {v3, v0}, Landroid/view/View;->setVisibility(I)V

    .line 832
    const v0, 0x7f1419b7

    .line 835
    invoke-static {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 838
    move-result-object v0

    .line 839
    iget-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->identifier:Ljava/lang/String;

    .line 841
    new-instance v5, Ljava/lang/StringBuilder;

    .line 843
    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    .line 846
    invoke-virtual {v5, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 849
    const-string v0, ": "

    const-string v0, ": "

    .line 851
    invoke-virtual {v5, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 854
    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 857
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 860
    move-result-object v0

    .line 861
    invoke-virtual {v3, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 864
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->fixedLocation:Z

    .line 866
    move-object/from16 v3, v38

    .line 868
    invoke-virtual {v3, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 871
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->drawOverSystemApps:Z

    .line 873
    move-object/from16 v4, v56

    .line 875
    invoke-virtual {v4, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 878
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconText:Ljava/lang/String;

    .line 880
    move-object/from16 v5, v34

    .line 882
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 885
    new-instance v0, Lp30;

    .line 887
    const/4 v11, 0x2

    .line 888
    invoke-direct {v0, v1, v2, v7, v11}, Lp30;-><init>(Ljava/lang/Object;Landroid/view/View;Ljava/lang/Object;I)V

    .line 891
    invoke-virtual {v5, v0}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 894
    const v0, 0x7f0a052d

    .line 897
    move-object/from16 v11, v33

    .line 899
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 902
    move-result-object v0

    .line 903
    check-cast v0, Landroid/widget/Spinner;

    .line 905
    const/16 v3, 0x8

    .line 907
    if-eqz v0, :cond_3af

    .line 909
    invoke-virtual {v0, v3}, Landroid/view/View;->setVisibility(I)V

    .line 912
    :cond_3af
    const v0, 0x7f0a0ac0

    .line 915
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 918
    move-result-object v0

    .line 919
    check-cast v0, Landroid/widget/CheckBox;

    .line 921
    if-eqz v0, :cond_3bd

    .line 923
    invoke-virtual {v0, v3}, Landroid/view/View;->setVisibility(I)V

    .line 926
    :cond_3bd
    const v0, 0x7f0a0ac1

    .line 929
    invoke-virtual {v11, v0}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 932
    move-result-object v0

    .line 933
    if-eqz v0, :cond_3c9

    .line 935
    invoke-virtual {v0, v3}, Landroid/view/View;->setVisibility(I)V

    .line 938
    :cond_3c9
    new-instance v21, Lx46;

    .line 940
    const/16 v28, 0x0

    .line 942
    move-object/from16 v25, v10

    .line 944
    move-object/from16 v24, v12

    .line 946
    move-object/from16 v26, v29

    move-object/from16 v26, v29

    .line 948
    move-object/from16 v27, v30

    move-object/from16 v27, v30

    .line 950
    invoke-direct/range {v21 .. v28}, Lx46;-><init>(Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/Button;Landroid/widget/Button;I)V

    .line 953
    move-object/from16 v39, v4

    move-object/from16 v39, v4

    .line 955
    move-object/from16 v34, v5

    move-object/from16 v34, v5

    .line 957
    move-object/from16 v28, v9

    move-object/from16 v28, v9

    .line 959
    move-object/from16 v5, v21

    .line 961
    move-object/from16 v12, v23

    .line 963
    move-object/from16 v0, v24

    .line 965
    move-object/from16 v9, v25

    .line 967
    move-object/from16 v3, v26

    move-object/from16 v3, v26

    .line 969
    move-object/from16 v4, v27

    .line 971
    move-object/from16 v10, v52

    .line 973
    move-object/from16 v25, v13

    move-object/from16 v25, v13

    .line 975
    move-object/from16 v13, v22

    .line 977
    invoke-virtual {v10, v5}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 980
    const v5, 0x7f140bf5

    .line 983
    invoke-virtual {v10, v5}, Landroid/widget/TextView;->setText(I)V

    .line 986
    iget-boolean v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 988
    invoke-virtual {v13, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 991
    iget-boolean v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 993
    invoke-virtual {v12, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 996
    iget-boolean v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 998
    invoke-virtual {v0, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 1001
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 1003
    invoke-virtual {v9, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 1006
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 1008
    invoke-virtual {v3, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 1011
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 1013
    invoke-virtual {v4, v0}, Landroid/view/View;->setEnabled(Z)V

    .line 1016
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->xVarName:Ljava/lang/String;

    .line 1018
    if-eqz v0, :cond_42d

    .line 1020
    invoke-virtual {v13, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1023
    goto :goto_436

    .line 1024
    :cond_42d
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->xLocation:I

    .line 1026
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1029
    move-result-object v0

    .line 1030
    invoke-virtual {v13, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1033
    :goto_436
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->yVarName:Ljava/lang/String;

    .line 1035
    if-eqz v0, :cond_43e

    .line 1037
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1040
    goto :goto_447

    .line 1041
    :cond_43e
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->yLocation:I

    .line 1043
    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1046
    move-result-object v0

    .line 1047
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1050
    :goto_447
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->updateLocation:Z

    .line 1052
    invoke-virtual {v10, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1055
    new-instance v0, Lqnc;

    .line 1057
    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    .line 1060
    new-instance v5, Lj70;

    .line 1062
    move-object/from16 v27, v9

    .line 1064
    const/4 v9, 0x4

    .line 1065
    invoke-direct {v5, v9, v0, v13}, Lj70;-><init>(ILqnc;Landroid/widget/EditText;)V

    .line 1068
    invoke-virtual {v13, v5}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 1071
    new-instance v5, Lqnc;

    .line 1073
    invoke-direct {v5}, Ljava/lang/Object;-><init>()V

    .line 1076
    new-instance v9, Lj70;

    .line 1078
    move-object/from16 v52, v10

    move-object/from16 v52, v10

    .line 1080
    const/4 v10, 0x5

    .line 1081
    invoke-direct {v9, v10, v5, v12}, Lj70;-><init>(ILqnc;Landroid/widget/EditText;)V

    .line 1084
    invoke-virtual {v12, v9}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 1087
    new-instance v9, Lg70;

    .line 1089
    invoke-direct {v9, v10, v0, v13}, Lg70;-><init>(ILqnc;Landroid/widget/EditText;)V

    .line 1092
    new-instance v0, Lva3;

    .line 1094
    const/16 v10, 0x1d

    .line 1096
    invoke-direct {v0, v10, v1, v9}, Lva3;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 1099
    invoke-virtual {v3, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1102
    new-instance v0, Lg70;

    .line 1104
    const/4 v9, 0x6

    .line 1105
    invoke-direct {v0, v9, v5, v12}, Lg70;-><init>(ILqnc;Landroid/widget/EditText;)V

    .line 1108
    new-instance v3, Ly46;

    .line 1110
    const/4 v5, 0x0

    .line 1111
    invoke-direct {v3, v5, v1, v0}, Ly46;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 1114
    invoke-virtual {v4, v3}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1117
    new-instance v0, Ljava/lang/ref/WeakReference;

    .line 1119
    invoke-direct {v0, v2}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 1122
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->fabRef:Ljava/lang/ref/WeakReference;

    .line 1124
    new-instance v0, Ljava/lang/ref/WeakReference;

    .line 1126
    invoke-direct {v0, v7}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 1129
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->paddingSeekBarRef:Ljava/lang/ref/WeakReference;

    .line 1131
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->size:I

    .line 1133
    if-nez v0, :cond_4a0

    .line 1135
    const/4 v3, 0x1

    .line 1136
    goto :goto_4a1

    .line 1137
    :cond_4a0
    const/4 v3, 0x0

    .line 1138
    :goto_4a1
    iput-boolean v3, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->normalSizeSelected:Z

    .line 1140
    if-nez v0, :cond_4b2

    .line 1142
    move-object/from16 v10, v48

    .line 1144
    const/4 v3, 0x1

    .line 1145
    invoke-virtual {v10, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1148
    const/4 v0, 0x0

    .line 1149
    invoke-virtual {v2, v0}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setSize(I)V

    .line 1152
    move-object/from16 v0, v49

    .line 1154
    goto :goto_4bd

    .line 1155
    :cond_4b2
    move-object/from16 v10, v48

    .line 1157
    move-object/from16 v0, v49

    .line 1159
    const/4 v3, 0x1

    .line 1160
    invoke-virtual {v0, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1163
    invoke-virtual {v2, v3}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setSize(I)V

    .line 1166
    :goto_4bd
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->transparentBackground:Z

    .line 1168
    move-object/from16 v4, v51

    move-object/from16 v4, v51

    .line 1170
    invoke-virtual {v4, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1173
    new-instance v3, Lze0;

    .line 1175
    const/16 v5, 0xd

    .line 1177
    invoke-direct {v3, v5, v2, v1}, Lze0;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 1180
    invoke-virtual {v4, v3}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1183
    move-object v3, v4

    .line 1184
    new-instance v4, Lql;

    .line 1186
    move-object/from16 v5, v32

    .line 1188
    const/16 v9, 0x8

    .line 1190
    invoke-direct {v4, v5, v1, v8, v9}, Lql;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1193
    invoke-virtual {v4}, Lql;->invoke()Ljava/lang/Object;

    .line 1196
    move-object/from16 v49, v0

    move-object/from16 v49, v0

    .line 1198
    new-instance v0, Lgs5;

    .line 1200
    const/4 v5, 0x1

    .line 1201
    move-object/from16 v24, v7

    .line 1203
    move-object/from16 v33, v11

    .line 1205
    move-object/from16 v26, v12

    move-object/from16 v26, v12

    .line 1207
    move-object/from16 v9, v32

    .line 1209
    move-object/from16 v12, v34

    .line 1211
    move-object/from16 v11, v39

    .line 1213
    move-object/from16 v7, v49

    .line 1215
    invoke-direct/range {v0 .. v5}, Lgs5;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1218
    invoke-virtual {v9, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1221
    new-instance v0, Lgs5;

    .line 1223
    const/4 v5, 0x2

    .line 1224
    move-object/from16 v1, p0

    .line 1226
    move-object v9, v3

    .line 1227
    move-object/from16 v3, v24

    .line 1229
    invoke-direct/range {v0 .. v5}, Lgs5;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1232
    invoke-virtual {v8, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1235
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintEnabled:Z

    .line 1237
    move-object/from16 v5, v57

    move-object/from16 v5, v57

    .line 1239
    invoke-virtual {v5, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1242
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 1245
    move-result-object v0

    .line 1246
    iget-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintColorVariable:Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;

    .line 1248
    iget v8, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintColor:I

    .line 1250
    move-object/from16 v24, v13

    .line 1252
    const/4 v13, 0x0

    .line 1253
    invoke-static {v0, v4, v8, v13}, Lcom/arlosoft/macrodroid/variables/a;->e(Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)I

    .line 1256
    move-result v0

    .line 1257
    invoke-static {v0}, Landroid/content/res/ColorStateList;->valueOf(I)Landroid/content/res/ColorStateList;

    .line 1260
    move-result-object v0

    .line 1261
    move-object/from16 v4, v58

    .line 1263
    invoke-virtual {v4, v0}, Landroid/widget/ImageView;->setImageTintList(Landroid/content/res/ColorStateList;)V

    .line 1266
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintEnabled:Z

    .line 1268
    if-eqz v0, :cond_52f

    .line 1270
    const/4 v8, 0x0

    .line 1271
    goto :goto_530

    .line 1272
    :cond_52f
    const/4 v8, 0x4

    .line 1273
    :goto_530
    invoke-virtual {v4, v8}, Landroid/widget/ImageView;->setVisibility(I)V

    .line 1276
    new-instance v0, Lng;

    .line 1278
    const/4 v8, 0x5

    .line 1279
    invoke-direct {v0, v1, v4, v2, v8}, Lng;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1282
    invoke-virtual {v5, v0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1285
    new-instance v0, Lto4;

    .line 1287
    const/16 v8, 0x15

    .line 1289
    invoke-direct {v0, v1, v4, v2, v8}, Lto4;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1292
    invoke-virtual {v4, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1295
    const/16 v0, 0x1c

    .line 1297
    invoke-virtual {v3, v0}, Landroid/widget/ProgressBar;->setMax(I)V

    .line 1300
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->padding:I

    .line 1302
    invoke-virtual {v3, v0}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 1305
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->padding:I

    .line 1307
    move-object v8, v14

    .line 1308
    int-to-double v13, v0

    .line 1309
    const-wide v29, 0x3fd1eb851eb851ecL    # 0.28

    .line 1314
    div-double v13, v13, v29

    .line 1316
    invoke-static {v13, v14}, Ljava/lang/Math;->round(D)J

    .line 1319
    move-result-wide v13

    .line 1320
    new-instance v0, Ljava/lang/StringBuilder;

    .line 1322
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 1325
    invoke-virtual {v0, v13, v14}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 1328
    const-string v13, "%"

    const-string v13, "%"

    .line 1330
    invoke-virtual {v0, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1333
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1336
    move-result-object v0

    .line 1337
    move-object/from16 v14, v47

    .line 1339
    invoke-virtual {v14, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1342
    new-instance v0, Lz46;

    .line 1344
    invoke-direct {v0, v14, v1, v2}, Lz46;-><init>(Landroid/widget/TextView;Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;Lcom/google/android/material/floatingactionbutton/FloatingActionButton;)V

    .line 1347
    invoke-virtual {v3, v0}, Landroid/widget/SeekBar;->setOnSeekBarChangeListener(Landroid/widget/SeekBar$OnSeekBarChangeListener;)V

    .line 1350
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->alpha:I

    .line 1352
    move-object/from16 v14, v31

    .line 1354
    invoke-virtual {v14, v0}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 1357
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->alpha:I

    .line 1359
    move-object/from16 v29, v8

    .line 1361
    move-object/from16 v8, v46

    move-object/from16 v8, v46

    .line 1363
    invoke-static {v0, v8, v13}, Ll60;->z(ILandroid/widget/TextView;Ljava/lang/String;)V

    .line 1366
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->alpha:I

    .line 1368
    int-to-float v0, v0

    .line 1369
    const/high16 v30, 0x42c80000    # 100.0f

    .line 1371
    div-float v0, v0, v30

    .line 1373
    move-object/from16 v41, v4

    move-object/from16 v41, v4

    .line 1375
    move-object/from16 v4, v20

    .line 1377
    invoke-virtual {v4, v0}, Landroid/view/View;->setAlpha(F)V

    .line 1380
    move-object/from16 v0, v50

    .line 1382
    const/16 v4, 0x8

    .line 1384
    invoke-virtual {v0, v4}, Landroid/view/View;->setVisibility(I)V

    .line 1387
    new-instance v0, La56;

    .line 1389
    const/4 v4, 0x0

    .line 1390
    invoke-direct {v0, v8, v2, v4}, La56;-><init>(Landroid/widget/TextView;Lcom/google/android/material/floatingactionbutton/FloatingActionButton;I)V

    .line 1393
    invoke-virtual {v14, v0}, Landroid/widget/SeekBar;->setOnSeekBarChangeListener(Landroid/widget/SeekBar$OnSeekBarChangeListener;)V

    .line 1396
    new-instance v0, Lng;

    .line 1398
    const/4 v4, 0x6

    .line 1399
    invoke-direct {v0, v2, v1, v3, v4}, Lng;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1402
    invoke-virtual {v7, v0}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1405
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->transparentBackground:Z

    .line 1407
    if-eqz v0, :cond_5c4

    .line 1409
    move-object/from16 v40, v5

    .line 1411
    move-object/from16 v39, v11

    .line 1413
    const/4 v0, 0x0

    .line 1414
    goto :goto_5d5

    .line 1415
    :cond_5c4
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 1418
    move-result-object v0

    .line 1419
    iget-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconBgColorVariable:Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;

    .line 1421
    move-object/from16 v40, v5

    .line 1423
    iget v5, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconBgColor:I

    .line 1425
    move-object/from16 v39, v11

    .line 1427
    const/4 v11, 0x0

    .line 1428
    invoke-static {v0, v4, v5, v11}, Lcom/arlosoft/macrodroid/variables/a;->e(Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)I

    .line 1431
    move-result v0

    .line 1432
    :goto_5d5
    invoke-static {v0}, Landroid/content/res/ColorStateList;->valueOf(I)Landroid/content/res/ColorStateList;

    .line 1435
    move-result-object v0

    .line 1436
    invoke-virtual {v2, v0}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setBackgroundTintList(Landroid/content/res/ColorStateList;)V

    .line 1439
    new-instance v0, Ln30;

    .line 1441
    const/4 v4, 0x3

    .line 1442
    move-object/from16 v5, v19

    move-object/from16 v5, v19

    .line 1444
    invoke-direct {v0, v4, v5}, Ln30;-><init>(ILandroid/app/Activity;)V

    .line 1447
    invoke-virtual {v6, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1450
    iget-boolean v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->isInitialised:Z

    .line 1452
    if-nez v0, :cond_6cc

    .line 1454
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->Q0()I

    .line 1457
    move-result v0

    .line 1458
    if-nez v0, :cond_5f5

    .line 1460
    const/4 v0, 0x1

    .line 1461
    goto :goto_5f6

    .line 1462
    :cond_5f5
    const/4 v0, 0x0

    .line 1463
    :goto_5f6
    invoke-virtual {v15, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1466
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->Q0()I

    .line 1469
    move-result v0

    .line 1470
    const/4 v11, 0x1

    .line 1471
    if-ne v0, v11, :cond_604

    .line 1473
    move v0, v11

    .line 1474
    :goto_601
    move-object/from16 v4, v29

    .line 1476
    goto :goto_606

    .line 1477
    :cond_604
    const/4 v0, 0x0

    .line 1478
    goto :goto_601

    .line 1479
    :goto_606
    invoke-virtual {v4, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1482
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->M0()Ljava/lang/String;

    .line 1485
    move-result-object v0

    .line 1486
    invoke-virtual {v12, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1489
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->i1()Z

    .line 1492
    move-result v0

    .line 1493
    invoke-virtual {v9, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1496
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->g1()I

    .line 1499
    move-result v0

    .line 1500
    if-ne v0, v11, :cond_61f

    .line 1502
    const/4 v0, 0x1

    .line 1503
    goto :goto_620

    .line 1504
    :cond_61f
    const/4 v0, 0x0

    .line 1505
    :goto_620
    invoke-virtual {v7, v0}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1508
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->b1()I

    .line 1511
    move-result v0

    .line 1512
    invoke-virtual {v3, v0}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 1515
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->G0()I

    .line 1518
    move-result v0

    .line 1519
    invoke-virtual {v14, v0}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 1522
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->G0()I

    .line 1525
    move-result v0

    .line 1526
    new-instance v4, Ljava/lang/StringBuilder;

    .line 1528
    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    .line 1531
    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 1534
    invoke-virtual {v4, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1537
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1540
    move-result-object v0

    .line 1541
    invoke-virtual {v8, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1544
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->g1()I

    .line 1547
    move-result v0

    .line 1548
    if-nez v0, :cond_656

    .line 1550
    const/4 v11, 0x1

    .line 1551
    invoke-virtual {v10, v11}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1554
    const/4 v0, 0x0

    .line 1555
    invoke-virtual {v2, v0}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setSize(I)V

    .line 1558
    goto :goto_65e

    .line 1559
    :cond_656
    const/4 v0, 0x0

    .line 1560
    const/4 v11, 0x1

    .line 1561
    invoke-virtual {v7, v11}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1564
    invoke-virtual {v2, v11}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setSize(I)V

    .line 1567
    :goto_65e
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->i1()Z

    .line 1570
    move-result v4

    .line 1571
    if-eqz v4, :cond_666

    .line 1573
    move v8, v0

    .line 1574
    goto :goto_66a

    .line 1575
    :cond_666
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->H0()I

    .line 1578
    move-result v8

    .line 1579
    :goto_66a
    invoke-static {v8}, Landroid/content/res/ColorStateList;->valueOf(I)Landroid/content/res/ColorStateList;

    .line 1582
    move-result-object v4

    .line 1583
    invoke-virtual {v2, v4}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setBackgroundTintList(Landroid/content/res/ColorStateList;)V

    .line 1586
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->H0()I

    .line 1589
    move-result v4

    .line 1590
    iput v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconBgColor:I

    .line 1592
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->b1()I

    .line 1595
    move-result v4

    .line 1596
    iget v6, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->workingIconType:I

    .line 1598
    invoke-virtual {v1, v2, v4, v6}, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->r0(Lcom/google/android/material/floatingactionbutton/FloatingActionButton;II)V

    .line 1601
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->W0()Ljava/lang/String;

    .line 1604
    move-result-object v4

    .line 1605
    iput-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->imageUri:Ljava/lang/String;

    .line 1607
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->S0()Ljava/lang/String;

    .line 1610
    move-result-object v4

    .line 1611
    iput-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->imagePackageName:Ljava/lang/String;

    .line 1613
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->U0()Ljava/lang/String;

    .line 1616
    move-result-object v4

    .line 1617
    iput-object v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->imageResourceName:Ljava/lang/String;

    .line 1619
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->T0()I

    .line 1622
    move-result v4

    .line 1623
    iput v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->imageResourceId:I

    .line 1625
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->I0()Z

    .line 1628
    move-result v4

    .line 1629
    iput-boolean v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->drawOverSystemApps:Z

    .line 1631
    move-object/from16 v11, v39

    .line 1633
    invoke-virtual {v11, v4}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1636
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->P0()Z

    .line 1639
    move-result v4

    .line 1640
    iput-boolean v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintEnabled:Z

    .line 1642
    invoke-virtual/range {p1 .. p1}, Lcom/arlosoft/macrodroid/triggers/FloatingButtonTrigger;->O0()I

    .line 1645
    move-result v4

    .line 1646
    iput v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintColor:I

    .line 1648
    iget-boolean v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintEnabled:Z

    .line 1650
    move-object/from16 v6, v40

    .line 1652
    invoke-virtual {v6, v4}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1655
    iget v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintColor:I

    .line 1657
    invoke-static {v4}, Landroid/content/res/ColorStateList;->valueOf(I)Landroid/content/res/ColorStateList;

    .line 1660
    move-result-object v4

    .line 1661
    move-object/from16 v6, v41

    .line 1663
    invoke-virtual {v6, v4}, Landroid/widget/ImageView;->setImageTintList(Landroid/content/res/ColorStateList;)V

    .line 1666
    iget-boolean v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->iconTintEnabled:Z

    .line 1668
    if-eqz v4, :cond_6c7

    .line 1670
    move v8, v0

    .line 1671
    goto :goto_6c8

    .line 1672
    :cond_6c7
    const/4 v8, 0x4

    .line 1673
    :goto_6c8
    invoke-virtual {v6, v8}, Landroid/widget/ImageView;->setVisibility(I)V

    .line 1676
    goto :goto_6ce

    .line 1677
    :cond_6cc
    move-object/from16 v11, v39

    .line 1679
    :goto_6ce
    iget v0, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->padding:I

    .line 1681
    iget v4, v1, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->workingIconType:I

    .line 1683
    invoke-virtual {v1, v2, v0, v4}, Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;->r0(Lcom/google/android/material/floatingactionbutton/FloatingActionButton;II)V

    .line 1686
    new-instance v0, Lso4;

    .line 1688
    const/16 v2, 0x17

    .line 1690
    invoke-direct {v0, v12, v2}, Lso4;-><init>(Landroid/widget/EditText;I)V

    .line 1693
    new-instance v2, Lto4;

    .line 1695
    const/16 v4, 0x14

    .line 1697
    invoke-direct {v2, v5, v0, v1, v4}, Lto4;-><init>(Landroid/app/Activity;Ltr9;Lcom/arlosoft/macrodroid/common/SelectableItem;I)V

    .line 1700
    move-object/from16 v5, v55

    .line 1702
    invoke-virtual {v5, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1705
    new-instance v0, Llz1;

    .line 1707
    move-object v2, v1

    .line 1708
    move-object v5, v3

    move-object v5, v3

    .line 1709
    move-object v7, v9

    .line 1710
    move-object v6, v10

    .line 1711
    move-object/from16 v16, v11

    .line 1713
    move-object v4, v14

    .line 1714
    move-object v11, v15

    .line 1715
    move-object/from16 v59, v17

    .line 1717
    move-object/from16 v60, v18

    move-object/from16 v60, v18

    .line 1719
    move-object/from16 v13, v24

    move-object/from16 v13, v24

    .line 1721
    move-object/from16 v15, v25

    .line 1723
    move-object/from16 v14, v26

    move-object/from16 v14, v26

    .line 1725
    move-object/from16 v9, v27

    .line 1727
    move-object/from16 v10, v28

    .line 1729
    move-object/from16 v1, v33

    move-object/from16 v1, v33

    .line 1731
    move-object/from16 v3, v38

    .line 1733
    move-object/from16 v8, v52

    .line 1735
    invoke-direct/range {v0 .. v16}, Llz1;-><init>(Lvf0;Lcom/arlosoft/macrodroid/action/FloatingButtonConfigureAction;Landroid/widget/CheckBox;Landroid/widget/SeekBar;Landroid/widget/SeekBar;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Landroid/widget/RadioButton;Landroid/widget/CheckBox;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/Spinner;Landroid/widget/CheckBox;)V

    .line 1738
    move-object/from16 v2, v59

    .line 1740
    invoke-virtual {v2, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1743
    new-instance v0, Lb45;

    .line 1745
    const/16 v2, 0xb

    .line 1747
    invoke-direct {v0, v1, v2}, Lb45;-><init>(Lvf0;I)V

    .line 1750
    move-object/from16 v2, v60

    .line 1752
    invoke-virtual {v2, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1755
    invoke-virtual {v1}, Landroid/app/Dialog;->show()V

    .line 1758
    return-void
.end method
