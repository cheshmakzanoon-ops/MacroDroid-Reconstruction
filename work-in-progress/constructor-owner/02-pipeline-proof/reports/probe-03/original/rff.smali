.class public abstract Lrff;
.super Lo73;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Lvn6;


# instance fields
.field private final arity:I


# direct methods
.method public constructor <init>(ILm73;)V
    .locals 1

    .line 1
    invoke-direct {p0, p2}, Lo73;-><init>(Lm73;)V

    .line 2
    .line 3
    .line 4
    iput p1, p0, Lrff;->arity:I

    .line 5
    .line 6
    return-void
.end method


# virtual methods
.method public getArity()I
    .locals 1

    .line 1
    const-string v0, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget p0, p0, Lrff;->arity:I

    .line 2
    .line 3
    return p0
.end method

.method public toString()Ljava/lang/String;
    .locals 2

    .line 1
    invoke-virtual {p0}, Lt11;->getCompletion()Lm73;

    .line 2
    .line 3
    .line 4
    move-result-object v0

    .line 5
    const/4 v1, 0x3

    if-nez v0, :cond_f

    .line 6
    .line 7
    sget-object v0, Lkpc;->a:Llpc;

    .line 8
    .line 9
    invoke-virtual {v0, p0}, Llpc;->h(Lvn6;)Ljava/lang/String;

    .line 10
    .line 11
    .line 12
    move-result-object p0

    .line 13
    const/4 v1, 0x3

    return-object p0

    .line 14
    :cond_f
    invoke-super {p0}, Lt11;->toString()Ljava/lang/String;

    .line 15
    .line 16
    .line 17
    move-result-object p0

    .line 18
    const/4 v1, 0x3

    return-object p0
.end method
