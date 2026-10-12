.class public final Lv6;
.super Landroid/animation/AnimatorListenerAdapter;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public final synthetic a:I

.field public final synthetic b:Ljava/lang/Object;


# direct methods
.method public synthetic constructor <init>(Ljava/lang/Object;I)V
    .locals 1

    .line 1
    iput p2, p0, Lv6;->a:I

    .line 2
    .line 3
    iput-object p1, p0, Lv6;->b:Ljava/lang/Object;

    .line 4
    .line 5
    const/4 v0, 0x2

    invoke-direct {p0}, Landroid/animation/AnimatorListenerAdapter;-><init>()V

    .line 6
    .line 7
    .line 8
    const/4 v0, 0x6

    return-void
.end method


# virtual methods
.method public onAnimationCancel(Landroid/animation/Animator;)V
    .locals 5

    .line 1
    const-string v4, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget v0, p0, Lv6;->a:I

    .line 2
    .line 3
    const/4 v4, 0x7

    const/high16 v1, 0x3f800000    # 1.0f

    .line 4
    .line 5
    const/4 v4, 0x0

    const/4 v2, 0x0

    .line 6
    const/4 v4, 0x0

    iget-object v3, p0, Lv6;->b:Ljava/lang/Object;

    .line 7
    .line 8
    sparse-switch v0, :sswitch_data_5c

    .line 9
    .line 10
    .line 11
    const/4 v4, 0x3

    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationCancel(Landroid/animation/Animator;)V

    .line 12
    .line 13
    .line 14
    return-void

    .line 15
    :sswitch_14
    const/4 v4, 0x2

    check-cast v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;

    .line 16
    .line 17
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->k:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;

    .line 18
    .line 19
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;->setInnerCircleRadiusProgress(F)V

    .line 20
    .line 21
    .line 22
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->k:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;

    .line 23
    .line 24
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;->setOuterCircleRadiusProgress(F)V

    .line 25
    .line 26
    .line 27
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->j:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/DotsView;

    .line 28
    .line 29
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/DotsView;->setCurrentProgress(F)V

    .line 30
    .line 31
    .line 32
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->l:Landroid/widget/ImageView;

    .line 33
    .line 34
    invoke-virtual {p0, v1}, Landroid/view/View;->setScaleX(F)V

    .line 35
    .line 36
    .line 37
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->l:Landroid/widget/ImageView;

    .line 38
    .line 39
    const/4 v4, 0x0

    invoke-virtual {p0, v1}, Landroid/view/View;->setScaleY(F)V

    .line 40
    .line 41
    .line 42
    return-void

    .line 43
    :sswitch_32
    check-cast v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;

    .line 44
    .line 45
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->k:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;

    .line 46
    .line 47
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;->setInnerCircleRadiusProgress(F)V

    .line 48
    .line 49
    .line 50
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->k:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;

    .line 51
    .line 52
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/CircleView;->setOuterCircleRadiusProgress(F)V

    .line 53
    .line 54
    .line 55
    const/4 v4, 0x1

    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->j:Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/DotsView;

    .line 56
    .line 57
    invoke-virtual {p0, v2}, Lcom/arlosoft/macrodroid/widget/sparkbutton/helpers/DotsView;->setCurrentProgress(F)V

    .line 58
    .line 59
    .line 60
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->l:Landroid/widget/ImageView;

    .line 61
    .line 62
    invoke-virtual {p0, v1}, Landroid/view/View;->setScaleX(F)V

    .line 63
    .line 64
    .line 65
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->l:Landroid/widget/ImageView;

    .line 66
    .line 67
    invoke-virtual {p0, v1}, Landroid/view/View;->setScaleY(F)V

    .line 68
    .line 69
    .line 70
    return-void

    .line 71
    :sswitch_4f
    const/4 v4, 0x6

    check-cast v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;

    .line 72
    .line 73
    const/4 p0, 0x0

    .line 74
    const/4 v4, 0x4

    iput-object p0, v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;->w:Landroid/view/ViewPropertyAnimator;

    .line 75
    .line 76
    const/4 p0, 0x6

    const/4 p0, 0x0

    .line 77
    iput-boolean p0, v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;->j:Z

    .line 78
    .line 79
    return-void

    .line 80
    nop

    .line 81
    :sswitch_data_5c
    .sparse-switch
        0x0 -> :sswitch_4f
        0x4 -> :sswitch_32
        0x5 -> :sswitch_14
    .end sparse-switch
.end method

