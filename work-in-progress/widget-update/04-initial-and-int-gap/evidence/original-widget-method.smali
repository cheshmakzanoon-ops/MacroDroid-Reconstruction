.method public final m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;
    .locals 12

    .line 1
    instance-of v0, p3, Lcom/arlosoft/macrodroid/widget/custom/b;

    .line 2
    .line 3
    if-eqz v0, :cond_14

    .line 4
    .line 5
    move-object v0, p3

    move-object v0, p3

    .line 6
    check-cast v0, Lcom/arlosoft/macrodroid/widget/custom/b;

    .line 7
    .line 8
    iget v1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    .line 9
    .line 10
    const/high16 v2, -0x80000000

    .line 11
    .line 12
    and-int v3, v1, v2

    .line 13
    .line 14
    if-eqz v3, :cond_14

    .line 15
    .line 16
    sub-int/2addr v1, v2

    .line 17
    iput v1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    .line 18
    .line 19
    goto :goto_19

    .line 20
    :cond_14
    new-instance v0, Lcom/arlosoft/macrodroid/widget/custom/b;

    .line 21
    .line 22
    invoke-direct {v0, p0, p3}, Lcom/arlosoft/macrodroid/widget/custom/b;-><init>(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Lo73;)V

    .line 23
    .line 24
    .line 25
    :goto_19
    iget-object p3, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->result:Ljava/lang/Object;

    .line 26
    .line 27
    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 28
    .line 29
    iget v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    .line 30
    .line 31
    const/4 v3, 0x0

    .line 32
    const/4 v4, 0x1

    .line 33
    const/4 v5, 0x2

    .line 34
    const/4 v6, 0x0

    .line 35
    if-eqz v2, :cond_90

    .line 36
    .line 37
    if-eq v2, v4, :cond_57

    .line 38
    .line 39
    if-ne v2, v5, :cond_51

    .line 40
    .line 41
    iget p0, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    .line 42
    .line 43
    iget p1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    .line 44
    .line 45
    iget-object p2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    .line 46
    .line 47
    check-cast p2, Lgy6;

    .line 48
    .line 49
    iget-object p2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    .line 50
    .line 51
    check-cast p2, Ljava/util/Iterator;

    .line 52
    .line 53
    iget-object v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    .line 54
    .line 55
    check-cast v2, Ljava/lang/Iterable;

    .line 56
    .line 57
    iget-object v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    .line 58
    .line 59
    check-cast v2, Lhn9;

    .line 60
    .line 61
    iget-object v7, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    .line 62
    .line 63
    check-cast v7, Lwx6;

    .line 64
    .line 65
    iget-object v8, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    .line 66
    .line 67
    check-cast v8, Ljava/util/List;

    .line 68
    .line 69
    iget-object v8, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    .line 70
    .line 71
    check-cast v8, Landroid/content/Context;

    .line 72
    .line 73
    :try_start_49
    invoke-static {p3}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_4c
    .catch Ljava/lang/Exception; {:try_start_49 .. :try_end_4c} :catch_4e

    .line 74
    .line 75
    .line 76
    goto/16 :goto_11b

    .line 77
    .line 78
    :catch_4e
    move-exception p3

    .line 79
    goto/16 :goto_135

    .line 80
    .line 81
    :cond_51
    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 82
    .line 83
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 84
    .line 85
    .line 86
    return-object v6

    .line 87
    :cond_57
    iget p0, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I

    .line 88
    .line 89
    iget p1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    .line 90
    .line 91
    iget p2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    .line 92
    .line 93
    iget-object v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    .line 94
    .line 95
    check-cast v2, Lgy6;

    .line 96
    .line 97
    iget-object v7, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    .line 98
    .line 99
    check-cast v7, Ljava/util/Iterator;

    .line 100
    .line 101
    iget-object v8, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    .line 102
    .line 103
    check-cast v8, Ljava/lang/Iterable;

    .line 104
    .line 105
    iget-object v8, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    .line 106
    .line 107
    check-cast v8, Lhn9;

    .line 108
    .line 109
    iget-object v9, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    .line 110
    .line 111
    check-cast v9, Lwx6;

    .line 112
    .line 113
    iget-object v10, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    .line 114
    .line 115
    check-cast v10, Ljava/util/List;

    .line 116
    .line 117
    iget-object v10, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    .line 118
    .line 119
    check-cast v10, Landroid/content/Context;

    .line 120
    .line 121
    :try_start_79
    invoke-static {p3}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_7c
    .catch Ljava/lang/Exception; {:try_start_79 .. :try_end_7c} :catch_86

    .line 122
    .line 123
    .line 124
    move v11, p1

    .line 125
    move p1, p0

    .line 126
    move p0, v11

    .line 127
    move-object v11, v8

    .line 128
    move-object v8, v2

    move-object v8, v2

    .line 129
    move-object v2, v11

    move-object v2, v11

    .line 130
    goto/16 :goto_f7

    .line 131
    .line 132
    :catch_86
    move-exception p3

    .line 133
    move p0, p1

    .line 134
    move p1, p2

    .line 135
    move-object p2, v7

    .line 136
    move-object v2, v8

    move-object v2, v8

    .line 137
    :goto_8c
    move-object v7, v9

    .line 138
    move-object v8, v10

    .line 139
    goto/16 :goto_135

    .line 140
    .line 141
    :cond_90
    invoke-static {p3}, Lu2f;->P(Ljava/lang/Object;)V

    .line 142
    .line 143
    .line 144
    invoke-interface {p2}, Ljava/util/List;->isEmpty()Z

    .line 145
    .line 146
    .line 147
    move-result p3

    .line 148
    if-eqz p3, :cond_9b

    .line 149
    .line 150
    goto/16 :goto_153

    .line 151
    .line 152
    :cond_9b
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    .line 153
    .line 154
    .line 155
    new-instance p0, Lwx6;

    .line 156
    .line 157
    invoke-direct {p0, p1}, Lwx6;-><init>(Landroid/content/Context;)V

    .line 158
    .line 159
    .line 160
    new-instance p3, Lhn9;

    .line 161
    .line 162
    invoke-direct {p3}, Lhn9;-><init>()V

    .line 163
    .line 164
    .line 165
    invoke-interface {p2}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 166
    .line 167
    .line 168
    move-result-object p2

    .line 169
    move-object v7, p0

    .line 170
    move-object v2, p3

    .line 171
    move p0, v3

    .line 172
    :goto_af
    invoke-interface {p2}, Ljava/util/Iterator;->hasNext()Z

    .line 173
    .line 174
    .line 175
    move-result p3

    .line 176
    if-eqz p3, :cond_153

    .line 177
    .line 178
    invoke-interface {p2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 179
    .line 180
    .line 181
    move-result-object p3

    .line 182
    check-cast p3, Ljava/lang/Number;

    .line 183
    .line 184
    invoke-virtual {p3}, Ljava/lang/Number;->intValue()I

    .line 185
    .line 186
    .line 187
    move-result p3

    .line 188
    :try_start_bf
    iget-object v8, v7, Lwx6;->b:Landroid/appwidget/AppWidgetManager;

    .line 189
    .line 190
    invoke-virtual {v8, p3}, Landroid/appwidget/AppWidgetManager;->getAppWidgetInfo(I)Landroid/appwidget/AppWidgetProviderInfo;

    .line 191
    .line 192
    .line 193
    move-result-object v8

    .line 194
    if-eqz v8, :cond_12d

    .line 195
    .line 196
    new-instance v8, Lmh0;

    .line 197
    .line 198
    invoke-direct {v8, p3}, Lmh0;-><init>(I)V

    .line 199
    .line 200
    .line 201
    new-instance v9, Lzhh;

    .line 202
    .line 203
    invoke-direct {v9, v5, v6}, Lrff;-><init>(ILm73;)V

    .line 204
    .line 205
    .line 206
    iput-object p1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    .line 207
    .line 208
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    .line 209
    .line 210
    iput-object v7, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    .line 211
    .line 212
    iput-object v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    .line 213
    .line 214
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    .line 215
    .line 216
    iput-object p2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    .line 217
    .line 218
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    .line 219
    .line 220
    iput-object v8, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    .line 221
    .line 222
    iput p0, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    .line 223
    .line 224
    iput p3, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    .line 225
    .line 226
    iput v3, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I

    .line 227
    .line 228
    iput v4, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    .line 229
    .line 230
    invoke-static {p1, v8, v9, v0}, Lrjb;->M(Landroid/content/Context;Lgy6;Ljn6;Lo73;)Ljava/lang/Object;

    .line 231
    .line 232
    .line 233
    move-result-object v9
    :try_end_ed
    .catch Ljava/lang/Exception; {:try_start_bf .. :try_end_ed} :catch_124

    .line 234
    if-ne v9, v1, :cond_f0

    .line 235
    .line 236
    goto :goto_115

    .line 237
    :cond_f0
    move-object v10, p1

    .line 238
    move p1, v3

    .line 239
    move-object v9, v7

    .line 240
    move-object v7, p2

    .line 241
    move p2, p0

    .line 242
    move p0, p3

    move p0, p3

    .line 243
    :goto_f7
    :try_start_f7
    iput-object v10, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    .line 244
    .line 245
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    .line 246
    .line 247
    iput-object v9, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    .line 248
    .line 249
    iput-object v2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    .line 250
    .line 251
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    .line 252
    .line 253
    iput-object v7, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    .line 254
    .line 255
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    .line 256
    .line 257
    iput-object v6, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    .line 258
    .line 259
    iput p2, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    .line 260
    .line 261
    iput p0, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    .line 262
    .line 263
    iput p1, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I

    .line 264
    .line 265
    iput v5, v0, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    .line 266
    .line 267
    invoke-virtual {v2, v10, v8, v0}, Lrx6;->d(Landroid/content/Context;Lgy6;Lo73;)Ljava/lang/Object;

    .line 268
    .line 269
    .line 270
    move-result-object p0
    :try_end_113
    .catch Ljava/lang/Exception; {:try_start_f7 .. :try_end_113} :catch_11f

    .line 271
    if-ne p0, v1, :cond_116

    .line 272
    .line 273
    :goto_115
    return-object v1

    .line 274
    :cond_116
    move p1, p2

    .line 275
    move-object p2, v7

    .line 276
    move-object v7, v9

    .line 277
    move-object v8, v10

    move-object v8, v10

    .line 278
    :goto_11b
    move p0, p1

    move p0, p1

    .line 279
    move-object p1, v8

    .line 280
    goto :goto_af

    .line 281
    :catch_11f
    move-exception p3

    .line 282
    move p1, p2

    .line 283
    move-object p2, v7

    .line 284
    goto/16 :goto_8c

    .line 285
    .line 286
    :catch_124
    move-exception v8

    .line 287
    move-object v11, p1

    .line 288
    move p1, p0

    move p1, p0

    .line 289
    move p0, p3

    .line 290
    move-object p3, v8

    .line 291
    move-object v8, v11

    move-object v8, v11

    .line 292
    goto :goto_135

    .line 293
    :cond_12d
    :try_start_12d
    const-string v8, "Invalid AppWidget ID."

    .line 294
    .line 295
    new-instance v9, Ljava/lang/IllegalArgumentException;

    .line 296
    .line 297
    invoke-direct {v9, v8}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    .line 298
    .line 299
    .line 300
    throw v9
    :try_end_135
    .catch Ljava/lang/Exception; {:try_start_12d .. :try_end_135} :catch_124

    .line 301
    :goto_135
    invoke-virtual {p3}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 302
    .line 303
    .line 304
    move-result-object p3

    .line 305
    new-instance v9, Ljava/lang/StringBuilder;

    .line 306
    .line 307
    const-string v10, "Failed to update custom widget instance "

    .line 308
    .line 309
    invoke-direct {v9, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 310
    .line 311
    .line 312
    invoke-virtual {v9, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 313
    .line 314
    .line 315
    const-string p0, ": "

    .line 316
    .line 317
    invoke-virtual {v9, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 318
    .line 319
    .line 320
    invoke-virtual {v9, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 321
    .line 322
    .line 323
    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 324
    .line 325
    .line 326
    move-result-object p0

    .line 327
    invoke-static {p0}, Lkjf;->h(Ljava/lang/String;)V

    .line 328
    .line 329
    .line 330
    goto :goto_11b

    .line 331
    :cond_153
    :goto_153
    sget-object p0, Lblg;->a:Lblg;

    .line 332
    .line 333
    return-object p0
.end method