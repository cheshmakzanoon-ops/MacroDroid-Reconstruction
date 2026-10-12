.class public final Lrecovered/probe/WidgetMethodProbe;
.super Ljava/lang/Object;


# static fields
.field private static manager:Ljava/lang/Object;

.field private static managerType:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation
.end field

.field private static stateConstructor:Ljava/lang/reflect/Constructor;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/reflect/Constructor<",
            "*>;"
        }
    .end annotation
.end field

.field private static stateType:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation
.end field

.field private static unit:Ljava/lang/Object;

.field private static update:Ljava/lang/reflect/Method;


# direct methods
.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static failure(Ljava/util/List;Ljava/lang/Object;Ljava/lang/Class;)Ljava/lang/Throwable;
    .locals 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "*>;",
            "Ljava/lang/Object;",
            "Ljava/lang/Class<",
            "*>;)",
            "Ljava/lang/Throwable;"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    :try_start_0
    invoke-static {p0, p1}, Lrecovered/probe/WidgetMethodProbe;->invoke(Ljava/util/List;Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_3
    .catch Ljava/lang/reflect/InvocationTargetException; {:try_start_0 .. :try_end_3} :catch_1c

    new-instance p0, Ljava/lang/AssertionError;

    new-instance p1, Ljava/lang/StringBuilder;

    const-string v0, "Expected target method to throw "

    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p0

    :catch_1c
    move-exception p0

    invoke-virtual {p0}, Ljava/lang/reflect/InvocationTargetException;->getCause()Ljava/lang/Throwable;

    move-result-object p0

    if-eqz p0, :cond_2b

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object p1

    if-ne p1, p2, :cond_2b

    const/4 p1, 0x1

    goto :goto_2c

    :cond_2b
    const/4 p1, 0x0

    :goto_2c
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Expected "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    const-string v0, " but observed "

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    if-nez p0, :cond_46

    const-string v0, "null"

    goto :goto_4e

    :cond_46
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v0

    :goto_4e
    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-static {p1, p2}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    return-object p0
.end method

.method private static field(Ljava/lang/String;)Ljava/lang/reflect/Field;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->stateType:Ljava/lang/Class;

    invoke-virtual {v0, p0}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    return-object p0
.end method

.method private static invoke(Ljava/util/List;Ljava/lang/Object;)Ljava/lang/Object;
    .locals 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "*>;",
            "Ljava/lang/Object;",
            ")",
            "Ljava/lang/Object;"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->update:Ljava/lang/reflect/Method;

    sget-object v1, Lrecovered/probe/WidgetMethodProbe;->manager:Ljava/lang/Object;

    const/4 v2, 0x3

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    const/4 v4, 0x0

    aput-object v3, v2, v4

    const/4 v3, 0x1

    aput-object p0, v2, v3

    const/4 p0, 0x2

    aput-object p1, v2, p0

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    return-object p0
.end method

.method public static main([Ljava/lang/String;)V
    .locals 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    array-length p0, p0

    const/4 v0, 0x1

    const/4 v1, 0x0

    if-nez p0, :cond_7

    move p0, v0

    goto :goto_8

    :cond_7
    move p0, v1

    :goto_8
    const-string v2, "Widget probe takes no arguments"

    invoke-static {p0, v2}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    invoke-static {}, Lrecovered/probe/WidgetMethodProbe;->prepare()V

    invoke-static {}, Ljava/util/Collections;->emptyList()Ljava/util/List;

    move-result-object p0

    const/4 v2, 0x0

    invoke-static {p0, v2}, Lrecovered/probe/WidgetMethodProbe;->invoke(Ljava/util/List;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    sget-object v3, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    if-ne p0, v3, :cond_1f

    move p0, v0

    goto :goto_20

    :cond_1f
    move p0, v1

    :goto_20
    const-string v3, "Fresh empty list did not return the real Unit singleton"

    invoke-static {p0, v3}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string p0, "fresh-empty-unit-identity"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    invoke-static {}, Lrecovered/probe/WidgetMethodProbe;->slots()[Ljava/lang/Object;

    move-result-object p0

    invoke-static {v1, p0}, Lrecovered/probe/WidgetMethodProbe;->newState(I[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v3

    invoke-static {}, Ljava/util/Collections;->emptyList()Ljava/util/List;

    move-result-object v4

    invoke-static {v4, v3}, Lrecovered/probe/WidgetMethodProbe;->invoke(Ljava/util/List;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    sget-object v5, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    if-ne v4, v5, :cond_40

    move v4, v0

    goto :goto_41

    :cond_40
    move v4, v1

    :goto_41
    const-string v5, "Reused label 0 did not return Unit"

    invoke-static {v4, v5}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    invoke-static {v3, v1, p0}, Lrecovered/probe/WidgetMethodProbe;->unchangedState(Ljava/lang/Object;I[Ljava/lang/Object;)V

    const-string p0, "reused-label-zero-empty"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    invoke-static {}, Lrecovered/probe/WidgetMethodProbe;->slots()[Ljava/lang/Object;

    move-result-object p0

    const/4 v3, 0x2

    invoke-static {v3, p0}, Lrecovered/probe/WidgetMethodProbe;->newState(I[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    invoke-static {v2, v4}, Lrecovered/probe/WidgetMethodProbe;->invoke(Ljava/util/List;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    sget-object v6, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    if-ne v5, v6, :cond_61

    move v5, v0

    goto :goto_62

    :cond_61
    move v5, v1

    :goto_62
    const-string v6, "Label 2 with empty iterator did not return Unit"

    invoke-static {v5, v6}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    invoke-static {v4, v3, p0}, Lrecovered/probe/WidgetMethodProbe;->unchangedState(Ljava/lang/Object;I[Ljava/lang/Object;)V

    const-string p0, "resumed-label-two-empty"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    invoke-static {}, Lrecovered/probe/WidgetMethodProbe;->slots()[Ljava/lang/Object;

    move-result-object p0

    const/4 v4, 0x3

    invoke-static {v4, p0}, Lrecovered/probe/WidgetMethodProbe;->newState(I[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    const-class v6, Ljava/lang/IllegalStateException;

    invoke-static {v2, v5, v6}, Lrecovered/probe/WidgetMethodProbe;->failure(Ljava/util/List;Ljava/lang/Object;Ljava/lang/Class;)Ljava/lang/Throwable;

    move-result-object v6

    const-string v7, "call to \'resume\' before \'invoke\' with coroutine"

    invoke-virtual {v6}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v7, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    const-string v7, "Invalid-label exception message differs from the preserved literal"

    invoke-static {v6, v7}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    invoke-static {v5, v4, p0}, Lrecovered/probe/WidgetMethodProbe;->unchangedState(Ljava/lang/Object;I[Ljava/lang/Object;)V

    const-string p0, "invalid-label-exact-exception"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    const/4 p0, 0x7

    const/4 v5, 0x4

    filled-new-array {p0, v5, v0}, [I

    move-result-object p0

    :goto_9b
    if-ge v1, v4, :cond_cc

    aget v0, p0, v1

    invoke-static {}, Lrecovered/probe/WidgetMethodProbe;->slots()[Ljava/lang/Object;

    move-result-object v5

    const/16 v6, 0x347

    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v6

    aput-object v6, v5, v0

    invoke-static {v3, v5}, Lrecovered/probe/WidgetMethodProbe;->newState(I[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v6

    const-class v7, Ljava/lang/ClassCastException;

    invoke-static {v2, v6, v7}, Lrecovered/probe/WidgetMethodProbe;->failure(Ljava/util/List;Ljava/lang/Object;Ljava/lang/Class;)Ljava/lang/Throwable;

    invoke-static {v6, v3, v5}, Lrecovered/probe/WidgetMethodProbe;->unchangedState(Ljava/lang/Object;I[Ljava/lang/Object;)V

    new-instance v5, Ljava/lang/StringBuilder;

    const-string v6, "label-two-dead-cast-L"

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v5, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_9b

    :cond_cc
    const-class p0, Ljava/lang/NullPointerException;

    invoke-static {v2, v2, p0}, Lrecovered/probe/WidgetMethodProbe;->failure(Ljava/util/List;Ljava/lang/Object;Ljava/lang/Class;)Ljava/lang/Throwable;

    const-string p0, "null-list-exception-type"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->passed(Ljava/lang/String;)V

    sget-object p0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    const-string v0, "WIDGET_METHOD_ART_OK cases=8"

    invoke-virtual {p0, v0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    return-void
.end method

.method private static newState(I[Ljava/lang/Object;)Ljava/lang/Object;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->stateConstructor:Ljava/lang/reflect/Constructor;

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Object;

    sget-object v2, Lrecovered/probe/WidgetMethodProbe;->manager:Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const/4 v2, 0x0

    const/4 v4, 0x1

    aput-object v2, v1, v4

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    const-string v1, "label"

    invoke-static {v1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v1

    const/high16 v2, -0x80000000

    or-int/2addr p0, v2

    invoke-virtual {v1, v0, p0}, Ljava/lang/reflect/Field;->setInt(Ljava/lang/Object;I)V

    const-string p0, "result"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    sget-object v1, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    const-string p0, "I$0"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    const/16 v1, -0xd

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Field;->setInt(Ljava/lang/Object;I)V

    const-string p0, "I$1"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    const/16 v1, 0x1a1

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Field;->setInt(Ljava/lang/Object;I)V

    const-string p0, "I$2"

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    const v1, 0x7fffffff

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Field;->setInt(Ljava/lang/Object;I)V

    :goto_4b
    array-length p0, p1

    if-ge v3, p0, :cond_69

    new-instance p0, Ljava/lang/StringBuilder;

    const-string v1, "L$"

    invoke-direct {p0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p0

    aget-object v1, p1, v3

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_4b

    :cond_69
    return-object v0
.end method

.method private static passed(Ljava/lang/String;)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    const-string v1, "d"

    invoke-virtual {v0, v1}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    if-nez v0, :cond_11

    const/4 v0, 0x1

    goto :goto_12

    :cond_11
    const/4 v0, 0x0

    :goto_12
    const-string v1, "A probe case changed the application Context field"

    invoke-static {v0, v1}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "WIDGET_ART_CASE_OK "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    return-void
.end method

.method private static prepare()V
    .locals 15
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    const-class v0, Lrecovered/probe/WidgetMethodProbe;

    invoke-virtual {v0}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v0

    const-string v1, "android.os.Looper"

    const/4 v2, 0x1

    invoke-static {v1, v2, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v1

    const/4 v3, 0x0

    new-array v4, v3, [Ljava/lang/Class;

    const-string v5, "getMainLooper"

    invoke-virtual {v1, v5, v4}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    new-array v6, v3, [Ljava/lang/Object;

    const/4 v7, 0x0

    invoke-virtual {v4, v7, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    const-string v6, "myLooper"

    if-nez v4, :cond_50

    new-array v4, v3, [Ljava/lang/Class;

    invoke-virtual {v1, v6, v4}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    new-array v8, v3, [Ljava/lang/Object;

    invoke-virtual {v4, v7, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    if-nez v4, :cond_31

    move v4, v2

    goto :goto_32

    :cond_31
    move v4, v3

    :goto_32
    const-string v8, "Guest main thread already has a non-main Looper"

    invoke-static {v4, v8}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string v4, "prepareMainLooper"

    new-array v8, v3, [Ljava/lang/Class;

    invoke-virtual {v1, v4, v8}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    new-array v8, v3, [Ljava/lang/Object;

    invoke-virtual {v4, v7, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    new-array v4, v3, [Ljava/lang/Class;

    invoke-virtual {v1, v5, v4}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    new-array v5, v3, [Ljava/lang/Object;

    invoke-virtual {v4, v7, v5}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    :cond_50
    if-eqz v4, :cond_62

    new-array v5, v3, [Ljava/lang/Class;

    invoke-virtual {v1, v6, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    new-array v5, v3, [Ljava/lang/Object;

    invoke-virtual {v1, v7, v5}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    if-ne v1, v4, :cond_62

    move v1, v2

    goto :goto_63

    :cond_62
    move v1, v3

    :goto_63
    const-string v4, "Guest main Looper was not prepared on this thread"

    invoke-static {v1, v4}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string v1, "com.arlosoft.macrodroid.widget.custom.WidgetUpdateManager"

    invoke-static {v1, v2, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v1

    sput-object v1, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    const-string v1, "com.arlosoft.macrodroid.widget.custom.b"

    invoke-static {v1, v2, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v1

    sput-object v1, Lrecovered/probe/WidgetMethodProbe;->stateType:Ljava/lang/Class;

    const-string v1, "o73"

    invoke-static {v1, v3, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v1

    const-string v4, "blg"

    invoke-static {v4, v2, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v4

    const/4 v5, 0x4

    new-array v6, v5, [Ljava/lang/Class;

    sget-object v8, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    aput-object v8, v6, v3

    sget-object v8, Lrecovered/probe/WidgetMethodProbe;->stateType:Ljava/lang/Class;

    aput-object v8, v6, v2

    const/4 v8, 0x2

    aput-object v1, v6, v8

    const/4 v9, 0x3

    aput-object v4, v6, v9

    move v10, v3

    :goto_96
    if-ge v10, v5, :cond_bc

    aget-object v11, v6, v10

    invoke-virtual {v11}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v12

    if-ne v12, v0, :cond_a2

    move v12, v2

    goto :goto_a3

    :cond_a2
    move v12, v3

    :goto_a3
    new-instance v13, Ljava/lang/StringBuilder;

    const-string v14, "Application class came from another classloader: "

    invoke-direct {v13, v14}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v11}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v11

    invoke-virtual {v13, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v11

    invoke-virtual {v11}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v11

    invoke-static {v12, v11}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    add-int/lit8 v10, v10, 0x1

    goto :goto_96

    :cond_bc
    sget-object v5, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    const-string v6, "a"

    invoke-virtual {v5, v6}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v5

    invoke-virtual {v5, v7}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    sput-object v5, Lrecovered/probe/WidgetMethodProbe;->manager:Ljava/lang/Object;

    invoke-virtual {v4, v6}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v5

    invoke-virtual {v5, v7}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    sput-object v5, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    sget-object v5, Lrecovered/probe/WidgetMethodProbe;->manager:Ljava/lang/Object;

    if-eqz v5, :cond_e2

    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    sget-object v6, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    if-ne v5, v6, :cond_e2

    move v5, v2

    goto :goto_e3

    :cond_e2
    move v5, v3

    :goto_e3
    const-string v6, "Real manager singleton identity is invalid"

    invoke-static {v5, v6}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    sget-object v5, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    if-eqz v5, :cond_f4

    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    if-ne v5, v4, :cond_f4

    move v4, v2

    goto :goto_f5

    :cond_f4
    move v4, v3

    :goto_f5
    const-string v5, "Real Unit singleton identity is invalid"

    invoke-static {v4, v5}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string v4, "android.content.Context"

    invoke-static {v4, v3, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v0

    sget-object v4, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    new-array v5, v9, [Ljava/lang/Class;

    aput-object v0, v5, v3

    const-class v0, Ljava/util/List;

    aput-object v0, v5, v2

    aput-object v1, v5, v8

    const-string v0, "m"

    invoke-virtual {v4, v0, v5}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lrecovered/probe/WidgetMethodProbe;->update:Ljava/lang/reflect/Method;

    invoke-virtual {v0}, Ljava/lang/reflect/Method;->getDeclaringClass()Ljava/lang/Class;

    move-result-object v0

    sget-object v4, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    if-ne v0, v4, :cond_128

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->update:Ljava/lang/reflect/Method;

    invoke-virtual {v0}, Ljava/lang/reflect/Method;->getReturnType()Ljava/lang/Class;

    move-result-object v0

    const-class v4, Ljava/lang/Object;

    if-ne v0, v4, :cond_128

    move v0, v2

    goto :goto_129

    :cond_128
    move v0, v3

    :goto_129
    const-string v4, "Selected method has an unexpected owner or return type"

    invoke-static {v0, v4}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->update:Ljava/lang/reflect/Method;

    invoke-virtual {v0}, Ljava/lang/reflect/Method;->getModifiers()I

    move-result v0

    const/16 v4, 0x11

    if-ne v0, v4, :cond_13a

    move v0, v2

    goto :goto_13b

    :cond_13a
    move v0, v3

    :goto_13b
    const-string v4, "Selected method is not the preserved public final instance method"

    invoke-static {v0, v4}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->stateType:Ljava/lang/Class;

    new-array v4, v8, [Ljava/lang/Class;

    sget-object v5, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    aput-object v5, v4, v3

    aput-object v1, v4, v2

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v0

    sput-object v0, Lrecovered/probe/WidgetMethodProbe;->stateConstructor:Ljava/lang/reflect/Constructor;

    invoke-virtual {v0, v2}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->managerType:Ljava/lang/Class;

    const-string v1, "d"

    invoke-virtual {v0, v1}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    invoke-virtual {v0, v7}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    if-nez v0, :cond_162

    goto :goto_163

    :cond_162
    move v2, v3

    :goto_163
    const-string v0, "Guest initialization unexpectedly set an application Context"

    invoke-static {v2, v0}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    return-void
.end method

.method private static require(ZLjava/lang/String;)V
    .locals 0

    if-eqz p0, :cond_3

    return-void

    :cond_3
    new-instance p0, Ljava/lang/AssertionError;

    invoke-direct {p0, p1}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p0
.end method

.method private static slots()[Ljava/lang/Object;
    .locals 5

    invoke-static {}, Ljava/util/Collections;->emptyList()Ljava/util/List;

    move-result-object v0

    invoke-interface {v0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v0

    new-instance v1, Ljava/lang/Object;

    invoke-direct {v1}, Ljava/lang/Object;-><init>()V

    const/16 v2, 0x8

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    const/4 v4, 0x0

    aput-object v4, v2, v3

    const/4 v3, 0x1

    aput-object v4, v2, v3

    const/4 v3, 0x2

    aput-object v4, v2, v3

    const/4 v3, 0x3

    aput-object v4, v2, v3

    const/4 v3, 0x4

    aput-object v4, v2, v3

    const/4 v3, 0x5

    aput-object v0, v2, v3

    const/4 v0, 0x6

    aput-object v1, v2, v0

    const/4 v0, 0x7

    aput-object v4, v2, v0

    return-object v2
.end method

.method private static unchangedState(Ljava/lang/Object;I[Ljava/lang/Object;)V
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    const-string v0, "label"

    invoke-static {v0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    invoke-virtual {v0, p0}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result v0

    const/4 v1, 0x1

    const/4 v2, 0x0

    if-ne v0, p1, :cond_10

    move p1, v1

    goto :goto_11

    :cond_10
    move p1, v2

    :goto_11
    const-string v0, "Continuation high bit or saved label changed incorrectly"

    invoke-static {p1, v0}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string p1, "result"

    invoke-static {p1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->unit:Ljava/lang/Object;

    if-ne p1, v0, :cond_34

    const-string p1, "this$0"

    invoke-static {p1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    sget-object v0, Lrecovered/probe/WidgetMethodProbe;->manager:Ljava/lang/Object;

    if-ne p1, v0, :cond_34

    move p1, v1

    goto :goto_35

    :cond_34
    move p1, v2

    :goto_35
    const-string v0, "Continuation result or owner identity changed"

    invoke-static {p1, v0}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    const-string p1, "I$0"

    invoke-static {p1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result p1

    const/16 v0, -0xd

    if-ne p1, v0, :cond_67

    const-string p1, "I$1"

    invoke-static {p1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result p1

    const/16 v0, 0x1a1

    if-ne p1, v0, :cond_67

    const-string p1, "I$2"

    invoke-static {p1}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result p1

    const v0, 0x7fffffff

    if-ne p1, v0, :cond_67

    move p1, v1

    goto :goto_68

    :cond_67
    move p1, v2

    :goto_68
    const-string v0, "Saved integer state changed on a service-free branch"

    invoke-static {p1, v0}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    move p1, v2

    :goto_6e
    array-length v0, p2

    if-ge p1, v0, :cond_a4

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v3, "L$"

    invoke-direct {v0, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lrecovered/probe/WidgetMethodProbe;->field(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    invoke-virtual {v0, p0}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    aget-object v3, p2, p1

    if-ne v0, v3, :cond_8e

    move v0, v1

    goto :goto_8f

    :cond_8e
    move v0, v2

    :goto_8f
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "Saved object slot changed: L$"

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v0, v3}, Lrecovered/probe/WidgetMethodProbe;->require(ZLjava/lang/String;)V

    add-int/lit8 p1, p1, 0x1

    goto :goto_6e

    :cond_a4
    return-void
.end method
