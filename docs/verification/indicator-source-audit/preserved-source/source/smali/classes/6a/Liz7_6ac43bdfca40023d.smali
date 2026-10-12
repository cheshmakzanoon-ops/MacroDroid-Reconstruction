.class public final Liz7;
.super Landroid/animation/AnimatorListenerAdapter;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public final synthetic a:I

.field public final synthetic b:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;


# direct methods
.method public synthetic constructor <init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;I)V
    .locals 1

    .line 1
    const/4 v0, 0x5

    iput p2, p0, Liz7;->a:I

    .line 2
    .line 3
    iput-object p1, p0, Liz7;->b:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 4
    .line 5
    invoke-direct {p0}, Landroid/animation/AnimatorListenerAdapter;-><init>()V

    .line 6
    .line 7
    .line 8
    return-void
.end method


# virtual methods
.method public final onAnimationEnd(Landroid/animation/Animator;)V
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget p1, p0, Liz7;->a:I

    .line 2
    .line 3
    iget-object p0, p0, Liz7;->b:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 4
    .line 5
    packed-switch p1, :pswitch_data_18

    .line 6
    .line 7
    .line 8
    const/4 p1, 0x1

    .line 9
    iput-boolean p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->x:Z

    .line 10
    .line 11
    const/4 v0, 0x3

    return-void

    .line 12
    :pswitch_e
    sget p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->K:I

    .line 13
    .line 14
    invoke-virtual {p0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f()V

    .line 15
    .line 16
    .line 17
    const/4 v0, 0x7

    const/4 p1, 0x0

    .line 18
    iput-boolean p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->E:Z

    .line 19
    .line 20
    return-void

    .line 21
    :pswitch_data_18
    .packed-switch 0x0
        :pswitch_e
    .end packed-switch
.end method

.method public onAnimationStart(Landroid/animation/Animator;)V
    .locals 2

    .line 1
    iget v0, p0, Liz7;->a:I

    .line 2
    .line 3
    packed-switch v0, :pswitch_data_10

    .line 4
    .line 5
    .line 6
    invoke-super {p0, p1}, Landroid/animation/AnimatorListenerAdapter;->onAnimationStart(Landroid/animation/Animator;)V

    .line 7
    .line 8
    .line 9
    return-void

    .line 10
    :pswitch_9
    iget-object p0, p0, Liz7;->b:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 11
    .line 12
    const/4 p1, 0x0

    .line 13
    iput-boolean p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->x:Z

    .line 14
    .line 15
    const/4 v1, 0x2

    return-void

    .line 16
    .line 17
    :pswitch_data_10
    .packed-switch 0x1
        :pswitch_9
    .end packed-switch
.end method
