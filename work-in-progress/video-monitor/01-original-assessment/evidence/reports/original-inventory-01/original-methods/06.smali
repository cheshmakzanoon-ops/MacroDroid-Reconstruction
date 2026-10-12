.method public final invoke(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    .locals 33

    .line 1
    move-object/from16 v0, p0

    .line 3
    move-object/from16 v1, p1

    move-object/from16 v1, p1

    .line 5
    check-cast v1, Lyt2;

    .line 7
    move-object/from16 v2, p2

    move-object/from16 v2, p2

    .line 9
    check-cast v2, Ljava/lang/Integer;

    .line 11
    invoke-virtual {v2}, Ljava/lang/Integer;->intValue()I

    .line 14
    move-result v2

    .line 15
    sget-object v3, Lcom/arlosoft/macrodroid/action/activities/SelectionDialogActivity;->x:Lcom/arlosoft/macrodroid/action/activities/SelectionDialogActivity$a;

    .line 17
    and-int/lit8 v3, v2, 0xb

    .line 19
    const/4 v4, 0x0

    .line 20
    const/4 v5, 0x1

    .line 21
    const/4 v6, 0x2

    .line 22
    if-eq v3, v6, :cond_1d

    .line 24
    move v3, v5

    .line 25
    goto :goto_1e

    .line 26
    :cond_1d
    move v3, v4

    .line 27
    :goto_1e
    and-int/2addr v2, v5

    .line 28
    check-cast v1, Lnr6;

    .line 30
    invoke-virtual {v1, v2, v3}, Lnr6;->P(IZ)Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_189

    .line 36
    iget v2, v0, Li4e;->a:I

    .line 38
    invoke-static {v2}, Lbq5;->e(I)J

    .line 41
    move-result-wide v2

    .line 42
    sget-object v7, Lwyh;->e:Led2;

    .line 44
    sget-object v8, Leba;->a:Leba;

    .line 46
    invoke-static {v8, v2, v3, v7}, Lngc;->e(Lhba;JLvee;)Lhba;

    .line 49
    move-result-object v2

    .line 50
    sget-object v3, Lkj0;->c:Lwra;

    .line 52
    sget-object v7, Lsra;->o:Ll71;

    .line 54
    invoke-static {v3, v7, v1, v4}, Lrm2;->a(Ljj0;Lnp;Lyt2;I)Ltm2;

    .line 57
    move-result-object v3

    .line 58
    iget-wide v9, v1, Lnr6;->T:J

    .line 60
    const/16 v7, 0x20

    .line 62
    ushr-long v11, v9, v7

    .line 64
    xor-long/2addr v9, v11

    .line 65
    long-to-int v7, v9

    .line 66
    invoke-virtual {v1}, Lnr6;->m()Lnob;

    .line 69
    move-result-object v9

    .line 70
    invoke-static {v1, v2}, Lead;->P(Lyt2;Lhba;)Lhba;

    .line 73
    move-result-object v2

    .line 74
    sget-object v10, Lkt2;->x1:Ljt2;

    .line 76
    invoke-virtual {v10}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 79
    sget-object v10, Ljt2;->b:Ltv8;

    .line 81
    invoke-virtual {v1}, Lnr6;->d0()V

    .line 84
    iget-boolean v11, v1, Lnr6;->S:Z

    .line 86
    if-eqz v11, :cond_5f

    .line 88
    invoke-virtual {v1, v10}, Lnr6;->l(Lum6;)V

    .line 91
    goto :goto_62

    .line 92
    :cond_5f
    invoke-virtual {v1}, Lnr6;->m0()V

    .line 95
    :goto_62
    sget-object v10, Ljt2;->f:Le30;

    .line 97
    invoke-static {v1, v10, v3}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 100
    sget-object v3, Ljt2;->e:Le30;

    .line 102
    invoke-static {v1, v3, v9}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 105
    invoke-static {v7}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 108
    move-result-object v3

    .line 109
    sget-object v7, Ljt2;->g:Le30;

    .line 111
    invoke-static {v1, v7, v3}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 114
    sget-object v3, Ljt2;->h:Lce;

    .line 116
    invoke-static {v1, v3}, Lhae;->I(Lyt2;Lwm6;)V

    .line 119
    sget-object v3, Ljt2;->d:Le30;

    .line 121
    invoke-static {v1, v3, v2}, Lhae;->N(Lyt2;Ljn6;Ljava/lang/Object;)V

    .line 124
    iget-object v7, v0, Li4e;->b:Ljava/lang/String;

    .line 126
    invoke-virtual {v7}, Ljava/lang/String;->length()I

    .line 129
    move-result v2

    .line 130
    iget v3, v0, Li4e;->d:I

    .line 132
    const/high16 v9, 0x41000000    # 8.0f

    .line 134
    const/4 v10, 0x3

    .line 135
    if-lez v2, :cond_117

    .line 137
    const v2, 0x147158c8

    .line 140
    invoke-virtual {v1, v2}, Lnr6;->Z(I)V

    .line 143
    iget v2, v0, Li4e;->c:I

    .line 145
    if-eq v2, v5, :cond_9c

    .line 147
    if-eq v2, v6, :cond_9a

    .line 149
    const/4 v2, 0x5

    .line 150
    goto :goto_9d

    .line 151
    :cond_9a
    const/4 v2, 0x6

    .line 152
    goto :goto_9d

    .line 153
    :cond_9c
    move v2, v10

    .line 154
    :goto_9d
    const/16 v6, 0x16

    .line 156
    invoke-static {v6}, Lvdg;->S(I)J

    .line 159
    move-result-wide v11

    .line 160
    invoke-static {v3}, Lbq5;->e(I)J

    .line 163
    move-result-wide v13

    .line 164
    const/high16 v6, 0x41c00000    # 24.0f

    .line 166
    invoke-static {v8, v6, v9}, Lgl9;->O(Lhba;FF)Lhba;

    .line 169
    move-result-object v6

    .line 170
    sget-object v15, Lhpe;->a:Laz5;

    .line 172
    invoke-interface {v6, v15}, Lhba;->then(Lhba;)Lhba;

    .line 175
    move-result-object v6

    .line 176
    new-instance v15, Lpvf;

    .line 178
    invoke-direct {v15, v2}, Lpvf;-><init>(I)V

    .line 181
    const/16 v29, 0x0

    .line 183
    const v30, 0x1fdf0

    .line 186
    move v2, v9

    .line 187
    move-wide/from16 v31, v13

    .line 189
    move v14, v10

    move v14, v10

    .line 190
    move-wide/from16 v9, v31

    .line 192
    const/4 v13, 0x0

    .line 193
    move/from16 v16, v14

    move/from16 v16, v14

    .line 195
    const/4 v14, 0x0

    .line 196
    move-object/from16 v18, v15

    move-object/from16 v18, v15

    .line 198
    const/4 v15, 0x0

    .line 199
    move/from16 v19, v16

    move/from16 v19, v16

    .line 201
    const-wide/16 v16, 0x0

    .line 203
    move/from16 v21, v19

    .line 205
    const-wide/16 v19, 0x0

    .line 207
    move/from16 v22, v21

    move/from16 v22, v21

    .line 209
    const/16 v21, 0x0

    .line 211
    move/from16 v23, v22

    move/from16 v23, v22

    .line 213
    const/16 v22, 0x0

    .line 215
    move/from16 v24, v23

    .line 217
    const/16 v23, 0x0

    .line 219
    move/from16 v25, v24

    move/from16 v25, v24

    .line 221
    const/16 v24, 0x0

    .line 223
    move/from16 v26, v25

    .line 225
    const/16 v25, 0x0

    .line 227
    move/from16 v27, v26

    .line 229
    const/16 v26, 0x0

    .line 231
    const/16 v28, 0xc30

    .line 233
    move/from16 v31, v27

    move/from16 v31, v27

    .line 235
    move-object/from16 v27, v1

    .line 237
    move/from16 v1, v31

    move/from16 v1, v31

    .line 239
    move-object/from16 v31, v8

    move-object/from16 v31, v8

    .line 241
    move-object v8, v6

    .line 242
    move-object/from16 v6, v31

    move-object/from16 v6, v31

    .line 244
    invoke-static/range {v7 .. v30}, Lfyf;->b(Ljava/lang/String;Lhba;JJLah6;Lfh6;Lzf6;JLpvf;JIZIILwm6;Lezf;Lyt2;III)V

    .line 247
    move-object/from16 v22, v7

    .line 249
    move-object/from16 v7, v27

    .line 251
    :goto_113
    invoke-virtual {v7, v4}, Lnr6;->q(Z)V

    .line 254
    goto :goto_127

    .line 255
    :cond_117
    move-object/from16 v22, v7

    move-object/from16 v22, v7

    .line 257
    move-object v6, v8

    .line 258
    move v2, v9

    .line 259
    move-object v7, v1

    move-object v7, v1

    .line 260
    move v1, v10

    .line 261
    const v8, 0x13b394a2

    .line 264
    invoke-virtual {v7, v8}, Lnr6;->Z(I)V

    .line 267
    goto :goto_113

    .line 268
    :goto_127
    iget v4, v0, Li4e;->e:I

    .line 270
    const/4 v9, 0x0

    .line 271
    if-ne v4, v1, :cond_135

    .line 273
    invoke-virtual/range {v22 .. v22}, Ljava/lang/String;->length()I

    .line 276
    move-result v8

    .line 277
    if-nez v8, :cond_135

    .line 279
    move v10, v9

    move v10, v9

    .line 280
    goto :goto_137

    .line 281
    :cond_135
    move v10, v2

    move v10, v2

    .line 282
    :goto_137
    if-ne v4, v1, :cond_13b

    .line 284
    move v12, v9

    .line 285
    goto :goto_13d

    .line 286
    :cond_13b
    move v12, v2

    move v12, v2

    .line 287
    :goto_13d
    const/4 v11, 0x0

    .line 288
    const/4 v13, 0x5

    .line 289
    const/4 v9, 0x0

    .line 290
    move-object v8, v6

    .line 291
    invoke-static/range {v8 .. v13}, Lgl9;->R(Lhba;FFFFI)Lhba;

    .line 294
    move-result-object v1

    .line 295
    new-instance v15, Lj4e;

    .line 297
    iget-object v10, v0, Li4e;->f:Ljava/util/List;

    .line 299
    iget-object v11, v0, Li4e;->g:Lcom/arlosoft/macrodroid/action/activities/SelectionDialogActivity;

    .line 301
    iget-object v13, v0, Li4e;->h:Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;

    .line 303
    iget-object v14, v0, Li4e;->i:Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;

    .line 305
    move-object v9, v15

    .line 306
    iget-object v15, v0, Li4e;->j:Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;

    .line 308
    iget-object v2, v0, Li4e;->k:Lcom/arlosoft/macrodroid/triggers/Trigger;

    .line 310
    iget v6, v0, Li4e;->l:I

    .line 312
    iget-object v8, v0, Li4e;->m:Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 314
    iget-boolean v12, v0, Li4e;->n:Z

    .line 316
    iget-object v0, v0, Li4e;->o:Ljava/util/Stack;

    .line 318
    move-object/from16 v20, v0

    move-object/from16 v20, v0

    .line 320
    move-object/from16 v16, v2

    .line 322
    move/from16 v21, v3

    .line 324
    move/from16 v17, v6

    .line 326
    move-object/from16 v18, v8

    .line 328
    move/from16 v19, v12

    .line 330
    move v12, v4

    .line 331
    invoke-direct/range {v9 .. v22}, Lj4e;-><init>(Ljava/util/List;Lcom/arlosoft/macrodroid/action/activities/SelectionDialogActivity;ILcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;Lcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;Lcom/arlosoft/macrodroid/triggers/Trigger;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;ILjava/lang/String;)V

    .line 334
    const/16 v17, 0x0

    .line 336
    const/16 v18, 0x1fe

    .line 338
    const/4 v8, 0x0

    .line 339
    move-object v15, v9

    move-object v15, v9

    .line 340
    const/4 v9, 0x0

    .line 341
    const/4 v10, 0x0

    .line 342
    const/4 v11, 0x0

    .line 343
    const/4 v12, 0x0

    .line 344
    const/4 v13, 0x0

    .line 345
    const/4 v14, 0x0

    .line 346
    move-object/from16 v16, v7

    .line 348
    move-object v7, v1

    .line 349
    invoke-static/range {v7 .. v18}, Ljtg;->c(Lhba;Lz39;Lfdb;Ljj0;Lnp;La46;ZLzbb;Lwm6;Lyt2;II)V

    .line 352
    move-object/from16 v7, v16

    move-object/from16 v7, v16

    .line 354
    invoke-virtual {v7, v5}, Lnr6;->q(Z)V

    .line 357
    goto :goto_18d

    .line 358
    :cond_189
    move-object v7, v1

    .line 359
    invoke-virtual {v7}, Lnr6;->S()V

    .line 362
    :goto_18d
    sget-object v0, Lblg;->a:Lblg;

    .line 364
    return-object v0
.end method
