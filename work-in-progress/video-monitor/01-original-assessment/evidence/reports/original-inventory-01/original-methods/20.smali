.method public final l(Lo73;)Ljava/lang/Object;
    .locals 13

    .line 1
    instance-of v0, p1, Lcom/arlosoft/macrodroid/upgrade/billing/d;

    .line 3
    if-eqz v0, :cond_16

    .line 5
    move-object v0, p1

    .line 6
    check-cast v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;

    .line 8
    iget v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->label:I

    .line 10
    const/high16 v2, -0x80000000

    .line 12
    and-int v3, v1, v2

    .line 14
    const/4 v12, 0x5

    if-eqz v3, :cond_16

    .line 16
    const/4 v12, 0x6

    sub-int/2addr v1, v2

    .line 17
    iput v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->label:I

    .line 19
    const/4 v12, 0x7

    goto :goto_1b

    .line 20
    :cond_16
    new-instance v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;

    .line 22
    invoke-direct {v0, p0, p1}, Lcom/arlosoft/macrodroid/upgrade/billing/d;-><init>(Lcom/arlosoft/macrodroid/upgrade/billing/e;Lo73;)V

    .line 25
    :goto_1b
    iget-object p1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->result:Ljava/lang/Object;

    .line 27
    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 29
    iget v2, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->label:I

    .line 31
    const/4 v12, 0x5

    const/16 v3, 0xd

    .line 33
    const/4 v4, 0x0

    .line 34
    const/4 v12, 0x3

    sget-object v5, Lcom/arlosoft/macrodroid/upgrade/billing/e;->p:Ljava/lang/String;

    .line 36
    iget-object v6, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->f:Lcom/android/billingclient/api/BillingClient;

    .line 38
    const/4 v7, 0x2

    .line 39
    const/4 v12, 0x1

    const/4 v8, 0x0

    .line 40
    const/4 v12, 0x6

    const/4 v9, 0x1

    .line 41
    const/4 v12, 0x7

    if-eqz v2, :cond_5a

    .line 43
    if-eq v2, v9, :cond_52

    .line 45
    if-ne v2, v7, :cond_49

    .line 47
    iget-object v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$2:Ljava/lang/Object;

    .line 49
    check-cast v1, Lcom/android/billingclient/api/QueryPurchasesParams;

    .line 51
    const/4 v12, 0x1

    iget-object v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$1:Ljava/lang/Object;

    .line 53
    check-cast v1, Ldib;

    .line 55
    iget-object v0, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$0:Ljava/lang/Object;

    .line 57
    const/4 v12, 0x2

    check-cast v0, Lcom/android/billingclient/api/QueryPurchasesParams;

    .line 59
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 62
    goto/16 :goto_125

    .line 64
    :cond_49
    const-string p0, "fwe/oeep n  /vm/re iu/oeeaicukl hnobtitt//s/rol/ ro"

    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 66
    const/4 v12, 0x0

    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 69
    return-object v4

    .line 70
    :cond_52
    iget-object v2, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$0:Ljava/lang/Object;

    .line 72
    check-cast v2, Lcom/android/billingclient/api/QueryPurchasesParams;

    .line 74
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 77
    goto :goto_9f

    .line 78
    :cond_5a
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 81
    invoke-static {}, Lcom/android/billingclient/api/QueryPurchasesParams;->newBuilder()Lcom/android/billingclient/api/QueryPurchasesParams$Builder;

    .line 84
    move-result-object p1

    .line 85
    const/4 v12, 0x0

    const-string v2, "inapp"

    .line 87
    const/4 v12, 0x6

    invoke-virtual {p1, v2}, Lcom/android/billingclient/api/QueryPurchasesParams$Builder;->setProductType(Ljava/lang/String;)Lcom/android/billingclient/api/QueryPurchasesParams$Builder;

    .line 90
    move-result-object p1

    .line 91
    const/4 v12, 0x6

    invoke-virtual {p1}, Lcom/android/billingclient/api/QueryPurchasesParams$Builder;->build()Lcom/android/billingclient/api/QueryPurchasesParams;

    .line 94
    move-result-object p1

    .line 95
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 98
    const/4 v12, 0x3

    iput-object p1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$0:Ljava/lang/Object;

    .line 100
    iput v8, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->I$0:I

    .line 102
    const/4 v12, 0x3

    iput v9, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->label:I

    .line 104
    const/4 v12, 0x5

    new-instance v2, Lp12;

    .line 106
    const/4 v12, 0x4

    invoke-static {v0}, La9f;->a0(Lm73;)Lm73;

    .line 109
    move-result-object v10

    .line 110
    const/4 v12, 0x2

    invoke-direct {v2, v9, v10}, Lp12;-><init>(ILm73;)V

    .line 113
    invoke-virtual {v2}, Lp12;->t()V

    .line 116
    new-instance v10, Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 118
    const/4 v12, 0x6

    invoke-direct {v10, v8}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    .line 121
    new-instance v11, Lzh4;

    .line 123
    invoke-direct {v11, v3, v10, v2}, Lzh4;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 126
    invoke-virtual {v6, p1, v11}, Lcom/android/billingclient/api/BillingClient;->queryPurchasesAsync(Lcom/android/billingclient/api/QueryPurchasesParams;Lcom/android/billingclient/api/PurchasesResponseListener;)V

    .line 129
    invoke-virtual {v2}, Lp12;->r()Ljava/lang/Object;

    .line 132
    move-result-object p1

    .line 133
    if-ne p1, v1, :cond_9f

    .line 135
    const/4 v12, 0x3

    goto/16 :goto_123

    .line 136
    :cond_9f
    :goto_9f
    const/4 v12, 0x4

    check-cast p1, Ldib;

    .line 138
    invoke-virtual {p1}, Ldib;->d()Ljava/lang/Object;

    .line 141
    move-result-object v2

    .line 142
    const/4 v12, 0x7

    check-cast v2, Lcom/android/billingclient/api/BillingResult;

    .line 144
    invoke-virtual {v2}, Lcom/android/billingclient/api/BillingResult;->getResponseCode()I

    .line 147
    move-result v2

    .line 148
    if-eqz v2, :cond_d2

    .line 150
    invoke-virtual {p1}, Ldib;->d()Ljava/lang/Object;

    .line 153
    move-result-object p1

    .line 154
    check-cast p1, Lcom/android/billingclient/api/BillingResult;

    .line 156
    invoke-virtual {p1}, Lcom/android/billingclient/api/BillingResult;->getDebugMessage()Ljava/lang/String;

    .line 159
    move-result-object p1

    .line 160
    new-instance v2, Ljava/lang/StringBuilder;

    .line 162
    const/4 v12, 0x4

    const-string v10, "Problem getting purchases: "

    .line 164
    invoke-direct {v2, v10}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 167
    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 170
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 173
    move-result-object p1

    .line 174
    const/4 v12, 0x1

    invoke-static {v5, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 177
    move-result p1

    .line 178
    invoke-static {p1}, Lcp6;->f(I)V

    .line 181
    const/4 v12, 0x2

    goto :goto_df

    .line 182
    :cond_d2
    const/4 v12, 0x3

    invoke-virtual {p1}, Ldib;->e()Ljava/lang/Object;

    .line 185
    move-result-object p1

    .line 186
    const/4 v12, 0x6

    check-cast p1, Ljava/util/List;

    .line 188
    iget-object v2, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->b:Ljava/util/ArrayList;

    .line 190
    invoke-virtual {p0, p1, v2}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->j(Ljava/util/List;Ljava/util/List;)V

    .line 193
    :goto_df
    invoke-static {}, Lcom/android/billingclient/api/QueryPurchasesParams;->newBuilder()Lcom/android/billingclient/api/QueryPurchasesParams$Builder;

    .line 196
    move-result-object p1

    .line 197
    const-string/jumbo v2, "subs"

    .line 199
    const/4 v12, 0x6

    invoke-virtual {p1, v2}, Lcom/android/billingclient/api/QueryPurchasesParams$Builder;->setProductType(Ljava/lang/String;)Lcom/android/billingclient/api/QueryPurchasesParams$Builder;

    .line 202
    move-result-object p1

    .line 203
    invoke-virtual {p1}, Lcom/android/billingclient/api/QueryPurchasesParams$Builder;->build()Lcom/android/billingclient/api/QueryPurchasesParams;

    .line 206
    move-result-object p1

    .line 207
    const/4 v12, 0x0

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 210
    iput-object v4, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$0:Ljava/lang/Object;

    .line 212
    iput-object v4, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$1:Ljava/lang/Object;

    .line 214
    const/4 v12, 0x3

    iput-object p1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->L$2:Ljava/lang/Object;

    .line 216
    iput v8, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->I$0:I

    .line 218
    iput v7, v0, Lcom/arlosoft/macrodroid/upgrade/billing/d;->label:I

    .line 220
    const/4 v12, 0x6

    new-instance v2, Lp12;

    .line 222
    const/4 v12, 0x4

    invoke-static {v0}, La9f;->a0(Lm73;)Lm73;

    .line 225
    move-result-object v0

    .line 226
    const/4 v12, 0x6

    invoke-direct {v2, v9, v0}, Lp12;-><init>(ILm73;)V

    .line 229
    invoke-virtual {v2}, Lp12;->t()V

    .line 232
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 234
    const/4 v12, 0x4

    invoke-direct {v0, v8}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    .line 237
    new-instance v4, Llq7;

    .line 239
    invoke-direct {v4, v3, v0, v2}, Llq7;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 242
    invoke-virtual {v6, p1, v4}, Lcom/android/billingclient/api/BillingClient;->queryPurchasesAsync(Lcom/android/billingclient/api/QueryPurchasesParams;Lcom/android/billingclient/api/PurchasesResponseListener;)V

    .line 245
    const/4 v12, 0x1

    invoke-virtual {v2}, Lp12;->r()Ljava/lang/Object;

    .line 248
    move-result-object p1

    .line 249
    const/4 v12, 0x4

    if-ne p1, v1, :cond_125

    .line 251
    :goto_123
    const/4 v12, 0x2

    return-object v1

    .line 252
    :cond_125
    :goto_125
    check-cast p1, Ldib;

    .line 254
    invoke-virtual {p1}, Ldib;->d()Ljava/lang/Object;

    .line 257
    move-result-object v0

    .line 258
    check-cast v0, Lcom/android/billingclient/api/BillingResult;

    .line 260
    invoke-virtual {v0}, Lcom/android/billingclient/api/BillingResult;->getResponseCode()I

    .line 263
    move-result v0

    .line 264
    const/4 v12, 0x7

    if-eqz v0, :cond_15b

    .line 266
    invoke-virtual {p1}, Ldib;->d()Ljava/lang/Object;

    .line 269
    move-result-object p0

    .line 270
    check-cast p0, Lcom/android/billingclient/api/BillingResult;

    .line 272
    const/4 v12, 0x2

    invoke-virtual {p0}, Lcom/android/billingclient/api/BillingResult;->getDebugMessage()Ljava/lang/String;

    .line 275
    move-result-object p0

    .line 276
    const/4 v12, 0x7

    new-instance p1, Ljava/lang/StringBuilder;

    .line 278
    const-string v0, "glsbitc q:buoopgneis tmrisne Pr"

    const-string v0, "Problem getting subscriptions: "

    .line 280
    const/4 v12, 0x3

    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 283
    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 286
    const/4 v12, 0x7

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 289
    move-result-object p0

    .line 290
    invoke-static {v5, p0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 293
    move-result p0

    .line 294
    const/4 v12, 0x2

    invoke-static {p0}, Lcp6;->f(I)V

    .line 297
    goto :goto_169

    .line 298
    :cond_15b
    const/4 v12, 0x7

    invoke-virtual {p1}, Ldib;->e()Ljava/lang/Object;

    .line 301
    move-result-object p1

    .line 302
    const/4 v12, 0x1

    check-cast p1, Ljava/util/List;

    .line 304
    iget-object v0, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->d:Ljava/util/List;

    .line 306
    const/4 v12, 0x2

    invoke-virtual {p0, p1, v0}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->j(Ljava/util/List;Ljava/util/List;)V

    .line 309
    :goto_169
    sget-object p0, Lblg;->a:Lblg;

    .line 311
    const/4 v12, 0x2

    return-object p0
.end method
