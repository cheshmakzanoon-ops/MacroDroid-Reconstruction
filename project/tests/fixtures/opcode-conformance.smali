.class public final Loracle/Primitives;
.super Ljava/lang/Object;

.method public static cmplFloat(FF)I
    .locals 1
    cmpl-float v0, p0, p1
    return v0
.end method
.method public static cmpgFloat(FF)I
    .locals 1
    cmpg-float v0, p0, p1
    return v0
.end method
.method public static cmplDouble(DD)I
    .locals 1
    cmpl-double v0, p0, p2
    return v0
.end method
.method public static cmpgDouble(DD)I
    .locals 1
    cmpg-double v0, p0, p2
    return v0
.end method
.method public static compareLong(JJ)I
    .locals 1
    cmp-long v0, p0, p2
    return v0
.end method
.method public static asFloat(I)F
    .locals 1
    int-to-float v0, p0
    return v0
.end method
.method public static asDouble(I)D
    .locals 2
    int-to-double v0, p0
    return-wide v0
.end method
.method public static arithmetic(DD)D
    .locals 2
    move-wide v0, p0
    sub-double/2addr v0, p2
    mul-double/2addr v0, p2
    div-double/2addr v0, p0
    add-double/2addr v0, p0
    return-wide v0
.end method
.method public static xor(II)I
    .locals 1
    move v0, p0
    xor-int/2addr v0, p1
    return v0
.end method
.method public static negativeZeroFloat()F
    .locals 1
    const v0, -0x80000000
    return v0
.end method
.method public static negativeZeroDouble()D
    .locals 2
    const-wide v0, -0x8000000000000000L
    return-wide v0
.end method
.method public static uninitialized()I
    .locals 1
    return v0
.end method
.method public static unsupported(I)I
    .locals 1
    neg-int v0, p0
    return v0
.end method

.method public static addLong(JJ)J
    .locals 2
    add-long v0, p0, p2
    return-wide v0
.end method

.method public static addLong2(JJ)J
    .locals 2
    move-wide v0, p0
    add-long/2addr v0, p2
    return-wide v0
.end method

.method public static subLong(JJ)J
    .locals 2
    sub-long v0, p0, p2
    return-wide v0
.end method

.method public static subLong2(JJ)J
    .locals 2
    move-wide v0, p0
    sub-long/2addr v0, p2
    return-wide v0
.end method

.method public static mulLong(JJ)J
    .locals 2
    mul-long v0, p0, p2
    return-wide v0
.end method

.method public static mulLong2(JJ)J
    .locals 2
    move-wide v0, p0
    mul-long/2addr v0, p2
    return-wide v0
.end method

.method public static divLong(JJ)J
    .locals 2
    div-long v0, p0, p2
    return-wide v0
.end method

.method public static divLong2(JJ)J
    .locals 2
    move-wide v0, p0
    div-long/2addr v0, p2
    return-wide v0
.end method

.method public static negLong(J)J
    .locals 2
    neg-long v0, p0
    return-wide v0
.end method

.method public static asChar(I)C
    .locals 2
    int-to-char v0, p0
    return v0
.end method

.method public static longAsInt(J)I
    .locals 2
    long-to-int v0, p0
    return v0
.end method

.method public static doubleAsLong(D)J
    .locals 2
    double-to-long v0, p0
    return-wide v0
.end method

.method public static subtractInt(II)I
    .locals 2
    sub-int v0, p0, p1
    return v0
.end method

.method public static subtractInt2(II)I
    .locals 2
    move v0, p0
    sub-int/2addr v0, p1
    return v0
.end method
