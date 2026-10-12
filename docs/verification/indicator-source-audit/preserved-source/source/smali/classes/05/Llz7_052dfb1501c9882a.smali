.class public final Llz7;
.super Landroid/animation/AnimatorListenerAdapter;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public final synthetic a:[I

.field public final synthetic b:F

.field public final synthetic c:F

.field public final synthetic d:Lmz7;


# direct methods
.method public constructor <init>(Lmz7;[IFF)V
    .locals 1

    .line 1
    const/4 v0, 0x7

    iput-object p1, p0, Llz7;->d:Lmz7;

    .line 2
    .line 3
    iput-object p2, p0, Llz7;->a:[I

    .line 4
    .line 5
    const/4 v0, 0x6

    iput p3, p0, Llz7;->b:F

    .line 6
    .line 7
    iput p4, p0, Llz7;->c:F

    .line 8
    .line 9
    invoke-direct {p0}, Landroid/animation/AnimatorListenerAdapter;-><init>()V

    .line 10
    .line 11
    .line 12
    return-void
.end method


# virtual methods
.method public final onAnimationEnd(Landroid/animation/Animator;)V
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget-object p0, p0, Llz7;->d:Lmz7;

    .line 2
    .line 3
    const/4 v0, 0x3

    iget-object p0, p0, Lmz7;->c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 4
    .line 5
    const/high16 p1, -0x40800000    # -1.0f

    .line 6
    .line 7
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 8
    .line 9
    const/4 v0, 0x3

    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 10
    .line 11
    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 12
    .line 13
    const/4 v0, 0x5

    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 14
    .line 15
    .line 16
    return-void
.end method

.method public final onAnimationStart(Landroid/animation/Animator;)V
    .locals 7

    .line 1
    iget-object p1, p0, Llz7;->d:Lmz7;

    .line 2
    .line 3
    const/4 v6, 0x4

    iget-object p1, p1, Lmz7;->c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 4
    .line 5
    iget-object v0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->z:[F

    .line 6
    .line 7
    const/4 v6, 0x4

    const/4 v1, 0x0

    .line 8
    invoke-static {v0, v1}, Ljava/util/Arrays;->fill([FF)V

    .line 9
    .line 10
    .line 11
    sget-object v0, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 12
    .line 13
    invoke-virtual {p1}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 14
    .line 15
    .line 16
    iget-object v0, p0, Llz7;->a:[I

    .line 17
    .line 18
    array-length v1, v0

    .line 19
    const/4 v2, 0x0

    .line 20
    :goto_15
    if-ge v2, v1, :cond_30

    .line 21
    .line 22
    const/4 v6, 0x7

    aget v3, v0, v2

    .line 23
    .line 24
    iget-object v4, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->C:[F

    .line 25
    .line 26
    const/4 v6, 0x6

    array-length v5, v4

    .line 27
    const/4 v6, 0x2

    if-ge v3, v5, :cond_26

    .line 28
    .line 29
    const v5, 0x3727c5ac    # 1.0E-5f

    .line 30
    .line 31
    .line 32
    aput v5, v4, v3

    .line 33
    .line 34
    :cond_26
    const/4 v6, 0x1

    sget-object v3, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 35
    .line 36
    invoke-virtual {p1}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 37
    .line 38
    .line 39
    add-int/lit8 v2, v2, 0x1

    .line 40
    .line 41
    const/4 v6, 0x5

    goto :goto_15

    .line 42
    :cond_30
    const/4 v6, 0x5

    iget v0, p0, Llz7;->b:F

    .line 43
    .line 44
    iput v0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 45
    .line 46
    const/4 v6, 0x0

    iget p0, p0, Llz7;->c:F

    .line 47
    .line 48
    iput p0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 49
    .line 50
    sget-object p0, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 51
    .line 52
    invoke-virtual {p1}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 53
    .line 54
    .line 55
    return-void
.end method
