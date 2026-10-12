.class public final Loracle/EnginePrimitives;
.super Ljava/lang/Object;

.method public static longAsDouble(J)D
 .locals 2
 long-to-double v0, p0
 return-wide v0
.end method
.method public static doubleAsInt(D)I
 .locals 1
 double-to-int v0, p0
 return v0
.end method
.method public static underLock(Ljava/lang/Object;)Z
 .locals 2
 monitor-enter p0
 :begin
 invoke-static {p0}, Ljava/lang/Thread;->holdsLock(Ljava/lang/Object;)Z
 move-result v0
 monitor-exit p0
 :end
 return v0
 :error
 move-exception v1
 monitor-exit p0
 throw v1
 .catchall {:begin .. :end} :error
.end method
.method public static nestedLocks(Ljava/lang/Object;Ljava/lang/Object;)I
 .locals 3
 monitor-enter p0
 :outer
 monitor-enter p1
 :inner
 invoke-static {p0}, Ljava/lang/Thread;->holdsLock(Ljava/lang/Object;)Z
 move-result v0
 invoke-static {p1}, Ljava/lang/Thread;->holdsLock(Ljava/lang/Object;)Z
 move-result v1
 add-int/2addr v0, v1
 monitor-exit p1
 :innerEnd
 monitor-exit p0
 :outerEnd
 return v0
 :innerError
 move-exception v2
 monitor-exit p1
 throw v2
 :outerError
 move-exception v2
 monitor-exit p0
 throw v2
 .catchall {:inner .. :innerEnd} :innerError
 .catchall {:outer .. :inner} :outerError
 .catchall {:innerEnd .. :outerEnd} :outerError
 .catchall {:innerError .. :outerError} :outerError
.end method
.method public static throwInside(Ljava/lang/Object;Ljava/lang/Throwable;)V
 .locals 1
 monitor-enter p0
 :begin
 throw p1
 :end
 :error
 move-exception v0
 monitor-exit p0
 throw v0
 .catchall {:begin .. :end} :error
.end method
.method public static interruptedWait(Ljava/lang/Object;)Z
 .locals 2
 monitor-enter p0
 :begin
 invoke-virtual {p0}, Ljava/lang/Object;->wait()V
 :afterWait
 const/4 v0, 0x0
 :leave
 monitor-exit p0
 :end
 return v0
 :interrupt
 move-exception v1
 :restore
 invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;
 move-result-object v1
 invoke-virtual {v1}, Ljava/lang/Thread;->interrupt()V
 const/4 v0, 0x1
 goto :leave
 :restoreEnd
 :error
 move-exception v1
 monitor-exit p0
 throw v1
 .catch Ljava/lang/InterruptedException; {:begin .. :afterWait} :interrupt
 .catchall {:begin .. :end} :error
 .catchall {:restore .. :restoreEnd} :error
.end method
.method public static timedWait(Ljava/lang/Object;)Z
 .locals 3
 monitor-enter p0
 :begin
 const-wide/16 v0, 0x3e8
 invoke-virtual {p0, v0, v1}, Ljava/lang/Object;->wait(J)V
 invoke-static {p0}, Ljava/lang/Thread;->holdsLock(Ljava/lang/Object;)Z
 move-result v0
 monitor-exit p0
 :end
 return v0
 :error
 move-exception v2
 monitor-exit p0
 throw v2
 .catchall {:begin .. :end} :error
.end method
# Invalid synthetic sequences below exercise interpreter rejection/exception-PC
# semantics only; no assertion that ART's verifier would accept these methods.
.method public static advancedExitPc(Ljava/lang/Object;)Z
 .locals 1
 monitor-exit p0
 :advanced
 const/4 v0, 0x0
 return v0
 :end
 :handler
 move-exception v0
 const/4 v0, 0x1
 return v0
 .catch Ljava/lang/IllegalMonitorStateException; {:advanced .. :end} :handler
.end method
.method public static crossedLocks(Ljava/lang/Object;Ljava/lang/Object;)V
 .locals 0
 monitor-enter p0
 monitor-enter p1
 monitor-exit p0
 monitor-exit p1
 return-void
.end method
.method public static missingExit(Ljava/lang/Object;)V
 .locals 0
 monitor-enter p0
 return-void
.end method
