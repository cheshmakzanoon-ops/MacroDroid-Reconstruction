.class public abstract Lcom/arlosoft/macrodroid/common/SelectableItem;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Landroid/os/Parcelable;


# static fields
.field protected static final MIN_CLICK_DIFF_MS:I = 0x3e8


# instance fields
.field protected transient addingFavourite:Z

.field private disableLogging:Z

.field private transient hasCommentEdited:Z

.field private transient hasEdited:Z

.field private transient isAddingNew:Z

.field private transient isCollapsed:Z

.field private m_SIGUID:J

.field private transient m_activityRef:Ljava/lang/ref/WeakReference;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/ref/WeakReference<",
            "Landroid/app/Activity;",
            ">;"
        }
    .end annotation
.end field

.field protected m_classType:Ljava/lang/String;

.field private m_comment:Ljava/lang/String;

.field private m_constraintList:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/arlosoft/macrodroid/constraint/Constraint;",
            ">;"
        }
    .end annotation
.end field

.field private m_isDisabled:Z

.field private m_isOrCondition:Z

.field protected transient m_lastClickTime:J

.field protected transient m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

.field protected transient m_returnOnComplete:Z

.field protected transient oldSearchText:Ljava/lang/String;

.field protected transient searchSelectedIndexCache:Ljava/util/HashMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/HashMap<",
            "Ljava/lang/String;",
            "Ljava/lang/Integer;",
            ">;"
        }
    .end annotation
.end field

.field protected transient serializedFormBeforeEdit:Ljava/lang/String;


# direct methods
.method public constructor <init>()V
    .locals 5

    .line 83
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 84
    const/4 v4, 0x4

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v4, 0x3

    invoke-virtual {v0}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object v0

    const/4 v4, 0x4

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_classType:Ljava/lang/String;

    .line 85
    new-instance v0, Ljava/util/HashMap;

    const/4 v4, 0x2

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    const/4 v4, 0x0

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->searchSelectedIndexCache:Ljava/util/HashMap;

    .line 86
    const/4 v4, 0x1

    const-string v0, ""

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->oldSearchText:Ljava/lang/String;

    const-wide/16 v0, 0x0

    .line 87
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_lastClickTime:J

    const/4 v2, 0x0

    .line 88
    iput-boolean v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->disableLogging:Z

    .line 89
    iput-boolean v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasEdited:Z

    .line 90
    const/4 v4, 0x7

    iput-boolean v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasCommentEdited:Z

    .line 91
    iput-boolean v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isAddingNew:Z

    .line 92
    new-instance v2, Ljava/util/ArrayList;

    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    const/4 v4, 0x1

    iput-object v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 93
    iget-wide v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    cmp-long v0, v2, v0

    if-nez v0, :cond_45

    .line 94
    invoke-static {}, Ljava/util/UUID;->randomUUID()Ljava/util/UUID;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/UUID;->getLeastSignificantBits()J

    move-result-wide v0

    const/4 v4, 0x4

    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    :cond_45
    return-void
.end method

