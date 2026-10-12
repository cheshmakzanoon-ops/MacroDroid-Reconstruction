.class public Lagency/tango/materialintroscreen/widgets/InkPageIndicator;
.super Landroid/view/View;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Lz5h;
.implements Landroid/view/View$OnAttachStateChangeListener;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;
    }
.end annotation


# static fields
.field public static final synthetic K:I


# instance fields
.field public A:F

.field public B:F

.field public C:[F

.field public D:Z

.field public E:Z

.field public F:Landroid/graphics/Paint;

.field public final G:Landroid/graphics/Path;

.field public H:Landroid/animation/ValueAnimator;

.field public I:Lmz7;

.field public J:[Lnz7;

.field public final a:Landroid/graphics/Paint;

.field public final b:Landroid/graphics/Path;

.field public final c:Landroid/graphics/Path;

.field public final d:Landroid/graphics/Path;

.field public final e:Landroid/graphics/RectF;

.field public final f:Los5;

.field public g:F

.field public h:F

.field public final i:I

.field public final j:I

.field public final k:J

.field public l:I

.field public final m:F

.field public final n:F

.field public final o:J

.field public p:F

.field public q:F

.field public r:F

.field public s:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

.field public t:I

.field public u:I

.field public v:I

.field public w:F

.field public x:Z

.field public y:[F

.field public z:[F


# direct methods
.method public constructor <init>(Landroid/content/Context;Landroid/util/AttributeSet;)V
    .locals 2

    const/4 v0, 0x0

    .line 162
    invoke-direct {p0, p1, p2, v0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V

    const/4 v1, 0x1

    return-void
.end method

.method public constructor <init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V
    .locals 5

    .line 1
    invoke-direct {p0, p1, p2, p3}, Landroid/view/View;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V

    .line 2
    .line 3
    .line 4
    invoke-virtual {p1}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    .line 5
    .line 6
    .line 7
    move-result-object p1

    .line 8
    const/4 v4, 0x0

    invoke-virtual {p1}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    .line 9
    .line 10
    .line 11
    move-result-object p1

    .line 12
    const/4 v4, 0x5

    iget p1, p1, Landroid/util/DisplayMetrics;->density:F

    .line 13
    .line 14
    float-to-int p1, p1

    .line 15
    const/4 v4, 0x5

    invoke-virtual {p0}, Landroid/view/View;->getContext()Landroid/content/Context;

    .line 16
    .line 17
    .line 18
    move-result-object v0

    .line 19
    const/4 v4, 0x1

    sget-object v1, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator:[I

    .line 20
    .line 21
    const/4 v2, 0x0

    .line 22
    const/4 v4, 0x4

    invoke-virtual {v0, p2, v1, p3, v2}, Landroid/content/Context;->obtainStyledAttributes(Landroid/util/AttributeSet;[III)Landroid/content/res/TypedArray;

    .line 23
    .line 24
    .line 25
    move-result-object p2

    .line 26
    const/4 v4, 0x0

    sget p3, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator_dotDiameter:I

    .line 27
    .line 28
    const/4 v4, 0x5

    mul-int/lit8 v0, p1, 0x8

    .line 29
    .line 30
    const/4 v4, 0x5

    invoke-virtual {p2, p3, v0}, Landroid/content/res/TypedArray;->getDimensionPixelSize(II)I

    .line 31
    .line 32
    .line 33
    move-result p3

    .line 34
    const/4 v4, 0x3

    iput p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->i:I

    .line 35
    .line 36
    div-int/lit8 p3, p3, 0x2

    .line 37
    .line 38
    int-to-float p3, p3

    .line 39
    iput p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->m:F

    .line 40
    .line 41
    const/high16 v0, 0x40000000    # 2.0f

    .line 42
    .line 43
    const/4 v4, 0x6

    div-float/2addr p3, v0

    .line 44
    const/4 v4, 0x0

    iput p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->n:F

    .line 45
    .line 46
    sget p3, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator_dotGap:I

    .line 47
    .line 48
    mul-int/lit8 p1, p1, 0xc

    .line 49
    .line 50
    const/4 v4, 0x2

    invoke-virtual {p2, p3, p1}, Landroid/content/res/TypedArray;->getDimensionPixelSize(II)I

    .line 51
    .line 52
    .line 53
    move-result p1

    .line 54
    const/4 v4, 0x2

    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->j:I

    .line 55
    .line 56
    sget p1, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator_animationDuration:I

    .line 57
    .line 58
    const/4 v4, 0x6

    const/16 p3, 0x190

    .line 59
    .line 60
    invoke-virtual {p2, p1, p3}, Landroid/content/res/TypedArray;->getInteger(II)I

    .line 61
    .line 62
    .line 63
    move-result p1

    .line 64
    int-to-long v0, p1

    .line 65
    iput-wide v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->k:J

    .line 66
    .line 67
    const-wide/16 v2, 0x2

    .line 68
    .line 69
    div-long/2addr v0, v2

    .line 70
    iput-wide v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->o:J

    .line 71
    .line 72
    const/4 v4, 0x0

    sget p1, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator_pageIndicatorColor:I

    .line 73
    .line 74
    const/4 v4, 0x1

    const p3, -0x7f000001

    .line 75
    .line 76
    .line 77
    invoke-virtual {p2, p1, p3}, Landroid/content/res/TypedArray;->getColor(II)I

    .line 78
    .line 79
    .line 80
    move-result p1

    .line 81
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->l:I

    .line 82
    .line 83
    sget p1, Lagency/tango/materialintroscreen/R$styleable;->InkPageIndicator_currentPageIndicatorColor:I

    .line 84
    .line 85
    const/4 v4, 0x6

    const/4 p3, -0x1

    .line 86
    invoke-virtual {p2, p1, p3}, Landroid/content/res/TypedArray;->getColor(II)I

    .line 87
    .line 88
    .line 89
    move-result p1

    .line 90
    invoke-virtual {p2}, Landroid/content/res/TypedArray;->recycle()V

    .line 91
    .line 92
    .line 93
    new-instance p2, Landroid/graphics/Paint;

    .line 94
    .line 95
    const/4 p3, 0x1

    .line 96
    const/4 v4, 0x5

    invoke-direct {p2, p3}, Landroid/graphics/Paint;-><init>(I)V

    .line 97
    .line 98
    .line 99
    iput-object p2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->F:Landroid/graphics/Paint;

    .line 100
    .line 101
    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->l:I

    .line 102
    .line 103
    invoke-virtual {p2, v0}, Landroid/graphics/Paint;->setColor(I)V

    .line 104
    .line 105
    .line 106
    new-instance p2, Landroid/graphics/Paint;

    .line 107
    .line 108
    invoke-direct {p2, p3}, Landroid/graphics/Paint;-><init>(I)V

    .line 109
    .line 110
    .line 111
    const/4 v4, 0x5

    iput-object p2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->a:Landroid/graphics/Paint;

    .line 112
    .line 113
    invoke-virtual {p2, p1}, Landroid/graphics/Paint;->setColor(I)V

    .line 114
    .line 115
    .line 116
    new-instance p1, Los5;

    .line 117
    .line 118
    invoke-direct {p1, p3}, Los5;-><init>(I)V

    .line 119
    .line 120
    .line 121
    const/4 v4, 0x3

    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f:Los5;

    .line 122
    .line 123
    const/4 v4, 0x0

    new-instance p1, Landroid/graphics/Path;

    .line 124
    .line 125
    invoke-direct {p1}, Landroid/graphics/Path;-><init>()V

    .line 126
    .line 127
    .line 128
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->G:Landroid/graphics/Path;

    .line 129
    .line 130
    new-instance p1, Landroid/graphics/Path;

    .line 131
    .line 132
    invoke-direct {p1}, Landroid/graphics/Path;-><init>()V

    .line 133
    .line 134
    .line 135
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->b:Landroid/graphics/Path;

    .line 136
    .line 137
    new-instance p1, Landroid/graphics/Path;

    .line 138
    .line 139
    invoke-direct {p1}, Landroid/graphics/Path;-><init>()V

    .line 140
    .line 141
    .line 142
    const/4 v4, 0x2

    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->c:Landroid/graphics/Path;

    .line 143
    .line 144
    new-instance p1, Landroid/graphics/Path;

    .line 145
    .line 146
    const/4 v4, 0x1

    invoke-direct {p1}, Landroid/graphics/Path;-><init>()V

    .line 147
    .line 148
    .line 149
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->d:Landroid/graphics/Path;

    .line 150
    .line 151
    new-instance p1, Landroid/graphics/RectF;

    .line 152
    .line 153
    invoke-direct {p1}, Landroid/graphics/RectF;-><init>()V

    .line 154
    .line 155
    .line 156
    const/4 v4, 0x3

    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->e:Landroid/graphics/RectF;

    .line 157
    .line 158
    invoke-virtual {p0, p0}, Landroid/view/View;->addOnAttachStateChangeListener(Landroid/view/View$OnAttachStateChangeListener;)V

    .line 159
    .line 160
    .line 161
    return-void
.end method

.method public static bridge synthetic a(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;)I
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getCount()I

    .line 2
    .line 3
    .line 4
    move-result p0

    .line 5
    const/4 v0, 0x1

    return p0
.end method

.method public static bridge synthetic e(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;I)V
    .locals 1

    .line 1
    invoke-direct {p0, p1}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->setPageCount(I)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method private getCount()I
    .locals 1

    .line 1
    iget-object p0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->s:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 2
    .line 3
    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->getAdapter()Lcre;

    .line 4
    .line 5
    .line 6
    move-result-object p0

    .line 7
    const/4 v0, 0x2

    invoke-virtual {p0}, Lcre;->n()I

    .line 8
    .line 9
    .line 10
    move-result p0

    .line 11
    return p0
.end method

.method private getDesiredHeight()I
    .locals 3

    .line 1
    invoke-virtual {p0}, Landroid/view/View;->getPaddingTop()I

    .line 2
    .line 3
    .line 4
    move-result v0

    .line 5
    iget v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->i:I

    .line 6
    .line 7
    add-int/2addr v0, v1

    .line 8
    invoke-virtual {p0}, Landroid/view/View;->getPaddingBottom()I

    .line 9
    .line 10
    .line 11
    move-result p0

    .line 12
    const/4 v2, 0x7

    add-int/2addr p0, v0

    .line 13
    const/4 v2, 0x7

    return p0
.end method

.method private getDesiredWidth()I
    .locals 3

    .line 1
    invoke-virtual {p0}, Landroid/view/View;->getPaddingLeft()I

    .line 2
    .line 3
    .line 4
    move-result v0

    .line 5
    const/4 v2, 0x2

    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getRequiredWidth()I

    .line 6
    .line 7
    .line 8
    move-result v1

    .line 9
    const/4 v2, 0x3

    add-int/2addr v0, v1

    .line 10
    const/4 v2, 0x3

    invoke-virtual {p0}, Landroid/view/View;->getPaddingRight()I

    .line 11
    .line 12
    .line 13
    move-result p0

    .line 14
    add-int/2addr p0, v0

    .line 15
    return p0
.end method

.method private getRequiredWidth()I
    .locals 3

    .line 1
    const/4 v2, 0x7

    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 2
    .line 3
    iget v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->i:I

    .line 4
    .line 5
    const/4 v2, 0x3

    mul-int/2addr v1, v0

    .line 6
    add-int/lit8 v0, v0, -0x1

    .line 7
    .line 8
    iget p0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->j:I

    .line 9
    .line 10
    mul-int/2addr v0, p0

    .line 11
    add-int/2addr v0, v1

    .line 12
    return v0
.end method

.method private getRetreatingJoinPath()Landroid/graphics/Path;
    .locals 7

    .line 1
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->b:Landroid/graphics/Path;

    .line 2
    .line 3
    invoke-virtual {v0}, Landroid/graphics/Path;->rewind()V

    .line 4
    .line 5
    .line 6
    iget v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 7
    .line 8
    const/4 v6, 0x4

    iget v2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 9
    .line 10
    iget v3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 11
    .line 12
    iget v4, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 13
    .line 14
    const/4 v6, 0x5

    iget-object v5, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->e:Landroid/graphics/RectF;

    .line 15
    .line 16
    invoke-virtual {v5, v1, v2, v3, v4}, Landroid/graphics/RectF;->set(FFFF)V

    .line 17
    .line 18
    .line 19
    iget p0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->m:F

    .line 20
    .line 21
    sget-object v1, Landroid/graphics/Path$Direction;->CW:Landroid/graphics/Path$Direction;

    .line 22
    .line 23
    invoke-virtual {v0, v5, p0, p0, v1}, Landroid/graphics/Path;->addRoundRect(Landroid/graphics/RectF;FFLandroid/graphics/Path$Direction;)V

    .line 24
    .line 25
    .line 26
    const/4 v6, 0x6

    return-object v0
.end method

.method private setPageCount(I)V
    .locals 1

    .line 1
    const/4 v0, 0x3

    if-lez p1, :cond_c

    .line 2
    .line 3
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 4
    .line 5
    const/4 v0, 0x2

    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f()V

    .line 6
    .line 7
    .line 8
    invoke-virtual {p0}, Landroid/view/View;->requestLayout()V

    .line 9
    .line 10
    .line 11
    :cond_c
    return-void
.end method

.method private setSelectedPage(I)V
    .locals 11

    .line 1
    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 2
    .line 3
    if-ne p1, v0, :cond_6

    .line 4
    .line 5
    goto/16 :goto_e7

    .line 6
    .line 7
    :cond_6
    const/4 v10, 0x4

    const/4 v1, 0x1

    .line 8
    const/4 v10, 0x4

    iput-boolean v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->E:Z

    .line 9
    .line 10
    const/4 v10, 0x4

    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 11
    .line 12
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 13
    .line 14
    sub-int v0, p1, v0

    .line 15
    .line 16
    const/4 v10, 0x1

    invoke-static {v0}, Ljava/lang/Math;->abs(I)I

    .line 17
    .line 18
    .line 19
    move-result v6

    .line 20
    const/4 v0, 0x0

    .line 21
    const/4 v10, 0x7

    if-le v6, v1, :cond_5a

    .line 22
    .line 23
    iget v2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 24
    .line 25
    const/high16 v3, 0x3f800000    # 1.0f

    .line 26
    .line 27
    const/4 v10, 0x2

    if-le p1, v2, :cond_3b

    .line 28
    .line 29
    move v2, v0

    .line 30
    :goto_23
    if-ge v2, v6, :cond_5a

    .line 31
    .line 32
    iget v4, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 33
    .line 34
    add-int/2addr v4, v2

    .line 35
    const/4 v10, 0x5

    iget-object v5, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 36
    .line 37
    if-eqz v5, :cond_38

    .line 38
    .line 39
    const/4 v10, 0x5

    array-length v7, v5

    .line 40
    if-ge v4, v7, :cond_38

    .line 41
    .line 42
    aput v3, v5, v4

    .line 43
    .line 44
    sget-object v4, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 45
    .line 46
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 47
    .line 48
    .line 49
    :cond_38
    add-int/lit8 v2, v2, 0x1

    .line 50
    .line 51
    goto :goto_23

    .line 52
    :cond_3b
    const/4 v10, 0x4

    const/4 v2, -0x1

    .line 53
    :goto_3d
    neg-int v4, v6

    .line 54
    const/4 v10, 0x1

    if-le v2, v4, :cond_5a

    .line 55
    .line 56
    const/4 v10, 0x6

    iget v4, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 57
    .line 58
    add-int/2addr v4, v2

    .line 59
    const/4 v10, 0x1

    iget-object v5, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 60
    .line 61
    if-eqz v5, :cond_55

    .line 62
    .line 63
    array-length v7, v5

    .line 64
    if-ge v4, v7, :cond_55

    .line 65
    .line 66
    aput v3, v5, v4

    .line 67
    .line 68
    sget-object v4, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 69
    .line 70
    const/4 v10, 0x7

    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 71
    .line 72
    .line 73
    :cond_55
    const/4 v10, 0x7

    add-int/lit8 v2, v2, -0x1

    .line 74
    .line 75
    const/4 v10, 0x2

    goto :goto_3d

    .line 76
    :cond_5a
    const/4 v10, 0x4

    iget-object v2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 77
    .line 78
    if-eqz v2, :cond_e7

    .line 79
    .line 80
    aget v2, v2, p1

    .line 81
    .line 82
    const/4 v10, 0x2

    iget v4, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 83
    .line 84
    iget v3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 85
    .line 86
    const/4 v10, 0x0

    const/4 v5, 0x2

    .line 87
    new-array v5, v5, [F

    .line 88
    .line 89
    const/4 v10, 0x0

    aput v3, v5, v0

    .line 90
    .line 91
    const/4 v10, 0x7

    aput v2, v5, v1

    .line 92
    .line 93
    invoke-static {v5}, Landroid/animation/ValueAnimator;->ofFloat([F)Landroid/animation/ValueAnimator;

    .line 94
    .line 95
    .line 96
    move-result-object v8

    .line 97
    move v3, v2

    .line 98
    new-instance v2, Lmz7;

    .line 99
    .line 100
    iget v5, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 101
    .line 102
    const/high16 v7, 0x3e800000    # 0.25f

    .line 103
    .line 104
    if-le p1, v4, :cond_8f

    .line 105
    .line 106
    new-instance v9, Ljz7;

    .line 107
    .line 108
    const/4 v10, 0x0

    sub-float v5, v3, v5

    .line 109
    .line 110
    const/4 v10, 0x7

    mul-float/2addr v5, v7

    .line 111
    sub-float/2addr v3, v5

    .line 112
    invoke-direct {v9, v3, v1}, Ljz7;-><init>(FI)V

    .line 113
    .line 114
    .line 115
    :goto_88
    move-object v3, p0

    .line 116
    const/4 v10, 0x2

    move v5, p1

    .line 117
    move-object v7, v9

    move-object v7, v9

    .line 118
    const/4 v10, 0x5

    goto :goto_9b

    .line 119
    :cond_8f
    const/4 v10, 0x6

    new-instance v9, Ljz7;

    .line 120
    .line 121
    invoke-static {v5, v3, v7, v3}, Lq77;->t(FFFF)F

    .line 122
    .line 123
    .line 124
    move-result v3

    .line 125
    const/4 v10, 0x6

    invoke-direct {v9, v3, v0}, Ljz7;-><init>(FI)V

    .line 126
    .line 127
    .line 128
    goto :goto_88

    .line 129
    :goto_9b
    invoke-direct/range {v2 .. v7}, Lmz7;-><init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;IIILjz7;)V

    .line 130
    .line 131
    .line 132
    iput-object v2, v3, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->I:Lmz7;

    .line 133
    .line 134
    new-instance p0, Liz7;

    .line 135
    .line 136
    invoke-direct {p0, v3, v0}, Liz7;-><init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;I)V

    .line 137
    .line 138
    .line 139
    invoke-virtual {v2, p0}, Landroid/animation/Animator;->addListener(Landroid/animation/Animator$AnimatorListener;)V

    .line 140
    .line 141
    .line 142
    new-instance p0, Lx82;

    .line 143
    .line 144
    const/4 v10, 0x5

    const/4 p1, 0x5

    .line 145
    invoke-direct {p0, v3, p1}, Lx82;-><init>(Ljava/lang/Object;I)V

    .line 146
    .line 147
    .line 148
    const/4 v10, 0x0

    invoke-virtual {v8, p0}, Landroid/animation/ValueAnimator;->addUpdateListener(Landroid/animation/ValueAnimator$AnimatorUpdateListener;)V

    .line 149
    .line 150
    .line 151
    const/4 v10, 0x2

    new-instance p0, Liz7;

    .line 152
    .line 153
    invoke-direct {p0, v3, v1}, Liz7;-><init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;I)V

    .line 154
    .line 155
    .line 156
    invoke-virtual {v8, p0}, Landroid/animation/Animator;->addListener(Landroid/animation/Animator$AnimatorListener;)V

    .line 157
    .line 158
    .line 159
    iget-boolean p0, v3, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->x:Z

    .line 160
    .line 161
    const/4 v10, 0x6

    const-wide/16 v0, 0x4

    .line 162
    .line 163
    const/4 v10, 0x7

    iget-wide v4, v3, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->k:J

    .line 164
    .line 165
    const/4 v10, 0x1

    if-eqz p0, :cond_cc

    .line 166
    .line 167
    const/4 v10, 0x0

    div-long p0, v4, v0

    .line 168
    .line 169
    const/4 v10, 0x5

    goto :goto_ce

    .line 170
    :cond_cc
    const-wide/16 p0, 0x0

    .line 171
    .line 172
    :goto_ce
    invoke-virtual {v8, p0, p1}, Landroid/animation/ValueAnimator;->setStartDelay(J)V

    .line 173
    .line 174
    .line 175
    const-wide/16 p0, 0x3

    const-wide/16 p0, 0x3

    .line 176
    .line 177
    const/4 v10, 0x4

    mul-long/2addr v4, p0

    .line 178
    div-long/2addr v4, v0

    .line 179
    const/4 v10, 0x4

    invoke-virtual {v8, v4, v5}, Landroid/animation/ValueAnimator;->setDuration(J)Landroid/animation/ValueAnimator;

    .line 180
    .line 181
    .line 182
    iget-object p0, v3, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f:Los5;

    .line 183
    .line 184
    invoke-virtual {v8, p0}, Landroid/animation/ValueAnimator;->setInterpolator(Landroid/animation/TimeInterpolator;)V

    .line 185
    .line 186
    .line 187
    const/4 v10, 0x1

    iput-object v8, v3, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->H:Landroid/animation/ValueAnimator;

    .line 188
    .line 189
    invoke-virtual {v8}, Landroid/animation/ValueAnimator;->start()V

    .line 190
    .line 191
    .line 192
    :cond_e7
    :goto_e7
    return-void
.end method


# virtual methods
.method public final b(IFI)V
    .locals 2

    .line 1
    iget-boolean p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->D:Z

    .line 2
    .line 3
    const/4 v1, 0x6

    if-eqz p3, :cond_2e

    .line 4
    .line 5
    iget-boolean p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->E:Z

    .line 6
    .line 7
    if-eqz p3, :cond_d

    .line 8
    .line 9
    const/4 v1, 0x0

    iget p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->v:I

    .line 10
    .line 11
    goto :goto_10

    .line 12
    :cond_d
    const/4 v1, 0x0

    iget p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 13
    .line 14
    :goto_10
    if-eq p3, p1, :cond_1e

    .line 15
    .line 16
    const/high16 v0, 0x3f800000    # 1.0f

    .line 17
    .line 18
    sub-float p2, v0, p2

    .line 19
    .line 20
    cmpl-float v0, p2, v0

    .line 21
    .line 22
    if-nez v0, :cond_1e

    .line 23
    .line 24
    invoke-static {p3, p1}, Ljava/lang/Math;->min(II)I

    .line 25
    .line 26
    .line 27
    move-result p1

    .line 28
    :cond_1e
    iget-object p3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 29
    .line 30
    if-eqz p3, :cond_2e

    .line 31
    .line 32
    const/4 v1, 0x7

    array-length v0, p3

    .line 33
    if-ge p1, v0, :cond_2e

    .line 34
    .line 35
    const/4 v1, 0x3

    aput p2, p3, p1

    .line 36
    .line 37
    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 38
    .line 39
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 40
    .line 41
    .line 42
    :cond_2e
    return-void
.end method

.method public final c(I)V
    .locals 1

    .line 1
    return-void
.end method

.method public final d(I)V
    .locals 2

    .line 1
    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 2
    .line 3
    if-ge p1, v0, :cond_12

    .line 4
    .line 5
    iget-boolean v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->D:Z

    .line 6
    .line 7
    const/4 v1, 0x2

    if-eqz v0, :cond_e

    .line 8
    .line 9
    const/4 v1, 0x2

    invoke-direct {p0, p1}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->setSelectedPage(I)V

    .line 10
    .line 11
    .line 12
    return-void

    .line 13
    :cond_e
    const/4 v1, 0x6

    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g()V

    .line 14
    .line 15
    .line 16
    :cond_12
    return-void
.end method

.method public final f()V
    .locals 4

    .line 1
    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 2
    .line 3
    const/4 v3, 0x3

    const/4 v1, 0x1

    .line 4
    const/4 v3, 0x5

    sub-int/2addr v0, v1

    .line 5
    const/4 v3, 0x5

    new-array v0, v0, [F

    .line 6
    .line 7
    iput-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 8
    .line 9
    const/4 v2, 0x0

    .line 10
    invoke-static {v0, v2}, Ljava/util/Arrays;->fill([FF)V

    .line 11
    .line 12
    .line 13
    const/4 v3, 0x7

    iget v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 14
    .line 15
    new-array v0, v0, [F

    .line 16
    .line 17
    iput-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->C:[F

    .line 18
    .line 19
    const/4 v3, 0x3

    invoke-static {v0, v2}, Ljava/util/Arrays;->fill([FF)V

    .line 20
    .line 21
    .line 22
    const/4 v3, 0x0

    const/high16 v0, -0x40800000    # -1.0f

    .line 23
    .line 24
    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 25
    .line 26
    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 27
    .line 28
    iput-boolean v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->x:Z

    .line 29
    .line 30
    const/4 v3, 0x6

    return-void
.end method

.method public final g()V
    .locals 3

    .line 1
    const/4 v2, 0x3

    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->s:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 2
    .line 3
    const/4 v2, 0x3

    if-eqz v0, :cond_10

    .line 4
    .line 5
    const/4 v2, 0x6

    invoke-virtual {v0}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 6
    .line 7
    .line 8
    move-result v0

    .line 9
    const/4 v2, 0x1

    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 10
    .line 11
    const/4 v2, 0x3

    goto :goto_15

    .line 12
    :cond_10
    const/4 v2, 0x0

    const/4 v0, 0x0

    .line 13
    const/4 v2, 0x1

    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 14
    .line 15
    :goto_15
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 16
    .line 17
    if-eqz v0, :cond_30

    .line 18
    .line 19
    const/4 v2, 0x6

    array-length v0, v0

    .line 20
    if-lez v0, :cond_30

    .line 21
    .line 22
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->H:Landroid/animation/ValueAnimator;

    .line 23
    .line 24
    if-eqz v0, :cond_28

    .line 25
    .line 26
    invoke-virtual {v0}, Landroid/animation/ValueAnimator;->isStarted()Z

    .line 27
    .line 28
    .line 29
    move-result v0

    .line 30
    const/4 v2, 0x3

    if-nez v0, :cond_30

    .line 31
    .line 32
    :cond_28
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 33
    .line 34
    iget v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 35
    .line 36
    aget v0, v0, v1

    .line 37
    .line 38
    iput v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 39
    .line 40
    :cond_30
    return-void
.end method

.method public final onDraw(Landroid/graphics/Canvas;)V
    .locals 39

    .line 1
    move-object/from16 v0, p0

    .line 2
    .line 3
    move-object/from16 v1, p1

    .line 4
    .line 5
    iget-object v2, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->s:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 6
    .line 7
    if-eqz v2, :cond_22a

    .line 8
    .line 9
    iget v2, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 10
    .line 11
    if-nez v2, :cond_e

    .line 12
    .line 13
    goto/16 :goto_22a

    .line 14
    .line 15
    :cond_e
    iget-object v2, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->G:Landroid/graphics/Path;

    .line 16
    .line 17
    invoke-virtual {v2}, Landroid/graphics/Path;->rewind()V

    .line 18
    .line 19
    .line 20
    const/4 v3, 0x0

    .line 21
    :goto_14
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 22
    .line 23
    iget v5, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->m:F

    .line 24
    .line 25
    const/high16 v6, -0x40800000    # -1.0f

    .line 26
    .line 27
    if-ge v3, v4, :cond_20d

    .line 28
    .line 29
    add-int/lit8 v4, v4, -0x1

    .line 30
    .line 31
    if-ne v3, v4, :cond_22

    .line 32
    .line 33
    move v7, v3

    .line 34
    goto :goto_24

    .line 35
    :cond_22
    add-int/lit8 v7, v3, 0x1

    .line 36
    .line 37
    :goto_24
    iget-object v8, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 38
    .line 39
    aget v14, v8, v3

    .line 40
    .line 41
    aget v7, v8, v7

    .line 42
    .line 43
    if-ne v3, v4, :cond_2f

    .line 44
    .line 45
    move v4, v6

    move v4, v6

    .line 46
    goto :goto_33

    .line 47
    :cond_2f
    iget-object v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 48
    .line 49
    aget v4, v4, v3

    .line 50
    .line 51
    :goto_33
    iget-object v8, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->C:[F

    .line 52
    .line 53
    aget v8, v8, v3

    .line 54
    .line 55
    iget-object v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->b:Landroid/graphics/Path;

    .line 56
    .line 57
    invoke-virtual {v9}, Landroid/graphics/Path;->rewind()V

    .line 58
    .line 59
    .line 60
    const/4 v10, 0x0

    .line 61
    cmpl-float v11, v4, v10

    .line 62
    .line 63
    if-eqz v11, :cond_45

    .line 64
    .line 65
    cmpl-float v12, v4, v6

    .line 66
    .line 67
    if-nez v12, :cond_5c

    .line 68
    .line 69
    :cond_45
    cmpl-float v10, v8, v10

    .line 70
    .line 71
    if-nez v10, :cond_5c

    .line 72
    .line 73
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 74
    .line 75
    if-ne v3, v10, :cond_51

    .line 76
    .line 77
    iget-boolean v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->x:Z

    .line 78
    .line 79
    if-nez v10, :cond_5c

    .line 80
    .line 81
    :cond_51
    iget-object v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 82
    .line 83
    aget v10, v10, v3

    .line 84
    .line 85
    iget v12, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 86
    .line 87
    sget-object v13, Landroid/graphics/Path$Direction;->CW:Landroid/graphics/Path$Direction;

    .line 88
    .line 89
    invoke-virtual {v9, v10, v12, v5, v13}, Landroid/graphics/Path;->addCircle(FFFLandroid/graphics/Path$Direction;)V

    .line 90
    .line 91
    .line 92
    :cond_5c
    const/high16 v22, 0x3f000000    # 0.5f

    .line 93
    .line 94
    iget v12, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->j:I

    .line 95
    .line 96
    move/from16 v23, v6

    .line 97
    .line 98
    iget-object v6, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->e:Landroid/graphics/RectF;

    .line 99
    .line 100
    if-lez v11, :cond_127

    .line 101
    .line 102
    cmpg-float v11, v4, v22

    .line 103
    .line 104
    if-gtz v11, :cond_127

    .line 105
    .line 106
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 107
    .line 108
    cmpl-float v11, v11, v23

    .line 109
    .line 110
    if-nez v11, :cond_127

    .line 111
    .line 112
    iget-object v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->c:Landroid/graphics/Path;

    .line 113
    .line 114
    invoke-virtual {v11}, Landroid/graphics/Path;->rewind()V

    .line 115
    .line 116
    .line 117
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 118
    .line 119
    invoke-virtual {v11, v14, v10}, Landroid/graphics/Path;->moveTo(FF)V

    .line 120
    .line 121
    .line 122
    sub-float v10, v14, v5

    .line 123
    .line 124
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 125
    .line 126
    add-float v15, v14, v5

    .line 127
    .line 128
    move/from16 v31, v3

    .line 129
    .line 130
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 131
    .line 132
    invoke-virtual {v6, v10, v13, v15, v3}, Landroid/graphics/RectF;->set(FFFF)V

    .line 133
    .line 134
    .line 135
    const/4 v3, 0x1

    .line 136
    const/high16 v10, 0x43340000    # 180.0f

    .line 137
    .line 138
    const/high16 v13, 0x42b40000    # 90.0f

    .line 139
    .line 140
    invoke-virtual {v11, v6, v13, v10, v3}, Landroid/graphics/Path;->arcTo(Landroid/graphics/RectF;FFZ)V

    .line 141
    .line 142
    .line 143
    int-to-float v3, v12

    .line 144
    mul-float/2addr v3, v4

    .line 145
    add-float/2addr v15, v3

    .line 146
    iput v15, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 147
    .line 148
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 149
    .line 150
    iput v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 151
    .line 152
    move/from16 v18, v3

    .line 153
    .line 154
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->n:F

    .line 155
    .line 156
    add-float v25, v14, v3

    .line 157
    .line 158
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 159
    .line 160
    sub-float v28, v10, v3

    .line 161
    .line 162
    move/from16 v29, v15

    move/from16 v29, v15

    .line 163
    .line 164
    move/from16 v30, v10

    .line 165
    .line 166
    move-object/from16 v24, v11

    .line 167
    .line 168
    move/from16 v26, v13

    move/from16 v26, v13

    .line 169
    .line 170
    move/from16 v27, v15

    .line 171
    .line 172
    invoke-virtual/range {v24 .. v30}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 173
    .line 174
    .line 175
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 176
    .line 177
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 178
    .line 179
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 180
    .line 181
    add-float/2addr v11, v3

    .line 182
    move v15, v13

    move v15, v13

    .line 183
    move/from16 v20, v3

    move/from16 v20, v3

    .line 184
    .line 185
    move-object v3, v9

    move-object v3, v9

    .line 186
    move-object/from16 v9, v24

    move-object/from16 v9, v24

    .line 187
    .line 188
    move/from16 v24, v12

    .line 189
    .line 190
    move/from16 v12, v25

    .line 191
    .line 192
    move/from16 v25, v4

    .line 193
    .line 194
    const/high16 v4, 0x42b40000    # 90.0f

    .line 195
    .line 196
    invoke-virtual/range {v9 .. v15}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 197
    .line 198
    .line 199
    invoke-virtual {v3, v9}, Landroid/graphics/Path;->addPath(Landroid/graphics/Path;)V

    .line 200
    .line 201
    .line 202
    iget-object v15, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->d:Landroid/graphics/Path;

    .line 203
    .line 204
    invoke-virtual {v15}, Landroid/graphics/Path;->rewind()V

    .line 205
    .line 206
    .line 207
    iget v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 208
    .line 209
    invoke-virtual {v15, v7, v9}, Landroid/graphics/Path;->moveTo(FF)V

    .line 210
    .line 211
    .line 212
    sub-float v9, v7, v5

    .line 213
    .line 214
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 215
    .line 216
    add-float v11, v7, v5

    .line 217
    .line 218
    iget v12, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 219
    .line 220
    invoke-virtual {v6, v9, v10, v11, v12}, Landroid/graphics/RectF;->set(FFFF)V

    .line 221
    .line 222
    .line 223
    const/high16 v10, -0x3ccc0000    # -180.0f

    .line 224
    .line 225
    const/4 v11, 0x1

    .line 226
    invoke-virtual {v15, v6, v4, v10, v11}, Landroid/graphics/Path;->arcTo(Landroid/graphics/RectF;FFZ)V

    .line 227
    .line 228
    .line 229
    sub-float v9, v9, v18

    .line 230
    .line 231
    iput v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 232
    .line 233
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 234
    .line 235
    iput v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 236
    .line 237
    sub-float v33, v7, v20

    .line 238
    .line 239
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 240
    .line 241
    sub-float v36, v10, v20

    .line 242
    .line 243
    move/from16 v37, v9

    move/from16 v37, v9

    .line 244
    .line 245
    move/from16 v35, v9

    .line 246
    .line 247
    move/from16 v38, v10

    .line 248
    .line 249
    move/from16 v34, v11

    .line 250
    .line 251
    move-object/from16 v32, v15

    .line 252
    .line 253
    invoke-virtual/range {v32 .. v38}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 254
    .line 255
    .line 256
    iget v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 257
    .line 258
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 259
    .line 260
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 261
    .line 262
    add-float v17, v11, v20

    .line 263
    .line 264
    move/from16 v21, v9

    move/from16 v21, v9

    .line 265
    .line 266
    move/from16 v20, v7

    .line 267
    .line 268
    move/from16 v19, v9

    .line 269
    .line 270
    move/from16 v16, v10

    .line 271
    .line 272
    move/from16 v18, v33

    .line 273
    .line 274
    invoke-virtual/range {v15 .. v21}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 275
    .line 276
    .line 277
    invoke-virtual {v3, v15}, Landroid/graphics/Path;->addPath(Landroid/graphics/Path;)V

    .line 278
    .line 279
    .line 280
    goto :goto_130

    .line 281
    :cond_127
    move/from16 v31, v3

    .line 282
    .line 283
    move/from16 v25, v4

    .line 284
    .line 285
    move-object v3, v9

    .line 286
    move/from16 v24, v12

    .line 287
    .line 288
    const/high16 v4, 0x42b40000    # 90.0f

    .line 289
    .line 290
    :goto_130
    cmpl-float v9, v25, v22

    .line 291
    .line 292
    const/high16 v22, 0x3f800000    # 1.0f

    .line 293
    .line 294
    if-lez v9, :cond_1da

    .line 295
    .line 296
    cmpg-float v9, v25, v22

    .line 297
    .line 298
    if-gez v9, :cond_1da

    .line 299
    .line 300
    iget v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 301
    .line 302
    cmpl-float v9, v9, v23

    .line 303
    .line 304
    if-nez v9, :cond_1da

    .line 305
    .line 306
    const v9, 0x3e4ccccd    # 0.2f

    .line 307
    .line 308
    .line 309
    sub-float v9, v25, v9

    .line 310
    .line 311
    const/high16 v10, 0x3fa00000    # 1.25f

    .line 312
    .line 313
    mul-float/2addr v9, v10

    .line 314
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 315
    .line 316
    invoke-virtual {v3, v14, v10}, Landroid/graphics/Path;->moveTo(FF)V

    .line 317
    .line 318
    .line 319
    sub-float v10, v14, v5

    .line 320
    .line 321
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 322
    .line 323
    add-float v12, v14, v5

    .line 324
    .line 325
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 326
    .line 327
    invoke-virtual {v6, v10, v11, v12, v13}, Landroid/graphics/RectF;->set(FFFF)V

    .line 328
    .line 329
    .line 330
    const/high16 v10, 0x43340000    # 180.0f

    .line 331
    .line 332
    const/4 v11, 0x1

    .line 333
    invoke-virtual {v3, v6, v4, v10, v11}, Landroid/graphics/Path;->arcTo(Landroid/graphics/RectF;FFZ)V

    .line 334
    .line 335
    .line 336
    div-int/lit8 v4, v24, 0x2

    .line 337
    .line 338
    int-to-float v4, v4

    .line 339
    add-float/2addr v12, v4

    .line 340
    iput v12, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 341
    .line 342
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 343
    .line 344
    mul-float v11, v9, v5

    .line 345
    .line 346
    sub-float/2addr v4, v11

    .line 347
    iput v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 348
    .line 349
    sub-float v16, v12, v11

    .line 350
    .line 351
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 352
    .line 353
    sub-float v9, v22, v9

    .line 354
    .line 355
    mul-float/2addr v9, v5

    .line 356
    sub-float v18, v12, v9

    .line 357
    .line 358
    move/from16 v21, v4

    .line 359
    .line 360
    move-object v15, v3

    .line 361
    move/from16 v19, v4

    move/from16 v19, v4

    .line 362
    .line 363
    move/from16 v20, v12

    .line 364
    .line 365
    move/from16 v17, v13

    .line 366
    .line 367
    invoke-virtual/range {v15 .. v21}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 368
    .line 369
    .line 370
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 371
    .line 372
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 373
    .line 374
    add-float v16, v9, v4

    .line 375
    .line 376
    iget v12, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 377
    .line 378
    add-float v18, v11, v4

    .line 379
    .line 380
    move/from16 v21, v3

    .line 381
    .line 382
    move/from16 v19, v3

    move/from16 v19, v3

    .line 383
    .line 384
    move/from16 v20, v7

    move/from16 v20, v7

    .line 385
    .line 386
    move/from16 v17, v12

    move/from16 v17, v12

    .line 387
    .line 388
    invoke-virtual/range {v15 .. v21}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 389
    .line 390
    .line 391
    sub-float v3, v7, v5

    .line 392
    .line 393
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 394
    .line 395
    add-float v12, v7, v5

    .line 396
    .line 397
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 398
    .line 399
    invoke-virtual {v6, v3, v4, v12, v13}, Landroid/graphics/RectF;->set(FFFF)V

    .line 400
    .line 401
    .line 402
    const/high16 v3, 0x43870000    # 270.0f

    .line 403
    .line 404
    const/4 v4, 0x1

    .line 405
    invoke-virtual {v15, v6, v3, v10, v4}, Landroid/graphics/Path;->arcTo(Landroid/graphics/RectF;FFZ)V

    .line 406
    .line 407
    .line 408
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 409
    .line 410
    add-float/2addr v3, v11

    .line 411
    iput v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 412
    .line 413
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 414
    .line 415
    add-float v16, v11, v4

    .line 416
    .line 417
    iget v10, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 418
    .line 419
    add-float v18, v9, v4

    .line 420
    .line 421
    move/from16 v21, v3

    .line 422
    .line 423
    move/from16 v19, v3

    .line 424
    .line 425
    move/from16 v20, v4

    .line 426
    .line 427
    move/from16 v17, v10

    .line 428
    .line 429
    invoke-virtual/range {v15 .. v21}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 430
    .line 431
    .line 432
    iget v13, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 433
    .line 434
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g:F

    .line 435
    .line 436
    sub-float v10, v3, v9

    .line 437
    .line 438
    move v9, v11

    .line 439
    iget v11, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->h:F

    .line 440
    .line 441
    sub-float v12, v3, v9

    .line 442
    .line 443
    move-object v3, v15

    .line 444
    move v15, v13

    move v15, v13

    .line 445
    move-object v9, v3

    .line 446
    invoke-virtual/range {v9 .. v15}, Landroid/graphics/Path;->cubicTo(FFFFFF)V

    .line 447
    .line 448
    .line 449
    move-object v15, v9

    .line 450
    goto :goto_1db

    .line 451
    :cond_1da
    move-object v15, v3

    .line 452
    :goto_1db
    cmpl-float v3, v25, v22

    .line 453
    .line 454
    if-nez v3, :cond_1f4

    .line 455
    .line 456
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 457
    .line 458
    cmpl-float v3, v3, v23

    .line 459
    .line 460
    if-nez v3, :cond_1f4

    .line 461
    .line 462
    sub-float v3, v14, v5

    .line 463
    .line 464
    iget v4, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 465
    .line 466
    add-float/2addr v7, v5

    .line 467
    iget v9, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 468
    .line 469
    invoke-virtual {v6, v3, v4, v7, v9}, Landroid/graphics/RectF;->set(FFFF)V

    .line 470
    .line 471
    .line 472
    sget-object v3, Landroid/graphics/Path$Direction;->CW:Landroid/graphics/Path$Direction;

    .line 473
    .line 474
    invoke-virtual {v15, v6, v5, v5, v3}, Landroid/graphics/Path;->addRoundRect(Landroid/graphics/RectF;FFLandroid/graphics/Path$Direction;)V

    .line 475
    .line 476
    .line 477
    :cond_1f4
    const v3, 0x3727c5ac    # 1.0E-5f

    .line 478
    .line 479
    .line 480
    cmpl-float v3, v8, v3

    .line 481
    .line 482
    if-lez v3, :cond_203

    .line 483
    .line 484
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 485
    .line 486
    mul-float/2addr v8, v5

    .line 487
    sget-object v4, Landroid/graphics/Path$Direction;->CW:Landroid/graphics/Path$Direction;

    .line 488
    .line 489
    invoke-virtual {v15, v14, v3, v8, v4}, Landroid/graphics/Path;->addCircle(FFFLandroid/graphics/Path$Direction;)V

    .line 490
    .line 491
    .line 492
    :cond_203
    invoke-virtual {v15, v2}, Landroid/graphics/Path;->addPath(Landroid/graphics/Path;)V

    .line 493
    .line 494
    .line 495
    invoke-virtual {v2, v15}, Landroid/graphics/Path;->addPath(Landroid/graphics/Path;)V

    .line 496
    .line 497
    .line 498
    add-int/lit8 v3, v31, 0x1

    .line 499
    .line 500
    goto/16 :goto_14

    .line 501
    .line 502
    :cond_20d
    move/from16 v23, v6

    .line 503
    .line 504
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 505
    .line 506
    cmpl-float v3, v3, v23

    .line 507
    .line 508
    if-eqz v3, :cond_21c

    .line 509
    .line 510
    invoke-direct {v0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getRetreatingJoinPath()Landroid/graphics/Path;

    .line 511
    .line 512
    .line 513
    move-result-object v3

    .line 514
    invoke-virtual {v2, v3}, Landroid/graphics/Path;->addPath(Landroid/graphics/Path;)V

    .line 515
    .line 516
    .line 517
    :cond_21c
    iget-object v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->F:Landroid/graphics/Paint;

    .line 518
    .line 519
    invoke-virtual {v1, v2, v3}, Landroid/graphics/Canvas;->drawPath(Landroid/graphics/Path;Landroid/graphics/Paint;)V

    .line 520
    .line 521
    .line 522
    iget v2, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 523
    .line 524
    iget v3, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 525
    .line 526
    iget-object v0, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->a:Landroid/graphics/Paint;

    .line 527
    .line 528
    invoke-virtual {v1, v2, v3, v5, v0}, Landroid/graphics/Canvas;->drawCircle(FFFLandroid/graphics/Paint;)V

    .line 529
    .line 530
    .line 531
    :cond_22a
    :goto_22a
    return-void
.end method

.method public final onMeasure(II)V
    .locals 6

    .line 1
    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getDesiredHeight()I

    .line 2
    .line 3
    .line 4
    move-result v0

    .line 5
    invoke-static {p2}, Landroid/view/View$MeasureSpec;->getMode(I)I

    .line 6
    .line 7
    .line 8
    move-result v1

    .line 9
    const/4 v5, 0x6

    const/high16 v2, 0x40000000    # 2.0f

    .line 10
    .line 11
    const/4 v5, 0x1

    const/high16 v3, -0x80000000

    .line 12
    .line 13
    const/4 v5, 0x1

    if-eq v1, v3, :cond_19

    .line 14
    .line 15
    if-eq v1, v2, :cond_14

    .line 16
    .line 17
    goto :goto_23

    .line 18
    :cond_14
    invoke-static {p2}, Landroid/view/View$MeasureSpec;->getSize(I)I

    .line 19
    .line 20
    .line 21
    move-result v0

    .line 22
    goto :goto_23

    .line 23
    :cond_19
    const/4 v5, 0x4

    invoke-static {p2}, Landroid/view/View$MeasureSpec;->getSize(I)I

    .line 24
    .line 25
    .line 26
    move-result p2

    .line 27
    const/4 v5, 0x3

    invoke-static {v0, p2}, Ljava/lang/Math;->min(II)I

    .line 28
    .line 29
    .line 30
    move-result v0

    .line 31
    :goto_23
    const/4 v5, 0x4

    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getDesiredWidth()I

    .line 32
    .line 33
    .line 34
    move-result p2

    .line 35
    const/4 v5, 0x5

    invoke-static {p1}, Landroid/view/View$MeasureSpec;->getMode(I)I

    .line 36
    .line 37
    .line 38
    move-result v1

    .line 39
    if-eq v1, v3, :cond_38

    .line 40
    .line 41
    if-eq v1, v2, :cond_32

    .line 42
    .line 43
    goto :goto_40

    .line 44
    :cond_32
    invoke-static {p1}, Landroid/view/View$MeasureSpec;->getSize(I)I

    .line 45
    .line 46
    .line 47
    move-result p2

    .line 48
    const/4 v5, 0x4

    goto :goto_40

    .line 49
    :cond_38
    invoke-static {p1}, Landroid/view/View$MeasureSpec;->getSize(I)I

    .line 50
    .line 51
    .line 52
    move-result p1

    .line 53
    invoke-static {p2, p1}, Ljava/lang/Math;->min(II)I

    .line 54
    .line 55
    .line 56
    move-result p2

    .line 57
    :goto_40
    const/4 v5, 0x3

    invoke-virtual {p0, p2, v0}, Landroid/view/View;->setMeasuredDimension(II)V

    .line 58
    .line 59
    .line 60
    invoke-virtual {p0}, Landroid/view/View;->getPaddingLeft()I

    .line 61
    .line 62
    .line 63
    move-result p1

    .line 64
    const/4 v5, 0x3

    invoke-virtual {p0}, Landroid/view/View;->getPaddingTop()I

    .line 65
    .line 66
    .line 67
    move-result v0

    .line 68
    const/4 v5, 0x5

    invoke-virtual {p0}, Landroid/view/View;->getPaddingRight()I

    .line 69
    .line 70
    .line 71
    move-result v1

    .line 72
    const/4 v5, 0x3

    sub-int/2addr p2, v1

    .line 73
    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getRequiredWidth()I

    .line 74
    .line 75
    .line 76
    move-result v1

    .line 77
    const/4 v5, 0x4

    sub-int/2addr p2, p1

    .line 78
    sub-int/2addr p2, v1

    .line 79
    div-int/lit8 p2, p2, 0x2

    .line 80
    .line 81
    add-int/2addr p2, p1

    .line 82
    int-to-float p1, p2

    .line 83
    iget p2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->m:F

    .line 84
    .line 85
    const/4 v5, 0x4

    add-float/2addr p1, p2

    .line 86
    iget v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 87
    .line 88
    new-array v1, v1, [F

    .line 89
    .line 90
    iput-object v1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 91
    .line 92
    const/4 v5, 0x2

    const/4 v1, 0x0

    .line 93
    :goto_6b
    iget v2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->t:I

    .line 94
    .line 95
    iget v3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->i:I

    .line 96
    .line 97
    if-ge v1, v2, :cond_80

    .line 98
    .line 99
    iget-object v2, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 100
    .line 101
    iget v4, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->j:I

    .line 102
    .line 103
    add-int/2addr v3, v4

    .line 104
    mul-int/2addr v3, v1

    .line 105
    int-to-float v3, v3

    .line 106
    const/4 v5, 0x5

    add-float/2addr v3, p1

    .line 107
    aput v3, v2, v1

    .line 108
    .line 109
    const/4 v5, 0x5

    add-int/lit8 v1, v1, 0x1

    .line 110
    .line 111
    goto :goto_6b

    .line 112
    :cond_80
    int-to-float p1, v0

    .line 113
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->p:F

    .line 114
    .line 115
    add-float/2addr p1, p2

    .line 116
    const/4 v5, 0x5

    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->q:F

    .line 117
    .line 118
    add-int/2addr v0, v3

    .line 119
    const/4 v5, 0x5

    int-to-float p1, v0

    .line 120
    const/4 v5, 0x7

    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->r:F

    .line 121
    .line 122
    const/4 v5, 0x0

    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g()V

    .line 123
    .line 124
    .line 125
    const/4 v5, 0x7

    return-void
.end method

.method public final onRestoreInstanceState(Landroid/os/Parcelable;)V
    .locals 2

    .line 1
    check-cast p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;

    .line 2
    .line 3
    const/4 v1, 0x4

    invoke-virtual {p1}, Landroid/view/AbsSavedState;->getSuperState()Landroid/os/Parcelable;

    .line 4
    .line 5
    .line 6
    move-result-object v0

    .line 7
    const/4 v1, 0x1

    invoke-super {p0, v0}, Landroid/view/View;->onRestoreInstanceState(Landroid/os/Parcelable;)V

    .line 8
    .line 9
    .line 10
    iget p1, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;->a:I

    .line 11
    .line 12
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 13
    .line 14
    invoke-virtual {p0}, Landroid/view/View;->requestLayout()V

    .line 15
    .line 16
    .line 17
    const/4 v1, 0x3

    return-void
.end method

.method public final onSaveInstanceState()Landroid/os/Parcelable;
    .locals 3

    .line 1
    invoke-super {p0}, Landroid/view/View;->onSaveInstanceState()Landroid/os/Parcelable;

    .line 2
    .line 3
    .line 4
    move-result-object v0

    .line 5
    new-instance v1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;

    .line 6
    .line 7
    invoke-direct {v1, v0}, Landroid/view/View$BaseSavedState;-><init>(Landroid/os/Parcelable;)V

    .line 8
    .line 9
    .line 10
    const/4 v2, 0x5

    iget p0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->u:I

    .line 11
    .line 12
    iput p0, v1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;->a:I

    .line 13
    .line 14
    return-object v1
.end method

.method public final onViewAttachedToWindow(Landroid/view/View;)V
    .locals 1

    .line 1
    const/4 p1, 0x1

    .line 2
    iput-boolean p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->D:Z

    .line 3
    .line 4
    return-void
.end method

.method public final onViewDetachedFromWindow(Landroid/view/View;)V
    .locals 1

    .line 1
    const/4 v0, 0x4

    const/4 p1, 0x0

    .line 2
    iput-boolean p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->D:Z

    .line 3
    .line 4
    const/4 v0, 0x5

    return-void
.end method

.method public setPageIndicatorColor(I)V
    .locals 2

    .line 1
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->l:I

    .line 2
    .line 3
    new-instance p1, Landroid/graphics/Paint;

    .line 4
    .line 5
    const/4 v0, 0x1

    .line 6
    invoke-direct {p1, v0}, Landroid/graphics/Paint;-><init>(I)V

    .line 7
    .line 8
    .line 9
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->F:Landroid/graphics/Paint;

    .line 10
    .line 11
    const/4 v1, 0x0

    iget p0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->l:I

    .line 12
    .line 13
    invoke-virtual {p1, p0}, Landroid/graphics/Paint;->setColor(I)V

    .line 14
    .line 15
    .line 16
    return-void
.end method

.method public setViewPager(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;)V
    .locals 3

    .line 1
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->s:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 2
    .line 3
    iget-object v0, p1, Landroidx/viewpager/widget/ViewPager;->R:Ljava/util/ArrayList;

    .line 4
    .line 5
    if-nez v0, :cond_d

    .line 6
    .line 7
    new-instance v0, Ljava/util/ArrayList;

    .line 8
    .line 9
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 10
    .line 11
    .line 12
    iput-object v0, p1, Landroidx/viewpager/widget/ViewPager;->R:Ljava/util/ArrayList;

    .line 13
    .line 14
    :cond_d
    const/4 v2, 0x5

    invoke-interface {v0, p0}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 15
    .line 16
    .line 17
    invoke-direct {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->getCount()I

    .line 18
    .line 19
    .line 20
    move-result v0

    .line 21
    invoke-direct {p0, v0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->setPageCount(I)V

    .line 22
    .line 23
    .line 24
    invoke-virtual {p1}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->getAdapter()Lcre;

    .line 25
    .line 26
    .line 27
    move-result-object p1

    .line 28
    new-instance v0, Loe3;

    .line 29
    .line 30
    const/4 v1, 0x1

    .line 31
    invoke-direct {v0, p0, v1}, Loe3;-><init>(Ljava/lang/Object;I)V

    .line 32
    .line 33
    .line 34
    iget-object p1, p1, Lnfb;->a:Landroid/database/DataSetObservable;

    .line 35
    .line 36
    invoke-virtual {p1, v0}, Landroid/database/Observable;->registerObserver(Ljava/lang/Object;)V

    .line 37
    .line 38
    .line 39
    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->g()V

    .line 40
    .line 41
    .line 42
    const/4 v2, 0x4

    return-void
.end method
