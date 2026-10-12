.class public final Lrecovered/ui/WidgetUpdateMethods;
.super Ljava/lang/Object;


# direct methods
.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static update(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;
    .locals 18

    move-object/from16 v0, p0

    move-object/from16 v1, p3

    instance-of v2, v1, Lcom/arlosoft/macrodroid/widget/custom/b;

    if-eqz v2, :cond_1d

    move-object v2, v1

    check-cast v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    iget v3, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    const/high16 v4, -0x80000000

    and-int v5, v3, v4

    if-eqz v5, :cond_17

    sub-int/2addr v3, v4

    iput v3, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    goto :goto_22

    :cond_17
    new-instance v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    invoke-direct {v2, v0, v1}, Lcom/arlosoft/macrodroid/widget/custom/b;-><init>(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Lo73;)V

    goto :goto_22

    :cond_1d
    new-instance v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    invoke-direct {v2, v0, v1}, Lcom/arlosoft/macrodroid/widget/custom/b;-><init>(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Lo73;)V

    :goto_22
    iget-object v1, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->result:Ljava/lang/Object;

    sget-object v3, Lv93;->COROUTINE_SUSPENDED:Lv93;

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    const/4 v5, 0x1

    const/4 v6, 0x2

    const-string v7, ": "

    const-string v8, "Failed to update custom widget instance "

    const/4 v10, 0x0

    if-ne v4, v6, :cond_7f

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iget v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    check-cast v0, Lgy6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    move-object v12, v0

    check-cast v12, Ljava/util/Iterator;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    check-cast v0, Ljava/lang/Iterable;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    move-object v13, v0

    check-cast v13, Lhn9;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    move-object v14, v0

    check-cast v14, Lwx6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    check-cast v0, Ljava/util/List;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    move-object v15, v0

    check-cast v15, Landroid/content/Context;

    :try_start_55
    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_58
    .catch Ljava/lang/Exception; {:try_start_55 .. :try_end_58} :catch_59

    goto :goto_76

    :catch_59
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    :goto_76
    move-object/from16 v16, v10

    move-object v5, v14

    const/4 v1, 0x0

    move-object v14, v12

    move v12, v11

    const/4 v11, 0x0

    goto/16 :goto_103

    :cond_7f
    if-ne v4, v5, :cond_d9

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I

    iget v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iget v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    move-object v13, v0

    check-cast v13, Lgy6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    move-object v14, v0

    check-cast v14, Ljava/util/Iterator;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    check-cast v0, Ljava/lang/Iterable;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    move-object v15, v0

    check-cast v15, Lhn9;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    move-object/from16 v16, v0

    check-cast v16, Lwx6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    check-cast v0, Ljava/util/List;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    move-object/from16 v17, v0

    check-cast v17, Landroid/content/Context;

    :try_start_aa
    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_ad
    .catch Ljava/lang/Exception; {:try_start_aa .. :try_end_ad} :catch_af

    move v0, v5

    goto :goto_cd

    :catch_af
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v11}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    const/4 v0, 0x0

    :goto_cd
    move v1, v11

    move v11, v4

    move v4, v1

    move v1, v0

    move-object/from16 v5, v16

    move-object/from16 v16, v13

    move-object v13, v15

    move-object/from16 v15, v17

    goto :goto_103

    :cond_d9
    if-nez v4, :cond_1c7

    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V

    invoke-interface/range {p2 .. p2}, Ljava/util/List;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_e7

    sget-object v0, Lblg;->a:Lblg;

    return-object v0

    :cond_e7
    invoke-virtual/range {p0 .. p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    new-instance v14, Lwx6;

    move-object/from16 v0, p1

    invoke-direct {v14, v0}, Lwx6;-><init>(Landroid/content/Context;)V

    new-instance v13, Lhn9;

    invoke-direct {v13}, Lhn9;-><init>()V

    invoke-interface/range {p2 .. p2}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    move-result-object v12

    move-object v15, v0

    move-object/from16 v16, v10

    move-object v5, v14

    const/4 v1, 0x0

    const/4 v4, 0x0

    const/4 v11, 0x0

    move-object v14, v12

    const/4 v12, 0x0

    :goto_103
    if-nez v1, :cond_17e

    invoke-interface {v14}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-nez v0, :cond_10e

    sget-object v0, Lblg;->a:Lblg;

    return-object v0

    :cond_10e
    invoke-interface {v14}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/Number;

    invoke-virtual {v0}, Ljava/lang/Number;->intValue()I

    move-result v4

    :try_start_118
    iget-object v0, v5, Lwx6;->b:Landroid/appwidget/AppWidgetManager;

    invoke-virtual {v0, v4}, Landroid/appwidget/AppWidgetManager;->getAppWidgetInfo(I)Landroid/appwidget/AppWidgetProviderInfo;

    move-result-object v0

    if-eqz v0, :cond_154

    new-instance v9, Lmh0;

    invoke-direct {v9, v4}, Lmh0;-><init>(I)V
    :try_end_125
    .catch Ljava/lang/Exception; {:try_start_118 .. :try_end_125} :catch_15f

    :try_start_125
    new-instance v0, Lzhh;

    invoke-direct {v0, v6, v10}, Lzhh;-><init>(ILm73;)V

    iput-object v15, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    iput-object v5, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    iput-object v13, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    iput-object v14, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    iput-object v9, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    iput v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iput v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    const/4 v6, 0x0

    iput v6, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I
    :try_end_141
    .catch Ljava/lang/Exception; {:try_start_125 .. :try_end_141} :catch_14f

    const/4 v6, 0x1

    :try_start_142
    iput v6, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    invoke-static {v15, v9, v0, v2}, Lrjb;->M(Landroid/content/Context;Lgy6;Ljn6;Lo73;)Ljava/lang/Object;

    move-result-object v0
    :try_end_148
    .catch Ljava/lang/Exception; {:try_start_142 .. :try_end_148} :catch_14d

    if-ne v0, v3, :cond_14b

    goto :goto_1a0

    :cond_14b
    const/4 v11, 0x0

    goto :goto_181

    :catch_14d
    move-exception v0

    goto :goto_151

    :catch_14f
    move-exception v0

    const/4 v6, 0x1

    :goto_151
    move-object/from16 v16, v9

    goto :goto_161

    :cond_154
    const/4 v6, 0x1

    :try_start_155
    new-instance v0, Ljava/lang/IllegalArgumentException;

    const-string v9, "Invalid AppWidget ID."

    invoke-direct {v0, v9}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_15d
    .catch Ljava/lang/Exception; {:try_start_155 .. :try_end_15d} :catch_15d

    :catch_15d
    move-exception v0

    goto :goto_161

    :catch_15f
    move-exception v0

    const/4 v6, 0x1

    :goto_161
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v9, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v9

    invoke-virtual {v9, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v9

    invoke-virtual {v9, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    goto :goto_1c4

    :cond_17e
    const/4 v6, 0x1

    move-object/from16 v9, v16

    :goto_181
    :try_start_181
    iput-object v15, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    iput-object v5, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    iput-object v13, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    iput-object v14, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    iput v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iput v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iput v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I
    :try_end_197
    .catch Ljava/lang/Exception; {:try_start_181 .. :try_end_197} :catch_1a3

    const/4 v1, 0x2

    :try_start_198
    iput v1, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    invoke-virtual {v13, v15, v9, v2}, Lrx6;->d(Landroid/content/Context;Lgy6;Lo73;)Ljava/lang/Object;

    move-result-object v0
    :try_end_19e
    .catch Ljava/lang/Exception; {:try_start_198 .. :try_end_19e} :catch_1a1

    if-ne v0, v3, :cond_1c1

    :goto_1a0
    return-object v3

    :catch_1a1
    move-exception v0

    goto :goto_1a5

    :catch_1a3
    move-exception v0

    const/4 v1, 0x2

    :goto_1a5
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    :cond_1c1
    move-object/from16 v16, v9

    const/4 v1, 0x0

    :goto_1c4
    const/4 v6, 0x2

    goto/16 :goto_103

    :cond_1c7
    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    return-object v10
.end method
