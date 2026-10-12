.method public final k(Lo73;)Ljava/lang/Object;
    .locals 11

    .line 1
    const/4 v10, 0x7

    instance-of v0, p1, Lcom/arlosoft/macrodroid/upgrade/billing/c;

    .line 3
    const/4 v10, 0x1

    if-eqz v0, :cond_18

    .line 5
    move-object v0, p1

    .line 6
    const/4 v10, 0x1

    check-cast v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;

    .line 8
    iget v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->label:I

    .line 10
    const/high16 v2, -0x80000000

    .line 12
    and-int v3, v1, v2

    .line 14
    const/4 v10, 0x5

    if-eqz v3, :cond_18

    .line 16
    sub-int/2addr v1, v2

    .line 17
    const/4 v10, 0x1

    iput v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->label:I

    .line 19
    goto :goto_1d

    .line 20
    :cond_18
    new-instance v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;

    .line 22
    invoke-direct {v0, p0, p1}, Lcom/arlosoft/macrodroid/upgrade/billing/c;-><init>(Lcom/arlosoft/macrodroid/upgrade/billing/e;Lo73;)V

    .line 25
    :goto_1d
    const/4 v10, 0x4

    iget-object p1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->result:Ljava/lang/Object;

    .line 27
    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 29
    iget v2, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->label:I

    .line 31
    iget-object v3, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->f:Lcom/android/billingclient/api/BillingClient;

    .line 33
    const/4 v10, 0x5

    const/16 v4, 0xa

    .line 35
    const/4 v5, 0x2

    move v10, v5

    .line 36
    const/4 v6, 0x1

    .line 37
    const/4 v7, 0x0

    .line 38
    if-eqz v2, :cond_57

    .line 40
    if-eq v2, v6, :cond_4a

    .line 42
    const/4 v10, 0x0

    if-ne v2, v5, :cond_43

    .line 44
    const/4 v10, 0x5

    iget-object v1, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$1:Ljava/lang/Object;

    .line 46
    check-cast v1, Lcom/android/billingclient/api/QueryProductDetailsParams;

    .line 48
    iget-object v0, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$0:Ljava/lang/Object;

    .line 50
    check-cast v0, Ljava/util/List;

    .line 52
    const/4 v10, 0x2

    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 55
    goto/16 :goto_127

    .line 57
    :cond_43
    const/4 v10, 0x5

    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 59
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 62
    return-object v7

    .line 63
    :cond_4a
    iget-object v2, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$1:Ljava/lang/Object;

    .line 65
    check-cast v2, Lcom/android/billingclient/api/QueryProductDetailsParams;

    .line 67
    const/4 v10, 0x1

    iget-object v2, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$0:Ljava/lang/Object;

    .line 69
    check-cast v2, Ljava/util/List;

    .line 71
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 74
    goto :goto_b9

    .line 75
    :cond_57
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 78
    iget-object p1, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->b:Ljava/util/ArrayList;

    .line 80
    invoke-virtual {p1}, Ljava/util/ArrayList;->isEmpty()Z

    .line 83
    move-result v2

    .line 84
    if-eqz v2, :cond_63

    .line 86
    goto :goto_c9

    .line 87
    :cond_63
    const/4 v10, 0x3

    new-instance v2, Ljava/util/ArrayList;

    .line 89
    invoke-static {p1, v4}, Lyj2;->j0(Ljava/lang/Iterable;I)I

    .line 92
    move-result v8

    .line 93
    const/4 v10, 0x6

    invoke-direct {v2, v8}, Ljava/util/ArrayList;-><init>(I)V

    .line 96
    invoke-virtual {p1}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 99
    move-result-object p1

    .line 100
    :goto_72
    invoke-interface {p1}, Ljava/util/Iterator;->hasNext()Z

    .line 103
    move-result v8

    .line 104
    const/4 v10, 0x2

    if-eqz v8, :cond_9b

    .line 106
    invoke-interface {p1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 109
    move-result-object v8

    .line 110
    check-cast v8, Ljava/lang/String;

    .line 112
    invoke-static {}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product;->newBuilder()Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 115
    move-result-object v9

    .line 116
    const/4 v10, 0x4

    invoke-virtual {v9, v8}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->setProductId(Ljava/lang/String;)Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 119
    move-result-object v8

    .line 120
    const/4 v10, 0x3

    const-string v9, "auinp"

    const-string v9, "inapp"

    .line 122
    const/4 v10, 0x0

    invoke-virtual {v8, v9}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->setProductType(Ljava/lang/String;)Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 125
    move-result-object v8

    .line 126
    const/4 v10, 0x3

    invoke-virtual {v8}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->build()Lcom/android/billingclient/api/QueryProductDetailsParams$Product;

    .line 129
    move-result-object v8

    .line 130
    invoke-virtual {v2, v8}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 133
    goto :goto_72

    .line 134
    :cond_9b
    invoke-static {}, Lcom/android/billingclient/api/QueryProductDetailsParams;->newBuilder()Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;

    .line 137
    move-result-object p1

    .line 138
    invoke-virtual {p1, v2}, Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;->setProductList(Ljava/util/List;)Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;

    .line 141
    move-result-object p1

    .line 142
    invoke-virtual {p1}, Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;->build()Lcom/android/billingclient/api/QueryProductDetailsParams;

    .line 145
    move-result-object p1

    .line 146
    const/4 v10, 0x4

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 149
    iput-object v7, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$0:Ljava/lang/Object;

    .line 151
    iput-object v7, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$1:Ljava/lang/Object;

    .line 153
    iput v6, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->label:I

    .line 155
    invoke-static {v3, p1, v0}, Lcom/android/billingclient/api/BillingClientKotlinKt;->queryProductDetails(Lcom/android/billingclient/api/BillingClient;Lcom/android/billingclient/api/QueryProductDetailsParams;Lm73;)Ljava/lang/Object;

    .line 158
    move-result-object p1

    .line 159
    const/4 v10, 0x6

    if-ne p1, v1, :cond_b9

    .line 161
    goto :goto_126

    .line 162
    :cond_b9
    :goto_b9
    const/4 v10, 0x5

    check-cast p1, Lcom/android/billingclient/api/ProductDetailsResult;

    .line 164
    const/4 v10, 0x3

    invoke-virtual {p1}, Lcom/android/billingclient/api/ProductDetailsResult;->getBillingResult()Lcom/android/billingclient/api/BillingResult;

    .line 167
    move-result-object v2

    .line 168
    invoke-virtual {p1}, Lcom/android/billingclient/api/ProductDetailsResult;->getProductDetailsList()Ljava/util/List;

    .line 171
    move-result-object p1

    .line 172
    const/4 v10, 0x7

    invoke-virtual {p0, v2, p1}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->i(Lcom/android/billingclient/api/BillingResult;Ljava/util/List;)V

    .line 175
    :goto_c9
    const/4 v10, 0x1

    iget-object p1, p0, Lcom/arlosoft/macrodroid/upgrade/billing/e;->d:Ljava/util/List;

    .line 177
    invoke-interface {p1}, Ljava/util/Collection;->isEmpty()Z

    .line 180
    move-result v2

    .line 181
    if-eqz v2, :cond_d4

    .line 183
    const/4 v10, 0x4

    goto :goto_134

    .line 184
    :cond_d4
    new-instance v2, Ljava/util/ArrayList;

    .line 186
    invoke-static {p1, v4}, Lyj2;->j0(Ljava/lang/Iterable;I)I

    .line 189
    move-result v4

    .line 190
    const/4 v10, 0x7

    invoke-direct {v2, v4}, Ljava/util/ArrayList;-><init>(I)V

    .line 193
    invoke-interface {p1}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 196
    move-result-object p1

    .line 197
    :goto_e2
    invoke-interface {p1}, Ljava/util/Iterator;->hasNext()Z

    .line 200
    move-result v4

    .line 201
    if-eqz v4, :cond_109

    .line 203
    invoke-interface {p1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 206
    move-result-object v4

    .line 207
    check-cast v4, Ljava/lang/String;

    .line 209
    const/4 v10, 0x4

    invoke-static {}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product;->newBuilder()Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 212
    move-result-object v6

    .line 213
    invoke-virtual {v6, v4}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->setProductId(Ljava/lang/String;)Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 216
    move-result-object v4

    .line 217
    const/4 v10, 0x6

    const-string/jumbo v6, "subs"

    .line 219
    invoke-virtual {v4, v6}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->setProductType(Ljava/lang/String;)Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;

    .line 222
    move-result-object v4

    .line 223
    const/4 v10, 0x2

    invoke-virtual {v4}, Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;->build()Lcom/android/billingclient/api/QueryProductDetailsParams$Product;

    .line 226
    move-result-object v4

    .line 227
    const/4 v10, 0x0

    invoke-virtual {v2, v4}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 230
    goto :goto_e2

    .line 231
    :cond_109
    invoke-static {}, Lcom/android/billingclient/api/QueryProductDetailsParams;->newBuilder()Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;

    .line 234
    move-result-object p1

    .line 235
    invoke-virtual {p1, v2}, Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;->setProductList(Ljava/util/List;)Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;

    .line 238
    move-result-object p1

    .line 239
    invoke-virtual {p1}, Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;->build()Lcom/android/billingclient/api/QueryProductDetailsParams;

    .line 242
    move-result-object p1

    .line 243
    const/4 v10, 0x2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 246
    iput-object v7, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$0:Ljava/lang/Object;

    .line 248
    const/4 v10, 0x0

    iput-object v7, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->L$1:Ljava/lang/Object;

    .line 250
    iput v5, v0, Lcom/arlosoft/macrodroid/upgrade/billing/c;->label:I

    .line 252
    invoke-static {v3, p1, v0}, Lcom/android/billingclient/api/BillingClientKotlinKt;->queryProductDetails(Lcom/android/billingclient/api/BillingClient;Lcom/android/billingclient/api/QueryProductDetailsParams;Lm73;)Ljava/lang/Object;

    .line 255
    move-result-object p1

    .line 256
    if-ne p1, v1, :cond_127

    .line 258
    :goto_126
    return-object v1

    .line 259
    :cond_127
    :goto_127
    check-cast p1, Lcom/android/billingclient/api/ProductDetailsResult;

    .line 261
    invoke-virtual {p1}, Lcom/android/billingclient/api/ProductDetailsResult;->getBillingResult()Lcom/android/billingclient/api/BillingResult;

    .line 264
    move-result-object v0

    .line 265
    invoke-virtual {p1}, Lcom/android/billingclient/api/ProductDetailsResult;->getProductDetailsList()Ljava/util/List;

    .line 268
    move-result-object p1

    .line 269
    invoke-virtual {p0, v0, p1}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->i(Lcom/android/billingclient/api/BillingResult;Ljava/util/List;)V

    .line 272
    :goto_134
    const/4 v10, 0x4

    sget-object p0, Lblg;->a:Lblg;

    .line 274
    return-object p0
.end method
