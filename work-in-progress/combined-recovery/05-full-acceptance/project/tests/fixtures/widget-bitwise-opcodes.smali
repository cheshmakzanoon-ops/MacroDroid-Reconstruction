.class public LWidgetBitwiseProbe;
.super Ljava/lang/Object;

.method public static ordinary(II)I
    .registers 3
    and-int v0, p0, p1
    return v0
.end method

.method public static leftAlias(II)I
    .registers 2
    and-int p0, p0, p1
    return p0
.end method

.method public static rightAlias(II)I
    .registers 2
    and-int p1, p0, p1
    return p1
.end method

.method public static highBit(I)I
    .registers 2
    const/high16 v0, -0x80000000
    and-int v0, p0, v0
    return v0
.end method
