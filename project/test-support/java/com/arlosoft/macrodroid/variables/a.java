package com.arlosoft.macrodroid.variables;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.TouchControl;
public class a {
    public static Object lastMacro, lastVariable, lastInfo;
    public static int lastBaseColor, colorCalls;
    public static int e(Macro macro,VariableWithDictionaryKeys variable,int color,TriggerContextInfo info) {
        TouchControl.hit("color.resolve:"+(macro==null?"null":macro.testId)+":"+(variable==null?"null":variable.testId)+":"+color+":"+(info==null?"null":"trigger-context"));
        colorCalls++;lastMacro=macro;lastVariable=variable;lastInfo=info;lastBaseColor=color;
        return TouchControl.resolveColor?TouchControl.resolvedColor:color;
    }
}