.method public final onAnimationEnd(Landroid/animation/Animator;)V
    .locals 5

    .line 1
    iget v0, p0, Lv6;->a:I

    .line 2
    .line 3
    const/4 v1, 0x0

    const/4 v1, 0x0

    .line 4
    const/4 v2, 0x0

    .line 5
    iget-object v3, p0, Lv6;->b:Ljava/lang/Object;

    .line 6
    .line 7
    const/4 v4, 0x4

    packed-switch v0, :pswitch_data_ac

    .line 8
    .line 9
    .line 10
    check-cast v3, Landroidx/transition/Transition;

    .line 11
    .line 12
    const/4 v4, 0x4

    invoke-virtual {v3}, Landroidx/transition/Transition;->q()V

    .line 13
    .line 14
    .line 15
    invoke-virtual {p1, p0}, Landroid/animation/Animator;->removeListener(Landroid/animation/Animator$AnimatorListener;)V

    .line 16
    .line 17
    .line 18
    const/4 v4, 0x2

    return-void

    .line 19
    :pswitch_16
    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationEnd(Landroid/animation/Animator;)V

    .line 20
    .line 21
    .line 22
    check-cast v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;

    .line 23
    .line 24
    const/4 v4, 0x3

    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton2;->q:Lwwe;

    .line 25
    .line 26
    if-eqz p0, :cond_23

    .line 27
    .line 28
    invoke-interface {p0}, Lwwe;->o()V

    .line 29
    .line 30
    .line 31
    :cond_23
    return-void

    .line 32
    :pswitch_24
    const/4 v4, 0x5

    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationEnd(Landroid/animation/Animator;)V

    .line 33
    .line 34
    .line 35
    const/4 v4, 0x2

    check-cast v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;

    .line 36
    .line 37
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/sparkbutton/SparkButton;->q:Lwwe;

    .line 38
    .line 39
    const/4 v4, 0x0

    if-eqz p0, :cond_33

    .line 40
    .line 41
    invoke-interface {p0}, Lwwe;->o()V

    .line 42
    .line 43
    .line 44
    :cond_33
    return-void

    .line 45
    :pswitch_34
    check-cast v3, Lnz7;

    .line 46
    .line 47
    iget-object p0, v3, Lnz7;->d:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 48
    .line 49
    iget p1, v3, Lnz7;->c:I

    .line 50
    .line 51
    sget v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->K:I

    .line 52
    .line 53
    const/4 v4, 0x1

    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->C:[F

    .line 54
    .line 55
    array-length v1, v0

    .line 56
    const/4 v4, 0x0

    if-ge p1, v1, :cond_47

    .line 57
    .line 58
    const/4 v1, 0x0

    .line 59
    const/4 v4, 0x7

    aput v1, v0, p1

    .line 60
    .line 61
    :cond_47
    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 62
    .line 63
    const/4 v4, 0x1

    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 64
    .line 65
    .line 66
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 67
    .line 68
    .line 69
    const/4 v4, 0x7

    return-void

    .line 70
    :pswitch_52
    check-cast v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;

    .line 71
    .line 72
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->e:Lzt2;

    .line 73
    .line 74
    iget-boolean p1, p0, Lzt2;->g:Z

    .line 75
    .line 76
    if-nez p1, :cond_5c

    .line 77
    .line 78
    const/4 v4, 0x0

    goto :goto_81

    .line 79
    :cond_5c
    iput-object v2, p0, Lzt2;->k:Ljava/lang/Object;

    .line 80
    .line 81
    const/4 v4, 0x4

    invoke-virtual {p0}, Lzt2;->f()V

    .line 82
    .line 83
    .line 84
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->i:Landroid/graphics/drawable/Drawable;

    .line 85
    .line 86
    const/16 p1, 0xff

    .line 87
    .line 88
    if-eqz p0, :cond_6c

    .line 89
    .line 90
    const/4 v4, 0x1

    invoke-virtual {p0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 91
    .line 92
    .line 93
    :cond_6c
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->j:Landroid/graphics/drawable/Drawable;

    .line 94
    .line 95
    invoke-virtual {p0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 96
    .line 97
    .line 98
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->c:Landroid/animation/LayoutTransition;

    .line 99
    .line 100
    if-eqz p0, :cond_81

    .line 101
    .line 102
    invoke-virtual {v3}, Landroid/view/ViewGroup;->getLayoutTransition()Landroid/animation/LayoutTransition;

    .line 103
    .line 104
    .line 105
    move-result-object p0

    .line 106
    if-nez p0, :cond_81

    .line 107
    .line 108
    iget-object p0, v3, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->c:Landroid/animation/LayoutTransition;

    .line 109
    .line 110
    const/4 v4, 0x1

    invoke-virtual {v3, p0}, Landroid/view/ViewGroup;->setLayoutTransition(Landroid/animation/LayoutTransition;)V

    .line 111
    .line 112
    .line 113
    :cond_81
    :goto_81
    const/4 v4, 0x7

    return-void

    .line 114
    :pswitch_83
    new-instance p0, Ljava/util/ArrayList;

    .line 115
    .line 116
    check-cast v3, Lz50;

    .line 117
    .line 118
    iget-object p1, v3, Lz50;->e:Ljava/util/ArrayList;

    .line 119
    .line 120
    const/4 v4, 0x1

    invoke-direct {p0, p1}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 121
    .line 122
    .line 123
    invoke-virtual {p0}, Ljava/util/ArrayList;->size()I

    .line 124
    .line 125
    .line 126
    move-result p1

    .line 127
    :goto_91
    if-ge v1, p1, :cond_a2

    .line 128
    .line 129
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    .line 130
    .line 131
    .line 132
    move-result-object v0

    .line 133
    const/4 v4, 0x5

    check-cast v0, Lj40;

    .line 134
    .line 135
    const/4 v4, 0x2

    invoke-virtual {v0, v3}, Lj40;->b(Landroid/graphics/drawable/Drawable;)V

    .line 136
    .line 137
    .line 138
    add-int/lit8 v1, v1, 0x1

    .line 139
    .line 140
    const/4 v4, 0x7

    goto :goto_91

    .line 141
    :cond_a2
    return-void

    .line 142
    :pswitch_a3
    check-cast v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;

    .line 143
    .line 144
    iput-object v2, v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;->w:Landroid/view/ViewPropertyAnimator;

    .line 145
    .line 146
    const/4 v4, 0x2

    iput-boolean v1, v3, Landroidx/appcompat/widget/ActionBarOverlayLayout;->j:Z

    .line 147
    .line 148
    const/4 v4, 0x3

    return-void

    .line 149
    :pswitch_data_ac
    .packed-switch 0x0
        :pswitch_a3
        :pswitch_83
        :pswitch_52
        :pswitch_34
        :pswitch_24
        :pswitch_16
    .end packed-switch
.end method

.method public onAnimationStart(Landroid/animation/Animator;)V
    .locals 4

    .line 1
    iget v0, p0, Lv6;->a:I

    .line 2
    .line 3
    const/4 v1, 0x0

    .line 4
    const/4 v3, 0x0

    iget-object v2, p0, Lv6;->b:Ljava/lang/Object;

    .line 5
    .line 6
    const/4 v3, 0x2

    packed-switch v0, :pswitch_data_40

    .line 7
    .line 8
    .line 9
    :pswitch_a
    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationStart(Landroid/animation/Animator;)V

    .line 10
    .line 11
    .line 12
    return-void

    .line 13
    :pswitch_e
    const/4 v3, 0x2

    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationEnd(Landroid/animation/Animator;)V

    .line 14
    .line 15
    .line 16
    const/4 v3, 0x4

    return-void

    .line 17
    :pswitch_14
    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationEnd(Landroid/animation/Animator;)V

    .line 18
    .line 19
    .line 20
    return-void

    .line 21
    :pswitch_18
    check-cast v2, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;

    .line 22
    .line 23
    iget-object p0, v2, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->e:Lzt2;

    .line 24
    .line 25
    const/4 v3, 0x5

    iput-boolean v1, p0, Lzt2;->h:Z

    .line 26
    .line 27
    return-void

    .line 28
    :pswitch_20
    new-instance p0, Ljava/util/ArrayList;

    .line 29
    .line 30
    const/4 v3, 0x5

    check-cast v2, Lz50;

    .line 31
    .line 32
    iget-object p1, v2, Lz50;->e:Ljava/util/ArrayList;

    .line 33
    .line 34
    invoke-direct {p0, p1}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    .line 35
    .line 36
    .line 37
    const/4 v3, 0x4

    invoke-virtual {p0}, Ljava/util/ArrayList;->size()I

    .line 38
    .line 39
    .line 40
    move-result p1

    .line 41
    :goto_2f
    if-ge v1, p1, :cond_3e

    .line 42
    .line 43
    invoke-virtual {p0, v1}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    .line 44
    .line 45
    .line 46
    move-result-object v0

    .line 47
    const/4 v3, 0x4

    check-cast v0, Lj40;

    .line 48
    .line 49
    invoke-virtual {v0, v2}, Lj40;->c(Landroid/graphics/drawable/Drawable;)V

    .line 50
    .line 51
    .line 52
    add-int/lit8 v1, v1, 0x1

    .line 53
    .line 54
    goto :goto_2f

    .line 55
    :cond_3e
    return-void

    .line 56
    nop

    .line 57
    :pswitch_data_40
    .packed-switch 0x1
        :pswitch_20
        :pswitch_18
        :pswitch_a
        :pswitch_14
        :pswitch_e
    .end packed-switch
.end method
