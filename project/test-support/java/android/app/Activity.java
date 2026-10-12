package android.app;

public class Activity extends android.content.Context {
    public boolean finishing, destroyed;
    public int finishingReads, destroyedReads, dispatches;
    public boolean isFinishing() {
        finishingReads++; defpackage.TouchControl.hit("activity.finishing:"+testContextId); return finishing;
    }
    public boolean isDestroyed() {
        destroyedReads++; defpackage.TouchControl.hit("activity.destroyed:"+testContextId); return destroyed;
    }
    public void runOnUiThread(Runnable runnable) {
        defpackage.TouchControl.hit("activity.runOnUiThread:"+testContextId+":"+defpackage.SceneControl.id(runnable));
        dispatches++; defpackage.SceneControl.queuedTasks.add(runnable);
    }
}
