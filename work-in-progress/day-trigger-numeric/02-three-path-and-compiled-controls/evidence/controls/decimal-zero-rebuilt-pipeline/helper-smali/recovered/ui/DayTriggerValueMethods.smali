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

    if-eqz v0, :cond_10

    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;->getIntValue()J

    move-result-wide v0

    long-to-int p0, v0

    return p0

    :cond_10
    instance-of p0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    const/4 p0, 0x0

    return p0
.end method
