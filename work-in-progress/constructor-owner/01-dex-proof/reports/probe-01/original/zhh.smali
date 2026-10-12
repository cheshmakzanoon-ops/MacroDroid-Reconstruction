.class public final Lzhh;
.super Lrff;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Ljn6;


# instance fields
.field synthetic L$0:Ljava/lang/Object;

.field label:I


# virtual methods
.method public final create(Ljava/lang/Object;Lm73;)Lm73;
    .locals 2

    .line 1
    const-string v1, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    new-instance p0, Lzhh;

    .line 2
    .line 3
    const/4 v0, 0x2

    .line 4
    invoke-direct {p0, v0, p2}, Lrff;-><init>(ILm73;)V

    .line 5
    .line 6
    .line 7
    const/4 v1, 0x1

    iput-object p1, p0, Lzhh;->L$0:Ljava/lang/Object;

    .line 8
    .line 9
    return-object p0
.end method

.method public final invoke(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    .locals 1

    .line 1
    check-cast p1, Ltha;

    .line 2
    .line 3
    check-cast p2, Lm73;

    .line 4
    .line 5
    invoke-virtual {p0, p1, p2}, Lzhh;->create(Ljava/lang/Object;Lm73;)Lm73;

    .line 6
    .line 7
    .line 8
    move-result-object p0

    .line 9
    const/4 v0, 0x4

    check-cast p0, Lzhh;

    .line 10
    .line 11
    const/4 v0, 0x6

    sget-object p1, Lblg;->a:Lblg;

    .line 12
    .line 13
    const/4 v0, 0x6

    invoke-virtual {p0, p1}, Lzhh;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;

    .line 14
    .line 15
    .line 16
    const/4 v0, 0x6

    return-object p1
.end method

.method public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;
    .locals 6

    .line 1
    const/4 v5, 0x1

    iget-object v0, p0, Lzhh;->L$0:Ljava/lang/Object;

    .line 2
    .line 3
    check-cast v0, Ltha;

    .line 4
    .line 5
    const/4 v5, 0x7

    sget-object v1, Lv93;->COROUTINE_SUSPENDED:Lv93;

    .line 6
    .line 7
    iget p0, p0, Lzhh;->label:I

    .line 8
    .line 9
    const/4 v5, 0x3

    if-nez p0, :cond_40

    .line 10
    .line 11
    const/4 v5, 0x1

    invoke-static {p1}, Lu2f;->P(Ljava/lang/Object;)V

    .line 12
    .line 13
    .line 14
    sget-object p0, Lhn9;->a:Lhn9$a;

    .line 15
    .line 16
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 17
    .line 18
    .line 19
    sget-object p1, Lhn9;->b:Li1c;

    .line 20
    .line 21
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 22
    .line 23
    .line 24
    invoke-virtual {v0, p1}, Ltha;->c(Li1c;)Ljava/lang/Object;

    .line 25
    .line 26
    .line 27
    move-result-object p0

    .line 28
    const/4 v5, 0x5

    check-cast p0, Ljava/lang/Long;

    .line 29
    .line 30
    const/4 v5, 0x6

    if-eqz p0, :cond_2b

    .line 31
    .line 32
    invoke-virtual {p0}, Ljava/lang/Long;->longValue()J

    .line 33
    .line 34
    .line 35
    move-result-wide v1

    .line 36
    const/4 v5, 0x3

    goto :goto_2d

    .line 37
    :cond_2b
    const-wide/16 v1, 0x0

    .line 38
    .line 39
    :goto_2d
    const/4 v5, 0x1

    const-wide/16 v3, 0x1

    .line 40
    .line 41
    const/4 v5, 0x5

    add-long/2addr v1, v3

    .line 42
    const/4 v5, 0x7

    new-instance p0, Ljava/lang/Long;

    .line 43
    .line 44
    invoke-direct {p0, v1, v2}, Ljava/lang/Long;-><init>(J)V

    .line 45
    .line 46
    .line 47
    const/4 v5, 0x0

    invoke-virtual {v0, p1, p0}, Ltha;->e(Li1c;Ljava/lang/Object;)V

    .line 48
    .line 49
    .line 50
    const/4 v5, 0x3

    sget-object p0, Lblg;->a:Lblg;

    .line 51
    .line 52
    return-object p0

    .line 53
    :cond_40
    const/4 v5, 0x5

    const-string p0, "call to \'resume\' before \'invoke\' with coroutine"

    .line 54
    .line 55
    invoke-static {p0}, Le6d;->r(Ljava/lang/String;)V

    .line 56
    .line 57
    .line 58
    const/4 p0, 0x0

    .line 59
    return-object p0
.end method
