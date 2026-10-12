.class public final Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Lsxg;


# static fields
.field public static final a:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;

.field public static final b:Lg73;

.field public static final c:Landroid/os/Handler;

.field public static d:Landroid/content/Context;

.field public static e:Z

.field public static volatile f:Ljava/util/Map;

.field public static final g:Ljava/util/LinkedHashSet;

.field public static h:Z

.field public static final i:Lrw7;

.field public static volatile j:Ljava/util/Set;

.field public static volatile k:J

.field public static l:Landroid/os/HandlerThread;

.field public static m:Landroid/os/Handler;

.field public static volatile n:Z

.field public static final o:Lj$/util/concurrent/ConcurrentHashMap;

.field public static p:Lihh;

.field public static q:Z

.field public static final r:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$screenReceiver$1;

.field public static final s:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .line 1
    new-instance v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;

    .line 2
    .line 3
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;-><init>()V

    .line 4
    .line 5
    .line 6
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;

    .line 7
    .line 8
    invoke-static {}, Lkv;->c()Lbdf;

    .line 9
    .line 10
    .line 11
    move-result-object v0

    .line 12
    sget-object v1, Lzp4;->a:Lad4;

    .line 13
    .line 14
    const/4 v2, 0x2

    invoke-static {v0, v1}, Lmx2;->O(Lg93;Li93;)Li93;

    .line 15
    .line 16
    .line 17
    move-result-object v0

    .line 18
    invoke-static {v0}, Lpm6;->c(Li93;)Lg73;

    .line 19
    .line 20
    .line 21
    move-result-object v0

    .line 22
    const/4 v2, 0x7

    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->b:Lg73;

    .line 23
    .line 24
    const/4 v2, 0x1

    new-instance v0, Landroid/os/Handler;

    .line 25
    .line 26
    const/4 v2, 0x2

    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    .line 27
    .line 28
    .line 29
    move-result-object v1

    .line 30
    const/4 v2, 0x2

    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 31
    .line 32
    .line 33
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->c:Landroid/os/Handler;

    .line 34
    .line 35
    sget-object v0, Loc5;->a:Loc5;

    .line 36
    .line 37
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->f:Ljava/util/Map;

    .line 38
    .line 39
    new-instance v0, Ljava/util/LinkedHashSet;

    .line 40
    .line 41
    const/4 v2, 0x3

    invoke-direct {v0}, Ljava/util/LinkedHashSet;-><init>()V

    .line 42
    .line 43
    .line 44
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->g:Ljava/util/LinkedHashSet;

    .line 45
    .line 46
    new-instance v0, Lrw7;

    .line 47
    .line 48
    const/16 v1, 0xe

    .line 49
    .line 50
    invoke-direct {v0, v1}, Lrw7;-><init>(I)V

    .line 51
    .line 52
    .line 53
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->i:Lrw7;

    .line 54
    .line 55
    const/4 v2, 0x2

    sget-object v0, Lvc5;->a:Lvc5;

    .line 56
    .line 57
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 58
    .line 59
    const/4 v2, 0x4

    const-wide/16 v0, 0x3e8

    .line 60
    .line 61
    sput-wide v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->k:J

    .line 62
    .line 63
    new-instance v0, Lj$/util/concurrent/ConcurrentHashMap;

    .line 64
    .line 65
    const/4 v2, 0x2

    invoke-direct {v0}, Lj$/util/concurrent/ConcurrentHashMap;-><init>()V

    .line 66
    .line 67
    .line 68
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->o:Lj$/util/concurrent/ConcurrentHashMap;

    .line 69
    .line 70
    new-instance v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$screenReceiver$1;

    .line 71
    .line 72
    const/4 v2, 0x1

    invoke-direct {v0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$screenReceiver$1;-><init>()V

    .line 73
    .line 74
    .line 75
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->r:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$screenReceiver$1;

    .line 76
    .line 77
    const/4 v2, 0x2

    new-instance v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;

    .line 78
    .line 79
    invoke-direct {v0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;-><init>()V

    .line 80
    .line 81
    .line 82
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->s:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;

    .line 83
    .line 84
    return-void
.end method

.method private constructor <init>()V
    .locals 1

    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static c()Z
    .locals 4

    .line 1
    const-string v3, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 2
    .line 3
    const/4 v1, 0x0

    .line 4
    if-nez v0, :cond_8

    .line 5
    .line 6
    goto :goto_2d

    .line 7
    :cond_8
    const-string v2, "display"

    .line 8
    .line 9
    invoke-virtual {v0, v2}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    .line 10
    .line 11
    .line 12
    move-result-object v0

    .line 13
    const/4 v3, 0x3

    instance-of v2, v0, Landroid/hardware/display/DisplayManager;

    .line 14
    .line 15
    if-eqz v2, :cond_17

    .line 16
    .line 17
    check-cast v0, Landroid/hardware/display/DisplayManager;

    .line 18
    .line 19
    const/4 v3, 0x7

    goto :goto_18

    .line 20
    :cond_17
    const/4 v0, 0x0

    .line 21
    :goto_18
    const/4 v3, 0x6

    if-eqz v0, :cond_2d

    .line 22
    .line 23
    const/4 v3, 0x6

    invoke-virtual {v0, v1}, Landroid/hardware/display/DisplayManager;->getDisplay(I)Landroid/view/Display;

    .line 24
    .line 25
    .line 26
    move-result-object v0

    .line 27
    const/4 v3, 0x7

    if-eqz v0, :cond_2d

    .line 28
    .line 29
    invoke-virtual {v0}, Landroid/view/Display;->getState()I

    .line 30
    .line 31
    .line 32
    move-result v0

    .line 33
    const/4 v2, 0x2

    .line 34
    if-ne v0, v2, :cond_2d

    .line 35
    .line 36
    const/4 v0, 0x1

    const/4 v0, 0x1

    .line 37
    return v0

    .line 38
    :cond_2d
    :goto_2d
    return v1
.end method

.method public static e()V
    .locals 10

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 2
    .line 3
    const/4 v9, 0x5

    if-nez v0, :cond_7

    .line 4
    .line 5
    const/4 v9, 0x3

    return-void

    .line 6
    :cond_7
    sget-object v1, Lseh;->a:Lseh;

    .line 7
    .line 8
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 9
    .line 10
    .line 11
    invoke-static {v0}, Lseh;->d(Landroid/content/Context;)Ljava/util/Map;

    .line 12
    .line 13
    .line 14
    move-result-object v1

    .line 15
    invoke-interface {v1}, Ljava/util/Map;->values()Ljava/util/Collection;

    .line 16
    .line 17
    .line 18
    move-result-object v1

    .line 19
    check-cast v1, Ljava/lang/Iterable;

    .line 20
    .line 21
    const/4 v9, 0x7

    invoke-static {v1}, Lxj2;->o1(Ljava/lang/Iterable;)Ljava/util/Set;

    .line 22
    .line 23
    .line 24
    move-result-object v1

    .line 25
    const/4 v9, 0x4

    new-instance v2, Ljava/util/LinkedHashMap;

    .line 26
    .line 27
    invoke-direct {v2}, Ljava/util/LinkedHashMap;-><init>()V

    .line 28
    .line 29
    .line 30
    move-object v3, v1

    .line 31
    check-cast v3, Ljava/lang/Iterable;

    .line 32
    .line 33
    invoke-interface {v3}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 34
    .line 35
    .line 36
    move-result-object v3

    .line 37
    :goto_28
    invoke-interface {v3}, Ljava/util/Iterator;->hasNext()Z

    .line 38
    .line 39
    .line 40
    move-result v4

    .line 41
    const/4 v9, 0x6

    if-eqz v4, :cond_59

    .line 42
    .line 43
    const/4 v9, 0x6

    invoke-interface {v3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 44
    .line 45
    .line 46
    move-result-object v4

    .line 47
    check-cast v4, Ljava/lang/String;

    .line 48
    .line 49
    sget-object v5, Lti3;->a:Lti3;

    .line 50
    .line 51
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 52
    .line 53
    .line 54
    invoke-static {v0, v4}, Lti3;->e(Landroid/content/Context;Ljava/lang/String;)Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;

    .line 55
    .line 56
    .line 57
    move-result-object v5

    .line 58
    if-nez v5, :cond_42

    .line 59
    .line 60
    goto :goto_28

    .line 61
    :cond_42
    new-instance v6, Lshh;

    .line 62
    .line 63
    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getReferencedVariableNames()Ljava/util/Set;

    .line 64
    .line 65
    .line 66
    move-result-object v7

    .line 67
    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getMagicTextFields()Ljava/util/List;

    .line 68
    .line 69
    .line 70
    move-result-object v8

    .line 71
    const/4 v9, 0x2

    invoke-virtual {v5}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getImageUris()Ljava/util/List;

    .line 72
    .line 73
    .line 74
    move-result-object v5

    .line 75
    invoke-direct {v6, v7, v8, v5}, Lshh;-><init>(Ljava/util/Set;Ljava/util/List;Ljava/util/List;)V

    .line 76
    .line 77
    .line 78
    const/4 v9, 0x0

    invoke-interface {v2, v4, v6}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 79
    .line 80
    .line 81
    goto :goto_28

    .line 82
    :cond_59
    sput-object v2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->f:Ljava/util/Map;

    .line 83
    .line 84
    sget-object v2, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 85
    .line 86
    const/4 v9, 0x4

    invoke-static {v0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 87
    .line 88
    .line 89
    move-result-object v0

    .line 90
    const/4 v9, 0x6

    const-string v2, "preferences:custom_widget_refresh_interval"

    .line 91
    .line 92
    const/4 v3, 0x0

    .line 93
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    .line 94
    .line 95
    .line 96
    move-result v0

    .line 97
    const/4 v9, 0x4

    sget-object v2, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->Companion:Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig$a;

    .line 98
    .line 99
    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 100
    .line 101
    .line 102
    const/4 v9, 0x7

    const-wide/16 v2, 0x3e8

    const-wide/16 v2, 0x3e8

    .line 103
    .line 104
    if-gez v0, :cond_87

    .line 105
    .line 106
    const/4 v9, 0x1

    sput-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 107
    .line 108
    neg-int v0, v0

    .line 109
    const/4 v1, 0x1

    .line 110
    if-ge v0, v1, :cond_80

    .line 111
    .line 112
    const/4 v9, 0x7

    move v0, v1

    .line 113
    :cond_80
    int-to-long v0, v0

    .line 114
    mul-long/2addr v0, v2

    .line 115
    const/4 v9, 0x1

    sput-wide v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->k:J

    .line 116
    .line 117
    const/4 v9, 0x5

    return-void

    .line 118
    :cond_87
    sget-object v0, Lvc5;->a:Lvc5;

    .line 119
    .line 120
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 121
    .line 122
    sput-wide v2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->k:J

    .line 123
    .line 124
    return-void
.end method

.method public static g(Ljava/lang/String;Ljava/lang/String;)Z
    .locals 7

    .line 1
    const/4 v6, 0x1

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 5
    .line 6
    .line 7
    const/4 v6, 0x3

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    .line 8
    .line 9
    .line 10
    move-result v0

    .line 11
    const/4 v1, 0x0

    .line 12
    const/4 v6, 0x0

    if-nez v0, :cond_11

    .line 13
    .line 14
    goto :goto_1a

    .line 15
    :cond_11
    move v0, v1

    .line 16
    :goto_12
    const/4 v2, 0x4

    .line 17
    const/4 v6, 0x3

    invoke-static {p0, p1, v0, v1, v2}, Lz8f;->I1(Ljava/lang/CharSequence;Ljava/lang/String;IZI)I

    .line 18
    .line 19
    .line 20
    move-result v0

    .line 21
    if-gez v0, :cond_1b

    .line 22
    .line 23
    :goto_1a
    return v1

    .line 24
    :cond_1b
    const/4 v6, 0x2

    add-int/lit8 v2, v0, -0x1

    .line 25
    .line 26
    const/4 v3, 0x0

    .line 27
    const/4 v6, 0x3

    if-ltz v2, :cond_32

    .line 28
    .line 29
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    .line 30
    .line 31
    .line 32
    move-result v4

    .line 33
    if-ge v2, v4, :cond_32

    .line 34
    .line 35
    invoke-virtual {p0, v2}, Ljava/lang/String;->charAt(I)C

    .line 36
    .line 37
    .line 38
    move-result v2

    .line 39
    invoke-static {v2}, Ljava/lang/Character;->valueOf(C)Ljava/lang/Character;

    .line 40
    .line 41
    .line 42
    move-result-object v2

    .line 43
    const/4 v6, 0x7

    goto :goto_33

    .line 44
    :cond_32
    move-object v2, v3

    .line 45
    :goto_33
    invoke-virtual {p1}, Ljava/lang/String;->length()I

    .line 46
    .line 47
    .line 48
    move-result v4

    .line 49
    add-int/2addr v4, v0

    .line 50
    if-ltz v4, :cond_4a

    .line 51
    .line 52
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    .line 53
    .line 54
    .line 55
    move-result v5

    .line 56
    const/4 v6, 0x5

    if-ge v4, v5, :cond_4a

    .line 57
    .line 58
    invoke-virtual {p0, v4}, Ljava/lang/String;->charAt(I)C

    .line 59
    .line 60
    .line 61
    move-result v3

    .line 62
    const/4 v6, 0x7

    invoke-static {v3}, Ljava/lang/Character;->valueOf(C)Ljava/lang/Character;

    .line 63
    .line 64
    .line 65
    move-result-object v3

    .line 66
    :cond_4a
    if-nez v2, :cond_4d

    .line 67
    .line 68
    goto :goto_8b

    .line 69
    :cond_4d
    const/4 v6, 0x5

    invoke-virtual {v2}, Ljava/lang/Character;->charValue()C

    .line 70
    .line 71
    .line 72
    move-result v2

    .line 73
    const/16 v4, 0x3d

    .line 74
    .line 75
    if-ne v2, v4, :cond_8b

    .line 76
    .line 77
    const/4 v6, 0x2

    if-nez v3, :cond_5a

    .line 78
    .line 79
    goto :goto_64

    .line 80
    :cond_5a
    const/4 v6, 0x5

    invoke-virtual {v3}, Ljava/lang/Character;->charValue()C

    .line 81
    .line 82
    .line 83
    move-result v2

    .line 84
    const/4 v6, 0x2

    const/16 v4, 0x5d

    .line 85
    .line 86
    if-eq v2, v4, :cond_88

    .line 87
    .line 88
    :goto_64
    const/4 v6, 0x7

    if-nez v3, :cond_68

    .line 89
    .line 90
    goto :goto_70

    .line 91
    :cond_68
    invoke-virtual {v3}, Ljava/lang/Character;->charValue()C

    .line 92
    .line 93
    .line 94
    move-result v2

    .line 95
    const/16 v4, 0x7d

    .line 96
    .line 97
    if-eq v2, v4, :cond_88

    .line 98
    .line 99
    :goto_70
    if-nez v3, :cond_73

    .line 100
    .line 101
    goto :goto_7c

    .line 102
    :cond_73
    invoke-virtual {v3}, Ljava/lang/Character;->charValue()C

    .line 103
    .line 104
    .line 105
    move-result v2

    .line 106
    const/4 v6, 0x3

    const/16 v4, 0x5b

    .line 107
    .line 108
    if-eq v2, v4, :cond_88

    .line 109
    .line 110
    :goto_7c
    if-nez v3, :cond_7f

    .line 111
    .line 112
    goto :goto_8b

    .line 113
    :cond_7f
    invoke-virtual {v3}, Ljava/lang/Character;->charValue()C

    .line 114
    .line 115
    .line 116
    move-result v2

    .line 117
    const/4 v6, 0x6

    const/16 v3, 0x2e

    .line 118
    .line 119
    if-ne v2, v3, :cond_8b

    .line 120
    .line 121
    :cond_88
    const/4 p0, 0x1

    .line 122
    const/4 v6, 0x4

    return p0

    .line 123
    :cond_8b
    :goto_8b
    add-int/lit8 v0, v0, 0x1

    .line 124
    .line 125
    const/4 v6, 0x1

    goto :goto_12
.end method

.method public static h()V
    .locals 15

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 2
    .line 3
    const/4 v14, 0x4

    if-nez v0, :cond_7

    .line 4
    .line 5
    goto/16 :goto_169

    .line 6
    .line 7
    :cond_7
    :try_start_7
    const/4 v14, 0x5

    invoke-static {v0}, Lnnh;->g(Landroid/content/Context;)Lnnh;

    .line 8
    .line 9
    .line 10
    move-result-object v1

    .line 11
    const/4 v14, 0x7

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
    :try_end_10
    .catch Ljava/lang/Exception; {:try_start_7 .. :try_end_10} :catch_178

    .line 12
    .line 13
    .line 14
    sget-object v2, Lseh;->a:Lseh;

    .line 15
    .line 16
    const/4 v14, 0x1

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 17
    .line 18
    .line 19
    invoke-static {v0}, Lseh;->a(Landroid/content/Context;)Ljava/util/Map;

    .line 20
    .line 21
    .line 22
    move-result-object v2

    .line 23
    invoke-interface {v2}, Ljava/util/Map;->values()Ljava/util/Collection;

    .line 24
    .line 25
    .line 26
    move-result-object v2

    .line 27
    const/4 v14, 0x4

    check-cast v2, Ljava/lang/Iterable;

    .line 28
    .line 29
    invoke-static {v2}, Lxj2;->o1(Ljava/lang/Iterable;)Ljava/util/Set;

    .line 30
    .line 31
    .line 32
    move-result-object v2

    .line 33
    sget-object v3, Lcom/arlosoft/macrodroid/settings/c;->a:[Ljava/util/Locale;

    .line 34
    .line 35
    invoke-static {v0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;

    .line 36
    .line 37
    .line 38
    move-result-object v3

    .line 39
    const/4 v14, 0x6

    const-string v4, "preferences:custom_widget_refresh_interval"

    .line 40
    .line 41
    const/4 v5, 0x0

    .line 42
    invoke-interface {v3, v4, v5}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    .line 43
    .line 44
    .line 45
    move-result v3

    .line 46
    const/4 v14, 0x3

    new-instance v4, Ljava/util/LinkedHashSet;

    .line 47
    .line 48
    invoke-direct {v4}, Ljava/util/LinkedHashSet;-><init>()V

    .line 49
    .line 50
    .line 51
    const/4 v14, 0x7

    sget-object v6, Lti3;->a:Lti3;

    .line 52
    .line 53
    invoke-virtual {v6}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 54
    .line 55
    .line 56
    invoke-static {v0}, Lti3;->f(Landroid/content/Context;)Ljava/util/List;

    .line 57
    .line 58
    .line 59
    move-result-object v0

    .line 60
    const/4 v14, 0x2

    invoke-interface {v0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 61
    .line 62
    .line 63
    move-result-object v0

    .line 64
    :goto_48
    const/4 v14, 0x7

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 65
    .line 66
    .line 67
    move-result v6

    .line 68
    const/4 v14, 0x6

    const-string v7, "efs_misrdch_ougeestwr"

    const-string v7, "custom_widget_refresh"

    .line 69
    .line 70
    const/4 v14, 0x6

    const-string v8, "custom_widget_refresh_"

    .line 71
    .line 72
    if-eqz v6, :cond_e3

    .line 73
    .line 74
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 75
    .line 76
    .line 77
    move-result-object v6

    .line 78
    const/4 v14, 0x2

    check-cast v6, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;

    .line 79
    .line 80
    const/4 v14, 0x2

    invoke-virtual {v6}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getId()Ljava/lang/String;

    .line 81
    .line 82
    .line 83
    move-result-object v9

    .line 84
    const/4 v14, 0x5

    invoke-static {v8, v9}, Ljb3;->z(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 85
    .line 86
    .line 87
    move-result-object v8

    .line 88
    invoke-virtual {v6}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getId()Ljava/lang/String;

    .line 89
    .line 90
    .line 91
    move-result-object v9

    .line 92
    const/4 v14, 0x3

    invoke-interface {v2, v9}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    .line 93
    .line 94
    .line 95
    move-result v9

    .line 96
    const/4 v14, 0x0

    if-eqz v9, :cond_dd

    .line 97
    .line 98
    if-lez v3, :cond_dd

    .line 99
    .line 100
    const/4 v14, 0x2

    invoke-interface {v4, v8}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 101
    .line 102
    .line 103
    const/16 v9, 0xf

    .line 104
    .line 105
    if-ge v3, v9, :cond_80

    .line 106
    .line 107
    const/4 v14, 0x1

    goto :goto_82

    .line 108
    :cond_80
    const/4 v14, 0x7

    move v9, v3

    .line 109
    :goto_82
    int-to-long v9, v9

    .line 110
    new-instance v11, Lhnb;

    .line 111
    .line 112
    const-class v12, Lcom/arlosoft/macrodroid/widget/custom/PeriodicWidgetRefreshWorker;

    .line 113
    .line 114
    sget-object v13, Ljava/util/concurrent/TimeUnit;->MINUTES:Ljava/util/concurrent/TimeUnit;

    .line 115
    .line 116
    invoke-direct {v11, v12, v9, v10, v13}, Lhnb;-><init>(Ljava/lang/Class;JLjava/util/concurrent/TimeUnit;)V

    .line 117
    .line 118
    .line 119
    const/4 v14, 0x1

    invoke-virtual {v6}, Lcom/arlosoft/macrodroid/widget/custom/data/CustomWidgetConfig;->getId()Ljava/lang/String;

    .line 120
    .line 121
    .line 122
    move-result-object v6

    .line 123
    const/4 v14, 0x5

    new-instance v9, Ldib;

    .line 124
    .line 125
    const-string v10, "definitionId"

    .line 126
    .line 127
    invoke-direct {v9, v10, v6}, Ldib;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 128
    .line 129
    .line 130
    const/4 v6, 0x6

    const/4 v6, 0x1

    .line 131
    new-array v6, v6, [Ldib;

    .line 132
    .line 133
    aput-object v9, v6, v5

    .line 134
    .line 135
    new-instance v9, Ljm3;

    .line 136
    .line 137
    const/4 v14, 0x3

    const/4 v10, 0x3

    .line 138
    invoke-direct {v9, v10}, Ljm3;-><init>(I)V

    .line 139
    .line 140
    .line 141
    const/4 v14, 0x2

    aget-object v6, v6, v5

    .line 142
    .line 143
    const/4 v14, 0x6

    invoke-virtual {v6}, Ldib;->d()Ljava/lang/Object;

    .line 144
    .line 145
    .line 146
    move-result-object v10

    .line 147
    const/4 v14, 0x1

    check-cast v10, Ljava/lang/String;

    .line 148
    .line 149
    invoke-virtual {v6}, Ldib;->e()Ljava/lang/Object;

    .line 150
    .line 151
    .line 152
    move-result-object v6

    .line 153
    const/4 v14, 0x7

    invoke-virtual {v9, v6, v10}, Ljm3;->q(Ljava/lang/Object;Ljava/lang/String;)V

    .line 154
    .line 155
    .line 156
    invoke-virtual {v9}, Ljm3;->i()Lqz3;

    .line 157
    .line 158
    .line 159
    move-result-object v6

    .line 160
    const/4 v14, 0x0

    invoke-virtual {v11, v6}, Lq3c;->y(Lqz3;)Lq3c;

    .line 161
    .line 162
    .line 163
    move-result-object v6

    .line 164
    check-cast v6, Lhnb;

    .line 165
    .line 166
    iget-object v9, v6, Lq3c;->d:Ljava/lang/Object;

    .line 167
    .line 168
    check-cast v9, Ljava/util/Set;

    .line 169
    .line 170
    invoke-interface {v9, v7}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 171
    .line 172
    .line 173
    invoke-interface {v9, v8}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 174
    .line 175
    .line 176
    invoke-virtual {v6}, Lq3c;->b()Laoh;

    .line 177
    .line 178
    .line 179
    move-result-object v6

    .line 180
    const/4 v14, 0x7

    check-cast v6, Linb;

    .line 181
    .line 182
    sget-object v7, Lql5;->UPDATE:Lql5;

    .line 183
    .line 184
    invoke-virtual {v1, v8, v7, v6}, Lnnh;->d(Ljava/lang/String;Lql5;Linb;)Lzra;

    .line 185
    .line 186
    .line 187
    const/4 v14, 0x0

    goto/16 :goto_48

    .line 188
    :cond_dd
    const/4 v14, 0x6

    invoke-virtual {v1, v8}, Lnnh;->b(Ljava/lang/String;)Lzra;

    .line 189
    .line 190
    .line 191
    goto/16 :goto_48

    .line 192
    :cond_e3
    :try_start_e3
    const/4 v14, 0x6

    iget-object v0, v1, Lnnh;->c:Landroidx/work/impl/WorkDatabase;

    .line 193
    .line 194
    iget-object v2, v1, Lnnh;->d:Lopf;

    .line 195
    .line 196
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 197
    .line 198
    .line 199
    const/4 v14, 0x7

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 200
    .line 201
    .line 202
    const/4 v14, 0x4

    new-instance v3, Lg3f;

    .line 203
    .line 204
    invoke-direct {v3, v7}, Lg3f;-><init>(Ljava/lang/String;)V

    .line 205
    .line 206
    .line 207
    check-cast v2, Lsnh;

    .line 208
    .line 209
    iget-object v2, v2, Lsnh;->a:Lnf0;

    .line 210
    .line 211
    const/4 v14, 0x0

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 212
    .line 213
    .line 214
    const-string v6, "uFsmtoSttaudelra"

    const-string v6, "loadStatusFuture"

    .line 215
    .line 216
    const/4 v14, 0x5

    new-instance v7, Li3f;

    .line 217
    .line 218
    invoke-direct {v7, v3, v0}, Li3f;-><init>(Lwm6;Landroidx/work/impl/WorkDatabase;)V

    .line 219
    .line 220
    .line 221
    const/4 v14, 0x0

    invoke-static {v2, v6, v7}, Lrjb;->q(Ljava/util/concurrent/Executor;Ljava/lang/String;Lum6;)Lkt1;

    .line 222
    .line 223
    .line 224
    move-result-object v0

    .line 225
    iget-object v0, v0, Lkt1;->b:Ljt1;

    .line 226
    .line 227
    const/4 v14, 0x7

    invoke-virtual {v0}, Li3;->get()Ljava/lang/Object;

    .line 228
    .line 229
    .line 230
    move-result-object v0

    .line 231
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 232
    .line 233
    .line 234
    check-cast v0, Ljava/lang/Iterable;

    .line 235
    .line 236
    const/4 v14, 0x6

    invoke-interface {v0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 237
    .line 238
    .line 239
    move-result-object v0

    .line 240
    :cond_11d
    :goto_11d
    const/4 v14, 0x2

    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 241
    .line 242
    .line 243
    move-result v2

    .line 244
    const/4 v14, 0x6

    if-eqz v2, :cond_169

    .line 245
    .line 246
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 247
    .line 248
    .line 249
    move-result-object v2

    .line 250
    const/4 v14, 0x0

    check-cast v2, Ljnh;

    .line 251
    .line 252
    const/4 v14, 0x2

    iget-object v3, v2, Ljnh;->b:Linh;

    .line 253
    .line 254
    const/4 v14, 0x5

    invoke-virtual {v3}, Linh;->isFinished()Z

    .line 255
    .line 256
    .line 257
    move-result v3

    .line 258
    if-nez v3, :cond_11d

    .line 259
    .line 260
    iget-object v2, v2, Ljnh;->c:Ljava/util/HashSet;

    .line 261
    .line 262
    invoke-interface {v2}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 263
    .line 264
    .line 265
    move-result-object v2

    .line 266
    :cond_13c
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    .line 267
    .line 268
    .line 269
    move-result v3

    .line 270
    const/4 v14, 0x1

    if-eqz v3, :cond_155

    .line 271
    .line 272
    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 273
    .line 274
    .line 275
    move-result-object v3

    .line 276
    move-object v6, v3

    move-object v6, v3

    .line 277
    const/4 v14, 0x6

    check-cast v6, Ljava/lang/String;

    .line 278
    .line 279
    const/4 v14, 0x7

    invoke-static {v6, v8, v5}, Lg9f;->t1(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 280
    .line 281
    .line 282
    move-result v6

    .line 283
    if-eqz v6, :cond_13c

    .line 284
    .line 285
    const/4 v14, 0x5

    goto :goto_156

    .line 286
    :cond_155
    const/4 v3, 0x0

    .line 287
    :goto_156
    const/4 v14, 0x7

    check-cast v3, Ljava/lang/String;

    .line 288
    .line 289
    if-nez v3, :cond_15c

    .line 290
    .line 291
    goto :goto_11d

    .line 292
    :cond_15c
    const/4 v14, 0x6

    invoke-interface {v4, v3}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    .line 293
    .line 294
    .line 295
    move-result v2

    .line 296
    const/4 v14, 0x1

    if-nez v2, :cond_11d

    .line 297
    .line 298
    const/4 v14, 0x0

    invoke-virtual {v1, v3}, Lnnh;->b(Ljava/lang/String;)Lzra;
    :try_end_168
    .catch Ljava/lang/Exception; {:try_start_e3 .. :try_end_168} :catch_16a

    .line 299
    .line 300
    .line 301
    goto :goto_11d

    .line 302
    :cond_169
    :goto_169
    return-void

    .line 303
    :catch_16a
    move-exception v0

    .line 304
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 305
    .line 306
    .line 307
    move-result-object v0

    .line 308
    const/4 v14, 0x0

    const-string v1, "d dsorwgieo:hoelwetn eiektef   pdpeaarsr oh Fr"

    const-string v1, "Failed to sweep orphaned widget refresh work: "

    .line 309
    .line 310
    invoke-static {v1, v0}, Lbl5;->D(Ljava/lang/String;Ljava/lang/String;)V

    .line 311
    .line 312
    .line 313
    return-void

    .line 314
    :catch_178
    move-exception v0

    .line 315
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    .line 316
    .line 317
    .line 318
    move-result-object v0

    .line 319
    const-string v1, "Failed to schedule widget refresh work: "

    .line 320
    .line 321
    invoke-static {v1, v0}, Lbl5;->D(Ljava/lang/String;Ljava/lang/String;)V

    .line 322
    .line 323
    .line 324
    return-void
.end method


# virtual methods
.method public final M(Lcom/arlosoft/macrodroid/common/MacroDroidVariable;Lcom/arlosoft/macrodroid/variables/VariableValue;Lcom/arlosoft/macrodroid/variables/VariableValue;J)V
    .locals 6

    .line 1
    const/4 v5, 0x7

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    const/4 v5, 0x4

    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 5
    .line 6
    .line 7
    const/4 v5, 0x0

    invoke-virtual {p3}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 8
    .line 9
    .line 10
    invoke-virtual {p1}, Lcom/arlosoft/macrodroid/common/MacroDroidVariable;->D()Ljava/lang/String;

    .line 11
    .line 12
    .line 13
    move-result-object p0

    .line 14
    const/4 v5, 0x6

    if-nez p0, :cond_16

    .line 15
    .line 16
    const/4 v5, 0x5

    goto/16 :goto_d2

    .line 17
    .line 18
    :cond_16
    sget-object p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->f:Ljava/util/Map;

    .line 19
    .line 20
    const/4 v5, 0x7

    new-instance p2, Ljava/util/LinkedHashMap;

    .line 21
    .line 22
    invoke-direct {p2}, Ljava/util/LinkedHashMap;-><init>()V

    .line 23
    .line 24
    .line 25
    const/4 v5, 0x2

    invoke-interface {p1}, Ljava/util/Map;->entrySet()Ljava/util/Set;

    .line 26
    .line 27
    .line 28
    move-result-object p3

    .line 29
    const/4 v5, 0x2

    invoke-interface {p3}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    .line 30
    .line 31
    .line 32
    move-result-object p3

    .line 33
    :cond_28
    :goto_28
    const/4 v5, 0x6

    invoke-interface {p3}, Ljava/util/Iterator;->hasNext()Z

    .line 34
    .line 35
    .line 36
    move-result p4

    .line 37
    if-eqz p4, :cond_7d

    .line 38
    .line 39
    const/4 v5, 0x3

    invoke-interface {p3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 40
    .line 41
    .line 42
    move-result-object p4

    .line 43
    const/4 v5, 0x4

    check-cast p4, Ljava/util/Map$Entry;

    .line 44
    .line 45
    invoke-interface {p4}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    .line 46
    .line 47
    .line 48
    move-result-object p5

    .line 49
    const/4 v5, 0x2

    check-cast p5, Lshh;

    .line 50
    .line 51
    iget-object v0, p5, Lshh;->a:Ljava/util/Set;

    .line 52
    .line 53
    invoke-interface {v0, p0}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    .line 54
    .line 55
    .line 56
    move-result v0

    .line 57
    if-nez v0, :cond_70

    .line 58
    .line 59
    iget-object p5, p5, Lshh;->b:Ljava/util/List;

    .line 60
    .line 61
    if-eqz p5, :cond_51

    .line 62
    .line 63
    invoke-interface {p5}, Ljava/util/Collection;->isEmpty()Z

    .line 64
    .line 65
    .line 66
    move-result v0

    .line 67
    if-eqz v0, :cond_51

    .line 68
    .line 69
    goto :goto_28

    .line 70
    :cond_51
    invoke-interface {p5}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 71
    .line 72
    .line 73
    move-result-object p5

    .line 74
    :cond_55
    invoke-interface {p5}, Ljava/util/Iterator;->hasNext()Z

    .line 75
    .line 76
    .line 77
    move-result v0

    .line 78
    const/4 v5, 0x0

    if-eqz v0, :cond_28

    .line 79
    .line 80
    const/4 v5, 0x2

    invoke-interface {p5}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 81
    .line 82
    .line 83
    move-result-object v0

    .line 84
    check-cast v0, Ljava/lang/String;

    .line 85
    .line 86
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;

    .line 87
    .line 88
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 89
    .line 90
    .line 91
    const/4 v5, 0x0

    invoke-static {v0, p0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->g(Ljava/lang/String;Ljava/lang/String;)Z

    .line 92
    .line 93
    .line 94
    move-result v0

    .line 95
    const/4 v5, 0x5

    if-eqz v0, :cond_55

    .line 96
    .line 97
    :cond_70
    invoke-interface {p4}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    .line 98
    .line 99
    .line 100
    move-result-object p5

    .line 101
    const/4 v5, 0x3

    invoke-interface {p4}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    .line 102
    .line 103
    .line 104
    move-result-object p4

    .line 105
    invoke-virtual {p2, p5, p4}, Ljava/util/AbstractMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 106
    .line 107
    .line 108
    goto :goto_28

    .line 109
    :cond_7d
    invoke-virtual {p2}, Ljava/util/LinkedHashMap;->keySet()Ljava/util/Set;

    .line 110
    .line 111
    .line 112
    move-result-object p2

    .line 113
    const/4 v5, 0x3

    check-cast p2, Ljava/lang/Iterable;

    .line 114
    .line 115
    new-instance p3, Ljava/util/LinkedHashSet;

    .line 116
    .line 117
    const/4 v5, 0x6

    invoke-direct {p3}, Ljava/util/LinkedHashSet;-><init>()V

    .line 118
    .line 119
    .line 120
    const/4 v5, 0x2

    invoke-interface {p2}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 121
    .line 122
    .line 123
    move-result-object p2

    .line 124
    :cond_8f
    :goto_8f
    const/4 v5, 0x4

    invoke-interface {p2}, Ljava/util/Iterator;->hasNext()Z

    .line 125
    .line 126
    .line 127
    move-result p4

    .line 128
    const/4 p5, 0x1

    .line 129
    const/4 v5, 0x2

    if-eqz p4, :cond_cb

    .line 130
    .line 131
    invoke-interface {p2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 132
    .line 133
    .line 134
    move-result-object p4

    .line 135
    move-object v0, p4

    .line 136
    check-cast v0, Ljava/lang/String;

    .line 137
    .line 138
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 139
    .line 140
    invoke-interface {v1, v0}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    .line 141
    .line 142
    .line 143
    move-result v1

    .line 144
    const/4 v5, 0x1

    if-eqz v1, :cond_c6

    .line 145
    .line 146
    const/4 v5, 0x4

    sget-wide v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->k:J

    .line 147
    .line 148
    const/4 v5, 0x6

    const-wide/16 v3, 0x3e8

    .line 149
    .line 150
    cmp-long v1, v1, v3

    .line 151
    .line 152
    const/4 v5, 0x2

    if-gtz v1, :cond_c6

    .line 153
    .line 154
    invoke-interface {p1, v0}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    .line 155
    .line 156
    .line 157
    move-result-object v0

    .line 158
    check-cast v0, Lshh;

    .line 159
    .line 160
    if-eqz v0, :cond_8f

    .line 161
    .line 162
    iget-object v0, v0, Lshh;->a:Ljava/util/Set;

    .line 163
    .line 164
    if-eqz v0, :cond_8f

    .line 165
    .line 166
    invoke-interface {v0, p0}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    .line 167
    .line 168
    .line 169
    move-result v0

    .line 170
    const/4 v5, 0x5

    if-ne v0, p5, :cond_8f

    .line 171
    .line 172
    :cond_c6
    invoke-interface {p3, p4}, Ljava/util/Collection;->add(Ljava/lang/Object;)Z

    .line 173
    .line 174
    .line 175
    const/4 v5, 0x0

    goto :goto_8f

    .line 176
    :cond_cb
    const/4 v5, 0x5

    invoke-interface {p3}, Ljava/util/Set;->isEmpty()Z

    .line 177
    .line 178
    .line 179
    move-result p0

    .line 180
    if-eqz p0, :cond_d4

    .line 181
    .line 182
    :goto_d2
    const/4 v5, 0x4

    return-void

    .line 183
    :cond_d4
    sget-object p0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->g:Ljava/util/LinkedHashSet;

    .line 184
    .line 185
    monitor-enter p0

    .line 186
    :try_start_d7
    const/4 v5, 0x3

    invoke-interface {p0, p3}, Ljava/util/Set;->addAll(Ljava/util/Collection;)Z

    .line 187
    .line 188
    .line 189
    const/4 v5, 0x7

    sget-boolean p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->h:Z
    :try_end_de
    .catchall {:try_start_d7 .. :try_end_de} :catchall_f2

    .line 190
    .line 191
    if-eqz p1, :cond_e2

    .line 192
    .line 193
    monitor-exit p0

    .line 194
    return-void

    .line 195
    :cond_e2
    :try_start_e2
    sput-boolean p5, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->h:Z
    :try_end_e4
    .catchall {:try_start_e2 .. :try_end_e4} :catchall_f2

    .line 196
    .line 197
    const/4 v5, 0x5

    monitor-exit p0

    .line 198
    sget-object p0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->c:Landroid/os/Handler;

    .line 199
    .line 200
    sget-object p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->i:Lrw7;

    .line 201
    .line 202
    const-wide/16 p2, 0x12c

    const-wide/16 p2, 0x12c

    .line 203
    .line 204
    invoke-virtual {p0, p1, p2, p3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 205
    .line 206
    .line 207
    return-void

    .line 208
    :catchall_f2
    move-exception p1

    .line 209
    const/4 v5, 0x2

    monitor-exit p0

    .line 210
    throw p1
.end method

.method public final declared-synchronized a(Landroid/content/Context;)V
    .locals 5

    .line 1
    monitor-enter p0

    .line 2
    :try_start_1
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 3
    .line 4
    if-nez v0, :cond_f

    .line 5
    .line 6
    invoke-virtual {p1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 7
    .line 8
    .line 9
    move-result-object p1

    .line 10
    sput-object p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 11
    .line 12
    goto :goto_f

    .line 13
    :catchall_c
    move-exception p1

    .line 14
    const/4 v4, 0x6

    goto :goto_44

    .line 15
    :cond_f
    :goto_f
    sget-boolean p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->e:Z

    .line 16
    .line 17
    const/4 v0, 0x1

    .line 18
    if-nez p1, :cond_1d

    .line 19
    .line 20
    sput-boolean v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->e:Z

    .line 21
    .line 22
    invoke-static {}, Lcom/arlosoft/macrodroid/common/a;->q()Lcom/arlosoft/macrodroid/common/a;

    .line 23
    .line 24
    .line 25
    move-result-object p1

    .line 26
    invoke-virtual {p1, p0}, Lcom/arlosoft/macrodroid/common/a;->b(Lsxg;)V

    .line 27
    .line 28
    .line 29
    :cond_1d
    sget-object p1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 30
    .line 31
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 32
    .line 33
    .line 34
    sget-boolean v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->q:Z

    .line 35
    .line 36
    if-eqz v1, :cond_27

    .line 37
    .line 38
    goto :goto_41

    .line 39
    :cond_27
    new-instance v1, Landroid/content/IntentFilter;

    .line 40
    .line 41
    invoke-direct {v1}, Landroid/content/IntentFilter;-><init>()V

    .line 42
    .line 43
    .line 44
    const-string v2, "android.intent.action.SCREEN_ON"

    .line 45
    .line 46
    invoke-virtual {v1, v2}, Landroid/content/IntentFilter;->addAction(Ljava/lang/String;)V

    .line 47
    .line 48
    .line 49
    const/4 v4, 0x2

    const-string v2, "nFEaEbn.RtoCcd.t_inSraiNdentOo.i"

    const-string v2, "android.intent.action.SCREEN_OFF"

    .line 50
    .line 51
    invoke-virtual {v1, v2}, Landroid/content/IntentFilter;->addAction(Ljava/lang/String;)V

    .line 52
    .line 53
    .line 54
    sget-object v2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->r:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$screenReceiver$1;

    .line 55
    .line 56
    const/4 v3, 0x2

    .line 57
    invoke-static {p1, v2, v1, v3}, Lw63;->registerReceiver(Landroid/content/Context;Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;I)Landroid/content/Intent;

    .line 58
    .line 59
    .line 60
    sput-boolean v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->q:Z
    :try_end_41
    .catchall {:try_start_1 .. :try_end_41} :catchall_c

    .line 61
    .line 62
    :goto_41
    const/4 v4, 0x0

    monitor-exit p0

    .line 63
    return-void

    .line 64
    :goto_44
    :try_start_44
    monitor-exit p0
    :try_end_45
    .catchall {:try_start_44 .. :try_end_45} :catchall_c

    .line 65
    throw p1
.end method

.method public final b(Landroid/content/Context;Ljava/util/List;)V
    .locals 2

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-interface {p2}, Ljava/util/List;->isEmpty()Z

    .line 5
    .line 6
    .line 7
    move-result v0

    .line 8
    const/4 v1, 0x6

    if-eqz v0, :cond_b

    .line 9
    .line 10
    return-void

    .line 11
    :cond_b
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    .line 12
    .line 13
    .line 14
    invoke-virtual {p1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 15
    .line 16
    .line 17
    move-result-object p0

    .line 18
    const/4 v1, 0x4

    new-instance p1, Lvhh;

    .line 19
    .line 20
    const/4 v0, 0x0

    .line 21
    invoke-direct {p1, v0, p0, p2}, Lvhh;-><init>(Lm73;Landroid/content/Context;Ljava/util/List;)V

    .line 22
    .line 23
    .line 24
    const/4 p0, 0x3

    or-int/2addr v1, p0

    .line 25
    sget-object p2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->b:Lg73;

    .line 26
    .line 27
    const/4 v1, 0x0

    invoke-static {p2, v0, v0, p1, p0}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 28
    .line 29
    .line 30
    return-void
.end method

.method public final d(Landroid/content/Context;)V
    .locals 3

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    .line 5
    .line 6
    .line 7
    const/4 v2, 0x6

    new-instance p0, Lxhh;

    .line 8
    .line 9
    const/4 p1, 0x2

    .line 10
    const/4 v0, 0x0

    move v2, v0

    .line 11
    invoke-direct {p0, p1, v0}, Lrff;-><init>(ILm73;)V

    .line 12
    .line 13
    .line 14
    const/4 p1, 0x3

    .line 15
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->b:Lg73;

    .line 16
    .line 17
    invoke-static {v1, v0, v0, p0, p1}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 18
    .line 19
    .line 20
    return-void
.end method

.method public final f()V
    .locals 2

    .line 1
    const/4 v1, 0x3

    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 2
    .line 3
    check-cast v0, Ljava/util/Collection;

    .line 4
    .line 5
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 6
    .line 7
    .line 8
    move-result v0

    .line 9
    const/4 v1, 0x1

    if-nez v0, :cond_17

    .line 10
    .line 11
    invoke-static {}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->c()Z

    .line 12
    .line 13
    .line 14
    move-result v0

    .line 15
    const/4 v1, 0x5

    if-eqz v0, :cond_17

    .line 16
    .line 17
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->i()V

    .line 18
    .line 19
    .line 20
    return-void

    .line 21
    :cond_17
    const/4 v1, 0x2

    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 22
    .line 23
    const/4 v1, 0x1

    invoke-interface {v0}, Ljava/util/Set;->isEmpty()Z

    .line 24
    .line 25
    .line 26
    move-result v0

    .line 27
    const/4 v1, 0x5

    if-eqz v0, :cond_25

    .line 28
    .line 29
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j()V

    .line 30
    .line 31
    .line 32
    :cond_25
    const/4 v1, 0x4

    return-void
.end method

.method public final declared-synchronized i()V
    .locals 5

    .line 1
    const/4 v4, 0x6

    const-string v0, "ertg euefi: dk vaerctrodTiWLsi"

    const-string v0, "LiveWidgetTicker: started for "

    .line 2
    .line 3
    monitor-enter p0

    .line 4
    :try_start_6
    sget-boolean v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->n:Z
    :try_end_8
    .catchall {:try_start_6 .. :try_end_8} :catchall_62

    .line 5
    .line 6
    if-eqz v1, :cond_c

    .line 7
    .line 8
    monitor-exit p0

    .line 9
    return-void

    .line 10
    :cond_c
    :try_start_c
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 11
    .line 12
    invoke-interface {v1}, Ljava/util/Set;->isEmpty()Z

    .line 13
    .line 14
    .line 15
    move-result v1
    :try_end_12
    .catchall {:try_start_c .. :try_end_12} :catchall_62

    .line 16
    if-eqz v1, :cond_16

    .line 17
    .line 18
    monitor-exit p0

    .line 19
    return-void

    .line 20
    :cond_16
    :try_start_16
    new-instance v1, Landroid/os/HandlerThread;

    .line 21
    .line 22
    const/4 v4, 0x3

    const-string v2, "LiveWidgetTicker"

    .line 23
    .line 24
    invoke-direct {v1, v2}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    .line 25
    .line 26
    .line 27
    invoke-virtual {v1}, Ljava/lang/Thread;->start()V

    .line 28
    .line 29
    .line 30
    new-instance v2, Landroid/os/Handler;

    .line 31
    .line 32
    invoke-virtual {v1}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    .line 33
    .line 34
    .line 35
    move-result-object v3

    .line 36
    invoke-direct {v2, v3}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 37
    .line 38
    .line 39
    sput-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->l:Landroid/os/HandlerThread;

    .line 40
    .line 41
    sput-object v2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m:Landroid/os/Handler;

    .line 42
    .line 43
    const/4 v4, 0x1

    const/4 v1, 0x1

    .line 44
    sput-boolean v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->n:Z

    .line 45
    .line 46
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->j:Ljava/util/Set;

    .line 47
    .line 48
    invoke-interface {v1}, Ljava/util/Set;->size()I

    .line 49
    .line 50
    .line 51
    move-result v1

    .line 52
    const/4 v4, 0x2

    new-instance v3, Ljava/lang/StringBuilder;

    .line 53
    .line 54
    invoke-direct {v3, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 55
    .line 56
    .line 57
    const/4 v4, 0x6

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    .line 58
    .line 59
    .line 60
    const-string v0, " live widget(s)"

    .line 61
    .line 62
    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 63
    .line 64
    .line 65
    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 66
    .line 67
    .line 68
    move-result-object v0

    .line 69
    invoke-static {v0}, Lkjf;->f(Ljava/lang/String;)V

    .line 70
    .line 71
    .line 72
    const/4 v4, 0x2

    new-instance v0, Lrw7;

    .line 73
    .line 74
    const/16 v1, 0xf

    .line 75
    .line 76
    invoke-direct {v0, v1}, Lrw7;-><init>(I)V

    .line 77
    .line 78
    .line 79
    invoke-virtual {v2, v0}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 80
    .line 81
    .line 82
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->s:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;

    .line 83
    .line 84
    invoke-virtual {v2, v0}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
    :try_end_5e
    .catchall {:try_start_16 .. :try_end_5e} :catchall_62

    .line 85
    .line 86
    .line 87
    const/4 v4, 0x2

    monitor-exit p0

    .line 88
    const/4 v4, 0x6

    return-void

    .line 89
    :catchall_62
    move-exception v0

    .line 90
    :try_start_63
    monitor-exit p0
    :try_end_64
    .catchall {:try_start_63 .. :try_end_64} :catchall_62

    .line 91
    const/4 v4, 0x2

    throw v0
.end method

.method public final declared-synchronized j()V
    .locals 3

    .line 1
    const/4 v2, 0x4

    monitor-enter p0

    .line 2
    :try_start_2
    const/4 v2, 0x4

    sget-boolean v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->n:Z
    :try_end_5
    .catchall {:try_start_2 .. :try_end_5} :catchall_1a

    .line 3
    .line 4
    if-nez v0, :cond_b

    .line 5
    .line 6
    const/4 v2, 0x6

    monitor-exit p0

    .line 7
    const/4 v2, 0x4

    return-void

    .line 8
    :cond_b
    const/4 v2, 0x7

    const/4 v0, 0x0

    .line 9
    :try_start_d
    sput-boolean v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->n:Z

    .line 10
    .line 11
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m:Landroid/os/Handler;

    .line 12
    .line 13
    const/4 v2, 0x6

    if-eqz v0, :cond_1d

    .line 14
    .line 15
    sget-object v1, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->s:Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager$a;

    .line 16
    .line 17
    invoke-virtual {v0, v1}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V

    .line 18
    .line 19
    .line 20
    goto :goto_1d

    .line 21
    :catchall_1a
    move-exception v0

    .line 22
    const/4 v2, 0x6

    goto :goto_34

    .line 23
    :cond_1d
    :goto_1d
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->l:Landroid/os/HandlerThread;

    .line 24
    .line 25
    const/4 v2, 0x7

    if-eqz v0, :cond_25

    .line 26
    .line 27
    invoke-virtual {v0}, Landroid/os/HandlerThread;->quitSafely()Z

    .line 28
    .line 29
    .line 30
    :cond_25
    const/4 v2, 0x4

    const/4 v0, 0x0

    .line 31
    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->l:Landroid/os/HandlerThread;

    .line 32
    .line 33
    const/4 v2, 0x7

    sput-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m:Landroid/os/Handler;

    .line 34
    .line 35
    const/4 v2, 0x6

    const-string v0, "LiveWidgetTicker: stopped"

    .line 36
    .line 37
    invoke-static {v0}, Lkjf;->f(Ljava/lang/String;)V
    :try_end_32
    .catchall {:try_start_d .. :try_end_32} :catchall_1a

    .line 38
    .line 39
    .line 40
    monitor-exit p0

    .line 41
    return-void

    .line 42
    :goto_34
    :try_start_34
    monitor-exit p0
    :try_end_35
    .catchall {:try_start_34 .. :try_end_35} :catchall_1a

    .line 43
    throw v0
.end method

.method public final k()V
    .locals 3

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 2
    .line 3
    if-nez v0, :cond_5

    .line 4
    .line 5
    return-void

    .line 6
    :cond_5
    const/4 v2, 0x1

    sget-object v1, Lseh;->a:Lseh;

    .line 7
    .line 8
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 9
    .line 10
    .line 11
    const/4 v2, 0x2

    invoke-static {v0}, Lseh;->a(Landroid/content/Context;)Ljava/util/Map;

    .line 12
    .line 13
    .line 14
    move-result-object v1

    .line 15
    const/4 v2, 0x3

    invoke-interface {v1}, Ljava/util/Map;->keySet()Ljava/util/Set;

    .line 16
    .line 17
    .line 18
    move-result-object v1

    .line 19
    check-cast v1, Ljava/lang/Iterable;

    .line 20
    .line 21
    invoke-static {v1}, Lxj2;->j1(Ljava/lang/Iterable;)Ljava/util/List;

    .line 22
    .line 23
    .line 24
    move-result-object v1

    .line 25
    const/4 v2, 0x1

    invoke-virtual {p0, v0, v1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->l(Landroid/content/Context;Ljava/util/List;)V

    .line 26
    .line 27
    .line 28
    return-void
.end method

.method public final l(Landroid/content/Context;Ljava/util/List;)V
    .locals 2

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-interface {p2}, Ljava/util/List;->isEmpty()Z

    .line 5
    .line 6
    .line 7
    move-result v0

    .line 8
    const/4 v1, 0x3

    if-eqz v0, :cond_b

    .line 9
    .line 10
    return-void

    .line 11
    :cond_b
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    .line 12
    .line 13
    .line 14
    invoke-virtual {p1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    .line 15
    .line 16
    .line 17
    move-result-object p0

    .line 18
    const/4 v1, 0x4

    new-instance p1, Lyhh;

    .line 19
    .line 20
    const/4 v0, 0x0

    .line 21
    invoke-direct {p1, v0, p0, p2}, Lyhh;-><init>(Lm73;Landroid/content/Context;Ljava/util/List;)V

    .line 22
    .line 23
    .line 24
    const/4 p0, 0x3

    move v1, p0

    .line 25
    sget-object p2, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->b:Lg73;

    .line 26
    .line 27
    invoke-static {p2, v0, v0, p1, p0}, Ldt9;->N(Lu93;Li93;Ly93;Ljn6;I)Luze;

    .line 28
    .line 29
    .line 30
    return-void
.end method

.method public final m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;
    .locals 18

    move-object/from16 v0, p0

    move-object/from16 v1, p3

    instance-of v2, v1, Lcom/arlosoft/macrodroid/widget/custom/b;

    if-eqz v2, :cond_1d

    move-object v2, v1

    check-cast v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    iget v3, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    const/high16 v4, -0x80000000

    and-int v5, v3, v4

    if-eqz v5, :cond_17

    sub-int/2addr v3, v4

    iput v3, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    goto :goto_22

    :cond_17
    new-instance v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    invoke-direct {v2, v0, v1}, Lcom/arlosoft/macrodroid/widget/custom/b;-><init>(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Lo73;)V

    goto :goto_22

    :cond_1d
    new-instance v2, Lcom/arlosoft/macrodroid/widget/custom/b;

    invoke-direct {v2, v0, v1}, Lcom/arlosoft/macrodroid/widget/custom/b;-><init>(Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;Lo73;)V

    :goto_22
    iget-object v1, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->result:Ljava/lang/Object;

    sget-object v3, Lv93;->COROUTINE_SUSPENDED:Lv93;

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    const/4 v5, 0x1

    const/4 v6, 0x2

    const-string v7, ": "

    const-string v8, "Failed to update custom widget instance "

    const/4 v10, 0x0

    if-ne v4, v6, :cond_7f

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iget v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    check-cast v0, Lgy6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    move-object v12, v0

    check-cast v12, Ljava/util/Iterator;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    check-cast v0, Ljava/lang/Iterable;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    move-object v13, v0

    check-cast v13, Lhn9;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    move-object v14, v0

    check-cast v14, Lwx6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    check-cast v0, Ljava/util/List;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    move-object v15, v0

    check-cast v15, Landroid/content/Context;

    :try_start_55
    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_58
    .catch Ljava/lang/Exception; {:try_start_55 .. :try_end_58} :catch_59

    goto :goto_76

    :catch_59
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    :goto_76
    move-object/from16 v16, v10

    move-object v5, v14

    const/4 v1, 0x0

    move-object v14, v12

    move v12, v11

    const/4 v11, 0x0

    goto/16 :goto_103

    :cond_7f
    if-ne v4, v5, :cond_d9

    iget v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I

    iget v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iget v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    move-object v13, v0

    check-cast v13, Lgy6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    move-object v14, v0

    check-cast v14, Ljava/util/Iterator;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    check-cast v0, Ljava/lang/Iterable;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    move-object v15, v0

    check-cast v15, Lhn9;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    move-object/from16 v16, v0

    check-cast v16, Lwx6;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    check-cast v0, Ljava/util/List;

    iget-object v0, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    move-object/from16 v17, v0

    check-cast v17, Landroid/content/Context;

    :try_start_aa
    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V
    :try_end_ad
    .catch Ljava/lang/Exception; {:try_start_aa .. :try_end_ad} :catch_af

    move v0, v5

    goto :goto_cd

    :catch_af
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v11}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    const/4 v0, 0x0

    :goto_cd
    move v1, v11

    move v11, v4

    move v4, v1

    move v1, v0

    move-object/from16 v5, v16

    move-object/from16 v16, v13

    move-object v13, v15

    move-object/from16 v15, v17

    goto :goto_103

    :cond_d9
    if-nez v4, :cond_1c7

    invoke-static {v1}, Lu2f;->P(Ljava/lang/Object;)V

    invoke-interface/range {p2 .. p2}, Ljava/util/List;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_e7

    sget-object v0, Lblg;->a:Lblg;

    return-object v0

    :cond_e7
    invoke-virtual/range {p0 .. p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->a(Landroid/content/Context;)V

    new-instance v14, Lwx6;

    move-object/from16 v0, p1

    invoke-direct {v14, v0}, Lwx6;-><init>(Landroid/content/Context;)V

    new-instance v13, Lhn9;

    invoke-direct {v13}, Lhn9;-><init>()V

    invoke-interface/range {p2 .. p2}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    move-result-object v12

    move-object v15, v0

    move-object/from16 v16, v10

    move-object v5, v14

    const/4 v1, 0x0

    const/4 v4, 0x0

    const/4 v11, 0x0

    move-object v14, v12

    const/4 v12, 0x0

    :goto_103
    if-nez v1, :cond_17e

    invoke-interface {v14}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-nez v0, :cond_10e

    sget-object v0, Lblg;->a:Lblg;

    return-object v0

    :cond_10e
    invoke-interface {v14}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/Number;

    invoke-virtual {v0}, Ljava/lang/Number;->intValue()I

    move-result v4

    :try_start_118
    iget-object v0, v5, Lwx6;->b:Landroid/appwidget/AppWidgetManager;

    invoke-virtual {v0, v4}, Landroid/appwidget/AppWidgetManager;->getAppWidgetInfo(I)Landroid/appwidget/AppWidgetProviderInfo;

    move-result-object v0

    if-eqz v0, :cond_154

    new-instance v9, Lmh0;

    invoke-direct {v9, v4}, Lmh0;-><init>(I)V
    :try_end_125
    .catch Ljava/lang/Exception; {:try_start_118 .. :try_end_125} :catch_15f

    :try_start_125
    new-instance v0, Lzhh;

    invoke-direct {v0, v6, v10}, Lrff;-><init>(ILm73;)V

    iput-object v15, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    iput-object v5, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    iput-object v13, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    iput-object v14, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    iput-object v9, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    iput v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iput v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    const/4 v6, 0x0

    iput v6, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I
    :try_end_141
    .catch Ljava/lang/Exception; {:try_start_125 .. :try_end_141} :catch_14f

    const/4 v6, 0x1

    :try_start_142
    iput v6, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    invoke-static {v15, v9, v0, v2}, Lrjb;->M(Landroid/content/Context;Lgy6;Ljn6;Lo73;)Ljava/lang/Object;

    move-result-object v0
    :try_end_148
    .catch Ljava/lang/Exception; {:try_start_142 .. :try_end_148} :catch_14d

    if-ne v0, v3, :cond_14b

    goto :goto_1a0

    :cond_14b
    const/4 v11, 0x0

    goto :goto_181

    :catch_14d
    move-exception v0

    goto :goto_151

    :catch_14f
    move-exception v0

    const/4 v6, 0x1

    :goto_151
    move-object/from16 v16, v9

    goto :goto_161

    :cond_154
    const/4 v6, 0x1

    :try_start_155
    new-instance v0, Ljava/lang/IllegalArgumentException;

    const-string v9, "Invalid AppWidget ID."

    invoke-direct {v0, v9}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_15d
    .catch Ljava/lang/Exception; {:try_start_155 .. :try_end_15d} :catch_15d

    :catch_15d
    move-exception v0

    goto :goto_161

    :catch_15f
    move-exception v0

    const/4 v6, 0x1

    :goto_161
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v9, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v9

    invoke-virtual {v9, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v9

    invoke-virtual {v9, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    goto :goto_1c4

    :cond_17e
    const/4 v6, 0x1

    move-object/from16 v9, v16

    :goto_181
    :try_start_181
    iput-object v15, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$0:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$1:Ljava/lang/Object;

    iput-object v5, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$2:Ljava/lang/Object;

    iput-object v13, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$3:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$4:Ljava/lang/Object;

    iput-object v14, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$5:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$6:Ljava/lang/Object;

    iput-object v10, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->L$7:Ljava/lang/Object;

    iput v12, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$0:I

    iput v4, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$1:I

    iput v11, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->I$2:I
    :try_end_197
    .catch Ljava/lang/Exception; {:try_start_181 .. :try_end_197} :catch_1a3

    const/4 v1, 0x2

    :try_start_198
    iput v1, v2, Lcom/arlosoft/macrodroid/widget/custom/b;->label:I

    invoke-virtual {v13, v15, v9, v2}, Lrx6;->d(Landroid/content/Context;Lgy6;Lo73;)Ljava/lang/Object;

    move-result-object v0
    :try_end_19e
    .catch Ljava/lang/Exception; {:try_start_198 .. :try_end_19e} :catch_1a1

    if-ne v0, v3, :cond_1c1

    :goto_1a0
    return-object v3

    :catch_1a1
    move-exception v0

    goto :goto_1a5

    :catch_1a3
    move-exception v0

    const/4 v1, 0x2

    :goto_1a5
    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    :cond_1c1
    move-object/from16 v16, v9

    const/4 v1, 0x0

    :goto_1c4
    const/4 v6, 0x2

    goto/16 :goto_103

    :cond_1c7
    const-string v0, "call to \'resume\' before \'invoke\' with coroutine"

    invoke-static {v0}, Le6d;->r(Ljava/lang/String;)V

    return-object v10
.end method

.method public final n(Ljava/lang/String;)V
    .locals 3

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    sget-object v0, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->d:Landroid/content/Context;

    .line 5
    .line 6
    if-nez v0, :cond_8

    .line 7
    .line 8
    goto :goto_18

    .line 9
    :cond_8
    sget-object v1, Lseh;->a:Lseh;

    .line 10
    .line 11
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 12
    .line 13
    .line 14
    invoke-static {v0, p1}, Lseh;->b(Landroid/content/Context;Ljava/lang/String;)Ljava/util/ArrayList;

    .line 15
    .line 16
    .line 17
    move-result-object p1

    .line 18
    const/4 v2, 0x4

    invoke-virtual {p1}, Ljava/util/ArrayList;->isEmpty()Z

    .line 19
    .line 20
    .line 21
    move-result v1

    .line 22
    if-eqz v1, :cond_19

    .line 23
    .line 24
    :goto_18
    return-void

    .line 25
    :cond_19
    const/4 v2, 0x6

    invoke-virtual {p0, v0, p1}, Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->l(Landroid/content/Context;Ljava/util/List;)V

    .line 26
    .line 27
    .line 28
    return-void
.end method
