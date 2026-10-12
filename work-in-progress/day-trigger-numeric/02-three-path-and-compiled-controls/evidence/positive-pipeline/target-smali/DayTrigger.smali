.class public Lcom/arlosoft/macrodroid/triggers/DayTrigger;
.super Lcom/arlosoft/macrodroid/triggers/Trigger;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Lm57;
.implements La67;


# static fields
.field public static final CREATOR:Landroid/os/Parcelable$Creator;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Landroid/os/Parcelable$Creator<",
            "Lcom/arlosoft/macrodroid/triggers/DayTrigger;",
            ">;"
        }
    .end annotation
.end field

.field public static final DICTIONARY_KEYS_EXTRA:Ljava/lang/String; = "DictionaryKeys"

.field private static final EXTRA_ALARM_ID:Ljava/lang/String; = "alarmId"

.field private static final ID_SET_DAY_OF_MONTH:I = 0x2

.field private static final ID_SET_DAY_OF_WEEK:I = 0x1

.field public static final OPTION_DAY_OF_MONTH:I = 0x1

.field public static final OPTION_DAY_OF_WEEK:I = 0x0

.field public static final USE_VARIABLE_EXTRA:Ljava/lang/String; = "UseVariable"

.field public static final VARIABLE_NAME_EXTRA:Ljava/lang/String; = "VariableName"

.field private static final s_activeVariableTriggers:Ljava/util/Set;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Set<",
            "Lcom/arlosoft/macrodroid/triggers/DayTrigger;",
            ">;"
        }
    .end annotation
.end field

.field private static s_configuringTrigger:Lcom/arlosoft/macrodroid/triggers/DayTrigger; = null

.field private static s_uniqueId:I = 0x4e20

.field private static s_variableListenerCounter:I

.field private static s_variableUpdateListener:Lsxg;


# instance fields
.field private m_alarmId:Ljava/lang/String;

.field private transient m_alarmTrackerId:I

.field private m_dayOfMonth:I

.field private m_dayOfWeek:I

.field private m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

.field private m_hour:I

.field private transient m_localVariableUpdateListener:Lsxg;

.field private m_minute:I

.field private m_monthOfYear:I

.field private m_option:I

.field private final transient m_timeChangedReceiver:Lcom/arlosoft/macrodroid/triggers/c;

.field private m_useAlarm:Z

.field private m_useVariable:Z

.field private m_variableName:Ljava/lang/String;

.field private transient pendingIntent:Landroid/app/PendingIntent;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 1
    new-instance v0, Ljava/util/HashSet;

    .line 3
    invoke-direct {v0}, Ljava/util/HashSet;-><init>()V

    .line 6
    const/4 v1, 0x3

    sput-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_activeVariableTriggers:Ljava/util/Set;

    .line 8
    const/4 v1, 0x3

    new-instance v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger$a;

    .line 10
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/triggers/DayTrigger$a;-><init>()V

    .line 13
    sput-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->CREATOR:Landroid/os/Parcelable$Creator;

    .line 15
    return-void
.end method

