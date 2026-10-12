.class public Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;
.super Landroidx/viewpager/widget/ViewPager;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;
    }
.end annotation


# instance fields
.field public i0:F

.field public j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

.field public final k0:Ljava/util/ArrayList;


# direct methods
.method public constructor <init>(Landroid/content/Context;Landroid/util/AttributeSet;)V
    .locals 1

    .line 1
    invoke-direct {p0, p1, p2}, Landroidx/viewpager/widget/ViewPager;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;)V

    .line 2
    .line 3
    .line 4
    new-instance p1, Ljava/util/ArrayList;

    .line 5
    .line 6
    invoke-direct {p1}, Ljava/util/ArrayList;-><init>()V

    .line 7
    .line 8
    .line 9
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->k0:Ljava/util/ArrayList;

    .line 10
    .line 11
    sget-object p1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->all:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 12
    .line 13
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 14
    .line 15
    return-void
.end method


# virtual methods
.method public getAdapter()Lcre;
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    invoke-super {p0}, Landroidx/viewpager/widget/ViewPager;->getAdapter()Lnfb;

    .line 2
    .line 3
    .line 4
    move-result-object p0

    .line 5
    check-cast p0, Lcre;

    .line 6
    .line 7
    return-object p0
.end method

.method public bridge synthetic getAdapter()Lnfb;
    .locals 1

    .line 8
    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->getAdapter()Lcre;

    move-result-object p0

    return-object p0
.end method

.method public getPreviousItem()I
    .locals 1

    .line 1
    invoke-virtual {p0}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 2
    .line 3
    .line 4
    move-result p0

    .line 5
    add-int/lit8 p0, p0, -0x1

    .line 6
    .line 7
    return p0
.end method

.method public final onInterceptTouchEvent(Landroid/view/MotionEvent;)Z
    .locals 2

    .line 1
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->x(Landroid/view/MotionEvent;)Z

    .line 2
    .line 3
    .line 4
    move-result v0

    .line 5
    if-eqz v0, :cond_c

    .line 6
    .line 7
    const/4 v1, 0x7

    invoke-super {p0, p1}, Landroidx/viewpager/widget/ViewPager;->onInterceptTouchEvent(Landroid/view/MotionEvent;)Z

    .line 8
    .line 9
    .line 10
    move-result p0

    .line 11
    return p0

    .line 12
    :cond_c
    const/4 p0, 0x0

    .line 13
    return p0
.end method

