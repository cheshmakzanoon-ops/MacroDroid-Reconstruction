.method public final z0(Ljava/util/ArrayList;I)V
    .locals 47

    .line 1
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 3
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 6
    move-result-object v0

    .line 7
    const v2, 0x7f150360

    .line 10
    const v4, 0x7f0d0801

    .line 13
    invoke-static {v0, v2, v4}, Lbl5;->h(Landroid/app/Activity;II)Lvf0;

    .line 16
    move-result-object v2

    .line 17
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_variable:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 19
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 22
    move-result-object v4

    .line 23
    invoke-virtual {v2, v4}, Lvf0;->setTitle(Ljava/lang/CharSequence;)V

    .line 26
    new-instance v4, Landroid/view/WindowManager$LayoutParams;

    .line 28
    invoke-direct {v4}, Landroid/view/WindowManager$LayoutParams;-><init>()V

    .line 31
    invoke-static {v2, v4}, Lbl5;->A(Lvf0;Landroid/view/WindowManager$LayoutParams;)V

    .line 34
    const/4 v5, -0x1

    .line 35
    iput v5, v4, Landroid/view/WindowManager$LayoutParams;->width:I

    .line 37
    invoke-virtual {v2}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    .line 40
    move-result-object v5

    .line 41
    invoke-virtual {v5, v4}, Landroid/view/Window;->setAttributes(Landroid/view/WindowManager$LayoutParams;)V

    .line 44
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_otherValueToCompare:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 46
    iput-object v4, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->workingOtherVarToCompare:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 48
    iget-object v4, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->compareVarDictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 50
    iput-object v4, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->workingCompareVarDictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 52
    const v4, 0x7f0a121f

    .line 55
    invoke-virtual {v2, v4}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 58
    move-result-object v4

    .line 59
    check-cast v4, Landroid/widget/Button;

    .line 61
    const v5, 0x7f0a121e

    .line 64
    invoke-virtual {v2, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 67
    move-result-object v5

    .line 68
    check-cast v5, Landroid/widget/Button;

    .line 70
    const v6, 0x7f0a1225

    .line 73
    invoke-virtual {v2, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 76
    move-result-object v6

    .line 77
    check-cast v6, Landroid/widget/RadioGroup;

    .line 79
    const v7, 0x7f0a122b

    .line 82
    invoke-virtual {v2, v7}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 85
    move-result-object v7

    .line 86
    check-cast v7, Landroid/widget/RadioButton;

    .line 88
    const v8, 0x7f0a1227

    .line 91
    invoke-virtual {v2, v8}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 94
    move-result-object v8

    .line 95
    check-cast v8, Landroid/widget/RadioButton;

    .line 97
    const v9, 0x7f0a1220

    .line 100
    invoke-virtual {v2, v9}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 103
    move-result-object v9

    .line 104
    check-cast v9, Landroid/view/ViewGroup;

    .line 106
    const v10, 0x7f0a1226

    .line 109
    invoke-virtual {v2, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 112
    move-result-object v10

    .line 113
    check-cast v10, Landroid/widget/RadioButton;

    .line 115
    const v11, 0x7f0a1229

    .line 118
    invoke-virtual {v2, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 121
    move-result-object v11

    .line 122
    check-cast v11, Landroid/widget/RadioButton;

    .line 124
    const v12, 0x7f0a1228

    .line 127
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 130
    move-result-object v12

    .line 131
    check-cast v12, Landroid/widget/RadioButton;

    .line 133
    const v13, 0x7f0a122a

    .line 136
    invoke-virtual {v2, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 139
    move-result-object v13

    .line 140
    check-cast v13, Landroid/widget/RadioButton;

    .line 142
    const v14, 0x7f0a1221

    .line 145
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 148
    move-result-object v14

    .line 149
    check-cast v14, Landroid/widget/EditText;

    .line 151
    const v15, 0x7f0a1222

    .line 154
    invoke-virtual {v2, v15}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 157
    move-result-object v15

    .line 158
    check-cast v15, Landroid/widget/RadioButton;

    .line 160
    move-object/from16 v16, v5

    move-object/from16 v16, v5

    .line 162
    const v5, 0x7f0a1223

    .line 165
    invoke-virtual {v2, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 168
    move-result-object v5

    .line 169
    check-cast v5, Landroid/widget/RadioButton;

    .line 171
    move-object/from16 v17, v5

    move-object/from16 v17, v5

    .line 173
    const v5, 0x7f0a1224

    .line 176
    invoke-virtual {v2, v5}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 179
    move-result-object v5

    .line 180
    check-cast v5, Landroid/widget/Spinner;

    .line 182
    move-object/from16 v18, v10

    .line 184
    const v10, 0x7f0a122f

    .line 187
    invoke-virtual {v2, v10}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 190
    move-result-object v10

    .line 191
    check-cast v10, Landroid/widget/RadioGroup;

    .line 193
    move-object/from16 v19, v13

    .line 195
    const v13, 0x7f0a1231

    .line 198
    invoke-virtual {v2, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 201
    move-result-object v13

    .line 202
    check-cast v13, Landroid/widget/RadioButton;

    .line 204
    move-object/from16 v20, v11

    .line 206
    const v11, 0x7f0a1233

    .line 209
    invoke-virtual {v2, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 212
    move-result-object v11

    .line 213
    check-cast v11, Landroid/widget/RadioButton;

    .line 215
    move-object/from16 v21, v12

    move-object/from16 v21, v12

    .line 217
    const v12, 0x7f0a1230

    .line 220
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 223
    move-result-object v12

    .line 224
    check-cast v12, Landroid/widget/RadioButton;

    .line 226
    move-object/from16 v22, v14

    .line 228
    const v14, 0x7f0a1232

    .line 231
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 234
    move-result-object v14

    .line 235
    check-cast v14, Landroid/widget/RadioButton;

    .line 237
    move-object/from16 v23, v14

    .line 239
    const v14, 0x7f0a122d

    .line 242
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 245
    move-result-object v14

    .line 246
    check-cast v14, Landroid/widget/EditText;

    .line 248
    move-object/from16 v24, v14

    .line 250
    const v14, 0x7f0a122c

    .line 253
    invoke-virtual {v2, v14}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 256
    move-result-object v14

    .line 257
    check-cast v14, Landroid/widget/LinearLayout;

    .line 259
    move-object/from16 v25, v12

    .line 261
    const v12, 0x7f0a122e

    .line 264
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 267
    move-result-object v12

    .line 268
    check-cast v12, Landroid/widget/Button;

    .line 270
    move-object/from16 v26, v12

    .line 272
    const v12, 0x7f0a1234

    .line 275
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 278
    move-result-object v12

    .line 279
    check-cast v12, Landroid/widget/TextView;

    .line 281
    move-object/from16 v27, v11

    .line 283
    const v11, 0x7f0a05db

    .line 286
    invoke-virtual {v2, v11}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 289
    move-result-object v11

    .line 290
    check-cast v11, Landroid/widget/CheckBox;

    .line 292
    move-object/from16 v28, v13

    .line 294
    const v13, 0x7f0a09cd

    .line 297
    invoke-virtual {v2, v13}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 300
    move-result-object v13

    .line 301
    check-cast v13, Landroid/widget/CheckBox;

    .line 303
    move-object/from16 v29, v6

    .line 305
    const v6, 0x7f0a0641

    .line 308
    invoke-virtual {v2, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 311
    move-result-object v6

    .line 312
    check-cast v6, Landroid/widget/RadioButton;

    .line 314
    move-object/from16 v30, v6

    move-object/from16 v30, v6

    .line 316
    const v6, 0x7f0a063e

    .line 319
    invoke-virtual {v2, v6}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 322
    move-result-object v6

    .line 323
    check-cast v6, Landroid/widget/EditText;

    .line 325
    const v3, 0x7f0a0640

    .line 328
    invoke-virtual {v2, v3}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 331
    move-result-object v3

    .line 332
    check-cast v3, Landroid/widget/Button;

    .line 334
    move-object/from16 v31, v12

    .line 336
    const v12, 0x7f0a063f

    .line 339
    invoke-virtual {v2, v12}, Lvf0;->findViewById(I)Landroid/view/View;

    .line 342
    move-result-object v12

    .line 343
    check-cast v12, Landroid/widget/LinearLayout;

    .line 345
    move-object/from16 v32, v2

    .line 347
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllVariables()Ljava/util/ArrayList;

    .line 350
    move-result-object v2

    .line 351
    invoke-interface {v2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 354
    move-result-object v33

    .line 355
    :goto_16c
    invoke-interface/range {v33 .. v33}, Ljava/util/Iterator;->hasNext()Z

    .line 358
    move-result v34

    .line 359
    move-object/from16 v35, v14

    .line 361
    if-eqz v34, :cond_1a2

    .line 363
    invoke-interface/range {v33 .. v33}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 366
    move-result-object v34

    .line 367
    check-cast v34, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 369
    invoke-virtual/range {v34 .. v34}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->N()I

    .line 372
    move-result v14

    .line 373
    move-object/from16 v37, v8

    .line 375
    const/4 v8, 0x3

    .line 376
    if-eq v14, v8, :cond_18a

    .line 378
    invoke-virtual/range {v34 .. v34}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->N()I

    .line 381
    move-result v8

    .line 382
    const/4 v14, 0x1

    .line 383
    if-ne v8, v14, :cond_19a

    .line 385
    :cond_18a
    invoke-virtual/range {v34 .. v34}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 388
    move-result-object v8

    .line 389
    iget-object v14, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_variable:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 391
    invoke-virtual {v14}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 394
    move-result-object v14

    .line 395
    invoke-virtual {v8, v14}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 398
    move-result v8

    .line 399
    if-eqz v8, :cond_19d

    .line 401
    :cond_19a
    invoke-interface/range {v33 .. v33}, Ljava/util/Iterator;->remove()V

    .line 404
    :cond_19d
    move-object/from16 v14, v35

    .line 406
    move-object/from16 v8, v37

    .line 408
    goto :goto_16c

    .line 409
    :cond_1a2
    move-object/from16 v37, v8

    .line 411
    invoke-interface {v2}, Ljava/util/List;->size()I

    .line 414
    move-result v8

    .line 415
    const/4 v14, 0x0

    .line 416
    if-lez v8, :cond_20b

    .line 418
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_otherValueToCompare:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 420
    if-nez v8, :cond_1bd

    .line 422
    invoke-interface {v2}, Ljava/util/List;->size()I

    .line 425
    move-result v8

    .line 426
    if-lez v8, :cond_1bd

    .line 428
    invoke-interface {v2, v14}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 431
    move-result-object v8

    .line 432
    check-cast v8, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 434
    iput-object v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_otherValueToCompare:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 436
    :cond_1bd
    invoke-interface {v2}, Ljava/util/List;->size()I

    .line 439
    move-result v8

    .line 440
    new-array v8, v8, [Ljava/lang/String;

    .line 442
    move-object/from16 v34, v7

    move-object/from16 v34, v7

    .line 444
    move-object/from16 v38, v10

    .line 446
    move v7, v14

    .line 447
    :goto_1ca
    invoke-interface {v2}, Ljava/util/List;->size()I

    .line 450
    move-result v10

    .line 451
    if-ge v14, v10, :cond_1f2

    .line 453
    invoke-interface {v2, v14}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 456
    move-result-object v10

    .line 457
    check-cast v10, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 459
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 462
    move-result-object v10

    .line 463
    aput-object v10, v8, v14

    .line 465
    move-object/from16 v39, v2

    .line 467
    iget-object v2, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_otherValueToCompare:Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 469
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 472
    move-result-object v2

    .line 473
    invoke-virtual {v10, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 476
    move-result v2

    .line 477
    if-eqz v2, :cond_1eb

    .line 479
    move v7, v14

    .line 480
    :cond_1eb
    add-int/lit8 v14, v14, 0x1

    .line 482
    move-object/from16 v2, v39

    move-object/from16 v2, v39

    .line 484
    goto :goto_1ca

    .line 485
    :cond_1f2
    new-instance v2, Landroid/widget/ArrayAdapter;

    .line 487
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 490
    move-result-object v10

    .line 491
    const v14, 0x7f0d07d7

    .line 494
    invoke-direct {v2, v10, v14, v8}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;I[Ljava/lang/Object;)V

    .line 497
    const v8, 0x7f0d07d2

    .line 500
    invoke-virtual {v2, v8}, Landroid/widget/ArrayAdapter;->setDropDownViewResource(I)V

    .line 503
    invoke-virtual {v5, v2}, Landroid/widget/Spinner;->setAdapter(Landroid/widget/SpinnerAdapter;)V

    .line 506
    invoke-virtual {v5, v7}, Landroid/widget/AdapterView;->setSelection(I)V

    .line 509
    goto :goto_245

    .line 510
    :cond_20b
    move-object/from16 v39, v2

    .line 512
    move-object/from16 v34, v7

    move-object/from16 v34, v7

    .line 514
    move-object/from16 v38, v10

    .line 516
    invoke-interface/range {v39 .. v39}, Ljava/util/List;->size()I

    .line 519
    move-result v2

    .line 520
    if-nez v2, :cond_245

    .line 522
    invoke-virtual/range {v17 .. v17}, Landroid/widget/CompoundButton;->isChecked()Z

    .line 525
    move-result v2

    .line 526
    if-eqz v2, :cond_245

    .line 528
    const/4 v14, 0x1

    .line 529
    invoke-virtual {v15, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 532
    invoke-virtual {v15}, Landroid/widget/CompoundButton;->isChecked()Z

    .line 535
    move-result v2

    .line 536
    invoke-virtual/range {v17 .. v17}, Landroid/widget/CompoundButton;->isChecked()Z

    .line 539
    move-result v7

    .line 540
    invoke-virtual/range {v30 .. v30}, Landroid/widget/CompoundButton;->isChecked()Z

    .line 543
    invoke-virtual/range {v22 .. v22}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    .line 546
    move-result-object v8

    .line 547
    invoke-virtual {v8}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 550
    move-result-object v8

    .line 551
    invoke-virtual {v6}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    .line 554
    move-result-object v10

    .line 555
    invoke-virtual {v10}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 558
    move-result-object v10

    .line 559
    invoke-virtual {v1, v8, v10, v2, v7}, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->K0(Ljava/lang/String;Ljava/lang/String;ZZ)Z

    .line 562
    move-result v2

    .line 563
    invoke-virtual {v4, v2}, Landroid/view/View;->setEnabled(Z)V

    .line 566
    :cond_245
    :goto_245
    iget-object v2, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 568
    invoke-virtual {v6, v2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 571
    new-instance v2, Lkhg;

    .line 573
    const/16 v7, 0x14

    .line 575
    invoke-direct {v2, v6, v7}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 578
    new-instance v7, Lfrf;

    .line 580
    const/16 v8, 0xe

    .line 582
    invoke-direct {v7, v1, v0, v2, v8}, Lfrf;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 585
    invoke-virtual {v3, v7}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 588
    const/16 v2, 0x8

    .line 590
    invoke-virtual {v12, v2}, Landroid/view/View;->setVisibility(I)V

    .line 593
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->enableRegex:Z

    .line 595
    invoke-virtual {v11, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 598
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->checkCase:Z

    .line 600
    const/4 v14, 0x1

    .line 601
    xor-int/2addr v7, v14

    .line 602
    invoke-virtual {v13, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 605
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->enableRegex:Z

    .line 607
    xor-int/2addr v7, v14

    .line 608
    invoke-virtual {v13, v7}, Landroid/view/View;->setEnabled(Z)V

    .line 611
    new-instance v7, Lfc0;

    .line 613
    const/4 v8, 0x5

    .line 614
    invoke-direct {v7, v13, v8}, Lfc0;-><init>(Landroid/widget/CheckBox;I)V

    .line 617
    invoke-virtual {v11, v7}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 620
    if-nez p2, :cond_2c8

    .line 622
    invoke-virtual {v9, v2}, Landroid/view/View;->setVisibility(I)V

    .line 625
    move-object/from16 v10, v38

    .line 627
    invoke-virtual {v10, v2}, Landroid/view/View;->setVisibility(I)V

    .line 630
    invoke-virtual {v4, v14}, Landroid/view/View;->setEnabled(Z)V

    .line 633
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_booleanValue:Z

    .line 635
    move-object/from16 v8, v34

    move-object/from16 v8, v34

    .line 637
    invoke-virtual {v8, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 640
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_booleanValue:Z

    .line 642
    xor-int/2addr v7, v14

    .line 643
    move-object/from16 v9, v37

    .line 645
    invoke-virtual {v9, v7}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 648
    move-object/from16 v7, v35

    move-object/from16 v7, v35

    .line 650
    invoke-virtual {v7, v2}, Landroid/view/View;->setVisibility(I)V

    .line 653
    move-object/from16 v7, v31

    .line 655
    invoke-virtual {v7, v2}, Landroid/view/View;->setVisibility(I)V

    .line 658
    invoke-virtual {v11, v2}, Landroid/view/View;->setVisibility(I)V

    .line 661
    invoke-virtual {v13, v2}, Landroid/view/View;->setVisibility(I)V

    .line 664
    move/from16 v2, p2

    .line 666
    move-object/from16 v34, v0

    .line 668
    move-object/from16 v29, v3

    .line 670
    move-object/from16 v18, v6

    .line 672
    move v6, v14

    .line 673
    move-object/from16 v3, v19

    .line 675
    move-object/from16 v7, v20

    .line 677
    move-object/from16 v10, v22

    .line 679
    move-object/from16 v14, v25

    move-object/from16 v14, v25

    .line 681
    move-object/from16 v9, v28

    move-object/from16 v9, v28

    .line 683
    move-object/from16 v25, v5

    .line 685
    move-object/from16 v5, v21

    .line 687
    goto/16 :goto_44d

    .line 689
    :cond_2c8
    move/from16 v2, p2

    .line 691
    move-object/from16 v8, v34

    .line 693
    move-object/from16 v7, v35

    move-object/from16 v7, v35

    .line 695
    move-object/from16 v10, v38

    .line 697
    move-object/from16 v34, v0

    .line 699
    move-object/from16 v0, v31

    move-object/from16 v0, v31

    .line 701
    if-eq v2, v14, :cond_2e1

    .line 703
    move/from16 v36, v14

    move/from16 v36, v14

    .line 705
    const/4 v14, 0x3

    .line 706
    if-ne v2, v14, :cond_2f1

    .line 708
    :cond_2e1
    move-object/from16 v14, v25

    .line 710
    move-object/from16 v9, v28

    move-object/from16 v9, v28

    .line 712
    move-object/from16 v25, v5

    .line 714
    move-object/from16 v5, v29

    .line 716
    move-object/from16 v29, v3

    .line 718
    const/16 v3, 0x8

    .line 720
    goto/16 :goto_3ae

    .line 722
    :cond_2f1
    move-object/from16 v14, v29

    .line 724
    move-object/from16 v29, v3

    .line 726
    const/16 v3, 0x8

    .line 728
    invoke-virtual {v14, v3}, Landroid/view/View;->setVisibility(I)V

    .line 731
    invoke-virtual {v9, v3}, Landroid/view/View;->setVisibility(I)V

    .line 734
    iget v3, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringComparisonType:I

    .line 736
    if-nez v3, :cond_320

    .line 738
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringEqual:Z

    .line 740
    move-object/from16 v9, v28

    move-object/from16 v9, v28

    .line 742
    invoke-virtual {v9, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 745
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringEqual:Z

    .line 747
    xor-int/lit8 v3, v3, 0x1

    .line 749
    move-object/from16 v7, v27

    move-object/from16 v7, v27

    .line 751
    invoke-virtual {v7, v3}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 754
    move-object/from16 v3, v23

    .line 756
    move-object/from16 v10, v25

    .line 758
    move/from16 v14, v36

    move/from16 v14, v36

    .line 760
    move-object/from16 v25, v5

    .line 762
    goto :goto_346

    .line 763
    :cond_320
    move-object/from16 v7, v27

    move-object/from16 v7, v27

    .line 765
    move-object/from16 v9, v28

    .line 767
    move/from16 v14, v36

    .line 769
    if-ne v3, v14, :cond_336

    .line 771
    move-object/from16 v10, v25

    .line 773
    invoke-virtual {v10, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 776
    move-object/from16 v25, v5

    .line 778
    :cond_331
    move-object/from16 v3, v23

    move-object/from16 v3, v23

    .line 780
    goto :goto_346

    .line 781
    :cond_336
    move-object/from16 v10, v25

    .line 783
    move-object/from16 v25, v5

    move-object/from16 v25, v5

    .line 785
    const/4 v5, 0x2

    .line 786
    if-ne v3, v5, :cond_331

    .line 788
    move-object/from16 v3, v23

    move-object/from16 v3, v23

    .line 790
    invoke-virtual {v3, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 793
    :goto_346
    iget-object v5, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringValue:Ljava/lang/String;

    .line 795
    move-object/from16 v14, v24

    .line 797
    invoke-virtual {v14, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 800
    invoke-virtual {v14}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    .line 803
    move-result-object v5

    .line 804
    invoke-interface {v5}, Ljava/lang/CharSequence;->length()I

    .line 807
    move-result v5

    .line 808
    invoke-virtual {v14, v5}, Landroid/widget/EditText;->setSelection(I)V

    .line 811
    const/4 v5, 0x1

    .line 812
    invoke-virtual {v4, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 815
    const/4 v5, 0x0

    .line 816
    invoke-virtual {v13, v5}, Landroid/view/View;->setVisibility(I)V

    .line 819
    const/4 v5, 0x6

    .line 820
    if-ne v2, v5, :cond_395

    .line 822
    const/16 v5, 0x8

    .line 824
    invoke-virtual {v10, v5}, Landroid/view/View;->setVisibility(I)V

    .line 827
    invoke-virtual {v3, v5}, Landroid/view/View;->setVisibility(I)V

    .line 830
    invoke-virtual {v11, v5}, Landroid/view/View;->setVisibility(I)V

    .line 833
    invoke-virtual {v13, v5}, Landroid/view/View;->setVisibility(I)V

    .line 836
    invoke-virtual {v0, v5}, Landroid/view/View;->setVisibility(I)V

    .line 839
    iget v0, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringComparisonType:I

    .line 841
    if-eqz v0, :cond_37c

    .line 843
    const/4 v5, 0x1

    .line 844
    invoke-virtual {v9, v5}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 847
    :cond_37c
    iget-object v0, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_stringValue:Ljava/lang/String;

    .line 849
    invoke-static {v0}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    .line 852
    move-result v0

    .line 853
    if-eqz v0, :cond_395

    .line 855
    const-wide v23, 0xffffffffL

    const-wide v23, 0xffffffffL

    .line 860
    invoke-static/range {v23 .. v24}, Lcom/arlosoft/macrodroid/variables/a;->b(J)Ljava/lang/String;

    .line 863
    move-result-object v0

    .line 864
    invoke-virtual {v14, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 867
    :cond_395
    move-object/from16 v23, v3

    move-object/from16 v23, v3

    .line 869
    move-object/from16 v18, v6

    .line 871
    move-object/from16 v27, v7

    .line 873
    move-object/from16 v24, v14

    .line 875
    move-object/from16 v3, v19

    .line 877
    move-object/from16 v7, v20

    move-object/from16 v7, v20

    .line 879
    move-object/from16 v5, v21

    .line 881
    const/4 v6, 0x1

    .line 882
    move-object v14, v10

    move-object v14, v10

    .line 883
    move-object/from16 v10, v22

    .line 885
    goto/16 :goto_44d

    .line 887
    :goto_3ae
    invoke-virtual {v5, v3}, Landroid/view/View;->setVisibility(I)V

    .line 890
    invoke-virtual {v10, v3}, Landroid/view/View;->setVisibility(I)V

    .line 893
    invoke-virtual/range {v22 .. v22}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    .line 896
    move-result-object v5

    .line 897
    invoke-interface {v5}, Ljava/lang/CharSequence;->length()I

    .line 900
    move-result v5

    .line 901
    move-object/from16 v10, v22

    .line 903
    invoke-virtual {v10, v5}, Landroid/widget/EditText;->setSelection(I)V

    .line 906
    invoke-virtual {v7, v3}, Landroid/view/View;->setVisibility(I)V

    .line 909
    invoke-virtual {v0, v3}, Landroid/view/View;->setVisibility(I)V

    .line 912
    invoke-virtual {v11, v3}, Landroid/view/View;->setVisibility(I)V

    .line 915
    invoke-virtual {v13, v3}, Landroid/view/View;->setVisibility(I)V

    .line 918
    const/4 v5, 0x0

    .line 919
    invoke-virtual {v12, v5}, Landroid/view/View;->setVisibility(I)V

    .line 922
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 925
    move-result-object v0

    .line 926
    invoke-static {v0, v12}, Lhp5;->a(Landroid/content/Context;Landroid/widget/LinearLayout;)V

    .line 929
    const/4 v0, 0x3

    .line 930
    if-ne v2, v0, :cond_3eb

    .line 932
    const/16 v0, 0x2002

    .line 934
    invoke-virtual {v10, v0}, Landroid/widget/TextView;->setInputType(I)V

    .line 937
    move-object v0, v6

    .line 938
    iget-wide v5, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_doubleValue:D

    .line 940
    invoke-static {v5, v6}, Ljava/lang/String;->valueOf(D)Ljava/lang/String;

    .line 943
    move-result-object v5

    .line 944
    invoke-virtual {v10, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 947
    goto :goto_3fa

    .line 948
    :cond_3eb
    move-object v0, v6

    .line 949
    const/16 v5, 0x1002

    .line 951
    invoke-virtual {v10, v5}, Landroid/widget/TextView;->setInputType(I)V

    .line 954
    iget-wide v5, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intValue:J

    .line 956
    invoke-static {v5, v6}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;

    .line 959
    move-result-object v5

    .line 960
    invoke-virtual {v10, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 963
    :goto_3fa
    invoke-virtual {v10}, Landroid/widget/TextView;->length()I

    .line 966
    move-result v5

    .line 967
    invoke-virtual {v10, v5}, Landroid/widget/EditText;->setSelection(I)V

    .line 970
    invoke-virtual {v10}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    .line 973
    move-result-object v5

    .line 974
    invoke-interface {v5}, Ljava/lang/CharSequence;->length()I

    .line 977
    move-result v5

    .line 978
    if-lez v5, :cond_40d

    .line 980
    const/4 v5, 0x1

    .line 981
    goto :goto_40e

    .line 982
    :cond_40d
    const/4 v5, 0x0

    .line 983
    :goto_40e
    invoke-virtual {v4, v5}, Landroid/view/View;->setEnabled(Z)V

    .line 986
    iget-boolean v5, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intGreaterThan:Z

    .line 988
    if-eqz v5, :cond_424

    .line 990
    move-object/from16 v5, v21

    .line 992
    const/4 v6, 0x1

    .line 993
    invoke-virtual {v5, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 996
    move-object/from16 v18, v0

    move-object/from16 v18, v0

    .line 998
    move-object/from16 v3, v19

    .line 1000
    move-object/from16 v7, v20

    .line 1002
    goto :goto_44d

    .line 1003
    :cond_424
    move-object/from16 v5, v21

    .line 1005
    const/4 v6, 0x1

    .line 1006
    iget-boolean v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intLessThan:Z

    .line 1008
    if-eqz v7, :cond_435

    .line 1010
    move-object/from16 v7, v20

    .line 1012
    invoke-virtual {v7, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1015
    move-object/from16 v18, v0

    .line 1017
    move-object/from16 v3, v19

    .line 1019
    goto :goto_44d

    .line 1020
    :cond_435
    move-object/from16 v7, v20

    .line 1022
    iget-boolean v3, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intNotEqual:Z

    .line 1024
    if-eqz v3, :cond_443

    .line 1026
    move-object/from16 v3, v19

    .line 1028
    invoke-virtual {v3, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1031
    move-object/from16 v18, v0

    .line 1033
    goto :goto_44d

    .line 1034
    :cond_443
    move-object/from16 v3, v18

    .line 1036
    move-object/from16 v18, v0

    .line 1038
    move-object v0, v3

    .line 1039
    move-object/from16 v3, v19

    .line 1041
    invoke-virtual {v0, v6}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1044
    :goto_44d
    new-instance v0, Lji0;

    .line 1046
    const/16 v1, 0x13

    .line 1048
    invoke-direct {v0, v1, v4}, Lji0;-><init>(ILandroid/widget/Button;)V

    .line 1051
    invoke-virtual {v10, v0}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 1054
    new-instance v0, Loxg;

    .line 1056
    move-object/from16 v1, p0

    .line 1058
    move-object/from16 v19, p1

    .line 1060
    move-object/from16 v41, v4

    .line 1062
    move/from16 v36, v6

    .line 1064
    move-object v6, v7

    .line 1065
    move-object v4, v8

    .line 1066
    move-object/from16 v46, v12

    .line 1068
    move-object/from16 v43, v15

    .line 1070
    move-object/from16 v42, v16

    .line 1072
    move-object/from16 v15, v23

    .line 1074
    move-object/from16 v16, v24

    .line 1076
    move-object/from16 v44, v26

    .line 1078
    move-object/from16 v45, v29

    move-object/from16 v45, v29

    .line 1080
    move-object/from16 v8, v30

    .line 1082
    move-object/from16 v20, v32

    .line 1084
    move-object/from16 v40, v34

    .line 1086
    const/16 v31, 0x8

    .line 1088
    const/16 v33, 0x0

    .line 1090
    move-object v7, v3

    .line 1091
    move-object v12, v9

    .line 1092
    move-object/from16 v9, v18

    .line 1094
    move v3, v2

    .line 1095
    move-object/from16 v18, v11

    .line 1097
    move-object/from16 v11, v17

    .line 1099
    move-object/from16 v2, v25

    move-object/from16 v2, v25

    .line 1101
    move-object/from16 v17, v13

    .line 1103
    move-object/from16 v13, v27

    .line 1105
    invoke-direct/range {v0 .. v20}, Loxg;-><init>(Lcom/arlosoft/macrodroid/triggers/VariableTrigger;Landroid/widget/Spinner;ILandroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/CheckBox;Landroid/widget/CheckBox;Ljava/util/ArrayList;Lvf0;)V

    .line 1108
    move-object v6, v0

    move-object v6, v0

    .line 1109
    move-object v5, v2

    move-object v5, v2

    .line 1110
    move-object v4, v8

    move-object v4, v8

    .line 1111
    move-object v0, v9

    move-object v0, v9

    .line 1112
    move-object v3, v10

    .line 1113
    move-object v2, v11

    move-object v2, v11

    .line 1114
    move-object/from16 v14, v16

    .line 1116
    move-object/from16 v11, v20

    move-object/from16 v11, v20

    .line 1118
    move-object/from16 v9, v41

    .line 1120
    invoke-virtual {v9, v6}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1123
    new-instance v6, Ltkf;

    .line 1125
    const/16 v7, 0x19

    .line 1127
    invoke-direct {v6, v11, v7}, Ltkf;-><init>(Lvf0;I)V

    .line 1130
    move-object/from16 v7, v42

    move-object/from16 v7, v42

    .line 1132
    invoke-virtual {v7, v6}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1135
    new-instance v6, Lkhg;

    .line 1137
    const/16 v7, 0x13

    .line 1139
    invoke-direct {v6, v14, v7}, Lkhg;-><init>(Landroid/widget/EditText;I)V

    .line 1142
    new-instance v7, Lfrf;

    .line 1144
    const/16 v8, 0xd

    .line 1146
    move-object/from16 v10, v40

    move-object/from16 v10, v40

    .line 1148
    invoke-direct {v7, v1, v10, v6, v8}, Lfrf;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 1151
    move-object/from16 v12, v44

    .line 1153
    invoke-virtual {v12, v7}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 1156
    iget-boolean v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intCompareVariable:Z

    .line 1158
    if-nez v6, :cond_4db

    .line 1160
    iget-object v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1162
    if-nez v6, :cond_4db

    .line 1164
    move/from16 v14, v36

    .line 1166
    :goto_4d6
    move-object/from16 v10, v43

    move-object/from16 v10, v43

    .line 1168
    goto :goto_4de

    .line 1169
    :cond_4db
    move/from16 v14, v33

    .line 1171
    goto :goto_4d6

    .line 1172
    :goto_4de
    invoke-virtual {v10, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1175
    iget-boolean v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intCompareVariable:Z

    .line 1177
    if-nez v6, :cond_4ec

    .line 1179
    iget-object v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1181
    if-nez v6, :cond_4ec

    .line 1183
    move/from16 v14, v36

    .line 1185
    goto :goto_4ee

    .line 1186
    :cond_4ec
    move/from16 v14, v33

    .line 1188
    :goto_4ee
    invoke-virtual {v3, v14}, Landroid/view/View;->setEnabled(Z)V

    .line 1191
    iget-object v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1193
    if-eqz v6, :cond_4f8

    .line 1195
    move/from16 v14, v36

    .line 1197
    goto :goto_4fa

    .line 1198
    :cond_4f8
    move/from16 v14, v33

    .line 1200
    :goto_4fa
    invoke-virtual {v4, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1203
    iget-object v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1205
    if-eqz v6, :cond_504

    .line 1207
    move/from16 v14, v36

    .line 1209
    goto :goto_508

    .line 1210
    :cond_504
    move/from16 v14, v33

    move/from16 v14, v33

    .line 1212
    :goto_508
    invoke-virtual {v0, v14}, Landroid/view/View;->setEnabled(Z)V

    .line 1215
    iget-object v6, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1217
    if-eqz v6, :cond_516

    .line 1219
    move/from16 v14, v36

    move/from16 v14, v36

    .line 1221
    :goto_513
    move-object/from16 v6, v45

    .line 1223
    goto :goto_519

    .line 1224
    :cond_516
    move/from16 v14, v33

    .line 1226
    goto :goto_513

    .line 1227
    :goto_519
    invoke-virtual {v6, v14}, Landroid/view/View;->setEnabled(Z)V

    .line 1230
    iget-object v7, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1232
    if-eqz v7, :cond_527

    .line 1234
    move/from16 v14, v33

    .line 1236
    :goto_522
    move-object/from16 v7, v46

    move-object/from16 v7, v46

    .line 1238
    goto :goto_52c

    .line 1239
    :cond_527
    move/from16 v14, v31

    move/from16 v14, v31

    .line 1241
    goto :goto_522

    .line 1242
    :goto_52c
    invoke-virtual {v7, v14}, Landroid/view/View;->setVisibility(I)V

    .line 1245
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1247
    invoke-virtual {v0, v8}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 1250
    iget-boolean v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intCompareVariable:Z

    .line 1252
    if-eqz v8, :cond_53f

    .line 1254
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1256
    if-nez v8, :cond_53f

    .line 1258
    move/from16 v14, v36

    .line 1260
    goto :goto_541

    .line 1261
    :cond_53f
    move/from16 v14, v33

    .line 1263
    :goto_541
    invoke-virtual {v2, v14}, Landroid/widget/CompoundButton;->setChecked(Z)V

    .line 1266
    iget-boolean v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_intCompareVariable:Z

    .line 1268
    if-eqz v8, :cond_551

    .line 1270
    iget-object v8, v1, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->m_expression:Ljava/lang/String;

    .line 1272
    if-nez v8, :cond_551

    .line 1274
    move/from16 v14, v33

    move/from16 v14, v33

    .line 1276
    goto :goto_553

    .line 1277
    :cond_551
    move/from16 v14, v31

    .line 1279
    :goto_553
    invoke-virtual {v5, v14}, Landroid/view/View;->setVisibility(I)V

    .line 1282
    invoke-virtual {v2}, Landroid/widget/CompoundButton;->isChecked()Z

    .line 1285
    move-result v8

    .line 1286
    if-eqz v8, :cond_55f

    .line 1288
    invoke-virtual {v1, v5}, Lcom/arlosoft/macrodroid/triggers/VariableTrigger;->x0(Landroid/widget/Spinner;)V

    .line 1291
    :cond_55f
    move-object/from16 v18, v0

    .line 1293
    new-instance v0, Llxg;

    .line 1295
    move-object v8, v3

    .line 1296
    move-object v3, v10

    .line 1297
    move-object v10, v2

    move-object v10, v2

    .line 1298
    move-object v2, v5

    move-object v2, v5

    .line 1299
    move-object/from16 v5, v18

    .line 1301
    invoke-direct/range {v0 .. v10}, Llxg;-><init>(Lcom/arlosoft/macrodroid/triggers/VariableTrigger;Landroid/widget/Spinner;Landroid/widget/RadioButton;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/Button;Landroid/widget/LinearLayout;Landroid/widget/EditText;Landroid/widget/Button;Landroid/widget/RadioButton;)V

    .line 1304
    move-object v1, v0

    move-object v1, v0

    .line 1305
    move-object v0, v5

    move-object v0, v5

    .line 1306
    move-object v5, v2

    .line 1307
    move-object v2, v10

    .line 1308
    move-object v10, v3

    .line 1309
    move-object v3, v8

    .line 1310
    invoke-virtual {v2, v1}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1313
    move-object/from16 v18, v0

    .line 1315
    new-instance v0, Llxg;

    .line 1317
    move-object/from16 v1, p0

    .line 1319
    move-object v8, v5

    .line 1320
    move-object/from16 v5, v18

    .line 1322
    invoke-direct/range {v0 .. v10}, Llxg;-><init>(Lcom/arlosoft/macrodroid/triggers/VariableTrigger;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/Button;Landroid/widget/LinearLayout;Landroid/widget/Spinner;Landroid/widget/Button;Landroid/widget/RadioButton;)V

    .line 1325
    move-object v1, v0

    .line 1326
    move-object v0, v5

    move-object v0, v5

    .line 1327
    move-object v5, v8

    move-object v5, v8

    .line 1328
    invoke-virtual {v10, v1}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1331
    move-object/from16 v18, v0

    .line 1333
    new-instance v0, Llxg;

    .line 1335
    move-object v1, v4

    .line 1336
    move-object v4, v2

    .line 1337
    move-object v2, v10

    .line 1338
    move-object v10, v1

    move-object v10, v1

    .line 1339
    move-object/from16 v1, p0

    .line 1341
    move-object v8, v7

    .line 1342
    move-object v7, v6

    .line 1343
    move-object/from16 v6, v18

    .line 1345
    invoke-direct/range {v0 .. v10}, Llxg;-><init>(Lcom/arlosoft/macrodroid/triggers/VariableTrigger;Landroid/widget/RadioButton;Landroid/widget/EditText;Landroid/widget/RadioButton;Landroid/widget/Spinner;Landroid/widget/EditText;Landroid/widget/Button;Landroid/widget/LinearLayout;Landroid/widget/Button;Landroid/widget/RadioButton;)V

    .line 1348
    move-object v2, v0

    .line 1349
    move-object v0, v6

    .line 1350
    move-object v4, v10

    .line 1351
    invoke-virtual {v4, v2}, Landroid/widget/CompoundButton;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V

    .line 1354
    new-instance v2, Ltg;

    .line 1356
    const/16 v3, 0xa

    .line 1358
    invoke-direct {v2, v1, v0, v9, v3}, Ltg;-><init>(Lcom/arlosoft/macrodroid/common/SelectableItem;Landroid/widget/EditText;Landroid/widget/Button;I)V

    .line 1361
    invoke-virtual {v0, v2}, Landroid/widget/TextView;->addTextChangedListener(Landroid/text/TextWatcher;)V

    .line 1364
    invoke-virtual {v11}, Landroid/app/Dialog;->show()V

    .line 1367
    return-void
.end method
