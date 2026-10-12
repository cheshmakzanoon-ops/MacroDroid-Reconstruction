package com.arlosoft.macrodroid.action;

import android.content.Context;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.scene.data.SceneDescription;
import defpackage.TouchControl;

/** Host-only mutable dependency results used to observe each original lookup. */
public class CustomSceneAction extends Action {
    public SceneDescription sceneDescription;
    public int contextReads, macroReads, guidReads, itemReads, nameReads;
    public Context[] contextSequence;
    public Macro[] macroSequence;
    public Long[] guidSequence;
    public long[] itemSequence;
    public String[] nameSequence;
    @Override public Context getContext() {
        int index = contextReads++; TouchControl.hit("scene.context:"+index);
        return contextSequence == null ? context : contextSequence[Math.min(index, contextSequence.length-1)];
    }
    @Override public Macro getMacro() {
        int index = macroReads++; TouchControl.hit("scene.macro:"+index);
        return macroSequence == null ? macro : macroSequence[Math.min(index, macroSequence.length-1)];
    }
    @Override public Long getMacroGuid() {
        int index = guidReads++; TouchControl.hit("scene.guid:"+index);
        return guidSequence == null ? macroGuid : guidSequence[Math.min(index, guidSequence.length-1)];
    }
    @Override public long getSIGUID() {
        int index = itemReads++; TouchControl.hit("scene.item:"+index);
        return itemSequence == null ? itemGuid : itemSequence[Math.min(index, itemSequence.length-1)];
    }
    @Override public String getName() {
        int index = nameReads++; TouchControl.hit("scene.name:"+index);
        return nameSequence == null ? configured : nameSequence[Math.min(index, nameSequence.length-1)];
    }
}