.method public constructor <init>(Landroid/os/Parcel;)V
    .locals 4

    .line 1
    invoke-direct {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;-><init>()V

    .line 4
    new-instance v0, Ljava/util/ArrayList;

    .line 6
    const/4 v3, 0x6

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 9
    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 11
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->init()V

    .line 14
    invoke-virtual {p1}, Landroid/os/Parcel;->readLong()J

    .line 17
    move-result-wide v0

    .line 18
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 20
    const-class v0, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 22
    invoke-virtual {v0}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;

    .line 25
    move-result-object v0

    .line 26
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->readArrayList(Ljava/lang/ClassLoader;)Ljava/util/ArrayList;

    .line 29
    move-result-object v0

    .line 30
    const/4 v3, 0x7

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 32
    const/4 v3, 0x2

    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 35
    move-result v0

    .line 36
    const/4 v3, 0x2

    const/4 v1, 0x0

    .line 37
    const/4 v2, 0x1

    .line 38
    if-eqz v0, :cond_2d

    .line 40
    move v0, v2

    .line 41
    goto :goto_2e

    .line 42
    :cond_2d
    move v0, v1

    .line 43
    :goto_2e
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isOrCondition:Z

    .line 45
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 48
    move-result v0

    .line 49
    if-eqz v0, :cond_3a

    .line 51
    const/4 v3, 0x6

    move v0, v2

    .line 52
    const/4 v3, 0x5

    goto :goto_3c

    .line 53
    :cond_3a
    const/4 v3, 0x6

    move v0, v1

    .line 54
    :goto_3c
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 56
    invoke-virtual {p1}, Landroid/os/Parcel;->readString()Ljava/lang/String;

    .line 59
    move-result-object v0

    .line 60
    const/4 v3, 0x6

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 62
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 65
    move-result v0

    .line 66
    if-eqz v0, :cond_4d

    .line 68
    move v0, v2

    .line 69
    goto :goto_4e

    .line 70
    :cond_4d
    move v0, v1

    .line 71
    :goto_4e
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isCollapsed:Z

    .line 73
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 76
    move-result p1

    .line 77
    const/4 v3, 0x5

    if-eqz p1, :cond_58

    .line 79
    move v1, v2

    .line 80
    :cond_58
    iput-boolean v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->disableLogging:Z

    .line 82
    return-void
.end method

.method public static P(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/util/ArrayList;Ljava/util/ArrayList;)V
    .locals 4

    .line 1
    const-string v3, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 4
    move-result-object v0

    .line 5
    invoke-interface {v0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 8
    move-result-object v0

    .line 9
    :cond_a
    :goto_a
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 12
    move-result v1

    .line 13
    const/4 v3, 0x5

    if-eqz v1, :cond_3a

    .line 15
    const/4 v3, 0x4

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 18
    move-result-object v1

    .line 19
    const/4 v3, 0x6

    check-cast v1, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 21
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;

    .line 24
    move-result-object v2

    .line 25
    const/4 v3, 0x0

    invoke-virtual {p2, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 28
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 31
    move-result-object v2

    .line 32
    const/4 v3, 0x6

    instance-of v2, v2, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 34
    if-eqz v2, :cond_a

    .line 36
    invoke-virtual {p0, p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->setParentKeys(Ljava/util/List;)V

    .line 39
    invoke-virtual {p1, p0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 42
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 45
    move-result-object v1

    .line 46
    check-cast v1, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 48
    invoke-static {v1, p1, p2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->P(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/util/ArrayList;Ljava/util/ArrayList;)V

    .line 51
    goto :goto_a

    .line 52
    :cond_3a
    return-void
.end method

.method public static R(Ljava/lang/String;Ljava/lang/String;)Z
    .locals 4

    .line 1
    const/4 v3, 0x3

    const/4 v0, 0x0

    .line 2
    const/4 v3, 0x1

    if-nez p1, :cond_7

    .line 4
    const/4 v3, 0x7

    return v0

    .line 5
    :cond_7
    const-string v1, "&amp;"

    .line 7
    const-string v2, "&"

    .line 9
    invoke-static {p1, v1, v2, v0}, Lg9f;->p1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    .line 12
    move-result-object p1

    .line 13
    const/4 v3, 0x1

    const-string v1, "&lt;"

    .line 15
    const-string v2, "<"

    .line 17
    invoke-static {p1, v1, v2, v0}, Lg9f;->p1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    .line 20
    move-result-object p1

    .line 21
    const/4 v3, 0x5

    const-string v1, ";gt&"

    const-string v1, "&gt;"

    .line 23
    const-string v2, ">"

    const-string v2, ">"

    .line 25
    const/4 v3, 0x2

    invoke-static {p1, v1, v2, v0}, Lg9f;->p1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    .line 28
    move-result-object p1

    .line 29
    const/4 v3, 0x3

    const-string v1, "&quot;"

    .line 31
    const/4 v3, 0x4

    const-string v2, "\""

    .line 33
    invoke-static {p1, v1, v2, v0}, Lg9f;->p1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    .line 36
    move-result-object p1

    .line 37
    const/4 v3, 0x3

    const-string v1, "&#39;"

    .line 39
    const-string v2, "\'"

    .line 41
    invoke-static {p1, v1, v2, v0}, Lg9f;->p1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;

    .line 44
    move-result-object p1

    .line 45
    invoke-virtual {p1}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;

    .line 48
    move-result-object p1

    .line 49
    invoke-virtual {p0}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;

    .line 52
    move-result-object p0

    .line 53
    invoke-virtual {p1, p0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 56
    move-result p0

    .line 57
    return p0
.end method

.method public static getNoItemsText(I)I
    .locals 2

    .line 1
    if-eqz p0, :cond_e

    .line 3
    const/4 v1, 0x3

    const/4 v0, 0x1

    .line 4
    if-eq p0, v0, :cond_a

    .line 6
    const p0, 0x7f1410b0

    .line 9
    return p0

    .line 10
    :cond_a
    const p0, 0x7f1410a5

    .line 13
    return p0

    .line 14
    :cond_e
    const p0, 0x7f1410d4

    .line 17
    const/4 v1, 0x4

    return p0
.end method

.method public static getSettingBoolean(Landroid/content/Context;Ljava/lang/String;)Z
    .locals 2

    .line 1
    invoke-static {p0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x0

    .line 6
    invoke-interface {p0, p1, v0}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    .line 9
    move-result p0

    .line 10
    return p0
.end method

.method public static getString(I)Ljava/lang/String;
    .locals 2

    .line 1
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x3

    invoke-virtual {v0, p0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 8
    move-result-object p0

    .line 9
    const/4 v1, 0x7

    return-object p0
.end method

.method public static setSettingBoolean(Landroid/content/Context;Ljava/lang/String;Z)V
    .locals 1

    .line 1
    const/4 v0, 0x7

    invoke-static {p0, p1, p2}, Lni9;->D(Landroid/content/Context;Ljava/lang/String;Z)V

    .line 4
    return-void
.end method


# virtual methods
.method public final Q(Ljava/lang/String;)Z
    .locals 3

    .line 1
    const/4 v2, 0x1

    const/4 v0, 0x0

    .line 2
    if-nez p1, :cond_5

    .line 4
    return v0

    .line 5
    :cond_5
    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 8
    move-result-object p1

    .line 9
    const/4 v2, 0x2

    invoke-virtual {p1}, Ljava/lang/String;->isEmpty()Z

    .line 12
    move-result v1

    .line 13
    const/4 v2, 0x2

    if-eqz v1, :cond_12

    .line 15
    return v0

    .line 16
    :cond_12
    const-string v1, "["

    .line 18
    const/4 v2, 0x3

    invoke-virtual {p1, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 21
    move-result v1

    .line 22
    const/4 v2, 0x2

    if-nez v1, :cond_34

    .line 24
    const/4 v2, 0x1

    const-string/jumbo v1, "{"

    const-string/jumbo v1, "{"

    .line 26
    invoke-virtual {p1, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 29
    move-result v1

    .line 30
    if-eqz v1, :cond_2a

    .line 32
    goto :goto_34

    .line 33
    :cond_2a
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 36
    move-result-object p0

    .line 37
    const/4 v2, 0x3

    if-nez p0, :cond_34

    .line 39
    const/4 p0, 0x1

    .line 40
    const/4 v2, 0x1

    return p0

    .line 41
    :cond_34
    :goto_34
    return v0
.end method

.method public addConstraint(Lcom/arlosoft/macrodroid/constraint/Constraint;)V
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 4
    move-result-object p0

    .line 5
    invoke-interface {p0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 8
    return-void
.end method

.method public addConstraintAtIndex(Lcom/arlosoft/macrodroid/constraint/Constraint;I)V
    .locals 2

    .line 1
    const/4 v1, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 4
    move-result-object p0

    .line 5
    const/4 v1, 0x1

    invoke-interface {p0}, Ljava/util/List;->size()I

    .line 8
    move-result v0

    .line 9
    const/4 v1, 0x7

    if-lt p2, v0, :cond_19

    .line 11
    invoke-interface {p0}, Ljava/util/List;->size()I

    .line 14
    move-result p2

    .line 15
    add-int/lit8 p2, p2, -0x1

    .line 17
    const/4 v0, 0x1

    const/4 v0, 0x0

    .line 18
    invoke-static {p2, v0}, Ljava/lang/Math;->max(II)I

    .line 21
    move-result p2

    .line 22
    :cond_19
    const/4 v1, 0x1

    invoke-interface {p0, p2, p1}, Ljava/util/List;->add(ILjava/lang/Object;)V

    .line 25
    return-void
.end method

.method public addVariable(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V
    .locals 2

    .line 1
    const/4 v1, 0x4

    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    const/4 v1, 0x2

    if-eqz v0, :cond_18

    .line 5
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->i0()Z

    .line 8
    move-result v0

    .line 9
    if-eqz v0, :cond_18

    .line 11
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 13
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariables()Ljava/util/List;

    .line 16
    move-result-object p0

    .line 17
    const/4 v1, 0x0

    invoke-interface {p0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 20
    const/4 v1, 0x6

    return-void

    .line 21
    :cond_18
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 24
    move-result-object p0

    .line 25
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/a;->a(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 28
    const/4 v1, 0x2

    return-void
.end method

.method public allowConfigurationWithoutHelperFile()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public anonymizeForTemplate()V
    .locals 2

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 4
    move-result-object p0

    .line 5
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 8
    move-result-object p0

    .line 9
    :goto_8
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 12
    move-result v0

    .line 13
    if-eqz v0, :cond_19

    .line 15
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 18
    move-result-object v0

    .line 19
    const/4 v1, 0x6

    check-cast v0, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 21
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->anonymizeForTemplate()V

    .line 24
    goto :goto_8

    .line 25
    :cond_19
    return-void
.end method

.method public applyImport()V
    .locals 7

    .line 1
    instance-of v0, p0, Ly57;

    .line 3
    if-eqz v0, :cond_32

    .line 5
    move-object v0, p0

    .line 6
    check-cast v0, Ly57;

    .line 8
    invoke-interface {v0}, Ly57;->r()Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 11
    move-result-object v0

    .line 12
    if-eqz v0, :cond_7d

    .line 14
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 17
    move-result-object v1

    .line 18
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 21
    move-result-object v2

    .line 22
    invoke-virtual {v1, v2}, Lcom/arlosoft/macrodroid/common/a;->s(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 25
    move-result-object v1

    .line 26
    if-nez v1, :cond_7d

    .line 28
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 30
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 33
    move-result-object v2

    .line 34
    const/4 v6, 0x1

    invoke-virtual {v1, v2}, Lcom/arlosoft/macrodroid/macro/Macro;->findLocalVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 37
    move-result-object v1

    .line 38
    const/4 v6, 0x1

    if-nez v1, :cond_7d

    .line 40
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object v1

    .line 44
    const/4 v6, 0x4

    invoke-virtual {v1, v0}, Lcom/arlosoft/macrodroid/common/a;->a(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 47
    goto :goto_7d

    .line 48
    :cond_32
    instance-of v0, p0, Lb67;

    .line 50
    if-eqz v0, :cond_7d

    .line 52
    move-object v0, p0

    move-object v0, p0

    .line 53
    const/4 v6, 0x3

    check-cast v0, Lb67;

    .line 55
    invoke-interface {v0}, Lb67;->i()Ljava/util/ArrayList;

    .line 58
    move-result-object v0

    .line 59
    const/4 v6, 0x6

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 62
    move-result-object v0

    .line 63
    :cond_44
    :goto_44
    const/4 v6, 0x3

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 66
    move-result v1

    .line 67
    const/4 v6, 0x2

    if-eqz v1, :cond_7d

    .line 69
    const/4 v6, 0x2

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 72
    move-result-object v1

    .line 73
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 75
    if-eqz v1, :cond_44

    .line 77
    const/4 v6, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 80
    move-result-object v2

    .line 81
    const/4 v6, 0x1

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 84
    move-result-object v3

    .line 85
    invoke-virtual {v2, v3}, Lcom/arlosoft/macrodroid/common/a;->s(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 88
    move-result-object v2

    .line 89
    if-nez v2, :cond_44

    .line 91
    iget-object v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 93
    if-eqz v2, :cond_74

    .line 95
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 98
    move-result-object v3

    .line 99
    const/4 v6, 0x3

    invoke-virtual {v2, v3}, Lcom/arlosoft/macrodroid/macro/Macro;->findLocalVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 102
    move-result-object v2

    .line 103
    if-nez v2, :cond_44

    .line 105
    :cond_74
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 108
    move-result-object v2

    .line 109
    invoke-virtual {v2, v1}, Lcom/arlosoft/macrodroid/common/a;->a(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 112
    const/4 v6, 0x7

    goto :goto_44

    .line 113
    :cond_7d
    :goto_7d
    instance-of v0, p0, Lz57;

    .line 115
    const/4 v1, 0x0

    .line 116
    if-eqz v0, :cond_b9

    .line 118
    move-object v0, p0

    move-object v0, p0

    .line 119
    check-cast v0, Lz57;

    .line 121
    const/4 v6, 0x2

    invoke-interface {v0}, Lz57;->k()Ljava/lang/String;

    .line 124
    move-result-object v2

    .line 125
    const/4 v6, 0x2

    if-eqz v2, :cond_92

    .line 127
    invoke-virtual {v2}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 130
    move-result-object v2

    .line 131
    :cond_92
    if-eqz v2, :cond_b9

    .line 133
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 136
    move-result-object v3

    .line 137
    invoke-virtual {v3, v2}, Lcom/arlosoft/macrodroid/common/a;->s(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 140
    move-result-object v3

    .line 141
    const/4 v6, 0x3

    if-nez v3, :cond_b9

    .line 143
    const/4 v6, 0x3

    iget-object v3, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 145
    const/4 v6, 0x0

    invoke-virtual {v3, v2}, Lcom/arlosoft/macrodroid/macro/Macro;->findLocalVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 148
    move-result-object v3

    .line 149
    if-nez v3, :cond_b9

    .line 151
    new-instance v3, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 153
    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getTypeFromClass(Lz57;)I

    .line 156
    move-result v0

    .line 157
    invoke-direct {v3, v0, v2, v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;-><init>(ILjava/lang/String;Z)V

    .line 160
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 163
    move-result-object v0

    .line 164
    invoke-virtual {v0, v3}, Lcom/arlosoft/macrodroid/common/a;->a(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 167
    :cond_b9
    instance-of v0, p0, La67;

    .line 169
    if-eqz v0, :cond_115

    .line 171
    move-object v0, p0

    .line 172
    const/4 v6, 0x4

    check-cast v0, La67;

    .line 174
    invoke-interface {v0}, La67;->getVariableNames()[Ljava/lang/String;

    .line 177
    move-result-object v0

    .line 178
    move v2, v1

    .line 179
    :goto_c6
    array-length v3, v0

    .line 180
    if-ge v2, v3, :cond_115

    .line 182
    aget-object v3, v0, v2

    .line 184
    if-eqz v3, :cond_d1

    .line 186
    invoke-virtual {v3}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 189
    move-result-object v3

    .line 190
    :cond_d1
    const/4 v6, 0x2

    if-eqz v3, :cond_112

    .line 192
    invoke-virtual {v3}, Ljava/lang/String;->isEmpty()Z

    .line 195
    move-result v4

    .line 196
    const/4 v6, 0x1

    if-nez v4, :cond_112

    .line 198
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 201
    move-result-object v4

    .line 202
    const/4 v6, 0x0

    invoke-virtual {v4, v3}, Lcom/arlosoft/macrodroid/common/a;->s(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 205
    move-result-object v4

    .line 206
    if-nez v4, :cond_112

    .line 208
    const/4 v6, 0x0

    iget-object v4, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 210
    if-eqz v4, :cond_f3

    .line 212
    const/4 v6, 0x2

    invoke-virtual {v4, v3}, Lcom/arlosoft/macrodroid/macro/Macro;->findLocalVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 215
    move-result-object v4

    .line 216
    const/4 v6, 0x7

    if-nez v4, :cond_112

    .line 218
    :cond_f3
    :try_start_f3
    move-object v4, p0

    .line 219
    check-cast v4, La67;

    .line 221
    invoke-interface {v4}, La67;->getVariableTypes()[Ljava/lang/Integer;

    .line 224
    move-result-object v4

    .line 225
    const/4 v6, 0x1

    aget-object v4, v4, v2

    .line 227
    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    .line 230
    move-result v4
    :try_end_101
    .catch Ljava/lang/Exception; {:try_start_f3 .. :try_end_101} :catch_102

    .line 231
    goto :goto_104

    .line 232
    :catch_102
    const/4 v6, 0x6

    const/4 v4, 0x2

    .line 233
    :goto_104
    new-instance v5, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 235
    invoke-direct {v5, v4, v3, v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;-><init>(ILjava/lang/String;Z)V

    .line 238
    const/4 v6, 0x5

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 241
    move-result-object v3

    .line 242
    const/4 v6, 0x5

    invoke-virtual {v3, v5}, Lcom/arlosoft/macrodroid/common/a;->a(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 245
    :cond_112
    add-int/lit8 v2, v2, 0x1

    .line 247
    goto :goto_c6

    .line 248
    :cond_115
    return-void
.end method

.method public applyImport(Z)V
    .locals 1

    if-eqz p1, :cond_e

    .line 249
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->doesSupportPreApply()Z

    move-result p1

    const/4 v0, 0x0

    if-eqz p1, :cond_e

    .line 250
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->preApplyImport()V

    const/4 v0, 0x0

    return-void

    .line 251
    :cond_e
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->applyImport()V

    return-void
.end method

.method public applyMagicText(Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;
    .locals 3

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 4
    move-result-object v0

    .line 5
    const/4 v2, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    move-result-object p0

    .line 9
    sget-object v1, Lkxg$a;->TO_STRING:Lkxg$a;

    .line 11
    invoke-static {v0, p1, p2, p0, v1}, Lsr9;->m(Landroid/content/Context;Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lcom/arlosoft/macrodroid/macro/Macro;Lkxg$a;)Ljava/lang/String;

    .line 14
    move-result-object p0

    .line 15
    const/4 v2, 0x0

    invoke-static {p0}, Lvdg;->h0(Ljava/lang/String;)Ljava/lang/String;

    .line 18
    move-result-object p0

    .line 19
    return-object p0
.end method

.method public applyMagicText(Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lkxg$a;)Ljava/lang/String;
    .locals 2

    .line 20
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    move-result-object v0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    move-result-object p0

    invoke-static {v0, p1, p2, p0, p3}, Lsr9;->m(Landroid/content/Context;Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lcom/arlosoft/macrodroid/macro/Macro;Lkxg$a;)Ljava/lang/String;

    move-result-object p0

    .line 21
    const/4 v1, 0x5

    invoke-static {p0}, Lvdg;->h0(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    const/4 v1, 0x5

    return-object p0
.end method

.method public applyMagicTextLeaveNewLines(Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0, p1, p2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->applyMagicTextNoNewLines(Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x1

    return-object p0
.end method

.method public applyMagicTextNoNewLines(Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;
    .locals 3

    .line 1
    const/4 v2, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 4
    move-result-object v0

    .line 5
    const/4 v2, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    move-result-object p0

    .line 9
    const/4 v2, 0x4

    sget-object v1, Lkxg$a;->TO_STRING:Lkxg$a;

    .line 11
    invoke-static {v0, p1, p2, p0, v1}, Lsr9;->m(Landroid/content/Context;Ljava/lang/String;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lcom/arlosoft/macrodroid/macro/Macro;Lkxg$a;)Ljava/lang/String;

    .line 14
    move-result-object p0

    .line 15
    return-object p0
.end method

.method public canRunWhenInvalid()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public canUseConnectivityHelperApp()Landroid/util/Pair;
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Landroid/util/Pair<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 p0, 0x0

    move v0, p0

    .line 2
    return-object p0
.end method

.method public canUseShizukuAsHelperAlternative()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x2

    return p0
.end method

.method public checkActivityAlive()Z
    .locals 3

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_activityRef:Ljava/lang/ref/WeakReference;

    .line 3
    const/4 v0, 0x0

    .line 4
    if-nez p0, :cond_6

    .line 6
    return v0

    .line 7
    :cond_6
    invoke-virtual {p0}, Ljava/lang/ref/Reference;->get()Ljava/lang/Object;

    .line 10
    move-result-object p0

    .line 11
    const/4 v2, 0x6

    check-cast p0, Landroid/app/Activity;

    .line 13
    if-nez p0, :cond_10

    .line 15
    return v0

    .line 16
    :cond_10
    instance-of v0, p0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 18
    const/4 v1, 0x1

    .line 19
    if-eqz v0, :cond_1f

    .line 21
    check-cast p0, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 23
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;->T0()Z

    .line 26
    move-result p0

    .line 27
    const/4 v2, 0x4

    xor-int/2addr p0, v1

    .line 28
    const/4 v2, 0x3

    return p0

    .line 29
    :cond_1f
    const/4 v2, 0x1

    return v1
.end method

.method public checkAllPermissions()Z
    .locals 2

    const/4 v0, 0x0

    .line 958
    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkAllPermissions(Z)Z

    move-result p0

    const/4 v1, 0x5

    return p0
.end method

.method public checkAllPermissions(Z)Z
    .locals 9

    .line 1
    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 3
    const/4 v1, 0x1

    .line 4
    const/4 v8, 0x4

    if-eqz v0, :cond_8

    .line 6
    goto/16 :goto_43e

    .line 8
    :cond_8
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresWriteSettings()Z

    .line 11
    move-result v0

    .line 12
    const/4 v8, 0x4

    const/4 v2, 0x0

    .line 13
    const/4 v3, 0x6

    const/4 v3, 0x0

    .line 14
    if-eqz v0, :cond_30

    .line 16
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 19
    move-result-object v0

    .line 20
    invoke-static {v0}, Landroid/provider/Settings$System;->canWrite(Landroid/content/Context;)Z

    .line 23
    move-result v0

    .line 24
    if-nez v0, :cond_30

    .line 26
    const-string p1, "Missing write settings permission"

    .line 28
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 31
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 34
    move-result-object p1

    .line 35
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 38
    move-result-object p0

    .line 39
    invoke-static {p1, p0, v2, v1}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 42
    const/4 v8, 0x6

    return v3

    .line 43
    :cond_30
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanDrawOverlays()Z

    .line 46
    move-result v0

    .line 47
    const/4 v4, 0x2

    .line 48
    if-eqz v0, :cond_77

    .line 50
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 53
    move-result-object v0

    .line 54
    invoke-static {v0}, Llob;->a(Landroid/content/Context;)Z

    .line 57
    move-result v0

    .line 58
    const/4 v8, 0x3

    if-nez v0, :cond_77

    .line 60
    const/4 v8, 0x5

    new-instance p1, Ljava/lang/StringBuilder;

    .line 62
    const-string v0, "Cannot run "

    .line 64
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 67
    const/4 v8, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 70
    move-result-object v0

    .line 71
    const/4 v8, 0x2

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 74
    const-string v0, " - the display over other apps permission is not enabled"

    .line 76
    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 79
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 82
    move-result-object p1

    .line 83
    const/4 v8, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 86
    move-result-object v0

    .line 87
    const/4 v8, 0x0

    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 90
    move-result-wide v0

    .line 91
    const/4 v8, 0x0

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 94
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 97
    move-result-object p1

    .line 98
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 101
    move-result-object p0

    .line 102
    invoke-static {p1, p0, v2, v4}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 105
    return v3

    .line 106
    :cond_77
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresCanShowBubbles()Z

    .line 109
    move-result v0

    .line 110
    const/4 v8, 0x4

    if-eqz v0, :cond_cc

    .line 112
    const/4 v8, 0x3

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 114
    const/16 v5, 0x1d

    .line 116
    const/4 v8, 0x1

    if-ge v0, v5, :cond_88

    .line 118
    goto/16 :goto_43e

    .line 120
    :cond_88
    :try_start_88
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 123
    move-result-object v0

    .line 124
    invoke-virtual {v0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 127
    move-result-object v0

    .line 128
    const/4 v8, 0x1

    const-string v5, "notification_bubbles"

    .line 130
    const/4 v8, 0x3

    invoke-static {v0, v5}, Landroid/provider/Settings$Global;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 133
    move-result v0
    :try_end_99
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_88 .. :try_end_99} :catch_9f

    .line 134
    const/4 v8, 0x5

    if-ne v0, v1, :cond_9d

    .line 136
    goto :goto_9f

    .line 137
    :cond_9d
    move v0, v3

    .line 138
    goto :goto_a0

    .line 139
    :catch_9f
    :goto_9f
    move v0, v1

    .line 140
    :goto_a0
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 143
    move-result-object v5

    .line 144
    const/4 v8, 0x7

    const-class v6, Landroid/app/NotificationManager;

    .line 146
    invoke-virtual {v5, v6}, Landroid/content/Context;->getSystemService(Ljava/lang/Class;)Ljava/lang/Object;

    .line 149
    move-result-object v5

    .line 150
    check-cast v5, Landroid/app/NotificationManager;

    .line 152
    if-eqz v0, :cond_b8

    .line 154
    invoke-virtual {v5}, Landroid/app/NotificationManager;->areBubblesAllowed()Z

    .line 157
    move-result v0

    .line 158
    const/4 v8, 0x4

    if-eqz v0, :cond_b8

    .line 160
    const/4 v8, 0x3

    goto :goto_cc

    .line 161
    :cond_b8
    const-string p1, "Missing show bubbles permission"

    .line 163
    const/4 v8, 0x0

    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 166
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 169
    move-result-object p1

    .line 170
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 173
    move-result-object p0

    .line 174
    const/16 v0, 0xf

    .line 176
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 179
    return v3

    .line 180
    :cond_cc
    :goto_cc
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresLocationServicesEnabled()Z

    .line 183
    move-result v0

    .line 184
    if-eqz v0, :cond_f4

    .line 186
    :try_start_d3
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 189
    move-result-object v0

    .line 190
    invoke-virtual {v0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 193
    move-result-object v0

    .line 194
    const-string v5, "ldscaon_mioet"

    const-string v5, "location_mode"

    .line 196
    invoke-static {v0, v5}, Landroid/provider/Settings$Secure;->getInt(Landroid/content/ContentResolver;Ljava/lang/String;)I

    .line 199
    move-result v0
    :try_end_e3
    .catch Landroid/provider/Settings$SettingNotFoundException; {:try_start_d3 .. :try_end_e3} :catch_f4

    .line 200
    if-eqz v0, :cond_e6

    .line 202
    goto :goto_f4

    .line 203
    :cond_e6
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 206
    move-result-object p1

    .line 207
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 210
    move-result-object p0

    .line 211
    const/16 v0, 0xb

    .line 213
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 216
    return v3

    .line 217
    :catch_f4
    :cond_f4
    :goto_f4
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUsageAccess()Z

    .line 220
    move-result v0

    .line 221
    if-eqz v0, :cond_13b

    .line 223
    :try_start_fa
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 226
    move-result-object v0

    .line 227
    invoke-virtual {v0}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 230
    move-result-object v0

    .line 231
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 234
    move-result-object v5

    .line 235
    invoke-virtual {v5}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 238
    move-result-object v5

    .line 239
    invoke-virtual {v0, v5, v3}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;I)Landroid/content/pm/ApplicationInfo;

    .line 242
    move-result-object v0

    .line 243
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 246
    move-result-object v5

    .line 247
    const-string v6, "aopmps"

    const-string v6, "appops"

    .line 249
    invoke-virtual {v5, v6}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 252
    move-result-object v5

    .line 253
    const/4 v8, 0x0

    check-cast v5, Landroid/app/AppOpsManager;

    .line 255
    const-string v6, "android:get_usage_stats"

    .line 257
    iget v7, v0, Landroid/content/pm/ApplicationInfo;->uid:I

    .line 259
    iget-object v0, v0, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    .line 261
    invoke-virtual {v5, v6, v7, v0}, Landroid/app/AppOpsManager;->checkOpNoThrow(Ljava/lang/String;ILjava/lang/String;)I

    .line 264
    move-result v0
    :try_end_129
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_fa .. :try_end_129} :catch_12d

    .line 265
    const/4 v8, 0x1

    if-nez v0, :cond_12d

    .line 267
    goto :goto_13b

    .line 268
    :catch_12d
    :cond_12d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 271
    move-result-object p1

    .line 272
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 275
    move-result-object p0

    .line 276
    const/4 v0, 0x3

    .line 277
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 280
    const/4 v8, 0x5

    return v3

    .line 281
    :cond_13b
    :goto_13b
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessibility()Z

    .line 284
    move-result v0

    .line 285
    const-wide/16 v5, 0x7d0

    .line 287
    const/4 v8, 0x3

    if-eqz v0, :cond_179

    .line 289
    const/4 v8, 0x7

    if-eqz p1, :cond_15a

    .line 291
    new-instance v0, Landroid/os/Handler;

    .line 293
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 296
    move-result-object v7

    .line 297
    invoke-direct {v0, v7}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 300
    new-instance v7, Lsl9;

    .line 302
    const/4 v8, 0x1

    invoke-direct {v7, v1, p0}, Lsl9;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 305
    invoke-virtual {v0, v7, v5, v6}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 308
    goto :goto_179

    .line 309
    :cond_15a
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 312
    move-result-object v0

    .line 313
    const/4 v8, 0x2

    invoke-static {v0}, Lhtg;->I(Landroid/content/Context;)Z

    .line 316
    move-result v0

    .line 317
    if-nez v0, :cond_179

    .line 319
    const-string p1, "Accessibility service is not enabled"

    .line 321
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 324
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 327
    move-result-object p1

    .line 328
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 331
    move-result-object p0

    .line 332
    const/4 v8, 0x7

    const/4 v0, 0x4

    .line 333
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 336
    const/4 v8, 0x7

    return v3

    .line 337
    :cond_179
    :goto_179
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresUIInteractionAccessibility()Z

    .line 340
    move-result v0

    .line 341
    if-eqz v0, :cond_1b9

    .line 343
    if-eqz p1, :cond_196

    .line 345
    const/4 v8, 0x4

    new-instance p1, Landroid/os/Handler;

    .line 347
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 350
    move-result-object v0

    .line 351
    const/4 v8, 0x2

    invoke-direct {p1, v0}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 354
    new-instance v0, Lsl9;

    .line 356
    invoke-direct {v0, v4, p0}, Lsl9;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 359
    invoke-virtual {p1, v0, v5, v6}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 362
    goto :goto_1b9

    .line 363
    :cond_196
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 366
    move-result-object p1

    .line 367
    const/4 v8, 0x6

    invoke-static {p1}, Lhtg;->J(Landroid/content/Context;)Z

    .line 370
    move-result p1

    .line 371
    const/4 v8, 0x5

    if-nez p1, :cond_1b9

    .line 373
    const-string p1, "UI interaction accessibility service is not enabled"

    .line 375
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 378
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 381
    move-result-object p1

    .line 382
    const/4 v8, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 385
    move-result-object p0

    .line 386
    const/4 v8, 0x7

    const/16 v0, 0xa

    .line 388
    const/4 v8, 0x4

    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 391
    const/4 v8, 0x3

    return v3

    .line 392
    :cond_1b9
    :goto_1b9
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDeviceAdmin()Z

    .line 395
    move-result p1

    .line 396
    if-eqz p1, :cond_1f6

    .line 398
    const/4 v8, 0x0

    new-instance p1, Landroid/content/ComponentName;

    .line 400
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 403
    move-result-object v0

    .line 404
    const-class v4, Lcom/arlosoft/macrodroid/triggers/receivers/MacroDroidDeviceAdminReceiver;

    .line 406
    invoke-direct {p1, v0, v4}, Landroid/content/ComponentName;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 409
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 412
    move-result-object v0

    .line 413
    const-string v4, "device_policy"

    .line 415
    invoke-virtual {v0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 418
    move-result-object v0

    .line 419
    const/4 v8, 0x3

    check-cast v0, Landroid/app/admin/DevicePolicyManager;

    .line 421
    invoke-virtual {v0, p1}, Landroid/app/admin/DevicePolicyManager;->isAdminActive(Landroid/content/ComponentName;)Z

    .line 424
    move-result p1

    .line 425
    if-nez p1, :cond_1f6

    .line 427
    const/4 v8, 0x0

    const-string p1, "Device admin access for MacroDroid is not enabled"

    .line 429
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 432
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 435
    move-result-object p1

    .line 436
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 439
    move-result-object p0

    .line 440
    const/4 v8, 0x1

    const/4 v0, 0x5

    .line 441
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 444
    const/4 v8, 0x0

    return v3

    .line 445
    :cond_1f6
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNotificationAccess()Z

    .line 448
    move-result p1

    .line 449
    if-eqz p1, :cond_247

    .line 451
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 454
    move-result-object p1

    .line 455
    const/4 v8, 0x2

    invoke-virtual {p1}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    .line 458
    move-result-object p1

    .line 459
    const/4 v8, 0x2

    const-string v0, "enabled_notification_listeners"

    .line 461
    invoke-static {p1, v0}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    .line 464
    move-result-object p1

    .line 465
    const/4 v8, 0x3

    if-eqz p1, :cond_234

    .line 467
    const/4 v8, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 470
    move-result-object v0

    .line 471
    invoke-virtual {v0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 474
    move-result-object v0

    .line 475
    const/4 v8, 0x1

    invoke-virtual {p1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 478
    move-result v0

    .line 479
    const/4 v8, 0x4

    if-eqz v0, :cond_234

    .line 481
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 483
    const/16 v4, 0x1a

    .line 485
    if-lt v0, v4, :cond_247

    .line 487
    const/4 v8, 0x4

    const-class v0, Lcom/arlosoft/macrodroid/triggers/services/NotificationServiceOreo;

    .line 489
    invoke-virtual {v0}, Ljava/lang/Class;->getName()Ljava/lang/String;

    .line 492
    move-result-object v0

    .line 493
    const/4 v8, 0x6

    invoke-virtual {p1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    .line 496
    move-result p1

    .line 497
    if-nez p1, :cond_247

    .line 499
    :cond_234
    const-string p1, "Notification access for MacroDroid is not enabled"

    .line 501
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 504
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 507
    move-result-object p1

    .line 508
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 511
    move-result-object p0

    .line 512
    const/4 v8, 0x6

    const/4 v0, 0x6

    .line 513
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 516
    return v3

    .line 517
    :cond_247
    const/4 v8, 0x7

    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 519
    const/16 v0, 0x18

    .line 521
    const/4 v8, 0x4

    if-lt p1, v0, :cond_27f

    .line 523
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAccessNotificationPolicy()Z

    .line 526
    move-result v0

    .line 527
    const/4 v8, 0x6

    if-eqz v0, :cond_27f

    .line 529
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 532
    move-result-object v0

    .line 533
    const-string v4, "aincontiifoo"

    const-string v4, "notification"

    .line 535
    const/4 v8, 0x7

    invoke-virtual {v0, v4}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 538
    move-result-object v0

    .line 539
    check-cast v0, Landroid/app/NotificationManager;

    .line 541
    invoke-virtual {v0}, Landroid/app/NotificationManager;->isNotificationPolicyAccessGranted()Z

    .line 544
    move-result v0

    .line 545
    if-nez v0, :cond_27f

    .line 547
    const/4 v8, 0x1

    const-string p1, "Notification policy access for MacroDroid is not enabled"

    .line 549
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 552
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 555
    move-result-object p1

    .line 556
    const/4 v8, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 559
    move-result-object p0

    .line 560
    const/4 v0, 0x7

    .line 561
    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 564
    return v3

    .line 565
    :cond_27f
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresDefaultAssist()Z

    .line 568
    move-result v0

    .line 569
    const/4 v8, 0x1

    if-eqz v0, :cond_2a7

    .line 571
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 574
    move-result-object v0

    .line 575
    invoke-static {v0}, Lgi0;->d(Landroid/content/Context;)Z

    .line 578
    move-result v0

    .line 579
    const/4 v8, 0x6

    if-nez v0, :cond_2a7

    .line 581
    const-string p1, "Default app permission for MacroDroid is not enabled"

    .line 583
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 586
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 589
    move-result-object p1

    .line 590
    const/4 v8, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 593
    move-result-object p0

    .line 594
    const/16 v0, 0xc

    .line 596
    const/4 v8, 0x3

    invoke-static {p1, p0, v2, v0}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 599
    return v3

    .line 600
    :cond_2a7
    const/4 v8, 0x4

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    .line 603
    move-result-wide v4

    .line 604
    const/4 v8, 0x2

    sget-object v0, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->E:Lcom/arlosoft/macrodroid/app/MacroDroidApplication$a;

    .line 606
    const/4 v8, 0x2

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 609
    sget-wide v6, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->G:J

    .line 611
    sub-long/2addr v4, v6

    .line 612
    const-wide/16 v6, 0x3e8

    const-wide/16 v6, 0x3e8

    .line 614
    div-long/2addr v4, v6

    .line 615
    const/4 v8, 0x1

    const-wide/16 v6, 0x3c

    .line 617
    cmp-long v0, v4, v6

    .line 619
    const/4 v8, 0x7

    if-lez v0, :cond_33a

    .line 621
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresShizuku()Z

    .line 624
    move-result v0

    .line 625
    if-eqz v0, :cond_33a

    .line 627
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 630
    move-result-object v0

    .line 631
    const/4 v8, 0x4

    iget-object v0, v0, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->n:Ldje;

    .line 633
    invoke-virtual {v0, v3}, Ldje;->c(Z)Ljje;

    .line 636
    move-result-object v0

    .line 637
    sget-object v4, Ljje;->GRANTED:Ljje;

    .line 639
    if-eq v0, v4, :cond_33a

    .line 641
    sget-object p1, Ljje;->VERSION_NOT_SUPPORTED:Ljje;

    .line 643
    if-ne v0, p1, :cond_2ef

    .line 645
    const p1, 0x7f14141b

    .line 648
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 651
    move-result-object p1

    .line 652
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 655
    move-result-wide v0

    .line 656
    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 659
    const/16 p1, 0x10

    .line 661
    const/4 v8, 0x1

    goto :goto_32d

    .line 662
    :cond_2ef
    sget-object p1, Ljje;->NOT_INSTALLED:Ljje;

    .line 664
    if-ne v0, p1, :cond_306

    .line 666
    const p1, 0x7f141417

    .line 669
    const/4 v8, 0x5

    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 672
    move-result-object p1

    .line 673
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 676
    move-result-wide v0

    .line 677
    const/4 v8, 0x5

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 680
    const/16 p1, 0x11

    .line 682
    goto :goto_32d

    .line 683
    :cond_306
    sget-object p1, Ljje;->NOT_RUNNING:Ljje;

    .line 685
    if-ne v0, p1, :cond_31c

    .line 687
    const p1, 0x7f141418

    .line 690
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 693
    move-result-object p1

    .line 694
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 697
    move-result-wide v0

    .line 698
    const/4 v8, 0x2

    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 701
    const/16 p1, 0x12

    .line 703
    goto :goto_32d

    .line 704
    :cond_31c
    const p1, 0x7f141416

    .line 707
    invoke-static {p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 710
    move-result-object p1

    .line 711
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 714
    move-result-wide v0

    .line 715
    invoke-static {v0, v1, p1}, Lkjf;->g(JLjava/lang/String;)V

    .line 718
    const/16 p1, 0x13

    .line 720
    :goto_32d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 723
    move-result-object v0

    .line 724
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 727
    move-result-object p0

    .line 728
    const/4 v8, 0x3

    invoke-static {v0, p0, v2, p1}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 731
    return v3

    .line 732
    :cond_33a
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresAllFilesAccess()Z

    .line 735
    move-result v0

    .line 736
    const/4 v8, 0x1

    if-eqz v0, :cond_35d

    .line 738
    const/16 v0, 0x1e

    .line 740
    const/4 v8, 0x6

    if-lt p1, v0, :cond_35d

    .line 742
    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    .line 745
    move-result p1

    .line 746
    const/4 v8, 0x0

    if-nez p1, :cond_35d

    .line 748
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 751
    move-result-object p1

    .line 752
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 755
    move-result-object v0

    .line 756
    const/4 v8, 0x3

    const/16 v4, 0x14

    .line 758
    const/4 v8, 0x4

    invoke-static {p1, v0, v2, v4}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 761
    :cond_35d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFileVersion()Landroid/util/Pair;

    .line 764
    move-result-object p1

    .line 765
    if-eqz p1, :cond_3f9

    .line 767
    iget-object v0, p1, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 769
    const/4 v8, 0x0

    check-cast v0, Ljava/lang/Integer;

    .line 771
    invoke-virtual {v0}, Ljava/lang/Integer;->intValue()I

    .line 774
    move-result v0

    .line 775
    const-string v2, "em.adbopa.crrrmor.tohcdfseolli"

    const-string v2, "com.arlosoft.macrodroid.helper"

    .line 777
    const/4 v8, 0x1

    invoke-static {v2}, Lgi0;->b(Ljava/lang/String;)I

    .line 780
    move-result v2

    .line 781
    const/4 v8, 0x6

    if-le v0, v2, :cond_3f9

    .line 783
    const/4 v8, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseConnectivityHelperApp()Landroid/util/Pair;

    .line 786
    move-result-object v0

    .line 787
    const/16 v2, 0xd

    .line 789
    const/4 v8, 0x2

    const-string v4, "+) must be installed to use this feature."

    .line 791
    const/4 v8, 0x1

    const-string v5, "(rocnMuvdo UsKrD  rPaeeviaHrle lAi"

    const-string v5, "MacroDroid Universal Helper APK (v"

    .line 793
    if-nez v0, :cond_3b3

    .line 795
    new-instance v0, Ljava/lang/StringBuilder;

    .line 797
    invoke-direct {v0, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 800
    iget-object v5, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 802
    const/4 v8, 0x4

    check-cast v5, Ljava/lang/String;

    .line 804
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 807
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 810
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 813
    move-result-object v0

    .line 814
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 817
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 820
    move-result-object v0

    .line 821
    const/4 v8, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 824
    move-result-object v4

    .line 825
    const/4 v8, 0x2

    iget-object p1, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 827
    const/4 v8, 0x3

    check-cast p1, Ljava/lang/String;

    .line 829
    invoke-static {v0, v4, p1, v2}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 832
    goto :goto_3f9

    .line 833
    :cond_3b3
    iget-object v6, v0, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 835
    check-cast v6, Ljava/lang/Integer;

    .line 837
    invoke-virtual {v6}, Ljava/lang/Integer;->intValue()I

    .line 840
    move-result v6

    .line 841
    const-string v7, "com.arlosoft.macrodroid.connectivityhelper"

    .line 843
    const/4 v8, 0x4

    invoke-static {v7}, Lgi0;->b(Ljava/lang/String;)I

    .line 846
    move-result v7

    .line 847
    if-le v6, v7, :cond_3f9

    .line 849
    new-instance v6, Ljava/lang/StringBuilder;

    .line 851
    invoke-direct {v6, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 854
    iget-object v5, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 856
    const/4 v8, 0x7

    check-cast v5, Ljava/lang/String;

    .line 858
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 861
    const-string v5, "+) or Connectivity Helper APK (v"

    .line 863
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 866
    iget-object v0, v0, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 868
    check-cast v0, Ljava/lang/String;

    .line 870
    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 873
    invoke-virtual {v6, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 876
    const/4 v8, 0x0

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 879
    move-result-object v0

    .line 880
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 883
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 886
    move-result-object v0

    .line 887
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 890
    move-result-object v4

    .line 891
    const/4 v8, 0x7

    iget-object p1, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    .line 893
    check-cast p1, Ljava/lang/String;

    .line 895
    const/4 v8, 0x0

    invoke-static {v0, v4, p1, v2}, Llob;->w(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;I)V

    .line 898
    :cond_3f9
    :goto_3f9
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 901
    move-result-object p1

    .line 902
    const/4 v8, 0x5

    if-eqz p1, :cond_43e

    .line 904
    array-length v0, p1

    .line 905
    move v2, v3

    .line 906
    :goto_402
    if-ge v2, v0, :cond_43e

    .line 908
    const/4 v8, 0x7

    aget-object v4, p1, v2

    .line 910
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 913
    move-result-object v5

    .line 914
    const/4 v8, 0x3

    invoke-static {v5, v4}, Lw63;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    .line 917
    move-result v5

    .line 918
    if-eqz v5, :cond_439

    .line 920
    new-instance p1, Ljava/lang/StringBuilder;

    .line 922
    const/4 v8, 0x2

    const-string v0, "Permission "

    .line 924
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 927
    invoke-virtual {p1, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 930
    const/4 v8, 0x5

    const-string v0, "n ner cpdMb a rrldoesDtfo ooai"

    const-string v0, " for MacroDroid is not enabled"

    .line 932
    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 935
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 938
    move-result-object p1

    .line 939
    invoke-static {p1}, Lkjf;->h(Ljava/lang/String;)V

    .line 942
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 945
    move-result-object p1

    .line 946
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 949
    move-result-object p0

    .line 950
    invoke-static {p1, v4, p0}, Llob;->v(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V

    .line 953
    const/4 v8, 0x2

    return v3

    .line 954
    :cond_439
    const/4 v8, 0x4

    add-int/lit8 v2, v2, 0x1

    .line 956
    const/4 v8, 0x7

    goto :goto_402

    .line 957
    :cond_43e
    :goto_43e
    return v1
.end method

.method public checkAndroidPermissionsAndSelectItem(Landroid/app/Activity;)V
    .locals 4

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 4
    move-result-object v0

    .line 5
    const/4 v3, 0x1

    array-length v1, v0

    .line 6
    const/4 v3, 0x1

    if-nez v1, :cond_d

    .line 8
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->handleItemSelectedSafe()V

    .line 11
    return-void

    .line 12
    :cond_d
    new-instance v1, Lspa;

    .line 14
    const/16 v2, 0xd

    .line 16
    invoke-direct {v1, v2, p0, v0}, Lspa;-><init>(ILjava/lang/Object;Ljava/lang/Object;)V

    .line 19
    invoke-static {p1, v0, v1}, Lrk5;->b(Landroid/app/Activity;[Ljava/lang/String;Lqk5;)V

    .line 22
    return-void
.end method

.method public checkOnImport()Z
    .locals 1

    .line 1
    const/4 v0, 0x0

    const/4 p0, 0x1

    .line 2
    return p0
.end method

.method public checkPermissionsOnConfigure()Z
    .locals 1

    .line 1
    const/4 v0, 0x3

    const/4 p0, 0x1

    .line 2
    return p0
.end method

.method public clearHasEdited()V
    .locals 2

    .line 1
    const/4 v1, 0x3

    const/4 v0, 0x0

    .line 2
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasEdited:Z

    .line 4
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasCommentEdited:Z

    .line 6
    const/4 v1, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 9
    move-result-object p0

    .line 10
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 13
    move-result-object p0

    .line 14
    :cond_f
    :goto_f
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 17
    move-result v0

    .line 18
    const/4 v1, 0x1

    if-eqz v0, :cond_24

    .line 20
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 23
    move-result-object v0

    .line 24
    const/4 v1, 0x2

    check-cast v0, Lcom/arlosoft/macrodroid/common/SelectableItem;

    .line 26
    const/4 v1, 0x7

    if-eqz v0, :cond_f

    .line 28
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->clearHasEdited()V

    .line 31
    goto :goto_f

    .line 32
    :cond_24
    return-void
.end method

.method public configureForExport()V
    .locals 1

    .line 1
    const/4 v0, 0x2

    return-void
.end method

.method public configureOnImport()V
    .locals 1

    .line 1
    return-void
.end method

.method public constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z
    .locals 2

    const/4 v0, 0x3

    const/4 v0, 0x0

    .line 370
    invoke-virtual {p0, p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Z)Z

    move-result p0

    return p0
.end method

.method public constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Z)Z
    .locals 3

    const/4 v2, 0x4

    const/4 v0, 0x1

    const/4 v2, 0x5

    const/4 v1, 0x0

    .line 368
    invoke-virtual {p0, p1, p2, v0, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZZZ)Z

    move-result p0

    return p0
.end method

.method public constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZZ)Z
    .locals 2

    const/4 v0, 0x0

    .line 369
    invoke-virtual {p0, p1, p2, p3, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZZZ)Z

    move-result p0

    const/4 v1, 0x7

    return p0
.end method

.method public constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZZZ)Z
    .locals 7

    .line 1
    const/4 v0, 0x0

    .line 2
    const/4 v6, 0x4

    if-nez p4, :cond_9

    .line 4
    iget-boolean p4, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 6
    if-eqz p4, :cond_9

    .line 8
    return v0

    .line 9
    :cond_9
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 12
    move-result-object p4

    .line 13
    const/4 v6, 0x0

    invoke-interface {p4}, Ljava/util/List;->size()I

    .line 16
    move-result p4

    .line 17
    const/4 v1, 0x1

    .line 18
    if-nez p4, :cond_16

    .line 20
    return v1

    .line 21
    :cond_16
    iget-boolean p4, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isOrCondition:Z

    .line 23
    const-string v2, ")"

    .line 25
    const/4 v3, 0x0

    .line 26
    if-nez p4, :cond_f5

    .line 28
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 31
    move-result-object p4

    .line 32
    invoke-interface {p4}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 35
    move-result-object p4

    .line 36
    :cond_25
    const/4 v6, 0x3

    invoke-interface {p4}, Ljava/util/Iterator;->hasNext()Z

    .line 39
    move-result v4

    .line 40
    if-eqz v4, :cond_f3

    .line 42
    invoke-interface {p4}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 45
    move-result-object v4

    .line 46
    const/4 v6, 0x3

    check-cast v4, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 48
    const/4 v6, 0x6

    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isEnabled()Z

    .line 51
    move-result v5

    .line 52
    if-eqz v5, :cond_25

    .line 54
    invoke-virtual {v4, p1}, Lcom/arlosoft/macrodroid/constraint/Constraint;->X(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z

    .line 57
    move-result v5

    .line 58
    const/4 v6, 0x3

    if-nez v5, :cond_25

    .line 60
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 63
    move-result-object p4

    .line 64
    if-eqz p4, :cond_52

    .line 66
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 69
    move-result-object p4

    .line 70
    const/4 v6, 0x2

    invoke-virtual {p4}, Lcom/arlosoft/macrodroid/macro/Macro;->isDetailLoggingExcluded()Z

    .line 73
    move-result p4

    .line 74
    if-nez p4, :cond_f1

    .line 76
    :cond_52
    const/4 v6, 0x5

    if-eqz p2, :cond_b5

    .line 78
    instance-of p2, p0, Lcom/arlosoft/macrodroid/action/ConditionAction;

    .line 80
    const/4 v6, 0x4

    if-eqz p2, :cond_64

    .line 82
    move-object p2, p0

    .line 83
    check-cast p2, Lcom/arlosoft/macrodroid/action/ConditionAction;

    .line 85
    const/4 v6, 0x5

    invoke-virtual {p2}, Lcom/arlosoft/macrodroid/action/ConditionAction;->Z()Z

    .line 88
    move-result p2

    .line 89
    if-nez p2, :cond_f1

    .line 91
    :cond_64
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 94
    move-result p2

    .line 95
    const/4 v6, 0x7

    if-nez p2, :cond_f1

    .line 97
    const/4 v6, 0x1

    if-eqz p3, :cond_f1

    .line 99
    new-instance p2, Ljava/lang/StringBuilder;

    .line 101
    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    .line 104
    const/4 v6, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getLogEntryStart()Ljava/lang/String;

    .line 107
    move-result-object p3

    .line 108
    const/4 v6, 0x2

    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 111
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 114
    move-result-object p1

    .line 115
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 118
    const/4 v6, 0x7

    const-string p1, " If condition failed: "

    .line 120
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 123
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 126
    move-result-object p1

    .line 127
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 130
    const-string p1, " ("

    const-string p1, " ("

    .line 132
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 135
    const/4 v6, 0x5

    iget-object p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 137
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/macro/Macro;->getName()Ljava/lang/String;

    .line 140
    move-result-object p1

    .line 141
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 144
    invoke-virtual {p2, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 147
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 150
    move-result-object p1

    .line 151
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 154
    move-result-object p0

    .line 155
    invoke-virtual {p0}, Ljava/lang/Long;->longValue()J

    .line 158
    move-result-wide p2

    .line 159
    const/4 v6, 0x3

    invoke-static {p1, v3, p2, p3}, Lkjf;->c(Ljava/lang/String;Ljava/lang/Integer;J)V

    .line 162
    goto :goto_f1

    .line 163
    :cond_b5
    const/4 v6, 0x4

    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 166
    move-result p2

    .line 167
    const/4 v6, 0x3

    if-nez p2, :cond_f1

    .line 169
    if-eqz p3, :cond_f1

    .line 171
    new-instance p2, Ljava/lang/StringBuilder;

    .line 173
    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    .line 176
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getLogEntryStart()Ljava/lang/String;

    .line 179
    move-result-object p3

    .line 180
    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 183
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 186
    move-result-object p3

    .line 187
    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 190
    const-string p3, "crootn aqvie n d  bfasleoediedk iitct :unsn"

    const-string p3, " did not invoke because constraint failed: "

    .line 192
    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 195
    invoke-virtual {v4, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 198
    move-result-object p1

    .line 199
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 202
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 205
    move-result-object p1

    .line 206
    const/4 v6, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 209
    move-result-object p0

    .line 210
    const/4 v6, 0x6

    invoke-virtual {p0}, Ljava/lang/Long;->longValue()J

    .line 213
    move-result-wide p2

    .line 214
    invoke-static {p1, v3, p2, p3}, Lkjf;->c(Ljava/lang/String;Ljava/lang/Integer;J)V

    .line 217
    :cond_f1
    :goto_f1
    const/4 v6, 0x0

    return v0

    .line 218
    :cond_f3
    const/4 v6, 0x1

    return v1

    .line 219
    :cond_f5
    const/4 v6, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 222
    move-result-object p2

    .line 223
    invoke-interface {p2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 226
    move-result-object p2

    .line 227
    move p4, v0

    .line 228
    :cond_ff
    invoke-interface {p2}, Ljava/util/Iterator;->hasNext()Z

    .line 231
    move-result v4

    .line 232
    const/4 v6, 0x5

    if-eqz v4, :cond_11d

    .line 234
    invoke-interface {p2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 237
    move-result-object v4

    .line 238
    check-cast v4, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 240
    const/4 v6, 0x2

    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isEnabled()Z

    .line 243
    move-result v5

    .line 244
    if-eqz v5, :cond_ff

    .line 246
    const/4 v6, 0x3

    add-int/lit8 p4, p4, 0x1

    .line 248
    invoke-virtual {v4, p1}, Lcom/arlosoft/macrodroid/constraint/Constraint;->X(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z

    .line 251
    move-result v4

    .line 252
    if-eqz v4, :cond_ff

    .line 254
    return v1

    .line 255
    :cond_11d
    if-lez p4, :cond_193

    .line 257
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 260
    move-result-object p2

    .line 261
    if-eqz p2, :cond_130

    .line 263
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 266
    move-result-object p2

    .line 267
    const/4 v6, 0x4

    invoke-virtual {p2}, Lcom/arlosoft/macrodroid/macro/Macro;->isDetailLoggingExcluded()Z

    .line 270
    move-result p2

    .line 271
    if-nez p2, :cond_193

    .line 273
    :cond_130
    const/4 v6, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 276
    move-result-object p2

    .line 277
    const/4 v6, 0x4

    invoke-interface {p2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 280
    move-result-object p2

    .line 281
    :cond_13a
    invoke-interface {p2}, Ljava/util/Iterator;->hasNext()Z

    .line 284
    move-result v4

    .line 285
    if-eqz v4, :cond_15b

    .line 287
    invoke-interface {p2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 290
    move-result-object v4

    .line 291
    check-cast v4, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 293
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 296
    move-result v4

    .line 297
    if-nez v4, :cond_193

    .line 299
    instance-of v4, p0, Lcom/arlosoft/macrodroid/action/ConditionAction;

    .line 301
    if-eqz v4, :cond_13a

    .line 303
    move-object v4, p0

    .line 304
    check-cast v4, Lcom/arlosoft/macrodroid/action/ConditionAction;

    .line 306
    invoke-virtual {v4}, Lcom/arlosoft/macrodroid/action/ConditionAction;->Z()Z

    .line 309
    move-result v4

    .line 310
    const/4 v6, 0x6

    if-eqz v4, :cond_13a

    .line 312
    goto :goto_193

    .line 313
    :cond_15b
    const/4 v6, 0x4

    if-eqz p3, :cond_193

    .line 315
    new-instance p2, Ljava/lang/StringBuilder;

    .line 317
    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    .line 320
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getLogEntryStart()Ljava/lang/String;

    .line 323
    move-result-object p3

    .line 324
    const/4 v6, 0x3

    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 327
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 330
    move-result-object p1

    .line 331
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 334
    const-string p1, " did not invoke because no constraints were true ("

    .line 336
    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 339
    const/4 v6, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 342
    move-result-object p1

    .line 343
    const/4 v6, 0x4

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 346
    invoke-virtual {p2, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 349
    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 352
    move-result-object p1

    .line 353
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 356
    move-result-object p0

    .line 357
    invoke-virtual {p0}, Ljava/lang/Long;->longValue()J

    .line 360
    move-result-wide p2

    .line 361
    const/4 v6, 0x2

    invoke-static {p1, v3, p2, p3}, Lkjf;->c(Ljava/lang/String;Ljava/lang/Integer;J)V

    .line 364
    :cond_193
    :goto_193
    if-gtz p4, :cond_196

    .line 366
    return v1

    .line 367
    :cond_196
    return v0
.end method

.method public describeContents()I
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public displaySafeSecondaryOptionsDialog()V
    .locals 2

    .line 1
    const/4 v1, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkActivityAlive()Z

    .line 4
    move-result v0

    .line 5
    if-eqz v0, :cond_b

    .line 7
    const/4 v1, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->displaySecondaryOptionsDialog()Lzo;

    .line 10
    :cond_b
    const/4 v1, 0x7

    return-void
.end method

.method public displaySecondaryOptionsDialog()Lzo;
    .locals 6

    .line 1
    const/4 v5, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->showSearchInSecondaryOptionsDialog()Z

    .line 4
    move-result v0

    .line 5
    const/4 v5, 0x2

    if-eqz v0, :cond_f

    .line 7
    const/4 v5, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->displaySecondaryOptionsDialogWithSearch()Lzo;

    .line 10
    move-result-object p0

    .line 11
    const/4 v5, 0x0

    return-object p0

    .line 12
    :cond_f
    const/4 v5, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptions()[Ljava/lang/String;

    .line 15
    move-result-object v0

    .line 16
    if-eqz v0, :cond_9b

    .line 18
    array-length v1, v0

    .line 19
    if-nez v1, :cond_1b

    .line 21
    goto/16 :goto_9b

    .line 22
    :cond_1b
    const/4 v5, 0x5

    new-instance v1, Lyo;

    .line 24
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 27
    move-result-object v2

    .line 28
    const/4 v5, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAlertDialogTheme()I

    .line 31
    move-result v3

    .line 32
    const/4 v5, 0x7

    invoke-direct {v1, v2, v3}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 35
    const/4 v5, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptionsTitle()Ljava/lang/String;

    .line 38
    move-result-object v2

    .line 39
    iget-object v3, v1, Lyo;->a:Lvo;

    .line 41
    iput-object v2, v3, Lvo;->e:Ljava/lang/CharSequence;

    .line 43
    const/4 v5, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getCheckedItemIndex()I

    .line 46
    move-result v2

    .line 47
    const/4 v5, 0x1

    new-instance v3, Ld2e;

    .line 49
    const/4 v4, 0x1

    .line 50
    invoke-direct {v3, v4, p0}, Ld2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 53
    invoke-virtual {v1, v0, v2, v3}, Lyo;->j([Ljava/lang/CharSequence;ILandroid/content/DialogInterface$OnClickListener;)V

    .line 56
    const/4 v5, 0x2

    new-instance v2, Ld2e;

    .line 58
    const/4 v3, 0x2

    .line 59
    invoke-direct {v2, v3, p0}, Ld2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 62
    const/high16 v3, 0x1040000

    .line 64
    invoke-virtual {v1, v3, v2}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 67
    new-instance v2, Ld2e;

    .line 69
    const/4 v5, 0x0

    const/4 v3, 0x3

    .line 70
    invoke-direct {v2, v3, p0}, Ld2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 73
    const/4 v5, 0x4

    const v3, 0x104000a

    .line 76
    invoke-virtual {v1, v3, v2}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 79
    const/4 v5, 0x0

    invoke-virtual {v1}, Lyo;->a()Lzo;

    .line 82
    move-result-object v1

    .line 83
    const/4 v5, 0x1

    invoke-virtual {v1}, Landroid/app/Dialog;->show()V

    .line 86
    const/4 v5, 0x1

    new-instance v2, Le2e;

    .line 88
    invoke-direct {v2, v4, p0}, Le2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 91
    invoke-virtual {v1, v2}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 94
    array-length v0, v0

    .line 95
    const/16 v2, 0x32

    .line 97
    if-le v0, v2, :cond_99

    .line 99
    iget-object v0, v1, Lzo;->g:Lxo;

    .line 101
    const/4 v5, 0x3

    iget-object v0, v0, Lxo;->f:Landroidx/appcompat/app/AlertController$RecycleListView;

    .line 103
    const/4 v5, 0x1

    invoke-virtual {v0, v4}, Landroid/widget/AbsListView;->setFastScrollEnabled(Z)V

    .line 106
    const/4 v5, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 109
    move-result-object p0

    .line 110
    invoke-virtual {p0}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    .line 113
    move-result-object p0

    .line 114
    const v2, 0x7f0700bf

    .line 117
    invoke-virtual {p0, v2}, Landroid/content/res/Resources;->getDimensionPixelSize(I)I

    .line 120
    move-result p0

    .line 121
    const/4 v5, 0x6

    const/4 v2, 0x0

    .line 122
    const/4 v5, 0x2

    invoke-virtual {v0, v2, v2, p0, v2}, Landroid/view/View;->setPadding(IIII)V

    .line 125
    const/high16 p0, 0x2000000

    .line 127
    const/4 v5, 0x4

    invoke-virtual {v0, p0}, Landroid/view/View;->setScrollBarStyle(I)V

    .line 130
    :cond_99
    const/4 v5, 0x0

    return-object v1

    .line 131
    :cond_9b
    :goto_9b
    const/4 v5, 0x6

    const/4 p0, 0x0

    .line 132
    const/4 v5, 0x2

    return-object p0
.end method

.method public displaySecondaryOptionsDialogWithSearch()Lzo;
    .locals 11

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptions()[Ljava/lang/String;

    .line 4
    move-result-object v3

    .line 5
    const/4 v0, 0x0

    .line 6
    if-eqz v3, :cond_d6

    .line 8
    const/4 v10, 0x6

    array-length v1, v3

    .line 9
    if-nez v1, :cond_d

    .line 11
    goto/16 :goto_d6

    .line 13
    :cond_d
    const-string v1, ""

    .line 15
    iput-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->oldSearchText:Ljava/lang/String;

    .line 17
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->searchSelectedIndexCache:Ljava/util/HashMap;

    .line 19
    invoke-virtual {v1}, Ljava/util/HashMap;->clear()V

    .line 22
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 25
    move-result-object v1

    .line 26
    const/4 v10, 0x3

    invoke-virtual {v1}, Landroid/app/Activity;->getLayoutInflater()Landroid/view/LayoutInflater;

    .line 29
    move-result-object v1

    .line 30
    const/4 v10, 0x1

    const v2, 0x7f0d0290

    .line 33
    invoke-virtual {v1, v2, v0}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    .line 36
    move-result-object v0

    .line 37
    const/4 v10, 0x3

    const v1, 0x7f0a0eea

    .line 40
    invoke-virtual {v0, v1}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    .line 43
    move-result-object v1

    .line 44
    move-object v6, v1

    .line 45
    check-cast v6, Landroid/widget/SearchView;

    .line 47
    const v1, 0x7f0a0a89

    .line 50
    const/4 v10, 0x0

    invoke-virtual {v0, v1}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    .line 53
    move-result-object v1

    .line 54
    move-object v2, v1

    .line 55
    const/4 v10, 0x1

    check-cast v2, Landroid/widget/ListView;

    .line 57
    new-instance v4, Lso;

    .line 59
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 62
    move-result-object v1

    .line 63
    const/4 v10, 0x2

    invoke-direct {v4, v1, v3}, Lso;-><init>(Landroid/content/ContextWrapper;[Ljava/lang/String;)V

    .line 66
    const/4 v10, 0x2

    invoke-virtual {v2, v4}, Landroid/widget/ListView;->setAdapter(Landroid/widget/ListAdapter;)V

    .line 69
    const/4 v7, 0x1

    move v10, v7

    .line 70
    invoke-virtual {v2, v7}, Landroid/widget/AbsListView;->setChoiceMode(I)V

    .line 73
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getCheckedItemIndex()I

    .line 76
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getCheckedItemIndex()I

    .line 79
    move-result v1

    .line 80
    invoke-virtual {v2, v1, v7}, Landroid/widget/AbsListView;->setItemChecked(IZ)V

    .line 83
    const/4 v10, 0x5

    new-instance v8, Lyo;

    .line 85
    const/4 v10, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 88
    move-result-object v1

    .line 89
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAlertDialogTheme()I

    .line 92
    move-result v5

    .line 93
    const/4 v10, 0x7

    invoke-direct {v8, v1, v5}, Lyo;-><init>(Landroid/content/Context;I)V

    .line 96
    const/4 v10, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptionsTitle()Ljava/lang/String;

    .line 99
    move-result-object v1

    .line 100
    iget-object v5, v8, Lyo;->a:Lvo;

    .line 102
    iput-object v1, v5, Lvo;->e:Ljava/lang/CharSequence;

    .line 104
    invoke-virtual {v8, v0}, Lyo;->m(Landroid/view/View;)V

    .line 107
    const/4 v10, 0x2

    new-instance v0, Ld2e;

    .line 109
    const/4 v9, 0x0

    or-int/2addr v10, v9

    .line 110
    invoke-direct {v0, v9, p0}, Ld2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 113
    const/4 v10, 0x2

    const/high16 v1, 0x1040000

    .line 115
    invoke-virtual {v8, v1, v0}, Lyo;->e(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 118
    new-instance v0, Lz4;

    .line 120
    const/4 v10, 0x5

    const/16 v5, 0xd

    .line 122
    move-object v1, p0

    move-object v1, p0

    .line 123
    invoke-direct/range {v0 .. v5}, Lz4;-><init>(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V

    .line 126
    const/4 v10, 0x5

    const p0, 0x104000a

    .line 129
    invoke-virtual {v8, p0, v0}, Lyo;->g(ILandroid/content/DialogInterface$OnClickListener;)Lyo;

    .line 132
    const/4 v10, 0x3

    invoke-virtual {v8}, Lyo;->a()Lzo;

    .line 135
    move-result-object p0

    .line 136
    invoke-virtual {p0}, Landroid/app/Dialog;->show()V

    .line 139
    invoke-static {p0, v9}, Lxje;->m(Landroid/app/Dialog;I)V

    .line 142
    const/4 v10, 0x7

    new-instance v0, Le2e;

    .line 144
    invoke-direct {v0, v9, v1}, Le2e;-><init>(ILcom/arlosoft/macrodroid/common/SelectableItem;)V

    .line 147
    const/4 v10, 0x5

    invoke-virtual {p0, v0}, Landroid/app/Dialog;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)V

    .line 150
    array-length v0, v3

    .line 151
    const/4 v10, 0x3

    const/16 v3, 0x32

    .line 153
    const/4 v10, 0x7

    if-le v0, v3, :cond_cd

    .line 155
    invoke-virtual {v2, v7}, Landroid/widget/AbsListView;->setFastScrollEnabled(Z)V

    .line 158
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 161
    move-result-object v0

    .line 162
    invoke-virtual {v0}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    .line 165
    move-result-object v0

    .line 166
    const v3, 0x7f0700bf

    .line 169
    invoke-virtual {v0, v3}, Landroid/content/res/Resources;->getDimensionPixelSize(I)I

    .line 172
    move-result v0

    .line 173
    const/4 v10, 0x3

    invoke-virtual {v2, v9, v9, v0, v9}, Landroid/view/View;->setPadding(IIII)V

    .line 176
    const/high16 v0, 0x2000000

    .line 178
    invoke-virtual {v2, v0}, Landroid/view/View;->setScrollBarStyle(I)V

    .line 181
    :cond_cd
    new-instance v0, Lcom/arlosoft/macrodroid/common/c;

    .line 183
    invoke-direct {v0, v1, v2, v4, p0}, Lcom/arlosoft/macrodroid/common/c;-><init>(Lcom/arlosoft/macrodroid/common/SelectableItem;Landroid/widget/ListView;Lso;Lzo;)V

    .line 186
    invoke-virtual {v6, v0}, Landroid/widget/SearchView;->setOnQueryTextListener(Landroid/widget/SearchView$OnQueryTextListener;)V

    .line 189
    return-object p0

    .line 190
    :cond_d6
    :goto_d6
    return-object v0
.end method

.method public doesSupportPreApply()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public forceRemoveConstraint(Lcom/arlosoft/macrodroid/constraint/Constraint;)V
    .locals 1

    .line 1
    const/4 v0, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x6

    invoke-interface {p0, p1}, Ljava/util/List;->remove(Ljava/lang/Object;)Z

    .line 8
    const/4 v0, 0x5

    return-void
.end method

.method public getActivity()Landroid/app/Activity;
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_activityRef:Ljava/lang/ref/WeakReference;

    .line 3
    const/4 v0, 0x5

    if-eqz p0, :cond_d

    .line 5
    const/4 v0, 0x6

    invoke-virtual {p0}, Ljava/lang/ref/Reference;->get()Ljava/lang/Object;

    .line 8
    move-result-object p0

    .line 9
    check-cast p0, Landroid/app/Activity;

    .line 11
    return-object p0

    .line 12
    :cond_d
    const/4 p0, 0x0

    .line 13
    return-object p0
.end method

.method public getAdbHackAdditionalCommands()Ljava/lang/String;
    .locals 1

    .line 1
    const/4 v0, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    invoke-virtual {p0}, Lk2e;->getAdbHackAdditionalCommands()Ljava/lang/String;

    .line 8
    move-result-object p0

    .line 9
    const/4 v0, 0x7

    return-object p0
.end method

.method public getAdbHackPermissionRequired()Ljava/util/List;
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x0

    invoke-virtual {p0}, Lk2e;->getAdbHackPermissionRequired()Ljava/util/List;

    .line 8
    move-result-object p0

    .line 9
    return-object p0
.end method

.method public getAlertDialogTheme()I
    .locals 1

    .line 1
    const/4 v0, 0x3

    const p0, 0x7f150337

    .line 4
    const/4 v0, 0x2

    return p0
.end method

.method public getAllArrayVariables()Ljava/util/ArrayList;
    .locals 6
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    const/4 v5, 0x0

    if-eqz p0, :cond_2a

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_12
    :goto_12
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    if-eqz v1, :cond_2a

    .line 24
    const/4 v5, 0x1

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 33
    move-result v2

    .line 34
    const/4 v5, 0x5

    if-eqz v2, :cond_12

    .line 36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 39
    goto :goto_12

    .line 40
    :cond_2a
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object p0

    .line 44
    const/4 v5, 0x1

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 47
    new-instance v1, Ljava/util/ArrayList;

    .line 49
    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V

    .line 52
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/a;->a:Lj$/util/concurrent/ConcurrentHashMap;

    .line 54
    const/4 v5, 0x3

    invoke-virtual {p0}, Lj$/util/concurrent/ConcurrentHashMap;->values()Ljava/util/Collection;

    .line 57
    move-result-object p0

    .line 58
    invoke-interface {p0}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    .line 61
    move-result-object p0

    .line 62
    :cond_42
    :goto_42
    const/4 v5, 0x4

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 65
    move-result v2

    .line 66
    const/4 v5, 0x5

    if-eqz v2, :cond_5c

    .line 68
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 71
    move-result-object v2

    .line 72
    check-cast v2, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 74
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->N()I

    .line 77
    move-result v3

    .line 78
    const/4 v5, 0x5

    const/4 v4, 0x5

    .line 79
    if-ne v3, v4, :cond_42

    .line 81
    invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 84
    goto :goto_42

    .line 85
    :cond_5c
    invoke-static {v1}, Lcom/arlosoft/macrodroid/common/a;->D(Ljava/util/ArrayList;)V

    .line 88
    const/4 v5, 0x7

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 91
    return-object v0
.end method

.method public getAllArrayVariablesIncludingWithChildren()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_34

    .line 10
    const/4 v3, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x3

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x0

    if-eqz v1, :cond_34

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    const/4 v3, 0x2

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 33
    move-result v2

    .line 34
    if-nez v2, :cond_2f

    .line 36
    const/4 v3, 0x4

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->s()Z

    .line 39
    move-result v2

    .line 40
    const/4 v3, 0x3

    if-eqz v2, :cond_13

    .line 42
    :cond_2f
    const/4 v3, 0x4

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 45
    goto :goto_13

    .line 46
    :cond_34
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 49
    move-result-object p0

    .line 50
    const/4 v1, 0x1

    .line 51
    const/4 v3, 0x6

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 54
    move-result-object p0

    .line 55
    invoke-virtual {p0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 58
    move-result-object p0

    .line 59
    :cond_42
    :goto_42
    const/4 v3, 0x5

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 62
    move-result v1

    .line 63
    if-eqz v1, :cond_61

    .line 65
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 68
    move-result-object v1

    .line 69
    const/4 v3, 0x3

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 71
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 74
    move-result v2

    .line 75
    const/4 v3, 0x3

    if-nez v2, :cond_5d

    .line 77
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->s()Z

    .line 80
    move-result v2

    .line 81
    if-eqz v2, :cond_42

    .line 83
    :cond_5d
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 86
    goto :goto_42

    .line 87
    :cond_61
    return-object v0
.end method

.method public getAllBooleanVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x2

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2c

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x7

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x5

    if-eqz v1, :cond_2c

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    const/4 v3, 0x5

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->b0()Z

    .line 33
    move-result v2

    .line 34
    const/4 v3, 0x7

    if-eqz v2, :cond_13

    .line 36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 39
    goto :goto_13

    .line 40
    :cond_2c
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object p0

    .line 44
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->g()Ljava/util/ArrayList;

    .line 47
    move-result-object p0

    .line 48
    const/4 v3, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 51
    return-object v0
.end method

.method public getAllColorVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x5

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    const/4 v3, 0x6

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2f

    .line 10
    const/4 v1, 0x0

    .line 11
    const/4 v3, 0x7

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSortedForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v3, 0x2

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 18
    move-result-object p0

    .line 19
    :cond_16
    :goto_16
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 22
    move-result v1

    .line 23
    const/4 v3, 0x2

    if-eqz v1, :cond_2f

    .line 25
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 28
    move-result-object v1

    .line 29
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 31
    const/4 v3, 0x4

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->e0()Z

    .line 34
    move-result v2

    .line 35
    if-eqz v2, :cond_16

    .line 37
    const/4 v3, 0x5

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 40
    goto :goto_16

    .line 41
    :cond_2f
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 44
    move-result-object p0

    .line 45
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->h()Ljava/util/ArrayList;

    .line 48
    move-result-object p0

    .line 49
    const/4 v3, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 52
    return-object v0
.end method

.method public getAllDecimalVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    const/4 v3, 0x5

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2a

    .line 10
    const/4 v3, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x0

    if-eqz v1, :cond_2a

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->f0()Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_13

    .line 36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 39
    goto :goto_13

    .line 40
    :cond_2a
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object p0

    .line 44
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->i()Ljava/util/ArrayList;

    .line 47
    move-result-object p0

    .line 48
    const/4 v3, 0x7

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 51
    return-object v0
.end method

.method public getAllDictionaryAndArrayVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    const/4 v3, 0x7

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    const/4 v3, 0x4

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_34

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    const/4 v3, 0x4

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    if-eqz v1, :cond_34

    .line 24
    const/4 v3, 0x7

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    const/4 v3, 0x3

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 33
    move-result v2

    .line 34
    const/4 v3, 0x2

    if-nez v2, :cond_30

    .line 36
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 39
    move-result v2

    .line 40
    const/4 v3, 0x6

    if-eqz v2, :cond_13

    .line 42
    :cond_30
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 45
    goto :goto_13

    .line 46
    :cond_34
    const/4 v3, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 49
    move-result-object p0

    .line 50
    const/4 v3, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->j()Ljava/util/ArrayList;

    .line 53
    move-result-object p0

    .line 54
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 57
    return-object v0
.end method

.method public getAllDictionaryOrArrayVariables(Z)Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(Z)",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x4

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_3c

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariables()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x1

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x3

    if-eqz v1, :cond_3c

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    const/4 v3, 0x1

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    const/4 v3, 0x6

    if-eqz p1, :cond_2e

    .line 32
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 35
    move-result v2

    .line 36
    if-eqz v2, :cond_2e

    .line 38
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 41
    goto :goto_13

    .line 42
    :cond_2e
    const/4 v3, 0x7

    if-nez p1, :cond_13

    .line 44
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 47
    move-result v2

    .line 48
    if-nez v2, :cond_13

    .line 50
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 53
    const/4 v3, 0x0

    goto :goto_13

    .line 54
    :cond_3c
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 57
    move-result-object p0

    .line 58
    const/4 v3, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->j()Ljava/util/ArrayList;

    .line 61
    move-result-object p0

    .line 62
    const/4 v3, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 65
    return-object v0
.end method

.method public getAllDictionaryVariables()Ljava/util/ArrayList;
    .locals 6
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_30

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v5, 0x1

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_12
    :goto_12
    const/4 v5, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    if-eqz v1, :cond_30

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_12

    .line 36
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 39
    move-result v2

    .line 40
    if-nez v2, :cond_12

    .line 42
    const/4 v5, 0x0

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 45
    goto :goto_12

    .line 46
    :cond_30
    const/4 v5, 0x7

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 49
    move-result-object p0

    .line 50
    const/4 v5, 0x5

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 53
    new-instance v1, Ljava/util/ArrayList;

    .line 55
    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V

    .line 58
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/a;->a:Lj$/util/concurrent/ConcurrentHashMap;

    .line 60
    invoke-virtual {p0}, Lj$/util/concurrent/ConcurrentHashMap;->values()Ljava/util/Collection;

    .line 63
    move-result-object p0

    .line 64
    const/4 v5, 0x5

    invoke-interface {p0}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    .line 67
    move-result-object p0

    .line 68
    :cond_49
    :goto_49
    const/4 v5, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 71
    move-result v2

    .line 72
    if-eqz v2, :cond_62

    .line 74
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 77
    move-result-object v2

    .line 78
    check-cast v2, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 80
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->N()I

    .line 83
    move-result v3

    .line 84
    const/4 v4, 0x0

    const/4 v4, 0x4

    .line 85
    if-ne v3, v4, :cond_49

    .line 87
    invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 90
    goto :goto_49

    .line 91
    :cond_62
    invoke-static {v1}, Lcom/arlosoft/macrodroid/common/a;->D(Ljava/util/ArrayList;)V

    .line 94
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 97
    return-object v0
.end method

.method public getAllDictionaryVariablesIncludingWithChildren()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_3a

    .line 10
    const/4 v3, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x7

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_13
    :goto_13
    const/4 v3, 0x1

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x5

    if-eqz v1, :cond_3a

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    const/4 v3, 0x2

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_2f

    .line 36
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 39
    move-result v2

    .line 40
    const/4 v3, 0x0

    if-eqz v2, :cond_36

    .line 42
    :cond_2f
    const/4 v3, 0x5

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->w()Z

    .line 45
    move-result v2

    .line 46
    if-eqz v2, :cond_13

    .line 48
    :cond_36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 51
    goto :goto_13

    .line 52
    :cond_3a
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 55
    move-result-object p0

    .line 56
    const/4 v3, 0x2

    const/4 v1, 0x1

    .line 57
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 60
    move-result-object p0

    .line 61
    const/4 v3, 0x1

    invoke-virtual {p0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 64
    move-result-object p0

    .line 65
    :cond_49
    :goto_49
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 68
    move-result v1

    .line 69
    if-eqz v1, :cond_6f

    .line 71
    const/4 v3, 0x5

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 74
    move-result-object v1

    .line 75
    const/4 v3, 0x2

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 77
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 80
    move-result v2

    .line 81
    if-eqz v2, :cond_63

    .line 83
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 86
    move-result v2

    .line 87
    if-eqz v2, :cond_69

    .line 89
    :cond_63
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->w()Z

    .line 92
    move-result v2

    .line 93
    if-eqz v2, :cond_49

    .line 95
    :cond_69
    const/4 v3, 0x5

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 98
    const/4 v3, 0x7

    goto :goto_49

    .line 99
    :cond_6f
    return-object v0
.end method

.method public getAllInputStringVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2c

    .line 10
    const/4 v3, 0x3

    const/4 v1, 0x1

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSortedForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 18
    move-result-object p0

    .line 19
    :cond_13
    :goto_13
    const/4 v3, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 22
    move-result v1

    .line 23
    if-eqz v1, :cond_2c

    .line 25
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 28
    move-result-object v1

    .line 29
    const/4 v3, 0x6

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 31
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->k0()Z

    .line 34
    move-result v2

    .line 35
    const/4 v3, 0x0

    if-eqz v2, :cond_13

    .line 37
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 40
    goto :goto_13

    .line 41
    :cond_2c
    const/4 v3, 0x6

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 44
    move-result-object p0

    .line 45
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->m()Ljava/util/ArrayList;

    .line 48
    move-result-object p0

    .line 49
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 52
    const/4 v3, 0x1

    return-object v0
.end method

.method public getAllInputVariables()Ljava/util/ArrayList;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v2, 0x1

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    const/4 v1, 0x1

    .line 9
    if-eqz p0, :cond_14

    .line 11
    const/4 v2, 0x4

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v2, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_14
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v2, 0x3

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 25
    move-result-object p0

    .line 26
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 29
    return-object v0
.end method

.method public getAllIntegerVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x2

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    const/4 v3, 0x0

    if-eqz p0, :cond_2e

    .line 10
    const/4 v3, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x2

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_15
    :goto_15
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    const/4 v3, 0x3

    if-eqz v1, :cond_2e

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    const/4 v3, 0x6

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->h0()Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_15

    .line 36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 39
    const/4 v3, 0x4

    goto :goto_15

    .line 40
    :cond_2e
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object p0

    .line 44
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->k()Ljava/util/ArrayList;

    .line 47
    move-result-object p0

    .line 48
    const/4 v3, 0x5

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 51
    const/4 v3, 0x0

    return-object v0
.end method

.method public getAllOutputBooleanVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2d

    .line 10
    const/4 v1, 0x0

    .line 11
    const/4 v3, 0x1

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSortedForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 18
    move-result-object p0

    .line 19
    :cond_13
    :goto_13
    const/4 v3, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 22
    move-result v1

    .line 23
    if-eqz v1, :cond_2d

    .line 25
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 28
    move-result-object v1

    .line 29
    const/4 v3, 0x0

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 31
    const/4 v3, 0x5

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->b0()Z

    .line 34
    move-result v2

    .line 35
    const/4 v3, 0x7

    if-eqz v2, :cond_13

    .line 37
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 40
    goto :goto_13

    .line 41
    :cond_2d
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 44
    move-result-object p0

    .line 45
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->g()Ljava/util/ArrayList;

    .line 48
    move-result-object p0

    .line 49
    const/4 v3, 0x0

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 52
    return-object v0
.end method

.method public getAllOutputDictionaryAndArrayVariableValues()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x3

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    const/4 v3, 0x4

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_46

    .line 10
    const/4 v3, 0x5

    const/4 v1, 0x0

    .line 11
    const/4 v3, 0x2

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSortedForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v3, 0x5

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 18
    move-result-object p0

    .line 19
    :cond_17
    :goto_17
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 22
    move-result v1

    .line 23
    const/4 v3, 0x6

    if-eqz v1, :cond_46

    .line 25
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 28
    move-result-object v1

    .line 29
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 31
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 34
    move-result v2

    .line 35
    if-nez v2, :cond_30

    .line 37
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 40
    move-result v2

    .line 41
    if-eqz v2, :cond_17

    .line 43
    :cond_30
    const/4 v3, 0x0

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->m()Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 46
    move-result-object v2

    .line 47
    invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 50
    new-instance v2, Ljava/util/ArrayList;

    .line 52
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 55
    const/4 v3, 0x3

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->m()Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 58
    move-result-object v1

    .line 59
    invoke-static {v1, v0, v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->P(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/util/ArrayList;Ljava/util/ArrayList;)V

    .line 62
    goto :goto_17

    .line 63
    :cond_46
    return-object v0
.end method

.method public getAllOutputStringVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2b

    .line 10
    const/4 v3, 0x1

    const/4 v1, 0x0

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSortedForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 18
    move-result-object p0

    .line 19
    :cond_13
    :goto_13
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 22
    move-result v1

    .line 23
    if-eqz v1, :cond_2b

    .line 25
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 28
    move-result-object v1

    .line 29
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 31
    const/4 v3, 0x5

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->k0()Z

    .line 34
    move-result v2

    .line 35
    const/4 v3, 0x6

    if-eqz v2, :cond_13

    .line 37
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 40
    goto :goto_13

    .line 41
    :cond_2b
    const/4 v3, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 44
    move-result-object p0

    .line 45
    const/4 v3, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->m()Ljava/util/ArrayList;

    .line 48
    move-result-object p0

    .line 49
    const/4 v3, 0x7

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 52
    return-object v0
.end method

.method public getAllOutputVariables()Ljava/util/ArrayList;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v2, 0x5

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    const/4 v2, 0x0

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    const/4 v2, 0x7

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_15

    .line 10
    const/4 v1, 0x0

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v2, 0x2

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_15
    const/4 v2, 0x5

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v1, 0x1

    .line 23
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    return-object v0
.end method

.method public getAllOutputVariablesWithBooleans()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    const/4 v3, 0x5

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_14

    .line 10
    const/4 v3, 0x7

    const/4 v1, 0x0

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v3, 0x7

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_14
    const/4 v3, 0x2

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v1, 0x1

    .line 23
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    const/4 v3, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    const/4 v3, 0x2

    new-instance p0, Ljava/util/ArrayList;

    .line 32
    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 35
    const/4 v3, 0x1

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 38
    move-result-object v0

    .line 39
    :cond_2d
    :goto_2d
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 42
    move-result v1

    .line 43
    if-eqz v1, :cond_52

    .line 45
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 48
    move-result-object v1

    .line 49
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    const/4 v3, 0x4

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->b0()Z

    .line 54
    move-result v2

    .line 55
    if-nez v2, :cond_4d

    .line 57
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 60
    move-result v2

    .line 61
    if-nez v2, :cond_4d

    .line 63
    const/4 v3, 0x4

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 66
    move-result v2

    .line 67
    if-eqz v2, :cond_2d

    .line 69
    :cond_4d
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 72
    const/4 v3, 0x6

    goto :goto_2d

    .line 73
    :cond_52
    return-object p0
.end method

.method public getAllOutputVariablesWithColors()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_13

    .line 10
    const/4 v3, 0x3

    const/4 v1, 0x0

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v3, 0x1

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_13
    const/4 v3, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v1, 0x1

    .line 23
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    const/4 v3, 0x0

    new-instance p0, Ljava/util/ArrayList;

    .line 32
    const/4 v3, 0x3

    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 35
    const/4 v3, 0x6

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 38
    move-result-object v0

    .line 39
    :cond_2c
    :goto_2c
    const/4 v3, 0x2

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 42
    move-result v1

    .line 43
    if-eqz v1, :cond_59

    .line 45
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 48
    move-result-object v1

    .line 49
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    const/4 v3, 0x1

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->e0()Z

    .line 54
    move-result v2

    .line 55
    const/4 v3, 0x3

    if-nez v2, :cond_55

    .line 57
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 60
    move-result v2

    .line 61
    const/4 v3, 0x5

    if-nez v2, :cond_4f

    .line 63
    const/4 v3, 0x6

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 66
    move-result v2

    .line 67
    if-eqz v2, :cond_2c

    .line 69
    :cond_4f
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->u()Z

    .line 72
    move-result v2

    .line 73
    if-eqz v2, :cond_2c

    .line 75
    :cond_55
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 78
    goto :goto_2c

    .line 79
    :cond_59
    const/4 v3, 0x2

    return-object p0
.end method

.method public getAllOutputVariablesWithDecimals()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v3, 0x6

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_13

    .line 10
    const/4 v1, 0x0

    shr-int/2addr v3, v1

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_13
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v1, 0x1

    .line 23
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    const/4 v3, 0x6

    new-instance p0, Ljava/util/ArrayList;

    .line 32
    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 35
    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 38
    move-result-object v0

    .line 39
    :cond_29
    :goto_29
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 42
    move-result v1

    .line 43
    const/4 v3, 0x2

    if-eqz v1, :cond_4f

    .line 45
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 48
    move-result-object v1

    .line 49
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    const/4 v3, 0x1

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->f0()Z

    .line 54
    move-result v2

    .line 55
    if-nez v2, :cond_4b

    .line 57
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 60
    move-result v2

    .line 61
    const/4 v3, 0x0

    if-nez v2, :cond_4b

    .line 63
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 66
    move-result v2

    .line 67
    const/4 v3, 0x4

    if-eqz v2, :cond_29

    .line 69
    :cond_4b
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 72
    goto :goto_29

    .line 73
    :cond_4f
    return-object p0
.end method

.method public getAllOutputVariablesWithIntegers()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_13

    .line 10
    const/4 v3, 0x4

    const/4 v1, 0x0

    .line 11
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    const/4 v3, 0x3

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_13
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v3, 0x7

    const/4 v1, 0x1

    .line 23
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    const/4 v3, 0x4

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    new-instance p0, Ljava/util/ArrayList;

    .line 32
    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 35
    const/4 v3, 0x0

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 38
    move-result-object v0

    .line 39
    :cond_2b
    :goto_2b
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 42
    move-result v1

    .line 43
    const/4 v3, 0x0

    if-eqz v1, :cond_51

    .line 45
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 48
    move-result-object v1

    .line 49
    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    const/4 v3, 0x6

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->h0()Z

    .line 54
    move-result v2

    .line 55
    if-nez v2, :cond_4c

    .line 57
    const/4 v3, 0x6

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 60
    move-result v2

    .line 61
    if-nez v2, :cond_4c

    .line 63
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 66
    move-result v2

    .line 67
    if-eqz v2, :cond_2b

    .line 69
    :cond_4c
    const/4 v3, 0x2

    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 72
    goto :goto_2b

    .line 73
    :cond_51
    return-object p0
.end method

.method public getAllOutputVariablesWithStrings()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    const/4 v3, 0x1

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_14

    .line 10
    const/4 v1, 0x2

    const/4 v1, 0x0

    .line 11
    const/4 v3, 0x7

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesForDirection(Z)Ljava/util/List;

    .line 14
    move-result-object p0

    .line 15
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 18
    :cond_14
    const/4 v3, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 21
    move-result-object p0

    .line 22
    const/4 v3, 0x6

    const/4 v1, 0x1

    .line 23
    const/4 v3, 0x5

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 26
    move-result-object p0

    .line 27
    const/4 v3, 0x1

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 30
    new-instance p0, Ljava/util/ArrayList;

    .line 32
    const/4 v3, 0x2

    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 35
    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 38
    move-result-object v0

    .line 39
    :cond_2e
    :goto_2e
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 42
    move-result v1

    .line 43
    if-eqz v1, :cond_53

    .line 45
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 48
    move-result-object v1

    .line 49
    const/4 v3, 0x6

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->k0()Z

    .line 54
    move-result v2

    .line 55
    if-nez v2, :cond_4f

    .line 57
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->g0()Z

    .line 60
    move-result v2

    .line 61
    const/4 v3, 0x5

    if-nez v2, :cond_4f

    .line 63
    const/4 v3, 0x5

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->a0()Z

    .line 66
    move-result v2

    .line 67
    if-eqz v2, :cond_2e

    .line 69
    :cond_4f
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 72
    goto :goto_2e

    .line 73
    :cond_53
    return-object p0
.end method

.method public getAllStringVariables()Ljava/util/ArrayList;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_2a

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    const/4 v3, 0x3

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 17
    move-result-object p0

    .line 18
    :cond_12
    :goto_12
    const/4 v3, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 21
    move-result v1

    .line 22
    if-eqz v1, :cond_2a

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    const/4 v3, 0x5

    check-cast v1, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 30
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->k0()Z

    .line 33
    move-result v2

    .line 34
    if-eqz v2, :cond_12

    .line 36
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 39
    goto :goto_12

    .line 40
    :cond_2a
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 43
    move-result-object p0

    .line 44
    const/4 v3, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/a;->m()Ljava/util/ArrayList;

    .line 47
    move-result-object p0

    .line 48
    const/4 v3, 0x0

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 51
    return-object v0
.end method

.method public getAllVariables()Ljava/util/ArrayList;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/ArrayList<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 8
    if-eqz p0, :cond_10

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariablesSorted()Ljava/util/List;

    .line 13
    move-result-object p0

    .line 14
    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 17
    :cond_10
    const/4 v2, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 20
    move-result-object p0

    .line 21
    const/4 v1, 0x1

    .line 22
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/a;->o(Z)Ljava/util/ArrayList;

    .line 25
    move-result-object p0

    .line 26
    const/4 v2, 0x0

    invoke-virtual {v0, p0}, Ljava/util/ArrayList;->addAll(Ljava/util/Collection;)Z

    .line 29
    return-object v0
.end method

.method public getAppCompatActivity()Landroidx/appcompat/app/AppCompatActivity;
    .locals 1

    .line 1
    const/4 v0, 0x4

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_activityRef:Ljava/lang/ref/WeakReference;

    .line 3
    if-eqz p0, :cond_d

    .line 5
    invoke-virtual {p0}, Ljava/lang/ref/Reference;->get()Ljava/lang/Object;

    .line 8
    move-result-object p0

    .line 9
    const/4 v0, 0x3

    check-cast p0, Landroidx/appcompat/app/AppCompatActivity;

    .line 11
    return-object p0

    .line 12
    :cond_d
    const/4 v0, 0x7

    const/4 p0, 0x0

    .line 13
    const/4 v0, 0x3

    return-object p0
.end method

.method public getCheckedItemIndex()I
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public getCollapsedName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x5

    return-object p0
.end method

.method public getComment()Ljava/lang/String;
    .locals 1

    .line 1
    const/4 v0, 0x1

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 3
    const/4 v0, 0x7

    return-object p0
.end method

.method public getConfiguredName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getConfiguredNameFlowControl()Ljava/lang/String;
    .locals 1

    .line 1
    const/4 v0, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getListModeName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getConstraintIsOrCondition()Z
    .locals 1

    .line 1
    const/4 v0, 0x1

    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isOrCondition:Z

    .line 3
    const/4 v0, 0x3

    return p0
.end method

.method public getConstraints()Ljava/util/List;
    .locals 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/arlosoft/macrodroid/constraint/Constraint;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 3
    if-nez v0, :cond_d

    .line 5
    new-instance v0, Ljava/util/ArrayList;

    .line 7
    const/4 v1, 0x0

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 10
    const/4 v1, 0x3

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 12
    :cond_d
    return-object v0
.end method

.method public getContext()Landroid/content/Context;
    .locals 1

    .line 1
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x3

    return-object p0
.end method

.method public getDescriptionDrawable()Landroid/graphics/drawable/Drawable;
    .locals 1

    .line 1
    const/4 v0, 0x0

    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x3

    return-object p0
.end method

.method public getDialogTheme()I
    .locals 1

    .line 1
    const/4 v0, 0x3

    const p0, 0x7f150337

    .line 4
    return p0
.end method

.method public getEditMacroConfiguredName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getEditModeAdvisory()Ljava/lang/String;
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return-object p0
.end method

.method public getEditModeWarning()Ljava/lang/String;
    .locals 7

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object v0

    .line 5
    const/4 v6, 0x1

    invoke-virtual {v0}, Lk2e;->minSDKVersion()I

    .line 8
    move-result v0

    .line 9
    const/4 v6, 0x4

    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 11
    const/4 v6, 0x5

    const/4 v2, 0x0

    .line 12
    const/4 v6, 0x3

    if-le v0, v1, :cond_e0

    .line 14
    const v0, 0x7f140bbc

    .line 17
    invoke-static {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 20
    move-result-object v0

    .line 21
    const/4 v6, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 24
    move-result-object p0

    .line 25
    const/4 v6, 0x6

    invoke-virtual {p0}, Lk2e;->minSDKVersion()I

    .line 28
    move-result p0

    .line 29
    const/4 v6, 0x4

    sget v1, Ll20;->a:I

    .line 31
    packed-switch p0, :pswitch_data_1ae

    .line 34
    invoke-static {p0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    .line 37
    move-result-object p0

    .line 38
    goto/16 :goto_d5

    .line 40
    :pswitch_2e
    const-string p0, "17"

    .line 42
    const/4 v6, 0x5

    goto/16 :goto_d5

    .line 44
    :pswitch_33
    const-string p0, "16"

    .line 46
    const/4 v6, 0x6

    goto/16 :goto_d5

    .line 48
    :pswitch_38
    const-string p0, "51"

    const-string p0, "15"

    .line 50
    goto/16 :goto_d5

    .line 52
    :pswitch_3e
    const-string p0, "41"

    const-string p0, "14"

    .line 54
    goto/16 :goto_d5

    .line 56
    :pswitch_44
    const/4 v6, 0x5

    const-string p0, "13"

    .line 58
    goto/16 :goto_d5

    .line 60
    :pswitch_49
    const/4 v6, 0x2

    const-string p0, "12"

    .line 62
    goto/16 :goto_d5

    .line 64
    :pswitch_4e
    const-string p0, "11"

    const-string p0, "11"

    .line 66
    goto/16 :goto_d5

    .line 68
    :pswitch_54
    const/4 v6, 0x5

    const-string p0, "10"

    .line 70
    goto/16 :goto_d5

    .line 72
    :pswitch_59
    const-string p0, "9"

    .line 74
    goto/16 :goto_d5

    .line 76
    :pswitch_5d
    const-string p0, "8.1"

    .line 78
    const/4 v6, 0x1

    goto/16 :goto_d5

    .line 80
    :pswitch_62
    const/4 v6, 0x6

    const-string p0, "8.0"

    .line 82
    goto :goto_d5

    .line 83
    :pswitch_66
    const-string p0, "71."

    const-string p0, "7.1"

    .line 85
    const/4 v6, 0x2

    goto :goto_d5

    .line 86
    :pswitch_6c
    const/4 v6, 0x7

    const-string p0, "7.0"

    .line 88
    const/4 v6, 0x6

    goto :goto_d5

    .line 89
    :pswitch_71
    const-string p0, "6.0"

    const-string p0, "6.0"

    .line 91
    goto :goto_d5

    .line 92
    :pswitch_76
    const-string p0, "5.1"

    .line 94
    goto :goto_d5

    .line 95
    :pswitch_79
    const/4 v6, 0x2

    const-string p0, "5.0"

    .line 97
    goto :goto_d5

    .line 98
    :pswitch_7d
    const/4 v6, 0x0

    const-string p0, "4.4W"

    .line 100
    goto :goto_d5

    .line 101
    :pswitch_81
    const/4 v6, 0x2

    const-string p0, "4.4"

    .line 103
    goto :goto_d5

    .line 104
    :pswitch_85
    const-string p0, "4.3"

    .line 106
    const/4 v6, 0x3

    goto :goto_d5

    .line 107
    :pswitch_89
    const/4 v6, 0x7

    const-string p0, "4.2"

    .line 109
    goto :goto_d5

    .line 110
    :pswitch_8d
    const-string p0, "4.1"

    const-string p0, "4.1"

    .line 112
    const/4 v6, 0x7

    goto :goto_d5

    .line 113
    :pswitch_93
    const-string p0, ".0s.4"

    const-string p0, "4.0.3"

    .line 115
    goto :goto_d5

    .line 116
    :pswitch_98
    const-string p0, "4.0"

    .line 118
    goto :goto_d5

    .line 119
    :pswitch_9b
    const-string p0, "3.2"

    .line 121
    const/4 v6, 0x6

    goto :goto_d5

    .line 122
    :pswitch_9f
    const-string p0, "3.1"

    .line 124
    goto :goto_d5

    .line 125
    :pswitch_a2
    const-string p0, ".30"

    const-string p0, "3.0"

    .line 127
    const/4 v6, 0x3

    goto :goto_d5

    .line 128
    :pswitch_a8
    const-string p0, ".3.m2"

    const-string p0, "2.3.3"

    .line 130
    goto :goto_d5

    .line 131
    :pswitch_ad
    const/4 v6, 0x0

    const-string p0, "2.3"

    .line 133
    goto :goto_d5

    .line 134
    :pswitch_b1
    const-string p0, "22."

    const-string p0, "2.2"

    .line 136
    goto :goto_d5

    .line 137
    :pswitch_b6
    const-string p0, ".12"

    const-string p0, "2.1"

    .line 139
    goto :goto_d5

    .line 140
    :pswitch_bb
    const-string p0, "2.0.1"

    .line 142
    const/4 v6, 0x3

    goto :goto_d5

    .line 143
    :pswitch_bf
    const-string p0, "20."

    const-string p0, "2.0"

    .line 145
    const/4 v6, 0x3

    goto :goto_d5

    .line 146
    :pswitch_c5
    const-string p0, "1.6"

    .line 148
    goto :goto_d5

    .line 149
    :pswitch_c8
    const-string p0, "1.5"

    .line 151
    goto :goto_d5

    .line 152
    :pswitch_cb
    const/4 v6, 0x0

    const-string p0, ".11"

    const-string p0, "1.1"

    .line 154
    goto :goto_d5

    .line 155
    :pswitch_d1
    const-string p0, ".01"

    const-string p0, "1.0"

    .line 157
    :goto_d5
    const/4 v1, 0x1

    .line 158
    new-array v1, v1, [Ljava/lang/Object;

    .line 160
    const/4 v6, 0x3

    aput-object p0, v1, v2

    .line 162
    invoke-static {v0, v1}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 165
    move-result-object p0

    .line 166
    return-object p0

    .line 167
    :cond_e0
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 169
    const/4 v6, 0x3

    const/4 v1, 0x0

    .line 170
    const/4 v6, 0x2

    if-eqz v0, :cond_188

    .line 172
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/macro/Macro;->isCompleted()Z

    .line 175
    move-result v0

    .line 176
    if-nez v0, :cond_f0

    .line 178
    const/4 v6, 0x6

    goto/16 :goto_188

    .line 180
    :cond_f0
    instance-of v0, p0, Ly57;

    .line 182
    const/4 v6, 0x0

    if-eqz v0, :cond_115

    .line 184
    move-object v0, p0

    .line 185
    const/4 v6, 0x1

    check-cast v0, Ly57;

    .line 187
    invoke-interface {v0}, Ly57;->r()Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 190
    move-result-object v0

    .line 191
    const/4 v6, 0x7

    if-eqz v0, :cond_115

    .line 193
    const/4 v6, 0x7

    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 196
    move-result-object v3

    .line 197
    invoke-virtual {p0, v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->Q(Ljava/lang/String;)Z

    .line 200
    move-result v3

    .line 201
    const/4 v6, 0x0

    if-eqz v3, :cond_115

    .line 203
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 206
    move-result-object p0

    .line 207
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 210
    move-result-object p0

    .line 211
    goto :goto_189

    .line 212
    :cond_115
    instance-of v0, p0, Lb67;

    .line 214
    if-eqz v0, :cond_14a

    .line 216
    move-object v0, p0

    .line 217
    check-cast v0, Lb67;

    .line 219
    const/4 v6, 0x5

    invoke-interface {v0}, Lb67;->i()Ljava/util/ArrayList;

    .line 222
    move-result-object v0

    .line 223
    const/4 v6, 0x4

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 226
    move-result-object v0

    .line 227
    :cond_126
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 230
    move-result v3

    .line 231
    const/4 v6, 0x7

    if-eqz v3, :cond_14a

    .line 233
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 236
    move-result-object v3

    .line 237
    check-cast v3, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 239
    if-eqz v3, :cond_126

    .line 241
    const/4 v6, 0x1

    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 244
    move-result-object v4

    .line 245
    const/4 v6, 0x3

    invoke-virtual {p0, v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->Q(Ljava/lang/String;)Z

    .line 248
    move-result v4

    .line 249
    if-eqz v4, :cond_126

    .line 251
    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 254
    move-result-object p0

    .line 255
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 258
    move-result-object p0

    .line 259
    goto :goto_189

    .line 260
    :cond_14a
    instance-of v0, p0, Lz57;

    .line 262
    if-eqz v0, :cond_164

    .line 264
    move-object v0, p0

    .line 265
    const/4 v6, 0x6

    check-cast v0, Lz57;

    .line 267
    const/4 v6, 0x1

    invoke-interface {v0}, Lz57;->k()Ljava/lang/String;

    .line 270
    move-result-object v0

    .line 271
    const/4 v6, 0x0

    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->Q(Ljava/lang/String;)Z

    .line 274
    move-result v3

    .line 275
    if-eqz v3, :cond_164

    .line 277
    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 280
    move-result-object p0

    .line 281
    const/4 v6, 0x5

    goto :goto_189

    .line 282
    :cond_164
    instance-of v0, p0, La67;

    .line 284
    if-eqz v0, :cond_188

    .line 286
    move-object v0, p0

    move-object v0, p0

    .line 287
    const/4 v6, 0x7

    check-cast v0, La67;

    .line 289
    invoke-interface {v0}, La67;->getVariableNames()[Ljava/lang/String;

    .line 292
    move-result-object v0

    .line 293
    const/4 v6, 0x1

    if-eqz v0, :cond_188

    .line 295
    array-length v3, v0

    .line 296
    :goto_175
    if-ge v2, v3, :cond_188

    .line 298
    aget-object v4, v0, v2

    .line 300
    const/4 v6, 0x4

    invoke-virtual {p0, v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->Q(Ljava/lang/String;)Z

    .line 303
    move-result v5

    .line 304
    if-eqz v5, :cond_185

    .line 306
    invoke-virtual {v4}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 309
    move-result-object p0

    .line 310
    goto :goto_189

    .line 311
    :cond_185
    add-int/lit8 v2, v2, 0x1

    .line 313
    goto :goto_175

    .line 314
    :cond_188
    :goto_188
    move-object p0, v1

    .line 315
    :goto_189
    if-eqz p0, :cond_1ad

    .line 317
    new-instance v0, Ljava/lang/StringBuilder;

    .line 319
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 322
    const v1, 0x7f14194f

    .line 325
    invoke-static {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 328
    move-result-object v1

    .line 329
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 332
    const-string v1, " ("

    .line 334
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 337
    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 340
    const-string p0, ")"

    .line 342
    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 345
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 348
    move-result-object p0

    .line 349
    const/4 v6, 0x1

    return-object p0

    .line 350
    :cond_1ad
    return-object v1

    .line 351
    :pswitch_data_1ae
    .packed-switch 0x1
        :pswitch_d1
        :pswitch_cb
        :pswitch_c8
        :pswitch_c5
        :pswitch_bf
        :pswitch_bb
        :pswitch_b6
        :pswitch_b1
        :pswitch_ad
        :pswitch_a8
        :pswitch_a2
        :pswitch_9f
        :pswitch_9b
        :pswitch_98
        :pswitch_93
        :pswitch_8d
        :pswitch_89
        :pswitch_85
        :pswitch_81
        :pswitch_7d
        :pswitch_79
        :pswitch_76
        :pswitch_71
        :pswitch_6c
        :pswitch_66
        :pswitch_62
        :pswitch_5d
        :pswitch_59
        :pswitch_54
        :pswitch_4e
        :pswitch_49
        :pswitch_44
        :pswitch_3e
        :pswitch_38
        :pswitch_33
        :pswitch_2e
    .end packed-switch
.end method

.method public getExtendedDetail()Ljava/lang/String;
    .locals 1

    .line 1
    const-string p0, ""

    .line 3
    return-object p0
.end method

.method public getHasCommentEdited()Z
    .locals 1

    .line 1
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasCommentEdited:Z

    .line 3
    return p0
.end method

.method public getHelpInfo()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x3

    invoke-virtual {p0}, Lk2e;->getHelpInfo()I

    .line 8
    move-result p0

    .line 9
    const/4 v0, 0x0

    invoke-static {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 12
    move-result-object p0

    .line 13
    const/4 v0, 0x1

    return-object p0
.end method

.method public getIcon()I
    .locals 1

    .line 1
    const/4 v0, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    invoke-virtual {p0}, Lk2e;->getIcon()I

    .line 8
    move-result p0

    .line 9
    return p0
.end method

.method public getImage()I
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public abstract getInfo()Lk2e;
.end method

.method public getListModeName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getListModeNameCharSequence()Ljava/lang/CharSequence;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getListModeName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getLogEntryStart()Ljava/lang/String;
    .locals 1

    .line 1
    const-string p0, ""

    const-string p0, ""

    .line 3
    const/4 v0, 0x3

    return-object p0
.end method

.method public getMacro()Lcom/arlosoft/macrodroid/macro/Macro;
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    return-object p0
.end method

.method public getMacroGuid()Ljava/lang/Long;
    .locals 3

    .line 1
    const/4 v2, 0x5

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    if-eqz p0, :cond_10

    .line 5
    const/4 v2, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getGUID()J

    .line 8
    move-result-wide v0

    .line 9
    const/4 v2, 0x7

    invoke-static {v0, v1}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 12
    move-result-object p0

    .line 13
    return-object p0

    .line 14
    :cond_10
    const-wide/16 v0, 0x0

    const-wide/16 v0, 0x0

    .line 16
    invoke-static {v0, v1}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    .line 19
    move-result-object p0

    .line 20
    const/4 v2, 0x6

    return-object p0
.end method

.method public getMacroName()Ljava/lang/String;
    .locals 3

    .line 1
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    if-eqz v0, :cond_a

    .line 5
    const/4 v2, 0x2

    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/macro/Macro;->getName()Ljava/lang/String;

    .line 8
    move-result-object p0

    .line 9
    return-object p0

    .line 10
    :cond_a
    const/4 v2, 0x2

    new-instance v0, Ljava/lang/StringBuilder;

    .line 12
    const-string v1, "No macro set for "

    .line 14
    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 17
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 20
    move-result-object p0

    .line 21
    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 24
    const-string p0, " cannot get macro name"

    .line 26
    const/4 v2, 0x5

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 29
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 32
    move-result-object p0

    .line 33
    invoke-static {p0}, Lkjf;->u(Ljava/lang/String;)V

    .line 36
    const-string p0, ""

    const-string p0, ""

    .line 38
    return-object p0
.end method

.method public getName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x3

    invoke-virtual {p0}, Lk2e;->getName()I

    .line 8
    move-result p0

    .line 9
    const/4 v0, 0x5

    invoke-static {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 12
    move-result-object p0

    .line 13
    return-object p0
.end method

.method public getPermissions()[Ljava/lang/String;
    .locals 1

    .line 1
    const/4 p0, 0x3

    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x1

    new-array p0, p0, [Ljava/lang/String;

    .line 4
    return-object p0
.end method

.method public getPermissionsOnImport()[Ljava/lang/String;
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    new-array p0, p0, [Ljava/lang/String;

    .line 4
    return-object p0
.end method

.method public getRequiredPermissions()[Ljava/lang/String;
    .locals 1

    .line 1
    const/4 v0, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public getSIGUID()J
    .locals 5

    .line 1
    iget-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 3
    const-wide/16 v2, 0x0

    .line 5
    const/4 v4, 0x1

    cmp-long v2, v0, v2

    .line 7
    if-nez v2, :cond_14

    .line 9
    invoke-static {}, Ljava/util/UUID;->randomUUID()Ljava/util/UUID;

    .line 12
    move-result-object v0

    .line 13
    const/4 v4, 0x7

    invoke-virtual {v0}, Ljava/util/UUID;->getLeastSignificantBits()J

    .line 16
    move-result-wide v0

    .line 17
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 19
    :cond_14
    return-wide v0
.end method

.method public getSecondaryOptions()[Ljava/lang/String;
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return-object p0
.end method

.method public getSecondaryOptionsTitle()Ljava/lang/String;
    .locals 2

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 4
    move-result-object p0

    .line 5
    const/4 v1, 0x1

    const v0, 0x7f14138b

    .line 8
    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 11
    move-result-object p0

    .line 12
    return-object p0
.end method

.method public getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getListModeName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x6

    return-object p0
.end method

.method public getTemplateConfiguredName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getListModeName()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x5

    return-object p0
.end method

.method public getTriggerList()Ljava/util/List;
    .locals 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/arlosoft/macrodroid/triggers/Trigger;",
            ">;"
        }
    .end annotation

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x3

    if-eqz v0, :cond_11

    .line 7
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 10
    move-result-object p0

    .line 11
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerList()Ljava/util/ArrayList;

    .line 14
    move-result-object p0

    .line 15
    const/4 v1, 0x1

    return-object p0

    .line 16
    :cond_11
    const/4 v1, 0x1

    new-instance p0, Ljava/util/ArrayList;

    .line 18
    const/4 v1, 0x5

    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 21
    return-object p0
.end method

.method public getTypeFromClass(Lz57;)I
    .locals 2

    .line 1
    instance-of p0, p1, Lh57;

    .line 3
    const/4 v1, 0x0

    if-eqz p0, :cond_8

    .line 5
    const/4 v1, 0x7

    const/4 p0, 0x0

    .line 6
    return p0

    .line 7
    :cond_8
    const/4 v1, 0x4

    instance-of p0, p1, Lw57;

    .line 9
    const/4 v0, 0x2

    .line 10
    if-eqz p0, :cond_f

    .line 12
    return v0

    .line 13
    :cond_f
    const/4 v1, 0x6

    instance-of p0, p1, Lp57;

    .line 15
    if-eqz p0, :cond_16

    .line 17
    const/4 p0, 0x1

    .line 18
    return p0

    .line 19
    :cond_16
    instance-of p0, p1, Ln57;

    .line 21
    if-eqz p0, :cond_1e

    .line 23
    const/4 p0, 0x0

    const/4 p0, 0x4

    .line 24
    const/4 v1, 0x4

    return p0

    .line 25
    :cond_1e
    return v0
.end method

.method public getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;
    .locals 3

    .line 1
    if-nez p1, :cond_5

    .line 3
    const/4 p0, 0x0

    .line 4
    const/4 v2, 0x3

    return-object p0

    .line 5
    :cond_5
    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    .line 8
    move-result-object p1

    .line 9
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 11
    const/4 v2, 0x2

    if-eqz p0, :cond_33

    .line 13
    const/4 v2, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->getLocalVariables()Ljava/util/List;

    .line 16
    move-result-object p0

    .line 17
    const/4 v2, 0x2

    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 20
    move-result-object p0

    .line 21
    :cond_18
    const/4 v2, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 24
    move-result v0

    .line 25
    const/4 v2, 0x4

    if-eqz v0, :cond_33

    .line 27
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 30
    move-result-object v0

    .line 31
    const/4 v2, 0x7

    check-cast v0, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 33
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 36
    move-result-object v1

    .line 37
    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 40
    move-result v1

    .line 41
    if-eqz v1, :cond_18

    .line 43
    const/4 v2, 0x7

    return-object v0

    .line 44
    :cond_33
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 47
    move-result-object p0

    .line 48
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/a;->s(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 51
    move-result-object p0

    .line 52
    return-object p0
.end method

.method public getVariablesOfType(I)Ljava/util/List;
    .locals 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(I)",
            "Ljava/util/List<",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v1, 0x1

    if-eqz p1, :cond_38

    .line 3
    const/4 v1, 0x5

    const/4 v0, 0x1

    .line 4
    if-eq p1, v0, :cond_32

    .line 6
    const/4 v1, 0x4

    const/4 v0, 0x2

    .line 7
    if-eq p1, v0, :cond_2d

    .line 9
    const/4 v1, 0x3

    const/4 v0, 0x3

    .line 10
    if-eq p1, v0, :cond_28

    .line 12
    const/4 v0, 0x4

    xor-int/2addr v1, v0

    .line 13
    if-eq p1, v0, :cond_23

    .line 15
    const/4 v0, 0x5

    shl-int/2addr v1, v0

    .line 16
    if-eq p1, v0, :cond_1e

    .line 18
    new-instance p0, Ljava/util/ArrayList;

    .line 20
    invoke-direct {p0}, Ljava/util/ArrayList;-><init>()V

    .line 23
    const/4 v1, 0x1

    return-object p0

    .line 24
    :cond_1e
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllArrayVariables()Ljava/util/ArrayList;

    .line 27
    move-result-object p0

    .line 28
    return-object p0

    .line 29
    :cond_23
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllDictionaryVariables()Ljava/util/ArrayList;

    .line 32
    move-result-object p0

    .line 33
    return-object p0

    .line 34
    :cond_28
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllDecimalVariables()Ljava/util/ArrayList;

    .line 37
    move-result-object p0

    .line 38
    return-object p0

    .line 39
    :cond_2d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllStringVariables()Ljava/util/ArrayList;

    .line 42
    move-result-object p0

    .line 43
    return-object p0

    .line 44
    :cond_32
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllIntegerVariables()Ljava/util/ArrayList;

    .line 47
    move-result-object p0

    .line 48
    const/4 v1, 0x0

    return-object p0

    .line 49
    :cond_38
    const/4 v1, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getAllBooleanVariables()Ljava/util/ArrayList;

    .line 52
    move-result-object p0

    .line 53
    return-object p0
.end method

.method public handleActivityResult(Landroid/app/Activity;IILandroid/content/Intent;)V
    .locals 1

    .line 1
    const/4 v0, 0x1

    return-void
.end method

.method public handleItemCancel()V
    .locals 3

    .line 1
    const/4 v2, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 4
    move-result-object p0

    .line 5
    const/4 v2, 0x5

    instance-of v0, p0, Lcom/arlosoft/macrodroid/actionblock/edit/ActionBlockEditActivity;

    .line 7
    const/4 v2, 0x3

    const/4 v1, 0x0

    .line 8
    if-eqz v0, :cond_13

    .line 10
    check-cast p0, Lcom/arlosoft/macrodroid/actionblock/edit/ActionBlockEditActivity;

    .line 12
    const/4 v2, 0x2

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/actionblock/edit/ActionBlockEditActivity;->D1(Z)V

    .line 15
    return-void

    .line 16
    :cond_13
    instance-of v0, p0, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;

    .line 18
    if-eqz v0, :cond_1c

    .line 20
    check-cast p0, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;

    .line 22
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;->D1(Z)V

    .line 25
    :cond_1c
    return-void
.end method

.method public handleItemComplete(Ljava/lang/Object;)V
    .locals 1

    .line 1
    return-void
.end method

.method public handleItemSelected()V
    .locals 2

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSecondaryOptions()[Ljava/lang/String;

    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x3

    if-eqz v0, :cond_f

    .line 7
    array-length v0, v0

    .line 8
    if-lez v0, :cond_f

    .line 10
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->displaySafeSecondaryOptionsDialog()V

    .line 13
    const/4 v1, 0x0

    return-void

    .line 14
    :cond_f
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->itemComplete()V

    .line 17
    return-void
.end method

.method public handleItemSelectedSafe()V
    .locals 4

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkActivityAlive()Z

    .line 4
    move-result v0

    .line 5
    const/4 v3, 0x2

    if-eqz v0, :cond_30

    .line 7
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 10
    move-result-object v0

    .line 11
    const/4 v3, 0x4

    if-eqz v0, :cond_2d

    .line 13
    const-string v1, "input_method"

    .line 15
    invoke-virtual {v0, v1}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 18
    move-result-object v1

    .line 19
    const/4 v3, 0x4

    check-cast v1, Landroid/view/inputmethod/InputMethodManager;

    .line 21
    const/4 v3, 0x1

    invoke-virtual {v0}, Landroid/app/Activity;->getCurrentFocus()Landroid/view/View;

    .line 24
    move-result-object v2

    .line 25
    if-nez v2, :cond_24

    .line 27
    const/4 v3, 0x1

    new-instance v2, Landroid/view/View;

    .line 29
    invoke-direct {v2, v0}, Landroid/view/View;-><init>(Landroid/content/Context;)V

    .line 32
    :cond_24
    invoke-virtual {v2}, Landroid/view/View;->getWindowToken()Landroid/os/IBinder;

    .line 35
    move-result-object v0

    .line 36
    const/4 v3, 0x2

    const/4 v2, 0x0

    .line 37
    invoke-virtual {v1, v0, v2}, Landroid/view/inputmethod/InputMethodManager;->hideSoftInputFromWindow(Landroid/os/IBinder;I)Z

    .line 40
    :cond_2d
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->handleItemSelected()V

    .line 43
    :cond_30
    const/4 v3, 0x6

    return-void
.end method

.method public handleOptionsDialogCancelled()V
    .locals 1

    .line 1
    return-void
.end method

.method public handleWarningClick()V
    .locals 1

    .line 1
    return-void
.end method

.method public hasAllSpecialPermissions(Landroid/app/Activity;)Z
    .locals 3

    .line 1
    const/4 v2, 0x5

    const/4 v0, 0x1

    .line 2
    const/4 v1, 0x0

    .line 3
    invoke-static {p1, p0, v0, v1}, Llob;->c(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;ZZ)Z

    .line 6
    move-result p0

    .line 7
    const/4 v2, 0x2

    return p0
.end method

.method public hasEdited()Z
    .locals 1

    .line 1
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasEdited:Z

    .line 3
    const/4 v0, 0x5

    return p0
.end method

.method public hasOptions()Z
    .locals 1

    .line 1
    const/4 v0, 0x6

    const/4 p0, 0x1

    .line 2
    const/4 v0, 0x5

    return p0
.end method

.method public init()V
    .locals 1

    .line 1
    return-void
.end method

.method public isChildOfIterateDictionary()Ly98;
    .locals 1

    .line 1
    const/4 v0, 0x3

    sget-object p0, Ly98;->NONE:Ly98;

    .line 3
    return-object p0
.end method

.method public isChildOfLoop()Z
    .locals 1

    .line 1
    const/4 v0, 0x5

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public isCollapsed()Z
    .locals 1

    .line 1
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isCollapsed:Z

    .line 3
    return p0
.end method

.method public isEnabled()Z
    .locals 1

    .line 1
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 3
    xor-int/lit8 p0, p0, 0x1

    .line 5
    return p0
.end method

.method public isExperimental()Z
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x1

    invoke-virtual {p0}, Lk2e;->isExperimental()Z

    .line 8
    move-result p0

    .line 9
    return p0
.end method

.method public isExtendedHtml()Z
    .locals 1

    .line 1
    const/4 v0, 0x3

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public isExtra()Z
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    if-eqz p0, :cond_a

    .line 5
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/macro/Macro;->isExtra()Z

    .line 8
    move-result p0

    .line 9
    const/4 v0, 0x5

    return p0

    .line 10
    :cond_a
    const/4 p0, 0x0

    .line 11
    return p0
.end method

.method public isLoggingDisabled()Z
    .locals 1

    .line 1
    const/4 v0, 0x0

    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->disableLogging:Z

    .line 3
    return p0
.end method

.method public isProOnly()Z
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    invoke-virtual {p0}, Lk2e;->isProOnly()Z

    .line 8
    move-result p0

    .line 9
    const/4 v0, 0x4

    return p0
.end method

.method public isRootOnly()Z
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x4

    invoke-virtual {p0}, Lk2e;->isRootOnly()Z

    .line 8
    move-result p0

    .line 9
    return p0
.end method

.method public isRootOnlyWithNoAdbHack()Z
    .locals 2

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 4
    move-result-object v0

    .line 5
    invoke-virtual {v0}, Lk2e;->isRootOnly()Z

    .line 8
    move-result v0

    .line 9
    if-eqz v0, :cond_17

    .line 11
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getInfo()Lk2e;

    .line 14
    move-result-object p0

    .line 15
    invoke-virtual {p0}, Lk2e;->supportsAdbHack()Z

    .line 18
    move-result p0

    .line 19
    if-nez p0, :cond_17

    .line 21
    const/4 v1, 0x3

    const/4 p0, 0x1

    .line 22
    return p0

    .line 23
    :cond_17
    const/4 p0, 0x0

    .line 24
    const/4 v1, 0x3

    return p0
.end method

.method public isValid()Z
    .locals 1

    .line 1
    const/4 p0, 0x1

    .line 2
    return p0
.end method

.method public itemComplete()V
    .locals 4

    .line 1
    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasEdited:Z

    .line 3
    if-nez v0, :cond_25

    .line 5
    const/4 v3, 0x2

    const/4 v0, 0x0

    .line 6
    invoke-static {v0, v0}, Lf37;->c(ZZ)Lcom/google/gson/GsonBuilder;

    .line 9
    move-result-object v1

    .line 10
    invoke-virtual {v1}, Lcom/google/gson/GsonBuilder;->b()Lcom/google/gson/Gson;

    .line 13
    move-result-object v1

    .line 14
    invoke-virtual {v1, p0}, Lcom/google/gson/Gson;->k(Ljava/lang/Object;)Ljava/lang/String;

    .line 17
    move-result-object v1

    .line 18
    const/4 v3, 0x4

    iget-boolean v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isAddingNew:Z

    .line 20
    if-nez v2, :cond_20

    .line 22
    iget-object v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->serializedFormBeforeEdit:Ljava/lang/String;

    .line 24
    const/4 v3, 0x3

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 27
    move-result v1

    .line 28
    if-nez v1, :cond_21

    .line 30
    :cond_20
    const/4 v0, 0x1

    .line 31
    :cond_21
    const/4 v3, 0x7

    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->setHasEdited(Z)V

    .line 34
    :cond_25
    return-void
.end method

.method public matchesSearchText(Ljava/lang/String;)Z
    .locals 6

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 4
    move-result-object v0

    .line 5
    const/4 v5, 0x7

    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 8
    move-result v0

    .line 9
    if-nez v0, :cond_104

    .line 11
    const/4 v5, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getName()Ljava/lang/String;

    .line 14
    move-result-object v0

    .line 15
    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 18
    move-result v0

    .line 19
    const/4 v5, 0x5

    if-nez v0, :cond_104

    .line 21
    const/4 v5, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getExtendedDetail()Ljava/lang/String;

    .line 24
    move-result-object v0

    .line 25
    const/4 v5, 0x7

    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 28
    move-result v0

    .line 29
    if-nez v0, :cond_104

    .line 31
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getComment()Ljava/lang/String;

    .line 34
    move-result-object v0

    .line 35
    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 38
    move-result v0

    .line 39
    const/4 v5, 0x2

    if-eqz v0, :cond_30

    .line 41
    goto/16 :goto_104

    .line 43
    :cond_30
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 46
    move-result-object v0

    .line 47
    invoke-interface {v0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 50
    move-result-object v0

    .line 51
    :cond_38
    const/4 v5, 0x4

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 54
    move-result v1

    .line 55
    if-eqz v1, :cond_4e

    .line 57
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 60
    move-result-object v1

    .line 61
    check-cast v1, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 63
    const/4 v5, 0x2

    invoke-virtual {v1, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->matchesSearchText(Ljava/lang/String;)Z

    .line 66
    move-result v1

    .line 67
    if-eqz v1, :cond_38

    .line 69
    goto/16 :goto_104

    .line 71
    :cond_4e
    instance-of v0, p0, La67;

    .line 73
    const/4 v1, 0x0

    .line 74
    if-eqz v0, :cond_73

    .line 76
    move-object v0, p0

    .line 77
    check-cast v0, La67;

    .line 79
    invoke-interface {v0}, La67;->getVariableNames()[Ljava/lang/String;

    .line 82
    move-result-object v0

    .line 83
    const/4 v5, 0x0

    array-length v2, v0

    .line 84
    move v3, v1

    move v3, v1

    .line 85
    :goto_5e
    const/4 v5, 0x6

    if-ge v3, v2, :cond_73

    .line 87
    aget-object v4, v0, v3

    .line 89
    const/4 v5, 0x2

    if-eqz v4, :cond_6f

    .line 91
    invoke-static {p1, v4}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 94
    move-result v4

    .line 95
    const/4 v5, 0x7

    if-eqz v4, :cond_6f

    .line 97
    goto/16 :goto_104

    .line 99
    :cond_6f
    add-int/lit8 v3, v3, 0x1

    .line 101
    const/4 v5, 0x6

    goto :goto_5e

    .line 102
    :cond_73
    const/4 v5, 0x3

    instance-of v0, p0, Lz57;

    .line 104
    if-eqz v0, :cond_90

    .line 106
    move-object v0, p0

    .line 107
    check-cast v0, Lz57;

    .line 109
    const/4 v5, 0x0

    invoke-interface {v0}, Lz57;->k()Ljava/lang/String;

    .line 112
    move-result-object v2

    .line 113
    if-eqz v2, :cond_90

    .line 115
    const/4 v5, 0x7

    invoke-interface {v0}, Lz57;->k()Ljava/lang/String;

    .line 118
    move-result-object v0

    .line 119
    const/4 v5, 0x2

    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 122
    move-result v0

    .line 123
    const/4 v5, 0x2

    if-eqz v0, :cond_90

    .line 125
    goto :goto_104

    .line 126
    :cond_90
    const/4 v5, 0x4

    instance-of v0, p0, Ly57;

    .line 128
    if-eqz v0, :cond_b0

    .line 130
    move-object v0, p0

    .line 131
    const/4 v5, 0x1

    check-cast v0, Ly57;

    .line 133
    invoke-interface {v0}, Ly57;->r()Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 136
    move-result-object v2

    .line 137
    const/4 v5, 0x2

    if-eqz v2, :cond_b0

    .line 139
    invoke-interface {v0}, Ly57;->r()Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 142
    move-result-object v0

    .line 143
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 146
    move-result-object v0

    .line 147
    const/4 v5, 0x7

    invoke-static {p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 150
    move-result v0

    .line 151
    if-eqz v0, :cond_b0

    .line 153
    goto :goto_104

    .line 154
    :cond_b0
    const/4 v5, 0x2

    instance-of v0, p0, Lb67;

    .line 156
    if-eqz v0, :cond_df

    .line 158
    move-object v0, p0

    .line 159
    const/4 v5, 0x2

    check-cast v0, Lb67;

    .line 161
    const/4 v5, 0x6

    invoke-interface {v0}, Lb67;->i()Ljava/util/ArrayList;

    .line 164
    move-result-object v0

    .line 165
    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 168
    move-result-object v0

    .line 169
    :cond_c2
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 172
    move-result v2

    .line 173
    const/4 v5, 0x5

    if-eqz v2, :cond_df

    .line 175
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 178
    move-result-object v2

    .line 179
    check-cast v2, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 181
    const/4 v5, 0x0

    if-eqz v2, :cond_c2

    .line 183
    invoke-virtual {v2}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 186
    move-result-object v2

    .line 187
    const/4 v5, 0x1

    invoke-static {p1, v2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 190
    move-result v2

    .line 191
    if-eqz v2, :cond_c2

    .line 193
    const/4 v5, 0x4

    goto :goto_104

    .line 194
    :cond_df
    instance-of v0, p0, Ldef;

    .line 196
    if-eqz v0, :cond_103

    .line 198
    check-cast p0, Ldef;

    .line 200
    const/4 v5, 0x4

    invoke-interface {p0}, Ldef;->getPossibleMagicText()[Ljava/lang/String;

    .line 203
    move-result-object p0

    .line 204
    const/4 v5, 0x2

    if-eqz p0, :cond_103

    .line 206
    array-length v0, p0

    .line 207
    move v2, v1

    .line 208
    :goto_ef
    const/4 v5, 0x1

    if-ge v2, v0, :cond_103

    .line 210
    aget-object v3, p0, v2

    .line 212
    const/4 v5, 0x0

    invoke-static {p1, v3}, Lcom/arlosoft/macrodroid/common/SelectableItem;->R(Ljava/lang/String;Ljava/lang/String;)Z

    .line 215
    move-result v3

    .line 216
    const/4 v5, 0x3

    if-eqz v3, :cond_fe

    .line 218
    const/4 v5, 0x6

    goto :goto_104

    .line 219
    :cond_fe
    const/4 v5, 0x2

    add-int/lit8 v2, v2, 0x1

    .line 221
    const/4 v5, 0x2

    goto :goto_ef

    .line 222
    :cond_103
    return v1

    .line 223
    :cond_104
    :goto_104
    const/4 p0, 0x1

    .line 224
    return p0
.end method

.method public onItemSelected()V
    .locals 2

    const/4 v0, 0x0

    .line 130
    const/4 v1, 0x7

    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->onItemSelected(Z)V

    return-void
.end method

.method public abstract onItemSelected(JJZ)V
.end method

.method public onItemSelected(Z)V
    .locals 7

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->addingFavourite:Z

    .line 3
    const/4 v6, 0x1

    invoke-static {}, Lcom/google/firebase/crashlytics/FirebaseCrashlytics;->getInstance()Lcom/google/firebase/crashlytics/FirebaseCrashlytics;

    .line 6
    move-result-object p1

    .line 7
    const/4 v6, 0x4

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 10
    move-result-object v0

    .line 11
    invoke-virtual {v0}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    .line 14
    move-result-object v0

    .line 15
    const/4 v6, 0x0

    const-string/jumbo v1, "tcmSodIote nleee "

    const-string v1, "onItemSelected - "

    .line 17
    invoke-virtual {v1, v0}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 20
    move-result-object v0

    .line 21
    iget-object p1, p1, Lcom/google/firebase/crashlytics/FirebaseCrashlytics;->a:Lcom/google/firebase/crashlytics/internal/common/CrashlyticsCore;

    .line 23
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 26
    move-result-wide v1

    .line 27
    iget-wide v3, p1, Lcom/google/firebase/crashlytics/internal/common/CrashlyticsCore;->d:J

    .line 29
    sub-long/2addr v1, v3

    .line 30
    iget-object v3, p1, Lcom/google/firebase/crashlytics/internal/common/CrashlyticsCore;->o:Lcom/google/firebase/crashlytics/internal/concurrency/CrashlyticsWorkers;

    .line 32
    iget-object v3, v3, Lcom/google/firebase/crashlytics/internal/concurrency/CrashlyticsWorkers;->a:Lcom/google/firebase/crashlytics/internal/concurrency/CrashlyticsWorker;

    .line 34
    new-instance v4, Lra3;

    .line 36
    invoke-direct {v4, p1, v1, v2, v0}, Lra3;-><init>(Lcom/google/firebase/crashlytics/internal/common/CrashlyticsCore;JLjava/lang/String;)V

    .line 39
    invoke-virtual {v3, v4}, Lcom/google/firebase/crashlytics/internal/concurrency/CrashlyticsWorker;->a(Ljava/lang/Runnable;)Lcom/google/android/gms/tasks/Task;

    .line 42
    const/4 p1, 0x0

    .line 43
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->setAddingNew(Z)V

    .line 46
    invoke-static {p1, p1}, Lf37;->c(ZZ)Lcom/google/gson/GsonBuilder;

    .line 49
    move-result-object v0

    .line 50
    const/4 v6, 0x0

    invoke-virtual {v0}, Lcom/google/gson/GsonBuilder;->b()Lcom/google/gson/Gson;

    .line 53
    move-result-object v0

    .line 54
    :try_start_3c
    const/4 v6, 0x5

    invoke-virtual {v0, p0}, Lcom/google/gson/Gson;->k(Ljava/lang/Object;)Ljava/lang/String;

    .line 57
    move-result-object v0

    .line 58
    const/4 v6, 0x4

    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->serializedFormBeforeEdit:Ljava/lang/String;
    :try_end_44
    .catchall {:try_start_3c .. :try_end_44} :catchall_45

    .line 60
    goto :goto_5f

    .line 61
    :catchall_45
    move-exception v0

    .line 62
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 65
    move-result-object v1

    .line 66
    const/4 v6, 0x1

    invoke-virtual {v1}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    .line 69
    move-result-object v1

    .line 70
    const-string v2, "Enir bro "

    const-string v2, "Error in "

    .line 72
    const/4 v6, 0x3

    invoke-virtual {v2, v1}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 75
    move-result-object v1

    .line 76
    const/4 v6, 0x6

    invoke-static {v1}, Lsz5;->a(Ljava/lang/String;)V

    .line 79
    invoke-static {v0}, Lsz5;->e(Ljava/lang/Throwable;)V

    .line 82
    :goto_5f
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 85
    move-result-wide v0

    .line 86
    const/4 v6, 0x4

    iget-wide v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_lastClickTime:J

    .line 88
    const-wide/16 v4, 0x3e8

    const-wide/16 v4, 0x3e8

    .line 90
    add-long/2addr v2, v4

    .line 91
    cmp-long v2, v0, v2

    .line 93
    if-lez v2, :cond_95

    .line 95
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_lastClickTime:J

    .line 97
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkPermissionsOnConfigure()Z

    .line 100
    move-result v0

    .line 101
    if-eqz v0, :cond_91

    .line 103
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkActivityAlive()Z

    .line 106
    move-result v0

    .line 107
    if-nez v0, :cond_7e

    .line 109
    goto :goto_95

    .line 110
    :cond_7e
    const/4 v6, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 113
    move-result-object v0

    .line 114
    const/4 v1, 0x7

    const/4 v1, 0x1

    .line 115
    invoke-static {v0, p0, v1, p1}, Llob;->c(Landroid/app/Activity;Lcom/arlosoft/macrodroid/common/SelectableItem;ZZ)Z

    .line 118
    move-result p1

    .line 119
    if-nez p1, :cond_8c

    .line 121
    goto :goto_95

    .line 122
    :cond_8c
    const/4 v6, 0x6

    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkAndroidPermissionsAndSelectItem(Landroid/app/Activity;)V

    .line 125
    goto :goto_95

    .line 126
    :cond_91
    const/4 v6, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->handleItemSelectedSafe()V

    .line 129
    :cond_95
    :goto_95
    return-void
.end method

.method public permissionsDenied([Ljava/lang/String;[I)V
    .locals 5

    .line 1
    const/4 v0, 0x0

    .line 2
    move v1, v0

    .line 3
    :goto_2
    const/4 v4, 0x6

    array-length v2, p2

    .line 4
    if-ge v1, v2, :cond_12

    .line 6
    const/4 v4, 0x6

    aget v2, p2, v1

    .line 8
    const/4 v3, -0x5

    const/4 v3, -0x1

    .line 9
    if-ne v2, v3, :cond_e

    .line 11
    goto :goto_14

    .line 12
    :cond_e
    add-int/lit8 v1, v1, 0x1

    .line 14
    const/4 v4, 0x0

    goto :goto_2

    .line 15
    :cond_12
    const/4 v4, 0x7

    move v1, v0

    .line 16
    :goto_14
    aget-object p1, p1, v1

    .line 18
    invoke-static {p1}, Llob;->e(Ljava/lang/String;)Ljava/lang/String;

    .line 21
    move-result-object p1

    .line 22
    const/4 v4, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 25
    move-result-object p2

    .line 26
    invoke-virtual {p2}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 29
    move-result-object p2

    .line 30
    const-string v1, " "

    .line 32
    invoke-static {p1, v1}, Lbl5;->x(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 35
    move-result-object p1

    .line 36
    const/4 v4, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 39
    move-result-object p0

    .line 40
    const v1, 0x7f14118e

    .line 43
    invoke-virtual {p0, v1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 46
    move-result-object p0

    .line 47
    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 50
    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 53
    move-result-object p0

    .line 54
    invoke-static {p2, p0, v0}, Le3g;->b(Landroid/content/Context;Ljava/lang/CharSequence;I)Le3g;

    .line 57
    move-result-object p0

    .line 58
    invoke-virtual {p0}, Le3g;->show()V

    .line 61
    return-void
.end method

.method public permissionsGranted()V
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->handleItemSelectedSafe()V

    .line 4
    const/4 v0, 0x0

    return-void
.end method

.method public postApplyImport()V
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->applyImport()V

    .line 4
    return-void
.end method

.method public preApplyImport()V
    .locals 1

    .line 1
    return-void
.end method

.method public refresh()V
    .locals 1

    .line 1
    return-void
.end method

.method public removeConstraint(Lcom/arlosoft/macrodroid/constraint/Constraint;)V
    .locals 3

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConstraints()Ljava/util/List;

    .line 4
    move-result-object v0

    .line 5
    invoke-interface {v0, p1}, Ljava/util/List;->remove(Ljava/lang/Object;)Z

    .line 8
    move-result v0

    .line 9
    if-nez v0, :cond_1e

    .line 11
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/constraint/Constraint;->g0()J

    .line 14
    move-result-wide v0

    .line 15
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 18
    move-result-object p0

    .line 19
    const/4 v2, 0x2

    if-eqz p0, :cond_1e

    .line 21
    invoke-virtual {p0, v0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->findChildByGUID(J)Lcom/arlosoft/macrodroid/common/SelectableItem;

    .line 24
    move-result-object p0

    .line 25
    if-eqz p0, :cond_1e

    .line 27
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->removeConstraint(Lcom/arlosoft/macrodroid/constraint/Constraint;)V

    .line 30
    :cond_1e
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/constraint/Constraint;->a0()V

    .line 33
    return-void
.end method

.method public requiresAccessNotificationPolicy()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresAccessibility()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresAllFilesAccess()Z
    .locals 1

    .line 1
    const/4 p0, 0x3

    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x6

    return p0
.end method

.method public requiresCanDrawOverlays()Z
    .locals 1

    .line 1
    const/4 p0, 0x4

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresCanShowBubbles()Z
    .locals 1

    .line 1
    const/4 v0, 0x7

    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x3

    return p0
.end method

.method public requiresCoarseLocationPermission()Z
    .locals 6

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v5, 0x4

    array-length v0, p0

    .line 6
    const/4 v1, 0x0

    .line 7
    move v2, v1

    .line 8
    :goto_8
    if-ge v2, v0, :cond_1b

    .line 10
    aget-object v3, p0, v2

    .line 12
    const-string v4, "android.permission.ACCESS_COARSE_LOCATION"

    .line 14
    invoke-virtual {v3, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 17
    move-result v3

    .line 18
    const/4 v5, 0x2

    if-eqz v3, :cond_18

    .line 20
    const/4 p0, 0x1

    .line 21
    const/4 v5, 0x6

    return p0

    .line 22
    :cond_18
    add-int/lit8 v2, v2, 0x1

    .line 24
    goto :goto_8

    .line 25
    :cond_1b
    return v1
.end method

.method public requiresDefaultAssist()Z
    .locals 1

    .line 1
    const/4 v0, 0x7

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresDeviceAdmin()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresFineLocationPermission()Z
    .locals 6

    .line 1
    const/4 v5, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v5, 0x3

    array-length v0, p0

    .line 6
    const/4 v5, 0x0

    const/4 v1, 0x0

    .line 7
    move v2, v1

    .line 8
    :goto_a
    if-ge v2, v0, :cond_1d

    .line 10
    aget-object v3, p0, v2

    .line 12
    const-string v4, "android.permission.ACCESS_FINE_LOCATION"

    .line 14
    invoke-virtual {v3, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 17
    move-result v3

    .line 18
    if-eqz v3, :cond_19

    .line 20
    const/4 p0, 0x1

    move v5, p0

    .line 21
    return p0

    .line 22
    :cond_19
    add-int/lit8 v2, v2, 0x1

    .line 24
    const/4 v5, 0x6

    goto :goto_a

    .line 25
    :cond_1d
    const/4 v5, 0x2

    return v1
.end method

.method public requiresLegacyHelperFile()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresLocationServicesEnabled()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x3

    return p0
.end method

.method public requiresNewConnectivityHelperFile(I)Z
    .locals 3

    .line 1
    const/4 v2, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseConnectivityHelperApp()Landroid/util/Pair;

    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x0

    .line 6
    if-nez v0, :cond_a

    .line 8
    const/4 v2, 0x0

    return v1

    .line 9
    :cond_a
    const/4 v2, 0x3

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFileVersion()Landroid/util/Pair;

    .line 12
    move-result-object p0

    .line 13
    if-nez p0, :cond_12

    .line 15
    return v1

    .line 16
    :cond_12
    iget-object p0, v0, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 18
    check-cast p0, Ljava/lang/Integer;

    .line 20
    invoke-virtual {p0}, Ljava/lang/Integer;->intValue()I

    .line 23
    move-result p0

    .line 24
    const/4 v2, 0x7

    if-le p0, p1, :cond_20

    .line 26
    const/4 v2, 0x2

    const/4 p0, 0x1

    .line 27
    return p0

    .line 28
    :cond_20
    return v1
.end method

.method public requiresNewHelperFile(I)Z
    .locals 2

    const/4 v0, 0x0

    .line 44
    const/4 v1, 0x7

    invoke-virtual {p0, p1, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFile(II)Z

    move-result p0

    const/4 v1, 0x5

    return p0
.end method

.method public requiresNewHelperFile(II)Z
    .locals 3

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->requiresNewHelperFileVersion()Landroid/util/Pair;

    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x0

    .line 6
    if-nez v0, :cond_8

    .line 8
    return v1

    .line 9
    :cond_8
    const/4 v2, 0x3

    iget-object v0, v0, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 11
    const/4 v2, 0x2

    check-cast v0, Ljava/lang/Integer;

    .line 13
    invoke-virtual {v0}, Ljava/lang/Integer;->intValue()I

    .line 16
    move-result v0

    .line 17
    const/4 v2, 0x4

    if-lt p1, v0, :cond_16

    .line 19
    return v1

    .line 20
    :cond_16
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseConnectivityHelperApp()Landroid/util/Pair;

    .line 23
    move-result-object p1

    .line 24
    const/4 v2, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->canUseConnectivityHelperApp()Landroid/util/Pair;

    .line 27
    move-result-object p0

    .line 28
    const/4 v0, 0x1

    .line 29
    if-nez p0, :cond_23

    .line 31
    return v0

    .line 32
    :cond_23
    iget-object p0, p1, Landroid/util/Pair;->first:Ljava/lang/Object;

    .line 34
    check-cast p0, Ljava/lang/Integer;

    .line 36
    invoke-virtual {p0}, Ljava/lang/Integer;->intValue()I

    .line 39
    move-result p0

    .line 40
    if-ge p2, p0, :cond_2f

    .line 42
    const/4 v2, 0x0

    return v0

    .line 43
    :cond_2f
    return v1
.end method

.method public requiresNewHelperFileVersion()Landroid/util/Pair;
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Landroid/util/Pair<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .line 1
    const/4 v0, 0x6

    const/4 p0, 0x0

    .line 2
    return-object p0
.end method

.method public requiresNotificationAccess()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresNotificationsEnabled()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresScheduleExactAlarm()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresShizuku()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x7

    return p0
.end method

.method public requiresUIInteractionAccessibility()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    move v0, p0

    .line 2
    return p0
.end method

.method public requiresUsageAccess()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresWriteSettings()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public requiresXiaomiBackgroundStart()Z
    .locals 1

    .line 1
    const/4 p0, 0x0

    .line 2
    const/4 v0, 0x5

    return p0
.end method

.method public secondaryItemConfirmed()V
    .locals 1

    .line 1
    return-void
.end method

.method public secondaryItemConfirmedSafe()V
    .locals 2

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkActivityAlive()Z

    .line 4
    move-result v0

    .line 5
    if-eqz v0, :cond_9

    .line 7
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->secondaryItemConfirmed()V

    .line 10
    :cond_9
    return-void
.end method

.method public secondaryItemSelected(I)V
    .locals 1

    .line 1
    return-void
.end method

.method public setActivity(Landroid/app/Activity;)V
    .locals 2

    .line 1
    new-instance v0, Ljava/lang/ref/WeakReference;

    .line 3
    invoke-direct {v0, p1}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 6
    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_activityRef:Ljava/lang/ref/WeakReference;

    .line 8
    const/4 v1, 0x1

    return-void
.end method

.method public setAddingFavourite(Z)V
    .locals 1

    .line 1
    const/4 v0, 0x2

    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->addingFavourite:Z

    .line 3
    return-void
.end method

.method public setAddingNew(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isAddingNew:Z

    .line 3
    return-void
.end method

.method public setCollapsed(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isCollapsed:Z

    .line 3
    return-void
.end method

.method public setComment(Ljava/lang/String;)V
    .locals 1

    .line 1
    iput-object p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 3
    return-void
.end method

.method public setConstraintIsOrCondition(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isOrCondition:Z

    .line 3
    const/4 v0, 0x3

    return-void
.end method

.method public setConstraintList(Ljava/util/List;)V
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/arlosoft/macrodroid/constraint/Constraint;",
            ">;)V"
        }
    .end annotation

    .line 1
    iput-object p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 3
    return-void
.end method

.method public setEnabled(Z)V
    .locals 1

    .line 1
    const/4 v0, 0x4

    xor-int/lit8 p1, p1, 0x1

    .line 3
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 5
    const/4 v0, 0x2

    return-void
.end method

.method public setGUID(J)V
    .locals 1

    .line 1
    iput-wide p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 3
    return-void
.end method

.method public setHasCommentEdited(Z)V
    .locals 1

    .line 1
    const/4 v0, 0x5

    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasCommentEdited:Z

    .line 3
    return-void
.end method

.method public setHasEdited(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->hasEdited:Z

    .line 3
    return-void
.end method

.method public setLoggingDisabled(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->disableLogging:Z

    .line 3
    const/4 v0, 0x6

    return-void
.end method

.method public setMacro(Lcom/arlosoft/macrodroid/macro/Macro;)V
    .locals 3

    .line 1
    iput-object p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    const/4 v2, 0x6

    iget-object p1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 5
    if-eqz p1, :cond_1f

    .line 7
    invoke-interface {p1}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 10
    move-result-object p1

    .line 11
    :goto_b
    invoke-interface {p1}, Ljava/util/Iterator;->hasNext()Z

    .line 14
    move-result v0

    .line 15
    if-eqz v0, :cond_1f

    .line 17
    invoke-interface {p1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 20
    move-result-object v0

    .line 21
    const/4 v2, 0x6

    check-cast v0, Lcom/arlosoft/macrodroid/constraint/Constraint;

    .line 23
    const/4 v2, 0x4

    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 25
    invoke-virtual {v0, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->setMacro(Lcom/arlosoft/macrodroid/macro/Macro;)V

    .line 28
    goto :goto_b

    .line 29
    :cond_1f
    return-void
.end method

.method public setNewGUID()V
    .locals 3

    .line 1
    const/4 v2, 0x1

    invoke-static {}, Ljava/util/UUID;->randomUUID()Ljava/util/UUID;

    .line 4
    move-result-object v0

    .line 5
    const/4 v2, 0x5

    invoke-virtual {v0}, Ljava/util/UUID;->getLeastSignificantBits()J

    .line 8
    move-result-wide v0

    .line 9
    iput-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 11
    return-void
.end method

.method public showSearchInSecondaryOptionsDialog()Z
    .locals 1

    .line 1
    const/4 v0, 0x4

    const/4 p0, 0x0

    .line 2
    return p0
.end method

.method public templateSelected()V
    .locals 1

    .line 1
    return-void
.end method

.method public validate()V
    .locals 2

    .line 1
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 3
    if-nez v0, :cond_c

    .line 5
    new-instance v0, Ljava/util/ArrayList;

    .line 7
    const/4 v1, 0x3

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 10
    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 12
    :cond_c
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 14
    if-nez v0, :cond_17

    .line 16
    const/4 v1, 0x0

    const-string v0, ""

    const-string v0, ""

    .line 18
    iput-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 20
    :cond_17
    return-void
.end method

.method public variableClear(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V
    .locals 3

    .line 132
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->N()I

    move-result v0

    invoke-static {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue;->createForType(I)Lcom/arlosoft/macrodroid/variables/VariableValue;

    move-result-object v0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    move-result v1

    const/4 v2, 0x2

    xor-int/lit8 v1, v1, 0x1

    const/4 v2, 0x7

    invoke-virtual {p0, p1, v0, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V

    return-void
.end method

.method public variableClear(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Ljava/util/List;)V
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lcom/arlosoft/macrodroid/common/MacroDroidVariable;",
            "Ljava/util/List<",
            "Ljava/lang/String;",
            ">;)V"
        }
    .end annotation

    .line 1
    const/4 v0, 0x0

    .line 2
    invoke-virtual {p1, p2, v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->M(Ljava/util/List;Z)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 5
    move-result-object v0

    .line 6
    const/4 v3, 0x3

    invoke-interface {p2}, Ljava/util/List;->isEmpty()Z

    .line 9
    move-result v1

    .line 10
    const/4 v3, 0x3

    if-eqz v1, :cond_36

    .line 12
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->m()Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 15
    move-result-object p0

    .line 16
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 19
    move-result-object p0

    .line 20
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 23
    move-result-object p0

    .line 24
    :goto_19
    const/4 v3, 0x6

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 27
    move-result p1

    .line 28
    if-eqz p1, :cond_92

    .line 30
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 33
    move-result-object p1

    .line 34
    check-cast p1, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 36
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 39
    move-result-object p2

    .line 40
    invoke-virtual {p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->getVariableType()I

    .line 43
    move-result p2

    .line 44
    invoke-static {p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->createForType(I)Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 47
    move-result-object p2

    .line 48
    invoke-virtual {p1, p2}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->setVariable(Lcom/arlosoft/macrodroid/variables/VariableValue;)V

    .line 51
    goto :goto_19

    .line 52
    :cond_36
    const/4 v3, 0x5

    if-eqz v0, :cond_92

    .line 54
    const/4 v3, 0x6

    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariableType()I

    .line 57
    move-result v1

    .line 58
    const/4 v2, 0x4

    .line 59
    const/4 v3, 0x2

    if-eq v1, v2, :cond_62

    .line 61
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariableType()I

    .line 64
    move-result v1

    .line 65
    const/4 v3, 0x5

    const/4 v2, 0x5

    .line 66
    if-ne v1, v2, :cond_4b

    .line 68
    goto :goto_62

    .line 69
    :cond_4b
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 72
    move-result-object v0

    .line 73
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue;->getVariableType()I

    .line 76
    move-result v0

    .line 77
    const/4 v3, 0x3

    invoke-static {v0, p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->createForType(ILjava/util/List;)Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 80
    move-result-object p2

    .line 81
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isLoggingDisabled()Z

    .line 84
    move-result v0

    .line 85
    xor-int/lit8 v0, v0, 0x1

    .line 87
    invoke-virtual {p0, p1, p2, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V

    .line 90
    return-void

    .line 91
    :cond_62
    :goto_62
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->m()Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 94
    move-result-object p0

    .line 95
    const/4 v3, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 98
    move-result-object p0

    .line 99
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 102
    move-result-object p0

    .line 103
    :goto_6f
    const/4 v3, 0x0

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 106
    move-result p1

    .line 107
    const/4 v3, 0x0

    if-eqz p1, :cond_92

    .line 109
    const/4 v3, 0x4

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 112
    move-result-object p1

    .line 113
    check-cast p1, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 115
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 118
    move-result-object p2

    .line 119
    const/4 v3, 0x4

    invoke-virtual {p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->getVariableType()I

    .line 122
    move-result p2

    .line 123
    const/4 v3, 0x3

    invoke-static {p2}, Lcom/arlosoft/macrodroid/variables/VariableValue;->createForType(I)Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 126
    move-result-object p2

    .line 127
    const/4 v3, 0x4

    invoke-virtual {p1, p2}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->setVariable(Lcom/arlosoft/macrodroid/variables/VariableValue;)V

    .line 130
    const/4 v3, 0x3

    goto :goto_6f

    .line 131
    :cond_92
    return-void
.end method

.method public variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V
    .locals 8

    .line 1
    const/4 v7, 0x0

    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 3
    if-eqz v0, :cond_9

    .line 5
    invoke-virtual {v0, p1, p2, p3}, Lcom/arlosoft/macrodroid/macro/Macro;->variableUpdate(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Z)V

    .line 8
    return-void

    .line 9
    :cond_9
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 12
    move-result-object v1

    .line 13
    iget-object p3, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 15
    if-eqz p3, :cond_18

    .line 17
    const/4 v7, 0x0

    invoke-virtual {p3}, Lcom/arlosoft/macrodroid/macro/Macro;->isDetailLoggingExcluded()Z

    .line 20
    move-result p3

    .line 21
    const/4 v7, 0x3

    goto :goto_1a

    .line 22
    :cond_18
    const/4 p3, 0x0

    move v7, p3

    .line 23
    :goto_1a
    xor-int/lit8 v5, p3, 0x1

    .line 25
    const/4 v7, 0x7

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 28
    move-result-object v6

    .line 29
    const/4 v4, 0x0

    move v7, v4

    .line 30
    move-object v2, p1

    move-object v2, p1

    .line 31
    move-object v3, p2

    .line 32
    const/4 v7, 0x3

    invoke-virtual/range {v1 .. v6}, Lcom/arlosoft/macrodroid/common/a;->E(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;ZLcom/arlosoft/macrodroid/macro/Macro;)V

    .line 35
    return-void
.end method

.method public writeToParcel(Landroid/os/Parcel;I)V
    .locals 3

    .line 1
    const/4 v2, 0x5

    iget-wide v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_SIGUID:J

    .line 3
    invoke-virtual {p1, v0, v1}, Landroid/os/Parcel;->writeLong(J)V

    .line 6
    iget-object p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_constraintList:Ljava/util/List;

    .line 8
    const/4 v2, 0x7

    invoke-virtual {p1, p2}, Landroid/os/Parcel;->writeList(Ljava/util/List;)V

    .line 11
    const/4 v2, 0x2

    iget-boolean p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isOrCondition:Z

    .line 13
    invoke-virtual {p1, p2}, Landroid/os/Parcel;->writeInt(I)V

    .line 16
    iget-boolean p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_isDisabled:Z

    .line 18
    const/4 v2, 0x4

    invoke-virtual {p1, p2}, Landroid/os/Parcel;->writeInt(I)V

    .line 21
    iget-object p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_comment:Ljava/lang/String;

    .line 23
    invoke-virtual {p1, p2}, Landroid/os/Parcel;->writeString(Ljava/lang/String;)V

    .line 26
    const/4 v2, 0x2

    iget-boolean p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->isCollapsed:Z

    .line 28
    invoke-virtual {p1, p2}, Landroid/os/Parcel;->writeInt(I)V

    .line 31
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->disableLogging:Z

    .line 33
    invoke-virtual {p1, p0}, Landroid/os/Parcel;->writeInt(I)V

    .line 36
    return-void
.end method
