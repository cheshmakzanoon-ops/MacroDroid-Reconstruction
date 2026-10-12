.method public static r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I
    .locals 3

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 4
    move-result-object p0

    .line 5
    const/4 v2, 0x4

    instance-of v0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    .line 7
    const/4 v2, 0x7

    if-eqz v0, :cond_13

    .line 9
    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    .line 11
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;->getIntValue()J

    .line 14
    move-result-wide v0

    .line 15
    const/4 v2, 0x6

    long-to-int p0, v0

    .line 16
    return p0

    .line 17
    :cond_13
    instance-of v0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    .line 19
    const/4 v2, 0x5

    if-eqz v0, :cond_22

    .line 21
    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    .line 23
    const/4 v2, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;->getDecimalValue()D

    .line 26
    move-result-wide v0

    .line 27
    const/4 v2, 0x4

    double-to-int p0, v0

    .line 28
    return p0

    .line 29
    :cond_22
    const/4 p0, 0x0

    .line 30
    const/4 v2, 0x6

    return p0
.end method