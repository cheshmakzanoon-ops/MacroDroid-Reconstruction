.method public static f(Landroid/content/Context;Landroid/content/Intent;)V
    .locals 44

    .line 1
    move-object/from16 v1, p0

    .line 3
    move-object/from16 v0, p1

    move-object/from16 v0, p1

    .line 5
    const-string v2, "FromUri"

    .line 7
    invoke-virtual {v0, v2}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 10
    move-result-object v2

    .line 11
    const-string v3, "ioTmr"

    const-string v3, "ToUri"

    .line 13
    invoke-virtual {v0, v3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 16
    move-result-object v3

    .line 17
    const-string v4, "FilePattern"

    .line 19
    invoke-virtual {v0, v4}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 22
    move-result-object v4

    .line 23
    const-string v5, "eeaFolPtdtror"

    const-string v5, "FolderPattern"

    .line 25
    invoke-virtual {v0, v5}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 28
    move-result-object v8

    .line 29
    const-string v5, "FileExtensions"

    .line 31
    invoke-virtual {v0, v5}, Landroid/content/Intent;->getStringArrayExtra(Ljava/lang/String;)[Ljava/lang/String;

    .line 34
    move-result-object v5

    .line 35
    const-string v6, "fromPath"

    .line 37
    invoke-virtual {v0, v6}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 40
    move-result-object v6

    .line 41
    const-string v7, "dfNombaerl"

    const-string v7, "folderName"

    .line 43
    invoke-virtual {v0, v7}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 46
    move-result-object v7

    .line 47
    const-string v9, "com.arlosoft.macrodroid.MACRO_NAME"

    .line 49
    invoke-virtual {v0, v9}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 52
    move-result-object v9

    .line 53
    const-string v10, "lfVariableName"

    .line 55
    invoke-virtual {v0, v10}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 58
    move-result-object v10

    .line 59
    const-string v11, "MacroGuid"

    .line 61
    const-wide/16 v12, 0x0

    .line 63
    invoke-virtual {v0, v11, v12, v13}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 66
    move-result-wide v14

    .line 67
    invoke-static {v14, v15}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 70
    move-result-object v11

    .line 71
    sget-object v16, Lcom/arlosoft/macrodroid/macro/b;->k:Lvq9;

    .line 73
    invoke-virtual/range {v16 .. v16}, Lvq9;->a()Lcom/arlosoft/macrodroid/macro/b;

    .line 76
    move-result-object v12

    .line 77
    invoke-virtual {v12, v14, v15}, Lcom/arlosoft/macrodroid/macro/b;->J(J)Lcom/arlosoft/macrodroid/macro/Macro;

    .line 80
    move-result-object v12

    .line 81
    if-nez v12, :cond_6c

    .line 83
    new-instance v0, Ljava/lang/StringBuilder;

    .line 85
    const-string v1, "File Operation failed: Could not find macro with GUID: "

    .line 87
    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 90
    invoke-virtual {v0, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 93
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 96
    move-result-object v0

    .line 97
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 100
    return-void

    .line 101
    :cond_6c
    const-string v11, "selectableItemGuid"

    .line 103
    move-object v15, v3

    .line 104
    move-object/from16 v16, v4

    .line 106
    const-wide/16 v13, 0x0

    .line 108
    invoke-virtual {v0, v11, v13, v14}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 111
    move-result-wide v3

    .line 112
    invoke-virtual {v12, v3, v4}, Lcom/arlosoft/macrodroid/macro/Macro;->findChildByGUID(J)Lcom/arlosoft/macrodroid/common/SelectableItem;

    .line 115
    move-result-object v3

    .line 116
    check-cast v3, Lcom/arlosoft/macrodroid/action/Action;

    .line 118
    if-nez v3, :cond_97

    .line 120
    new-instance v1, Ljava/lang/StringBuilder;

    .line 122
    const-string v2, "oaflaouinio oFtlch nedtte tip iw-ieOf ncdi   i:urdn d a"

    const-string v2, "File Operation failed - could not find action with id: "

    .line 124
    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 127
    invoke-virtual {v0, v11, v13, v14}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 130
    move-result-wide v2

    .line 131
    invoke-virtual {v1, v2, v3}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 134
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 137
    move-result-object v0

    .line 138
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 141
    return-void

    .line 142
    :cond_97
    const-string/jumbo v4, "spsTte"

    const-string v4, "IsTest"

    .line 144
    const/4 v11, 0x0

    .line 145
    invoke-virtual {v0, v4, v11}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 148
    move-result v13

    .line 149
    invoke-virtual {v0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 152
    move-result-object v4

    .line 153
    const-string v14, "NextActionIndex"

    .line 155
    invoke-virtual {v4, v14}, Landroid/os/BaseBundle;->getInt(Ljava/lang/String;)I

    .line 158
    move-result v19

    .line 159
    const-string v4, "ite_n_ncqbxtkcaoo"

    const-string v4, "block_next_action"

    .line 161
    invoke-virtual {v0, v4, v11}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 164
    move-result v14

    .line 165
    invoke-virtual {v0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 168
    move-result-object v4

    .line 169
    const-string v11, "TriggerContextInfo"

    .line 171
    invoke-virtual {v4, v11}, Landroid/os/Bundle;->getParcelable(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 174
    move-result-object v4

    .line 175
    move-object/from16 v20, v4

    .line 177
    check-cast v20, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 179
    const-string v4, "musiofm_orsce_era"

    const-string v4, "resume_macro_info"

    .line 181
    invoke-virtual {v0, v4}, Landroid/content/Intent;->getParcelableExtra(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 184
    move-result-object v4

    .line 185
    move-object/from16 v23, v4

    .line 187
    check-cast v23, Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;

    .line 189
    const-string v4, "force_not_enabled"

    .line 191
    const/4 v11, 0x0

    .line 192
    invoke-virtual {v0, v4, v11}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 195
    move-result v21

    .line 196
    const-string v4, "SkipEndifIndex"

    .line 198
    invoke-virtual {v0, v4}, Landroid/content/Intent;->hasExtra(Ljava/lang/String;)Z

    .line 201
    move-result v11

    .line 202
    if-eqz v11, :cond_eb

    .line 204
    invoke-virtual {v0, v4}, Landroid/content/Intent;->getSerializableExtra(Ljava/lang/String;)Ljava/io/Serializable;

    .line 207
    move-result-object v4

    .line 208
    check-cast v4, Ljava/util/ArrayList;

    .line 210
    invoke-static {v4}, Lhtg;->d(Ljava/util/ArrayList;)Ljava/util/Stack;

    .line 213
    move-result-object v4

    .line 214
    :goto_e6
    move-object/from16 v22, v4

    move-object/from16 v22, v4

    .line 216
    goto :goto_f1

    .line 217
    :cond_eb
    new-instance v4, Ljava/util/Stack;

    .line 219
    invoke-direct {v4}, Ljava/util/Stack;-><init>()V

    .line 222
    goto :goto_e6

    .line 223
    :goto_f1
    const-string v4, "lfDictionaryKeys"

    .line 225
    invoke-virtual {v0, v4}, Landroid/content/Intent;->getParcelableExtra(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 228
    move-result-object v4

    .line 229
    check-cast v4, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 231
    const-string v11, "lfOutputType"

    .line 233
    move-object/from16 v17, v4

    move-object/from16 v17, v4

    .line 235
    const/4 v4, 0x0

    .line 236
    invoke-virtual {v0, v11, v4}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 239
    move-result v11

    .line 240
    const-string v4, "lramyairfaeVNrAelba"

    const-string v4, "lfArrayVariableName"

    .line 242
    invoke-virtual {v0, v4}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 245
    move-result-object v4

    .line 246
    move-object/from16 v18, v12

    .line 248
    const-string v12, "lfSortBy"

    .line 250
    move/from16 v24, v13

    .line 252
    const/4 v13, 0x0

    .line 253
    invoke-virtual {v0, v12, v13}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 256
    move-result v12

    .line 257
    const-string v13, "lfSortAscending"

    .line 259
    move/from16 v25, v14

    .line 261
    const/4 v14, 0x1

    .line 262
    invoke-virtual {v0, v13, v14}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 265
    move-result v13

    .line 266
    const-string v14, "option"

    .line 268
    move/from16 v27, v13

    .line 270
    const/4 v13, 0x0

    .line 271
    invoke-virtual {v0, v14, v13}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 274
    move-result v14

    .line 275
    const-string v13, "fileOption"

    .line 277
    move-object/from16 v28, v15

    move-object/from16 v28, v15

    .line 279
    const/4 v15, -0x1

    .line 280
    invoke-virtual {v0, v13, v15}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 283
    move-result v13

    .line 284
    move-object/from16 v29, v10

    move-object/from16 v29, v10

    .line 286
    const-string v10, "conflictMode"

    .line 288
    invoke-virtual {v0, v10, v15}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 291
    move-result v10

    .line 292
    const-string v15, "cfxcooenPilift"

    const-string v15, "conflictPrefix"

    .line 294
    invoke-virtual {v0, v15}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 297
    move-result-object v15

    .line 298
    invoke-static {v2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 301
    move-result-object v0

    .line 302
    invoke-static {v1, v0}, Lzr4;->j(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 305
    move-result-object v30

    .line 306
    if-nez v30, :cond_179

    .line 308
    new-instance v0, Ljava/lang/Exception;

    .line 310
    const-string v1, "eoll2b1frFaOo rVn s piemiintlriD :"

    const-string v1, "FileOperationV21 fromDir is null: "

    .line 312
    invoke-static {v1, v2}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 315
    move-result-object v1

    .line 316
    invoke-direct {v0, v1}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    .line 319
    invoke-static {v0}, Lsz5;->e(Ljava/lang/Throwable;)V

    .line 322
    new-instance v0, Ljava/lang/StringBuilder;

    .line 324
    const-string v1, "File operation failure fromDir is null: "

    .line 326
    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 329
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 332
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 335
    move-result-object v0

    .line 336
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 339
    if-eqz v25, :cond_828

    .line 341
    if-nez v24, :cond_828

    .line 343
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 346
    return-void

    .line 347
    :cond_179
    invoke-virtual/range {v30 .. v30}, Lzr4;->f()Z

    .line 350
    move-result v31

    .line 351
    if-nez v31, :cond_1ad

    .line 353
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->e(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 356
    move-result-object v30

    .line 357
    if-eqz v30, :cond_191

    .line 359
    invoke-virtual/range {v30 .. v30}, Lzr4;->f()Z

    .line 362
    move-result v0

    .line 363
    if-nez v0, :cond_18c

    .line 365
    goto :goto_191

    .line 366
    :cond_18c
    move-object/from16 v2, v30

    .line 368
    move/from16 v30, v10

    .line 370
    goto :goto_1dd

    .line 371
    :cond_191
    :goto_191
    new-instance v0, Ljava/lang/StringBuilder;

    .line 373
    const-string v2, "File operation failed - from dir does not exist or is not accessible: "

    .line 375
    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 378
    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 381
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 384
    move-result-object v0

    .line 385
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 388
    invoke-static {v1, v9}, Lcxa;->c(Landroid/content/Context;Ljava/lang/String;)V

    .line 391
    if-eqz v25, :cond_828

    .line 393
    if-nez v24, :cond_828

    .line 395
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 398
    return-void

    .line 399
    :cond_1ad
    invoke-virtual/range {v30 .. v30}, Lzr4;->a()Z

    .line 402
    move-result v31

    .line 403
    if-nez v31, :cond_18c

    .line 405
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->e(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 408
    move-result-object v30

    .line 409
    if-eqz v30, :cond_1bf

    .line 411
    invoke-virtual/range {v30 .. v30}, Lzr4;->a()Z

    .line 414
    move-result v0

    .line 415
    if-nez v0, :cond_18c

    .line 417
    :cond_1bf
    const-string v0, ", "

    .line 419
    const-string v3, "]"

    .line 421
    const-string v4, "/CeatruM  aRoO/r/nre o[/dcnytF di"

    const-string v4, "Cannot read \'FROM\' directory: ["

    .line 423
    invoke-static {v4, v6, v0, v2, v3}, Lx9f;->E(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 426
    move-result-object v0

    .line 427
    invoke-virtual/range {v18 .. v18}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 430
    move-result-wide v2

    .line 431
    invoke-static {v2, v3, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 434
    invoke-static {v1, v9}, Lcxa;->c(Landroid/content/Context;Ljava/lang/String;)V

    .line 437
    if-eqz v25, :cond_828

    .line 439
    if-nez v24, :cond_828

    .line 441
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 444
    return-void

    .line 445
    :goto_1dd
    if-eqz v28, :cond_1e8

    .line 447
    invoke-static/range {v28 .. v28}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 450
    move-result-object v0

    .line 451
    move-object/from16 v32, v0

    move-object/from16 v32, v0

    .line 453
    goto :goto_1ea

    .line 454
    :cond_1e8
    const/16 v32, 0x0

    .line 456
    :goto_1ea
    const/4 v0, 0x3

    .line 457
    if-ne v14, v0, :cond_20c

    .line 459
    if-nez v7, :cond_1fb

    .line 461
    const-string v0, "erlu FrpsO Fien  no emalddioieatfllle :pan"

    const-string v0, "File Operation failed: Folder name is null"

    .line 463
    invoke-virtual/range {v18 .. v18}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 466
    move-result-wide v1

    .line 467
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 470
    return-void

    .line 471
    :cond_1fb
    invoke-virtual {v2, v7}, Lzr4;->g(Ljava/lang/String;)Lzr4;

    .line 474
    move-result-object v0

    .line 475
    if-nez v0, :cond_204

    .line 477
    invoke-virtual {v2, v7}, Lzr4;->c(Ljava/lang/String;)Lzr4;

    .line 480
    :cond_204
    if-eqz v25, :cond_828

    .line 482
    if-nez v24, :cond_828

    .line 484
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 487
    return-void

    .line 488
    :cond_20c
    move-object/from16 v7, v18

    move-object/from16 v7, v18

    .line 490
    move-object/from16 v10, v20

    .line 492
    move-object/from16 v18, v15

    .line 494
    const-string v0, "."

    const-string v0, "."

    .line 496
    const/4 v15, 0x4

    .line 497
    if-ne v14, v15, :cond_530

    .line 499
    invoke-virtual {v2}, Lzr4;->n()Landroid/net/Uri;

    .line 502
    move-result-object v2

    .line 503
    if-eqz v16, :cond_229

    .line 505
    new-instance v6, Lzih;

    .line 507
    move-object/from16 v9, v16

    .line 509
    invoke-direct {v6, v9}, Lzih;-><init>(Ljava/lang/String;)V

    .line 512
    goto :goto_22a

    .line 513
    :cond_229
    const/4 v6, 0x0

    .line 514
    :goto_22a
    if-eqz v8, :cond_232

    .line 516
    new-instance v9, Lzih;

    .line 518
    invoke-direct {v9, v8}, Lzih;-><init>(Ljava/lang/String;)V

    .line 521
    goto :goto_233

    .line 522
    :cond_232
    const/4 v9, 0x0

    .line 523
    :goto_233
    const/4 v8, 0x6

    .line 524
    if-eq v13, v8, :cond_23e

    .line 526
    const/4 v8, 0x7

    .line 527
    if-eq v13, v8, :cond_23e

    .line 529
    if-eqz v9, :cond_23c

    .line 531
    goto :goto_23e

    .line 532
    :cond_23c
    const/4 v8, 0x0

    .line 533
    goto :goto_23f

    .line 534
    :cond_23e
    :goto_23e
    const/4 v8, 0x1

    .line 535
    :goto_23f
    new-instance v13, Ljava/util/ArrayList;

    .line 537
    invoke-direct {v13}, Ljava/util/ArrayList;-><init>()V

    .line 540
    invoke-static {v1, v2}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->g(Landroid/content/Context;Landroid/net/Uri;)Ljava/util/ArrayList;

    .line 543
    move-result-object v2

    .line 544
    invoke-virtual {v2}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 547
    move-result-object v2

    .line 548
    :goto_24c
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    .line 551
    move-result v14

    .line 552
    if-eqz v14, :cond_31e

    .line 554
    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 557
    move-result-object v14

    .line 558
    check-cast v14, Lyx5;

    .line 560
    iget-object v15, v14, Lyx5;->b:Ljava/lang/String;

    .line 562
    move-object/from16 v18, v2

    .line 564
    iget-object v2, v14, Lyx5;->a:Landroid/net/Uri;

    .line 566
    move/from16 v28, v8

    .line 568
    iget-boolean v8, v14, Lyx5;->f:Z

    .line 570
    if-nez v15, :cond_26a

    .line 572
    move-object/from16 v2, v18

    .line 574
    move/from16 v8, v28

    .line 576
    :goto_268
    const/4 v15, 0x4

    .line 577
    goto :goto_24c

    .line 578
    :cond_26a
    if-eqz v28, :cond_29f

    .line 580
    if-nez v8, :cond_27a

    .line 582
    move-object/from16 v31, v6

    move-object/from16 v31, v6

    .line 584
    move/from16 v30, v8

    move/from16 v30, v8

    .line 586
    :cond_276
    :goto_276
    move-object/from16 v33, v9

    .line 588
    const/4 v8, 0x0

    .line 589
    goto :goto_2da

    .line 590
    :cond_27a
    if-eqz v9, :cond_295

    .line 592
    move/from16 v30, v8

    move/from16 v30, v8

    .line 594
    :try_start_280
    new-instance v8, Ljava/io/File;

    .line 596
    invoke-direct {v8, v15}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 599
    invoke-virtual {v9, v8}, Lzih;->accept(Ljava/io/File;)Z

    .line 602
    move-result v8

    .line 603
    :goto_289
    move-object/from16 v31, v6

    move-object/from16 v31, v6

    .line 605
    move-object/from16 v33, v9

    move-object/from16 v33, v9

    .line 607
    goto :goto_2da

    .line 608
    :catch_292
    move-object/from16 v31, v6

    .line 610
    goto :goto_276

    .line 611
    :cond_295
    move/from16 v30, v8

    .line 613
    :cond_297
    move-object/from16 v31, v6

    move-object/from16 v31, v6

    .line 615
    move-object/from16 v33, v9

    .line 617
    :goto_29d
    const/4 v8, 0x1

    .line 618
    goto :goto_2da

    .line 619
    :cond_29f
    move/from16 v30, v8

    .line 621
    if-eqz v6, :cond_2ad

    .line 623
    new-instance v8, Ljava/io/File;

    .line 625
    invoke-direct {v8, v15}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 628
    invoke-virtual {v6, v8}, Lzih;->accept(Ljava/io/File;)Z

    .line 631
    move-result v8
    :try_end_2ac
    .catch Ljava/lang/Exception; {:try_start_280 .. :try_end_2ac} :catch_292

    .line 632
    goto :goto_289

    .line 633
    :cond_2ad
    if-eqz v5, :cond_297

    .line 635
    array-length v8, v5

    .line 636
    if-lez v8, :cond_297

    .line 638
    invoke-virtual {v15}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;

    .line 641
    move-result-object v8

    .line 642
    array-length v15, v5

    .line 643
    move-object/from16 v31, v6

    .line 645
    const/4 v6, 0x0

    .line 646
    :goto_2ba
    if-ge v6, v15, :cond_276

    .line 648
    move/from16 v32, v6

    .line 650
    aget-object v6, v5, v32

    .line 652
    move-object/from16 v33, v9

    .line 654
    new-instance v9, Ljava/lang/StringBuilder;

    .line 656
    invoke-direct {v9, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 659
    invoke-virtual {v9, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 662
    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 665
    move-result-object v6

    .line 666
    invoke-virtual {v8, v6}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    .line 669
    move-result v6

    .line 670
    if-eqz v6, :cond_2d5

    .line 672
    goto :goto_29d

    .line 673
    :cond_2d5
    add-int/lit8 v6, v32, 0x1

    .line 675
    move-object/from16 v9, v33

    .line 677
    goto :goto_2ba

    .line 678
    :goto_2da
    if-nez v8, :cond_2e7

    .line 680
    :goto_2dc
    move-object/from16 v2, v18

    .line 682
    move/from16 v8, v28

    move/from16 v8, v28

    .line 684
    move-object/from16 v6, v31

    .line 686
    move-object/from16 v9, v33

    .line 688
    goto :goto_268

    .line 689
    :cond_2e7
    if-eqz v30, :cond_2f3

    .line 691
    const/4 v6, 0x0

    .line 692
    invoke-static {v1, v2, v6}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->d(Landroid/content/Context;Landroid/net/Uri;I)Ljava/util/ArrayList;

    .line 695
    move-result-object v8

    .line 696
    move-object/from16 v42, v8

    .line 698
    const/16 v36, 0x0

    .line 700
    goto :goto_2fd

    .line 701
    :cond_2f3
    iget-wide v8, v14, Lyx5;->d:J

    .line 703
    invoke-static {v8, v9}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 706
    move-result-object v6

    .line 707
    move-object/from16 v36, v6

    .line 709
    const/16 v42, 0x0

    .line 711
    :goto_2fd
    new-instance v34, Luw5;

    .line 713
    iget-object v6, v14, Lyx5;->b:Ljava/lang/String;

    .line 715
    iget-boolean v8, v14, Lyx5;->f:Z

    .line 717
    move/from16 v37, v8

    .line 719
    iget-wide v8, v14, Lyx5;->e:J

    .line 721
    iget-object v14, v14, Lyx5;->c:Ljava/lang/String;

    .line 723
    invoke-virtual {v2}, Landroid/net/Uri;->toString()Ljava/lang/String;

    .line 726
    move-result-object v41

    .line 727
    move-object/from16 v35, v6

    .line 729
    move-wide/from16 v38, v8

    .line 731
    move-object/from16 v40, v14

    move-object/from16 v40, v14

    .line 733
    invoke-direct/range {v34 .. v42}, Luw5;-><init>(Ljava/lang/String;Ljava/lang/Long;ZJLjava/lang/String;Ljava/lang/String;Ljava/util/List;)V

    .line 736
    move-object/from16 v2, v34

    .line 738
    invoke-virtual {v13, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 741
    goto :goto_2dc

    .line 742
    :cond_31e
    const-string v0, " areftrnq ebvaia el a  aiilnytn nl,alsaokr smvbCsia"

    const-string v0, "Cannot save file list, array variable name is blank"

    .line 744
    const/4 v2, 0x1

    .line 745
    if-ne v11, v2, :cond_4b3

    .line 747
    invoke-static {v1, v7, v10, v4}, Lsr9;->l(Landroid/content/Context;Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Ljava/lang/String;)Ljava/lang/String;

    .line 750
    move-result-object v1

    .line 751
    invoke-virtual {v1}, Ljava/lang/String;->isEmpty()Z

    .line 754
    move-result v4

    .line 755
    if-eqz v4, :cond_338

    .line 757
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 760
    move-result-wide v1

    .line 761
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 764
    goto/16 :goto_521

    .line 766
    :cond_338
    invoke-virtual {v3, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 769
    move-result-object v0

    .line 770
    if-nez v0, :cond_34b

    .line 772
    new-instance v0, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 774
    const/4 v4, 0x5

    .line 775
    invoke-direct {v0, v4, v1, v2}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;-><init>(ILjava/lang/String;Z)V

    .line 778
    invoke-virtual {v3, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->addVariable(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 781
    invoke-virtual {v3, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 784
    move-result-object v0

    .line 785
    :cond_34b
    if-nez v0, :cond_35c

    .line 787
    const-string v0, "Cannot save file list, array variable not available: "

    .line 789
    invoke-virtual {v0, v1}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 792
    move-result-object v0

    .line 793
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 796
    move-result-wide v1

    .line 797
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 800
    goto/16 :goto_521

    .line 802
    :cond_35c
    new-instance v1, Ljava/util/ArrayList;

    .line 804
    invoke-direct {v1, v13}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 807
    new-instance v2, Lw21;

    .line 809
    const/16 v4, 0x8

    .line 811
    invoke-direct {v2, v4}, Lw21;-><init>(I)V

    .line 814
    invoke-static {v2}, Lj$/util/Comparator$-CC;->comparing(Ljava/util/function/Function;)Ljava/util/Comparator;

    .line 817
    move-result-object v2

    .line 818
    const/4 v4, 0x1

    .line 819
    if-eq v12, v4, :cond_37f

    .line 821
    const/4 v5, 0x2

    .line 822
    if-eq v12, v5, :cond_375

    .line 824
    move-object v4, v2

    move-object v4, v2

    .line 825
    goto :goto_389

    .line 826
    :cond_375
    new-instance v5, Lxx5;

    .line 828
    invoke-direct {v5, v4}, Lxx5;-><init>(I)V

    .line 831
    invoke-static {v5}, Lj$/util/Comparator$-CC;->comparingLong(Ljava/util/function/ToLongFunction;)Ljava/util/Comparator;

    .line 834
    move-result-object v4

    .line 835
    goto :goto_389

    .line 836
    :cond_37f
    new-instance v4, Lxx5;

    .line 838
    const/4 v13, 0x0

    .line 839
    invoke-direct {v4, v13}, Lxx5;-><init>(I)V

    .line 842
    invoke-static {v4}, Lj$/util/Comparator$-CC;->comparingLong(Ljava/util/function/ToLongFunction;)Ljava/util/Comparator;

    .line 845
    move-result-object v4

    .line 846
    :goto_389
    if-nez v27, :cond_38f

    .line 848
    invoke-static {v4}, Lj$/util/Comparator$-EL;->reversed(Ljava/util/Comparator;)Ljava/util/Comparator;

    .line 851
    move-result-object v4

    .line 852
    :cond_38f
    if-nez v12, :cond_392

    .line 854
    goto :goto_396

    .line 855
    :cond_392
    invoke-static {v4, v2}, Lj$/util/Comparator$-EL;->thenComparing(Ljava/util/Comparator;Ljava/util/Comparator;)Ljava/util/Comparator;

    .line 858
    move-result-object v4

    .line 859
    :goto_396
    invoke-static {v1, v4}, Lj$/util/List$-EL;->sort(Ljava/util/List;Ljava/util/Comparator;)V

    .line 862
    new-instance v2, Ljava/util/ArrayList;

    .line 864
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 867
    const/4 v11, 0x0

    .line 868
    :goto_39f
    invoke-virtual {v1}, Ljava/util/ArrayList;->size()I

    .line 871
    move-result v4

    .line 872
    if-ge v11, v4, :cond_4a3

    .line 874
    invoke-virtual {v1, v11}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    .line 877
    move-result-object v4

    .line 878
    check-cast v4, Luw5;

    .line 880
    new-instance v5, Ljava/util/ArrayList;

    .line 882
    invoke-direct {v5}, Ljava/util/ArrayList;-><init>()V

    .line 885
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 887
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;

    .line 889
    iget-object v9, v4, Luw5;->a:Ljava/lang/String;

    .line 891
    iget-object v12, v4, Luw5;->g:Ljava/util/List;

    .line 893
    iget-object v13, v4, Luw5;->e:Ljava/lang/String;

    .line 895
    iget-wide v14, v4, Luw5;->d:J

    .line 897
    move-object/from16 p0, v1

    .line 899
    iget-object v1, v4, Luw5;->b:Ljava/lang/Long;

    .line 901
    move-object/from16 v16, v1

    move-object/from16 v16, v1

    .line 903
    const/4 v1, 0x0

    .line 904
    invoke-direct {v8, v9, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;-><init>(Ljava/lang/String;Ljava/util/List;)V

    .line 907
    const-string v9, "filename"

    .line 909
    invoke-direct {v6, v9, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 912
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 915
    if-eqz v16, :cond_3ee

    .line 917
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 919
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    .line 921
    move v9, v11

    move v9, v11

    .line 922
    move-object/from16 v17, v12

    .line 924
    invoke-virtual/range {v16 .. v16}, Ljava/lang/Long;->longValue()J

    .line 927
    move-result-wide v11

    .line 928
    invoke-direct {v8, v11, v12, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;-><init>(JLjava/util/List;)V

    .line 931
    const-string/jumbo v11, "yisez_sebs"

    const-string/jumbo v11, "size_bytes"

    .line 933
    invoke-direct {v6, v11, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 936
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 939
    goto :goto_3f2

    .line 940
    :cond_3ee
    move v9, v11

    move v9, v11

    .line 941
    move-object/from16 v17, v12

    .line 943
    :goto_3f2
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 945
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;

    .line 947
    iget-boolean v11, v4, Luw5;->c:Z

    .line 949
    invoke-direct {v8, v11, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;-><init>(ZLjava/util/List;)V

    .line 952
    const-string v11, "isDirectory"

    .line 954
    invoke-direct {v6, v11, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 957
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 960
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 962
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    .line 964
    invoke-direct {v8, v14, v15, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;-><init>(JLjava/util/List;)V

    .line 967
    const-string v11, "liTmfmMdoaeesdti"

    const-string v11, "lastModifiedTime"

    .line 969
    invoke-direct {v6, v11, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 972
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 975
    new-instance v6, Ljava/text/SimpleDateFormat;

    .line 977
    const-string v8, "mm :oHyys:d-M-ydyMs"

    const-string/jumbo v8, "yyyy-MM-dd HH:mm:ss"

    .line 979
    invoke-direct {v6, v8}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;)V

    .line 982
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 984
    new-instance v11, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;

    .line 986
    invoke-static {v14, v15}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 989
    move-result-object v12

    .line 990
    invoke-virtual {v6, v12}, Ljava/text/Format;->format(Ljava/lang/Object;)Ljava/lang/String;

    .line 993
    move-result-object v6

    .line 994
    invoke-direct {v11, v6, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;-><init>(Ljava/lang/String;Ljava/util/List;)V

    .line 997
    const-string v6, "lastModified"

    .line 999
    invoke-direct {v8, v6, v11, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 1002
    invoke-virtual {v5, v8}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1005
    if-eqz v13, :cond_448

    .line 1007
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 1009
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;

    .line 1011
    invoke-direct {v8, v13, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;-><init>(Ljava/lang/String;Ljava/util/List;)V

    .line 1014
    const-string v11, "emmpibyT"

    const-string v11, "mimeType"

    .line 1016
    invoke-direct {v6, v11, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 1019
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1022
    :cond_448
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 1024
    new-instance v8, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;

    .line 1026
    iget-object v4, v4, Luw5;->f:Ljava/lang/String;

    .line 1028
    invoke-direct {v8, v4, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$StringValue;-><init>(Ljava/lang/String;Ljava/util/List;)V

    .line 1031
    const-string/jumbo v4, "uri"

    .line 1033
    invoke-direct {v6, v4, v8, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 1036
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1039
    if-eqz v17, :cond_48b

    .line 1041
    invoke-interface/range {v17 .. v17}, Ljava/util/List;->isEmpty()Z

    .line 1044
    move-result v4

    .line 1045
    if-nez v4, :cond_48b

    .line 1047
    new-instance v4, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 1049
    new-instance v6, Ljava/util/ArrayList;

    .line 1051
    invoke-direct {v6}, Ljava/util/ArrayList;-><init>()V

    .line 1054
    const/4 v13, 0x0

    .line 1055
    invoke-direct {v4, v6, v13, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;-><init>(Ljava/util/List;ZLjava/util/List;)V

    .line 1058
    invoke-interface/range {v17 .. v17}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 1061
    move-result-object v6

    .line 1062
    :goto_471
    invoke-interface {v6}, Ljava/util/Iterator;->hasNext()Z

    .line 1065
    move-result v8

    .line 1066
    if-eqz v8, :cond_481

    .line 1068
    invoke-interface {v6}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 1071
    move-result-object v8

    .line 1072
    check-cast v8, Luw5;

    .line 1074
    invoke-static {v4, v8}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->a(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Luw5;)V

    .line 1077
    goto :goto_471

    .line 1078
    :cond_481
    new-instance v6, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 1080
    const-string v8, "children"

    .line 1082
    invoke-direct {v6, v8, v4, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 1085
    invoke-virtual {v5, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1088
    :cond_48b
    new-instance v4, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 1090
    const/4 v13, 0x0

    .line 1091
    invoke-direct {v4, v5, v13, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;-><init>(Ljava/util/List;ZLjava/util/List;)V

    .line 1094
    new-instance v5, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 1096
    invoke-static {v9}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 1099
    move-result-object v6

    .line 1100
    invoke-direct {v5, v6, v4, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;-><init>(Ljava/lang/String;Lcom/arlosoft/macrodroid/variables/VariableValue;Ljava/util/List;)V

    .line 1103
    invoke-virtual {v2, v5}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1106
    add-int/lit8 v11, v9, 0x1

    .line 1108
    move-object/from16 v1, p0

    .line 1110
    goto/16 :goto_39f

    .line 1112
    :cond_4a3
    const/4 v1, 0x0

    .line 1113
    new-instance v4, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 1115
    const/4 v5, 0x1

    .line 1116
    invoke-direct {v4, v2, v5, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;-><init>(Ljava/util/List;ZLjava/util/List;)V

    .line 1119
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 1122
    move-result v1

    .line 1123
    xor-int/2addr v1, v5

    .line 1124
    invoke-virtual {v7, v0, v4, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V

    .line 1127
    goto :goto_521

    .line 1128
    :cond_4b3
    move-object/from16 v2, v29

    .line 1130
    invoke-static {v1, v7, v10, v2}, Lsr9;->l(Landroid/content/Context;Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Ljava/lang/String;)Ljava/lang/String;

    .line 1133
    move-result-object v2

    .line 1134
    invoke-virtual {v2}, Ljava/lang/String;->length()I

    .line 1137
    move-result v4

    .line 1138
    if-nez v4, :cond_4c7

    .line 1140
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 1143
    move-result-wide v1

    .line 1144
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1147
    goto :goto_521

    .line 1148
    :cond_4c7
    invoke-virtual {v3, v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 1151
    move-result-object v0

    .line 1152
    if-nez v0, :cond_4db

    .line 1154
    new-instance v0, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 1156
    const/4 v4, 0x4

    .line 1157
    const/4 v5, 0x1

    .line 1158
    invoke-direct {v0, v4, v2, v5}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;-><init>(ILjava/lang/String;Z)V

    .line 1161
    invoke-virtual {v3, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->addVariable(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 1164
    invoke-virtual {v3, v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 1167
    move-result-object v0

    .line 1168
    :cond_4db
    if-nez v0, :cond_4e7

    .line 1170
    const-string v0, "Cannot read screen contents, array variable not available: ${variableName + VariableHelper.getFormattedDictionaryKeys(dictionaryKeys)}"

    .line 1172
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 1175
    move-result-wide v1

    .line 1176
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1179
    goto :goto_521

    .line 1180
    :cond_4e7
    if-eqz v17, :cond_4ee

    .line 1182
    invoke-virtual/range {v17 .. v17}, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;->getKeys()Ljava/util/List;

    .line 1185
    move-result-object v2

    .line 1186
    goto :goto_4f3

    .line 1187
    :cond_4ee
    new-instance v2, Ljava/util/ArrayList;

    .line 1189
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 1192
    :goto_4f3
    invoke-static {v1, v2, v10, v7}, Lcom/arlosoft/macrodroid/variables/n;->a(Landroid/content/Context;Ljava/util/List;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lcom/arlosoft/macrodroid/macro/Macro;)Ljava/util/ArrayList;

    .line 1195
    move-result-object v1

    .line 1196
    new-instance v2, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 1198
    new-instance v4, Ljava/util/ArrayList;

    .line 1200
    invoke-direct {v4}, Ljava/util/ArrayList;-><init>()V

    .line 1203
    const/4 v11, 0x0

    .line 1204
    invoke-direct {v2, v4, v11, v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;-><init>(Ljava/util/List;ZLjava/util/List;)V

    .line 1207
    invoke-virtual {v13}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 1210
    move-result-object v1

    .line 1211
    :goto_506
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 1214
    move-result v4

    .line 1215
    if-eqz v4, :cond_516

    .line 1217
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 1220
    move-result-object v4

    .line 1221
    check-cast v4, Luw5;

    .line 1223
    invoke-static {v2, v4}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->a(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Luw5;)V

    .line 1226
    goto :goto_506

    .line 1227
    :cond_516
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 1230
    move-result v1

    .line 1231
    const/16 v26, 0x1

    .line 1233
    xor-int/lit8 v1, v1, 0x1

    .line 1235
    invoke-virtual {v7, v0, v2, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V

    .line 1238
    :goto_521
    if-eqz v25, :cond_828

    .line 1240
    if-nez v24, :cond_828

    .line 1242
    move-object/from16 v18, v7

    .line 1244
    move-object/from16 v20, v10

    move-object/from16 v20, v10

    .line 1246
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 1249
    goto/16 :goto_828

    .line 1251
    :cond_530
    move-object/from16 v3, v16

    .line 1253
    const/4 v11, 0x0

    .line 1254
    new-instance v4, Ljava/util/ArrayList;

    .line 1256
    invoke-direct {v4}, Ljava/util/ArrayList;-><init>()V

    .line 1259
    if-eqz v3, :cond_57a

    .line 1261
    new-instance v0, Lzih;

    .line 1263
    invoke-direct {v0, v3}, Lzih;-><init>(Ljava/lang/String;)V

    .line 1266
    invoke-virtual {v2}, Lzr4;->s()[Lzr4;

    .line 1269
    move-result-object v3

    .line 1270
    array-length v5, v3

    .line 1271
    move v6, v11

    .line 1272
    :goto_545
    if-ge v6, v5, :cond_576

    .line 1274
    aget-object v13, v3, v6

    .line 1276
    invoke-virtual {v13}, Lzr4;->k()Ljava/lang/String;

    .line 1279
    move-result-object v15

    .line 1280
    if-eqz v15, :cond_572

    .line 1282
    invoke-virtual {v13}, Lzr4;->k()Ljava/lang/String;

    .line 1285
    invoke-virtual {v13}, Lzr4;->r()J

    .line 1288
    :try_start_555
    invoke-virtual {v13}, Lzr4;->o()Z

    .line 1291
    move-result v15

    .line 1292
    if-eqz v15, :cond_55f

    .line 1294
    const/4 v15, 0x4

    .line 1295
    if-ne v14, v15, :cond_572

    .line 1297
    goto :goto_560

    .line 1298
    :cond_55f
    const/4 v15, 0x4

    .line 1299
    :goto_560
    new-instance v11, Ljava/io/File;

    .line 1301
    invoke-virtual {v13}, Lzr4;->k()Ljava/lang/String;

    .line 1304
    move-result-object v15

    .line 1305
    invoke-direct {v11, v15}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 1308
    invoke-virtual {v0, v11}, Lzih;->accept(Ljava/io/File;)Z

    .line 1311
    move-result v11

    .line 1312
    if-eqz v11, :cond_572

    .line 1314
    invoke-virtual {v4, v13}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
    :try_end_572
    .catch Ljava/lang/Exception; {:try_start_555 .. :try_end_572} :catch_572

    .line 1317
    :catch_572
    :cond_572
    add-int/lit8 v6, v6, 0x1

    .line 1319
    const/4 v11, 0x0

    .line 1320
    goto :goto_545

    .line 1321
    :cond_576
    :goto_576
    move-object/from16 v17, v2

    .line 1323
    goto/16 :goto_5ec

    .line 1325
    :cond_57a
    if-eqz v5, :cond_7fe

    .line 1327
    if-nez v6, :cond_584

    .line 1329
    const-string v0, "FileOperationService: fromPath is null"

    .line 1331
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 1334
    return-void

    .line 1335
    :cond_584
    const-string v3, "/"

    .line 1337
    invoke-virtual {v6, v3}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    .line 1340
    move-result v3

    .line 1341
    if-eqz v3, :cond_590

    .line 1343
    invoke-virtual {v4, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1346
    goto :goto_576

    .line 1347
    :cond_590
    invoke-virtual {v2}, Lzr4;->s()[Lzr4;

    .line 1350
    move-result-object v3

    .line 1351
    array-length v6, v3

    .line 1352
    const/4 v11, 0x0

    .line 1353
    :goto_596
    if-ge v11, v6, :cond_576

    .line 1355
    aget-object v13, v3, v11

    .line 1357
    invoke-virtual {v13}, Lzr4;->k()Ljava/lang/String;

    .line 1360
    move-result-object v15

    .line 1361
    if-eqz v15, :cond_5de

    .line 1363
    invoke-virtual {v13}, Lzr4;->r()J

    .line 1366
    invoke-static {}, Ll1g;->a()V

    .line 1369
    array-length v12, v5

    .line 1370
    move-object/from16 v17, v2

    .line 1372
    const/4 v2, 0x0

    .line 1373
    :goto_5aa
    if-ge v2, v12, :cond_5d9

    .line 1375
    move/from16 v27, v2

    .line 1377
    aget-object v2, v5, v27

    .line 1379
    move-object/from16 v28, v3

    move-object/from16 v28, v3

    .line 1381
    invoke-virtual {v15}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;

    .line 1384
    move-result-object v3

    .line 1385
    move-object/from16 v29, v5

    move-object/from16 v29, v5

    .line 1387
    new-instance v5, Ljava/lang/StringBuilder;

    .line 1389
    invoke-direct {v5, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 1392
    invoke-virtual {v5, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1395
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1398
    move-result-object v2

    .line 1399
    invoke-virtual {v3, v2}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    .line 1402
    move-result v2

    .line 1403
    if-eqz v2, :cond_5d2

    .line 1405
    invoke-virtual {v4, v13}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 1408
    goto :goto_5e1

    .line 1409
    :cond_5d2
    add-int/lit8 v2, v27, 0x1

    .line 1411
    move-object/from16 v3, v28

    .line 1413
    move-object/from16 v5, v29

    .line 1415
    goto :goto_5aa

    .line 1416
    :cond_5d9
    :goto_5d9
    move-object/from16 v28, v3

    .line 1418
    move-object/from16 v29, v5

    .line 1420
    goto :goto_5e1

    .line 1421
    :cond_5de
    move-object/from16 v17, v2

    .line 1423
    goto :goto_5d9

    .line 1424
    :goto_5e1
    add-int/lit8 v11, v11, 0x1

    .line 1426
    move-object/from16 v2, v17

    .line 1428
    move-object/from16 v3, v28

    .line 1430
    move-object/from16 v5, v29

    move-object/from16 v5, v29

    .line 1432
    goto :goto_596

    .line 1433
    :goto_5ec
    invoke-virtual {v4}, Ljava/util/ArrayList;->isEmpty()Z

    .line 1436
    move-result v0

    .line 1437
    if-eqz v0, :cond_5ff

    .line 1439
    if-eqz v25, :cond_828

    .line 1441
    if-nez v24, :cond_828

    .line 1443
    move-object/from16 v18, v7

    .line 1445
    move-object/from16 v20, v10

    .line 1447
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 1450
    goto/16 :goto_828

    .line 1452
    :cond_5ff
    invoke-virtual {v4}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 1455
    move-result-object v11

    .line 1456
    const/4 v12, 0x0

    .line 1457
    :goto_604
    invoke-interface {v11}, Ljava/util/Iterator;->hasNext()Z

    .line 1460
    move-result v0

    .line 1461
    if-eqz v0, :cond_7a3

    .line 1463
    invoke-interface {v11}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 1466
    move-result-object v0

    .line 1467
    check-cast v0, Lzr4;

    .line 1469
    const/4 v13, 0x2

    .line 1470
    if-ne v14, v13, :cond_65a

    .line 1472
    if-eqz v8, :cond_646

    .line 1474
    new-instance v2, Lzih;

    .line 1476
    invoke-direct {v2, v8}, Lzih;-><init>(Ljava/lang/String;)V

    .line 1479
    invoke-virtual/range {v17 .. v17}, Lzr4;->s()[Lzr4;

    .line 1482
    move-result-object v3

    .line 1483
    array-length v4, v3

    .line 1484
    const/4 v5, 0x0

    .line 1485
    :goto_620
    if-ge v5, v4, :cond_649

    .line 1487
    aget-object v6, v3, v5

    .line 1489
    invoke-virtual {v0}, Lzr4;->k()Ljava/lang/String;

    .line 1492
    move-result-object v15

    .line 1493
    if-eqz v15, :cond_642

    .line 1495
    :try_start_62a
    invoke-virtual {v6}, Lzr4;->o()Z

    .line 1498
    move-result v15

    .line 1499
    if-eqz v15, :cond_642

    .line 1501
    new-instance v15, Ljava/io/File;

    .line 1503
    invoke-virtual {v6}, Lzr4;->k()Ljava/lang/String;

    .line 1506
    move-result-object v13

    .line 1507
    invoke-direct {v15, v13}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 1510
    invoke-virtual {v2, v15}, Lzih;->accept(Ljava/io/File;)Z

    .line 1513
    move-result v13

    .line 1514
    if-eqz v13, :cond_642

    .line 1516
    invoke-virtual {v6}, Lzr4;->e()Z
    :try_end_642
    .catch Ljava/lang/Exception; {:try_start_62a .. :try_end_642} :catch_642

    .line 1519
    :catch_642
    :cond_642
    add-int/lit8 v5, v5, 0x1

    .line 1521
    const/4 v13, 0x2

    .line 1522
    goto :goto_620

    .line 1523
    :cond_646
    invoke-virtual {v0}, Lzr4;->e()Z

    .line 1526
    :cond_649
    move v4, v14

    move v4, v14

    .line 1527
    move-object/from16 v2, v18

    .line 1529
    move/from16 v6, v30

    .line 1531
    move-object/from16 v13, v32

    .line 1533
    const/4 v3, 0x0

    .line 1534
    const/16 v26, 0x1

    .line 1536
    move-object/from16 v18, v7

    .line 1538
    move-object v7, v9

    move-object v7, v9

    .line 1539
    goto/16 :goto_791

    .line 1541
    :cond_65a
    move-object/from16 v13, v32

    .line 1543
    if-nez v13, :cond_674

    .line 1545
    const-string v0, "File Operation failed: Destination address is null"

    .line 1547
    invoke-virtual {v7}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 1550
    move-result-wide v1

    .line 1551
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1554
    if-eqz v25, :cond_828

    .line 1556
    if-nez v24, :cond_828

    .line 1558
    move-object/from16 v18, v7

    .line 1560
    move-object/from16 v20, v10

    .line 1562
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 1565
    goto/16 :goto_828

    .line 1567
    :cond_674
    move-object/from16 v43, v18

    .line 1569
    move-object/from16 v18, v7

    .line 1571
    move-object/from16 v7, v43

    .line 1573
    :try_start_67a
    invoke-static {v1, v13}, Lzr4;->j(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 1576
    move-result-object v2

    .line 1577
    invoke-virtual {v2}, Lzr4;->b()Z

    .line 1580
    move-result v3

    .line 1581
    if-nez v3, :cond_690

    .line 1583
    invoke-static {v1, v13}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->e(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 1586
    move-result-object v2

    .line 1587
    if-eqz v2, :cond_6a2

    .line 1589
    invoke-virtual {v2}, Lzr4;->b()Z

    .line 1592
    move-result v3

    .line 1593
    if-eqz v3, :cond_6a2

    .line 1595
    :cond_690
    move-object v15, v2

    move-object v15, v2

    .line 1596
    goto :goto_6a9

    .line 1597
    :catchall_693
    move-exception v0

    .line 1598
    const/4 v3, 0x0

    .line 1599
    goto/16 :goto_78c

    .line 1601
    :catch_697
    move-exception v0

    .line 1602
    move-object v2, v7

    move-object v2, v7

    .line 1603
    move-object v7, v9

    .line 1604
    move v4, v14

    .line 1605
    move/from16 v6, v30

    .line 1607
    const/16 v26, 0x1

    .line 1609
    goto/16 :goto_784

    .line 1611
    :cond_6a2
    invoke-static {v1, v9}, Lcxa;->c(Landroid/content/Context;Ljava/lang/String;)V
    :try_end_6a5
    .catch Ljava/lang/Exception; {:try_start_67a .. :try_end_6a5} :catch_697
    .catchall {:try_start_67a .. :try_end_6a5} :catchall_693

    .line 1614
    const/4 v1, 0x0

    .line 1615
    :try_start_6a6
    throw v1
    :try_end_6a7
    .catch Ljava/lang/Exception; {:try_start_6a6 .. :try_end_6a7} :catch_6a7

    .line 1616
    :catch_6a7
    :try_start_6a7
    throw v1
    :try_end_6a8
    .catch Ljava/lang/Exception; {:try_start_6a7 .. :try_end_6a8} :catch_6a8

    .line 1617
    :catch_6a8
    return-void

    .line 1618
    :goto_6a9
    :try_start_6a9
    invoke-virtual {v0}, Lzr4;->o()Z

    .line 1621
    move-result v2
    :try_end_6ad
    .catch Ljava/lang/Exception; {:try_start_6a9 .. :try_end_6ad} :catch_697
    .catchall {:try_start_6a9 .. :try_end_6ad} :catchall_693

    .line 1622
    if-eqz v2, :cond_76c

    .line 1624
    if-eqz v8, :cond_74f

    .line 1626
    :try_start_6b1
    new-instance v2, Lzih;

    .line 1628
    invoke-direct {v2, v8}, Lzih;-><init>(Ljava/lang/String;)V

    .line 1631
    invoke-virtual/range {v17 .. v17}, Lzr4;->s()[Lzr4;

    .line 1634
    move-result-object v3

    .line 1635
    array-length v4, v3

    .line 1636
    const/4 v5, 0x0

    .line 1637
    :goto_6bc
    if-ge v5, v4, :cond_746

    .line 1639
    aget-object v6, v3, v5

    .line 1641
    invoke-virtual {v0}, Lzr4;->k()Ljava/lang/String;

    .line 1644
    move-result-object v27

    .line 1645
    if-eqz v27, :cond_722

    .line 1647
    invoke-virtual {v0}, Lzr4;->k()Ljava/lang/String;

    .line 1650
    invoke-virtual {v0}, Lzr4;->r()J
    :try_end_6cc
    .catch Ljava/lang/Exception; {:try_start_6b1 .. :try_end_6cc} :catch_712
    .catchall {:try_start_6b1 .. :try_end_6cc} :catchall_693

    .line 1653
    :try_start_6cc
    invoke-virtual {v6}, Lzr4;->o()Z

    .line 1656
    move-result v27
    :try_end_6d0
    .catch Ljava/lang/Exception; {:try_start_6cc .. :try_end_6d0} :catch_722
    .catchall {:try_start_6cc .. :try_end_6d0} :catchall_693

    .line 1657
    if-eqz v27, :cond_722

    .line 1659
    move-object/from16 v27, v0

    move-object/from16 v27, v0

    .line 1661
    :try_start_6d6
    new-instance v0, Ljava/io/File;

    .line 1663
    invoke-virtual {v6}, Lzr4;->k()Ljava/lang/String;

    .line 1666
    move-result-object v1

    .line 1667
    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 1670
    invoke-virtual {v2, v0}, Lzih;->accept(Ljava/io/File;)Z

    .line 1673
    move-result v0

    .line 1674
    if-eqz v0, :cond_70e

    .line 1676
    invoke-virtual {v6}, Lzr4;->k()Ljava/lang/String;

    .line 1679
    move-result-object v0

    .line 1680
    invoke-virtual {v15, v0}, Lzr4;->c(Ljava/lang/String;)Lzr4;

    .line 1683
    move-result-object v0
    :try_end_6ed
    .catch Ljava/lang/Exception; {:try_start_6d6 .. :try_end_6ed} :catch_70e
    .catchall {:try_start_6d6 .. :try_end_6ed} :catchall_693

    .line 1684
    move v1, v14

    move v1, v14

    .line 1685
    move v14, v4

    .line 1686
    move v4, v1

    move v4, v1

    .line 1687
    move-object/from16 v1, p0

    .line 1689
    move/from16 v28, v5

    .line 1691
    move-object v5, v9

    .line 1692
    move-object v9, v3

    move-object v9, v3

    .line 1693
    move-object v3, v0

    move-object v3, v0

    .line 1694
    move-object v0, v2

    move-object v0, v2

    .line 1695
    move-object v2, v6

    .line 1696
    move/from16 v6, v30

    .line 1698
    :try_start_700
    invoke-static/range {v1 .. v7}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->h(Landroid/content/Context;Lzr4;Lzr4;ILjava/lang/String;ILjava/lang/String;)V
    :try_end_703
    .catch Ljava/lang/Exception; {:try_start_700 .. :try_end_703} :catch_70c
    .catchall {:try_start_700 .. :try_end_703} :catchall_693

    .line 1701
    const/4 v1, 0x1

    .line 1702
    if-ne v4, v1, :cond_731

    .line 1704
    if-eq v6, v1, :cond_731

    .line 1706
    :try_start_708
    invoke-virtual {v2}, Lzr4;->e()Z
    :try_end_70b
    .catch Ljava/lang/Exception; {:try_start_708 .. :try_end_70b} :catch_731
    .catchall {:try_start_708 .. :try_end_70b} :catchall_693

    .line 1709
    goto :goto_731

    .line 1710
    :catch_70c
    const/4 v1, 0x1

    .line 1711
    goto :goto_731

    .line 1712
    :catch_70e
    :cond_70e
    move v0, v14

    .line 1713
    move v14, v4

    .line 1714
    move v4, v0

    .line 1715
    goto :goto_728

    .line 1716
    :catch_712
    move-exception v0

    .line 1717
    move-object v5, v9

    .line 1718
    move v4, v14

    .line 1719
    move/from16 v6, v30

    .line 1721
    const/4 v1, 0x1

    .line 1722
    move/from16 v26, v1

    move/from16 v26, v1

    .line 1724
    move-object v2, v7

    .line 1725
    move-object/from16 v1, p0

    .line 1727
    move-object v7, v5

    .line 1728
    goto/16 :goto_784

    .line 1730
    :catch_722
    :cond_722
    move v1, v14

    .line 1731
    move v14, v4

    .line 1732
    move v4, v1

    move v4, v1

    .line 1733
    move-object/from16 v27, v0

    .line 1735
    :goto_728
    move-object v0, v2

    .line 1736
    move/from16 v28, v5

    .line 1738
    move-object v5, v9

    move-object v5, v9

    .line 1739
    move/from16 v6, v30

    .line 1741
    const/4 v1, 0x1

    .line 1742
    move-object v9, v3

    .line 1743
    :catch_731
    :cond_731
    :goto_731
    add-int/lit8 v2, v28, 0x1

    .line 1745
    move v1, v14

    .line 1746
    move v14, v4

    .line 1747
    move v4, v1

    move v4, v1

    .line 1748
    move-object/from16 v1, p0

    move-object/from16 v1, p0

    .line 1750
    move/from16 v30, v6

    .line 1752
    move-object v3, v9

    .line 1753
    move-object v9, v5

    move-object v9, v5

    .line 1754
    move v5, v2

    .line 1755
    move-object v2, v0

    .line 1756
    move-object/from16 v0, v27

    .line 1758
    goto/16 :goto_6bc

    .line 1759
    :cond_746
    move-object v1, v7

    move-object v1, v7

    .line 1760
    move-object v7, v9

    .line 1761
    move v4, v14

    .line 1762
    move/from16 v6, v30

    .line 1764
    const/16 v26, 0x1

    .line 1766
    goto :goto_75d

    .line 1767
    :cond_74f
    move-object v2, v0

    .line 1768
    move-object v5, v9

    .line 1769
    move v4, v14

    .line 1770
    move-object v3, v15

    .line 1771
    move/from16 v6, v30

    .line 1773
    const/16 v26, 0x1

    .line 1775
    :try_start_757
    invoke-static/range {v1 .. v7}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->h(Landroid/content/Context;Lzr4;Lzr4;ILjava/lang/String;ILjava/lang/String;)V
    :try_end_75a
    .catch Ljava/lang/Exception; {:try_start_757 .. :try_end_75a} :catch_762
    .catchall {:try_start_757 .. :try_end_75a} :catchall_693

    .line 1778
    move-object v1, v7

    move-object v1, v7

    .line 1779
    move-object v7, v5

    .line 1780
    :goto_75d
    move-object v2, v1

    .line 1781
    move-object/from16 v1, p0

    .line 1783
    :goto_760
    const/4 v3, 0x0

    .line 1784
    goto :goto_77e

    .line 1785
    :catch_762
    move-exception v0

    .line 1786
    move-object v1, v7

    move-object v1, v7

    .line 1787
    move-object v7, v5

    move-object v7, v5

    .line 1788
    move-object v2, v1

    move-object v2, v1

    .line 1789
    move-object/from16 v1, p0

    .line 1791
    goto :goto_784

    .line 1792
    :cond_76c
    move-object v2, v0

    .line 1793
    move-object v6, v7

    move-object v6, v7

    .line 1794
    move-object v7, v9

    .line 1795
    move v4, v14

    move v4, v14

    .line 1796
    move-object v3, v15

    .line 1797
    move/from16 v5, v30

    .line 1799
    const/16 v26, 0x1

    .line 1801
    :try_start_777
    invoke-static/range {v1 .. v6}, Lcom/arlosoft/macrodroid/action/services/FileOperationV21Service;->b(Landroid/content/Context;Lzr4;Lzr4;IILjava/lang/String;)Ljava/lang/String;

    .line 1804
    move-result-object v12
    :try_end_77b
    .catch Ljava/lang/Exception; {:try_start_777 .. :try_end_77b} :catch_780
    .catchall {:try_start_777 .. :try_end_77b} :catchall_693

    .line 1805
    move-object v2, v6

    .line 1806
    move v6, v5

    .line 1807
    goto :goto_760

    .line 1808
    :goto_77e
    :try_start_77e
    throw v3
    :try_end_77f
    .catch Ljava/lang/Exception; {:try_start_77e .. :try_end_77f} :catch_77f

    .line 1809
    :catch_77f
    :try_start_77f
    throw v3
    :try_end_780
    .catch Ljava/lang/Exception; {:try_start_77f .. :try_end_780} :catch_791

    .line 1810
    :catch_780
    move-exception v0

    .line 1811
    move-object v2, v6

    .line 1812
    move v6, v5

    move v6, v5

    .line 1813
    :goto_784
    if-nez v12, :cond_78a

    .line 1815
    :try_start_786
    invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;

    .line 1818
    move-result-object v12
    :try_end_78a
    .catchall {:try_start_786 .. :try_end_78a} :catchall_693

    .line 1819
    :cond_78a
    const/4 v3, 0x0

    .line 1820
    goto :goto_78f

    .line 1821
    :goto_78c
    :try_start_78c
    throw v3
    :try_end_78d
    .catch Ljava/lang/Exception; {:try_start_78c .. :try_end_78d} :catch_78d

    .line 1822
    :catch_78d
    :try_start_78d
    throw v3
    :try_end_78e
    .catch Ljava/lang/Exception; {:try_start_78d .. :try_end_78e} :catch_78e

    .line 1823
    :catch_78e
    throw v0

    .line 1824
    :goto_78f
    :try_start_78f
    throw v3
    :try_end_790
    .catch Ljava/lang/Exception; {:try_start_78f .. :try_end_790} :catch_790

    .line 1825
    :catch_790
    :try_start_790
    throw v3
    :try_end_791
    .catch Ljava/lang/Exception; {:try_start_790 .. :try_end_791} :catch_791

    .line 1826
    :catch_791
    :goto_791
    move v14, v4

    .line 1827
    move/from16 v30, v6

    move/from16 v30, v6

    .line 1829
    move-object v9, v7

    .line 1830
    move-object/from16 v32, v13

    move-object/from16 v32, v13

    .line 1832
    move-object/from16 v7, v18

    move-object/from16 v7, v18

    .line 1834
    move-object/from16 v18, v2

    .line 1836
    goto/16 :goto_604

    .line 1838
    :cond_7a3
    move-object/from16 v18, v7

    .line 1840
    move v4, v14

    move v4, v14

    .line 1841
    if-eqz v12, :cond_7f4

    .line 1843
    new-instance v0, Ljava/lang/StringBuilder;

    .line 1845
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 1848
    const v2, 0x7f140f36

    .line 1851
    invoke-virtual {v1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 1854
    move-result-object v3

    .line 1855
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1858
    const-string v3, ": "

    .line 1860
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1863
    invoke-static {}, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;->i0()[Ljava/lang/String;

    .line 1866
    move-result-object v5

    .line 1867
    aget-object v5, v5, v4

    .line 1869
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1872
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1875
    move-result-object v0

    .line 1876
    invoke-static {v1, v0, v12}, Lhtg;->h(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V

    .line 1879
    new-instance v0, Ljava/lang/StringBuilder;

    .line 1881
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 1884
    invoke-virtual {v1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 1887
    move-result-object v1

    .line 1888
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1891
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1894
    invoke-static {}, Lcom/arlosoft/macrodroid/action/FileOperationV21Action;->i0()[Ljava/lang/String;

    .line 1897
    move-result-object v1

    .line 1898
    aget-object v1, v1, v4

    .line 1900
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1903
    const-string v1, " - "

    .line 1905
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1908
    invoke-virtual {v0, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 1911
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 1914
    move-result-object v0

    .line 1915
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 1918
    :cond_7f4
    if-eqz v25, :cond_828

    .line 1920
    if-nez v24, :cond_828

    .line 1922
    move-object/from16 v20, v10

    .line 1924
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 1927
    goto :goto_828

    .line 1928
    :cond_7fe
    move-object/from16 v18, v7

    .line 1930
    move-object/from16 v20, v10

    .line 1932
    invoke-virtual/range {v18 .. v18}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 1935
    move-result-wide v2

    .line 1936
    const-string v0, " :nioluFP SuicensaieoeOEtFeii et btvrtenrasx ohtlFleipaner enanlrd"

    const-string v0, "FileOperationService: FilePattern and FileExtensions are both null"

    .line 1938
    invoke-static {v2, v3, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1941
    new-instance v2, Ljava/lang/RuntimeException;

    .line 1943
    invoke-direct {v2, v0}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    .line 1946
    invoke-static {v2}, Lsz5;->e(Ljava/lang/Throwable;)V

    .line 1949
    const v2, 0x7f140f36

    .line 1952
    invoke-virtual {v1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 1955
    move-result-object v0

    .line 1956
    const-string v2, "File Operation Failed"

    .line 1958
    invoke-static {v1, v0, v2}, Lhtg;->h(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V

    .line 1961
    if-eqz v25, :cond_828

    .line 1963
    if-nez v24, :cond_828

    .line 1965
    invoke-static/range {v18 .. v23}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroFromActivity(Lcom/arlosoft/macrodroid/macro/Macro;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V

    .line 1968
    :cond_828
    :goto_828
    return-void
.end method