.method public final onTouchEvent(Landroid/view/MotionEvent;)Z
    .locals 5

    .line 1
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->k0:Ljava/util/ArrayList;

    .line 2
    .line 3
    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    .line 4
    .line 5
    .line 6
    move-result-object v0

    .line 7
    :goto_6
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    .line 8
    .line 9
    .line 10
    move-result v1

    .line 11
    const/4 v4, 0x2

    if-eqz v1, :cond_3f

    .line 12
    .line 13
    const/4 v4, 0x0

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 14
    .line 15
    .line 16
    move-result-object v1

    .line 17
    const/4 v4, 0x4

    check-cast v1, Lap7;

    .line 18
    .line 19
    check-cast v1, Lwgf;

    .line 20
    .line 21
    iget-object v2, v1, Lwgf;->b:Lcre;

    .line 22
    .line 23
    const/4 v4, 0x3

    iget-object v1, v1, Lwgf;->a:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 24
    .line 25
    invoke-virtual {v1}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 26
    .line 27
    .line 28
    move-result v3

    .line 29
    invoke-virtual {v2, v3}, Lcre;->m(I)Lxpe;

    .line 30
    .line 31
    .line 32
    move-result-object v2

    .line 33
    const/4 v4, 0x0

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 34
    .line 35
    .line 36
    iget-object v3, v2, Lxpe;->h:[Ljava/lang/String;

    .line 37
    .line 38
    const/4 v4, 0x3

    invoke-virtual {v2, v3}, Lxpe;->q([Ljava/lang/String;)Z

    .line 39
    .line 40
    .line 41
    move-result v2

    .line 42
    if-eqz v2, :cond_38

    .line 43
    .line 44
    const/4 v4, 0x0

    sget-object v2, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->left:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 45
    .line 46
    invoke-virtual {v1, v2}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->setAllowedSwipeDirection(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;)V

    .line 47
    .line 48
    .line 49
    goto :goto_6

    .line 50
    :cond_38
    sget-object v2, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->all:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 51
    .line 52
    const/4 v4, 0x0

    invoke-virtual {v1, v2}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->setAllowedSwipeDirection(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;)V

    .line 53
    .line 54
    .line 55
    goto :goto_6

    .line 56
    :cond_3f
    invoke-virtual {p0, p1}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->x(Landroid/view/MotionEvent;)Z

    .line 57
    .line 58
    .line 59
    move-result v0

    .line 60
    const/4 v4, 0x6

    if-eqz v0, :cond_4b

    .line 61
    .line 62
    invoke-super {p0, p1}, Landroidx/viewpager/widget/ViewPager;->onTouchEvent(Landroid/view/MotionEvent;)Z

    .line 63
    .line 64
    .line 65
    move-result p0

    .line 66
    return p0

    .line 67
    :cond_4b
    const/4 p0, 0x0

    move v4, p0

    .line 68
    return p0
.end method

.method public setAllowedSwipeDirection(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;)V
    .locals 1

    .line 1
    iput-object p1, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 2
    .line 3
    return-void
.end method

.method public final x(Landroid/view/MotionEvent;)Z
    .locals 6

    .line 1
    const/4 v5, 0x0

    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 2
    .line 3
    sget-object v1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->all:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 4
    .line 5
    const/4 v5, 0x1

    const/4 v2, 0x1

    .line 6
    if-ne v0, v1, :cond_a

    .line 7
    .line 8
    return v2

    .line 9
    :cond_a
    const/4 v5, 0x1

    sget-object v1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->none:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 10
    .line 11
    const/4 v3, 0x2

    const/4 v3, 0x0

    .line 12
    if-ne v0, v1, :cond_13

    .line 13
    .line 14
    const/4 v5, 0x0

    return v3

    .line 15
    :cond_13
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getAction()I

    .line 16
    .line 17
    .line 18
    move-result v0

    .line 19
    if-nez v0, :cond_21

    .line 20
    .line 21
    const/4 v5, 0x5

    invoke-virtual {p1}, Landroid/view/MotionEvent;->getX()F

    .line 22
    .line 23
    .line 24
    move-result p1

    .line 25
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->i0:F

    .line 26
    .line 27
    return v2

    .line 28
    :cond_21
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getAction()I

    .line 29
    .line 30
    .line 31
    move-result v0

    .line 32
    const/4 v5, 0x2

    const/4 v1, 0x2

    .line 33
    if-ne v0, v1, :cond_53

    .line 34
    .line 35
    :try_start_29
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getX()F

    .line 36
    .line 37
    .line 38
    move-result p1

    .line 39
    iget v0, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->i0:F

    .line 40
    .line 41
    const/4 v5, 0x0

    sub-float/2addr p1, v0

    .line 42
    const/4 v5, 0x0

    const/4 v0, 0x0

    .line 43
    cmpl-float v1, p1, v0

    .line 44
    .line 45
    const/4 v5, 0x2

    if-lez v1, :cond_43

    .line 46
    .line 47
    iget-object v1, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 48
    .line 49
    sget-object v4, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->right:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 50
    .line 51
    const/4 v5, 0x0

    if-ne v1, v4, :cond_43

    .line 52
    .line 53
    const/4 v5, 0x4

    return v3

    .line 54
    :catch_41
    move-exception p0

    .line 55
    goto :goto_50

    .line 56
    :cond_43
    cmpg-float p1, p1, v0

    .line 57
    .line 58
    if-gez p1, :cond_53

    .line 59
    .line 60
    iget-object p0, p0, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->j0:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 61
    .line 62
    const/4 v5, 0x2

    sget-object p1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->left:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;
    :try_end_4c
    .catch Ljava/lang/Exception; {:try_start_29 .. :try_end_4c} :catch_41

    .line 63
    .line 64
    if-ne p0, p1, :cond_53

    .line 65
    .line 66
    const/4 v5, 0x4

    return v3

    .line 67
    :goto_50
    invoke-virtual {p0}, Ljava/lang/Throwable;->printStackTrace()V

    .line 68
    .line 69
    .line 70
    :cond_53
    const/4 v5, 0x2

    return v2
.end method