.method private constructor <init>()V
    .locals 2

    .line 94
    invoke-direct {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;-><init>()V

    .line 95
    new-instance v0, Lcom/arlosoft/macrodroid/triggers/c;

    invoke-direct {v0, p0}, Lcom/arlosoft/macrodroid/triggers/c;-><init>(Lcom/arlosoft/macrodroid/triggers/DayTrigger;)V

    const/4 v1, 0x1

    iput-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_timeChangedReceiver:Lcom/arlosoft/macrodroid/triggers/c;

    const/4 v1, 0x7

    const/4 v0, 0x0

    .line 96
    const/4 v1, 0x0

    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    const/4 v0, 0x1

    .line 97
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    return-void
.end method

.method public constructor <init>(Landroid/app/Activity;Lcom/arlosoft/macrodroid/macro/Macro;)V
    .locals 1

    .line 98
    invoke-direct {p0}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;-><init>()V

    .line 99
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->setActivity(Landroid/app/Activity;)V

    .line 100
    const/4 v0, 0x2

    iput-object p2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    return-void
.end method

.method public constructor <init>(Landroid/os/Parcel;)V
    .locals 4

    .line 1
    invoke-direct {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;-><init>(Landroid/os/Parcel;)V

    .line 4
    const/4 v3, 0x4

    new-instance v0, Lcom/arlosoft/macrodroid/triggers/c;

    .line 6
    invoke-direct {v0, p0}, Lcom/arlosoft/macrodroid/triggers/c;-><init>(Lcom/arlosoft/macrodroid/triggers/DayTrigger;)V

    .line 9
    iput-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_timeChangedReceiver:Lcom/arlosoft/macrodroid/triggers/c;

    .line 11
    const/4 v0, 0x0

    .line 12
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 14
    const/4 v1, 0x1

    .line 15
    const/4 v3, 0x2

    iput-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 17
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 20
    move-result v2

    .line 21
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 23
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 26
    move-result v2

    .line 27
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 29
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 32
    move-result v2

    .line 33
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 35
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 38
    move-result v2

    .line 39
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 41
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 44
    move-result v2

    .line 45
    const/4 v3, 0x3

    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 47
    const/4 v3, 0x6

    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 50
    move-result v2

    .line 51
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 53
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 56
    move-result v2

    .line 57
    if-eqz v2, :cond_41

    .line 59
    const/4 v3, 0x7

    move v2, v1

    .line 60
    goto :goto_43

    .line 61
    :cond_41
    const/4 v3, 0x7

    move v2, v0

    .line 62
    :goto_43
    iput-boolean v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 64
    invoke-virtual {p1}, Landroid/os/Parcel;->readInt()I

    .line 67
    move-result v2

    .line 68
    if-eqz v2, :cond_4d

    .line 70
    const/4 v3, 0x5

    move v0, v1

    .line 71
    :cond_4d
    iput-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 73
    const/4 v3, 0x0

    invoke-virtual {p1}, Landroid/os/Parcel;->readString()Ljava/lang/String;

    .line 76
    move-result-object v0

    .line 77
    iput-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 79
    const-class v0, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 81
    invoke-virtual {v0}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;

    .line 84
    move-result-object v0

    .line 85
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;

    .line 88
    move-result-object p1

    .line 89
    check-cast p1, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 91
    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 93
    const/4 v3, 0x5

    return-void
.end method

.method public static o0()V
    .locals 2

    .line 1
    const-string v1, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    const/4 v0, 0x0

    .line 2
    sput-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_configuringTrigger:Lcom/arlosoft/macrodroid/triggers/DayTrigger;

    .line 4
    return-void
.end method

.method public static p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;
    .locals 3

    .line 1
    const/4 v2, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 4
    move-result-object p0

    .line 5
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    .line 8
    move-result-object p0

    .line 9
    :cond_9
    const/4 v2, 0x5

    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 12
    move-result v0

    .line 13
    if-eqz v0, :cond_21

    .line 15
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 18
    move-result-object v0

    .line 19
    check-cast v0, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 21
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;

    .line 24
    move-result-object v1

    .line 25
    invoke-virtual {p1, v1}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    .line 28
    move-result v1

    .line 29
    if-eqz v1, :cond_9

    .line 31
    return-object v0

    .line 32
    :cond_21
    const/4 p0, 0x0

    .line 33
    const/4 v2, 0x0

    return-object p0
.end method

.method public static q0()Lcom/arlosoft/macrodroid/triggers/DayTrigger;
    .locals 2

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_configuringTrigger:Lcom/arlosoft/macrodroid/triggers/DayTrigger;

    .line 3
    const/4 v1, 0x3

    return-object v0
.end method

.method public static r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I
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
    instance-of v0, p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    if-eqz v0, :cond_1c

    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;->getDecimalValue()D

    move-result-wide v0

    double-to-int p0, v0

    return p0

    :cond_1c
    const/4 p0, 0x0

    return p0
.end method

.method public static w0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V
    .locals 4

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_activeVariableTriggers:Ljava/util/Set;

    .line 3
    const/4 v3, 0x4

    monitor-enter v0

    .line 4
    :try_start_4
    invoke-interface {v0}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    .line 7
    move-result-object v1

    .line 8
    :goto_8
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 11
    move-result v2

    .line 12
    if-eqz v2, :cond_1c

    .line 14
    const/4 v3, 0x1

    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 17
    move-result-object v2

    .line 18
    check-cast v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;

    .line 20
    invoke-virtual {v2, p0}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->n0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V

    .line 23
    const/4 v3, 0x7

    goto :goto_8

    .line 24
    :catchall_1a
    move-exception p0

    .line 25
    goto :goto_1e

    .line 26
    :cond_1c
    monitor-exit v0

    .line 27
    return-void

    .line 28
    :goto_1e
    monitor-exit v0
    :try_end_1f
    .catchall {:try_start_4 .. :try_end_1f} :catchall_1a

    .line 29
    const/4 v3, 0x5

    throw p0
.end method


# virtual methods
.method public final X()V
    .locals 5

    .line 1
    const/4 v4, 0x0

    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 3
    const/4 v4, 0x4

    const/4 v1, 0x0

    .line 4
    if-eqz v0, :cond_44

    .line 6
    sget-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_activeVariableTriggers:Ljava/util/Set;

    .line 8
    monitor-enter v0

    .line 9
    :try_start_a
    const/4 v4, 0x7

    invoke-interface {v0, p0}, Ljava/util/Set;->remove(Ljava/lang/Object;)Z

    .line 12
    const/4 v4, 0x3

    sget v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableListenerCounter:I

    .line 14
    if-lez v2, :cond_1a

    .line 16
    add-int/lit8 v2, v2, -0x1

    .line 18
    sput v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableListenerCounter:I

    .line 20
    goto :goto_1a

    .line 21
    :catchall_18
    move-exception p0

    .line 22
    goto :goto_41

    .line 23
    :cond_1a
    :goto_1a
    if-nez v2, :cond_2d

    .line 25
    const/4 v4, 0x7

    sget-object v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableUpdateListener:Lsxg;

    .line 27
    if-eqz v2, :cond_2d

    .line 29
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 32
    move-result-object v2

    .line 33
    sget-object v3, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableUpdateListener:Lsxg;

    .line 35
    const/4 v4, 0x7

    invoke-virtual {v2, v3}, Lcom/arlosoft/macrodroid/common/a;->B(Lsxg;)V

    .line 38
    sput-object v1, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableUpdateListener:Lsxg;

    .line 40
    :cond_2d
    monitor-exit v0
    :try_end_2e
    .catchall {:try_start_a .. :try_end_2e} :catchall_18

    .line 41
    const/4 v4, 0x0

    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 43
    const/4 v4, 0x6

    if-eqz v0, :cond_44

    .line 45
    const/4 v4, 0x3

    iget-object v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_localVariableUpdateListener:Lsxg;

    .line 47
    if-eqz v2, :cond_44

    .line 49
    const/4 v4, 0x2

    invoke-virtual {v0, v2}, Lcom/arlosoft/macrodroid/macro/Macro;->removeLocalVariableUpdatedListener(Lsxg;)V

    .line 52
    const/4 v4, 0x5

    iput-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_localVariableUpdateListener:Lsxg;

    .line 54
    goto :goto_44

    .line 55
    :goto_41
    :try_start_41
    monitor-exit v0
    :try_end_42
    .catchall {:try_start_41 .. :try_end_42} :catchall_18

    .line 56
    const/4 v4, 0x6

    throw p0

    .line 57
    :cond_44
    :goto_44
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 60
    move-result-object v0

    .line 61
    const/4 v4, 0x4

    iget-object v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_timeChangedReceiver:Lcom/arlosoft/macrodroid/triggers/c;

    .line 63
    invoke-virtual {v0, v2}, Landroid/content/Context;->unregisterReceiver(Landroid/content/BroadcastReceiver;)V

    .line 66
    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 68
    if-eqz v0, :cond_68

    .line 70
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 73
    move-result-object v0

    .line 74
    const/4 v4, 0x7

    const-string v2, "alarm"

    .line 76
    const/4 v4, 0x0

    invoke-virtual {v0, v2}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 79
    move-result-object v0

    .line 80
    check-cast v0, Landroid/app/AlarmManager;

    .line 82
    iget-object v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 84
    invoke-virtual {v0, v2}, Landroid/app/AlarmManager;->cancel(Landroid/app/PendingIntent;)V

    .line 87
    const/4 v4, 0x3

    iput-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 89
    :cond_68
    iput-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 91
    return-void
.end method

.method public final a0()V
    .locals 6

    .line 1
    const/4 v5, 0x0

    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 3
    if-nez v0, :cond_10

    .line 5
    invoke-static {}, Ljava/util/UUID;->randomUUID()Ljava/util/UUID;

    .line 8
    move-result-object v0

    .line 9
    invoke-virtual {v0}, Ljava/util/UUID;->toString()Ljava/lang/String;

    .line 12
    move-result-object v0

    .line 13
    const/4 v5, 0x7

    iput-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 15
    :cond_10
    const/4 v5, 0x5

    sget v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_uniqueId:I

    .line 17
    add-int/lit8 v1, v0, 0x1

    .line 19
    sput v1, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_uniqueId:I

    .line 21
    const/4 v5, 0x2

    iput v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmTrackerId:I

    .line 23
    const/4 v5, 0x3

    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 25
    const/4 v5, 0x7

    const/4 v1, 0x1

    .line 26
    const/4 v5, 0x7

    if-eqz v0, :cond_5b

    .line 28
    const/4 v5, 0x6

    sget-object v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_activeVariableTriggers:Ljava/util/Set;

    .line 30
    monitor-enter v0

    .line 31
    :try_start_26
    invoke-interface {v0, p0}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 34
    sget v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableListenerCounter:I

    .line 36
    const/4 v3, 0x0

    .line 37
    if-nez v2, :cond_44

    .line 39
    new-instance v2, Lo44;

    .line 41
    invoke-direct {v2, v3}, Lo44;-><init>(I)V

    .line 44
    sput-object v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableUpdateListener:Lsxg;

    .line 46
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 49
    move-result-object v2

    .line 50
    const/4 v5, 0x0

    sget-object v4, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableUpdateListener:Lsxg;

    .line 52
    const/4 v5, 0x6

    invoke-virtual {v2, v4}, Lcom/arlosoft/macrodroid/common/a;->b(Lsxg;)V

    .line 55
    goto :goto_44

    .line 56
    :catchall_41
    move-exception p0

    .line 57
    const/4 v5, 0x0

    goto :goto_59

    .line 58
    :cond_44
    :goto_44
    sget v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableListenerCounter:I

    .line 60
    add-int/2addr v2, v1

    .line 61
    sput v2, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_variableListenerCounter:I

    .line 63
    monitor-exit v0
    :try_end_4a
    .catchall {:try_start_26 .. :try_end_4a} :catchall_41

    .line 64
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 66
    if-eqz v0, :cond_5b

    .line 68
    new-instance v2, Lp44;

    .line 70
    invoke-direct {v2, p0, v3}, Lp44;-><init>(Ljava/lang/Object;I)V

    .line 73
    iput-object v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_localVariableUpdateListener:Lsxg;

    .line 75
    invoke-virtual {v0, v2}, Lcom/arlosoft/macrodroid/macro/Macro;->addLocalVariableUpdatedListener(Lsxg;)V

    .line 78
    goto :goto_5b

    .line 79
    :goto_59
    :try_start_59
    monitor-exit v0
    :try_end_5a
    .catchall {:try_start_59 .. :try_end_5a} :catchall_41

    .line 80
    throw p0

    .line 81
    :cond_5b
    :goto_5b
    new-instance v0, Landroid/content/IntentFilter;

    .line 83
    const-string v2, "nEsieMrt_idEctta.d.SnoonanT.IT"

    const-string v2, "android.intent.action.TIME_SET"

    .line 85
    const/4 v5, 0x4

    invoke-direct {v0, v2}, Landroid/content/IntentFilter;-><init>(Ljava/lang/String;)V

    .line 88
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 91
    move-result-object v2

    .line 92
    iget-object v3, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_timeChangedReceiver:Lcom/arlosoft/macrodroid/triggers/c;

    .line 94
    const/4 v4, 0x2

    .line 95
    invoke-static {v2, v3, v0, v4}, Lw63;->registerReceiver(Landroid/content/Context;Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;I)Landroid/content/Intent;

    .line 98
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->y0(Z)V

    .line 101
    const/4 v5, 0x5

    return-void
.end method

.method public final b()Lcom/arlosoft/macrodroid/variables/DictionaryKeys;
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 3
    return-object p0
.end method

.method public final getCheckedItemIndex()I
    .locals 1

    .line 1
    const/4 v0, 0x4

    iget p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 3
    const/4 v0, 0x1

    return p0
.end method

.method public final getConfiguredName()Ljava/lang/String;
    .locals 1

    .line 1
    iget p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 3
    if-nez p0, :cond_d

    .line 5
    const/4 v0, 0x5

    const p0, 0x7f1415f0

    .line 8
    invoke-static {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 11
    move-result-object p0

    .line 12
    return-object p0

    .line 13
    :cond_d
    const p0, 0x7f1415ef

    .line 16
    invoke-static {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 19
    move-result-object p0

    .line 20
    return-object p0
.end method

.method public final getExtendedDetail()Ljava/lang/String;
    .locals 15

    .line 1
    const/4 v14, 0x0

    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 3
    if-eqz v0, :cond_1b

    .line 5
    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 7
    if-eqz v0, :cond_1b

    .line 9
    new-instance v0, Ljava/lang/StringBuilder;

    .line 11
    const/4 v14, 0x1

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 14
    iget-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 16
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 19
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 21
    invoke-static {p0, v0}, Liu1;->o(Lcom/arlosoft/macrodroid/variables/DictionaryKeys;Ljava/lang/StringBuilder;)Ljava/lang/String;

    .line 24
    move-result-object p0

    .line 25
    return-object p0

    .line 26
    :cond_1b
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 28
    const/4 v1, 0x0

    .line 29
    const/4 v2, 0x1

    .line 30
    const-string v3, ":"

    .line 32
    const-string v4, " "

    .line 34
    const/4 v14, 0x7

    const-string v5, "%02d"

    .line 36
    if-nez v0, :cond_87

    .line 38
    const/4 v14, 0x1

    new-instance v0, Ljava/lang/StringBuilder;

    .line 40
    const/4 v14, 0x1

    iget v6, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 42
    const/4 v14, 0x3

    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 45
    move-result-object v7

    .line 46
    const/4 v12, 0x0

    .line 47
    const/4 v13, 0x4

    const/4 v13, 0x0

    .line 48
    const/16 v8, 0x7db

    .line 50
    const/4 v14, 0x2

    const/4 v9, 0x7

    .line 51
    const/4 v14, 0x6

    const/4 v10, 0x1

    .line 52
    const/4 v14, 0x4

    const/4 v11, 0x0

    .line 53
    invoke-virtual/range {v7 .. v13}, Ljava/util/Calendar;->set(IIIIII)V

    .line 56
    const/4 v8, 0x5

    or-int/2addr v14, v8

    .line 57
    invoke-virtual {v7, v8, v6}, Ljava/util/Calendar;->add(II)V

    .line 60
    new-array v6, v2, [Ljava/lang/Object;

    .line 62
    const/4 v14, 0x7

    aput-object v7, v6, v1

    .line 64
    const/4 v14, 0x3

    const-string v7, "%tA"

    .line 66
    invoke-static {v7, v6}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 69
    move-result-object v6

    .line 70
    invoke-direct {v0, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 73
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 76
    iget v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 78
    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 81
    move-result-object v4

    .line 82
    const/4 v14, 0x6

    new-array v6, v2, [Ljava/lang/Object;

    .line 84
    const/4 v14, 0x7

    aput-object v4, v6, v1

    .line 86
    invoke-static {v5, v6}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 89
    move-result-object v4

    .line 90
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 93
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 96
    const/4 v14, 0x5

    iget p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 98
    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 101
    move-result-object p0

    .line 102
    new-array v2, v2, [Ljava/lang/Object;

    .line 104
    aput-object p0, v2, v1

    .line 106
    const/4 v14, 0x6

    invoke-static {v5, v2}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 109
    move-result-object p0

    .line 110
    const/4 v14, 0x3

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 113
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 116
    move-result-object p0

    .line 117
    return-object p0

    .line 118
    :cond_87
    const/4 v14, 0x1

    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 120
    if-nez v0, :cond_96

    .line 122
    const v0, 0x7f1409f7

    .line 125
    const/4 v14, 0x2

    invoke-static {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getString(I)Ljava/lang/String;

    .line 128
    move-result-object v0

    .line 129
    const/4 v14, 0x3

    goto :goto_a0

    .line 130
    :cond_96
    invoke-static {}, Le44;->a()[Ljava/lang/String;

    .line 133
    move-result-object v0

    .line 134
    const/4 v14, 0x6

    iget v6, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 136
    sub-int/2addr v6, v2

    .line 137
    aget-object v0, v0, v6

    .line 139
    :goto_a0
    new-instance v6, Ljava/lang/StringBuilder;

    .line 141
    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    .line 144
    iget v7, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 146
    const-string v8, " ("

    .line 148
    invoke-static {v7, v4, v0, v8, v6}, Lni9;->y(ILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 151
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 153
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 156
    move-result-object v0

    .line 157
    new-array v4, v2, [Ljava/lang/Object;

    .line 159
    aput-object v0, v4, v1

    .line 161
    invoke-static {v5, v4}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 164
    move-result-object v0

    .line 165
    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 168
    invoke-virtual {v6, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 171
    iget p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 173
    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 176
    move-result-object p0

    .line 177
    new-array v0, v2, [Ljava/lang/Object;

    .line 179
    aput-object p0, v0, v1

    .line 181
    invoke-static {v5, v0}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    .line 184
    move-result-object p0

    .line 185
    invoke-virtual {v6, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 188
    const-string p0, ")"

    const-string p0, ")"

    .line 190
    const/4 v14, 0x4

    invoke-virtual {v6, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 193
    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 196
    move-result-object p0

    .line 197
    return-object p0
.end method

.method public final getInfo()Lk2e;
    .locals 1

    .line 1
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DayTriggerInfo;->getInstance()Lk2e;

    .line 4
    move-result-object p0

    .line 5
    return-object p0
.end method

.method public final getListModeName()Ljava/lang/String;
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->getExtendedDetail()Ljava/lang/String;

    .line 4
    move-result-object p0

    .line 5
    const/4 v0, 0x6

    return-object p0
.end method

.method public final getPermissions()[Ljava/lang/String;
    .locals 3

    .line 1
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 3
    const/16 v1, 0x1f

    .line 5
    if-lt v0, v1, :cond_a

    .line 7
    const/4 p0, 0x0

    .line 8
    new-array p0, p0, [Ljava/lang/String;

    .line 10
    return-object p0

    .line 11
    :cond_a
    invoke-super {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getPermissions()[Ljava/lang/String;

    .line 14
    move-result-object p0

    .line 15
    return-object p0
.end method

.method public final getSecondaryOptions()[Ljava/lang/String;
    .locals 3

    .line 1
    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 4
    move-result-object p0

    .line 5
    const v0, 0x7f1415f0

    .line 8
    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 11
    move-result-object p0

    .line 12
    const/4 v2, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/app/MacroDroidApplication;->i()Lcom/arlosoft/macrodroid/app/MacroDroidApplication;

    .line 15
    move-result-object v0

    .line 16
    const v1, 0x7f1415ef

    .line 19
    invoke-virtual {v0, v1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 22
    move-result-object v0

    .line 23
    const/4 v2, 0x2

    filled-new-array {p0, v0}, [Ljava/lang/String;

    .line 26
    move-result-object p0

    .line 27
    return-object p0
.end method

.method public final getVariableNames()[Ljava/lang/String;
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 3
    filled-new-array {p0}, [Ljava/lang/String;

    .line 6
    move-result-object p0

    .line 7
    const/4 v0, 0x6

    return-object p0
.end method

.method public final getVariableTypes()[Ljava/lang/Integer;
    .locals 3

    .line 1
    const/4 v2, 0x6

    const/4 p0, 0x4

    .line 2
    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 5
    move-result-object p0

    .line 6
    const/4 v2, 0x4

    const/4 v0, 0x1

    .line 7
    new-array v0, v0, [Ljava/lang/Integer;

    .line 9
    const/4 v1, 0x0

    .line 10
    aput-object p0, v0, v1

    .line 12
    const/4 v2, 0x6

    return-object v0
.end method

.method public final handleActivityResult(Landroid/app/Activity;IILandroid/content/Intent;)V
    .locals 9

    .line 1
    const/4 v8, 0x2

    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->setActivity(Landroid/app/Activity;)V

    .line 4
    const/4 p1, 0x0

    .line 5
    sput-object p1, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_configuringTrigger:Lcom/arlosoft/macrodroid/triggers/DayTrigger;

    .line 7
    const/4 p1, 0x0

    const/4 p1, 0x1

    .line 8
    const-string v0, "DictionaryKeys"

    .line 10
    const-string v1, "VariableName"

    .line 12
    const-string v2, "rUimaesaVbe"

    const-string v2, "UseVariable"

    .line 14
    const/4 v8, 0x2

    const-string v3, "lsmAorUa"

    const-string v3, "UseAlarm"

    .line 16
    const-string v4, "Minute"

    .line 18
    const/4 v8, 0x3

    const-string v5, "Hour"

    .line 20
    const/4 v6, -0x1

    .line 21
    const/4 v8, 0x6

    const/4 v7, 0x0

    .line 22
    if-ne p2, p1, :cond_57

    .line 24
    if-ne p3, v6, :cond_57

    .line 26
    invoke-virtual {p4, v5, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 29
    move-result p1

    .line 30
    const/4 v8, 0x6

    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 32
    invoke-virtual {p4, v4, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 35
    move-result p1

    .line 36
    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 38
    const-string p1, "DayOfWeek"

    .line 40
    invoke-virtual {p4, p1, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 43
    move-result p1

    .line 44
    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 46
    iget-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 48
    invoke-virtual {p4, v3, p1}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 51
    move-result p1

    .line 52
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 54
    invoke-virtual {p4, v2, v7}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 57
    move-result p1

    .line 58
    const/4 v8, 0x2

    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 60
    invoke-virtual {p4, v1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 63
    move-result-object p1

    .line 64
    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 66
    invoke-virtual {p4, v0}, Landroid/content/Intent;->getParcelableExtra(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 69
    move-result-object p1

    .line 70
    check-cast p1, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 72
    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 74
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->itemComplete()V

    .line 77
    :cond_57
    const/4 v8, 0x3

    const/4 p1, 0x2

    .line 78
    if-ne p2, p1, :cond_a1

    .line 80
    if-ne p3, v6, :cond_a1

    .line 82
    invoke-virtual {p4, v5, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 85
    move-result p1

    .line 86
    const/4 v8, 0x0

    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 88
    invoke-virtual {p4, v4, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 91
    move-result p1

    .line 92
    const/4 v8, 0x3

    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 94
    const/4 v8, 0x3

    const-string p1, "DayOfMonth"

    .line 96
    const/4 v8, 0x3

    invoke-virtual {p4, p1, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 99
    move-result p1

    .line 100
    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 102
    const-string p1, "MonthOfYear"

    .line 104
    const/4 v8, 0x4

    invoke-virtual {p4, p1, v7}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    .line 107
    move-result p1

    .line 108
    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 110
    iget-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 112
    invoke-virtual {p4, v3, p1}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 115
    move-result p1

    .line 116
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 118
    invoke-virtual {p4, v2, v7}, Landroid/content/Intent;->getBooleanExtra(Ljava/lang/String;Z)Z

    .line 121
    move-result p1

    .line 122
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 124
    invoke-virtual {p4, v1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    .line 127
    move-result-object p1

    .line 128
    const/4 v8, 0x7

    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 130
    const/4 v8, 0x3

    invoke-virtual {p4, v0}, Landroid/content/Intent;->getParcelableExtra(Ljava/lang/String;)Landroid/os/Parcelable;

    .line 133
    move-result-object p1

    .line 134
    const/4 v8, 0x5

    check-cast p1, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 136
    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 138
    const/4 v8, 0x2

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->itemComplete()V

    .line 141
    :cond_a1
    const/4 v8, 0x5

    return-void
.end method

.method public final j(Lcom/arlosoft/macrodroid/variables/DictionaryKeys;)V
    .locals 1

    .line 1
    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 3
    const/4 v0, 0x3

    return-void
.end method

.method public final n0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)V
    .locals 3

    .line 1
    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 3
    const/4 v2, 0x4

    if-eqz v0, :cond_41

    .line 5
    const/4 v2, 0x5

    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 7
    if-nez v0, :cond_c

    .line 9
    const/4 v2, 0x2

    goto :goto_41

    .line 10
    :cond_c
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 13
    move-result-object p1

    .line 14
    const/4 v2, 0x1

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    .line 17
    move-result p1

    .line 18
    const/4 v2, 0x3

    if-nez p1, :cond_19

    .line 20
    goto :goto_41

    .line 21
    :cond_19
    new-instance p1, Ljava/lang/StringBuilder;

    .line 23
    const/4 v2, 0x3

    const-string v0, "Day of Week/Month trigger rescheduling due to variable \'"

    .line 25
    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 28
    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 30
    const-string v1, "eh /gban/"

    const-string v1, "\' change"

    .line 32
    invoke-static {v0, v1, p1}, Lq77;->B(Ljava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)Ljava/lang/String;

    .line 35
    move-result-object p1

    .line 36
    const/4 v2, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 39
    move-result-object v0

    .line 40
    const/4 v2, 0x3

    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 43
    move-result-wide v0

    .line 44
    const/4 v2, 0x3

    invoke-static {v0, v1, p1}, Lkjf;->m(JLjava/lang/String;)V

    .line 47
    iget-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 49
    if-eqz p1, :cond_41

    .line 51
    const/4 p1, 0x1

    .line 52
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->y0(Z)V

    .line 55
    :cond_41
    :goto_41
    return-void
.end method

.method public final requiresScheduleExactAlarm()Z
    .locals 1

    .line 1
    const/4 p0, 0x1

    .line 2
    return p0
.end method

.method public final secondaryItemConfirmed()V
    .locals 11

    .line 1
    sput-object p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->s_configuringTrigger:Lcom/arlosoft/macrodroid/triggers/DayTrigger;

    .line 3
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 6
    move-result-object v0

    .line 7
    iget v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 9
    const/4 v10, 0x1

    const-string v2, "DictionaryKeys"

    .line 11
    const-string v3, "VariableName"

    .line 13
    const-string v4, "UseVariable"

    .line 15
    const/4 v10, 0x3

    const-string v5, "UseAlarm"

    .line 17
    const-string v6, "Minute"

    .line 19
    const-string v7, "Hour"

    .line 21
    if-nez v1, :cond_4f

    .line 23
    new-instance v1, Landroid/content/Intent;

    .line 25
    const-class v8, Lcom/arlosoft/macrodroid/triggers/activities/DayOfWeekConfigureActivity;

    .line 27
    invoke-direct {v1, v0, v8}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 30
    const-string v8, "DayOfWeek"

    .line 32
    const/4 v10, 0x5

    iget v9, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 34
    invoke-virtual {v1, v8, v9}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 37
    iget v8, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 39
    invoke-virtual {v1, v7, v8}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 42
    const/4 v10, 0x0

    iget v7, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 44
    invoke-virtual {v1, v6, v7}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 47
    iget-boolean v6, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 49
    invoke-virtual {v1, v5, v6}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 52
    iget-boolean v5, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 54
    invoke-virtual {v1, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 57
    iget-object v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 59
    invoke-virtual {v1, v3, v4}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 62
    const/4 v10, 0x2

    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 64
    const/4 v10, 0x0

    invoke-virtual {v1, v2, p0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 67
    const/4 p0, 0x4

    const/4 p0, 0x1

    .line 68
    const/4 v10, 0x4

    invoke-virtual {v0, v1, p0}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V

    .line 71
    return-void

    .line 72
    :cond_4f
    const/4 v10, 0x1

    new-instance v1, Landroid/content/Intent;

    .line 74
    const/4 v10, 0x2

    const-class v8, Lcom/arlosoft/macrodroid/triggers/activities/DayOfMonthConfigureActivity;

    .line 76
    const/4 v10, 0x7

    invoke-direct {v1, v0, v8}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 79
    const-string v8, "DohfaMunOy"

    const-string v8, "DayOfMonth"

    .line 81
    const/4 v10, 0x3

    iget v9, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 83
    invoke-virtual {v1, v8, v9}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 86
    const-string v8, "MonthOfYear"

    .line 88
    const/4 v10, 0x4

    iget v9, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 90
    invoke-virtual {v1, v8, v9}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 93
    const/4 v10, 0x0

    iget v8, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 95
    invoke-virtual {v1, v7, v8}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 98
    const/4 v10, 0x0

    iget v7, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 100
    const/4 v10, 0x6

    invoke-virtual {v1, v6, v7}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 103
    iget-boolean v6, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 105
    invoke-virtual {v1, v5, v6}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 108
    iget-boolean v5, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 110
    invoke-virtual {v1, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 113
    iget-object v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 115
    invoke-virtual {v1, v3, v4}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 118
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 120
    invoke-virtual {v1, v2, p0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 123
    const/4 p0, 0x2

    .line 124
    const/4 v10, 0x0

    invoke-virtual {v0, v1, p0}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V

    .line 127
    const/4 v10, 0x6

    return-void
.end method

.method public final secondaryItemSelected(I)V
    .locals 1

    .line 1
    iput p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 3
    return-void
.end method

.method public final setVariableNames([Ljava/lang/String;)V
    .locals 2

    .line 1
    array-length v0, p1

    .line 2
    if-lez v0, :cond_b

    .line 4
    const/4 v0, 0x0

    .line 5
    aget-object p1, p1, v0

    .line 7
    if-eqz p1, :cond_b

    .line 9
    const/4 v1, 0x3

    iput-object p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 11
    :cond_b
    return-void
.end method

.method public final t0()Ljava/lang/String;
    .locals 1

    .line 1
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 3
    return-object p0
.end method

.method public final v0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;
    .locals 5

    .line 1
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->R()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 4
    move-result-object v0

    .line 5
    instance-of v1, v0, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 7
    const/4 v2, 0x0

    .line 8
    if-nez v1, :cond_a

    .line 10
    goto :goto_4f

    .line 11
    :cond_a
    iget-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 13
    if-eqz v1, :cond_14

    .line 15
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;->getKeys()Ljava/util/List;

    .line 18
    move-result-object v1

    .line 19
    const/4 v4, 0x4

    goto :goto_16

    .line 20
    :cond_14
    move-object v1, v2

    move-object v1, v2

    .line 21
    :goto_16
    if-eqz v1, :cond_51

    .line 23
    invoke-interface {v1}, Ljava/util/List;->isEmpty()Z

    .line 26
    move-result v3

    .line 27
    if-eqz v3, :cond_1f

    .line 29
    goto :goto_51

    .line 30
    :cond_1f
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 33
    move-result-object v0

    .line 34
    iget-object v3, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 36
    if-eqz v3, :cond_2d

    .line 38
    const/4 v4, 0x1

    invoke-virtual {v3}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerContextInfo()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 41
    move-result-object v3

    .line 42
    goto :goto_2f

    .line 43
    :cond_2d
    move-object v3, v2

    move-object v3, v2

    .line 44
    :goto_2f
    const/4 v4, 0x2

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 46
    invoke-static {v0, v1, v3, p0}, Lcom/arlosoft/macrodroid/variables/n;->a(Landroid/content/Context;Ljava/util/List;Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Lcom/arlosoft/macrodroid/macro/Macro;)Ljava/util/ArrayList;

    .line 49
    move-result-object p0

    .line 50
    const/4 v0, 0x0

    .line 51
    invoke-virtual {p1, p0, v0}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->M(Ljava/util/List;Z)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 54
    move-result-object p0

    .line 55
    const/4 v4, 0x3

    if-eqz p0, :cond_4f

    .line 57
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 60
    move-result-object p1

    .line 61
    const/4 v4, 0x3

    instance-of p1, p1, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 63
    if-eqz p1, :cond_4f

    .line 65
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 68
    move-result-object p0

    .line 69
    check-cast p0, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 71
    const/4 v4, 0x4

    return-object p0

    .line 72
    :cond_4f
    :goto_4f
    const/4 v4, 0x2

    return-object v2

    .line 73
    :cond_51
    :goto_51
    check-cast v0, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 75
    return-object v0
.end method

.method public final validate()V
    .locals 6

    .line 1
    invoke-super {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->validate()V

    .line 4
    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 6
    const-string v1, "MacroDroid"

    .line 8
    if-nez v0, :cond_1b

    .line 10
    const/4 v5, 0x5

    const-string v0, "DayTrigger: m_dictionaryKeys was null, defaulting to new DictionaryKeys()"

    .line 12
    invoke-static {v1, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I

    .line 15
    new-instance v0, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 17
    new-instance v2, Ljava/util/ArrayList;

    .line 19
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 22
    invoke-direct {v0, v2}, Lcom/arlosoft/macrodroid/variables/DictionaryKeys;-><init>(Ljava/util/List;)V

    .line 25
    iput-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 27
    :cond_1b
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 29
    const/4 v2, 0x0

    .line 30
    if-ltz v0, :cond_24

    .line 32
    const/4 v3, 0x1

    const/4 v3, 0x1

    .line 33
    if-le v0, v3, :cond_34

    .line 35
    :cond_24
    new-instance v0, Ljava/lang/StringBuilder;

    .line 37
    const-string v3, "DayTrigger: m_option was out of range ("

    .line 39
    invoke-direct {v0, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 42
    iget v3, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 44
    const-string v4, "), defaulting to OPTION_DAY_OF_WEEK"

    .line 46
    invoke-static {v3, v4, v1, v0}, Liu1;->w(ILjava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 49
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 51
    :cond_34
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 53
    const-string v3, ")lan,t0p tg o ueif"

    const-string v3, "), defaulting to 0"

    .line 55
    if-ltz v0, :cond_41

    .line 57
    const/16 v4, 0x17

    .line 59
    const/4 v5, 0x5

    if-le v0, v4, :cond_51

    .line 61
    :cond_41
    new-instance v0, Ljava/lang/StringBuilder;

    .line 63
    const-string v4, "DayTrigger: m_hour was out of range ("

    .line 65
    const/4 v5, 0x2

    invoke-direct {v0, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 68
    const/4 v5, 0x7

    iget v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 70
    invoke-static {v4, v3, v1, v0}, Liu1;->w(ILjava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 73
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 75
    :cond_51
    const/4 v5, 0x4

    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 77
    const/4 v5, 0x5

    if-ltz v0, :cond_5b

    .line 79
    const/16 v4, 0x3b

    .line 81
    if-le v0, v4, :cond_6a

    .line 83
    :cond_5b
    const/4 v5, 0x6

    new-instance v0, Ljava/lang/StringBuilder;

    .line 85
    const-string v4, "DayTrigger: m_minute was out of range ("

    .line 87
    invoke-direct {v0, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 90
    iget v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 92
    invoke-static {v4, v3, v1, v0}, Liu1;->w(ILjava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 95
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 97
    :cond_6a
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 99
    if-ltz v0, :cond_71

    .line 101
    const/4 v4, 0x6

    .line 102
    if-le v0, v4, :cond_82

    .line 104
    :cond_71
    new-instance v0, Ljava/lang/StringBuilder;

    .line 106
    const-string v4, "m  rwWeoqdtaynf:igegaOgs uroDeTf( eaakry _"

    const-string v4, "DayTrigger: m_dayOfWeek was out of range ("

    .line 108
    const/4 v5, 0x3

    invoke-direct {v0, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 111
    iget v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 113
    invoke-static {v4, v3, v1, v0}, Liu1;->w(ILjava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 116
    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 118
    :cond_82
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 120
    if-ltz v0, :cond_8c

    .line 122
    const/16 v4, 0xc

    .line 124
    if-le v0, v4, :cond_8b

    .line 126
    goto :goto_8c

    .line 127
    :cond_8b
    return-void

    .line 128
    :cond_8c
    :goto_8c
    new-instance v0, Ljava/lang/StringBuilder;

    .line 130
    const/4 v5, 0x6

    const-string v4, "DayTrigger: m_monthOfYear was out of range ("

    .line 132
    invoke-direct {v0, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 135
    iget v4, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 137
    invoke-static {v4, v3, v1, v0}, Liu1;->w(ILjava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)V

    .line 140
    const/4 v5, 0x6

    iput v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 142
    return-void
.end method

.method public final writeToParcel(Landroid/os/Parcel;I)V
    .locals 2

    .line 1
    invoke-super {p0, p1, p2}, Lcom/arlosoft/macrodroid/common/SelectableItem;->writeToParcel(Landroid/os/Parcel;I)V

    .line 4
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 6
    const/4 v1, 0x5

    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 9
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 11
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 14
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 16
    const/4 v1, 0x7

    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 19
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 21
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 24
    const/4 v1, 0x1

    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 26
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 29
    iget v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 31
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 34
    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 36
    const/4 v1, 0x6

    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 39
    const/4 v1, 0x2

    iget-boolean v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 41
    const/4 v1, 0x3

    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeInt(I)V

    .line 44
    iget-object v0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 46
    invoke-virtual {p1, v0}, Landroid/os/Parcel;->writeString(Ljava/lang/String;)V

    .line 49
    const/4 v1, 0x4

    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 51
    invoke-virtual {p1, p0, p2}, Landroid/os/Parcel;->writeParcelable(Landroid/os/Parcelable;I)V

    .line 54
    return-void
.end method

.method public final x0(Landroid/content/Context;Ljava/lang/String;J)V
    .locals 7

    .line 1
    const-string v0, "rmsal"

    const-string v0, "alarm"

    .line 3
    :try_start_4
    iget-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 5
    const/4 v6, 0x6

    if-eqz v1, :cond_20

    .line 7
    const/4 v6, 0x0

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 10
    move-result-object v1

    .line 11
    const/4 v6, 0x2

    invoke-virtual {v1, v0}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 14
    move-result-object v1

    .line 15
    const/4 v6, 0x4

    check-cast v1, Landroid/app/AlarmManager;

    .line 17
    iget-object v2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 19
    const/4 v6, 0x0

    invoke-virtual {v1, v2}, Landroid/app/AlarmManager;->cancel(Landroid/app/PendingIntent;)V

    .line 22
    const/4 v6, 0x3

    const/4 v1, 0x0

    .line 23
    iput-object v1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;
    :try_end_20
    .catch Ljava/lang/Exception; {:try_start_4 .. :try_end_20} :catch_20

    .line 25
    :catch_20
    :cond_20
    const/4 v6, 0x0

    new-instance v1, Ljava/lang/StringBuilder;

    .line 27
    const/4 v6, 0x1

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 30
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroName()Ljava/lang/String;

    .line 33
    move-result-object v2

    .line 34
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 37
    const-string v2, " - Scheduling next wakeup for "

    .line 39
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 42
    const/4 v6, 0x3

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 45
    move-result-wide v2

    .line 46
    sub-long v2, p3, v2

    .line 48
    const-wide/16 v4, 0x3e8

    .line 50
    div-long/2addr v2, v4

    .line 51
    const/4 v6, 0x2

    const-string v4, "s"

    .line 53
    invoke-static {v2, v3, v4, v1}, Lni9;->r(JLjava/lang/String;Ljava/lang/StringBuilder;)Ljava/lang/String;

    .line 56
    move-result-object v1

    .line 57
    const/4 v6, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 60
    move-result-object v2

    .line 61
    invoke-virtual {v2}, Ljava/lang/Long;->longValue()J

    .line 64
    move-result-wide v2

    .line 65
    invoke-static {v2, v3, v1}, Lkjf;->q(JLjava/lang/String;)V

    .line 68
    const/4 v6, 0x3

    new-instance v1, Landroid/content/Intent;

    .line 70
    const-class v2, Lcom/arlosoft/macrodroid/triggers/receivers/DayTriggerReceiver;

    .line 72
    const/4 v6, 0x6

    invoke-direct {v1, p1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 75
    const/4 v6, 0x1

    const-string v2, "alarmId"

    .line 77
    const/4 v6, 0x1

    invoke-virtual {v1, v2, p2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 80
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 83
    move-result-object p2

    .line 84
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 87
    move-result-wide v2

    .line 88
    long-to-int v2, v2

    .line 89
    const/high16 v3, 0x8000000

    .line 91
    const/4 v6, 0x3

    sget v4, Lsmb;->a:I

    .line 93
    or-int/2addr v3, v4

    .line 94
    invoke-static {p2, v2, v1, v3}, Landroid/app/PendingIntent;->getBroadcast(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;

    .line 97
    move-result-object p2

    .line 98
    iput-object p2, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 100
    invoke-virtual {p1, v0}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 103
    move-result-object p1

    .line 104
    const/4 v6, 0x3

    check-cast p1, Landroid/app/AlarmManager;

    .line 106
    iget-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useAlarm:Z

    .line 108
    iget-object p0, p0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->pendingIntent:Landroid/app/PendingIntent;

    .line 110
    invoke-static {p3, p4, p1, p0}, Lpo;->d(JZLandroid/app/PendingIntent;)Z

    .line 113
    return-void
.end method

.method public final y0(Z)V
    .locals 22

    .line 1
    move-object/from16 v0, p0

    .line 3
    iget-boolean v1, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 5
    const/16 v2, 0xc

    .line 7
    const/4 v3, 0x7

    .line 8
    const/4 v4, 0x0

    .line 9
    const/4 v5, 0x1

    .line 10
    if-eqz v1, :cond_242

    .line 12
    if-eqz v1, :cond_3a

    .line 14
    iget-object v1, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 16
    if-nez v1, :cond_12

    .line 18
    goto :goto_3a

    .line 19
    :cond_12
    iget-object v7, v0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 21
    if-eqz v7, :cond_1b

    .line 23
    invoke-virtual {v7, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 26
    move-result-object v1

    .line 27
    goto :goto_1c

    .line 28
    :cond_1b
    const/4 v1, 0x0

    .line 29
    :goto_1c
    const-string v7, "rl/myk Ma /obaaWi/Dfhve oete "

    const-string v7, "Day of Week/Month variable \'"

    .line 31
    if-nez v1, :cond_3c

    .line 33
    new-instance v1, Ljava/lang/StringBuilder;

    .line 35
    invoke-direct {v1, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 38
    iget-object v7, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 40
    const-string v8, "\' not found"

    .line 42
    invoke-static {v7, v8, v1}, Lq77;->B(Ljava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)Ljava/lang/String;

    .line 45
    move-result-object v1

    .line 46
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 49
    move-result-object v7

    .line 50
    invoke-virtual {v7}, Ljava/lang/Long;->longValue()J

    .line 53
    move-result-wide v7

    .line 54
    invoke-static {v7, v8, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 57
    :cond_3a
    :goto_3a
    const/4 v1, 0x0

    .line 58
    goto :goto_9e

    .line 59
    :cond_3c
    invoke-virtual {v0, v1}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->v0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 62
    move-result-object v1

    .line 63
    if-nez v1, :cond_6a

    .line 65
    new-instance v1, Ljava/lang/StringBuilder;

    .line 67
    invoke-direct {v1, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 70
    iget-object v7, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 72
    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 75
    iget-object v7, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dictionaryKeys:Lcom/arlosoft/macrodroid/variables/DictionaryKeys;

    .line 77
    invoke-static {v7}, Lcom/arlosoft/macrodroid/variables/n;->s(Lcom/arlosoft/macrodroid/variables/DictionaryKeys;)Ljava/lang/String;

    .line 80
    move-result-object v7

    .line 81
    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 84
    const-string v7, "\' is not a dictionary or path not found"

    .line 86
    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 89
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 92
    move-result-object v1

    .line 93
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 96
    move-result-object v7

    .line 97
    invoke-virtual {v7}, Ljava/lang/Long;->longValue()J

    .line 100
    move-result-wide v7

    .line 101
    invoke-static {v7, v8, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 104
    goto :goto_3a

    .line 105
    :cond_6a
    const-string v7, "hour"

    .line 107
    invoke-static {v1, v7}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 110
    move-result-object v7

    .line 111
    const-string v8, "minute"

    .line 113
    invoke-static {v1, v8}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 116
    move-result-object v1

    .line 117
    if-eqz v7, :cond_7d

    .line 119
    invoke-static {v7}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I

    .line 122
    move-result v7

    .line 123
    goto :goto_7e

    .line 124
    :cond_7d
    move v7, v4

    .line 125
    :goto_7e
    if-eqz v1, :cond_85

    .line 127
    invoke-static {v1}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I

    .line 130
    move-result v1

    .line 131
    goto :goto_86

    .line 132
    :cond_85
    move v1, v4

    .line 133
    :goto_86
    const/16 v8, 0x17

    .line 135
    invoke-static {v8, v7}, Ljava/lang/Math;->min(II)I

    .line 138
    move-result v7

    .line 139
    invoke-static {v4, v7}, Ljava/lang/Math;->max(II)I

    .line 142
    move-result v7

    .line 143
    const/16 v8, 0x3b

    .line 145
    invoke-static {v8, v1}, Ljava/lang/Math;->min(II)I

    .line 148
    move-result v1

    .line 149
    invoke-static {v4, v1}, Ljava/lang/Math;->max(II)I

    .line 152
    move-result v1

    .line 153
    filled-new-array {v7, v1}, [I

    .line 156
    move-result-object v1

    .line 157
    :goto_9e
    if-nez v1, :cond_ae

    .line 159
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 162
    move-result-object v0

    .line 163
    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 166
    move-result-wide v0

    .line 167
    const-string v2, "Day of Week/Month trigger: Unable to read time from variable"

    .line 169
    invoke-static {v0, v1, v2}, Lkjf;->g(JLjava/lang/String;)V

    .line 172
    return-void

    .line 173
    :cond_ae
    aget v7, v1, v4

    .line 175
    aget v1, v1, v5

    .line 177
    iget v8, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 179
    iget-boolean v9, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 181
    const/4 v10, -0x1

    .line 182
    if-nez v8, :cond_15e

    .line 184
    if-eqz v9, :cond_cc

    .line 186
    iget-object v8, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 188
    if-nez v8, :cond_c0

    .line 190
    goto :goto_cc

    .line 191
    :cond_c0
    iget-object v9, v0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 193
    if-eqz v9, :cond_c9

    .line 195
    invoke-virtual {v9, v8}, Lcom/arlosoft/macrodroid/macro/Macro;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 198
    move-result-object v8

    .line 199
    goto :goto_ca

    .line 200
    :cond_c9
    const/4 v8, 0x0

    .line 201
    :goto_ca
    if-nez v8, :cond_cf

    .line 203
    :cond_cc
    :goto_cc
    const/4 v8, 0x0

    .line 204
    goto/16 :goto_142

    .line 206
    :cond_cf
    invoke-virtual {v0, v8}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->v0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 209
    move-result-object v8

    .line 210
    if-nez v8, :cond_d6

    .line 212
    goto :goto_cc

    .line 213
    :cond_d6
    const-string v9, "days"

    .line 215
    invoke-static {v8, v9}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 218
    move-result-object v8

    .line 219
    if-eqz v8, :cond_133

    .line 221
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 224
    move-result-object v9

    .line 225
    instance-of v9, v9, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 227
    if-nez v9, :cond_e7

    .line 229
    goto :goto_133

    .line 230
    :cond_e7
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 233
    move-result-object v8

    .line 234
    check-cast v8, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 236
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->isArray()Z

    .line 239
    move-result v9

    .line 240
    if-nez v9, :cond_103

    .line 242
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 245
    move-result-object v8

    .line 246
    invoke-virtual {v8}, Ljava/lang/Long;->longValue()J

    .line 249
    move-result-wide v8

    .line 250
    const-string v11, "Day of Week variable \'days\' is not an array, using all days disabled"

    .line 252
    invoke-static {v8, v9, v11}, Lkjf;->t(JLjava/lang/String;)V

    .line 255
    new-array v8, v3, [Z

    .line 257
    goto :goto_142

    .line 258
    :cond_103
    new-array v9, v3, [Z

    .line 260
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 263
    move-result-object v8

    .line 264
    move v11, v4

    move v11, v4

    .line 265
    :goto_10b
    invoke-interface {v8}, Ljava/util/List;->size()I

    .line 268
    move-result v12

    .line 269
    invoke-static {v3, v12}, Ljava/lang/Math;->min(II)I

    .line 272
    move-result v12

    .line 273
    if-ge v11, v12, :cond_131

    .line 275
    invoke-interface {v8, v11}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 278
    move-result-object v12

    .line 279
    check-cast v12, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 281
    if-nez v12, :cond_11e

    .line 283
    goto :goto_12e

    .line 284
    :cond_11e
    invoke-virtual {v12}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 287
    move-result-object v12

    .line 288
    instance-of v13, v12, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;

    .line 290
    if-eqz v13, :cond_12e

    .line 292
    check-cast v12, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;

    .line 294
    invoke-virtual {v12}, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;->getBooleanValue()Z

    .line 297
    move-result v12

    .line 298
    aput-boolean v12, v9, v11

    .line 300
    :cond_12e
    :goto_12e
    add-int/lit8 v11, v11, 0x1

    .line 302
    goto :goto_10b

    .line 303
    :cond_131
    move-object v8, v9

    .line 304
    goto :goto_142

    .line 305
    :cond_133
    :goto_133
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 308
    move-result-object v8

    .line 309
    invoke-virtual {v8}, Ljava/lang/Long;->longValue()J

    .line 312
    move-result-wide v8

    .line 313
    const-string v11, "Day of Week variable missing \'days\' array, using all days disabled"

    .line 315
    invoke-static {v8, v9, v11}, Lkjf;->t(JLjava/lang/String;)V

    .line 318
    new-array v8, v3, [Z

    .line 320
    :goto_142
    if-nez v8, :cond_152

    .line 322
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 325
    move-result-object v0

    .line 326
    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 329
    move-result-wide v0

    .line 330
    const-string v2, "Day of Week trigger: Unable to read days from variable"

    .line 332
    invoke-static {v0, v1, v2}, Lkjf;->g(JLjava/lang/String;)V

    .line 335
    return-void

    .line 336
    :cond_152
    iget v9, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 338
    iget v11, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 340
    move v12, v11

    move v12, v11

    .line 341
    move v11, v10

    move v11, v10

    .line 342
    move v10, v9

    move v10, v9

    .line 343
    goto/16 :goto_24d

    .line 345
    :cond_15e
    if-eqz v9, :cond_171

    .line 347
    iget-object v8, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 349
    if-nez v8, :cond_165

    .line 351
    goto :goto_171

    .line 352
    :cond_165
    iget-object v9, v0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 354
    if-eqz v9, :cond_16e

    .line 356
    invoke-virtual {v9, v8}, Lcom/arlosoft/macrodroid/macro/Macro;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 359
    move-result-object v8

    .line 360
    goto :goto_16f

    .line 361
    :cond_16e
    const/4 v8, 0x0

    .line 362
    :goto_16f
    if-nez v8, :cond_174

    .line 364
    :cond_171
    :goto_171
    move v9, v4

    move v9, v4

    .line 365
    goto :goto_188

    .line 366
    :cond_174
    invoke-virtual {v0, v8}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->v0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 369
    move-result-object v8

    .line 370
    if-nez v8, :cond_17b

    .line 372
    goto :goto_171

    .line 373
    :cond_17b
    const-string v9, "dayOfMonth"

    .line 375
    invoke-static {v8, v9}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 378
    move-result-object v8

    .line 379
    if-eqz v8, :cond_171

    .line 381
    invoke-static {v8}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I

    .line 384
    move-result v8

    .line 385
    move v9, v8

    .line 386
    :goto_188
    if-gtz v9, :cond_19c

    .line 388
    const-string v1, "Day of Month trigger: Invalid dayOfMonth from variable, value = "

    .line 390
    invoke-static {v9, v1}, Lx9f;->z(ILjava/lang/String;)Ljava/lang/String;

    .line 393
    move-result-object v1

    .line 394
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 397
    move-result-object v0

    .line 398
    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 401
    move-result-wide v2

    .line 402
    invoke-static {v2, v3, v1}, Lkjf;->g(JLjava/lang/String;)V

    .line 405
    return-void

    .line 406
    :cond_19c
    iget-boolean v8, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 408
    if-eqz v8, :cond_1b1

    .line 410
    iget-object v8, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_variableName:Ljava/lang/String;

    .line 412
    if-nez v8, :cond_1a5

    .line 414
    goto :goto_1b1

    .line 415
    :cond_1a5
    iget-object v11, v0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 417
    if-eqz v11, :cond_1ae

    .line 419
    invoke-virtual {v11, v8}, Lcom/arlosoft/macrodroid/macro/Macro;->getVariableByName(Ljava/lang/String;)Lcom/arlosoft/macrodroid/common/MacroDroidVariable;

    .line 422
    move-result-object v8

    .line 423
    goto :goto_1af

    .line 424
    :cond_1ae
    const/4 v8, 0x0

    .line 425
    :goto_1af
    if-nez v8, :cond_1b4

    .line 427
    :cond_1b1
    :goto_1b1
    const/4 v8, 0x0

    .line 428
    goto/16 :goto_228

    .line 430
    :cond_1b4
    invoke-virtual {v0, v8}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->v0(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;)Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 433
    move-result-object v8

    .line 434
    if-nez v8, :cond_1bb

    .line 436
    goto :goto_1b1

    .line 437
    :cond_1bb
    const-string v11, "months"

    .line 439
    invoke-static {v8, v11}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 442
    move-result-object v8

    .line 443
    if-eqz v8, :cond_217

    .line 445
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 448
    move-result-object v11

    .line 449
    instance-of v11, v11, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 451
    if-nez v11, :cond_1cc

    .line 453
    goto :goto_217

    .line 454
    :cond_1cc
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 457
    move-result-object v8

    .line 458
    check-cast v8, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;

    .line 460
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->isArray()Z

    .line 463
    move-result v11

    .line 464
    if-nez v11, :cond_1e8

    .line 466
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 469
    move-result-object v8

    .line 470
    invoke-virtual {v8}, Ljava/lang/Long;->longValue()J

    .line 473
    move-result-wide v11

    .line 474
    const-string v8, "Day of Month variable \'months\' is not an array, using all months disabled"

    .line 476
    invoke-static {v11, v12, v8}, Lkjf;->t(JLjava/lang/String;)V

    .line 479
    new-array v8, v2, [Z

    .line 481
    goto :goto_228

    .line 482
    :cond_1e8
    new-array v11, v2, [Z

    .line 484
    invoke-virtual {v8}, Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;

    .line 487
    move-result-object v8

    .line 488
    move v12, v4

    .line 489
    :goto_1ef
    invoke-interface {v8}, Ljava/util/List;->size()I

    .line 492
    move-result v13

    .line 493
    invoke-static {v2, v13}, Ljava/lang/Math;->min(II)I

    .line 496
    move-result v13

    .line 497
    if-ge v12, v13, :cond_215

    .line 499
    invoke-interface {v8, v12}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 502
    move-result-object v13

    .line 503
    check-cast v13, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;

    .line 505
    if-nez v13, :cond_202

    .line 507
    goto :goto_212

    .line 508
    :cond_202
    invoke-virtual {v13}, Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;

    .line 511
    move-result-object v13

    .line 512
    instance-of v14, v13, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;

    .line 514
    if-eqz v14, :cond_212

    .line 516
    check-cast v13, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;

    .line 518
    invoke-virtual {v13}, Lcom/arlosoft/macrodroid/variables/VariableValue$BooleanValue;->getBooleanValue()Z

    .line 521
    move-result v13

    .line 522
    aput-boolean v13, v11, v12

    .line 524
    :cond_212
    :goto_212
    add-int/lit8 v12, v12, 0x1

    .line 526
    goto :goto_1ef

    .line 527
    :cond_215
    move-object v8, v11

    .line 528
    goto :goto_228

    .line 529
    :cond_217
    :goto_217
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 532
    move-result-object v8

    .line 533
    invoke-virtual {v8}, Ljava/lang/Long;->longValue()J

    .line 536
    move-result-wide v11

    .line 537
    const-string v8, "ab  o srduhv /yro,o ttss leafhsina oDsgmanlgmoa/b/iyrhMs /iniamnl ae dnti"

    const-string v8, "Day of Month variable missing \'months\' array, using all months disabled"

    .line 539
    invoke-static {v11, v12, v8}, Lkjf;->t(JLjava/lang/String;)V

    .line 542
    new-array v8, v2, [Z

    .line 544
    :goto_228
    if-nez v8, :cond_23a

    .line 546
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 549
    move-result-object v0

    .line 550
    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    .line 553
    move-result-wide v0

    .line 554
    const-string v2, "reganb:Mrt oyetr goo reDlho  a damUfaaotierml tbsin vnfb "

    const-string v2, "Day of Month trigger: Unable to read months from variable"

    .line 556
    invoke-static {v0, v1, v2}, Lkjf;->g(JLjava/lang/String;)V

    .line 559
    return-void

    .line 560
    :cond_23a
    iget v11, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 562
    move v12, v10

    .line 563
    move v10, v9

    .line 564
    move-object v9, v8

    move-object v9, v8

    .line 565
    const/4 v8, 0x0

    .line 566
    goto :goto_24e

    .line 567
    :cond_242
    iget v7, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_hour:I

    .line 569
    iget v1, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_minute:I

    .line 571
    iget v11, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfWeek:I

    .line 573
    iget v10, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_dayOfMonth:I

    .line 575
    iget v12, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_monthOfYear:I

    .line 577
    const/4 v8, 0x0

    .line 578
    :goto_24d
    const/4 v9, 0x0

    .line 579
    :goto_24e
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 582
    move-result-object v13

    .line 583
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 586
    move-result-object v14

    .line 587
    const/16 v15, 0xb

    .line 589
    invoke-virtual {v13, v15}, Ljava/util/Calendar;->get(I)I

    .line 592
    move-result v6

    .line 593
    invoke-virtual {v13, v2}, Ljava/util/Calendar;->get(I)I

    .line 596
    move-result v5

    .line 597
    const/16 v4, 0xd

    .line 599
    invoke-virtual {v13, v4}, Ljava/util/Calendar;->get(I)I

    .line 602
    move-result v18

    .line 603
    iget v4, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_option:I

    .line 605
    const-wide v19, 0x7fffffffffffffffL

    .line 610
    if-nez v4, :cond_302

    .line 612
    invoke-virtual {v13, v3}, Ljava/util/Calendar;->get(I)I

    .line 615
    move-result v4

    .line 616
    add-int/lit8 v4, v4, 0x5

    .line 618
    rem-int/2addr v4, v3

    .line 619
    iget-boolean v9, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 621
    const/16 v10, 0xa

    .line 623
    const/4 v12, 0x6

    .line 624
    if-eqz v9, :cond_2db

    .line 626
    if-eqz v8, :cond_2db

    .line 628
    const/4 v9, 0x0

    .line 629
    const/16 v16, 0x0

    .line 631
    :goto_282
    if-ge v9, v3, :cond_2cb

    .line 633
    aget-boolean v11, v8, v9

    .line 635
    if-eqz v11, :cond_2c8

    .line 637
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 640
    move-result-object v11

    .line 641
    sub-int v13, v7, v6

    .line 643
    sub-int v14, v1, v5

    .line 645
    invoke-virtual {v11, v15, v13}, Ljava/util/Calendar;->add(II)V

    .line 648
    invoke-virtual {v11, v2, v14}, Ljava/util/Calendar;->add(II)V

    .line 651
    const/16 v13, 0xd

    .line 653
    const/4 v14, 0x0

    .line 654
    invoke-virtual {v11, v13, v14}, Ljava/util/Calendar;->set(II)V

    .line 657
    if-eq v4, v9, :cond_2a5

    .line 659
    sub-int v13, v9, v4

    .line 661
    add-int/2addr v13, v3

    .line 662
    rem-int/2addr v13, v3

    .line 663
    invoke-virtual {v11, v12, v13}, Ljava/util/Calendar;->add(II)V

    .line 666
    :cond_2a5
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 669
    move-result-object v13

    .line 670
    if-nez p1, :cond_2af

    .line 672
    const/4 v14, 0x1

    .line 673
    invoke-virtual {v13, v10, v14}, Ljava/util/Calendar;->add(II)V

    .line 676
    :cond_2af
    invoke-virtual {v11, v13}, Ljava/util/Calendar;->before(Ljava/lang/Object;)Z

    .line 679
    move-result v13

    .line 680
    if-eqz v13, :cond_2b8

    .line 682
    invoke-virtual {v11, v3, v3}, Ljava/util/Calendar;->add(II)V

    .line 685
    :cond_2b8
    invoke-virtual {v11}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 688
    move-result-wide v13

    .line 689
    cmp-long v13, v13, v19

    .line 691
    if-gez v13, :cond_2c8

    .line 693
    invoke-virtual {v11}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 696
    move-result-wide v13

    .line 697
    move-object/from16 v16, v11

    .line 699
    move-wide/from16 v19, v13

    .line 701
    :cond_2c8
    add-int/lit8 v9, v9, 0x1

    .line 703
    goto :goto_282

    .line 704
    :cond_2cb
    if-eqz v16, :cond_396

    .line 706
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 709
    move-result-object v1

    .line 710
    invoke-virtual/range {v16 .. v16}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 713
    move-result-wide v2

    .line 714
    iget-object v4, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 716
    invoke-virtual {v0, v1, v4, v2, v3}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->x0(Landroid/content/Context;Ljava/lang/String;J)V

    .line 719
    return-void

    .line 720
    :cond_2db
    sub-int/2addr v7, v6

    .line 721
    sub-int/2addr v1, v5

    .line 722
    invoke-virtual {v14, v15, v7}, Ljava/util/Calendar;->add(II)V

    .line 725
    invoke-virtual {v14, v2, v1}, Ljava/util/Calendar;->add(II)V

    .line 728
    const/16 v1, 0xd

    .line 730
    const/4 v2, 0x0

    .line 731
    invoke-virtual {v14, v1, v2}, Ljava/util/Calendar;->set(II)V

    .line 734
    if-eq v4, v11, :cond_2f1

    .line 736
    sub-int/2addr v11, v4

    .line 737
    add-int/2addr v11, v3

    .line 738
    rem-int/2addr v11, v3

    .line 739
    invoke-virtual {v14, v12, v11}, Ljava/util/Calendar;->add(II)V

    .line 742
    :cond_2f1
    if-nez p1, :cond_2f7

    .line 744
    const/4 v8, 0x1

    .line 745
    invoke-virtual {v13, v10, v8}, Ljava/util/Calendar;->add(II)V

    .line 748
    :cond_2f7
    invoke-virtual {v14, v13}, Ljava/util/Calendar;->before(Ljava/lang/Object;)Z

    .line 751
    move-result v1

    .line 752
    if-eqz v1, :cond_43b

    .line 754
    invoke-virtual {v14, v3, v3}, Ljava/util/Calendar;->add(II)V

    .line 757
    goto/16 :goto_43b

    .line 759
    :cond_302
    const/4 v8, 0x1

    .line 760
    if-ne v4, v8, :cond_43b

    .line 762
    const/4 v3, 0x5

    .line 763
    invoke-virtual {v13, v3}, Ljava/util/Calendar;->get(I)I

    .line 766
    move-result v4

    .line 767
    const/4 v11, 0x2

    .line 768
    invoke-virtual {v13, v11}, Ljava/util/Calendar;->get(I)I

    .line 771
    move-result v17

    .line 772
    move/from16 p1, v8

    move/from16 p1, v8

    .line 774
    add-int/lit8 v8, v17, 0x1

    .line 776
    invoke-virtual {v14, v15, v7}, Ljava/util/Calendar;->set(II)V

    .line 779
    invoke-virtual {v14, v2, v1}, Ljava/util/Calendar;->set(II)V

    .line 782
    const/4 v3, 0x0

    .line 783
    const/16 v11, 0xd

    .line 785
    invoke-virtual {v14, v11, v3}, Ljava/util/Calendar;->set(II)V

    .line 788
    iget-boolean v3, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_useVariable:Z

    .line 790
    if-eqz v3, :cond_397

    .line 792
    if-eqz v9, :cond_397

    .line 794
    const/4 v14, 0x0

    .line 795
    const/16 v16, 0x0

    .line 797
    :goto_32a
    if-ge v14, v2, :cond_387

    .line 799
    aget-boolean v3, v9, v14

    .line 801
    if-eqz v3, :cond_382

    .line 803
    invoke-static {}, Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;

    .line 806
    move-result-object v3

    .line 807
    invoke-virtual {v3, v15, v7}, Ljava/util/Calendar;->set(II)V

    .line 810
    invoke-virtual {v3, v2, v1}, Ljava/util/Calendar;->set(II)V

    .line 813
    const/4 v12, 0x0

    .line 814
    invoke-virtual {v3, v11, v12}, Ljava/util/Calendar;->set(II)V

    .line 817
    const/4 v11, 0x1

    .line 818
    invoke-virtual {v13, v11}, Ljava/util/Calendar;->get(I)I

    .line 821
    move-result v12

    .line 822
    invoke-virtual {v3, v11, v12}, Ljava/util/Calendar;->set(II)V

    .line 825
    const/4 v11, 0x2

    .line 826
    invoke-virtual {v3, v11, v14}, Ljava/util/Calendar;->set(II)V

    .line 829
    const/4 v11, 0x5

    .line 830
    invoke-virtual {v3, v11}, Ljava/util/Calendar;->getActualMaximum(I)I

    .line 833
    move-result v12

    .line 834
    if-ge v12, v10, :cond_352

    .line 836
    goto :goto_382

    .line 837
    :cond_352
    invoke-virtual {v3, v11, v10}, Ljava/util/Calendar;->set(II)V

    .line 840
    add-int/lit8 v11, v14, 0x1

    .line 842
    if-lt v11, v8, :cond_35e

    .line 844
    if-ne v11, v8, :cond_360

    .line 846
    if-gt v4, v10, :cond_35e

    .line 848
    goto :goto_360

    .line 849
    :cond_35e
    :goto_35e
    const/4 v11, 0x1

    .line 850
    goto :goto_36f

    .line 851
    :cond_360
    :goto_360
    if-ne v11, v8, :cond_366

    .line 853
    if-ne v4, v10, :cond_366

    .line 855
    if-gt v6, v7, :cond_35e

    .line 857
    :cond_366
    if-ne v11, v8, :cond_372

    .line 859
    if-ne v4, v10, :cond_372

    .line 861
    if-ne v6, v7, :cond_372

    .line 863
    if-lt v5, v1, :cond_372

    .line 865
    goto :goto_35e

    .line 866
    :goto_36f
    invoke-virtual {v3, v11, v11}, Ljava/util/Calendar;->add(II)V

    .line 869
    :cond_372
    invoke-virtual {v3}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 872
    move-result-wide v11

    .line 873
    cmp-long v11, v11, v19

    .line 875
    if-gez v11, :cond_382

    .line 877
    invoke-virtual {v3}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 880
    move-result-wide v11

    .line 881
    move-object/from16 v16, v3

    .line 883
    move-wide/from16 v19, v11

    .line 885
    :cond_382
    :goto_382
    add-int/lit8 v14, v14, 0x1

    .line 887
    const/16 v11, 0xd

    .line 889
    goto :goto_32a

    .line 890
    :cond_387
    if-eqz v16, :cond_396

    .line 892
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 895
    move-result-object v1

    .line 896
    invoke-virtual/range {v16 .. v16}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 899
    move-result-wide v2

    .line 900
    iget-object v4, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 902
    invoke-virtual {v0, v1, v4, v2, v3}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->x0(Landroid/content/Context;Ljava/lang/String;J)V

    .line 905
    :cond_396
    return-void

    .line 906
    :cond_397
    const/4 v3, 0x0

    .line 907
    if-nez v12, :cond_3fa

    .line 909
    const/4 v11, 0x2

    .line 910
    invoke-virtual {v13, v11}, Ljava/util/Calendar;->get(I)I

    .line 913
    move-result v8

    .line 914
    invoke-virtual {v14, v11, v8}, Ljava/util/Calendar;->set(II)V

    .line 917
    if-gt v4, v10, :cond_3a9

    .line 919
    if-ne v4, v10, :cond_3ac

    .line 921
    if-gt v6, v7, :cond_3a9

    .line 923
    goto :goto_3ac

    .line 924
    :cond_3a9
    :goto_3a9
    const/4 v8, 0x1

    .line 925
    const/4 v11, 0x2

    .line 926
    goto :goto_3be

    .line 927
    :cond_3ac
    :goto_3ac
    if-ne v4, v10, :cond_3b2

    .line 929
    if-ne v6, v7, :cond_3b2

    .line 931
    if-ge v5, v1, :cond_3a9

    .line 933
    :cond_3b2
    if-ne v4, v10, :cond_3bb

    .line 935
    if-ne v6, v7, :cond_3bb

    .line 937
    if-ne v5, v1, :cond_3bb

    .line 939
    if-lez v18, :cond_3bb

    .line 941
    goto :goto_3a9

    .line 942
    :cond_3bb
    const/4 v8, 0x1

    .line 943
    const/4 v11, 0x2

    .line 944
    goto :goto_3c1

    .line 945
    :goto_3be
    invoke-virtual {v14, v11, v8}, Ljava/util/Calendar;->add(II)V

    .line 948
    :goto_3c1
    invoke-virtual {v14, v11}, Ljava/util/Calendar;->get(I)I

    .line 951
    move-result v1

    .line 952
    invoke-virtual {v14, v8}, Ljava/util/Calendar;->get(I)I

    .line 955
    move-result v4

    .line 956
    move/from16 v21, v4

    move/from16 v21, v4

    .line 958
    move v4, v3

    .line 959
    move/from16 v3, v21

    move/from16 v3, v21

    .line 961
    :goto_3d2
    if-ge v4, v2, :cond_3f1

    .line 963
    invoke-virtual {v14, v8, v3}, Ljava/util/Calendar;->set(II)V

    .line 966
    add-int v5, v1, v4

    .line 968
    rem-int/2addr v5, v2

    .line 969
    invoke-virtual {v14, v11, v5}, Ljava/util/Calendar;->set(II)V

    .line 972
    const/4 v11, 0x5

    .line 973
    invoke-virtual {v14, v11}, Ljava/util/Calendar;->getActualMaximum(I)I

    .line 976
    move-result v6

    .line 977
    if-lt v6, v10, :cond_3e8

    .line 979
    invoke-virtual {v14, v11, v10}, Ljava/util/Calendar;->set(II)V

    .line 982
    goto :goto_43b

    .line 983
    :cond_3e8
    if-ne v5, v15, :cond_3ec

    .line 985
    add-int/lit8 v3, v3, 0x1

    .line 987
    :cond_3ec
    add-int/lit8 v4, v4, 0x1

    .line 989
    const/4 v8, 0x1

    .line 990
    const/4 v11, 0x2

    .line 991
    goto :goto_3d2

    .line 992
    :cond_3f1
    const/4 v11, 0x5

    .line 993
    invoke-virtual {v14, v11}, Ljava/util/Calendar;->getActualMaximum(I)I

    .line 996
    move-result v1

    .line 997
    invoke-virtual {v14, v11, v1}, Ljava/util/Calendar;->set(II)V

    .line 1000
    goto :goto_43b

    .line 1001
    :cond_3fa
    const/4 v2, 0x1

    .line 1002
    const/4 v11, 0x5

    .line 1003
    invoke-virtual {v13, v2}, Ljava/util/Calendar;->get(I)I

    .line 1006
    move-result v3

    .line 1007
    invoke-virtual {v14, v2, v3}, Ljava/util/Calendar;->set(II)V

    .line 1010
    add-int/lit8 v3, v12, -0x1

    .line 1012
    const/4 v9, 0x2

    .line 1013
    invoke-virtual {v14, v9, v3}, Ljava/util/Calendar;->set(II)V

    .line 1016
    invoke-virtual {v14, v11}, Ljava/util/Calendar;->getActualMaximum(I)I

    .line 1019
    move-result v3

    .line 1020
    if-lt v3, v10, :cond_413

    .line 1022
    invoke-virtual {v14, v11, v10}, Ljava/util/Calendar;->set(II)V

    .line 1025
    goto :goto_416

    .line 1026
    :cond_413
    invoke-virtual {v14, v2, v2}, Ljava/util/Calendar;->add(II)V

    .line 1029
    :goto_416
    if-gt v8, v12, :cond_41d

    .line 1031
    if-ne v8, v12, :cond_41f

    .line 1033
    if-gt v4, v10, :cond_41d

    .line 1035
    goto :goto_41f

    .line 1036
    :cond_41d
    :goto_41d
    const/4 v8, 0x1

    .line 1037
    goto :goto_438

    .line 1038
    :cond_41f
    :goto_41f
    if-ne v8, v12, :cond_425

    .line 1040
    if-ne v4, v10, :cond_425

    .line 1042
    if-gt v6, v7, :cond_41d

    .line 1044
    :cond_425
    if-ne v8, v12, :cond_42d

    .line 1046
    if-ne v4, v10, :cond_42d

    .line 1048
    if-ne v6, v7, :cond_42d

    .line 1050
    if-ge v5, v1, :cond_41d

    .line 1052
    :cond_42d
    if-ne v8, v12, :cond_43b

    .line 1054
    if-ne v4, v10, :cond_43b

    .line 1056
    if-ne v6, v7, :cond_43b

    .line 1058
    if-ne v5, v1, :cond_43b

    .line 1060
    if-lez v18, :cond_43b

    .line 1062
    goto :goto_41d

    .line 1063
    :goto_438
    invoke-virtual {v14, v8, v8}, Ljava/util/Calendar;->add(II)V

    .line 1066
    :cond_43b
    :goto_43b
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 1069
    move-result-object v1

    .line 1070
    invoke-virtual {v14}, Ljava/util/Calendar;->getTimeInMillis()J

    .line 1073
    move-result-wide v2

    .line 1074
    iget-object v4, v0, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->m_alarmId:Ljava/lang/String;

    .line 1076
    invoke-virtual {v0, v1, v4, v2, v3}, Lcom/arlosoft/macrodroid/triggers/DayTrigger;->x0(Landroid/content/Context;Ljava/lang/String;J)V

    .line 1079
    return-void
.end method
