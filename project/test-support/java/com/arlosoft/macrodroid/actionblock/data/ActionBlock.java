package com.arlosoft.macrodroid.actionblock.data;public class ActionBlock extends com.arlosoft.macrodroid.macro.Macro {public com.arlosoft.macrodroid.macro.Macro parent;public boolean testMode;public com.arlosoft.macrodroid.macro.Macro getTopLevelParentMacro(){defpackage.CoreTrace.add(testId+".parent");return parent;}public boolean isTestMode(){defpackage.CoreTrace.add(testId+".testMode");return testMode;}
 public boolean displayingScene; public int displayingSceneWrites;
 public void setDisplayingScene(boolean value){defpackage.TouchControl.hit("scene.displaying:"+testId+":"+value);displayingScene=value;displayingSceneWrites++;}
}
