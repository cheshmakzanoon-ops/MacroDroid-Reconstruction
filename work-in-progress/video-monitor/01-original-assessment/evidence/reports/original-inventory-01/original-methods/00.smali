.method public final i1(Lo73;)Ljava/lang/Object;
    .locals 8

    .line 1
    const/4 v7, 0x6

    instance-of v0, p1, Lcom/arlosoft/macrodroid/a;

    .line 3
    const/4 v7, 0x6

    if-eqz v0, :cond_16

    .line 5
    move-object v0, p1

    .line 6
    const/4 v7, 0x3

    check-cast v0, Lcom/arlosoft/macrodroid/a;

    .line 8
    iget v1, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 10
    const/high16 v2, -0x80000000

    .line 12
    and-int v3, v1, v2

    .line 14
    if-eqz v3, :cond_16

    .line 16
    sub-int/2addr v1, v2

    .line 17
    iput v1, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 19
    goto :goto_1c

    .line 20
    :cond_16
    const/4 v7, 0x2

    new-instance v0, Lcom/arlosoft/macrodroid/a;

    .line 22
    invoke-direct {v0, p0, p1}, Lcom/arlosoft/macrodroid/a;-><init>(Lcom/arlosoft/macrodroid/DonateActivity;Lo73;)V

    .line 25
    :goto_1c
    iget-object p1, v0, Lcom/arlosoft/macrodroid/a;->result:Ljava/lang/Object;

    .line 27
    const/4 v7, 0x1

    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 29
    iget v2, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 31
    const/4 v3, 0x3

    .line 32
    const/4 v7, 0x5

    const/4 v4, 0x2

    .line 33
    const/4 v7, 0x5

    const/4 v5, 0x1

    .line 34
    if-eqz v2, :cond_46

    .line 36
    if-eq v2, v5, :cond_41

    .line 38
    if-eq v2, v4, :cond_3d

    .line 40
    if-ne v2, v3, :cond_36

    .line 42
    const/4 v7, 0x2

    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 45
    const/4 v7, 0x4

    goto :goto_b0

    .line 46
    :cond_36
    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 48
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 51
    const/4 p0, 0x0

    .line 52
    return-object p0

    .line 53
    :cond_3d
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 56
    goto :goto_8f

    .line 57
    :cond_41
    const/4 v7, 0x2

    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 60
    goto :goto_6e

    .line 61
    :cond_46
    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 64
    const/4 v7, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/DonateActivity;->h1()Lcom/arlosoft/macrodroid/upgrade/billing/e;

    .line 67
    move-result-object p1

    .line 68
    const/4 v7, 0x7

    const-string v2, "donation_low"

    .line 70
    const/4 v7, 0x1

    invoke-virtual {p1, v2}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->e(Ljava/lang/String;)Lb81;

    .line 73
    move-result-object p1

    .line 74
    const/4 v7, 0x3

    invoke-static {p1, v5}, Lguh;->Q(Ly76;I)Lv96;

    .line 77
    move-result-object p1

    .line 78
    const/4 v7, 0x0

    new-instance v2, Lqs4;

    .line 80
    const/4 v6, 0x5

    const/4 v6, 0x0

    .line 81
    const/4 v7, 0x0

    invoke-direct {v2, p0, v6}, Lqs4;-><init>(Lcom/arlosoft/macrodroid/DonateActivity;I)V

    .line 84
    const/4 v7, 0x3

    iput v5, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 86
    invoke-virtual {p1, v2, v0}, Lv96;->collect(Ld86;Lm73;)Ljava/lang/Object;

    .line 89
    move-result-object p1

    .line 90
    if-ne p1, v1, :cond_6e

    .line 92
    goto :goto_af

    .line 93
    :cond_6e
    :goto_6e
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/DonateActivity;->h1()Lcom/arlosoft/macrodroid/upgrade/billing/e;

    .line 96
    move-result-object p1

    .line 97
    const/4 v7, 0x4

    const-string v2, "donation_medium"

    .line 99
    invoke-virtual {p1, v2}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->e(Ljava/lang/String;)Lb81;

    .line 102
    move-result-object p1

    .line 103
    const/4 v7, 0x4

    invoke-static {p1, v5}, Lguh;->Q(Ly76;I)Lv96;

    .line 106
    move-result-object p1

    .line 107
    new-instance v2, Lqs4;

    .line 109
    const/4 v7, 0x0

    invoke-direct {v2, p0, v5}, Lqs4;-><init>(Lcom/arlosoft/macrodroid/DonateActivity;I)V

    .line 112
    const/4 v7, 0x3

    iput v4, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 114
    invoke-virtual {p1, v2, v0}, Lv96;->collect(Ld86;Lm73;)Ljava/lang/Object;

    .line 117
    move-result-object p1

    .line 118
    const/4 v7, 0x2

    if-ne p1, v1, :cond_8f

    .line 120
    goto :goto_af

    .line 121
    :cond_8f
    :goto_8f
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/DonateActivity;->h1()Lcom/arlosoft/macrodroid/upgrade/billing/e;

    .line 124
    move-result-object p1

    .line 125
    const-string v2, "donation_high"

    .line 127
    invoke-virtual {p1, v2}, Lcom/arlosoft/macrodroid/upgrade/billing/e;->e(Ljava/lang/String;)Lb81;

    .line 130
    move-result-object p1

    .line 131
    const/4 v7, 0x5

    invoke-static {p1, v5}, Lguh;->Q(Ly76;I)Lv96;

    .line 134
    move-result-object p1

    .line 135
    const/4 v7, 0x7

    new-instance v2, Lqs4;

    .line 137
    invoke-direct {v2, p0, v4}, Lqs4;-><init>(Lcom/arlosoft/macrodroid/DonateActivity;I)V

    .line 140
    const/4 v7, 0x6

    iput v3, v0, Lcom/arlosoft/macrodroid/a;->label:I

    .line 142
    const/4 v7, 0x6

    invoke-virtual {p1, v2, v0}, Lv96;->collect(Ld86;Lm73;)Ljava/lang/Object;

    .line 145
    move-result-object p0

    .line 146
    const/4 v7, 0x4

    if-ne p0, v1, :cond_b0

    .line 148
    :goto_af
    return-object v1

    .line 149
    :cond_b0
    :goto_b0
    sget-object p0, Lblg;->a:Lblg;

    .line 151
    const/4 v7, 0x5

    return-object p0
.end method
