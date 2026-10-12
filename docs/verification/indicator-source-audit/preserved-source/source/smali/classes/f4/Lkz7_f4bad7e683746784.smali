.class public final Lkz7;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Landroid/animation/ValueAnimator$AnimatorUpdateListener;


# instance fields
.field public final synthetic a:I

.field public final synthetic b:Lmz7;


# direct methods
.method public synthetic constructor <init>(Lmz7;I)V
    .locals 1

    .line 1
    iput p2, p0, Lkz7;->a:I

    .line 2
    .line 3
    iput-object p1, p0, Lkz7;->b:Lmz7;

    .line 4
    .line 5
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 6
    .line 7
    .line 8
    return-void
.end method


# virtual methods
.method public final onAnimationUpdate(Landroid/animation/ValueAnimator;)V
    .locals 5

    .line 1
    const-string v4, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget v0, p0, Lkz7;->a:I

    .line 2
    .line 3
    const/4 v4, 0x1

    const/4 v1, 0x0

    .line 4
    iget-object p0, p0, Lkz7;->b:Lmz7;

    .line 5
    .line 6
    packed-switch v0, :pswitch_data_58

    .line 7
    .line 8
    .line 9
    iget-object p0, p0, Lmz7;->c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 10
    .line 11
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 12
    .line 13
    .line 14
    move-result-object p1

    .line 15
    const/4 v4, 0x1

    check-cast p1, Ljava/lang/Float;

    .line 16
    .line 17
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 18
    .line 19
    .line 20
    move-result p1

    .line 21
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 22
    .line 23
    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 24
    .line 25
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 26
    .line 27
    .line 28
    iget-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->J:[Lnz7;

    .line 29
    .line 30
    array-length v0, p1

    .line 31
    :goto_22
    if-ge v1, v0, :cond_2e

    .line 32
    .line 33
    aget-object v2, p1, v1

    .line 34
    .line 35
    iget v3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->B:F

    .line 36
    .line 37
    invoke-virtual {v2, v3}, Loz7;->b(F)V

    .line 38
    .line 39
    .line 40
    add-int/lit8 v1, v1, 0x1

    .line 41
    .line 42
    goto :goto_22

    .line 43
    :cond_2e
    return-void

    .line 44
    :pswitch_2f
    iget-object p0, p0, Lmz7;->c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 45
    .line 46
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 47
    .line 48
    .line 49
    move-result-object p1

    .line 50
    const/4 v4, 0x4

    check-cast p1, Ljava/lang/Float;

    .line 51
    .line 52
    const/4 v4, 0x4

    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 53
    .line 54
    .line 55
    move-result p1

    .line 56
    const/4 v4, 0x3

    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 57
    .line 58
    const/4 v4, 0x0

    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 59
    .line 60
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 61
    .line 62
    .line 63
    const/4 v4, 0x4

    iget-object p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->J:[Lnz7;

    .line 64
    .line 65
    array-length v0, p1

    .line 66
    :goto_4a
    if-ge v1, v0, :cond_56

    .line 67
    .line 68
    aget-object v2, p1, v1

    .line 69
    .line 70
    iget v3, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->A:F

    .line 71
    .line 72
    invoke-virtual {v2, v3}, Loz7;->b(F)V

    .line 73
    .line 74
    .line 75
    add-int/lit8 v1, v1, 0x1

    .line 76
    .line 77
    goto :goto_4a

    .line 78
    :cond_56
    const/4 v4, 0x4

    return-void

    .line 79
    :pswitch_data_58
    .packed-switch 0x0
        :pswitch_2f
    .end packed-switch
.end method
