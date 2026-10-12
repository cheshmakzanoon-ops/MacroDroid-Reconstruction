.method private static final Composable_sW7UJKQ$lambda$3(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Lrnc;Lhba;Leia;JLwm6;JZLyg1;Lyt2;I)Lblg;
    .locals 34

    .line 1
    move-object/from16 v0, p0

    move-object/from16 v0, p0

    .line 3
    move-object/from16 v1, p1

    move-object/from16 v1, p1

    .line 5
    move-object/from16 v9, p3

    move-object/from16 v9, p3

    .line 7
    move-object/from16 v2, p10

    move-object/from16 v2, p10

    .line 9
    sget-object v12, Lsra;->p:Ll71;

    .line 11
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 14
    and-int/lit8 v3, p12, 0xe

    .line 16
    const/4 v4, 0x2

    .line 17
    if-nez v3, :cond_2b

    .line 19
    move-object/from16 v3, p11

    .line 21
    check-cast v3, Lnr6;

    .line 23
    invoke-virtual {v3, v2}, Lnr6;->g(Ljava/lang/Object;)Z

    .line 26
    move-result v3

    .line 27
    if-eqz v3, :cond_26

    .line 29
    const/4 v3, 0x4

    .line 30
    goto :goto_28

    .line 31
    :cond_26
    move v3, v4

    move v3, v4

    .line 32
    :goto_28
    or-int v3, p12, v3

    .line 34
    goto :goto_2f

    .line 35
    :cond_2b
    move/from16 v3, p12

    move/from16 v3, p12

    .line 37
    :goto_2f
    and-int/lit8 v5, v3, 0x5b

    .line 39
    const/16 v6, 0x12

    .line 41
    const/4 v13, 0x0

    .line 42
    const/4 v14, 0x1

    .line 43
    if-eq v5, v6, :cond_39

    .line 45
    move v5, v14

    .line 46
    goto :goto_3b

    .line 47
    :cond_39
    move v5, v13

    move v5, v13

    .line 48
    :goto_3b
    and-int/2addr v3, v14

    .line 49
    move-object/from16 v7, p11

    .line 51
    check-cast v7, Lnr6;

    .line 53
    invoke-virtual {v7, v3, v5}, Lnr6;->P(IZ)Z

    .line 56
    move-result v3

    .line 57
    if-eqz v3, :cond_41e

    .line 59
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneItem;->getParent()Lcom/arlosoft/macrodroid/scene/components/SceneContainer;

    .line 62
    move-result-object v3

    .line 63
    instance-of v3, v3, Lcom/arlosoft/macrodroid/scene/components/SceneHorizontalLayout;

    .line 65
    const/high16 v5, 0x41800000    # 16.0f

    .line 67
    if-eqz v3, :cond_68

    .line 69
    const v2, -0x7974a1f0

    .line 72
    invoke-virtual {v7, v2}, Lnr6;->Z(I)V

    .line 75
    sget-object v2, Lmv;->a:Lk25;

    .line 77
    invoke-virtual {v7, v2}, Lnr6;->k(Landroidx/compose/runtime/d;)Ljava/lang/Object;

    .line 80
    move-result-object v2

    .line 81
    check-cast v2, Landroid/content/res/Configuration;

    .line 83
    iget v2, v2, Landroid/content/res/Configuration;->screenWidthDp:I

    .line 85
    int-to-float v2, v2

    .line 86
    const/high16 v3, 0x42000000    # 32.0f

    .line 88
    sub-float/2addr v2, v3

    .line 89
    invoke-virtual {v7, v13}, Lnr6;->q(Z)V

    .line 92
    goto :goto_78

    .line 93
    :cond_68
    const v3, -0x7971e8ae

    .line 96
    invoke-virtual {v7, v3}, Lnr6;->Z(I)V

    .line 99
    invoke-virtual {v7, v13}, Lnr6;->q(Z)V

    .line 102
    check-cast v2, Lzg1;

    .line 104
    invoke-virtual {v2}, Lzg1;->a()F

    .line 107
    move-result v2

    .line 108
    sub-float/2addr v2, v5

    .line 109
    :goto_78
    iget-object v3, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 111
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getWidthPercent()I

    .line 114
    move-result v3

    .line 115
    int-to-float v3, v3

    .line 116
    const/high16 v6, 0x42c80000    # 100.0f

    .line 118
    div-float/2addr v3, v6

    .line 119
    mul-float/2addr v3, v2

    .line 120
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 122
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 125
    move-result v2

    .line 126
    const/4 v15, 0x3

    .line 127
    if-eq v2, v4, :cond_97

    .line 129
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 131
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 134
    move-result v2

    .line 135
    if-ne v2, v15, :cond_95

    .line 137
    goto :goto_97

    .line 138
    :cond_95
    move v2, v13

    .line 139
    goto :goto_98

    .line 140
    :cond_97
    :goto_97
    move v2, v14

    .line 141
    :goto_98
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 144
    move-result-object v6

    .line 145
    check-cast v6, Lbi2;

    .line 147
    iget v6, v6, Lbi2;->a:F

    .line 149
    float-to-int v6, v6

    .line 150
    invoke-static {v6}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 153
    move-result-object v6

    .line 154
    invoke-virtual {v6}, Ljava/lang/String;->length()I

    .line 157
    move-result v6

    .line 158
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 161
    move-result-object v8

    .line 162
    check-cast v8, Lbi2;

    .line 164
    iget v8, v8, Lbi2;->b:F

    .line 166
    float-to-int v8, v8

    .line 167
    invoke-static {v8}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 170
    move-result-object v8

    .line 171
    invoke-virtual {v8}, Ljava/lang/String;->length()I

    .line 174
    move-result v8

    .line 175
    invoke-static {v6, v8}, Ljava/lang/Math;->max(II)I

    .line 178
    move-result v6

    .line 179
    if-eqz v2, :cond_cf

    .line 181
    int-to-float v6, v6

    .line 182
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getTextSizeValue()I

    .line 185
    move-result v8

    .line 186
    int-to-float v8, v8

    .line 187
    const v16, 0x3f19999a    # 0.6f

    .line 190
    mul-float v8, v8, v16

    .line 192
    mul-float/2addr v8, v6

    .line 193
    add-float/2addr v8, v5

    .line 194
    :goto_cd
    move v5, v8

    .line 195
    goto :goto_d1

    .line 196
    :cond_cf
    const/4 v8, 0x0

    .line 197
    goto :goto_cd

    .line 198
    :goto_d1
    if-eqz v2, :cond_ea

    .line 200
    sub-float/2addr v3, v5

    .line 201
    new-instance v2, Ljt4;

    .line 203
    invoke-direct {v2, v3}, Ljt4;-><init>(F)V

    .line 206
    new-instance v3, Ljt4;

    .line 208
    const/high16 v6, 0x42200000    # 40.0f

    .line 210
    invoke-direct {v3, v6}, Ljt4;-><init>(F)V

    .line 213
    invoke-virtual {v2, v3}, Ljt4;->compareTo(Ljava/lang/Object;)I

    .line 216
    move-result v6

    .line 217
    if-gez v6, :cond_e8

    .line 219
    move-object v2, v3

    move-object v2, v3

    .line 220
    :cond_e8
    iget v3, v2, Ljt4;->a:F

    .line 222
    :cond_ea
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 225
    move-result-object v2

    .line 226
    move-object v6, v2

    move-object v6, v2

    .line 227
    check-cast v6, Lbi2;

    .line 229
    iget v6, v6, Lbi2;->a:F

    .line 231
    check-cast v2, Lbi2;

    .line 233
    iget v2, v2, Lbi2;->b:F

    .line 235
    invoke-static {v6, v2}, Ljava/lang/Math;->max(FF)F

    .line 238
    move-result v2

    .line 239
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderStepSize()I

    .line 242
    move-result v8

    .line 243
    float-to-int v15, v2

    .line 244
    float-to-int v13, v6

    .line 245
    sub-int/2addr v15, v13

    .line 246
    invoke-static {v14, v15}, Ljava/lang/Math;->max(II)I

    .line 249
    move-result v13

    .line 250
    invoke-static {v8, v14, v13}, Lzg0;->q(III)I

    .line 253
    move-result v8

    .line 254
    invoke-static {v14, v8}, Ljava/lang/Math;->max(II)I

    .line 257
    move-result v13

    .line 258
    sub-float v8, v2, v6

    .line 260
    int-to-float v15, v13

    .line 261
    div-float/2addr v8, v15

    .line 262
    float-to-int v8, v8

    .line 263
    iget v4, v1, Lrnc;->element:F

    .line 265
    invoke-static {v4}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    .line 268
    move-result-object v4

    .line 269
    new-instance v14, Lxrd;

    .line 271
    move/from16 p11, v2

    .line 273
    const/4 v2, 0x0

    .line 274
    invoke-direct {v14, v0, v1, v9, v2}, Lxrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Lrnc;Leia;Lm73;)V

    .line 277
    invoke-static {v7, v14, v4}, Lead;->h(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 280
    invoke-static {v9}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->Composable_sW7UJKQ$lambda$1(Leia;)F

    .line 283
    move-result v1

    .line 284
    div-float/2addr v1, v15

    .line 285
    invoke-static {v1}, Lbz9;->F(F)I

    .line 288
    move-result v1

    .line 289
    mul-int/2addr v1, v13

    .line 290
    new-instance v2, Li38;

    .line 292
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 295
    move-result-object v4

    .line 296
    check-cast v4, Lbi2;

    .line 298
    iget v4, v4, Lbi2;->a:F

    .line 300
    float-to-int v4, v4

    .line 301
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 304
    move-result-object v14

    .line 305
    check-cast v14, Lbi2;

    .line 307
    iget v14, v14, Lbi2;->b:F

    .line 309
    float-to-int v14, v14

    .line 310
    const/4 v15, 0x1

    .line 311
    invoke-direct {v2, v4, v14, v15}, Lg38;-><init>(III)V

    .line 314
    invoke-static {v1, v2}, Lzg0;->r(ILi38;)I

    .line 317
    move-result v1

    .line 318
    invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 321
    move-result-object v1

    .line 322
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 324
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getWidthPercent()I

    .line 327
    move-result v2

    .line 328
    const/16 v4, 0x63

    .line 330
    if-lt v2, v4, :cond_15c

    .line 332
    sget-object v2, Lkj0;->f:Lura;

    .line 334
    goto :goto_170

    .line 335
    :cond_15c
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 337
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getAlignment()Lcom/arlosoft/macrodroid/scene/data/SceneAlignment;

    .line 340
    move-result-object v2

    .line 341
    if-eqz v2, :cond_16a

    .line 343
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/data/SceneAlignment;->getArrangementHorizontal()Lhj0;

    .line 346
    move-result-object v2

    .line 347
    if-nez v2, :cond_170

    .line 349
    :cond_16a
    sget-object v2, Lcom/arlosoft/macrodroid/scene/data/SceneAlignment;->Center:Lcom/arlosoft/macrodroid/scene/data/SceneAlignment;

    .line 351
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/data/SceneAlignment;->getArrangementHorizontal()Lhj0;

    .line 354
    move-result-object v2

    .line 355
    :cond_170
    :goto_170
    iget-object v4, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 357
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getPadding()Ljava/lang/String;

    .line 360
    move-result-object v4

    .line 361
    invoke-virtual {v0, v4}, Lcom/arlosoft/macrodroid/scene/components/SceneItem;->getPaddingValue(Ljava/lang/String;)I

    .line 364
    move-result v4

    .line 365
    sget-object v14, Lhpe;->a:Laz5;

    .line 367
    move-object/from16 v15, p2

    move-object/from16 v15, p2

    .line 369
    invoke-interface {v15, v14}, Lhba;->then(Lhba;)Lhba;

    .line 372
    move-result-object v14

    .line 373
    int-to-float v4, v4

    .line 374
    const/high16 p1, 0x41000000    # 8.0f

    .line 376
    add-float v15, v4, p1

    .line 378
    invoke-static {v14, v15, v4}, Lgl9;->O(Lhba;FF)Lhba;

    .line 381
    move-result-object v4

    .line 382
    sget-object v14, Lsra;->m:Lm71;

    .line 384
    const/16 v15, 0x30

    .line 386
    invoke-static {v2, v14, v7, v15}, Lw9d;->a(Lhj0;Lpp;Lyt2;I)Lx9d;

    .line 389
    move-result-object v2

    .line 390
    iget-wide v14, v7, Lnr6;->T:J

    .line 392
    const/16 v18, 0x20

    .line 394
    ushr-long v19, v14, v18

    .line 396
    xor-long v14, v14, v19

    .line 398
    long-to-int v14, v14

    .line 399
    invoke-virtual {v7}, Lnr6;->m()Lnob;

    .line 402
    move-result-object v15

    .line 403
    invoke-static {v7, v4}, Lead;->P(Lyt2;Lhba;)Lhba;

    .line 406
    move-result-object v4

    .line 407
    sget-object v19, Lkt2;->x1:Ljt2;

    .line 409
    invoke-virtual/range {v19 .. v19}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 412
    move/from16 v19, v8

    .line 414
    sget-object v8, Ljt2;->b:Ltv8;

    .line 416
    invoke-virtual {v7}, Lnr6;->d0()V

    .line 419
    move-object/from16 v20, v1

    .line 421
    iget-boolean v1, v7, Lnr6;->S:Z

    .line 423
    if-eqz v1, :cond_1bc

    .line 425
    invoke-virtual {v7, v8}, Lnr6;->l(Lum6;)V

    .line 428
    goto :goto_1bf

    .line 429
    :cond_1bc
    invoke-virtual {v7}, Lnr6;->m0()V

    .line 432
    :goto_1bf
    sget-object v1, Ljt2;->f:Le30;

    .line 434
    invoke-static {v7, v1, v2}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 437
    sget-object v2, Ljt2;->e:Le30;

    .line 439
    invoke-static {v7, v2, v15}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 442
    invoke-static {v14}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 445
    move-result-object v14

    .line 446
    sget-object v15, Ljt2;->g:Le30;

    .line 448
    invoke-static {v7, v15, v14}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 451
    sget-object v14, Ljt2;->h:Lce;

    .line 453
    invoke-static {v7, v14}, Lhae;->I(Lyt2;Lwm6;)V

    .line 456
    move-object/from16 p2, v8

    .line 458
    sget-object v8, Ljt2;->d:Le30;

    .line 460
    invoke-static {v7, v8, v4}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 463
    iget-object v4, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 465
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 468
    move-result v4

    .line 469
    move-object/from16 v21, v8

    move-object/from16 v21, v8

    .line 471
    sget-object v8, Leba;->a:Leba;

    .line 473
    move-object/from16 v23, v1

    .line 475
    const/4 v1, 0x2

    .line 476
    if-ne v4, v1, :cond_240

    .line 478
    const v1, 0xd3ef003

    .line 481
    invoke-virtual {v7, v1}, Lnr6;->Z(I)V

    .line 484
    invoke-static {v8, v5}, Lhpe;->m(Lhba;F)Lhba;

    .line 487
    move-result-object v1

    .line 488
    new-instance v4, Lb0h;

    .line 490
    invoke-direct {v4}, Ljava/lang/Object;-><init>()V

    .line 493
    invoke-interface {v1, v4}, Lhba;->then(Lhba;)Lhba;

    .line 496
    move-result-object v1

    .line 497
    move v4, v6

    move v4, v6

    .line 498
    new-instance v6, Ltrd;

    .line 500
    move-object/from16 v16, v1

    .line 502
    const/4 v1, 0x6

    .line 503
    invoke-direct {v6, v0, v9, v1}, Ltrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Leia;I)V

    .line 506
    move-object v1, v8

    move-object v1, v8

    .line 507
    const/high16 v8, 0x40000

    .line 509
    move-object/from16 v10, p2

    .line 511
    move-object/from16 v30, v1

    .line 513
    move-object v9, v2

    move-object v9, v2

    .line 514
    move/from16 v29, v5

    move/from16 v29, v5

    .line 516
    move-object/from16 v2, v16

    move-object/from16 v2, v16

    .line 518
    move-object/from16 v1, v20

    .line 520
    move-object/from16 v22, v21

    .line 522
    move-object/from16 v11, v23

    .line 524
    move-object/from16 v5, p6

    move-object/from16 v5, p6

    .line 526
    move/from16 v20, p11

    .line 528
    move/from16 v16, v4

    .line 530
    move-object/from16 v21, v12

    .line 532
    move/from16 p11, v13

    .line 534
    const v12, 0xc6d85fe

    .line 537
    move v13, v3

    .line 538
    move-wide/from16 v3, p4

    .line 540
    invoke-direct/range {v0 .. v8}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V

    .line 543
    const/4 v2, 0x0

    .line 544
    :goto_23a
    invoke-virtual {v7, v2}, Lnr6;->q(Z)V

    .line 547
    move-object/from16 v3, v30

    .line 549
    goto :goto_265

    .line 550
    :cond_240
    move-object/from16 v10, p2

    move-object/from16 v10, p2

    .line 552
    move-object v9, v2

    move-object v9, v2

    .line 553
    move/from16 v29, v5

    .line 555
    move/from16 v16, v6

    .line 557
    move-object/from16 v30, v8

    move-object/from16 v30, v8

    .line 559
    move-object/from16 v1, v20

    .line 561
    move-object/from16 v22, v21

    .line 563
    move-object/from16 v11, v23

    .line 565
    const/4 v2, 0x0

    .line 566
    move/from16 v20, p11

    .line 568
    move-object/from16 v21, v12

    .line 570
    move/from16 p11, v13

    move/from16 p11, v13

    .line 572
    const v12, 0xc6d85fe

    .line 575
    move v13, v3

    .line 576
    invoke-virtual {v7, v12}, Lnr6;->Z(I)V

    .line 579
    goto :goto_23a

    .line 580
    :goto_265
    invoke-static {v3, v13}, Lhpe;->m(Lhba;F)Lhba;

    .line 583
    move-result-object v4

    .line 584
    sget-object v5, Lkj0;->c:Lwra;

    .line 586
    sget-object v6, Lsra;->o:Ll71;

    .line 588
    invoke-static {v5, v6, v7, v2}, Lrm2;->a(Ljj0;Lnp;Lyt2;I)Ltm2;

    .line 591
    move-result-object v5

    .line 592
    iget-wide v12, v7, Lnr6;->T:J

    .line 594
    ushr-long v24, v12, v18

    .line 596
    xor-long v12, v12, v24

    .line 598
    long-to-int v2, v12

    .line 599
    invoke-virtual {v7}, Lnr6;->m()Lnob;

    .line 602
    move-result-object v6

    .line 603
    invoke-static {v7, v4}, Lead;->P(Lyt2;Lhba;)Lhba;

    .line 606
    move-result-object v4

    .line 607
    invoke-virtual {v7}, Lnr6;->d0()V

    .line 610
    iget-boolean v8, v7, Lnr6;->S:Z

    .line 612
    if-eqz v8, :cond_28b

    .line 614
    invoke-virtual {v7, v10}, Lnr6;->l(Lum6;)V

    .line 617
    goto :goto_28e

    .line 618
    :cond_28b
    invoke-virtual {v7}, Lnr6;->m0()V

    .line 621
    :goto_28e
    invoke-static {v7, v11, v5}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 624
    invoke-static {v7, v9, v6}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 627
    invoke-static {v2, v7, v15, v7, v14}, Lku1;->v(ILnr6;Le30;Lnr6;Lce;)V

    .line 630
    move-object/from16 v2, v22

    .line 632
    invoke-static {v7, v2, v4}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 635
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 637
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 640
    move-result v2

    .line 641
    const v9, -0x470ef6f8

    .line 644
    const/4 v15, 0x1

    .line 645
    if-ne v2, v15, :cond_2d9

    .line 647
    const v2, -0x462e5ad0

    .line 650
    invoke-virtual {v7, v2}, Lnr6;->Z(I)V

    .line 653
    new-instance v2, Lmb7;

    .line 655
    move-object/from16 v10, v21

    .line 657
    invoke-direct {v2, v10}, Lmb7;-><init>(Ll71;)V

    .line 660
    move/from16 v4, p1

    move/from16 v4, p1

    .line 662
    invoke-static {v2, v4, v15}, Lrm6;->H(Lhba;FI)Lhba;

    .line 665
    move-result-object v2

    .line 666
    new-instance v6, Ltrd;

    .line 668
    const/4 v4, 0x7

    .line 669
    move-object/from16 v11, p3

    move-object/from16 v11, p3

    .line 671
    invoke-direct {v6, v0, v11, v4}, Ltrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Leia;I)V

    .line 674
    const/high16 v8, 0x40000

    .line 676
    move-object/from16 v5, p6

    .line 678
    move-object/from16 v30, v3

    .line 680
    move-wide/from16 v3, p4

    .line 682
    invoke-direct/range {v0 .. v8}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V

    .line 685
    move-object/from16 v31, v1

    .line 687
    const/4 v2, 0x0

    .line 688
    :goto_2d5
    invoke-virtual {v7, v2}, Lnr6;->q(Z)V

    .line 691
    goto :goto_2ea

    .line 692
    :cond_2d9
    move-object/from16 v11, p3

    .line 694
    move-object/from16 v31, v1

    move-object/from16 v31, v1

    .line 696
    move-object/from16 v30, v3

    .line 698
    move-object/from16 v10, v21

    move-object/from16 v10, v21

    .line 700
    const/4 v2, 0x0

    .line 701
    invoke-virtual {v7, v9}, Lnr6;->Z(I)V

    .line 704
    goto :goto_2d5

    .line 705
    :goto_2ea
    invoke-static {v11}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->Composable_sW7UJKQ$lambda$1(Leia;)F

    .line 708
    move-result v32

    .line 709
    new-instance v0, Lbi2;

    .line 711
    move/from16 v4, v16

    move/from16 v4, v16

    .line 713
    move/from16 v6, v20

    .line 715
    invoke-direct {v0, v4, v6}, Lbi2;-><init>(FF)V

    .line 718
    const/4 v15, 0x1

    .line 719
    add-int/lit8 v8, v19, -0x1

    .line 721
    invoke-static {v8, v15}, Ljava/lang/Math;->max(II)I

    .line 724
    move-result v33

    .line 725
    const/high16 v1, 0x3f000000    # 0.5f

    .line 727
    move-wide/from16 v12, p7

    .line 729
    move/from16 v17, v15

    move/from16 v17, v15

    .line 731
    invoke-static {v12, v13, v1}, Lek2;->b(JF)J

    .line 734
    move-result-wide v14

    .line 735
    move/from16 v3, v17

    move/from16 v3, v17

    .line 737
    invoke-static {v12, v13, v1}, Lek2;->b(JF)J

    .line 740
    move-result-wide v16

    .line 741
    const v5, 0xc6d85fe

    .line 744
    sget-wide v22, Lek2;->l:J

    .line 746
    invoke-static {v12, v13, v1}, Lek2;->b(JF)J

    .line 749
    move-result-wide v18

    .line 750
    const/high16 v1, 0x3e800000    # 0.25f

    .line 752
    move-wide/from16 v20, v18

    .line 754
    invoke-static {v12, v13, v1}, Lek2;->b(JF)J

    .line 757
    move-result-wide v18

    .line 758
    invoke-static {v12, v13, v1}, Lek2;->b(JF)J

    .line 761
    move-result-wide v24

    .line 762
    const/high16 v27, 0xd80000

    .line 764
    const/16 v28, 0x300

    .line 766
    move-wide/from16 v12, v20

    .line 768
    move-wide/from16 v20, v24

    .line 770
    move-wide/from16 v24, v22

    .line 772
    move v8, v3

    move v8, v3

    .line 773
    move-object/from16 v26, v7

    .line 775
    move-object v1, v10

    move-object v1, v10

    .line 776
    const/4 v3, 0x3

    .line 777
    move-wide/from16 v10, p7

    .line 779
    move v7, v2

    .line 780
    move v2, v5

    move v2, v5

    .line 781
    move/from16 v5, p11

    .line 783
    invoke-static/range {v10 .. v28}, Lfl1;->s(JJJJJJJJLyt2;II)Lkd4;

    .line 786
    move-result-object v22

    .line 787
    move-object/from16 v23, v26

    move-object/from16 v23, v26

    .line 789
    new-instance v16, Lwrd;

    .line 791
    move/from16 v17, v8

    .line 793
    const/4 v8, 0x0

    .line 794
    move-object/from16 v19, v0

    move-object/from16 v19, v0

    .line 796
    move-object v10, v1

    move-object v10, v1

    .line 797
    move v12, v2

    .line 798
    move v13, v3

    .line 799
    move v14, v7

    .line 800
    move-object/from16 v0, v16

    .line 802
    move-object/from16 v11, v30

    .line 804
    move-object/from16 v1, p0

    .line 806
    move-object/from16 v7, p3

    .line 808
    move-object/from16 v2, p6

    .line 810
    move/from16 v3, p9

    .line 812
    invoke-direct/range {v0 .. v8}, Lwrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneItem;Lwm6;ZFIFLeia;I)V

    .line 815
    move-object v0, v1

    .line 816
    move-object v1, v7

    .line 817
    new-instance v2, Lmrc;

    .line 819
    const/16 v3, 0xf

    .line 821
    invoke-direct {v2, v0, v3}, Lmrc;-><init>(Ljava/lang/Object;I)V

    .line 824
    const/16 v24, 0x0

    .line 826
    const/16 v25, 0x84

    .line 828
    move/from16 v15, v17

    move/from16 v15, v17

    .line 830
    const/16 v17, 0x0

    .line 832
    move/from16 v18, p9

    move/from16 v18, p9

    .line 834
    move-object/from16 v21, v2

    .line 836
    move v2, v15

    move v2, v15

    .line 837
    move/from16 v15, v32

    .line 839
    move/from16 v20, v33

    .line 841
    invoke-static/range {v15 .. v25}, Lbre;->b(FLwm6;Lhba;ZLci2;ILum6;Lkd4;Lyt2;II)V

    .line 844
    move-object/from16 v7, v23

    move-object/from16 v7, v23

    .line 846
    iget-object v3, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 848
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 851
    move-result v3

    .line 852
    if-nez v3, :cond_3c1

    .line 854
    const v3, -0x45feb013

    .line 857
    invoke-virtual {v7, v3}, Lnr6;->Z(I)V

    .line 860
    new-instance v3, Lmb7;

    .line 862
    invoke-direct {v3, v10}, Lmb7;-><init>(Ll71;)V

    .line 865
    const/high16 v4, -0x3f000000    # -8.0f

    .line 867
    invoke-static {v3, v4, v2}, Lrm6;->H(Lhba;FI)Lhba;

    .line 870
    move-result-object v3

    .line 871
    new-instance v6, Ltrd;

    .line 873
    const/16 v4, 0x8

    .line 875
    invoke-direct {v6, v0, v1, v4}, Ltrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Leia;I)V

    .line 878
    const/high16 v8, 0x40000

    .line 880
    move-object/from16 v5, p6

    move-object/from16 v5, p6

    .line 882
    move-object v10, v1

    move-object v10, v1

    .line 883
    move v15, v2

    .line 884
    move-object v2, v3

    .line 885
    move-object/from16 v1, v31

    .line 887
    move-wide/from16 v3, p4

    .line 889
    invoke-direct/range {v0 .. v8}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V

    .line 892
    :goto_3bd
    invoke-virtual {v7, v14}, Lnr6;->q(Z)V

    .line 895
    goto :goto_3c9

    .line 896
    :cond_3c1
    move-object v10, v1

    .line 897
    move v15, v2

    .line 898
    move-object/from16 v1, v31

    .line 900
    invoke-virtual {v7, v9}, Lnr6;->Z(I)V

    .line 903
    goto :goto_3bd

    .line 904
    :goto_3c9
    invoke-virtual {v7, v15}, Lnr6;->q(Z)V

    .line 907
    iget-object v2, v0, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 909
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getValuePosition()I

    .line 912
    move-result v2

    .line 913
    if-ne v2, v13, :cond_416

    .line 915
    const v2, 0xd8c9910

    .line 918
    invoke-virtual {v7, v2}, Lnr6;->Z(I)V

    .line 921
    move/from16 v8, v29

    move/from16 v8, v29

    .line 923
    invoke-static {v11, v8}, Lhpe;->m(Lhba;F)Lhba;

    .line 926
    move-result-object v2

    .line 927
    new-instance v3, Lb0h;

    .line 929
    invoke-direct {v3}, Ljava/lang/Object;-><init>()V

    .line 932
    invoke-interface {v2, v3}, Lhba;->then(Lhba;)Lhba;

    .line 935
    move-result-object v2

    .line 936
    const/4 v3, 0x0

    .line 937
    const/16 v4, 0xe

    .line 939
    const/high16 v5, 0x40800000    # 4.0f

    .line 941
    const/4 v6, 0x0

    .line 942
    const/4 v8, 0x0

    .line 943
    move-object/from16 p7, v2

    .line 945
    move/from16 p11, v3

    .line 947
    move/from16 p12, v4

    .line 949
    move/from16 p8, v5

    .line 951
    move/from16 p9, v6

    .line 953
    move/from16 p10, v8

    .line 955
    invoke-static/range {p7 .. p12}, Lgl9;->R(Lhba;FFFFI)Lhba;

    .line 958
    move-result-object v2

    .line 959
    new-instance v6, Ltrd;

    .line 961
    const/16 v3, 0x9

    .line 963
    invoke-direct {v6, v0, v10, v3}, Ltrd;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneSlider;Leia;I)V

    .line 966
    const/high16 v8, 0x40000

    .line 968
    move-wide/from16 v3, p4

    .line 970
    move-object/from16 v5, p6

    .line 972
    invoke-direct/range {v0 .. v8}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V

    .line 975
    :goto_412
    invoke-virtual {v7, v14}, Lnr6;->q(Z)V

    .line 978
    goto :goto_41a

    .line 979
    :cond_416
    invoke-virtual {v7, v12}, Lnr6;->Z(I)V

    .line 982
    goto :goto_412

    .line 983
    :goto_41a
    invoke-virtual {v7, v15}, Lnr6;->q(Z)V

    .line 986
    goto :goto_421

    .line 987
    :cond_41e
    invoke-virtual {v7}, Lnr6;->S()V

    .line 990
    :goto_421
    sget-object v0, Lblg;->a:Lblg;

    .line 992
    return-object v0
.end method
