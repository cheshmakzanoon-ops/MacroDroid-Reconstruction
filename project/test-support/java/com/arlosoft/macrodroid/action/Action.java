package com.arlosoft.macrodroid.action;
import java.util.*;import com.arlosoft.macrodroid.common.SelectableItem;import com.arlosoft.macrodroid.macro.Macro;import com.arlosoft.macrodroid.triggers.TriggerContextInfo;import defpackage.*;
public class Action extends SelectableItem {
 public long debugExecutionGeneration;public String label="";public int executions,cancelAtExecution;
 public boolean cancelOnExecute,disableOnExecute,disableAppOnExecute;
 public static a Companion=new a();public static class a {public static LinkedHashMap d(List l){return recovered.engine.ActionScopeMethods.scopes(l);}}
 public static Map computeActionScopes(List l){return recovered.engine.ActionScopeMethods.compute(l);}
 public void setMacro(Macro m){CoreTrace.add(testId+".setMacroAction");macro=m;}
 public String getActionLabel(){CoreTrace.add(testId+".label");return label;}
 public void invokeActionWithPermissionCheck(TriggerContextInfo c){CoreTrace.add(testId+".invokeWithPermission:"+EngineRuntime.id(c));executions++;EngineRuntime.effects.add(testId);if(macro!=null){if(cancelOnExecute||(cancelAtExecution>0&&executions>=cancelAtExecution))macro.m_cancelFlag=true;if(disableOnExecute)macro.engineEnabled=false;if(disableAppOnExecute)Macro.sMacroDroidEnabled=false;}}
}
