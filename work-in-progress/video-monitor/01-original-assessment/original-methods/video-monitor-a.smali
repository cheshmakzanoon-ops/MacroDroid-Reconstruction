.method public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;
    .locals 23

    .line 1
    move-object/from16 v1, p0

    .line 2
    .line 3
    sget-object v2, Lblg;->a:Lblg;

    .line 4
    .line 5
    const-string v3, "KB"

    .line 6
    .line 7
    sget-object v4, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 8
    .line 9
    iget v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    .line 10
    .line 11
    const/4 v7, 0x2

    .line 12
    const/4 v8, 0x3

    .line 13
    const/4 v9, 0x0

    .line 14
    const/4 v10, 0x1

    .line 15
    if-eqz v0, :cond_41

    .line 16
    .line 17
    if-eq v0, v10, :cond_3d

    .line 18
    .line 19
    if-eq v0, v7, :cond_28

    .line 20
    .line 21
    if-ne v0, v8, :cond_22

    .line 22
    .line 23
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 24
    .line 25
    .line 26
    move-object v6, v9

    .line 27
    move/from16 v21, v10

    .line 28
    .line 29
    const-wide/16 v9, 0xbb8

    const-wide/16 v9, 0xbb8

    .line 30
    .line 31
    goto/16 :goto_210

    .line 32
    .line 33
    :cond_22
    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 34
    .line 35
    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    .line 36
    .line 37
    .line 38
    return-object v9

    .line 39
    :cond_28
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    .line 40
    .line 41
    check-cast v0, Ljava/io/File;

    .line 42
    .line 43
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    .line 44
    .line 45
    check-cast v0, Lqnc;

    .line 46
    .line 47
    :try_start_30
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_33
    .catch Ljava/lang/Exception; {:try_start_30 .. :try_end_33} :catch_34

    .line 48
    .line 49
    .line 50
    return-object v2

    .line 51
    :catch_34
    move-exception v0

    .line 52
    move/from16 v21, v10

    .line 53
    .line 54
    const-wide/16 v17, 0xbb8

    const-wide/16 v17, 0xbb8

    .line 55
    .line 56
    goto/16 :goto_1ef

    .line 57
    .line 58
    :cond_3d
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 59
    .line 60
    .line 61
    goto :goto_50

    .line 62
    :cond_41
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 63
    .line 64
    .line 65
    iput v10, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    .line 66
    .line 67
    const-wide/16 v11, 0x1388

    .line 68
    .line 69
    invoke-static {v11, v12, v1}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    .line 70
    .line 71
    .line 72
    move-result-object v0

    .line 73
    if-ne v0, v4, :cond_50

    .line 74
    .line 75
    goto/16 :goto_20f

    .line 76
    .line 77
    :cond_50
    :goto_50
    sget-object v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->A:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;

    .line 78
    .line 79
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 80
    .line 81
    .line 82
    sget-boolean v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->B:Z

    .line 83
    .line 84
    if-eqz v0, :cond_215

    .line 85
    .line 86
    :try_start_59
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 87
    .line 88
    iget-object v0, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 89
    .line 90
    if-eqz v0, :cond_65

    .line 91
    .line 92
    invoke-virtual {v0}, Ljava/io/File;->getParentFile()Ljava/io/File;

    .line 93
    .line 94
    .line 95
    move-result-object v0

    .line 96
    if-nez v0, :cond_6d

    .line 97
    .line 98
    :cond_65
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 99
    .line 100
    sget-object v11, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    .line 101
    .line 102
    invoke-virtual {v0, v11}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    .line 103
    .line 104
    .line 105
    move-result-object v0

    .line 106
    :cond_6d
    const/4 v11, 0x0

    .line 107
    if-eqz v0, :cond_ed

    .line 108
    .line 109
    iget-object v14, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 110
    .line 111
    const-wide/16 v15, 0x0

    .line 112
    .line 113
    invoke-virtual {v14, v0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c(Ljava/io/File;)J

    .line 114
    .line 115
    .line 116
    move-result-wide v12
    :try_end_78
    .catch Ljava/lang/Exception; {:try_start_59 .. :try_end_78} :catch_34

    .line 117
    const-wide/16 v17, 0xbb8

    .line 118
    .line 119
    :try_start_7a
    iget-wide v5, v14, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->x:J

    .line 120
    .line 121
    cmp-long v0, v5, v15

    .line 122
    .line 123
    const-wide/32 v19, 0x100000

    const-wide/32 v19, 0x100000

    .line 124
    .line 125
    .line 126
    if-lez v0, :cond_96

    .line 127
    .line 128
    const-wide/32 v21, 0x6400000

    const-wide/32 v21, 0x6400000

    .line 129
    .line 130
    .line 131
    sub-long v5, v5, v21

    .line 132
    .line 133
    cmp-long v0, v12, v5

    .line 134
    .line 135
    if-gez v0, :cond_93

    .line 136
    .line 137
    goto :goto_96

    .line 138
    :cond_93
    move/from16 v21, v10

    .line 139
    .line 140
    goto :goto_bb

    .line 141
    :cond_96
    :goto_96
    iput-wide v12, v14, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->x:J

    .line 142
    .line 143
    div-long v5, v12, v19

    .line 144
    .line 145
    new-instance v0, Ljava/lang/StringBuilder;

    .line 146
    .line 147
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    :try_end_9f
    .catch Ljava/lang/Exception; {:try_start_7a .. :try_end_9f} :catch_e8

    .line 148
    .line 149
    .line 150
    move/from16 v21, v10

    move/from16 v21, v10

    .line 151
    .line 152
    :try_start_a3
    const-string v10, "risdtad l cs- aeRAeiboeorvlgV n:aoige"

    const-string v10, "Recording Video - Available storage: "

    .line 153
    .line 154
    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 155
    .line 156
    .line 157
    invoke-virtual {v0, v5, v6}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 158
    .line 159
    .line 160
    const-string v5, "MB"

    .line 161
    .line 162
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 163
    .line 164
    .line 165
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 166
    .line 167
    .line 168
    move-result-object v0

    .line 169
    iget-wide v5, v14, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 170
    .line 171
    invoke-static {v5, v6, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 172
    .line 173
    .line 174
    :goto_bb
    const-wide/32 v5, 0x8000000

    .line 175
    .line 176
    .line 177
    cmp-long v0, v12, v5

    .line 178
    .line 179
    if-gez v0, :cond_e5

    .line 180
    .line 181
    div-long v12, v12, v19

    .line 182
    .line 183
    new-instance v0, Ljava/lang/StringBuilder;

    .line 184
    .line 185
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 186
    .line 187
    .line 188
    const-string v5, "CRITICAL: Storage space exhausted ("

    .line 189
    .line 190
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 191
    .line 192
    .line 193
    invoke-virtual {v0, v12, v13}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 194
    .line 195
    .line 196
    const-string v5, "MB remaining). Stopping recording."

    .line 197
    .line 198
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 199
    .line 200
    .line 201
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 202
    .line 203
    .line 204
    move-result-object v0

    .line 205
    iget-wide v5, v14, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 206
    .line 207
    invoke-static {v5, v6, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 208
    .line 209
    .line 210
    move/from16 v0, v21

    .line 211
    .line 212
    goto :goto_e6

    .line 213
    :catch_e2
    move-exception v0

    .line 214
    goto/16 :goto_1ef

    .line 215
    .line 216
    :cond_e5
    move v0, v11

    .line 217
    :goto_e6
    move v5, v0

    .line 218
    goto :goto_f4

    .line 219
    :catch_e8
    move-exception v0

    .line 220
    move/from16 v21, v10

    .line 221
    .line 222
    goto/16 :goto_1ef

    .line 223
    .line 224
    :cond_ed
    move/from16 v21, v10

    .line 225
    .line 226
    const-wide/16 v15, 0x0

    .line 227
    .line 228
    const-wide/16 v17, 0xbb8

    .line 229
    .line 230
    move v5, v11

    .line 231
    :goto_f4
    if-nez v5, :cond_1d2

    .line 232
    .line 233
    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 234
    .line 235
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
    :try_end_fb
    .catch Ljava/lang/Exception; {:try_start_a3 .. :try_end_fb} :catch_e2

    .line 236
    .line 237
    .line 238
    :try_start_fb
    iget-object v0, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 239
    .line 240
    if-eqz v0, :cond_116

    .line 241
    .line 242
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 243
    .line 244
    .line 245
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    .line 246
    .line 247
    .line 248
    move-result v0

    .line 249
    if-eqz v0, :cond_114

    .line 250
    .line 251
    iget-object v0, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 252
    .line 253
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 254
    .line 255
    .line 256
    invoke-virtual {v0}, Ljava/io/File;->length()J

    .line 257
    .line 258
    .line 259
    move-result-wide v12

    .line 260
    goto :goto_12d

    .line 261
    :catch_112
    move-exception v0

    .line 262
    goto :goto_11d

    .line 263
    :cond_114
    :goto_114
    move-wide v12, v15

    .line 264
    goto :goto_12d

    .line 265
    :cond_116
    iget-object v0, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;
    :try_end_118
    .catch Ljava/lang/Exception; {:try_start_fb .. :try_end_118} :catch_112

    .line 266
    .line 267
    if-eqz v0, :cond_114

    .line 268
    .line 269
    const-wide/16 v12, -0x1

    .line 270
    .line 271
    goto :goto_12d

    .line 272
    :goto_11d
    :try_start_11d
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 273
    .line 274
    .line 275
    move-result-object v0

    .line 276
    const-string v10, "Failed to get current video file size: "

    .line 277
    .line 278
    invoke-static {v10, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 279
    .line 280
    .line 281
    move-result-object v0

    .line 282
    iget-wide v12, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 283
    .line 284
    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 285
    .line 286
    .line 287
    goto :goto_114

    .line 288
    :goto_12d
    cmp-long v0, v12, v15

    .line 289
    .line 290
    if-ltz v0, :cond_1d2

    .line 291
    .line 292
    const-wide/16 v19, 0x400

    .line 293
    .line 294
    div-long v9, v12, v19

    .line 295
    .line 296
    new-instance v0, Ljava/lang/StringBuilder;

    .line 297
    .line 298
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 299
    .line 300
    .line 301
    const-string v14, "Current file size: "

    .line 302
    .line 303
    invoke-virtual {v0, v14}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 304
    .line 305
    .line 306
    invoke-virtual {v0, v9, v10}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 307
    .line 308
    .line 309
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 310
    .line 311
    .line 312
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 313
    .line 314
    .line 315
    move-result-object v0

    .line 316
    iget-object v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 317
    .line 318
    iget-wide v9, v9, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 319
    .line 320
    invoke-static {v9, v10, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 321
    .line 322
    .line 323
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 324
    .line 325
    iget-wide v9, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->v:J

    .line 326
    .line 327
    cmp-long v14, v9, v15

    .line 328
    .line 329
    if-lez v14, :cond_1ce

    .line 330
    .line 331
    sub-long v9, v12, v9

    .line 332
    .line 333
    cmp-long v14, v9, v15

    .line 334
    .line 335
    if-gtz v14, :cond_1af

    .line 336
    .line 337
    iget v9, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    .line 338
    .line 339
    add-int/lit8 v9, v9, 0x1

    .line 340
    .line 341
    iput v9, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    .line 342
    .line 343
    new-instance v0, Ljava/lang/StringBuilder;

    .line 344
    .line 345
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 346
    .line 347
    .line 348
    const-string v10, "File size not growing: check "

    .line 349
    .line 350
    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 351
    .line 352
    .line 353
    invoke-virtual {v0, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 354
    .line 355
    .line 356
    const-string v9, "/3"

    .line 357
    .line 358
    invoke-virtual {v0, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 359
    .line 360
    .line 361
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 362
    .line 363
    .line 364
    move-result-object v0

    .line 365
    iget-object v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 366
    .line 367
    iget-wide v9, v9, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 368
    .line 369
    invoke-static {v9, v10, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 370
    .line 371
    .line 372
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 373
    .line 374
    iget v0, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    .line 375
    .line 376
    if-lt v0, v8, :cond_1ce

    .line 377
    .line 378
    int-to-long v9, v0

    .line 379
    mul-long v9, v9, v17

    .line 380
    .line 381
    const-wide/16 v14, 0x3e8

    .line 382
    .line 383
    div-long/2addr v9, v14

    .line 384
    new-instance v0, Ljava/lang/StringBuilder;

    .line 385
    .line 386
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 387
    .line 388
    .line 389
    const-string v5, "I nmAosf:eIeldwd grCtTro VLofip RpiCg oe "

    const-string v5, "CRITICAL: Video file stopped growing for "

    .line 390
    .line 391
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 392
    .line 393
    .line 394
    invoke-virtual {v0, v9, v10}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 395
    .line 396
    .line 397
    const-string v5, " seconds. Storage may be full. Stopping recording."

    .line 398
    .line 399
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 400
    .line 401
    .line 402
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 403
    .line 404
    .line 405
    move-result-object v0

    .line 406
    iget-object v5, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 407
    .line 408
    iget-wide v9, v5, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 409
    .line 410
    invoke-static {v9, v10, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 411
    .line 412
    .line 413
    move/from16 v5, v21

    .line 414
    .line 415
    goto :goto_1ce

    .line 416
    :cond_1af
    iput v11, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    .line 417
    .line 418
    div-long v9, v9, v19

    .line 419
    .line 420
    new-instance v0, Ljava/lang/StringBuilder;

    .line 421
    .line 422
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 423
    .line 424
    .line 425
    const-string v11, "File growing normally: +"

    .line 426
    .line 427
    invoke-virtual {v0, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 428
    .line 429
    .line 430
    invoke-virtual {v0, v9, v10}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    .line 431
    .line 432
    .line 433
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 434
    .line 435
    .line 436
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 437
    .line 438
    .line 439
    move-result-object v0

    .line 440
    iget-object v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 441
    .line 442
    iget-wide v9, v9, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 443
    .line 444
    invoke-static {v9, v10, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 445
    .line 446
    .line 447
    :cond_1ce
    :goto_1ce
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 448
    .line 449
    iput-wide v12, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->v:J

    .line 450
    .line 451
    :cond_1d2
    if-eqz v5, :cond_1ed

    .line 452
    .line 453
    sget-object v0, Lzp4;->a:Lad4;

    .line 454
    .line 455
    sget-object v0, Lat9;->a:Lm47;

    .line 456
    .line 457
    new-instance v5, Ld31;

    .line 458
    .line 459
    iget-object v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 460
    .line 461
    const/4 v6, 0x0

    .line 462
    invoke-direct {v5, v9, v6}, Ld31;-><init>(Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;Lm73;)V

    .line 463
    .line 464
    .line 465
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    .line 466
    .line 467
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    .line 468
    .line 469
    iput v7, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    .line 470
    .line 471
    invoke-static {v0, v5, v1}, Ldt9;->e0(Li93;Ljn6;Lm73;)Ljava/lang/Object;

    .line 472
    .line 473
    .line 474
    move-result-object v0
    :try_end_1ea
    .catch Ljava/lang/Exception; {:try_start_11d .. :try_end_1ea} :catch_e2

    .line 475
    if-ne v0, v4, :cond_215

    .line 476
    .line 477
    goto :goto_20f

    .line 478
    :cond_1ed
    :goto_1ed
    const/4 v6, 0x0

    .line 479
    goto :goto_201

    .line 480
    :goto_1ef
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 481
    .line 482
    .line 483
    move-result-object v0

    .line 484
    const-string v5, "Error in storage monitoring: "

    .line 485
    .line 486
    invoke-static {v5, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 487
    .line 488
    .line 489
    move-result-object v0

    .line 490
    iget-object v5, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 491
    .line 492
    iget-wide v9, v5, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 493
    .line 494
    invoke-static {v9, v10, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 495
    .line 496
    .line 497
    goto :goto_1ed

    .line 498
    :goto_201
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    .line 499
    .line 500
    iput-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    .line 501
    .line 502
    iput v8, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    .line 503
    .line 504
    move-wide/from16 v9, v17

    .line 505
    .line 506
    invoke-static {v9, v10, v1}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    .line 507
    .line 508
    .line 509
    move-result-object v0

    .line 510
    if-ne v0, v4, :cond_210

    .line 511
    .line 512
    :goto_20f
    return-object v4

    .line 513
    :cond_210
    :goto_210
    move-object v9, v6

    .line 514
    move/from16 v10, v21

    .line 515
    .line 516
    goto/16 :goto_50

    .line 517
    .line 518
    :cond_215
    return-object v2
.end method
