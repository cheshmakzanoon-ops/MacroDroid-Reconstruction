.method private final SliderValueText-cf5BqRc(Ljava/lang/String;Lhba;JLwm6;Lwm6;Lyt2;I)V
    .locals 31
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "Lhba;",
            "J",
            "Lwm6;",
            "Lwm6;",
            "Lyt2;",
            "I)V"
        }
    .end annotation

    .line 1
    move-object/from16 v1, p0

    .line 3
    move/from16 v13, p8

    move/from16 v13, p8

    .line 5
    move-object/from16 v7, p7

    move-object/from16 v7, p7

    .line 7
    check-cast v7, Lnr6;

    .line 9
    const v0, 0x7f717a23

    .line 12
    invoke-virtual {v7, v0}, Lnr6;->b0(I)Lnr6;

    .line 15
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 18
    move-result-object v0

    .line 19
    sget-object v14, Lwt2;->a:Lura;

    .line 21
    if-ne v0, v14, :cond_23

    .line 23
    sget-object v0, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    .line 25
    invoke-static {v0}, Landroidx/compose/runtime/e;->e(Ljava/lang/Object;)Leia;

    .line 28
    move-result-object v0

    .line 29
    invoke-virtual {v7, v0}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 32
    :cond_23
    move-object/from16 v18, v0

    .line 34
    check-cast v18, Leia;

    .line 36
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 39
    move-result-object v0

    .line 40
    if-ne v0, v14, :cond_34

    .line 42
    invoke-static/range {p1 .. p1}, Landroidx/compose/runtime/e;->e(Ljava/lang/Object;)Leia;

    .line 45
    move-result-object v0

    .line 46
    invoke-virtual {v7, v0}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 49
    :cond_34
    move-object v8, v0

    move-object v8, v0

    .line 50
    check-cast v8, Leia;

    .line 52
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 55
    move-result-object v0

    .line 56
    if-ne v0, v14, :cond_47

    .line 58
    sget-object v0, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    .line 60
    invoke-static {v0}, Landroidx/compose/runtime/e;->e(Ljava/lang/Object;)Leia;

    .line 63
    move-result-object v0

    .line 64
    invoke-virtual {v7, v0}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 67
    :cond_47
    move-object v10, v0

    move-object v10, v0

    .line 68
    check-cast v10, Leia;

    .line 70
    invoke-direct {v1}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getSliderRange()Lci2;

    .line 73
    move-result-object v2

    .line 74
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 77
    move-result-object v0

    .line 78
    if-ne v0, v14, :cond_5d

    .line 80
    new-instance v0, Lke6;

    .line 82
    invoke-direct {v0}, Lke6;-><init>()V

    .line 85
    invoke-virtual {v7, v0}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 88
    :cond_5d
    move-object v5, v0

    move-object v5, v0

    .line 89
    check-cast v5, Lke6;

    .line 91
    invoke-static/range {v18 .. v18}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 94
    move-result v0

    .line 95
    invoke-virtual {v7, v0}, Lnr6;->h(Z)Z

    .line 98
    move-result v0

    .line 99
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 102
    move-result-object v3

    .line 103
    if-nez v0, :cond_71

    .line 105
    if-ne v3, v14, :cond_7a

    .line 107
    :cond_71
    sget-object v0, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    .line 109
    invoke-static {v0}, Landroidx/compose/runtime/e;->e(Ljava/lang/Object;)Leia;

    .line 112
    move-result-object v3

    .line 113
    invoke-virtual {v7, v3}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 116
    :cond_7a
    move-object v9, v3

    .line 117
    check-cast v9, Leia;

    .line 119
    invoke-virtual {v7, v2}, Lnr6;->g(Ljava/lang/Object;)Z

    .line 122
    move-result v0

    .line 123
    const v3, 0xe000

    .line 126
    and-int/2addr v3, v13

    .line 127
    xor-int/lit16 v3, v3, 0x6000

    .line 129
    const/16 v4, 0x4000

    .line 131
    const/4 v12, 0x0

    .line 132
    if-le v3, v4, :cond_97

    .line 134
    move-object/from16 v3, p6

    move-object/from16 v3, p6

    .line 136
    invoke-virtual {v7, v3}, Lnr6;->g(Ljava/lang/Object;)Z

    .line 139
    move-result v6

    .line 140
    if-nez v6, :cond_9d

    .line 142
    goto :goto_99

    .line 143
    :cond_97
    move-object/from16 v3, p6

    .line 145
    :goto_99
    and-int/lit16 v6, v13, 0x6000

    .line 147
    if-ne v6, v4, :cond_9f

    .line 149
    :cond_9d
    const/4 v4, 0x1

    .line 150
    goto :goto_a1

    .line 151
    :cond_9f
    move v4, v12

    move v4, v12

    .line 152
    :goto_a1
    or-int/2addr v0, v4

    .line 153
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 156
    move-result-object v4

    .line 157
    if-nez v0, :cond_ad

    .line 159
    if-ne v4, v14, :cond_ab

    .line 161
    goto :goto_ad

    .line 162
    :cond_ab
    move-object v0, v2

    .line 163
    goto :goto_ca

    .line 164
    :cond_ad
    :goto_ad
    new-instance v15, Lqrd;

    .line 166
    const/16 v21, 0x0

    .line 168
    move-object/from16 v16, v2

    .line 170
    move-object/from16 v17, v3

    .line 172
    move-object/from16 v19, v8

    move-object/from16 v19, v8

    .line 174
    move-object/from16 v20, v18

    .line 176
    move-object/from16 v18, v10

    move-object/from16 v18, v10

    .line 178
    invoke-direct/range {v15 .. v21}, Lqrd;-><init>(Lci2;Lwm6;Leia;Leia;Leia;I)V

    .line 181
    move-object/from16 v0, v16

    .line 183
    move-object/from16 v18, v20

    .line 185
    invoke-virtual {v7, v15}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 188
    move-object v4, v15

    .line 189
    :goto_ca
    check-cast v4, Lum6;

    .line 191
    sget-object v2, Lypd;->a:Lk25;

    .line 193
    invoke-virtual {v7, v2}, Lnr6;->k(Landroidx/compose/runtime/d;)Ljava/lang/Object;

    .line 196
    move-result-object v2

    .line 197
    check-cast v2, Ljava/lang/Boolean;

    .line 199
    if-nez v2, :cond_f6

    .line 201
    const v2, 0x68fc6bef

    .line 204
    invoke-virtual {v7, v2}, Lnr6;->Z(I)V

    .line 207
    sget-object v2, Lglh;->v:Ljava/util/WeakHashMap;

    .line 209
    invoke-static {v7}, Lbt9;->p(Lyt2;)Lglh;

    .line 212
    move-result-object v2

    .line 213
    iget-object v2, v2, Lglh;->c:Lc40;

    .line 215
    iget-object v2, v2, Lc40;->d:Leia;

    .line 217
    check-cast v2, Lnue;

    .line 219
    invoke-virtual {v2}, Lnue;->getValue()Ljava/lang/Object;

    .line 222
    move-result-object v2

    .line 223
    check-cast v2, Ljava/lang/Boolean;

    .line 225
    invoke-virtual {v2}, Ljava/lang/Boolean;->booleanValue()Z

    .line 228
    move-result v2

    .line 229
    invoke-virtual {v7, v12}, Lnr6;->q(Z)V

    .line 232
    goto :goto_103

    .line 233
    :cond_f6
    const v3, 0x68fc65e1

    .line 236
    invoke-virtual {v7, v3}, Lnr6;->Z(I)V

    .line 239
    invoke-virtual {v7, v12}, Lnr6;->q(Z)V

    .line 242
    invoke-virtual {v2}, Ljava/lang/Boolean;->booleanValue()Z

    .line 245
    move-result v2

    .line 246
    :goto_103
    invoke-static/range {v18 .. v18}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 249
    move-result v3

    .line 250
    invoke-virtual {v7, v3}, Lnr6;->h(Z)Z

    .line 253
    move-result v3

    .line 254
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 257
    move-result-object v6

    .line 258
    if-nez v3, :cond_113

    .line 260
    if-ne v6, v14, :cond_11c

    .line 262
    :cond_113
    sget-object v3, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    .line 264
    invoke-static {v3}, Landroidx/compose/runtime/e;->e(Ljava/lang/Object;)Leia;

    .line 267
    move-result-object v6

    .line 268
    invoke-virtual {v7, v6}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 271
    :cond_11c
    check-cast v6, Leia;

    .line 273
    invoke-static/range {v18 .. v18}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 276
    move-result v3

    .line 277
    invoke-static {v3}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    .line 280
    move-result-object v3

    .line 281
    invoke-static {v2}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    .line 284
    move-result-object v15

    .line 285
    invoke-virtual {v7, v2}, Lnr6;->h(Z)Z

    .line 288
    move-result v16

    .line 289
    invoke-virtual {v7, v6}, Lnr6;->g(Ljava/lang/Object;)Z

    .line 292
    move-result v17

    .line 293
    or-int v16, v16, v17

    .line 295
    invoke-virtual {v7, v4}, Lnr6;->g(Ljava/lang/Object;)Z

    .line 298
    move-result v17

    .line 299
    or-int v16, v16, v17

    .line 301
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 304
    move-result-object v11

    .line 305
    if-nez v16, :cond_142

    .line 307
    if-ne v11, v14, :cond_144

    .line 309
    :cond_142
    move-object v11, v15

    .line 310
    goto :goto_14c

    .line 311
    :cond_144
    move-object/from16 v17, v15

    .line 313
    move-object v15, v11

    .line 314
    move-object/from16 v11, v17

    .line 316
    move-object/from16 v17, v4

    .line 318
    goto :goto_160

    .line 319
    :goto_14c
    new-instance v15, Lzrd;

    .line 321
    const/16 v20, 0x0

    .line 323
    move/from16 v16, v2

    .line 325
    move-object/from16 v17, v4

    move-object/from16 v17, v4

    .line 327
    move-object/from16 v19, v6

    move-object/from16 v19, v6

    .line 329
    invoke-direct/range {v15 .. v20}, Lzrd;-><init>(ZLum6;Leia;Leia;Lm73;)V

    .line 332
    invoke-virtual {v7, v15}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 335
    :goto_160
    check-cast v15, Ljn6;

    .line 337
    invoke-static {v3, v11, v15, v7}, Lead;->i(Ljava/lang/Object;Ljava/lang/Object;Ljn6;Lyt2;)V

    .line 340
    sget-object v2, Lsra;->g:Ln71;

    .line 342
    invoke-static {v2, v12}, Ltg1;->c(Lrp;Z)Luz9;

    .line 345
    move-result-object v2

    .line 346
    iget-wide v3, v7, Lnr6;->T:J

    .line 348
    const/16 v6, 0x20

    .line 350
    ushr-long v15, v3, v6

    .line 352
    xor-long/2addr v3, v15

    .line 353
    long-to-int v3, v3

    .line 354
    invoke-virtual {v7}, Lnr6;->m()Lnob;

    .line 357
    move-result-object v4

    .line 358
    move-object/from16 v15, p2

    .line 360
    invoke-static {v7, v15}, Lead;->P(Lyt2;Lhba;)Lhba;

    .line 363
    move-result-object v11

    .line 364
    sget-object v16, Lkt2;->x1:Ljt2;

    .line 366
    invoke-virtual/range {v16 .. v16}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 369
    move/from16 v16, v6

    move/from16 v16, v6

    .line 371
    sget-object v6, Ljt2;->b:Ltv8;

    .line 373
    invoke-virtual {v7}, Lnr6;->d0()V

    .line 376
    iget-boolean v12, v7, Lnr6;->S:Z

    .line 378
    if-eqz v12, :cond_193

    .line 380
    invoke-virtual {v7, v6}, Lnr6;->l(Lum6;)V

    .line 383
    goto :goto_196

    .line 384
    :cond_193
    invoke-virtual {v7}, Lnr6;->m0()V

    .line 387
    :goto_196
    sget-object v12, Ljt2;->f:Le30;

    .line 389
    invoke-static {v7, v12, v2}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 392
    sget-object v2, Ljt2;->e:Le30;

    .line 394
    invoke-static {v7, v2, v4}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 397
    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 400
    move-result-object v3

    .line 401
    sget-object v4, Ljt2;->g:Le30;

    .line 403
    invoke-static {v7, v4, v3}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 406
    sget-object v3, Ljt2;->h:Lce;

    .line 408
    invoke-static {v7, v3}, Lhae;->I(Lyt2;Lwm6;)V

    .line 411
    move-object/from16 v20, v0

    .line 413
    sget-object v0, Ljt2;->d:Le30;

    .line 415
    invoke-static {v7, v0, v11}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 418
    invoke-static/range {v18 .. v18}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 421
    move-result v11

    .line 422
    move-object/from16 v21, v3

    .line 424
    sget-object v3, Leba;->a:Leba;

    .line 426
    move-object/from16 v22, v3

    move-object/from16 v22, v3

    .line 428
    const/4 v3, 0x0

    .line 429
    if-nez v11, :cond_28e

    .line 431
    const v0, 0x658179dd

    .line 434
    invoke-virtual {v7, v0}, Lnr6;->Z(I)V

    .line 437
    iget-object v0, v1, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 439
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getFontFamily()Ljava/lang/String;

    .line 442
    move-result-object v2

    .line 443
    if-nez v2, :cond_1e1

    .line 445
    const v0, 0x65840919

    .line 448
    invoke-virtual {v7, v0}, Lnr6;->Z(I)V

    .line 451
    const/4 v0, 0x0

    .line 452
    invoke-virtual {v7, v0}, Lnr6;->q(Z)V

    .line 455
    move-object v9, v3

    move-object v9, v3

    .line 456
    move-object/from16 v11, v22

    .line 458
    goto :goto_203

    .line 459
    :cond_1e1
    const v0, 0x6584091a

    .line 462
    invoke-virtual {v7, v0}, Lnr6;->Z(I)V

    .line 465
    sget-object v0, Lemd;->a:Lemd;

    .line 467
    sget v4, Lemd;->g:I

    .line 469
    shl-int/lit8 v6, v4, 0x9

    .line 471
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 474
    move-object v0, v3

    .line 475
    const/4 v3, 0x0

    .line 476
    const/4 v4, 0x0

    .line 477
    move-object v5, v7

    move-object v5, v7

    .line 478
    const/4 v7, 0x6

    .line 479
    move-object v9, v0

    move-object v9, v0

    .line 480
    move-object/from16 v11, v22

    .line 482
    invoke-static/range {v2 .. v7}, Lemd;->e(Ljava/lang/String;ZZLnr6;II)Lzf6;

    .line 485
    move-result-object v3

    .line 486
    move-object v7, v5

    .line 487
    const/4 v0, 0x0

    .line 488
    invoke-virtual {v7, v0}, Lnr6;->q(Z)V

    .line 491
    :goto_203
    if-nez v3, :cond_207

    .line 493
    sget-object v3, Lzf6;->a:Lga4;

    .line 495
    :cond_207
    move-object v10, v3

    move-object v10, v3

    .line 496
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/scene/components/SceneItem;->isEditMode()Z

    .line 499
    move-result v0

    .line 500
    if-nez v0, :cond_218

    .line 502
    invoke-direct {v1}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->isValueEditableOnTap()Z

    .line 505
    move-result v0

    .line 506
    if-eqz v0, :cond_216

    .line 508
    goto :goto_218

    .line 509
    :cond_216
    const/4 v0, 0x0

    .line 510
    goto :goto_219

    .line 511
    :cond_218
    :goto_218
    const/4 v0, 0x1

    .line 512
    :goto_219
    sget-object v12, Lgkd;->a:Lgkd;

    .line 514
    invoke-direct {v1}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->getTextSizeValue()I

    .line 517
    move-result v14

    .line 518
    iget-object v2, v1, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 520
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getTextColorVariable()Lcom/arlosoft/macrodroid/scene/data/SceneVariableData;

    .line 523
    move-result-object v2

    .line 524
    iget-object v3, v1, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 526
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getTextColor()I

    .line 529
    move-result v3

    .line 530
    invoke-virtual {v1, v2, v3}, Lcom/arlosoft/macrodroid/scene/components/SceneItem;->resolveColor(Lcom/arlosoft/macrodroid/scene/data/SceneVariableData;I)I

    .line 533
    move-result v2

    .line 534
    invoke-static {v2}, Lbq5;->e(I)J

    .line 537
    move-result-wide v16

    .line 538
    move-object/from16 v2, v20

    .line 540
    check-cast v2, Lbi2;

    .line 542
    iget v2, v2, Lbi2;->a:F

    .line 544
    float-to-int v2, v2

    .line 545
    invoke-static {v2}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 548
    move-result-object v2

    .line 549
    invoke-virtual {v2}, Ljava/lang/String;->length()I

    .line 552
    move-result v2

    .line 553
    move-object/from16 v3, v20

    .line 555
    check-cast v3, Lbi2;

    .line 557
    iget v3, v3, Lbi2;->b:F

    .line 559
    float-to-int v3, v3

    .line 560
    invoke-static {v3}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 563
    move-result-object v3

    .line 564
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    .line 567
    move-result v3

    .line 568
    invoke-static {v2, v3}, Ljava/lang/Math;->max(II)I

    .line 571
    move-result v20

    .line 572
    if-eqz v0, :cond_26c

    .line 574
    new-instance v0, Lpl;

    .line 576
    const/4 v6, 0x4

    .line 577
    move-object/from16 v2, p1

    .line 579
    move-object/from16 v3, p5

    .line 581
    move-object v5, v8

    .line 582
    move-object/from16 v4, v18

    .line 584
    invoke-direct/range {v0 .. v6}, Lpl;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Leia;Leia;I)V

    .line 587
    const/16 v1, 0xf

    .line 589
    const/4 v2, 0x0

    .line 590
    invoke-static {v11, v2, v9, v0, v1}, Lguh;->m(Lhba;ZLjava/lang/String;Lum6;I)Lhba;

    .line 593
    move-result-object v3

    .line 594
    goto :goto_26e

    .line 595
    :cond_26c
    const/4 v2, 0x0

    .line 596
    move-object v3, v11

    .line 597
    :goto_26e
    and-int/lit8 v0, v13, 0xe

    .line 599
    const/high16 v1, 0x180000

    .line 601
    or-int v9, v0, v1

    .line 603
    move-object/from16 v1, p1

    .line 605
    move-object v8, v7

    move-object v8, v7

    .line 606
    move-object v6, v10

    .line 607
    move-object v0, v12

    .line 608
    move-wide/from16 v4, v16

    .line 610
    move v10, v2

    .line 611
    move-object v7, v3

    .line 612
    move v3, v14

    .line 613
    move/from16 v2, v20

    move/from16 v2, v20

    .line 615
    invoke-virtual/range {v0 .. v9}, Lgkd;->p(Ljava/lang/String;IIJLzf6;Lhba;Lyt2;I)V

    .line 618
    move-object v1, v8

    .line 619
    invoke-virtual {v1, v10}, Lnr6;->q(Z)V

    .line 622
    move-object v7, v1

    .line 623
    const/4 v15, 0x1

    .line 624
    goto/16 :goto_3a1

    .line 626
    :cond_28e
    move-object v3, v1

    .line 627
    move-object v1, v7

    .line 628
    move-object/from16 v11, v22

    .line 630
    const/16 v19, 0x0

    .line 632
    const v7, 0x659dd819

    .line 635
    invoke-virtual {v1, v7}, Lnr6;->Z(I)V

    .line 638
    sget-object v7, Lsra;->p:Ll71;

    .line 640
    move-object/from16 v23, v5

    .line 642
    const/high16 v5, 0x40000000    # 2.0f

    .line 644
    invoke-static {v11, v5}, Lgl9;->N(Lhba;F)Lhba;

    .line 647
    move-result-object v5

    .line 648
    sget-object v11, Lkj0;->c:Lwra;

    .line 650
    const/16 v13, 0x30

    .line 652
    invoke-static {v11, v7, v1, v13}, Lrm2;->a(Ljj0;Lnp;Lyt2;I)Ltm2;

    .line 655
    move-result-object v7

    .line 656
    move-object/from16 v24, v14

    .line 658
    iget-wide v13, v1, Lnr6;->T:J

    .line 660
    ushr-long v25, v13, v16

    .line 662
    xor-long v13, v13, v25

    .line 664
    long-to-int v11, v13

    .line 665
    invoke-virtual {v1}, Lnr6;->m()Lnob;

    .line 668
    move-result-object v13

    .line 669
    invoke-static {v1, v5}, Lead;->P(Lyt2;Lhba;)Lhba;

    .line 672
    move-result-object v5

    .line 673
    invoke-virtual {v1}, Lnr6;->d0()V

    .line 676
    iget-boolean v14, v1, Lnr6;->S:Z

    .line 678
    if-eqz v14, :cond_2c8

    .line 680
    invoke-virtual {v1, v6}, Lnr6;->l(Lum6;)V

    .line 683
    goto :goto_2cb

    .line 684
    :cond_2c8
    invoke-virtual {v1}, Lnr6;->m0()V

    .line 687
    :goto_2cb
    invoke-static {v1, v12, v7}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 690
    invoke-static {v1, v2, v13}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 693
    move-object/from16 v2, v21

    move-object/from16 v2, v21

    .line 695
    invoke-static {v11, v1, v4, v1, v2}, Lku1;->v(ILnr6;Le30;Lnr6;Lce;)V

    .line 698
    invoke-static {v1, v0, v5}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 701
    iget-object v0, v3, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 703
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getTextColorVariable()Lcom/arlosoft/macrodroid/scene/data/SceneVariableData;

    .line 706
    move-result-object v0

    .line 707
    iget-object v2, v3, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->sceneSliderConfig:Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;

    .line 709
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/scene/components/SceneSliderConfig;->getTextColor()I

    .line 712
    move-result v2

    .line 713
    invoke-virtual {v3, v0, v2}, Lcom/arlosoft/macrodroid/scene/components/SceneItem;->resolveColor(Lcom/arlosoft/macrodroid/scene/data/SceneVariableData;I)I

    .line 716
    move-result v0

    .line 717
    invoke-static {v0}, Lbq5;->e(I)J

    .line 720
    move-result-wide v4

    .line 721
    new-instance v25, Landroidx/compose/foundation/text/selection/TextSelectionColors;

    .line 723
    const v0, 0x3e99999a    # 0.3f

    .line 726
    invoke-static {v4, v5, v0}, Lek2;->b(JF)J

    .line 729
    move-result-wide v28

    .line 730
    const/16 v30, 0x0

    .line 732
    move-wide/from16 v26, v4

    .line 734
    invoke-direct/range {v25 .. v30}, Landroidx/compose/foundation/text/selection/TextSelectionColors;-><init>(JJLy84;)V

    .line 737
    move-object/from16 v0, v25

    .line 739
    invoke-static {}, Landroidx/compose/foundation/text/selection/TextSelectionColorsKt;->getLocalTextSelectionColors()Landroidx/compose/runtime/d;

    .line 742
    move-result-object v2

    .line 743
    invoke-virtual {v2, v0}, Landroidx/compose/runtime/d;->a(Ljava/lang/Object;)Lmf0;

    .line 746
    move-result-object v13

    .line 747
    new-instance v0, Lrrd;

    .line 749
    move-wide/from16 v11, p3

    .line 751
    move-object v14, v1

    move-object v14, v1

    .line 752
    move-object v4, v3

    .line 753
    move-object/from16 v1, v17

    .line 755
    move-object/from16 v7, v18

    .line 757
    move-object/from16 v6, v20

    .line 759
    move-object/from16 v5, v23

    move-object/from16 v5, v23

    .line 761
    move-wide/from16 v2, v26

    .line 763
    const/4 v15, 0x1

    .line 764
    invoke-direct/range {v0 .. v12}, Lrrd;-><init>(Lum6;JLcom/arlosoft/macrodroid/scene/components/SceneSlider;Lke6;Lci2;Leia;Leia;Leia;Leia;J)V

    .line 767
    move-object v11, v5

    .line 768
    move-object/from16 v16, v6

    move-object/from16 v16, v6

    .line 770
    move-object/from16 v18, v10

    move-object/from16 v18, v10

    .line 772
    move-object v10, v7

    .line 773
    const v1, 0x36ad483

    .line 776
    invoke-static {v1, v0, v14}, Ldt9;->V(ILmn6;Lyt2;)Lnr2;

    .line 779
    move-result-object v0

    .line 780
    const/16 v1, 0x38

    .line 782
    invoke-static {v13, v0, v14, v1}, Lufg;->a(Lmf0;Ljn6;Lyt2;I)V

    .line 785
    invoke-static/range {v18 .. v18}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$7(Leia;)Z

    .line 788
    move-result v6

    .line 789
    new-instance v0, Lejd;

    .line 791
    const/4 v5, 0x3

    .line 792
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 794
    move-object/from16 v2, v16

    .line 796
    move-wide/from16 v3, v26

    .line 798
    invoke-direct/range {v0 .. v5}, Lejd;-><init>(Ljava/lang/Object;Ljava/lang/Object;JI)V

    .line 801
    const v1, 0x464b6a9b

    .line 804
    invoke-static {v1, v0, v14}, Ldt9;->V(ILmn6;Lyt2;)Lnr2;

    .line 807
    move-result-object v0

    .line 808
    const v8, 0x180006

    .line 811
    const/16 v9, 0x1e

    .line 813
    move v1, v6

    .line 814
    move-object v6, v0

    move-object v6, v0

    .line 815
    sget-object v0, Lwm2;->a:Lwm2;

    .line 817
    const/4 v2, 0x0

    .line 818
    const/4 v3, 0x0

    .line 819
    const/4 v4, 0x0

    .line 820
    const/4 v5, 0x0

    .line 821
    move-object v7, v14

    .line 822
    invoke-static/range {v0 .. v9}, Li68;->b(Lum2;ZLhba;Lug5;Lsl5;Ljava/lang/String;Lln6;Lyt2;II)V

    .line 825
    invoke-virtual {v7, v15}, Lnr6;->q(Z)V

    .line 828
    invoke-static {v10}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 831
    move-result v0

    .line 832
    invoke-static {v0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    .line 835
    move-result-object v0

    .line 836
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 839
    move-result-object v1

    .line 840
    move-object/from16 v2, v24

    .line 842
    if-ne v1, v2, :cond_37d

    .line 844
    new-instance v1, Lbsd;

    .line 846
    const/4 v9, 0x0

    .line 847
    invoke-direct {v1, v11, v10, v9}, Lbsd;-><init>(Lke6;Leia;Lm73;)V

    .line 850
    invoke-virtual {v7, v1}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 853
    :cond_37d
    check-cast v1, Ljn6;

    .line 855
    invoke-static {v7, v1, v0}, Lead;->h(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 858
    invoke-static {v10}, Lcom/arlosoft/macrodroid/scene/components/SceneSlider;->SliderValueText_cf5BqRc$lambda$1(Leia;)Z

    .line 861
    move-result v0

    .line 862
    invoke-virtual {v7}, Lnr6;->M()Ljava/lang/Object;

    .line 865
    move-result-object v1

    .line 866
    if-ne v1, v2, :cond_396

    .line 868
    new-instance v1, Lgpd;

    .line 870
    const/16 v2, 0xd

    .line 872
    invoke-direct {v1, v2, v10}, Lgpd;-><init>(ILeia;)V

    .line 875
    invoke-virtual {v7, v1}, Lnr6;->j0(Ljava/lang/Object;)V

    .line 878
    :cond_396
    check-cast v1, Lum6;

    .line 880
    const/16 v2, 0x30

    .line 882
    const/4 v10, 0x0

    .line 883
    invoke-static {v0, v1, v7, v2, v10}, Lxrh;->a(ZLum6;Lyt2;II)V

    .line 886
    invoke-virtual {v7, v10}, Lnr6;->q(Z)V

    .line 889
    :goto_3a1
    invoke-virtual {v7, v15}, Lnr6;->q(Z)V

    .line 892
    invoke-virtual {v7}, Lnr6;->s()Lukc;

    .line 895
    move-result-object v10

    .line 896
    if-eqz v10, :cond_3c6

    .line 898
    new-instance v0, Leod;

    .line 900
    const/4 v9, 0x1

    .line 901
    move-object/from16 v1, p0

    .line 903
    move-object/from16 v2, p1

    .line 905
    move-object/from16 v3, p2

    .line 907
    move-wide/from16 v4, p3

    .line 909
    move-object/from16 v6, p5

    move-object/from16 v6, p5

    .line 911
    move-object/from16 v7, p6

    move-object/from16 v7, p6

    .line 913
    move/from16 v8, p8

    move/from16 v8, p8

    .line 915
    invoke-direct/range {v0 .. v9}, Leod;-><init>(Lcom/arlosoft/macrodroid/scene/components/SceneItem;Ljava/lang/String;Lhba;JLwm6;Lwm6;II)V

    .line 918
    iput-object v0, v10, Lukc;->d:Ljn6;

    .line 920
    :cond_3c6
    return-void
.end method
