.class public final Lnz7;
.super Loz7;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public final c:I

.field public final synthetic d:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;


# direct methods
.method public constructor <init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;ILjz7;)V
    .locals 1

    .line 1
    iput-object p1, p0, Lnz7;->d:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 2
    .line 3
    const/4 v0, 0x2

    invoke-direct {p0, p3}, Loz7;-><init>(Ljz7;)V

    .line 4
    .line 5
    .line 6
    const/4 p3, 0x2

    .line 7
    const/4 v0, 0x6

    new-array p3, p3, [F

    .line 8
    .line 9
    fill-array-data p3, :array_34

    .line 10
    .line 11
    .line 12
    invoke-virtual {p0, p3}, Landroid/animation/ValueAnimator;->setFloatValues([F)V

    .line 13
    .line 14
    .line 15
    const/4 v0, 0x2

    iput p2, p0, Lnz7;->c:I

    .line 16
    .line 17
    iget-wide p2, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->o:J

    .line 18
    .line 19
    const/4 v0, 0x2

    invoke-virtual {p0, p2, p3}, Landroid/animation/ValueAnimator;->setDuration(J)Landroid/animation/ValueAnimator;

    .line 20
    .line 21
    .line 22
    const/4 v0, 0x4

    iget-object p1, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f:Los5;

    .line 23
    .line 24
    invoke-virtual {p0, p1}, Landroid/animation/Animator;->setInterpolator(Landroid/animation/TimeInterpolator;)V

    .line 25
    .line 26
    .line 27
    new-instance p1, Lx82;

    .line 28
    .line 29
    const/4 p2, 0x6

    .line 30
    invoke-direct {p1, p0, p2}, Lx82;-><init>(Ljava/lang/Object;I)V

    .line 31
    .line 32
    .line 33
    invoke-virtual {p0, p1}, Landroid/animation/ValueAnimator;->addUpdateListener(Landroid/animation/ValueAnimator$AnimatorUpdateListener;)V

    .line 34
    .line 35
    .line 36
    new-instance p1, Lv6;

    .line 37
    .line 38
    const/4 v0, 0x4

    const/4 p2, 0x3

    .line 39
    invoke-direct {p1, p0, p2}, Lv6;-><init>(Ljava/lang/Object;I)V

    .line 40
    .line 41
    .line 42
    const/4 v0, 0x0

    invoke-virtual {p0, p1}, Landroid/animation/Animator;->addListener(Landroid/animation/Animator$AnimatorListener;)V

    .line 43
    .line 44
    .line 45
    return-void

    .line 46
    .line 47
    :array_34
    .array-data 4
        0x3727c5ac    # 1.0E-5f
        0x3f800000    # 1.0f
    .end array-data
.end method
