package com.arlosoft.macrodroid.action;

import android.content.Context;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.variables.VariableWithDictionaryKeys;
import defpackage.TouchControl;

/** Public compile-only field surface; original visibility and storage remain in the APK. */
public class BlockTouchesAction extends Action {
    public int option, bgColor;
    public boolean showBlockedArea, useAccessibilityService;
    public float xPosition, yPosition, width, height;
    public VariableWithDictionaryKeys bgColorVariable;
    public Context[] contextSequence;
    public int contextReads, macroReads;
    @Override public Context getContext() {
        TouchControl.hit("block.context:"+contextReads);
        int read = contextReads++;
        return contextSequence == null ? context : contextSequence[Math.min(read, contextSequence.length-1)];
    }
    @Override public Macro getMacro() {
        TouchControl.hit("block.macro"); macroReads++; return macro;
    }
}
