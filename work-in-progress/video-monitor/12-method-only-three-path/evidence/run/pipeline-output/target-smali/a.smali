.class public final Lcom/arlosoft/macrodroid/action/services/a;
.super Lrff;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Ljn6;


# instance fields
.field L$0:Ljava/lang/Object;

.field L$1:Ljava/lang/Object;

.field label:I

.field final synthetic this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;


# direct methods
.method public constructor <init>(Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;Lm73;)V
    .locals 1

    .line 1
    iput-object p1, p0, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 2
    .line 3
    const/4 p1, 0x2

    .line 4
    invoke-direct {p0, p1, p2}, Lrff;-><init>(ILm73;)V

    .line 5
    .line 6
    .line 7
    const/4 v0, 0x3

    return-void
.end method


# virtual methods
.method public final create(Ljava/lang/Object;Lm73;)Lm73;
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    new-instance p1, Lcom/arlosoft/macrodroid/action/services/a;

    .line 2
    .line 3
    const/4 v0, 0x5

    iget-object p0, p0, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    .line 4
    .line 5
    invoke-direct {p1, p0, p2}, Lcom/arlosoft/macrodroid/action/services/a;-><init>(Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;Lm73;)V

    .line 6
    .line 7
    .line 8
    return-object p1
.end method

.method public final invoke(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    .locals 1

    .line 1
    const/4 v0, 0x1

    check-cast p1, Lu93;

    .line 2
    .line 3
    check-cast p2, Lm73;

    .line 4
    .line 5
    invoke-virtual {p0, p1, p2}, Lcom/arlosoft/macrodroid/action/services/a;->create(Ljava/lang/Object;Lm73;)Lm73;

    .line 6
    .line 7
    .line 8
    move-result-object p0

    .line 9
    check-cast p0, Lcom/arlosoft/macrodroid/action/services/a;

    .line 10
    .line 11
    sget-object p1, Lblg;->a:Lblg;

    .line 12
    .line 13
    const/4 v0, 0x1

    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;

    .line 14
    .line 15
    .line 16
    move-result-object p0

    .line 17
    const/4 v0, 0x0

    return-object p0
.end method

.method public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;
    .locals 26

    move-object/from16 v1, p0

    sget-object v2, Lblg;->a:Lblg;

    const-string v3, "KB"

    sget-object v4, Lv93;->COROUTINE_SUSPENDED:Lv93;

    iget v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    const-string v5, "Error in storage monitoring: "

    const/4 v6, 0x2

    const-wide/16 v7, 0xbb8

    const/4 v9, 0x3

    const/4 v10, 0x1

    const/4 v11, 0x0

    if-nez v0, :cond_23

    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    iput v10, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    const-wide/16 v12, 0x1388

    invoke-static {v12, v13, v1}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    move-result-object v0

    if-ne v0, v4, :cond_58

    goto/16 :goto_22a

    :cond_23
    if-ne v0, v10, :cond_29

    :goto_25
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V

    goto :goto_58

    :cond_29
    if-ne v0, v6, :cond_55

    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    check-cast v0, Ljava/io/File;

    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    check-cast v0, Lqnc;

    :try_start_33
    invoke-static/range {p1 .. p1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_36
    .catch Ljava/lang/Exception; {:try_start_33 .. :try_end_36} :catch_37

    return-object v2

    :catch_37
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v5, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iget-object v12, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v12, v12, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v12, v13, v0}, Lkjf;->g(JLjava/lang/String;)V

    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    iput v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    invoke-static {v7, v8, v1}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    move-result-object v0

    if-ne v0, v4, :cond_58

    goto/16 :goto_22a

    :cond_55
    if-ne v0, v9, :cond_234

    goto :goto_25

    :cond_58
    :goto_58
    sget-object v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->A:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService$a;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    sget-boolean v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->B:Z

    if-nez v0, :cond_63

    goto/16 :goto_202

    :cond_63
    :try_start_63
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-object v0, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    if-eqz v0, :cond_6d

    invoke-virtual {v0}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v0

    :cond_6d
    if-nez v0, :cond_77

    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    sget-object v12, Landroid/os/Environment;->DIRECTORY_MOVIES:Ljava/lang/String;

    invoke-virtual {v0, v12}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    move-result-object v0

    :cond_77
    const/4 v12, 0x0

    if-eqz v0, :cond_ee

    iget-object v15, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    const-wide/16 v16, 0x0

    invoke-virtual {v15, v0}, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->c(Ljava/io/File;)J

    move-result-wide v13
    :try_end_82
    .catch Ljava/lang/Exception; {:try_start_63 .. :try_end_82} :catch_207

    move-wide/from16 v18, v7

    :try_start_84
    iget-wide v7, v15, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->x:J

    cmp-long v0, v7, v16

    const-wide/32 v20, 0x100000

    if-lez v0, :cond_9a

    const-wide/32 v22, 0x6400000

    sub-long v7, v7, v22

    cmp-long v0, v13, v7

    if-gez v0, :cond_97

    goto :goto_9a

    :cond_97
    move/from16 v22, v10

    goto :goto_be

    :cond_9a
    :goto_9a
    iput-wide v13, v15, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->x:J

    div-long v7, v13, v20

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    :try_end_a3
    .catch Ljava/lang/Exception; {:try_start_84 .. :try_end_a3} :catch_eb

    move/from16 v22, v10

    :try_start_a5
    const-string v10, "Recording Video - Available storage: "

    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v7, v8}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v7, "MB"

    invoke-virtual {v0, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-wide v7, v15, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v7, v8, v0}, Lkjf;->q(JLjava/lang/String;)V

    :goto_be
    const-wide/32 v7, 0x8000000

    cmp-long v0, v13, v7

    if-gez v0, :cond_f4

    div-long v13, v13, v20

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "CRITICAL: Storage space exhausted ("

    invoke-virtual {v0, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v13, v14}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v7, "MB remaining). Stopping recording."

    invoke-virtual {v0, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-wide v7, v15, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v7, v8, v0}, Lkjf;->g(JLjava/lang/String;)V
    :try_end_e5
    .catch Ljava/lang/Exception; {:try_start_a5 .. :try_end_e5} :catch_e8

    move/from16 v7, v22

    goto :goto_f5

    :catch_e8
    move-exception v0

    goto/16 :goto_20c

    :catch_eb
    move-exception v0

    goto/16 :goto_20a

    :cond_ee
    move-wide/from16 v18, v7

    move/from16 v22, v10

    const-wide/16 v16, 0x0

    :cond_f4
    move v7, v12

    :goto_f5
    if-nez v7, :cond_1e3

    :try_start_f7
    iget-object v8, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
    :try_end_fc
    .catch Ljava/lang/Exception; {:try_start_f7 .. :try_end_fc} :catch_1e0

    :try_start_fc
    iget-object v0, v8, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    if-eqz v0, :cond_113

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v0

    if-eqz v0, :cond_12a

    iget-object v0, v8, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->t:Ljava/io/File;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    invoke-virtual {v0}, Ljava/io/File;->length()J

    move-result-wide v13

    goto :goto_12c

    :cond_113
    iget-object v0, v8, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->u:Landroid/os/ParcelFileDescriptor;
    :try_end_115
    .catch Ljava/lang/Exception; {:try_start_fc .. :try_end_115} :catch_11a

    if-eqz v0, :cond_12a

    const-wide/16 v13, -0x1

    goto :goto_12c

    :catch_11a
    move-exception v0

    :try_start_11b
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    const-string v10, "Failed to get current video file size: "

    invoke-static {v10, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iget-wide v13, v8, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v13, v14, v0}, Lkjf;->g(JLjava/lang/String;)V

    :cond_12a
    move-wide/from16 v13, v16

    :goto_12c
    cmp-long v0, v13, v16

    if-ltz v0, :cond_1e3

    const-wide/16 v20, 0x400

    move/from16 p1, v7

    div-long v6, v13, v20

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v10, "Current file size: "

    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v6, v7, v0}, Lkjf;->q(JLjava/lang/String;)V

    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->v:J

    cmp-long v10, v6, v16

    if-lez v10, :cond_1d9

    sub-long v6, v13, v6

    cmp-long v10, v6, v16

    if-gtz v10, :cond_1b7

    iget v6, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    add-int/lit8 v6, v6, 0x1

    iput v6, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "File size not growing: check "

    invoke-virtual {v0, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v6, "/3"

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v6, v7, v0}, Lkjf;->q(JLjava/lang/String;)V

    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget v0, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    if-lt v0, v9, :cond_1d9

    int-to-long v6, v0

    mul-long v6, v6, v18

    const-wide/16 v15, 0x3e8

    div-long/2addr v6, v15

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v10, "CRITICAL: Video file stopped growing for "

    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v6, " seconds. Storage may be full. Stopping recording."

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v6, v7, v0}, Lkjf;->g(JLjava/lang/String;)V

    move/from16 v7, v22

    goto :goto_1db

    :cond_1b7
    iput v12, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->w:I

    div-long v6, v6, v20

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v10, "File growing normally: +"

    invoke-virtual {v0, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v6, v7, v0}, Lkjf;->q(JLjava/lang/String;)V

    :cond_1d9
    move/from16 v7, p1

    :goto_1db
    iget-object v0, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iput-wide v13, v0, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->v:J

    goto :goto_1e7

    :catch_1e0
    move-exception v0

    const/4 v8, 0x2

    goto :goto_20d

    :cond_1e3
    move/from16 p1, v7

    move/from16 v7, p1

    :goto_1e7
    if-eqz v7, :cond_205

    sget-object v0, Lzp4;->a:Lad4;

    sget-object v0, Lat9;->a:Lm47;

    new-instance v6, Ld31;

    iget-object v7, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    invoke-direct {v6, v7, v11}, Ld31;-><init>(Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;Lm73;)V

    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;
    :try_end_1f8
    .catch Ljava/lang/Exception; {:try_start_11b .. :try_end_1f8} :catch_1e0

    const/4 v8, 0x2

    :try_start_1f9
    iput v8, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    invoke-static {v0, v6, v1}, Ldt9;->e0(Li93;Ljn6;Lm73;)Ljava/lang/Object;

    move-result-object v0
    :try_end_1ff
    .catch Ljava/lang/Exception; {:try_start_1f9 .. :try_end_1ff} :catch_203

    if-ne v0, v4, :cond_202

    goto :goto_22a

    :cond_202
    :goto_202
    return-object v2

    :catch_203
    move-exception v0

    goto :goto_20d

    :cond_205
    const/4 v8, 0x2

    goto :goto_21c

    :catch_207
    move-exception v0

    move-wide/from16 v18, v7

    :goto_20a
    move/from16 v22, v10

    :goto_20c
    move v8, v6

    :goto_20d
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v5, v0}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iget-object v6, v1, Lcom/arlosoft/macrodroid/action/services/a;->this$0:Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;

    iget-wide v6, v6, Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;->s:J

    invoke-static {v6, v7, v0}, Lkjf;->g(JLjava/lang/String;)V

    :goto_21c
    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$0:Ljava/lang/Object;

    iput-object v11, v1, Lcom/arlosoft/macrodroid/action/services/a;->L$1:Ljava/lang/Object;

    iput v9, v1, Lcom/arlosoft/macrodroid/action/services/a;->label:I

    move-wide/from16 v6, v18

    invoke-static {v6, v7, v1}, Lsz6;->s(JLm73;)Ljava/lang/Object;

    move-result-object v0

    if-ne v0, v4, :cond_22b

    :goto_22a
    return-object v4

    :cond_22b
    move-wide/from16 v24, v6

    move v6, v8

    move-wide/from16 v7, v24

    move/from16 v10, v22

    goto/16 :goto_58

    :cond_234
    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    return-object v11
.end method
