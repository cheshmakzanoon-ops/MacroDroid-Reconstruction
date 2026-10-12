.class public final Lrecovered/ui/DayTriggerValueMethods;
.super Ljava/lang/Object;


# direct methods
.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static numericValue(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I
    .locals 2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    move-result-object p0

    instance-of v0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    const/4 v1, 0x0

    if-eqz v0, :cond_a

    return v1

    :cond_a
    instance-of v0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    if-eqz v0, :cond_16

    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;->getDecimalValue()D

    move-result-wide v0

    double-to-int p0, v0

    return p0

    :cond_16
    return v1
.end method
