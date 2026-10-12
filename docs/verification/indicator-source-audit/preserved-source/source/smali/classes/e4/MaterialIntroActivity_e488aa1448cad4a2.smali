.class public abstract Lagency/tango/materialintroscreen/MaterialIntroActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"


# static fields
.field public static final synthetic A:I


# instance fields
.field public j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

.field public k:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

.field public l:Lcre;

.field public m:Landroid/widget/ImageButton;

.field public n:Landroid/widget/ImageButton;

.field public o:Landroid/widget/ImageButton;

.field public p:Landroidx/coordinatorlayout/widget/CoordinatorLayout;

.field public q:Landroid/widget/Button;

.field public r:Landroid/widget/LinearLayout;

.field public final s:Landroid/animation/ArgbEvaluator;

.field public t:Lmra;

.field public u:Lmra;

.field public v:Lmra;

.field public w:Lm7a;

.field public x:Lzk2;

.field public y:Lt6;

.field public final z:Landroid/util/SparseArray;


# direct methods
.method public constructor <init>()V
    .locals 2

    .line 1
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 2
    .line 3
    .line 4
    new-instance v0, Landroid/animation/ArgbEvaluator;

    .line 5
    .line 6
    const/4 v1, 0x3

    invoke-direct {v0}, Landroid/animation/ArgbEvaluator;-><init>()V

    .line 7
    .line 8
    .line 9
    iput-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->s:Landroid/animation/ArgbEvaluator;

    .line 10
    .line 11
    new-instance v0, Landroid/util/SparseArray;

    .line 12
    .line 13
    invoke-direct {v0}, Landroid/util/SparseArray;-><init>()V

    .line 14
    .line 15
    .line 16
    const/4 v1, 0x4

    iput-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->z:Landroid/util/SparseArray;

    .line 17
    .line 18
    return-void
.end method


# virtual methods
.method public final M0(Lxpe;)V
    .locals 3

    .line 1
    const-string v2, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    iget-object p0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 2
    .line 3
    iget-object v0, p0, Lcre;->i:Ljava/util/ArrayList;

    .line 4
    .line 5
    invoke-virtual {p0}, Lcre;->n()I

    .line 6
    .line 7
    .line 8
    move-result v1

    .line 9
    invoke-virtual {v0, v1, p1}, Ljava/util/ArrayList;->add(ILjava/lang/Object;)V

    .line 10
    .line 11
    .line 12
    monitor-enter p0

    .line 13
    :try_start_e
    const/4 v2, 0x7

    iget-object p1, p0, Lnfb;->b:Landroid/database/DataSetObserver;

    .line 14
    .line 15
    const/4 v2, 0x0

    if-eqz p1, :cond_1a

    .line 16
    .line 17
    invoke-virtual {p1}, Landroid/database/DataSetObserver;->onChanged()V

    .line 18
    .line 19
    .line 20
    goto :goto_1a

    .line 21
    :catchall_18
    move-exception p1

    .line 22
    goto :goto_21

    .line 23
    :cond_1a
    :goto_1a
    monitor-exit p0
    :try_end_1b
    .catchall {:try_start_e .. :try_end_1b} :catchall_18

    .line 24
    iget-object p0, p0, Lnfb;->a:Landroid/database/DataSetObservable;

    .line 25
    .line 26
    invoke-virtual {p0}, Landroid/database/DataSetObservable;->notifyChanged()V

    .line 27
    .line 28
    .line 29
    return-void

    .line 30
    :goto_21
    :try_start_21
    monitor-exit p0
    :try_end_22
    .catchall {:try_start_21 .. :try_end_22} :catchall_18

    .line 31
    throw p1
.end method

