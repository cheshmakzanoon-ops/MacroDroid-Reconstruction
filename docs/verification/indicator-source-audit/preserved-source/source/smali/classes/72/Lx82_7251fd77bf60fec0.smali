.class public final Lx82;
.super Ljava/lang/Object;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Landroid/animation/ValueAnimator$AnimatorUpdateListener;


# instance fields
.field public final synthetic a:I

.field public final synthetic b:Ljava/lang/Object;


# direct methods
.method public synthetic constructor <init>(Ljava/lang/Object;I)V
    .locals 1

    .line 1
    iput p2, p0, Lx82;->a:I

    .line 2
    .line 3
    const/4 v0, 0x7

    iput-object p1, p0, Lx82;->b:Ljava/lang/Object;

    .line 4
    .line 5
    const/4 v0, 0x0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 6
    .line 7
    .line 8
    return-void
.end method


# virtual methods
.method public final onAnimationUpdate(Landroid/animation/ValueAnimator;)V
    .locals 6

    .line 1
    const-string v5, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget v0, p0, Lx82;->a:I

    .line 2
    .line 3
    const/high16 v1, 0x3f800000    # 1.0f

    .line 4
    .line 5
    const/high16 v2, 0x437f0000    # 255.0f

    .line 6
    .line 7
    iget-object p0, p0, Lx82;->b:Ljava/lang/Object;

    .line 8
    .line 9
    packed-switch v0, :pswitch_data_114

    .line 10
    .line 11
    .line 12
    check-cast p0, Ltfd;

    .line 13
    .line 14
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 15
    .line 16
    .line 17
    move-result-object p1

    .line 18
    check-cast p1, Ljava/lang/Float;

    .line 19
    .line 20
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 21
    .line 22
    .line 23
    move-result p1

    .line 24
    const/4 v5, 0x5

    iput p1, p0, Ltfd;->h:F

    .line 25
    .line 26
    iget-object p0, p0, Ltfd;->e:Lcom/hanks/htextview/scale/ScaleTextView;

    .line 27
    .line 28
    invoke-virtual {p0}, Landroid/view/View;->invalidate()V

    .line 29
    .line 30
    .line 31
    const/4 v5, 0x5

    return-void

    .line 32
    :pswitch_23
    check-cast p0, Lv88;

    .line 33
    .line 34
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedFraction()F

    .line 35
    .line 36
    .line 37
    move-result p1

    .line 38
    iput p1, p0, Lv88;->m:F

    .line 39
    .line 40
    return-void

    .line 41
    :pswitch_2c
    check-cast p0, Lnz7;

    .line 42
    .line 43
    iget-object v0, p0, Lnz7;->d:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 44
    .line 45
    iget p0, p0, Lnz7;->c:I

    .line 46
    .line 47
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 48
    .line 49
    .line 50
    move-result-object p1

    .line 51
    const/4 v5, 0x1

    check-cast p1, Ljava/lang/Float;

    .line 52
    .line 53
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 54
    .line 55
    .line 56
    move-result p1

    .line 57
    sget v1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->K:I

    .line 58
    .line 59
    iget-object v1, v0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->C:[F

    .line 60
    .line 61
    array-length v2, v1

    .line 62
    if-ge p0, v2, :cond_46

    .line 63
    .line 64
    aput p1, v1, p0

    .line 65
    .line 66
    :cond_46
    sget-object p0, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 67
    .line 68
    invoke-virtual {v0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 69
    .line 70
    .line 71
    return-void

    .line 72
    :pswitch_4c
    check-cast p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 73
    .line 74
    const/4 v5, 0x0

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 75
    .line 76
    .line 77
    move-result-object p1

    .line 78
    check-cast p1, Ljava/lang/Float;

    .line 79
    .line 80
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 81
    .line 82
    .line 83
    move-result p1

    .line 84
    iput p1, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->w:F

    .line 85
    .line 86
    iget-object v0, p0, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->I:Lmz7;

    .line 87
    .line 88
    const/4 v5, 0x5

    invoke-virtual {v0, p1}, Loz7;->b(F)V

    .line 89
    .line 90
    .line 91
    const/4 v5, 0x1

    sget-object p1, Ln3h;->a:Ljava/util/WeakHashMap;

    .line 92
    .line 93
    invoke-virtual {p0}, Landroid/view/View;->postInvalidateOnAnimation()V

    .line 94
    .line 95
    .line 96
    const/4 v5, 0x4

    return-void

    .line 97
    :pswitch_69
    const/4 v5, 0x4

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 98
    .line 99
    .line 100
    move-result-object p1

    .line 101
    check-cast p1, Ljava/lang/Float;

    .line 102
    .line 103
    const/4 v5, 0x4

    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 104
    .line 105
    .line 106
    move-result p1

    .line 107
    const/4 v5, 0x4

    mul-float/2addr p1, v2

    .line 108
    float-to-int p1, p1

    .line 109
    check-cast p0, Lzs5;

    .line 110
    .line 111
    const/4 v5, 0x6

    iget-object v0, p0, Lzs5;->c:Landroid/graphics/drawable/StateListDrawable;

    .line 112
    .line 113
    invoke-virtual {v0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 114
    .line 115
    .line 116
    iget-object v0, p0, Lzs5;->d:Landroid/graphics/drawable/Drawable;

    .line 117
    .line 118
    invoke-virtual {v0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 119
    .line 120
    .line 121
    const/4 v5, 0x7

    iget-object p0, p0, Lzs5;->s:Landroidx/recyclerview/widget/RecyclerView;

    .line 122
    .line 123
    invoke-virtual {p0}, Landroid/view/View;->invalidate()V

    .line 124
    .line 125
    .line 126
    return-void

    .line 127
    :pswitch_8c
    check-cast p0, Lcom/arlosoft/macrodroid/uicomponent/ExpandableLayout;

    .line 128
    .line 129
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 130
    .line 131
    .line 132
    move-result-object p1

    .line 133
    const/4 v5, 0x2

    check-cast p1, Ljava/lang/Float;

    .line 134
    .line 135
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 136
    .line 137
    .line 138
    move-result p1

    .line 139
    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/uicomponent/ExpandableLayout;->setExpansion(F)V

    .line 140
    .line 141
    .line 142
    const/4 v5, 0x0

    return-void

    .line 143
    :pswitch_9e
    check-cast p0, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;

    .line 144
    .line 145
    iget-object v0, p0, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->e:Lzt2;

    .line 146
    .line 147
    iget-boolean v3, v0, Lzt2;->g:Z

    .line 148
    .line 149
    if-nez v3, :cond_a7

    .line 150
    .line 151
    goto :goto_e2

    .line 152
    :cond_a7
    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 153
    .line 154
    .line 155
    move-result-object v3

    .line 156
    const/4 v5, 0x6

    check-cast v3, Ljava/lang/Float;

    .line 157
    .line 158
    const/4 v5, 0x1

    invoke-virtual {v3}, Ljava/lang/Float;->intValue()I

    .line 159
    .line 160
    .line 161
    move-result v3

    .line 162
    const/4 v5, 0x4

    iput v3, v0, Lzt2;->e:I

    .line 163
    .line 164
    iget v3, v0, Lzt2;->c:I

    .line 165
    .line 166
    const/4 v5, 0x2

    iget-object v4, v0, Lzt2;->i:Ljava/lang/Object;

    .line 167
    .line 168
    check-cast v4, Landroid/view/View;

    .line 169
    .line 170
    const/4 v5, 0x6

    invoke-virtual {v4}, Landroid/view/View;->getTop()I

    .line 171
    .line 172
    .line 173
    move-result v4

    .line 174
    const/4 v5, 0x4

    sub-int/2addr v3, v4

    .line 175
    iget v4, v0, Lzt2;->e:I

    .line 176
    .line 177
    add-int/2addr v3, v4

    .line 178
    iput v3, v0, Lzt2;->f:I

    .line 179
    .line 180
    const/4 v5, 0x4

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedFraction()F

    .line 181
    .line 182
    .line 183
    move-result p1

    .line 184
    sub-float/2addr v1, p1

    .line 185
    mul-float/2addr v1, v2

    .line 186
    float-to-int p1, v1

    .line 187
    iget-object v0, p0, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->i:Landroid/graphics/drawable/Drawable;

    .line 188
    .line 189
    const/4 v5, 0x1

    if-eqz v0, :cond_d9

    .line 190
    .line 191
    invoke-virtual {v0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 192
    .line 193
    .line 194
    :cond_d9
    iget-object v0, p0, Lcom/arlosoft/macrodroid/widget/DragLinearLayout;->j:Landroid/graphics/drawable/Drawable;

    .line 195
    .line 196
    invoke-virtual {v0, p1}, Landroid/graphics/drawable/Drawable;->setAlpha(I)V

    .line 197
    .line 198
    .line 199
    const/4 v5, 0x6

    invoke-virtual {p0}, Landroid/view/View;->invalidate()V

    .line 200
    .line 201
    .line 202
    :goto_e2
    return-void

    .line 203
    :pswitch_e3
    check-cast p0, Lxi3;

    .line 204
    .line 205
    iget-boolean v0, p0, Lxi3;->i:Z

    .line 206
    .line 207
    if-eqz v0, :cond_f1

    .line 208
    .line 209
    const/4 v5, 0x6

    iget-object p0, p0, Lxi3;->c:Landroid/animation/ValueAnimator;

    .line 210
    .line 211
    invoke-virtual {p0}, Landroid/animation/ValueAnimator;->cancel()V

    .line 212
    .line 213
    .line 214
    const/4 v5, 0x7

    goto :goto_10b

    .line 215
    :cond_f1
    const/4 v5, 0x2

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    .line 216
    .line 217
    .line 218
    move-result-object p1

    .line 219
    const/4 v5, 0x7

    check-cast p1, Ljava/lang/Float;

    .line 220
    .line 221
    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    .line 222
    .line 223
    .line 224
    move-result p1

    .line 225
    sub-float/2addr v1, p1

    .line 226
    iput v1, p0, Lxi3;->h:F

    .line 227
    .line 228
    iget-boolean p1, p0, Lxi3;->i:Z

    .line 229
    .line 230
    if-eqz p1, :cond_106

    .line 231
    .line 232
    const/4 v5, 0x6

    goto :goto_10b

    .line 233
    :cond_106
    iget-object p0, p0, Lxi3;->b:Lorg/osmdroid/views/MapView;

    .line 234
    .line 235
    invoke-virtual {p0}, Landroid/view/View;->postInvalidate()V

    .line 236
    .line 237
    .line 238
    :goto_10b
    return-void

    .line 239
    :pswitch_10c
    check-cast p0, Lcom/github/mikephil/charting/charts/Chart;

    .line 240
    .line 241
    const/4 v5, 0x7

    invoke-virtual {p0}, Landroid/view/View;->postInvalidate()V

    .line 242
    .line 243
    .line 244
    const/4 v5, 0x5

    return-void

    .line 245
    :pswitch_data_114
    .packed-switch 0x0
        :pswitch_10c
        :pswitch_e3
        :pswitch_9e
        :pswitch_8c
        :pswitch_69
        :pswitch_4c
        :pswitch_2c
        :pswitch_23
    .end packed-switch
.end method
