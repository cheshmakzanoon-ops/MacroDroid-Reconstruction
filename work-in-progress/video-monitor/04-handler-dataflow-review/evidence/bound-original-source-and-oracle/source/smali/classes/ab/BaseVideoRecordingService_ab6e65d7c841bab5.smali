.class public abstract Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;
.super Landroidx/lifecycle/LifecycleService;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;
    }
.end annotation

.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000\u000c\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0004\u0008\'\u0018\u00002\u00020\u0001:\u0001\u0004B\u0007\u00a2\u0006\u0004\u0008\u0002\u0010\u0003\u00a8\u0006\u0005"
    }
    d2 = {
        "Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;",
        "Landroidx/lifecycle/LifecycleService;",
        "<init>",
        "()V",
        "a",
        "app_standardRelease"
    }
    k = 0x1
    mv = {
        0x2,
        0x2,
        0x0
    }
    xi = 0x30
.end annotation


# static fields
.field public static final A:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;

.field public static volatile B:Z


# instance fields
.field public b:La6c;

.field public c:Lq0h;

.field public d:Lulc;

.field public e:Ljava/util/concurrent/ExecutorService;

.field public f:J

.field public g:Z

.field public h:Ljava/lang/String;

.field public i:Ljava/lang/String;

.field public j:Ljava/lang/String;

.field public k:Ljava/lang/String;

.field public l:Z

.field public m:Ljava/lang/String;

.field public n:Ljava/lang/String;

.field public o:Z

.field public p:I

.field public q:Z

.field public r:Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;

.field public s:J

.field public t:Ljava/io/File;

.field public u:Landroid/os/ParcelFileDescriptor;

.field public v:J

.field public w:I

.field public x:J

.field public y:I

.field public z:Z


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .line 1
    new-instance v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;

    .line 2
    .line 3
    const/4 v1, 0x7

    const/4 v1, 0x0

    .line 4
    invoke-direct {v0, v1}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;-><init>(I)V

    .line 5
    .line 6
    .line 7
    sput-object v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->A:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;

    .line 8
    .line 9
    return-void
.end method

.method public constructor <init>()V
    .locals 3

    .line 1
    invoke-direct {p0}, Landroidx/lifecycle/LifecycleService;-><init>()V

    .line 2
    .line 3
    .line 4
    const/4 v0, -0x6

    const/4 v0, -0x1

    .line 5
    const/4 v2, 0x4

    iput v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->p:I

    .line 6
    .line 7
    const/4 v2, 0x3

    const-wide/16 v0, -0x1

    const-wide/16 v0, -0x1

    .line 8
    .line 9
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->x:J

    .line 10
    .line 11
    return-void
.end method


