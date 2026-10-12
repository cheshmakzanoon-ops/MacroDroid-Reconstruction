.class public abstract Loz7;
.super Landroid/animation/ValueAnimator;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public a:Z

.field public final b:Ljz7;


# direct methods
.method public constructor <init>(Ljz7;)V
    .locals 1

    .line 1
    invoke-direct {p0}, Landroid/animation/ValueAnimator;-><init>()V

    .line 2
    .line 3
    .line 4
    iput-object p1, p0, Loz7;->b:Ljz7;

    .line 5
    .line 6
    const/4 v0, 0x6

    const/4 p1, 0x0

    .line 7
    const/4 v0, 0x1

    iput-boolean p1, p0, Loz7;->a:Z

    .line 8
    .line 9
    return-void
.end method


# virtual methods
.method public final b(F)V
    .locals 5

    .line 1
    const-string v4, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget-boolean v0, p0, Loz7;->a:Z

    .line 2
    .line 3
    if-nez v0, :cond_27

    .line 4
    .line 5
    iget-object v0, p0, Loz7;->b:Ljz7;

    .line 6
    .line 7
    iget v1, v0, Ljz7;->b:I

    .line 8
    .line 9
    const/4 v2, 0x0

    .line 10
    const/4 v3, 0x1

    .line 11
    packed-switch v1, :pswitch_data_28

    .line 12
    .line 13
    .line 14
    const/4 v4, 0x0

    iget v0, v0, Ljz7;->a:F

    .line 15
    .line 16
    cmpl-float p1, p1, v0

    .line 17
    .line 18
    if-lez p1, :cond_20

    .line 19
    .line 20
    :goto_16
    move v2, v3

    .line 21
    goto :goto_20

    .line 22
    :pswitch_18
    iget v0, v0, Ljz7;->a:F

    .line 23
    .line 24
    cmpg-float p1, p1, v0

    .line 25
    .line 26
    if-gez p1, :cond_20

    .line 27
    .line 28
    const/4 v4, 0x4

    goto :goto_16

    .line 29
    :cond_20
    :goto_20
    if-eqz v2, :cond_27

    .line 30
    .line 31
    invoke-virtual {p0}, Landroid/animation/Animator;->start()V

    .line 32
    .line 33
    .line 34
    iput-boolean v3, p0, Loz7;->a:Z

    .line 35
    .line 36
    :cond_27
    return-void

    .line 37
    :pswitch_data_28
    .packed-switch 0x0
        :pswitch_18
    .end packed-switch
.end method
