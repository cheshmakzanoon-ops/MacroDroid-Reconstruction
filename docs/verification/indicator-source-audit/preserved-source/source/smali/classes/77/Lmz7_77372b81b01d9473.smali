.class public final Lmz7;
.super Loz7;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# instance fields
.field public final synthetic c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;


# direct methods
.method public constructor <init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;IIILjz7;)V
    .locals 10

    .line 1
    iput-object p1, p0, Lmz7;->c:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 2
    .line 3
    const/4 v9, 0x5

    invoke-direct {p0, p5}, Loz7;-><init>(Ljz7;)V

    .line 4
    .line 5
    .line 6
    iget-wide v0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->o:J

    .line 7
    .line 8
    const/4 v9, 0x1

    iget p5, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->m:F

    .line 9
    .line 10
    invoke-virtual {p0, v0, v1}, Landroid/animation/ValueAnimator;->setDuration(J)Landroid/animation/ValueAnimator;

    .line 11
    .line 12
    .line 13
    iget-object v0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->f:Los5;

    .line 14
    .line 15
    invoke-virtual {p0, v0}, Landroid/animation/Animator;->setInterpolator(Landroid/animation/TimeInterpolator;)V

    .line 16
    .line 17
    .line 18
    iget-object v0, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 19
    .line 20
    if-le p3, p2, :cond_22

    .line 21
    .line 22
    aget v0, v0, p2

    .line 23
    .line 24
    iget v1, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 25
    .line 26
    invoke-static {v0, v1}, Ljava/lang/Math;->min(FF)F

    .line 27
    .line 28
    .line 29
    move-result v0

    .line 30
    :goto_1f
    const/4 v9, 0x3

    sub-float/2addr v0, p5

    .line 31
    goto :goto_25

    .line 32
    :cond_22
    aget v0, v0, p3

    .line 33
    .line 34
    goto :goto_1f

    .line 35
    :goto_25
    iget-object v1, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 36
    .line 37
    if-le p3, p2, :cond_2f

    .line 38
    .line 39
    aget v2, v1, p3

    .line 40
    .line 41
    :goto_2b
    const/4 v9, 0x7

    sub-float/2addr v2, p5

    .line 42
    const/4 v9, 0x7

    goto :goto_32

    .line 43
    :cond_2f
    aget v2, v1, p3

    .line 44
    .line 45
    goto :goto_2b

    .line 46
    :goto_32
    if-le p3, p2, :cond_3a

    .line 47
    .line 48
    aget v1, v1, p3

    .line 49
    .line 50
    :goto_36
    const/4 v9, 0x3

    add-float/2addr v1, p5

    .line 51
    const/4 v9, 0x3

    goto :goto_44

    .line 52
    :cond_3a
    aget v1, v1, p2

    .line 53
    .line 54
    iget v3, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 55
    .line 56
    invoke-static {v1, v3}, Ljava/lang/Math;->max(FF)F

    .line 57
    .line 58
    .line 59
    move-result v1

    .line 60
    const/4 v9, 0x7

    goto :goto_36

    .line 61
    :goto_44
    iget-object v3, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 62
    .line 63
    if-le p3, p2, :cond_4d

    .line 64
    .line 65
    aget p3, v3, p3

    .line 66
    .line 67
    :goto_4a
    const/4 v9, 0x1

    add-float/2addr p3, p5

    .line 68
    goto :goto_50

    .line 69
    :cond_4d
    aget p3, v3, p3

    .line 70
    .line 71
    goto :goto_4a

    .line 72
    :goto_50
    const/4 v9, 0x3

    new-array p5, p4, [Lnz7;

    .line 73
    .line 74
    iput-object p5, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->J:[Lnz7;

    .line 75
    .line 76
    new-array p5, p4, [I

    .line 77
    .line 78
    cmpl-float v3, v0, v2

    .line 79
    .line 80
    const/4 v4, 0x2

    move v9, v4

    .line 81
    const/4 v5, 0x5

    const/4 v5, 0x1

    .line 82
    const/4 v9, 0x3

    const/4 v6, 0x0

    .line 83
    const/4 v9, 0x7

    if-eqz v3, :cond_96

    .line 84
    .line 85
    new-array p3, v4, [F

    .line 86
    .line 87
    aput v0, p3, v6

    .line 88
    .line 89
    aput v2, p3, v5

    .line 90
    .line 91
    invoke-virtual {p0, p3}, Landroid/animation/ValueAnimator;->setFloatValues([F)V

    .line 92
    .line 93
    .line 94
    move p3, v6

    .line 95
    :goto_6c
    if-ge p3, p4, :cond_8a

    .line 96
    .line 97
    iget-object v2, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->J:[Lnz7;

    .line 98
    .line 99
    new-instance v3, Lnz7;

    .line 100
    .line 101
    const/4 v9, 0x4

    add-int v4, p2, p3

    .line 102
    .line 103
    new-instance v7, Ljz7;

    .line 104
    .line 105
    iget-object v8, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 106
    .line 107
    aget v8, v8, v4

    .line 108
    .line 109
    const/4 v9, 0x1

    invoke-direct {v7, v8, v5}, Ljz7;-><init>(FI)V

    .line 110
    .line 111
    .line 112
    invoke-direct {v3, p1, v4, v7}, Lnz7;-><init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;ILjz7;)V

    .line 113
    .line 114
    .line 115
    aput-object v3, v2, p3

    .line 116
    .line 117
    aput v4, p5, p3

    .line 118
    .line 119
    const/4 v9, 0x2

    add-int/lit8 p3, p3, 0x1

    .line 120
    .line 121
    goto :goto_6c

    .line 122
    :cond_8a
    new-instance p1, Lkz7;

    .line 123
    .line 124
    const/4 v9, 0x0

    invoke-direct {p1, p0, v6}, Lkz7;-><init>(Lmz7;I)V

    .line 125
    .line 126
    .line 127
    const/4 v9, 0x3

    invoke-virtual {p0, p1}, Landroid/animation/ValueAnimator;->addUpdateListener(Landroid/animation/ValueAnimator$AnimatorUpdateListener;)V

    .line 128
    .line 129
    .line 130
    const/4 v9, 0x0

    goto :goto_cd

    .line 131
    :cond_96
    new-array v2, v4, [F

    .line 132
    .line 133
    aput v1, v2, v6

    .line 134
    .line 135
    const/4 v9, 0x2

    aput p3, v2, v5

    .line 136
    .line 137
    const/4 v9, 0x7

    invoke-virtual {p0, v2}, Landroid/animation/ValueAnimator;->setFloatValues([F)V

    .line 138
    .line 139
    .line 140
    const/4 v9, 0x5

    move p3, v6

    .line 141
    :goto_a3
    if-ge p3, p4, :cond_c4

    .line 142
    .line 143
    const/4 v9, 0x3

    iget-object v2, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->J:[Lnz7;

    .line 144
    .line 145
    new-instance v3, Lnz7;

    .line 146
    .line 147
    const/4 v9, 0x2

    sub-int v4, p2, p3

    .line 148
    .line 149
    const/4 v9, 0x1

    new-instance v7, Ljz7;

    .line 150
    .line 151
    iget-object v8, p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->y:[F

    .line 152
    .line 153
    aget v8, v8, v4

    .line 154
    .line 155
    invoke-direct {v7, v8, v6}, Ljz7;-><init>(FI)V

    .line 156
    .line 157
    .line 158
    invoke-direct {v3, p1, v4, v7}, Lnz7;-><init>(Lagency/tango/materialintroscreen/widgets/InkPageIndicator;ILjz7;)V

    .line 159
    .line 160
    .line 161
    const/4 v9, 0x3

    aput-object v3, v2, p3

    .line 162
    .line 163
    const/4 v9, 0x4

    aput v4, p5, p3

    .line 164
    .line 165
    add-int/lit8 p3, p3, 0x1

    .line 166
    .line 167
    const/4 v9, 0x7

    goto :goto_a3

    .line 168
    :cond_c4
    new-instance p1, Lkz7;

    .line 169
    .line 170
    const/4 v9, 0x6

    invoke-direct {p1, p0, v5}, Lkz7;-><init>(Lmz7;I)V

    .line 171
    .line 172
    .line 173
    invoke-virtual {p0, p1}, Landroid/animation/ValueAnimator;->addUpdateListener(Landroid/animation/ValueAnimator$AnimatorUpdateListener;)V

    .line 174
    .line 175
    .line 176
    :goto_cd
    new-instance p1, Llz7;

    .line 177
    .line 178
    invoke-direct {p1, p0, p5, v0, v1}, Llz7;-><init>(Lmz7;[IFF)V

    .line 179
    .line 180
    .line 181
    const/4 v9, 0x7

    invoke-virtual {p0, p1}, Landroid/animation/Animator;->addListener(Landroid/animation/Animator$AnimatorListener;)V

    .line 182
    .line 183
    .line 184
    return-void
.end method