# virtual methods
.method public final a()V
    .locals 12

    .line 1
    const-string v11, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->b:La6c;

    .line 2
    .line 3
    if-nez v0, :cond_7

    .line 4
    .line 5
    return-void

    .line 6
    :cond_7
    const/4 v11, 0x3

    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->m:Ljava/lang/String;

    .line 7
    .line 8
    if-eqz v1, :cond_66

    .line 9
    .line 10
    invoke-virtual {v1}, Ljava/lang/String;->hashCode()I

    .line 11
    .line 12
    .line 13
    move-result v2

    .line 14
    const/4 v11, 0x1

    const/16 v3, 0x8fc

    .line 15
    .line 16
    if-eq v2, v3, :cond_55

    .line 17
    .line 18
    const/16 v3, 0xa51

    .line 19
    .line 20
    if-eq v2, v3, :cond_43

    .line 21
    .line 22
    const v3, 0x10fc2

    .line 23
    .line 24
    .line 25
    if-eq v2, v3, :cond_34

    .line 26
    .line 27
    const v3, 0x14811

    .line 28
    .line 29
    .line 30
    if-eq v2, v3, :cond_24

    .line 31
    .line 32
    goto :goto_66

    .line 33
    :cond_24
    const/4 v11, 0x7

    const-string v2, "HDU"

    const-string v2, "UHD"

    .line 34
    .line 35
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 36
    .line 37
    .line 38
    move-result v1

    .line 39
    const/4 v11, 0x4

    if-nez v1, :cond_31

    .line 40
    .line 41
    goto :goto_66

    .line 42
    :cond_31
    sget-object v1, Lvw0;->h:Lvw0;

    .line 43
    .line 44
    goto :goto_7a

    .line 45
    :cond_34
    const-string v2, "FHD"

    .line 46
    .line 47
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 48
    .line 49
    .line 50
    move-result v1

    .line 51
    const/4 v11, 0x1

    if-nez v1, :cond_3e

    .line 52
    .line 53
    goto :goto_66

    .line 54
    :cond_3e
    const/4 v11, 0x3

    sget-object v1, Lvw0;->g:Lvw0;

    .line 55
    .line 56
    const/4 v11, 0x2

    goto :goto_7a

    .line 57
    :cond_43
    const/4 v11, 0x3

    const-string v2, "SD"

    const-string v2, "SD"

    .line 58
    .line 59
    const/4 v11, 0x6

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 60
    .line 61
    .line 62
    move-result v1

    .line 63
    if-nez v1, :cond_50

    .line 64
    .line 65
    goto :goto_66

    .line 66
    :cond_50
    const/4 v11, 0x2

    sget-object v1, Lvw0;->e:Lvw0;

    .line 67
    .line 68
    const/4 v11, 0x6

    goto :goto_7a

    .line 69
    :cond_55
    const/4 v11, 0x4

    const-string v2, "HD"

    .line 70
    .line 71
    const/4 v11, 0x1

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 72
    .line 73
    .line 74
    move-result v1

    .line 75
    const/4 v11, 0x3

    if-nez v1, :cond_62

    .line 76
    .line 77
    const/4 v11, 0x7

    goto :goto_66

    .line 78
    :cond_62
    const/4 v11, 0x2

    sget-object v1, Lvw0;->f:Lvw0;

    .line 79
    .line 80
    goto :goto_7a

    .line 81
    :cond_66
    :goto_66
    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->m:Ljava/lang/String;

    .line 82
    .line 83
    const/4 v11, 0x5

    const-string v2, "Unknown quality \'"

    .line 84
    .line 85
    const-string v3, "\', using HD quality"

    .line 86
    .line 87
    invoke-static {v2, v1, v3}, Lbl5;->t(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 88
    .line 89
    .line 90
    move-result-object v1

    .line 91
    const/4 v11, 0x3

    iget-wide v2, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 92
    .line 93
    const/4 v11, 0x7

    invoke-static {v2, v3, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 94
    .line 95
    .line 96
    sget-object v1, Lvw0;->f:Lvw0;

    .line 97
    .line 98
    :goto_7a
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 99
    .line 100
    .line 101
    const/4 v11, 0x0

    sget-object v2, Ltlc;->r0:Lo1c;

    .line 102
    .line 103
    sget-object v3, Ltlc;->s0:Lo1c;

    .line 104
    .line 105
    invoke-static {}, Lov0;->a()Lnv0;

    .line 106
    .line 107
    .line 108
    move-result-object v4

    .line 109
    invoke-virtual {v4}, Lnv0;->a()Lov0;

    .line 110
    .line 111
    .line 112
    move-result-object v4

    .line 113
    const/4 v11, 0x3

    invoke-static {}, Ltx0;->a()Lsx0;

    .line 114
    .line 115
    .line 116
    move-result-object v5

    .line 117
    const/4 v11, 0x1

    invoke-virtual {v5}, Lsx0;->a()Ltx0;

    .line 118
    .line 119
    .line 120
    move-result-object v5

    .line 121
    new-instance v6, Ldw0;

    .line 122
    .line 123
    const/4 v7, 0x4

    .line 124
    invoke-direct {v6, v1, v7}, Ldw0;-><init>(Lvw0;I)V

    .line 125
    .line 126
    .line 127
    sget-object v8, Lvw0;->l:Ljava/util/HashSet;

    .line 128
    .line 129
    const/4 v11, 0x3

    invoke-virtual {v8, v1}, Ljava/util/HashSet;->contains(Ljava/lang/Object;)Z

    .line 130
    .line 131
    .line 132
    move-result v8

    .line 133
    new-instance v9, Ljava/lang/StringBuilder;

    .line 134
    .line 135
    const-string v10, "lIsa lu avqt:diin"

    const-string v10, "Invalid quality: "

    .line 136
    .line 137
    invoke-direct {v9, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 138
    .line 139
    .line 140
    invoke-virtual {v9, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 141
    .line 142
    .line 143
    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 144
    .line 145
    .line 146
    move-result-object v9

    .line 147
    invoke-static {v9, v8}, Lila;->i(Ljava/lang/String;Z)V

    .line 148
    .line 149
    .line 150
    new-instance v8, Lrdb;

    .line 151
    .line 152
    invoke-static {v1}, Ljava/util/Collections;->singletonList(Ljava/lang/Object;)Ljava/util/List;

    .line 153
    .line 154
    .line 155
    move-result-object v1

    .line 156
    invoke-direct {v8, v1, v6}, Lrdb;-><init>(Ljava/util/List;Ldw0;)V

    .line 157
    .line 158
    .line 159
    const/4 v11, 0x5

    iget v1, v5, Ltx0;->b:I

    .line 160
    .line 161
    iget-object v6, v5, Ltx0;->c:Landroid/util/Range;

    .line 162
    .line 163
    const/4 v11, 0x7

    iget v5, v5, Ltx0;->d:I

    .line 164
    .line 165
    const-string v9, ""

    .line 166
    .line 167
    if-nez v6, :cond_d0

    .line 168
    .line 169
    const-string v10, " bitrate"

    .line 170
    .line 171
    const/4 v11, 0x6

    invoke-virtual {v9, v10}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 172
    .line 173
    .line 174
    move-result-object v9

    .line 175
    :cond_d0
    const/4 v11, 0x1

    invoke-virtual {v9}, Ljava/lang/String;->isEmpty()Z

    .line 176
    .line 177
    .line 178
    move-result v10

    .line 179
    if-eqz v10, :cond_233

    .line 180
    .line 181
    new-instance v9, Ltx0;

    .line 182
    .line 183
    invoke-direct {v9, v8, v1, v6, v5}, Ltx0;-><init>(Lrdb;ILandroid/util/Range;I)V

    .line 184
    .line 185
    .line 186
    new-instance v1, Ltlc;

    .line 187
    .line 188
    new-instance v5, Low0;

    .line 189
    .line 190
    const/4 v11, 0x1

    const/4 v6, -0x1

    .line 191
    invoke-direct {v5, v9, v4, v6}, Low0;-><init>(Ltx0;Lov0;I)V

    .line 192
    .line 193
    .line 194
    invoke-direct {v1, v5, v2, v2, v3}, Ltlc;-><init>(Low0;Lo1c;Lo1c;Lo1c;)V

    .line 195
    .line 196
    .line 197
    const/4 v11, 0x7

    sget-object v2, Lq0h;->E:Lo0h;

    .line 198
    .line 199
    new-instance v2, Lrde;

    .line 200
    .line 201
    invoke-direct {v2, v1}, Lrde;-><init>(Lv1h;)V

    .line 202
    .line 203
    .line 204
    new-instance v1, Lq0h;

    .line 205
    .line 206
    const/4 v11, 0x7

    new-instance v3, Lr0h;

    .line 207
    .line 208
    iget-object v2, v2, Lrde;->a:Ljava/lang/Object;

    .line 209
    .line 210
    check-cast v2, Lnha;

    .line 211
    .line 212
    const/4 v11, 0x1

    invoke-static {v2}, Lo8b;->a(Lfx2;)Lo8b;

    .line 213
    .line 214
    .line 215
    move-result-object v2

    .line 216
    invoke-direct {v3, v2}, Lr0h;-><init>(Lo8b;)V

    .line 217
    .line 218
    .line 219
    invoke-direct {v1, v3}, Lq0h;-><init>(Lr0h;)V

    .line 220
    .line 221
    .line 222
    iput-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c:Lq0h;

    .line 223
    .line 224
    iget v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->y:I

    .line 225
    .line 226
    const/4 v11, 0x6

    const/4 v2, 0x0

    .line 227
    const/4 v3, 0x1

    .line 228
    if-eq v1, v3, :cond_12e

    .line 229
    .line 230
    const/4 v4, 0x2

    .line 231
    if-eq v1, v4, :cond_134

    .line 232
    .line 233
    const/4 v11, 0x3

    const/4 v5, 0x3

    .line 234
    if-eq v1, v5, :cond_135

    .line 235
    .line 236
    if-eq v1, v7, :cond_132

    .line 237
    .line 238
    const-string v1, "display"

    .line 239
    .line 240
    invoke-virtual {p0, v1}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 241
    .line 242
    .line 243
    move-result-object v1

    .line 244
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 245
    .line 246
    .line 247
    const/4 v11, 0x1

    check-cast v1, Landroid/hardware/display/DisplayManager;

    .line 248
    .line 249
    invoke-virtual {v1, v2}, Landroid/hardware/display/DisplayManager;->getDisplay(I)Landroid/view/Display;

    .line 250
    .line 251
    .line 252
    move-result-object v1

    .line 253
    if-eqz v1, :cond_12e

    .line 254
    .line 255
    const/4 v11, 0x4

    invoke-virtual {v1}, Landroid/view/Display;->getRotation()I

    .line 256
    .line 257
    .line 258
    move-result v4

    .line 259
    goto :goto_135

    .line 260
    :cond_12e
    move v4, v2

    move v4, v2

    .line 261
    const/4 v11, 0x6

    goto :goto_135

    .line 262
    :cond_132
    move v4, v5

    .line 263
    goto :goto_135

    .line 264
    :cond_134
    move v4, v3

    .line 265
    :cond_135
    :goto_135
    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c:Lq0h;

    .line 266
    .line 267
    const/4 v11, 0x1

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 268
    .line 269
    .line 270
    const/4 v11, 0x3

    iget-object v5, v1, Luog;->g:Lyog;

    .line 271
    .line 272
    check-cast v5, Lft7;

    .line 273
    .line 274
    const/4 v11, 0x6

    invoke-interface {v5, v6}, Lft7;->H(I)I

    .line 275
    .line 276
    .line 277
    move-result v5

    .line 278
    if-eq v5, v6, :cond_149

    .line 279
    .line 280
    if-eq v5, v4, :cond_1c7

    .line 281
    .line 282
    :cond_149
    iget-object v5, v1, Luog;->e:Lyog;

    .line 283
    .line 284
    invoke-virtual {v1, v5}, Lq0h;->l(Lfx2;)Lxog;

    .line 285
    .line 286
    .line 287
    move-result-object v5

    .line 288
    move-object v7, v5

    move-object v7, v5

    .line 289
    const/4 v11, 0x3

    check-cast v7, Lrde;

    .line 290
    .line 291
    invoke-virtual {v7}, Lrde;->o()Lyog;

    .line 292
    .line 293
    .line 294
    move-result-object v8

    .line 295
    const/4 v11, 0x7

    check-cast v8, Lft7;

    .line 296
    .line 297
    invoke-interface {v8, v6}, Lft7;->H(I)I

    .line 298
    .line 299
    .line 300
    move-result v9

    .line 301
    if-eq v9, v6, :cond_163

    .line 302
    .line 303
    if-eq v9, v4, :cond_169

    .line 304
    .line 305
    :cond_163
    move-object v10, v5

    .line 306
    check-cast v10, Let7;

    .line 307
    .line 308
    invoke-interface {v10, v4}, Let7;->c(I)Ljava/lang/Object;

    .line 309
    .line 310
    .line 311
    :cond_169
    const/4 v11, 0x5

    if-eq v9, v6, :cond_1a0

    .line 312
    .line 313
    if-eq v4, v6, :cond_1a0

    .line 314
    .line 315
    if-ne v9, v4, :cond_171

    .line 316
    .line 317
    goto :goto_1a0

    .line 318
    :cond_171
    invoke-static {v9}, Lkv;->F(I)I

    .line 319
    .line 320
    .line 321
    move-result v6

    .line 322
    const/4 v11, 0x4

    invoke-static {v4}, Lkv;->F(I)I

    .line 323
    .line 324
    .line 325
    move-result v4

    .line 326
    sub-int/2addr v4, v6

    .line 327
    invoke-static {v4}, Ljava/lang/Math;->abs(I)I

    .line 328
    .line 329
    .line 330
    move-result v4

    .line 331
    rem-int/lit16 v4, v4, 0xb4

    .line 332
    .line 333
    const/16 v6, 0x5a

    .line 334
    .line 335
    if-ne v4, v6, :cond_1a0

    .line 336
    .line 337
    invoke-interface {v8}, Lft7;->v()Landroid/util/Size;

    .line 338
    .line 339
    .line 340
    move-result-object v4

    .line 341
    const/4 v11, 0x4

    if-eqz v4, :cond_1a0

    .line 342
    .line 343
    check-cast v5, Let7;

    .line 344
    .line 345
    new-instance v6, Landroid/util/Size;

    .line 346
    .line 347
    const/4 v11, 0x2

    invoke-virtual {v4}, Landroid/util/Size;->getHeight()I

    .line 348
    .line 349
    .line 350
    move-result v8

    .line 351
    invoke-virtual {v4}, Landroid/util/Size;->getWidth()I

    .line 352
    .line 353
    .line 354
    move-result v4

    .line 355
    const/4 v11, 0x4

    invoke-direct {v6, v8, v4}, Landroid/util/Size;-><init>(II)V

    .line 356
    .line 357
    .line 358
    invoke-interface {v5, v6}, Let7;->g(Landroid/util/Size;)Ljava/lang/Object;

    .line 359
    .line 360
    .line 361
    :cond_1a0
    :goto_1a0
    invoke-virtual {v7}, Lrde;->o()Lyog;

    .line 362
    .line 363
    .line 364
    move-result-object v4

    .line 365
    const/4 v11, 0x4

    iput-object v4, v1, Luog;->e:Lyog;

    .line 366
    .line 367
    const/4 v11, 0x6

    invoke-virtual {v1}, Luog;->c()Luy1;

    .line 368
    .line 369
    .line 370
    move-result-object v4

    .line 371
    const/4 v11, 0x2

    if-nez v4, :cond_1b5

    .line 372
    .line 373
    iget-object v4, v1, Luog;->e:Lyog;

    .line 374
    .line 375
    iput-object v4, v1, Luog;->g:Lyog;

    .line 376
    .line 377
    const/4 v11, 0x0

    goto :goto_1c4

    .line 378
    :cond_1b5
    invoke-interface {v4}, Luy1;->h()Lny1;

    .line 379
    .line 380
    .line 381
    move-result-object v4

    .line 382
    const/4 v11, 0x6

    iget-object v5, v1, Luog;->d:Lyog;

    .line 383
    .line 384
    iget-object v6, v1, Luog;->i:Lyog;

    .line 385
    .line 386
    invoke-virtual {v1, v4, v5, v6}, Luog;->n(Lny1;Lyog;Lyog;)Lyog;

    .line 387
    .line 388
    .line 389
    move-result-object v4

    .line 390
    iput-object v4, v1, Luog;->g:Lyog;

    .line 391
    .line 392
    :goto_1c4
    invoke-virtual {v1}, Lq0h;->M()V

    .line 393
    .line 394
    .line 395
    :cond_1c7
    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->n:Ljava/lang/String;

    .line 396
    .line 397
    const-string v4, "Front"

    .line 398
    .line 399
    invoke-static {v1, v4}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 400
    .line 401
    .line 402
    move-result v4

    .line 403
    const/4 v11, 0x4

    if-nez v4, :cond_1ff

    .line 404
    .line 405
    const v4, 0x7f140c31

    .line 406
    .line 407
    .line 408
    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 409
    .line 410
    .line 411
    move-result-object v4

    .line 412
    invoke-static {v1, v4}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 413
    .line 414
    .line 415
    move-result v4

    .line 416
    if-eqz v4, :cond_1e0

    .line 417
    .line 418
    goto :goto_1ff

    .line 419
    :cond_1e0
    const-string v4, "Rear"

    .line 420
    .line 421
    invoke-static {v1, v4}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 422
    .line 423
    .line 424
    move-result v4

    .line 425
    if-nez v4, :cond_1fc

    .line 426
    .line 427
    const v4, 0x7f141241

    .line 428
    .line 429
    .line 430
    const/4 v11, 0x1

    invoke-virtual {p0, v4}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 431
    .line 432
    .line 433
    move-result-object v4

    .line 434
    const/4 v11, 0x6

    invoke-static {v1, v4}, Lj68;->d(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 435
    .line 436
    .line 437
    move-result v1

    .line 438
    if-eqz v1, :cond_1f8

    .line 439
    .line 440
    goto :goto_1fc

    .line 441
    :cond_1f8
    const/4 v11, 0x3

    sget-object v1, Lj02;->c:Lj02;

    .line 442
    .line 443
    goto :goto_202

    .line 444
    :cond_1fc
    :goto_1fc
    sget-object v1, Lj02;->c:Lj02;

    .line 445
    .line 446
    goto :goto_202

    .line 447
    :cond_1ff
    :goto_1ff
    const/4 v11, 0x3

    sget-object v1, Lj02;->b:Lj02;

    .line 448
    .line 449
    :goto_202
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 450
    .line 451
    .line 452
    :try_start_205
    iget-object v4, v0, La6c;->a:Lg69;

    .line 453
    .line 454
    const/4 v11, 0x4

    invoke-virtual {v4}, Lg69;->f()V

    .line 455
    .line 456
    .line 457
    iget-object v4, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c:Lq0h;

    .line 458
    .line 459
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 460
    .line 461
    .line 462
    new-array v3, v3, [Luog;

    .line 463
    .line 464
    aput-object v4, v3, v2

    .line 465
    .line 466
    invoke-virtual {v0, p0, v1, v3}, La6c;->b(Ls69;Lj02;[Luog;)Ldw1;

    .line 467
    .line 468
    .line 469
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->e()V
    :try_end_21a
    .catch Ljava/lang/Exception; {:try_start_205 .. :try_end_21a} :catch_21c

    .line 470
    .line 471
    .line 472
    const/4 v11, 0x2

    return-void

    .line 473
    :catch_21c
    move-exception v0

    .line 474
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 475
    .line 476
    .line 477
    move-result-object v0

    .line 478
    const/4 v11, 0x0

    const-string v1, "Failed to bind camera: "

    .line 479
    .line 480
    const/4 v11, 0x0

    invoke-static {v1, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 481
    .line 482
    .line 483
    move-result-object v0

    .line 484
    const/4 v11, 0x4

    iget-wide v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 485
    .line 486
    invoke-static {v1, v2, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 487
    .line 488
    .line 489
    invoke-virtual {p0}, Landroid/app/Service;->stopSelf()V

    .line 490
    .line 491
    .line 492
    return-void

    .line 493
    :cond_233
    const-string p0, " timrrMepiorriinssp: eegdeqs"

    const-string p0, "Missing required properties:"

    .line 494
    .line 495
    const/4 v11, 0x5

    invoke-virtual {p0, v9}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 496
    .line 497
    .line 498
    move-result-object p0

    .line 499
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 500
    .line 501
    .line 502
    const/4 v11, 0x3

    return-void
.end method

.method public final b(Z)Landroid/app/Notification;
    .locals 7

    .line 1
    const/4 v6, 0x1

    if-eqz p1, :cond_b

    .line 2
    .line 3
    const p1, 0x7f141991

    .line 4
    .line 5
    .line 6
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 7
    .line 8
    .line 9
    move-result-object p1

    .line 10
    goto :goto_12

    .line 11
    :cond_b
    const p1, 0x7f141995

    .line 12
    .line 13
    .line 14
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 15
    .line 16
    .line 17
    move-result-object p1

    .line 18
    :goto_12
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 19
    .line 20
    .line 21
    new-instance v0, Landroid/content/Intent;

    .line 22
    .line 23
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 24
    .line 25
    .line 26
    move-result-object v1

    .line 27
    const/4 v6, 0x0

    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 28
    .line 29
    .line 30
    const-string v1, "stop_recording"

    .line 31
    .line 32
    const/4 v6, 0x5

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 33
    .line 34
    .line 35
    const/4 v6, 0x7

    const-string v1, "macro_guid"

    .line 36
    .line 37
    iget-wide v2, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 38
    .line 39
    invoke-virtual {v0, v1, v2, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;J)Landroid/content/Intent;

    .line 40
    .line 41
    .line 42
    const/high16 v1, 0xc000000

    .line 43
    .line 44
    const/4 v2, 0x0

    move v6, v2

    .line 45
    invoke-static {p0, v2, v0, v1}, Landroid/app/PendingIntent;->getService(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;

    .line 46
    .line 47
    .line 48
    move-result-object v0

    .line 49
    const/4 v6, 0x0

    new-instance v1, Lava;

    .line 50
    .line 51
    const-string v3, "video_recording_channel"

    .line 52
    .line 53
    invoke-direct {v1, p0, v3}, Lava;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 54
    .line 55
    .line 56
    invoke-static {p1}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 57
    .line 58
    .line 59
    move-result-object p1

    .line 60
    const/4 v6, 0x3

    iput-object p1, v1, Lava;->e:Ljava/lang/CharSequence;

    .line 61
    .line 62
    iget-boolean p1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->g:Z

    .line 63
    .line 64
    const/4 v3, 0x2

    const/4 v3, 0x1

    .line 65
    if-eqz p1, :cond_52

    .line 66
    .line 67
    const p1, 0x7f141996

    .line 68
    .line 69
    .line 70
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 71
    .line 72
    .line 73
    move-result-object p1

    .line 74
    goto :goto_64

    .line 75
    :cond_52
    iget-wide v4, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->f:J

    .line 76
    .line 77
    invoke-static {v4, v5}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 78
    .line 79
    .line 80
    move-result-object p1

    .line 81
    new-array v4, v3, [Ljava/lang/Object;

    .line 82
    .line 83
    aput-object p1, v4, v2

    .line 84
    .line 85
    const/4 v6, 0x0

    const p1, 0x7f141994

    .line 86
    .line 87
    .line 88
    invoke-virtual {p0, p1, v4}, Landroid/content/Context;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    .line 89
    .line 90
    .line 91
    move-result-object p1

    .line 92
    :goto_64
    invoke-static {p1}, Lava;->d(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    .line 93
    .line 94
    .line 95
    move-result-object p1

    .line 96
    iput-object p1, v1, Lava;->f:Ljava/lang/CharSequence;

    .line 97
    .line 98
    const p1, 0x7f080417

    .line 99
    .line 100
    .line 101
    iget-object v2, v1, Lava;->z:Landroid/app/Notification;

    .line 102
    .line 103
    iput p1, v2, Landroid/app/Notification;->icon:I

    .line 104
    .line 105
    iput v3, v1, Lava;->k:I

    .line 106
    .line 107
    const/4 v6, 0x4

    const/4 p1, 0x2

    .line 108
    const/4 v6, 0x1

    invoke-virtual {v1, p1, v3}, Lava;->g(IZ)V

    .line 109
    .line 110
    .line 111
    const p1, 0x7f14147b

    .line 112
    .line 113
    .line 114
    invoke-virtual {p0, p1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 115
    .line 116
    .line 117
    move-result-object p0

    .line 118
    const/4 v6, 0x3

    const p1, 0x7f0803e9

    .line 119
    .line 120
    .line 121
    const/4 v6, 0x5

    invoke-virtual {v1, p1, p0, v0}, Lava;->a(ILjava/lang/String;Landroid/app/PendingIntent;)V

    .line 122
    .line 123
    .line 124
    invoke-virtual {v1}, Lava;->b()Landroid/app/Notification;

    .line 125
    .line 126
    .line 127
    move-result-object p0

    .line 128
    const/4 v6, 0x2

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 129
    .line 130
    .line 131
    return-object p0
.end method

.method public final c(Ljava/io/File;)J
    .locals 4

    .line 1
    :try_start_0
    new-instance v0, Landroid/os/StatFs;

    .line 2
    .line 3
    invoke-virtual {p1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    .line 4
    .line 5
    .line 6
    move-result-object p1

    .line 7
    const/4 v3, 0x0

    invoke-direct {v0, p1}, Landroid/os/StatFs;-><init>(Ljava/lang/String;)V

    .line 8
    .line 9
    .line 10
    invoke-virtual {v0}, Landroid/os/StatFs;->getAvailableBlocksLong()J

    .line 11
    .line 12
    .line 13
    move-result-wide v1

    .line 14
    invoke-virtual {v0}, Landroid/os/StatFs;->getBlockSizeLong()J

    .line 15
    .line 16
    .line 17
    move-result-wide p0
    :try_end_12
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_12} :catch_14

    .line 18
    mul-long/2addr v1, p0

    .line 19
    return-wide v1

    .line 20
    :catch_14
    move-exception p1

    .line 21
    const/4 v3, 0x6

    invoke-virtual {p1}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 22
    .line 23
    .line 24
    move-result-object p1

    .line 25
    const-string v0, "Failed to get available storage: "

    .line 26
    .line 27
    invoke-static {v0, p1}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 28
    .line 29
    .line 30
    move-result-object p1

    .line 31
    const/4 v3, 0x2

    iget-wide v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 32
    .line 33
    const/4 v3, 0x6

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 34
    .line 35
    .line 36
    const-wide/16 p0, 0x0

    .line 37
    .line 38
    const/4 v3, 0x5

    return-wide p0
.end method

.method public abstract d()V
.end method

.method public final e()V
    .locals 20

    .line 1
    move-object/from16 v1, p0

    .line 2
    .line 3
    iget-object v2, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c:Lq0h;

    .line 4
    .line 5
    if-nez v2, :cond_7

    .line 6
    .line 7
    return-void

    .line 8
    :cond_7
    const-string v0, ".mp4"

    .line 9
    .line 10
    const-string v3, "Using default app-specific directory: "

    .line 11
    .line 12
    const-string v4, "gay oa:lafcblpLec th k"

    const-string v4, "Legacy path fallback: "

    .line 13
    .line 14
    const-string v5, "Using legacy path: "

    .line 15
    .line 16
    const-string v6, "Using SAF with FileDescriptor: "

    .line 17
    .line 18
    const-string v7, " slU beF iigsc pAn:ct ahlAlse"

    const-string v7, "Using All Files Access path: "

    .line 19
    .line 20
    iget-object v8, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->j:Ljava/lang/String;

    .line 21
    .line 22
    if-eqz v8, :cond_2c

    .line 23
    .line 24
    invoke-virtual {v8}, Ljava/lang/String;->length()I

    .line 25
    .line 26
    .line 27
    move-result v8

    .line 28
    if-nez v8, :cond_22

    .line 29
    .line 30
    goto :goto_2c

    .line 31
    :cond_22
    iget-object v8, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->j:Ljava/lang/String;

    .line 32
    .line 33
    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 34
    .line 35
    .line 36
    invoke-static {v8, v0}, Lz8f;->T1(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 37
    .line 38
    .line 39
    move-result-object v8

    .line 40
    goto :goto_4a

    .line 41
    :cond_2c
    :goto_2c
    new-instance v8, Ljava/text/SimpleDateFormat;

    .line 42
    .line 43
    const-string v9, "yHdsmMuyymdH_ys"

    const-string v9, "yyyyMMdd_HHmmss"

    .line 44
    .line 45
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    .line 46
    .line 47
    .line 48
    move-result-object v10

    .line 49
    invoke-direct {v8, v9, v10}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    .line 50
    .line 51
    .line 52
    new-instance v9, Ljava/util/Date;

    .line 53
    .line 54
    invoke-direct {v9}, Ljava/util/Date;-><init>()V

    .line 55
    .line 56
    .line 57
    invoke-virtual {v8, v9}, Ljava/text/DateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    .line 58
    .line 59
    .line 60
    move-result-object v8

    .line 61
    const-string v9, "OpVE_D"

    const-string v9, "VIDEO_"

    .line 62
    .line 63
    invoke-static {v9, v8}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 64
    .line 65
    .line 66
    move-result-object v8

    .line 67
    :goto_4a
    invoke-virtual {v8, v0}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 68
    .line 69
    .line 70
    move-result-object v8

    .line 71
    iget-boolean v9, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->l:Z

    .line 72
    .line 73
    const/4 v10, 0x0

    .line 74
    if-eqz v9, :cond_c0

    .line 75
    .line 76
    iget-object v9, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->k:Ljava/lang/String;

    .line 77
    .line 78
    if-eqz v9, :cond_c0

    .line 79
    .line 80
    invoke-virtual {v9}, Ljava/lang/String;->length()I

    .line 81
    .line 82
    .line 83
    move-result v9

    .line 84
    if-nez v9, :cond_5e

    .line 85
    .line 86
    goto :goto_c0

    .line 87
    :cond_5e
    :try_start_5e
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 88
    .line 89
    const/16 v3, 0x1e

    .line 90
    .line 91
    if-lt v0, v3, :cond_76

    .line 92
    .line 93
    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    .line 94
    .line 95
    .line 96
    move-result v0

    .line 97
    if-nez v0, :cond_76

    .line 98
    .line 99
    const-string v0, "All Files Access permission is required"

    .line 100
    .line 101
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 102
    .line 103
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 104
    .line 105
    .line 106
    :goto_71
    move-object v0, v10

    .line 107
    goto/16 :goto_261

    .line 108
    .line 109
    :catch_74
    move-exception v0

    .line 110
    goto :goto_b0

    .line 111
    :cond_76
    new-instance v0, Ljava/io/File;

    .line 112
    .line 113
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->k:Ljava/lang/String;

    .line 114
    .line 115
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 116
    .line 117
    .line 118
    invoke-direct {v0, v3}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 119
    .line 120
    .line 121
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    .line 122
    .line 123
    .line 124
    move-result v3

    .line 125
    if-nez v3, :cond_89

    .line 126
    .line 127
    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    .line 128
    .line 129
    .line 130
    :cond_89
    new-instance v3, Ljava/io/File;

    .line 131
    .line 132
    invoke-direct {v3, v0, v8}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 133
    .line 134
    .line 135
    iput-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 136
    .line 137
    invoke-virtual {v3}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    .line 138
    .line 139
    .line 140
    move-result-object v0

    .line 141
    new-instance v4, Ljava/lang/StringBuilder;

    .line 142
    .line 143
    invoke-direct {v4, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 144
    .line 145
    .line 146
    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 147
    .line 148
    .line 149
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 150
    .line 151
    .line 152
    move-result-object v0

    .line 153
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 154
    .line 155
    invoke-static {v4, v5, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 156
    .line 157
    .line 158
    new-instance v0, Lbw5;

    .line 159
    .line 160
    invoke-direct {v0, v3}, Lbw5;-><init>(Ljava/io/File;)V

    .line 161
    .line 162
    .line 163
    invoke-virtual {v0}, Lbw5;->T()Lay5;

    .line 164
    .line 165
    .line 166
    move-result-object v0
    :try_end_ae
    .catch Ljava/lang/Exception; {:try_start_5e .. :try_end_ae} :catch_74

    .line 167
    goto/16 :goto_261

    .line 168
    .line 169
    :goto_b0
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 170
    .line 171
    .line 172
    move-result-object v0

    .line 173
    const-string v3, "Failed to create All Files Access output options: "

    .line 174
    .line 175
    invoke-static {v3, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 176
    .line 177
    .line 178
    move-result-object v0

    .line 179
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 180
    .line 181
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 182
    .line 183
    .line 184
    goto :goto_71

    .line 185
    :cond_c0
    :goto_c0
    iget-object v7, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->h:Ljava/lang/String;

    .line 186
    .line 187
    if-eqz v7, :cond_175

    .line 188
    .line 189
    invoke-virtual {v7}, Ljava/lang/String;->length()I

    .line 190
    .line 191
    .line 192
    move-result v7

    .line 193
    if-nez v7, :cond_cc

    .line 194
    .line 195
    goto/16 :goto_175

    .line 196
    .line 197
    :cond_cc
    :try_start_cc
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->h:Ljava/lang/String;

    .line 198
    .line 199
    invoke-static {v3}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 200
    .line 201
    .line 202
    move-result-object v3

    .line 203
    invoke-static {v1, v3}, Lzr4;->j(Landroid/content/Context;Landroid/net/Uri;)Lzr4;

    .line 204
    .line 205
    .line 206
    move-result-object v3

    .line 207
    if-eqz v3, :cond_e8

    .line 208
    .line 209
    const-string v4, "dmv/oiepq"

    const-string v4, "video/mp4"

    .line 210
    .line 211
    invoke-static {v8, v0}, Lz8f;->T1(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 212
    .line 213
    .line 214
    move-result-object v0

    .line 215
    invoke-virtual {v3, v4, v0}, Lzr4;->d(Ljava/lang/String;Ljava/lang/String;)Lzr4;

    .line 216
    .line 217
    .line 218
    move-result-object v0

    .line 219
    goto :goto_ea

    .line 220
    :catch_e5
    move-exception v0

    .line 221
    goto/16 :goto_164

    .line 222
    .line 223
    :cond_e8
    move-object v0, v10

    move-object v0, v10

    .line 224
    :goto_ea
    if-eqz v0, :cond_f1

    .line 225
    .line 226
    invoke-virtual {v0}, Lzr4;->n()Landroid/net/Uri;

    .line 227
    .line 228
    .line 229
    move-result-object v3

    .line 230
    goto :goto_f3

    .line 231
    :cond_f1
    move-object v3, v10

    move-object v3, v10

    .line 232
    :goto_f3
    if-eqz v3, :cond_130

    .line 233
    .line 234
    invoke-virtual {v1}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 235
    .line 236
    .line 237
    move-result-object v3

    .line 238
    invoke-virtual {v0}, Lzr4;->n()Landroid/net/Uri;

    .line 239
    .line 240
    .line 241
    move-result-object v4

    .line 242
    const-string v5, "w"

    .line 243
    .line 244
    invoke-virtual {v3, v4, v5}, Landroid/content/ContentResolver;->openFileDescriptor(Landroid/net/Uri;Ljava/lang/String;)Landroid/os/ParcelFileDescriptor;

    .line 245
    .line 246
    .line 247
    move-result-object v3

    .line 248
    if-eqz v3, :cond_127

    .line 249
    .line 250
    iput-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;

    .line 251
    .line 252
    invoke-virtual {v0}, Lzr4;->n()Landroid/net/Uri;

    .line 253
    .line 254
    .line 255
    move-result-object v0

    .line 256
    new-instance v4, Ljava/lang/StringBuilder;

    .line 257
    .line 258
    invoke-direct {v4, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 259
    .line 260
    .line 261
    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 262
    .line 263
    .line 264
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 265
    .line 266
    .line 267
    move-result-object v0

    .line 268
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 269
    .line 270
    invoke-static {v4, v5, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 271
    .line 272
    .line 273
    new-instance v0, Lbw5;

    .line 274
    .line 275
    invoke-direct {v0, v3}, Lbw5;-><init>(Landroid/os/ParcelFileDescriptor;)V

    .line 276
    .line 277
    .line 278
    invoke-virtual {v0}, Lbw5;->S()Ldw5;

    .line 279
    .line 280
    .line 281
    move-result-object v0

    .line 282
    goto/16 :goto_261

    .line 283
    .line 284
    :cond_127
    const-string v0, "Failed to open FileDescriptor for SAF URI"

    .line 285
    .line 286
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 287
    .line 288
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 289
    .line 290
    .line 291
    goto/16 :goto_71

    .line 292
    .line 293
    :cond_130
    const-string v0, "Error - could not write to file: "

    .line 294
    .line 295
    const-string v3, ". Need to re-select path and grant access."

    .line 296
    .line 297
    invoke-static {v0, v8, v3}, Lbl5;->t(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 298
    .line 299
    .line 300
    move-result-object v0

    .line 301
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 302
    .line 303
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 304
    .line 305
    .line 306
    sget-object v0, Lcom/arlosoft/macrodroid/macro/b;->k:Lvq9;

    .line 307
    .line 308
    invoke-virtual {v0}, Lvq9;->a()Lcom/arlosoft/macrodroid/macro/b;

    .line 309
    .line 310
    .line 311
    move-result-object v0

    .line 312
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 313
    .line 314
    invoke-virtual {v0, v3, v4}, Lcom/arlosoft/macrodroid/macro/b;->J(J)Lcom/arlosoft/macrodroid/macro/Macro;

    .line 315
    .line 316
    .line 317
    move-result-object v0

    .line 318
    if-eqz v0, :cond_151

    .line 319
    .line 320
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/macro/Macro;->getName()Ljava/lang/String;

    .line 321
    .line 322
    .line 323
    move-result-object v0

    .line 324
    if-nez v0, :cond_155

    .line 325
    .line 326
    :cond_151
    const-string v0, "?"

    const-string v0, "?"

    .line 327
    .line 328
    :cond_155
    const v3, 0x7f141a25

    .line 329
    .line 330
    .line 331
    invoke-virtual {v1, v3}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 332
    .line 333
    .line 334
    move-result-object v3

    .line 335
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 336
    .line 337
    .line 338
    invoke-static {v1, v3, v0}, Lm6f;->a(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_162
    .catch Ljava/lang/Exception; {:try_start_cc .. :try_end_162} :catch_e5

    .line 339
    .line 340
    .line 341
    goto/16 :goto_71

    .line 342
    .line 343
    :goto_164
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 344
    .line 345
    .line 346
    move-result-object v0

    .line 347
    const-string v3, "Failed to create SAF output options: "

    .line 348
    .line 349
    invoke-static {v3, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 350
    .line 351
    .line 352
    move-result-object v0

    .line 353
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 354
    .line 355
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 356
    .line 357
    .line 358
    goto/16 :goto_71

    .line 359
    .line 360
    :cond_175
    :goto_175
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->i:Ljava/lang/String;

    .line 361
    .line 362
    if-eqz v0, :cond_218

    .line 363
    .line 364
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    .line 365
    .line 366
    .line 367
    move-result v0

    .line 368
    if-nez v0, :cond_181

    .line 369
    .line 370
    goto/16 :goto_218

    .line 371
    .line 372
    :cond_181
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 373
    .line 374
    const/16 v6, 0x1d

    .line 375
    .line 376
    if-ge v0, v6, :cond_218

    .line 377
    .line 378
    :try_start_187
    new-instance v0, Ljava/io/File;

    .line 379
    .line 380
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->i:Ljava/lang/String;

    .line 381
    .line 382
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 383
    .line 384
    .line 385
    invoke-direct {v0, v3}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 386
    .line 387
    .line 388
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    .line 389
    .line 390
    .line 391
    move-result v3

    .line 392
    if-nez v3, :cond_19d

    .line 393
    .line 394
    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    .line 395
    .line 396
    .line 397
    goto :goto_19d

    .line 398
    :catch_19b
    move-exception v0

    .line 399
    goto :goto_205

    .line 400
    :cond_19d
    :goto_19d
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    .line 401
    .line 402
    .line 403
    move-result v3

    .line 404
    if-eqz v3, :cond_1d0

    .line 405
    .line 406
    invoke-virtual {v0}, Ljava/io/File;->canWrite()Z

    .line 407
    .line 408
    .line 409
    move-result v3

    .line 410
    if-eqz v3, :cond_1d0

    .line 411
    .line 412
    new-instance v3, Ljava/io/File;

    .line 413
    .line 414
    invoke-direct {v3, v0, v8}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 415
    .line 416
    .line 417
    iput-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 418
    .line 419
    invoke-virtual {v3}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    .line 420
    .line 421
    .line 422
    move-result-object v0

    .line 423
    new-instance v4, Ljava/lang/StringBuilder;

    .line 424
    .line 425
    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 426
    .line 427
    .line 428
    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 429
    .line 430
    .line 431
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 432
    .line 433
    .line 434
    move-result-object v0

    .line 435
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 436
    .line 437
    invoke-static {v4, v5, v0}, Lkjf;->q(JLjava/lang/String;)V

    .line 438
    .line 439
    .line 440
    new-instance v0, Lbw5;

    .line 441
    .line 442
    invoke-direct {v0, v3}, Lbw5;-><init>(Ljava/io/File;)V

    .line 443
    .line 444
    .line 445
    invoke-virtual {v0}, Lbw5;->T()Lay5;

    .line 446
    .line 447
    .line 448
    move-result-object v0

    .line 449
    goto/16 :goto_261

    .line 450
    .line 451
    :cond_1d0
    new-instance v0, Ljava/io/File;

    .line 452
    .line 453
    sget-object v3, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    .line 454
    .line 455
    invoke-virtual {v1, v3}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    .line 456
    .line 457
    .line 458
    move-result-object v3

    .line 459
    invoke-direct {v0, v3, v8}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 460
    .line 461
    .line 462
    invoke-virtual {v0}, Ljava/io/File;->getParentFile()Ljava/io/File;

    .line 463
    .line 464
    .line 465
    move-result-object v3

    .line 466
    if-eqz v3, :cond_1e4

    .line 467
    .line 468
    invoke-virtual {v3}, Ljava/io/File;->mkdirs()Z

    .line 469
    .line 470
    .line 471
    :cond_1e4
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 472
    .line 473
    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    .line 474
    .line 475
    .line 476
    move-result-object v3

    .line 477
    new-instance v5, Ljava/lang/StringBuilder;

    .line 478
    .line 479
    invoke-direct {v5, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 480
    .line 481
    .line 482
    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 483
    .line 484
    .line 485
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 486
    .line 487
    .line 488
    move-result-object v3

    .line 489
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 490
    .line 491
    invoke-static {v4, v5, v3}, Lkjf;->q(JLjava/lang/String;)V

    .line 492
    .line 493
    .line 494
    new-instance v3, Lbw5;

    .line 495
    .line 496
    invoke-direct {v3, v0}, Lbw5;-><init>(Ljava/io/File;)V

    .line 497
    .line 498
    .line 499
    invoke-virtual {v3}, Lbw5;->T()Lay5;

    .line 500
    .line 501
    .line 502
    move-result-object v0
    :try_end_204
    .catch Ljava/lang/Exception; {:try_start_187 .. :try_end_204} :catch_19b

    .line 503
    goto :goto_261

    .line 504
    :goto_205
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 505
    .line 506
    .line 507
    move-result-object v0

    .line 508
    const-string v3, " as teoye autfoortc tiepp:nllai  oletF ugised"

    const-string v3, "Failed to create legacy file output options: "

    .line 509
    .line 510
    invoke-static {v3, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 511
    .line 512
    .line 513
    move-result-object v0

    .line 514
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 515
    .line 516
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 517
    .line 518
    .line 519
    goto/16 :goto_71

    .line 520
    .line 521
    :cond_218
    :goto_218
    :try_start_218
    new-instance v0, Ljava/io/File;

    .line 522
    .line 523
    sget-object v4, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    .line 524
    .line 525
    invoke-virtual {v1, v4}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    .line 526
    .line 527
    .line 528
    move-result-object v4

    .line 529
    invoke-direct {v0, v4, v8}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 530
    .line 531
    .line 532
    invoke-virtual {v0}, Ljava/io/File;->getParentFile()Ljava/io/File;

    .line 533
    .line 534
    .line 535
    move-result-object v4

    .line 536
    if-eqz v4, :cond_22f

    .line 537
    .line 538
    invoke-virtual {v4}, Ljava/io/File;->mkdirs()Z

    .line 539
    .line 540
    .line 541
    goto :goto_22f

    .line 542
    :catch_22d
    move-exception v0

    .line 543
    goto :goto_250

    .line 544
    :cond_22f
    :goto_22f
    iput-object v0, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 545
    .line 546
    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    .line 547
    .line 548
    .line 549
    move-result-object v4

    .line 550
    new-instance v5, Ljava/lang/StringBuilder;

    .line 551
    .line 552
    invoke-direct {v5, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 553
    .line 554
    .line 555
    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 556
    .line 557
    .line 558
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 559
    .line 560
    .line 561
    move-result-object v3

    .line 562
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 563
    .line 564
    invoke-static {v4, v5, v3}, Lkjf;->q(JLjava/lang/String;)V

    .line 565
    .line 566
    .line 567
    new-instance v3, Lbw5;

    .line 568
    .line 569
    invoke-direct {v3, v0}, Lbw5;-><init>(Ljava/io/File;)V

    .line 570
    .line 571
    .line 572
    invoke-virtual {v3}, Lbw5;->T()Lay5;

    .line 573
    .line 574
    .line 575
    move-result-object v0
    :try_end_24f
    .catch Ljava/lang/Exception; {:try_start_218 .. :try_end_24f} :catch_22d

    .line 576
    goto :goto_261

    .line 577
    :goto_250
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 578
    .line 579
    .line 580
    move-result-object v0

    .line 581
    const-string v3, "Failed to create default output options: "

    .line 582
    .line 583
    invoke-static {v3, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 584
    .line 585
    .line 586
    move-result-object v0

    .line 587
    iget-wide v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 588
    .line 589
    invoke-static {v3, v4, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 590
    .line 591
    .line 592
    goto/16 :goto_71

    .line 593
    .line 594
    :goto_261
    if-nez v0, :cond_26e

    .line 595
    .line 596
    const-string v0, "Failed to create output options for video recording"

    .line 597
    .line 598
    iget-wide v2, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 599
    .line 600
    invoke-static {v2, v3, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 601
    .line 602
    .line 603
    invoke-virtual {v1}, Landroid/app/Service;->stopSelf()V

    .line 604
    .line 605
    .line 606
    return-void

    .line 607
    :cond_26e
    iget-object v3, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 608
    .line 609
    if-eqz v3, :cond_27f

    .line 610
    .line 611
    invoke-virtual {v3}, Ljava/io/File;->getParentFile()Ljava/io/File;

    .line 612
    .line 613
    .line 614
    move-result-object v3

    .line 615
    if-nez v3, :cond_285

    .line 616
    .line 617
    sget-object v3, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    .line 618
    .line 619
    invoke-virtual {v1, v3}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    .line 620
    .line 621
    .line 622
    move-result-object v3

    .line 623
    goto :goto_285

    .line 624
    :cond_27f
    sget-object v3, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    .line 625
    .line 626
    invoke-virtual {v1, v3}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    .line 627
    .line 628
    .line 629
    move-result-object v3

    .line 630
    :cond_285
    :goto_285
    if-eqz v3, :cond_2b5

    .line 631
    .line 632
    invoke-virtual {v1, v3}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c(Ljava/io/File;)J

    .line 633
    .line 634
    .line 635
    move-result-wide v3

    .line 636
    const-wide/32 v5, 0x3200000

    .line 637
    .line 638
    .line 639
    cmp-long v5, v3, v5

    .line 640
    .line 641
    const-wide/32 v6, 0x100000

    .line 642
    .line 643
    .line 644
    if-gez v5, :cond_2a7

    .line 645
    .line 646
    div-long/2addr v3, v6

    .line 647
    const-string v0, "Insufficient storage space to start recording. Available: "

    .line 648
    .line 649
    const-string v2, "MB, Required: 50MB"

    .line 650
    .line 651
    invoke-static {v3, v4, v0, v2}, Lhvb;->v(JLjava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 652
    .line 653
    .line 654
    move-result-object v0

    .line 655
    iget-wide v2, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 656
    .line 657
    invoke-static {v2, v3, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 658
    .line 659
    .line 660
    invoke-virtual {v1}, Landroid/app/Service;->stopSelf()V

    .line 661
    .line 662
    .line 663
    return-void

    .line 664
    :cond_2a7
    div-long/2addr v3, v6

    .line 665
    const-string v5, "Available storage: "

    .line 666
    .line 667
    const-string v6, "MB"

    .line 668
    .line 669
    invoke-static {v3, v4, v5, v6}, Lhvb;->v(JLjava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 670
    .line 671
    .line 672
    move-result-object v3

    .line 673
    iget-wide v4, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 674
    .line 675
    invoke-static {v4, v5, v3}, Lkjf;->q(JLjava/lang/String;)V

    .line 676
    .line 677
    .line 678
    :cond_2b5
    instance-of v3, v0, Lay5;

    .line 679
    .line 680
    if-eqz v3, :cond_2c7

    .line 681
    .line 682
    invoke-virtual {v2}, Lq0h;->I()Lv1h;

    .line 683
    .line 684
    .line 685
    move-result-object v2

    .line 686
    check-cast v2, Ltlc;

    .line 687
    .line 688
    check-cast v0, Lay5;

    .line 689
    .line 690
    new-instance v3, Lvmb;

    .line 691
    .line 692
    invoke-direct {v3, v1, v2, v0}, Lvmb;-><init>(Landroid/content/Context;Ltlc;La3;)V

    .line 693
    .line 694
    .line 695
    goto :goto_2d7

    .line 696
    :cond_2c7
    instance-of v3, v0, Ldw5;

    .line 697
    .line 698
    if-eqz v3, :cond_425

    .line 699
    .line 700
    invoke-virtual {v2}, Lq0h;->I()Lv1h;

    .line 701
    .line 702
    .line 703
    move-result-object v2

    .line 704
    check-cast v2, Ltlc;

    .line 705
    .line 706
    check-cast v0, Ldw5;

    .line 707
    .line 708
    invoke-virtual {v2, v1, v0}, Ltlc;->r(Landroid/content/Context;Ldw5;)Lvmb;

    .line 709
    .line 710
    .line 711
    move-result-object v3

    .line 712
    :goto_2d7
    const-string v0, "android.permission.RECORD_AUDIO"

    .line 713
    .line 714
    invoke-static {v1, v0}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 715
    .line 716
    .line 717
    move-result v0

    .line 718
    const/4 v2, 0x0

    .line 719
    const/4 v4, 0x1

    .line 720
    if-nez v0, :cond_316

    .line 721
    .line 722
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 723
    .line 724
    .line 725
    iget-object v0, v3, Lvmb;->c:Landroid/content/Context;

    .line 726
    .line 727
    const-string v5, "a.RmEnr.eCOARsDdoii_iDpmndoUIrs"

    const-string v5, "android.permission.RECORD_AUDIO"

    .line 728
    .line 729
    invoke-static {v0, v5}, Lfg1;->l(Landroid/content/Context;Ljava/lang/String;)I

    .line 730
    .line 731
    .line 732
    move-result v0

    .line 733
    const/4 v5, -0x1

    .line 734
    if-eq v0, v5, :cond_30e

    .line 735
    .line 736
    iget-object v0, v3, Lvmb;->a:Ltlc;

    .line 737
    .line 738
    iget-object v0, v0, Ltlc;->E:Liq1;

    .line 739
    .line 740
    invoke-static {v0}, Ltlc;->k(Liq1;)Ljava/lang/Object;

    .line 741
    .line 742
    .line 743
    move-result-object v0

    .line 744
    check-cast v0, Low0;

    .line 745
    .line 746
    iget-object v0, v0, Low0;->b:Lov0;

    .line 747
    .line 748
    iget v0, v0, Lov0;->e:I

    .line 749
    .line 750
    if-eqz v0, :cond_304

    .line 751
    .line 752
    move v0, v4

    move v0, v4

    .line 753
    goto :goto_306

    .line 754
    :cond_304
    move v0, v2

    move v0, v2

    .line 755
    :goto_306
    const-string v5, "The Recorder this recording is associated to doesn\'t support audio."

    .line 756
    .line 757
    invoke-static {v5, v0}, Lila;->s(Ljava/lang/String;Z)V

    .line 758
    .line 759
    .line 760
    iput-boolean v4, v3, Lvmb;->f:Z

    .line 761
    .line 762
    goto :goto_316

    .line 763
    :cond_30e
    const-string v0, "ttcOoaesbfltiaoa_t eiurtoDonE lubtc  psiepAaotoCO n. rrn dede r UteIani eiphmDAgsgro R onedie odRvdamn"

    const-string v0, "Attempted to enable audio for recording but application does not have RECORD_AUDIO permission granted."

    .line 764
    .line 765
    invoke-static {v0}, Lhy2;->i(Ljava/lang/String;)V

    .line 766
    .line 767
    .line 768
    return-void

    .line 769
    :cond_316
    :goto_316
    invoke-static {v1}, Lw63;->getMainExecutor(Landroid/content/Context;)Ljava/util/concurrent/Executor;

    .line 770
    .line 771
    .line 772
    move-result-object v0

    .line 773
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 774
    .line 775
    .line 776
    new-instance v5, Lb31;

    .line 777
    .line 778
    invoke-direct {v5, v1, v2}, Lb31;-><init>(Ljava/lang/Object;I)V

    .line 779
    .line 780
    .line 781
    invoke-virtual {v3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 782
    .line 783
    .line 784
    iput-object v0, v3, Lvmb;->e:Ljava/util/concurrent/Executor;

    .line 785
    .line 786
    iput-object v5, v3, Lvmb;->d:Lb31;

    .line 787
    .line 788
    iget-object v5, v3, Lvmb;->a:Ltlc;

    .line 789
    .line 790
    iget-object v6, v5, Ltlc;->h:Ljava/lang/Object;

    .line 791
    .line 792
    monitor-enter v6

    .line 793
    :try_start_32e
    iget-wide v7, v5, Ltlc;->q:J

    .line 794
    .line 795
    const-wide/16 v11, 0x1

    .line 796
    .line 797
    add-long/2addr v7, v11

    .line 798
    iput-wide v7, v5, Ltlc;->q:J

    .line 799
    .line 800
    iget-object v0, v5, Ltlc;->l:Lslc;

    .line 801
    .line 802
    invoke-virtual {v0}, Ljava/lang/Enum;->ordinal()I

    .line 803
    .line 804
    .line 805
    move-result v0

    .line 806
    packed-switch v0, :pswitch_data_432

    .line 807
    .line 808
    .line 809
    move-wide v15, v7

    .line 810
    goto/16 :goto_3bb

    .line 811
    .line 812
    :pswitch_341
    iget-object v0, v5, Ltlc;->o:Lww0;

    .line 813
    .line 814
    :goto_343
    move-object v4, v10

    .line 815
    move-object v10, v0

    .line 816
    move-object v0, v4

    .line 817
    move v4, v2

    .line 818
    move-wide v15, v7

    .line 819
    goto/16 :goto_3c6

    .line 820
    .line 821
    :catchall_34a
    move-exception v0

    .line 822
    goto/16 :goto_423

    .line 823
    .line 824
    :pswitch_34d
    iget-object v0, v5, Ltlc;->p:Lww0;

    .line 825
    .line 826
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 827
    .line 828
    .line 829
    goto :goto_343

    .line 830
    :pswitch_353
    iget-object v0, v5, Ltlc;->l:Lslc;

    .line 831
    .line 832
    sget-object v9, Lslc;->IDLING:Lslc;

    .line 833
    .line 834
    if-ne v0, v9, :cond_369

    .line 835
    .line 836
    iget-object v0, v5, Ltlc;->o:Lww0;

    .line 837
    .line 838
    if-nez v0, :cond_363

    .line 839
    .line 840
    iget-object v0, v5, Ltlc;->p:Lww0;

    .line 841
    .line 842
    if-nez v0, :cond_363

    .line 843
    .line 844
    move v0, v4

    .line 845
    goto :goto_364

    .line 846
    :cond_363
    move v0, v2

    .line 847
    :goto_364
    const-string v11, "Expected recorder to be idle but a recording is either pending or in progress."

    .line 848
    .line 849
    invoke-static {v11, v0}, Lila;->s(Ljava/lang/String;Z)V
    :try_end_369
    .catchall {:try_start_32e .. :try_end_369} :catchall_34a

    .line 850
    .line 851
    .line 852
    :cond_369
    :try_start_369
    new-instance v13, Lww0;

    .line 853
    .line 854
    iget-object v14, v3, Lvmb;->b:La3;

    .line 855
    .line 856
    iget-object v15, v3, Lvmb;->e:Ljava/util/concurrent/Executor;

    .line 857
    .line 858
    iget-object v0, v3, Lvmb;->d:Lb31;

    .line 859
    .line 860
    iget-boolean v11, v3, Lvmb;->f:Z
    :try_end_373
    .catch Ljava/io/IOException; {:try_start_369 .. :try_end_373} :catch_3c3
    .catchall {:try_start_369 .. :try_end_373} :catchall_34a

    .line 861
    .line 862
    move-object/from16 v16, v0

    move-object/from16 v16, v0

    .line 863
    .line 864
    move-wide/from16 v18, v7

    .line 865
    .line 866
    move/from16 v17, v11

    .line 867
    .line 868
    :try_start_37b
    invoke-direct/range {v13 .. v19}, Lww0;-><init>(La3;Ljava/util/concurrent/Executor;Lb31;ZJ)V
    :try_end_37e
    .catch Ljava/io/IOException; {:try_start_37b .. :try_end_37e} :catch_3bf
    .catchall {:try_start_37b .. :try_end_37e} :catchall_34a

    .line 869
    .line 870
    .line 871
    move-wide/from16 v15, v18

    .line 872
    .line 873
    :try_start_380
    iget-object v0, v13, Lww0;->f:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 874
    .line 875
    invoke-virtual {v0, v2}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 876
    .line 877
    .line 878
    iget-object v0, v3, Lvmb;->c:Landroid/content/Context;

    .line 879
    .line 880
    invoke-virtual {v13, v0}, Lww0;->c(Landroid/content/Context;)V

    .line 881
    .line 882
    .line 883
    iput-object v13, v5, Ltlc;->p:Lww0;

    .line 884
    .line 885
    iget-object v0, v5, Ltlc;->l:Lslc;

    .line 886
    .line 887
    if-ne v0, v9, :cond_3a2

    .line 888
    .line 889
    sget-object v0, Lslc;->PENDING_RECORDING:Lslc;

    .line 890
    .line 891
    invoke-virtual {v5, v0}, Ltlc;->B(Lslc;)V

    .line 892
    .line 893
    .line 894
    iget-object v0, v5, Ltlc;->d:Le9e;

    .line 895
    .line 896
    new-instance v4, Lklc;

    .line 897
    .line 898
    invoke-direct {v4, v5, v2}, Lklc;-><init>(Ltlc;I)V

    .line 899
    .line 900
    .line 901
    invoke-virtual {v0, v4}, Le9e;->execute(Ljava/lang/Runnable;)V

    .line 902
    .line 903
    .line 904
    goto :goto_3bb

    .line 905
    :catch_3a0
    move-exception v0

    .line 906
    goto :goto_3c5

    .line 907
    :cond_3a2
    sget-object v7, Lslc;->ERROR:Lslc;

    .line 908
    .line 909
    if-ne v0, v7, :cond_3b6

    .line 910
    .line 911
    sget-object v0, Lslc;->PENDING_RECORDING:Lslc;

    .line 912
    .line 913
    invoke-virtual {v5, v0}, Ltlc;->B(Lslc;)V

    .line 914
    .line 915
    .line 916
    iget-object v0, v5, Ltlc;->d:Le9e;

    .line 917
    .line 918
    new-instance v7, Lklc;

    .line 919
    .line 920
    invoke-direct {v7, v5, v4}, Lklc;-><init>(Ltlc;I)V

    .line 921
    .line 922
    .line 923
    invoke-virtual {v0, v7}, Le9e;->execute(Ljava/lang/Runnable;)V

    .line 924
    .line 925
    .line 926
    goto :goto_3bb

    .line 927
    :cond_3b6
    sget-object v0, Lslc;->PENDING_RECORDING:Lslc;

    .line 928
    .line 929
    invoke-virtual {v5, v0}, Ltlc;->B(Lslc;)V
    :try_end_3bb
    .catch Ljava/io/IOException; {:try_start_380 .. :try_end_3bb} :catch_3a0
    .catchall {:try_start_380 .. :try_end_3bb} :catchall_34a

    .line 930
    .line 931
    .line 932
    :goto_3bb
    move v4, v2

    .line 933
    move-object v0, v10

    move-object v0, v10

    .line 934
    goto :goto_3c6

    .line 935
    :catch_3bf
    move-exception v0

    .line 936
    move-wide/from16 v15, v18

    .line 937
    .line 938
    goto :goto_3c5

    .line 939
    :catch_3c3
    move-exception v0

    .line 940
    move-wide v15, v7

    .line 941
    :goto_3c5
    const/4 v4, 0x5

    .line 942
    :goto_3c6
    :try_start_3c6
    monitor-exit v6
    :try_end_3c7
    .catchall {:try_start_3c6 .. :try_end_3c7} :catchall_34a

    .line 943
    if-nez v10, :cond_41d

    .line 944
    .line 945
    if-eqz v4, :cond_40b

    .line 946
    .line 947
    const-string v6, "eecrrbod"

    const-string v6, "Recorder"

    .line 948
    .line 949
    new-instance v7, Ljava/lang/StringBuilder;

    .line 950
    .line 951
    const-string v8, "Recording was started when the Recorder had encountered error "

    .line 952
    .line 953
    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 954
    .line 955
    .line 956
    invoke-virtual {v7, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 957
    .line 958
    .line 959
    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 960
    .line 961
    .line 962
    move-result-object v7

    .line 963
    invoke-static {v6, v7}, Lnug;->w(Ljava/lang/String;Ljava/lang/String;)V

    .line 964
    .line 965
    .line 966
    new-instance v13, Lww0;

    .line 967
    .line 968
    iget-object v14, v3, Lvmb;->b:La3;

    .line 969
    .line 970
    move-wide/from16 v18, v15

    .line 971
    .line 972
    iget-object v15, v3, Lvmb;->e:Ljava/util/concurrent/Executor;

    .line 973
    .line 974
    iget-object v6, v3, Lvmb;->d:Lb31;

    .line 975
    .line 976
    iget-boolean v7, v3, Lvmb;->f:Z

    .line 977
    .line 978
    move-object/from16 v16, v6

    .line 979
    .line 980
    move/from16 v17, v7

    .line 981
    .line 982
    invoke-direct/range {v13 .. v19}, Lww0;-><init>(La3;Ljava/util/concurrent/Executor;Lb31;ZJ)V

    .line 983
    .line 984
    .line 985
    move-wide/from16 v15, v18

    .line 986
    .line 987
    iget-object v6, v13, Lww0;->f:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 988
    .line 989
    invoke-virtual {v6, v2}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 990
    .line 991
    .line 992
    invoke-virtual {v5, v13, v4, v0}, Ltlc;->i(Lww0;ILjava/lang/Throwable;)V

    .line 993
    .line 994
    .line 995
    new-instance v13, Lulc;

    .line 996
    .line 997
    iget-object v14, v3, Lvmb;->a:Ltlc;

    .line 998
    .line 999
    iget-object v0, v3, Lvmb;->b:La3;

    .line 1000
    .line 1001
    const/16 v18, 0x1

    .line 1002
    .line 1003
    move-object/from16 v17, v0

    .line 1004
    .line 1005
    invoke-direct/range {v13 .. v18}, Lulc;-><init>(Ltlc;JLa3;Z)V

    .line 1006
    .line 1007
    .line 1008
    goto :goto_41a

    .line 1009
    :cond_40b
    new-instance v13, Lulc;

    .line 1010
    .line 1011
    iget-object v14, v3, Lvmb;->a:Ltlc;

    .line 1012
    .line 1013
    iget-object v0, v3, Lvmb;->b:La3;

    .line 1014
    .line 1015
    const/16 v18, 0x0

    .line 1016
    .line 1017
    move-object/from16 v17, v0

    move-object/from16 v17, v0

    .line 1018
    .line 1019
    invoke-direct/range {v13 .. v18}, Lulc;-><init>(Ltlc;JLa3;Z)V

    .line 1020
    .line 1021
    .line 1022
    :goto_41a
    iput-object v13, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->d:Lulc;

    .line 1023
    .line 1024
    return-void

    .line 1025
    :cond_41d
    const-string v0, "A recording is already in progress. Previous recordings must be stopped before a new recording can be started."

    .line 1026
    .line 1027
    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    .line 1028
    .line 1029
    .line 1030
    return-void

    .line 1031
    :goto_423
    :try_start_423
    monitor-exit v6
    :try_end_424
    .catchall {:try_start_423 .. :try_end_424} :catchall_34a

    .line 1032
    throw v0

    .line 1033
    :cond_425
    const-string v0, " ddsUrutoiofppn ie o rrn tn wkocvuoneigypotneto"

    const-string v0, "Unknown output options type for video recording"

    .line 1034
    .line 1035
    iget-wide v2, v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 1036
    .line 1037
    invoke-static {v2, v3, v0}, Lkjf;->g(JLjava/lang/String;)V

    .line 1038
    .line 1039
    .line 1040
    invoke-virtual {v1}, Landroid/app/Service;->stopSelf()V

    .line 1041
    .line 1042
    .line 1043
    return-void

    .line 1044
    .line 1045
    :pswitch_data_432
    .packed-switch 0x0
        :pswitch_353
        :pswitch_34d
        :pswitch_34d
        :pswitch_353
        :pswitch_341
        :pswitch_341
        :pswitch_353
        :pswitch_353
        :pswitch_353
    .end packed-switch
.end method

.method public final f()V
    .locals 5

    .line 1
    iget-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->d:Lulc;

    .line 2
    .line 3
    if-eqz v0, :cond_7

    .line 4
    .line 5
    invoke-virtual {v0}, Lulc;->close()V

    .line 6
    .line 7
    .line 8
    :cond_7
    const/4 v0, 0x0

    .line 9
    const/4 v4, 0x6

    iput-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->d:Lulc;

    .line 10
    .line 11
    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->b:La6c;

    .line 12
    .line 13
    const/4 v4, 0x5

    if-eqz v1, :cond_15

    .line 14
    .line 15
    iget-object v1, v1, La6c;->a:Lg69;

    .line 16
    .line 17
    invoke-virtual {v1}, Lg69;->f()V

    .line 18
    .line 19
    .line 20
    :cond_15
    const/4 v4, 0x4

    const/4 v1, 0x0

    .line 21
    const/4 v4, 0x4

    sput-boolean v1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->B:Z

    .line 22
    .line 23
    const/4 v4, 0x0

    iput-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    .line 24
    .line 25
    const-wide/16 v2, 0x0

    const-wide/16 v2, 0x0

    .line 26
    .line 27
    iput-wide v2, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->v:J

    .line 28
    .line 29
    iput v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    .line 30
    .line 31
    iget-object v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;

    .line 32
    .line 33
    const/4 v4, 0x2

    if-eqz v1, :cond_2d

    .line 34
    .line 35
    invoke-virtual {v1}, Landroid/os/ParcelFileDescriptor;->close()V

    .line 36
    .line 37
    .line 38
    :cond_2d
    iput-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;

    .line 39
    .line 40
    const/4 v4, 0x7

    const/4 v0, 0x1

    .line 41
    invoke-virtual {p0, v0}, Landroid/app/Service;->stopForeground(Z)V

    .line 42
    .line 43
    .line 44
    invoke-virtual {p0}, Landroid/app/Service;->stopSelf()V

    .line 45
    .line 46
    .line 47
    return-void
.end method

.method public final onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    const/4 p0, 0x0

    .line 5
    return-object p0
.end method

.method public final onCreate()V
    .locals 5

    .line 1
    const/4 v4, 0x6

    invoke-super {p0}, Landroidx/lifecycle/LifecycleService;->onCreate()V

    .line 2
    .line 3
    .line 4
    const/4 v4, 0x3

    const/16 v0, -0x13

    .line 5
    .line 6
    const/4 v4, 0x3

    invoke-static {v0}, Landroid/os/Process;->setThreadPriority(I)V

    .line 7
    .line 8
    .line 9
    invoke-static {}, Ljava/util/concurrent/Executors;->newSingleThreadExecutor()Ljava/util/concurrent/ExecutorService;

    .line 10
    .line 11
    .line 12
    move-result-object v0

    .line 13
    const/4 v4, 0x0

    iput-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->e:Ljava/util/concurrent/ExecutorService;

    .line 14
    .line 15
    const/4 v4, 0x4

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 16
    .line 17
    const/16 v1, 0x1a

    .line 18
    .line 19
    if-lt v0, v1, :cond_4b

    .line 20
    .line 21
    invoke-static {}, Lmr0;->c()V

    .line 22
    .line 23
    .line 24
    const v0, 0x7f141993

    .line 25
    .line 26
    .line 27
    const/4 v4, 0x3

    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 28
    .line 29
    .line 30
    move-result-object v0

    .line 31
    const/4 v4, 0x4

    new-instance v1, Landroid/app/NotificationChannel;

    .line 32
    .line 33
    const-string v2, "ongohdipleevced_inrcrn_"

    const-string v2, "video_recording_channel"

    .line 34
    .line 35
    const/4 v3, 0x4

    move v4, v3

    .line 36
    invoke-direct {v1, v2, v0, v3}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V

    .line 37
    .line 38
    .line 39
    const v0, 0x7f141992

    .line 40
    .line 41
    .line 42
    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 43
    .line 44
    .line 45
    move-result-object v0

    .line 46
    invoke-virtual {v1, v0}, Landroid/app/NotificationChannel;->setDescription(Ljava/lang/String;)V

    .line 47
    .line 48
    .line 49
    const/4 v0, 0x0

    .line 50
    invoke-virtual {v1, v0, v0}, Landroid/app/NotificationChannel;->setSound(Landroid/net/Uri;Landroid/media/AudioAttributes;)V

    .line 51
    .line 52
    .line 53
    const-class v0, Landroid/app/NotificationManager;

    .line 54
    .line 55
    invoke-virtual {p0, v0}, Landroid/content/Context;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    .line 56
    .line 57
    .line 58
    move-result-object p0

    .line 59
    const/4 v4, 0x4

    check-cast p0, Landroid/app/NotificationManager;

    .line 60
    .line 61
    const/4 v4, 0x4

    invoke-virtual {p0, v1}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V

    .line 62
    .line 63
    .line 64
    :cond_4b
    const/4 v4, 0x0

    return-void
.end method

.method public final onDestroy()V
    .locals 2

    .line 1
    invoke-super {p0}, Landroidx/lifecycle/LifecycleService;->onDestroy()V

    .line 2
    .line 3
    .line 4
    const/4 v1, 0x6

    const/4 v0, 0x0

    .line 5
    const/4 v1, 0x2

    sput-boolean v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->B:Z

    .line 6
    .line 7
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->f()V

    .line 8
    .line 9
    .line 10
    const/4 v1, 0x2

    iget-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->e:Ljava/util/concurrent/ExecutorService;

    .line 11
    .line 12
    if-eqz v0, :cond_13

    .line 13
    .line 14
    invoke-interface {v0}, Ljava/util/concurrent/ExecutorService;->shutdown()V

    .line 15
    .line 16
    .line 17
    :cond_13
    iget-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;

    .line 18
    .line 19
    if-eqz v0, :cond_1a

    .line 20
    .line 21
    invoke-virtual {v0}, Landroid/os/ParcelFileDescriptor;->close()V

    .line 22
    .line 23
    .line 24
    :cond_1a
    const/4 v0, 0x3

    const/4 v0, 0x0

    .line 25
    const/4 v1, 0x1

    iput-object v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;

    .line 26
    .line 27
    return-void
.end method

.method public final onStartCommand(Landroid/content/Intent;II)I
    .locals 8

    .line 1
    invoke-super {p0, p1, p2, p3}, Landroid/app/Service;->onStartCommand(Landroid/content/Intent;II)I

    .line 2
    .line 3
    .line 4
    const/4 v7, 0x7

    const/4 p2, 0x0

    .line 5
    if-eqz p1, :cond_c

    .line 6
    .line 7
    invoke-virtual {p1}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    .line 8
    .line 9
    .line 10
    move-result-object p3

    .line 11
    goto :goto_e

    .line 12
    :cond_c
    move-object p3, p2

    move-object p3, p2

    .line 13
    :goto_e
    const/4 v7, 0x4

    if-eqz p3, :cond_1c4

    .line 14
    .line 15
    invoke-virtual {p3}, Ljava/lang/String;->hashCode()I

    .line 16
    .line 17
    .line 18
    move-result v0

    .line 19
    const v1, -0x231455ac

    .line 20
    .line 21
    .line 22
    const-wide/16 v2, 0x0

    .line 23
    .line 24
    if-eq v0, v1, :cond_40

    .line 25
    .line 26
    const p2, -0x19711a0c

    .line 27
    .line 28
    .line 29
    if-eq v0, p2, :cond_23

    .line 30
    .line 31
    goto/16 :goto_1c4

    .line 32
    .line 33
    :cond_23
    const-string p2, "o_rtrcsnqpedog"

    const-string p2, "stop_recording"

    .line 34
    .line 35
    const/4 v7, 0x5

    invoke-virtual {p3, p2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 36
    .line 37
    .line 38
    move-result p2

    .line 39
    if-nez p2, :cond_31

    .line 40
    .line 41
    const/4 v7, 0x5

    goto/16 :goto_1c4

    .line 42
    .line 43
    :cond_31
    const-string p2, "macro_guid"

    .line 44
    .line 45
    invoke-virtual {p1, p2, v2, v3}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 46
    .line 47
    .line 48
    move-result-wide p1

    .line 49
    const/4 v7, 0x5

    iput-wide p1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 50
    .line 51
    const/4 v7, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->f()V

    .line 52
    .line 53
    .line 54
    goto/16 :goto_1c4

    .line 55
    .line 56
    :cond_40
    const-string v0, "start_recording"

    .line 57
    .line 58
    invoke-virtual {p3, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 59
    .line 60
    .line 61
    move-result p3

    .line 62
    const/4 v7, 0x5

    if-eqz p3, :cond_1c4

    .line 63
    .line 64
    const/4 v7, 0x2

    const-string p3, "itsaondu"

    const-string p3, "duration"

    .line 65
    .line 66
    const-wide/16 v0, 0xa

    .line 67
    .line 68
    invoke-virtual {p1, p3, v0, v1}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 69
    .line 70
    .line 71
    move-result-wide v0

    .line 72
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->f:J

    .line 73
    .line 74
    const-string p3, "record_until_stopped"

    .line 75
    .line 76
    const/4 v7, 0x5

    const/4 v0, 0x0

    .line 77
    const/4 v7, 0x3

    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 78
    .line 79
    .line 80
    move-result p3

    .line 81
    iput-boolean p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->g:Z

    .line 82
    .line 83
    const/4 v7, 0x3

    const-string p3, "rlnmostuei"

    const-string p3, "resolution"

    .line 84
    .line 85
    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 86
    .line 87
    .line 88
    move-result-object p3

    .line 89
    const/4 v7, 0x0

    if-nez p3, :cond_6f

    .line 90
    .line 91
    const-string p3, "HD"

    .line 92
    .line 93
    :cond_6f
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->m:Ljava/lang/String;

    .line 94
    .line 95
    const-string p3, "camera"

    .line 96
    .line 97
    const/4 v7, 0x1

    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 98
    .line 99
    .line 100
    move-result-object p3

    .line 101
    if-nez p3, :cond_7c

    .line 102
    .line 103
    const-string p3, "Rear"

    .line 104
    .line 105
    :cond_7c
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->n:Ljava/lang/String;

    .line 106
    .line 107
    const-string p3, "blocking_mode"

    .line 108
    .line 109
    const/4 v7, 0x0

    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 110
    .line 111
    .line 112
    move-result p3

    .line 113
    iput-boolean p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->o:Z

    .line 114
    .line 115
    const/4 v7, 0x2

    const-string p3, "macro_guid"

    .line 116
    .line 117
    invoke-virtual {p1, p3, v2, v3}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 118
    .line 119
    .line 120
    move-result-wide v4

    .line 121
    const/4 v7, 0x7

    iput-wide v4, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 122
    .line 123
    const/4 v7, 0x5

    const-string p3, "next_action"

    .line 124
    .line 125
    const/4 v7, 0x5

    const/4 v1, -0x1

    .line 126
    const/4 v7, 0x2

    invoke-virtual {p1, p3, v1}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 127
    .line 128
    .line 129
    move-result p3

    .line 130
    const/4 v7, 0x2

    iput p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->p:I

    .line 131
    .line 132
    const-string p3, "force_even_if_not_enabled"

    .line 133
    .line 134
    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 135
    .line 136
    .line 137
    move-result p3

    .line 138
    iput-boolean p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->q:Z

    .line 139
    .line 140
    const-string p3, "resume_macro_info"

    .line 141
    .line 142
    invoke-virtual {p1, p3}, Landroid/content/Intent;->getParcelableExtra(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 143
    .line 144
    .line 145
    move-result-object p3

    .line 146
    check-cast p3, Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;

    .line 147
    .line 148
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->r:Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;

    .line 149
    .line 150
    const/4 v7, 0x7

    const-string p3, "path_uri"

    .line 151
    .line 152
    const/4 v7, 0x4

    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 153
    .line 154
    .line 155
    move-result-object p3

    .line 156
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->h:Ljava/lang/String;

    .line 157
    .line 158
    const-string p3, "ptah"

    const-string p3, "path"

    .line 159
    .line 160
    const/4 v7, 0x4

    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 161
    .line 162
    .line 163
    move-result-object p3

    .line 164
    const/4 v7, 0x0

    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->i:Ljava/lang/String;

    .line 165
    .line 166
    const-string p3, "nlseocaimtou_mf"

    const-string p3, "custom_filename"

    .line 167
    .line 168
    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 169
    .line 170
    .line 171
    move-result-object p3

    .line 172
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->j:Ljava/lang/String;

    .line 173
    .line 174
    const-string p3, "use_all_files_access"

    .line 175
    .line 176
    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 177
    .line 178
    .line 179
    move-result p3

    .line 180
    const/4 v7, 0x0

    iput-boolean p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->l:Z

    .line 181
    .line 182
    const-string p3, "_talibhsll_efp"

    const-string p3, "all_files_path"

    .line 183
    .line 184
    const/4 v7, 0x4

    invoke-virtual {p1, p3}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 185
    .line 186
    .line 187
    move-result-object p3

    .line 188
    iput-object p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->k:Ljava/lang/String;

    .line 189
    .line 190
    const/4 v7, 0x4

    const-string p3, "macro_guid"

    .line 191
    .line 192
    invoke-virtual {p1, p3, v2, v3}, Landroid/content/Intent;->getLongExtra(Ljava/lang/String;J)J

    .line 193
    .line 194
    .line 195
    move-result-wide v1

    .line 196
    const/4 v7, 0x5

    iput-wide v1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 197
    .line 198
    const/4 v7, 0x1

    const-string p3, "usestT"

    const-string p3, "IsTest"

    .line 199
    .line 200
    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 201
    .line 202
    .line 203
    move-result p3

    .line 204
    const/4 v7, 0x4

    iput-boolean p3, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->z:Z

    .line 205
    .line 206
    const-string p3, "ienovttpdoroarr_i"

    const-string p3, "rotation_override"

    .line 207
    .line 208
    invoke-virtual {p1, p3, v0}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 209
    .line 210
    .line 211
    move-result p1

    .line 212
    iput p1, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->y:I

    .line 213
    .line 214
    const-string p1, "android.permission.CAMERA"

    .line 215
    .line 216
    invoke-static {p0, p1}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 217
    .line 218
    .line 219
    move-result p1

    .line 220
    if-nez p1, :cond_1b9

    .line 221
    .line 222
    const-string p1, "android.permission.RECORD_AUDIO"

    .line 223
    .line 224
    invoke-static {p0, p1}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 225
    .line 226
    .line 227
    move-result p1

    .line 228
    const/4 v7, 0x5

    if-nez p1, :cond_1b9

    .line 229
    .line 230
    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 231
    .line 232
    const/16 p3, 0x1d

    .line 233
    .line 234
    if-ge p1, p3, :cond_124

    .line 235
    .line 236
    const-string p1, "android.permission.WRITE_EXTERNAL_STORAGE"

    .line 237
    .line 238
    const/4 v7, 0x1

    invoke-static {p0, p1}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 239
    .line 240
    .line 241
    move-result p1

    .line 242
    if-nez p1, :cond_1b9

    .line 243
    .line 244
    :cond_124
    sget-boolean p1, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->B:Z

    .line 245
    .line 246
    if-eqz p1, :cond_135

    .line 247
    .line 248
    const-string p1, "Video recording already in progress"

    .line 249
    .line 250
    iget-wide p2, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 251
    .line 252
    const/4 v7, 0x7

    invoke-static {p2, p3, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 253
    .line 254
    .line 255
    invoke-virtual {p0}, Landroid/app/Service;->stopSelf()V

    .line 256
    .line 257
    .line 258
    goto/16 :goto_1c4

    .line 259
    .line 260
    :cond_135
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->d()V

    .line 261
    .line 262
    .line 263
    const/4 v7, 0x0

    sget-object p1, La6c;->b:La6c;

    .line 264
    .line 265
    iget-object p1, p1, La6c;->a:Lg69;

    .line 266
    .line 267
    iget-object v1, p1, Lg69;->a:Ljava/lang/Object;

    .line 268
    .line 269
    monitor-enter v1

    .line 270
    :try_start_140
    const/4 v7, 0x0

    iget-object v2, p1, Lg69;->b:Lso6;
    :try_end_143
    .catchall {:try_start_140 .. :try_end_143} :catchall_1b4

    .line 271
    .line 272
    const/16 v3, 0x15

    .line 273
    .line 274
    if-eqz v2, :cond_149

    .line 275
    .line 276
    monitor-exit v1

    .line 277
    goto :goto_187

    .line 278
    :cond_149
    :try_start_149
    new-instance v2, Lx02;

    .line 279
    .line 280
    invoke-direct {v2, p0, p2}, Lx02;-><init>(Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;Lf69;)V

    .line 281
    .line 282
    .line 283
    const/4 v7, 0x4

    iget p2, v2, Lx02;->r:I

    .line 284
    .line 285
    iput p2, p1, Lg69;->i:I

    .line 286
    .line 287
    const/4 v7, 0x3

    iget-object p2, p1, Lg69;->c:Lcom/google/common/util/concurrent/ListenableFuture;

    .line 288
    .line 289
    const/4 v7, 0x7

    invoke-static {p2}, Lso6;->a(Lcom/google/common/util/concurrent/ListenableFuture;)Lso6;

    .line 290
    .line 291
    .line 292
    move-result-object p2

    .line 293
    new-instance v4, Lbb6;

    .line 294
    .line 295
    invoke-direct {v4, v2, v3}, Lbb6;-><init>(Ljava/lang/Object;I)V

    .line 296
    .line 297
    .line 298
    new-instance v5, Lfd6;

    .line 299
    .line 300
    const/4 v7, 0x0

    const/16 v6, 0xb

    .line 301
    .line 302
    invoke-direct {v5, v4, v6}, Lfd6;-><init>(Ljava/lang/Object;I)V

    .line 303
    .line 304
    .line 305
    invoke-static {}, Lzn4;->b()Lzn4;

    .line 306
    .line 307
    .line 308
    move-result-object v4

    .line 309
    const/4 v7, 0x0

    invoke-static {p2, v5, v4}, Lxt0;->d0(Lcom/google/common/util/concurrent/ListenableFuture;Lxl0;Ljava/util/concurrent/Executor;)Ld62;

    .line 310
    .line 311
    .line 312
    move-result-object p2

    .line 313
    const/4 v7, 0x6

    iput-object p2, p1, Lg69;->b:Lso6;

    .line 314
    .line 315
    new-instance v4, Lqrb;

    .line 316
    .line 317
    invoke-direct {v4, p1, v2, p0, p3}, Lqrb;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 318
    .line 319
    .line 320
    invoke-static {}, Lzn4;->b()Lzn4;

    .line 321
    .line 322
    .line 323
    move-result-object p1

    .line 324
    const/4 v7, 0x4

    invoke-static {p2, v4, p1}, Lxt0;->d(Lcom/google/common/util/concurrent/ListenableFuture;Lro6;Ljava/util/concurrent/Executor;)V

    .line 325
    .line 326
    .line 327
    invoke-static {p2}, Lxt0;->I(Lcom/google/common/util/concurrent/ListenableFuture;)Lcom/google/common/util/concurrent/ListenableFuture;

    .line 328
    .line 329
    .line 330
    move-result-object v2
    :try_end_185
    .catchall {:try_start_149 .. :try_end_185} :catchall_1b4

    .line 331
    const/4 v7, 0x4

    monitor-exit v1

    .line 332
    :goto_187
    new-instance p1, Lz5c;

    .line 333
    .line 334
    invoke-direct {p1, v0}, Lz5c;-><init>(I)V

    .line 335
    .line 336
    .line 337
    new-instance p2, Lo1c;

    .line 338
    .line 339
    const/4 v7, 0x1

    invoke-direct {p2, p1}, Lo1c;-><init>(Lz5c;)V

    .line 340
    .line 341
    .line 342
    invoke-static {}, Lzn4;->b()Lzn4;

    .line 343
    .line 344
    .line 345
    move-result-object p1

    .line 346
    const/4 v7, 0x3

    new-instance p3, Lkm3;

    .line 347
    .line 348
    const/4 v7, 0x3

    const/16 v0, 0xd

    .line 349
    .line 350
    const/4 v7, 0x4

    invoke-direct {p3, p2, v0}, Lkm3;-><init>(Ljava/lang/Object;I)V

    .line 351
    .line 352
    .line 353
    invoke-static {v2, p3, p1}, Lxt0;->d0(Lcom/google/common/util/concurrent/ListenableFuture;Lxl0;Ljava/util/concurrent/Executor;)Ld62;

    .line 354
    .line 355
    .line 356
    move-result-object p1

    .line 357
    const/4 v7, 0x3

    new-instance p2, Lpv;

    .line 358
    .line 359
    invoke-direct {p2, v3, p0, p1}, Lpv;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 360
    .line 361
    .line 362
    const/4 v7, 0x6

    invoke-static {p0}, Lw63;->getMainExecutor(Landroid/content/Context;)Ljava/util/concurrent/Executor;

    .line 363
    .line 364
    .line 365
    move-result-object p0

    .line 366
    const/4 v7, 0x3

    invoke-virtual {p1, p2, p0}, Lso6;->addListener(Ljava/lang/Runnable;Ljava/util/concurrent/Executor;)V

    .line 367
    .line 368
    .line 369
    goto :goto_1c4

    .line 370
    :catchall_1b4
    move-exception p0

    .line 371
    const/4 v7, 0x6

    monitor-exit v1

    .line 372
    const/4 v7, 0x6

    throw p0

    .line 373
    :cond_1b9
    const-string p1, "Missing required permissions for video recording"

    .line 374
    .line 375
    iget-wide p2, p0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    .line 376
    .line 377
    const/4 v7, 0x4

    invoke-static {p2, p3, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 378
    .line 379
    .line 380
    invoke-virtual {p0}, Landroid/app/Service;->stopSelf()V

    .line 381
    .line 382
    .line 383
    :cond_1c4
    :goto_1c4
    const/4 p0, 0x2

    .line 384
    return p0
.end method