.method public final N0(ILxpe;)V
    .locals 3

    .line 1
    iget-object v0, p2, Lxpe;->h:[Ljava/lang/String;

    .line 2
    .line 3
    invoke-virtual {p2, v0}, Lxpe;->q([Ljava/lang/String;)Z

    .line 4
    .line 5
    .line 6
    move-result v0

    .line 7
    if-eqz v0, :cond_1d

    .line 8
    .line 9
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 10
    .line 11
    sget p2, Lagency/tango/materialintroscreen/R$drawable;->ic_next:I

    .line 12
    .line 13
    const/4 v2, 0x3

    invoke-static {p0, p2}, Lw63;->getDrawable(Landroid/content/Context;I)Landroid/graphics/drawable/Drawable;

    .line 14
    .line 15
    .line 16
    move-result-object p2

    .line 17
    invoke-virtual {p1, p2}, Landroid/widget/ImageView;->setImageDrawable(Landroid/graphics/drawable/Drawable;)V

    .line 18
    .line 19
    .line 20
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 21
    .line 22
    iget-object p0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->x:Lzk2;

    .line 23
    .line 24
    invoke-virtual {p1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 25
    .line 26
    .line 27
    const/4 v2, 0x3

    return-void

    .line 28
    :cond_1d
    const/4 v2, 0x1

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 29
    .line 30
    invoke-virtual {v0}, Lcre;->n()I

    .line 31
    .line 32
    .line 33
    move-result v0

    .line 34
    const/4 v1, 0x1

    .line 35
    const/4 v2, 0x4

    sub-int/2addr v0, v1

    .line 36
    if-ne p1, v0, :cond_2b

    .line 37
    .line 38
    const/4 v2, 0x7

    goto :goto_2d

    .line 39
    :cond_2b
    const/4 v2, 0x2

    const/4 v1, 0x0

    .line 40
    :goto_2d
    const/4 v2, 0x6

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 41
    .line 42
    if-eqz v1, :cond_45

    .line 43
    .line 44
    sget p1, Lagency/tango/materialintroscreen/R$drawable;->ic_finish:I

    .line 45
    .line 46
    invoke-static {p0, p1}, Lw63;->getDrawable(Landroid/content/Context;I)Landroid/graphics/drawable/Drawable;

    .line 47
    .line 48
    .line 49
    move-result-object p1

    .line 50
    const/4 v2, 0x0

    invoke-virtual {v0, p1}, Landroid/widget/ImageView;->setImageDrawable(Landroid/graphics/drawable/Drawable;)V

    .line 51
    .line 52
    .line 53
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 54
    .line 55
    const/4 v2, 0x6

    iget-object p0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->y:Lt6;

    .line 56
    .line 57
    invoke-virtual {p1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 58
    .line 59
    .line 60
    return-void

    .line 61
    :cond_45
    sget v1, Lagency/tango/materialintroscreen/R$drawable;->ic_next:I

    .line 62
    .line 63
    invoke-static {p0, v1}, Lw63;->getDrawable(Landroid/content/Context;I)Landroid/graphics/drawable/Drawable;

    .line 64
    .line 65
    .line 66
    move-result-object v1

    .line 67
    const/4 v2, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/ImageView;->setImageDrawable(Landroid/graphics/drawable/Drawable;)V

    .line 68
    .line 69
    .line 70
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 71
    .line 72
    const/4 v2, 0x6

    new-instance v1, Luy9;

    .line 73
    .line 74
    invoke-direct {v1, p0, p2, p1}, Luy9;-><init>(Lagency/tango/materialintroscreen/MaterialIntroActivity;Lxpe;I)V

    .line 75
    .line 76
    .line 77
    invoke-virtual {v0, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 78
    .line 79
    .line 80
    return-void
.end method

.method public O0()V
    .locals 1

    .line 1
    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .locals 6

    .line 1
    invoke-super {p0, p1}, Landroidx/fragment/app/FragmentActivity;->onCreate(Landroid/os/Bundle;)V

    .line 2
    .line 3
    .line 4
    const/4 v5, 0x3

    sget p1, Lagency/tango/materialintroscreen/R$layout;->activity_material_intro:I

    .line 5
    .line 6
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->setContentView(I)V

    .line 7
    .line 8
    .line 9
    sget p1, Lagency/tango/materialintroscreen/R$id;->view_pager_slides:I

    .line 10
    .line 11
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 12
    .line 13
    .line 14
    move-result-object p1

    .line 15
    check-cast p1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 16
    .line 17
    const/4 v5, 0x1

    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 18
    .line 19
    sget p1, Lagency/tango/materialintroscreen/R$id;->indicator:I

    .line 20
    .line 21
    const/4 v5, 0x0

    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 22
    .line 23
    .line 24
    move-result-object p1

    .line 25
    const/4 v5, 0x5

    check-cast p1, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 26
    .line 27
    const/4 v5, 0x5

    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->k:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 28
    .line 29
    sget p1, Lagency/tango/materialintroscreen/R$id;->button_back:I

    .line 30
    .line 31
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 32
    .line 33
    .line 34
    move-result-object p1

    .line 35
    check-cast p1, Landroid/widget/ImageButton;

    .line 36
    .line 37
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->m:Landroid/widget/ImageButton;

    .line 38
    .line 39
    sget p1, Lagency/tango/materialintroscreen/R$id;->button_next:I

    .line 40
    .line 41
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 42
    .line 43
    .line 44
    move-result-object p1

    .line 45
    check-cast p1, Landroid/widget/ImageButton;

    .line 46
    .line 47
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 48
    .line 49
    sget p1, Lagency/tango/materialintroscreen/R$id;->button_skip:I

    .line 50
    .line 51
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 52
    .line 53
    .line 54
    move-result-object p1

    .line 55
    const/4 v5, 0x6

    check-cast p1, Landroid/widget/ImageButton;

    .line 56
    .line 57
    const/4 v5, 0x3

    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->n:Landroid/widget/ImageButton;

    .line 58
    .line 59
    sget p1, Lagency/tango/materialintroscreen/R$id;->button_message:I

    .line 60
    .line 61
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 62
    .line 63
    .line 64
    move-result-object p1

    .line 65
    const/4 v5, 0x7

    check-cast p1, Landroid/widget/Button;

    .line 66
    .line 67
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->q:Landroid/widget/Button;

    .line 68
    .line 69
    sget p1, Lagency/tango/materialintroscreen/R$id;->coordinator_layout_slide:I

    .line 70
    .line 71
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 72
    .line 73
    .line 74
    move-result-object p1

    .line 75
    check-cast p1, Landroidx/coordinatorlayout/widget/CoordinatorLayout;

    .line 76
    .line 77
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->p:Landroidx/coordinatorlayout/widget/CoordinatorLayout;

    .line 78
    .line 79
    sget p1, Lagency/tango/materialintroscreen/R$id;->navigation_view:I

    .line 80
    .line 81
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->findViewById(I)Landroid/view/View;

    .line 82
    .line 83
    .line 84
    move-result-object p1

    .line 85
    check-cast p1, Landroid/widget/LinearLayout;

    .line 86
    .line 87
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->r:Landroid/widget/LinearLayout;

    .line 88
    .line 89
    const/4 v5, 0x2

    new-instance p1, Lcre;

    .line 90
    .line 91
    const/4 v5, 0x2

    invoke-virtual {p0}, Landroidx/fragment/app/FragmentActivity;->getSupportFragmentManager()Landroidx/fragment/app/y;

    .line 92
    .line 93
    .line 94
    move-result-object v0

    .line 95
    invoke-direct {p1, v0}, Lal6;-><init>(Landroidx/fragment/app/y;)V

    .line 96
    .line 97
    .line 98
    new-instance v0, Ljava/util/ArrayList;

    .line 99
    .line 100
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 101
    .line 102
    .line 103
    const/4 v5, 0x5

    iput-object v0, p1, Lcre;->i:Ljava/util/ArrayList;

    .line 104
    .line 105
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 106
    .line 107
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 108
    .line 109
    const/4 v5, 0x2

    invoke-virtual {v0, p1}, Landroidx/viewpager/widget/ViewPager;->setAdapter(Lnfb;)V

    .line 110
    .line 111
    .line 112
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 113
    .line 114
    const/4 v0, 0x4

    .line 115
    const/4 v5, 0x3

    invoke-virtual {p1, v0}, Landroidx/viewpager/widget/ViewPager;->setOffscreenPageLimit(I)V

    .line 116
    .line 117
    .line 118
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->k:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 119
    .line 120
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 121
    .line 122
    invoke-virtual {p1, v0}, Lagency/tango/materialintroscreen/widgets/InkPageIndicator;->setViewPager(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;)V

    .line 123
    .line 124
    .line 125
    new-instance p1, Lmra;

    .line 126
    .line 127
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->o:Landroid/widget/ImageButton;

    .line 128
    .line 129
    invoke-direct {p1, v0}, Lmra;-><init>(Landroid/view/View;)V

    .line 130
    .line 131
    .line 132
    new-instance v1, Ljj4;

    .line 133
    .line 134
    const/4 v2, 0x3

    .line 135
    invoke-direct {v1, v2}, Ljj4;-><init>(I)V

    .line 136
    .line 137
    .line 138
    const/4 v5, 0x6

    iput-object v1, p1, Lmra;->c:Lip7;

    .line 139
    .line 140
    const/4 v5, 0x2

    new-instance v1, Lh3d;

    .line 141
    .line 142
    const/4 v5, 0x3

    const/16 v3, 0x1d

    .line 143
    .line 144
    const/4 v5, 0x4

    invoke-direct {v1, v3}, Lh3d;-><init>(I)V

    .line 145
    .line 146
    .line 147
    iput-object v1, p1, Lmra;->d:Lip7;

    .line 148
    .line 149
    sget v1, Lagency/tango/materialintroscreen/R$anim;->shake_it:I

    .line 150
    .line 151
    if-eqz v1, :cond_b4

    .line 152
    .line 153
    invoke-virtual {v0}, Landroid/view/View;->getContext()Landroid/content/Context;

    .line 154
    .line 155
    .line 156
    move-result-object v0

    .line 157
    invoke-static {v0, v1}, Landroid/view/animation/AnimationUtils;->loadAnimation(Landroid/content/Context;I)Landroid/view/animation/Animation;

    .line 158
    .line 159
    .line 160
    move-result-object v0

    .line 161
    const/4 v5, 0x5

    iput-object v0, p1, Lmra;->e:Landroid/view/animation/Animation;

    .line 162
    .line 163
    :cond_b4
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->t:Lmra;

    .line 164
    .line 165
    new-instance p1, Lm7a;

    .line 166
    .line 167
    const/4 v5, 0x1

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->q:Landroid/widget/Button;

    .line 168
    .line 169
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 170
    .line 171
    invoke-direct {p1}, Ljava/lang/Object;-><init>()V

    .line 172
    .line 173
    .line 174
    iput-object v0, p1, Lm7a;->a:Landroid/widget/Button;

    .line 175
    .line 176
    iput-object v1, p1, Lm7a;->b:Lcre;

    .line 177
    .line 178
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->z:Landroid/util/SparseArray;

    .line 179
    .line 180
    iput-object v0, p1, Lm7a;->c:Landroid/util/SparseArray;

    .line 181
    .line 182
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->w:Lm7a;

    .line 183
    .line 184
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 185
    .line 186
    new-instance v0, Lwgf;

    .line 187
    .line 188
    invoke-direct {v0, p1, v1}, Lwgf;-><init>(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;Lcre;)V

    .line 189
    .line 190
    .line 191
    const/4 v5, 0x3

    iget-object p1, p1, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->k0:Ljava/util/ArrayList;

    .line 192
    .line 193
    invoke-virtual {p1, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 194
    .line 195
    .line 196
    new-instance p1, Lmra;

    .line 197
    .line 198
    const/4 v5, 0x4

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->k:Lagency/tango/materialintroscreen/widgets/InkPageIndicator;

    .line 199
    .line 200
    invoke-direct {p1, v0}, Lmra;-><init>(Landroid/view/View;)V

    .line 201
    .line 202
    .line 203
    new-instance v0, Lh3d;

    .line 204
    .line 205
    invoke-direct {v0, v3}, Lh3d;-><init>(I)V

    .line 206
    .line 207
    .line 208
    const/4 v5, 0x7

    iput-object v0, p1, Lmra;->d:Lip7;

    .line 209
    .line 210
    const/4 v5, 0x3

    new-instance v0, Ljj4;

    .line 211
    .line 212
    invoke-direct {v0, v2}, Ljj4;-><init>(I)V

    .line 213
    .line 214
    .line 215
    iput-object v0, p1, Lmra;->c:Lip7;

    .line 216
    .line 217
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->u:Lmra;

    .line 218
    .line 219
    new-instance p1, Lmra;

    .line 220
    .line 221
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 222
    .line 223
    invoke-direct {p1, v0}, Lmra;-><init>(Landroid/view/View;)V

    .line 224
    .line 225
    .line 226
    new-instance v0, Lwra;

    .line 227
    .line 228
    const/16 v1, 0x1c

    .line 229
    .line 230
    const/4 v5, 0x7

    invoke-direct {v0, v1}, Lwra;-><init>(I)V

    .line 231
    .line 232
    .line 233
    iput-object v0, p1, Lmra;->d:Lip7;

    .line 234
    .line 235
    new-instance v0, Lh3d;

    .line 236
    .line 237
    const/16 v1, 0xe

    .line 238
    .line 239
    invoke-direct {v0, v1}, Lh3d;-><init>(I)V

    .line 240
    .line 241
    .line 242
    iput-object v0, p1, Lmra;->c:Lip7;

    .line 243
    .line 244
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->v:Lmra;

    .line 245
    .line 246
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 247
    .line 248
    new-instance v0, Lt2h;

    .line 249
    .line 250
    const/4 v5, 0x3

    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 251
    .line 252
    invoke-direct {v0, v1}, Lt2h;-><init>(Lcre;)V

    .line 253
    .line 254
    .line 255
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->t:Lmra;

    .line 256
    .line 257
    iget-object v3, v0, Lt2h;->c:Ljava/util/ArrayList;

    .line 258
    .line 259
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 260
    .line 261
    .line 262
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->u:Lmra;

    .line 263
    .line 264
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 265
    .line 266
    .line 267
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->v:Lmra;

    .line 268
    .line 269
    const/4 v5, 0x3

    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 270
    .line 271
    .line 272
    const/4 v5, 0x7

    new-instance v1, Lty9;

    .line 273
    .line 274
    const/4 v3, 0x0

    .line 275
    const/4 v5, 0x6

    invoke-direct {v1, p0, v3}, Lty9;-><init>(Lagency/tango/materialintroscreen/MaterialIntroActivity;I)V

    .line 276
    .line 277
    .line 278
    iget-object v3, v0, Lt2h;->d:Ljava/util/ArrayList;

    .line 279
    .line 280
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 281
    .line 282
    .line 283
    new-instance v1, Lty9;

    .line 284
    .line 285
    const/4 v4, 0x1

    .line 286
    invoke-direct {v1, p0, v4}, Lty9;-><init>(Lagency/tango/materialintroscreen/MaterialIntroActivity;I)V

    .line 287
    .line 288
    .line 289
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 290
    .line 291
    .line 292
    const/4 v5, 0x1

    new-instance v1, Lty9;

    .line 293
    .line 294
    iget-object v4, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 295
    .line 296
    invoke-direct {v1}, Lty9;-><init>()V

    .line 297
    .line 298
    .line 299
    const/4 v5, 0x2

    iput-object v4, v1, Lty9;->b:Ljava/lang/Object;

    .line 300
    .line 301
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 302
    .line 303
    .line 304
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->w:Lm7a;

    .line 305
    .line 306
    const/4 v5, 0x6

    iget-object v3, v0, Lt2h;->b:Ljava/util/ArrayList;

    .line 307
    .line 308
    const/4 v5, 0x4

    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 309
    .line 310
    .line 311
    new-instance v1, Lsy9;

    .line 312
    .line 313
    const/4 v5, 0x7

    invoke-direct {v1, p0}, Lsy9;-><init>(Lagency/tango/materialintroscreen/MaterialIntroActivity;)V

    .line 314
    .line 315
    .line 316
    invoke-virtual {v3, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 317
    .line 318
    .line 319
    const/4 v5, 0x1

    iget-object v1, p1, Landroidx/viewpager/widget/ViewPager;->R:Ljava/util/ArrayList;

    .line 320
    .line 321
    if-nez v1, :cond_16b

    .line 322
    .line 323
    new-instance v1, Ljava/util/ArrayList;

    .line 324
    .line 325
    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V

    .line 326
    .line 327
    .line 328
    iput-object v1, p1, Landroidx/viewpager/widget/ViewPager;->R:Ljava/util/ArrayList;

    .line 329
    .line 330
    :cond_16b
    const/4 v5, 0x3

    invoke-interface {v1, v0}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 331
    .line 332
    .line 333
    new-instance p1, Lzk2;

    .line 334
    .line 335
    const/4 v5, 0x4

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->t:Lmra;

    .line 336
    .line 337
    invoke-direct {p1, v2, p0, v0}, Lzk2;-><init>(ILandroid/app/Activity;Ljava/lang/Object;)V

    .line 338
    .line 339
    .line 340
    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->x:Lzk2;

    .line 341
    .line 342
    new-instance p1, Lt6;

    .line 343
    .line 344
    const/4 v5, 0x4

    const/16 v0, 0x8

    .line 345
    .line 346
    const/4 v5, 0x3

    invoke-direct {p1, p0, v0}, Lt6;-><init>(Ljava/lang/Object;I)V

    .line 347
    .line 348
    .line 349
    const/4 v5, 0x1

    iput-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->y:Lt6;

    .line 350
    .line 351
    iget-object p1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 352
    .line 353
    new-instance v0, Lek6;

    .line 354
    .line 355
    const/16 v1, 0x12

    .line 356
    .line 357
    invoke-direct {v0, p0, v1}, Lek6;-><init>(Ljava/lang/Object;I)V

    .line 358
    .line 359
    .line 360
    invoke-virtual {p1, v0}, Landroid/view/View;->post(Ljava/lang/Runnable;)Z

    .line 361
    .line 362
    .line 363
    const/4 v5, 0x4

    invoke-virtual {p0}, Landroidx/activity/ComponentActivity;->getOnBackPressedDispatcher()Lt3b;

    .line 364
    .line 365
    .line 366
    move-result-object p1

    .line 367
    const/4 v5, 0x4

    new-instance v0, Lg9;

    .line 368
    .line 369
    const/4 v5, 0x2

    const/16 v1, 0xc

    .line 370
    .line 371
    invoke-direct {v0, p0, v1}, Lg9;-><init>(Ljava/lang/Object;I)V

    .line 372
    .line 373
    .line 374
    invoke-virtual {p1, p0, v0}, Lt3b;->a(Ls69;Lo3b;)V

    .line 375
    .line 376
    .line 377
    const/4 v5, 0x5

    return-void
.end method

.method public final onRequestPermissionsResult(I[Ljava/lang/String;[I)V
    .locals 5

    .line 1
    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->l:Lcre;

    .line 2
    .line 3
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 4
    .line 5
    invoke-virtual {v1}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 6
    .line 7
    .line 8
    move-result v1

    .line 9
    const/4 v4, 0x4

    invoke-virtual {v0, v1}, Lcre;->m(I)Lxpe;

    .line 10
    .line 11
    .line 12
    move-result-object v0

    .line 13
    iget-object v1, v0, Lxpe;->h:[Ljava/lang/String;

    .line 14
    .line 15
    invoke-virtual {v0, v1}, Lxpe;->q([Ljava/lang/String;)Z

    .line 16
    .line 17
    .line 18
    move-result v1

    .line 19
    const/4 v4, 0x1

    if-nez v1, :cond_36

    .line 20
    .line 21
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 22
    .line 23
    sget-object v2, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;->all:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;

    .line 24
    .line 25
    invoke-virtual {v1, v2}, Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;->setAllowedSwipeDirection(Lagency/tango/materialintroscreen/widgets/SwipeableViewPager$a;)V

    .line 26
    .line 27
    .line 28
    const/4 v4, 0x0

    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 29
    .line 30
    invoke-virtual {v1}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 31
    .line 32
    .line 33
    move-result v1

    .line 34
    invoke-virtual {p0, v1, v0}, Lagency/tango/materialintroscreen/MaterialIntroActivity;->N0(ILxpe;)V

    .line 35
    .line 36
    .line 37
    const/4 v4, 0x5

    iget-object v0, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->w:Lm7a;

    .line 38
    .line 39
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->j:Lagency/tango/materialintroscreen/widgets/SwipeableViewPager;

    .line 40
    .line 41
    invoke-virtual {v1}, Landroidx/viewpager/widget/ViewPager;->getCurrentItem()I

    .line 42
    .line 43
    .line 44
    move-result v1

    .line 45
    const/4 v4, 0x2

    invoke-virtual {v0, v1}, Lm7a;->a(I)V

    .line 46
    .line 47
    .line 48
    const/4 v4, 0x5

    goto :goto_6b

    .line 49
    :cond_36
    sget v0, Lagency/tango/materialintroscreen/R$string;->please_grant_permissions:I

    .line 50
    .line 51
    invoke-virtual {p0, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 52
    .line 53
    .line 54
    move-result-object v0

    .line 55
    iget-object v1, p0, Lagency/tango/materialintroscreen/MaterialIntroActivity;->p:Landroidx/coordinatorlayout/widget/CoordinatorLayout;

    .line 56
    .line 57
    invoke-static {v1, v0}, Lcom/google/android/material/snackbar/Snackbar;->g(Landroid/view/View;Ljava/lang/String;)Lcom/google/android/material/snackbar/Snackbar;

    .line 58
    .line 59
    .line 60
    move-result-object v0

    .line 61
    const/4 v4, 0x5

    new-instance v1, Lry9;

    .line 62
    .line 63
    invoke-direct {v1, p0}, Lry9;-><init>(Lagency/tango/materialintroscreen/MaterialIntroActivity;)V

    .line 64
    .line 65
    .line 66
    iget-object v2, v0, Lcom/google/android/material/snackbar/Snackbar;->C:Lry9;

    .line 67
    .line 68
    if-eqz v2, :cond_56

    .line 69
    .line 70
    iget-object v3, v0, Lcom/google/android/material/snackbar/BaseTransientBottomBar;->s:Ljava/util/ArrayList;

    .line 71
    .line 72
    const/4 v4, 0x4

    if-nez v3, :cond_52

    .line 73
    .line 74
    goto :goto_56

    .line 75
    :cond_52
    const/4 v4, 0x1

    invoke-virtual {v3, v2}, Ljava/util/ArrayList;->remove(Ljava/lang/Object;)Z

    .line 76
    .line 77
    .line 78
    :cond_56
    :goto_56
    iget-object v2, v0, Lcom/google/android/material/snackbar/BaseTransientBottomBar;->s:Ljava/util/ArrayList;

    .line 79
    .line 80
    const/4 v4, 0x1

    if-nez v2, :cond_62

    .line 81
    .line 82
    new-instance v2, Ljava/util/ArrayList;

    .line 83
    .line 84
    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 85
    .line 86
    .line 87
    iput-object v2, v0, Lcom/google/android/material/snackbar/BaseTransientBottomBar;->s:Ljava/util/ArrayList;

    .line 88
    .line 89
    :cond_62
    invoke-interface {v2, v1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 90
    .line 91
    .line 92
    iput-object v1, v0, Lcom/google/android/material/snackbar/Snackbar;->C:Lry9;

    .line 93
    .line 94
    const/4 v4, 0x5

    invoke-virtual {v0}, Lcom/google/android/material/snackbar/Snackbar;->h()V

    .line 95
    .line 96
    .line 97
    :goto_6b
    invoke-super {p0, p1, p2, p3}, Landroidx/fragment/app/FragmentActivity;->onRequestPermissionsResult(I[Ljava/lang/String;[I)V

    .line 98
    .line 99
    .line 100
    return-void
.end method
