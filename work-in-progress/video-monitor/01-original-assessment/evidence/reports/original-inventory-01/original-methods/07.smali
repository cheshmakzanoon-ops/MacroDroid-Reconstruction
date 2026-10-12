.method public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;
    .locals 37

    .line 1
    move-object/from16 v0, p0

    move-object/from16 v0, p0

    .line 3
    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 5
    iget v2, v0, Lcom/arlosoft/macrodroid/action/k;->label:I

    .line 7
    const/4 v3, 0x3

    .line 8
    const/4 v4, 0x2

    .line 9
    const/4 v5, 0x0

    .line 10
    const-string/jumbo v6, "uiInteractionConfig"

    .line 12
    const-class v7, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    const-class v7, Lcom/arlosoft/macrodroid/action/services/UIInteractionAccessibilityService;

    .line 14
    const/4 v8, 0x1

    .line 15
    const/4 v9, 0x0

    .line 16
    if-eqz v2, :cond_58

    .line 18
    if-eq v2, v8, :cond_54

    .line 20
    if-eq v2, v4, :cond_47

    .line 22
    if-ne v2, v3, :cond_3f

    .line 24
    iget v2, v0, Lcom/arlosoft/macrodroid/action/k;->I$1:I

    .line 26
    iget v4, v0, Lcom/arlosoft/macrodroid/action/k;->I$0:I

    .line 28
    iget-object v10, v0, Lcom/arlosoft/macrodroid/action/k;->L$5:Ljava/lang/Object;

    .line 30
    check-cast v10, Landroid/content/Intent;

    .line 32
    iget-object v10, v0, Lcom/arlosoft/macrodroid/action/k;->L$4:Ljava/lang/Object;

    .line 34
    check-cast v10, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 36
    iget-object v10, v0, Lcom/arlosoft/macrodroid/action/k;->L$3:Ljava/lang/Object;

    .line 38
    check-cast v10, Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 40
    iget-object v11, v0, Lcom/arlosoft/macrodroid/action/k;->L$2:Ljava/lang/Object;

    .line 42
    check-cast v11, Ljava/lang/CharSequence;

    .line 44
    iget-object v12, v0, Lcom/arlosoft/macrodroid/action/k;->L$1:Ljava/lang/Object;

    .line 46
    check-cast v12, Landroid/content/Intent;

    .line 48
    iget-object v12, v0, Lcom/arlosoft/macrodroid/action/k;->L$0:Ljava/lang/Object;

    .line 50
    check-cast v12, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 52
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 55
    move/from16 v16, v8

    .line 57
    goto/16 :goto_16e

    .line 59
    :cond_3f
    const-string v0, "o s o  iever/lrtnsnbe olcoa/kim/i/eo/urt /uc/thfwee"

    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 61
    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    .line 64
    return-object v9

    .line 65
    :cond_47
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->L$1:Ljava/lang/Object;

    .line 67
    check-cast v2, Landroid/content/Intent;

    .line 69
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->L$0:Ljava/lang/Object;

    .line 71
    check-cast v2, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 73
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 76
    goto/16 :goto_f0

    .line 78
    :cond_54
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 81
    goto :goto_6b

    .line 82
    :cond_58
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 85
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 87
    invoke-static {v2}, Lcom/arlosoft/macrodroid/action/PinUnlockAction;->U(Lcom/arlosoft/macrodroid/action/PinUnlockAction;)J

    .line 90
    move-result-wide v10

    .line 91
    iput v8, v0, Lcom/arlosoft/macrodroid/action/k;->label:I

    .line 93
    invoke-static {v10, v11, v0}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    .line 96
    move-result-object v2

    .line 97
    if-ne v2, v1, :cond_6b

    .line 99
    goto/16 :goto_16d

    .line 101
    :cond_6b
    :goto_6b
    new-instance v10, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;

    .line 103
    const v33, 0x3ff000

    .line 106
    const/16 v34, 0x0

    .line 108
    const/16 v11, 0x50

    .line 110
    const/16 v12, 0x50

    .line 112
    const/16 v13, 0x50

    .line 114
    const/16 v14, 0x1e

    .line 116
    const/4 v15, 0x1

    .line 117
    const/16 v16, 0x12c

    .line 119
    const/16 v17, 0x0

    .line 121
    const/16 v18, 0x0

    .line 123
    const/16 v19, 0x0

    .line 125
    const/16 v20, 0x0

    .line 127
    const/16 v21, 0x0

    .line 129
    const/16 v22, 0x1

    .line 131
    const/16 v23, 0x0

    .line 133
    const/16 v24, 0x0

    .line 135
    const/16 v25, 0x0

    .line 137
    const/16 v26, 0x0

    .line 139
    const/16 v27, 0x0

    .line 141
    const/16 v28, 0x0

    .line 143
    const/16 v29, 0x0

    .line 145
    const/16 v30, 0x0

    .line 147
    const/16 v31, 0x0

    .line 149
    const/16 v32, 0x0

    .line 151
    invoke-direct/range {v10 .. v34}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Gesture;-><init>(IIIIZILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZIIIIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZILy84;)V

    .line 154
    new-instance v2, Landroid/content/Intent;

    .line 156
    iget-object v11, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 158
    invoke-virtual {v11}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 161
    move-result-object v11

    .line 162
    invoke-direct {v2, v11, v7}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 165
    const-string/jumbo v11, "xStartVariableValue"

    .line 167
    const-wide/16 v12, 0x50

    .line 169
    invoke-virtual {v2, v11, v12, v13}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 172
    const-string/jumbo v11, "yStartVariableValue"

    .line 174
    invoke-virtual {v2, v11, v12, v13}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 177
    const-string v11, "luVmaxdaElVnreabe"

    const-string/jumbo v11, "xEndVariableValue"

    .line 179
    invoke-virtual {v2, v11, v12, v13}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 182
    const-string/jumbo v11, "yEndVariableValue"

    .line 184
    const-wide/16 v12, 0x1e

    .line 186
    invoke-virtual {v2, v11, v12, v13}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 189
    const-string v11, "durationVariableValue"

    .line 191
    const-wide/16 v12, 0x12c

    .line 193
    invoke-virtual {v2, v11, v12, v13}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 196
    invoke-virtual {v2, v6, v10}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 199
    iget-object v10, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 201
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 204
    move-result-object v10

    .line 205
    invoke-virtual {v10, v2}, Landroid/content/Context;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;

    .line 208
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 210
    invoke-static {v2}, Lcom/arlosoft/macrodroid/action/PinUnlockAction;->U(Lcom/arlosoft/macrodroid/action/PinUnlockAction;)J

    .line 213
    move-result-wide v10

    .line 214
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$0:Ljava/lang/Object;

    .line 216
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$1:Ljava/lang/Object;

    .line 218
    iput v4, v0, Lcom/arlosoft/macrodroid/action/k;->label:I

    .line 220
    invoke-static {v10, v11, v0}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    .line 223
    move-result-object v2

    .line 224
    if-ne v2, v1, :cond_f0

    .line 226
    goto/16 :goto_16d

    .line 228
    :cond_f0
    :goto_f0
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->$processedPin:Ljava/lang/String;

    .line 230
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 233
    iget-object v4, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 235
    move-object v11, v2

    move-object v11, v2

    .line 236
    move-object v10, v4

    .line 237
    move v2, v5

    .line 238
    move v4, v2

    move v4, v2

    .line 239
    :goto_fd
    invoke-interface {v11}, Ljava/lang/CharSequence;->length()I

    .line 242
    move-result v12

    .line 243
    if-ge v2, v12, :cond_173

    .line 245
    invoke-interface {v11, v2}, Ljava/lang/CharSequence;->charAt(I)C

    .line 248
    move-result v12

    .line 249
    int-to-char v13, v12

    .line 250
    new-instance v14, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 252
    int-to-char v15, v13

    .line 253
    invoke-static {v15}, Ljava/lang/String;->valueOf(C)Ljava/lang/String;

    .line 256
    move-result-object v21

    .line 257
    const v32, 0x1c000

    .line 260
    const/16 v33, 0x0

    .line 262
    const/4 v15, 0x1

    .line 263
    const/16 v16, 0x0

    .line 265
    const/16 v17, 0x0

    .line 267
    const/16 v18, 0x0

    .line 269
    const/16 v19, 0x0

    .line 271
    const/16 v20, 0x0

    .line 273
    const/16 v22, 0x1

    .line 275
    const/16 v23, 0x0

    .line 277
    const/16 v24, 0x0

    .line 279
    const/16 v25, 0x0

    .line 281
    const/16 v26, 0x0

    .line 283
    const/16 v27, 0x0

    .line 285
    const/16 v28, 0x0

    .line 287
    const/16 v29, 0x0

    .line 289
    const/16 v30, 0x0

    .line 291
    const/16 v31, 0x0

    .line 293
    invoke-direct/range {v14 .. v33}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;-><init>(IZLandroid/graphics/Point;ZLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/lang/String;ZLcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;ZLjava/lang/String;ZZLjava/lang/Integer;ILy84;)V

    .line 296
    new-instance v15, Landroid/content/Intent;

    .line 298
    move/from16 v16, v8

    .line 300
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 303
    move-result-object v8

    .line 304
    invoke-direct {v15, v8, v7}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 307
    invoke-virtual {v15, v6, v14}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 310
    invoke-virtual {v10}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 313
    move-result-object v8

    .line 314
    invoke-virtual {v8, v15}, Landroid/content/Context;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;

    .line 317
    invoke-static {v10}, Lcom/arlosoft/macrodroid/action/PinUnlockAction;->T(Lcom/arlosoft/macrodroid/action/PinUnlockAction;)J

    .line 320
    move-result-wide v14

    .line 321
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$0:Ljava/lang/Object;

    .line 323
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$1:Ljava/lang/Object;

    .line 325
    iput-object v11, v0, Lcom/arlosoft/macrodroid/action/k;->L$2:Ljava/lang/Object;

    .line 327
    iput-object v10, v0, Lcom/arlosoft/macrodroid/action/k;->L$3:Ljava/lang/Object;

    .line 329
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$4:Ljava/lang/Object;

    .line 331
    iput-object v9, v0, Lcom/arlosoft/macrodroid/action/k;->L$5:Ljava/lang/Object;

    .line 333
    iput v4, v0, Lcom/arlosoft/macrodroid/action/k;->I$0:I

    .line 335
    iput v2, v0, Lcom/arlosoft/macrodroid/action/k;->I$1:I

    .line 337
    iput-char v12, v0, Lcom/arlosoft/macrodroid/action/k;->C$0:C

    .line 339
    iput-char v13, v0, Lcom/arlosoft/macrodroid/action/k;->C$1:C

    .line 341
    iput v5, v0, Lcom/arlosoft/macrodroid/action/k;->I$2:I

    .line 343
    iput v3, v0, Lcom/arlosoft/macrodroid/action/k;->label:I

    .line 345
    invoke-static {v14, v15, v0}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    .line 348
    move-result-object v8

    .line 349
    if-ne v8, v1, :cond_16e

    .line 351
    :goto_16d
    return-object v1

    .line 352
    :cond_16e
    :goto_16e
    add-int/lit8 v2, v2, 0x1

    .line 354
    move/from16 v8, v16

    .line 356
    goto :goto_fd

    .line 357
    :cond_173
    new-instance v17, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;

    .line 359
    const v35, 0x1c000

    .line 362
    const/16 v36, 0x0

    .line 364
    const/16 v18, 0x4

    .line 366
    const/16 v19, 0x0

    .line 368
    const/16 v20, 0x0

    .line 370
    const/16 v21, 0x0

    .line 372
    const/16 v22, 0x0

    .line 374
    const/16 v23, 0x0

    .line 376
    const-string v24, "nter"

    const-string v24, "nter"

    .line 378
    const/16 v25, 0x0

    .line 380
    const-string v26, "nter"

    .line 382
    const-string v27, "nter"

    .line 384
    const/16 v28, 0x0

    .line 386
    const/16 v29, 0x0

    .line 388
    const/16 v30, 0x0

    .line 390
    const/16 v31, 0x0

    .line 392
    const/16 v32, 0x0

    .line 394
    const/16 v33, 0x0

    .line 396
    const/16 v34, 0x0

    .line 398
    invoke-direct/range {v17 .. v36}, Lcom/arlosoft/macrodroid/action/UiInteractionConfiguration$Click;-><init>(IZLandroid/graphics/Point;ZLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/lang/String;ZLcom/arlosoft/macrodroid/variables/VariableWithDictionaryKeys;ZLjava/lang/String;ZZLjava/lang/Integer;ILy84;)V

    .line 401
    move-object/from16 v1, v17

    move-object/from16 v1, v17

    .line 403
    new-instance v2, Landroid/content/Intent;

    .line 405
    iget-object v3, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 407
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 410
    move-result-object v3

    .line 411
    invoke-direct {v2, v3, v7}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 414
    invoke-virtual {v2, v6, v1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 417
    iget-object v1, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 419
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 422
    move-result-object v1

    .line 423
    invoke-virtual {v1, v2}, Landroid/content/Context;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;

    .line 426
    iget-boolean v1, v0, Lcom/arlosoft/macrodroid/action/k;->$isTest:Z

    .line 428
    if-nez v1, :cond_1d1

    .line 430
    iget-object v2, v0, Lcom/arlosoft/macrodroid/action/k;->this$0:Lcom/arlosoft/macrodroid/action/PinUnlockAction;

    .line 432
    iget v3, v0, Lcom/arlosoft/macrodroid/action/k;->$nextAction:I

    .line 434
    iget-object v4, v0, Lcom/arlosoft/macrodroid/action/k;->$contextInfo:Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 436
    iget-boolean v5, v0, Lcom/arlosoft/macrodroid/action/k;->$forceEvenIfNotEnabled:Z

    .line 438
    iget-object v6, v0, Lcom/arlosoft/macrodroid/action/k;->$skipEndifIndexStack:Ljava/util/Stack;

    .line 440
    iget-object v7, v0, Lcom/arlosoft/macrodroid/action/k;->$resumeMacroInfo:Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;

    .line 442
    iget-wide v8, v0, Lcom/arlosoft/macrodroid/action/k;->$capturedRunId:J

    .line 444
    invoke-virtual/range {v2 .. v9}, Lcom/arlosoft/macrodroid/action/Action;->continueMacroWithDebugSupportAsync(ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;J)V

    .line 447
    :cond_1d1
    sget-object v0, Lblg;->a:Lblg;

    .line 449
    return-object v0
.end method
