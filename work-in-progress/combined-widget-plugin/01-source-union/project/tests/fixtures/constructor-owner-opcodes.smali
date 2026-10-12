.class public LConstructorOwnerFixture;
.super Ljava/lang/Object;

.method public static parent()Ljava/lang/Object;
    .registers 3
    new-instance v0, Lzhh;
    const/4 v1, 0x2
    const/4 v2, 0x0
    invoke-direct {v0, v1, v2}, Lrff;-><init>(ILm73;)V
    return-object v0
.end method

.method public static other()Ljava/lang/Object;
    .registers 3
    new-instance v0, Lzhh;
    const/4 v1, 0x2
    const/4 v2, 0x0
    invoke-direct {v0, v1, v2}, Lrff;-><init>(ILm73;)V
    return-object v0
.end method

.method public static sameOwner()Ljava/lang/Object;
    .registers 3
    new-instance v0, Lzhh;
    const/4 v1, 0x2
    const/4 v2, 0x0
    invoke-direct {v0, v1, v2}, Lzhh;-><init>(ILm73;)V
    return-object v0
.end method

.method public static virtualConstructor()Ljava/lang/Object;
    .registers 3
    new-instance v0, Lzhh;
    const/4 v1, 0x2
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Lzhh;-><init>(ILm73;)V
    return-object v0
.end method
