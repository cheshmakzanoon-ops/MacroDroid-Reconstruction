package defpackage;

import com.arlosoft.macrodroid.scene.display.SceneDisplayActivity;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.data.ResumeMacroInfo;
import java.util.Stack;

/** Records the original Runnable constructor arguments; execution is a separate dependency. */
public class eld implements Runnable {
    public final int a, i;
    public final SceneDisplayActivity b;
    public final TriggerContextInfo c;
    public final long d, e;
    public final Stack f;
    public final boolean g;
    public final ResumeMacroInfo h;
    public eld(SceneDisplayActivity activity, TriggerContextInfo info, long guid, long item,
            Stack stack, boolean isTest, ResumeMacroInfo resume, int next, int kind) {
        a=kind; b=activity; c=info; d=guid; e=item; f=stack; g=isTest; h=resume; i=next;
        SceneControl.name(this, "task"+SceneControl.tasks.size()); SceneControl.tasks.add(this);
        TouchControl.hit("scene.task.new:"+kind+":"+SceneControl.id(activity)+":"+guid+":"+item+":"+next+":"+isTest);
    }
    @Override public void run() { SceneControl.runCalls++; TouchControl.hit("scene.task.run:"+SceneControl.id(this)); }
}
