package com.arlosoft.macrodroid.macro;
import java.util.*;
import com.arlosoft.macrodroid.action.WaitUntilTriggerAction;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.CoreTrace;
public class Macro {
 public boolean isActionBlock, categoryDisabled, orMode, detailExcluded, running;
 public static boolean sMacroDroidEnabled=true;
 public List m_constraintList=new ArrayList(); public ArrayList m_triggerList=new ArrayList();
 public WaitUntilTriggerAction actionWaitingForTriggerActive;
 public long guid=51L; public String name="macro", testId="macro";
 public long getGUID(){CoreTrace.add(testId+".guid");return guid;}
 public String getName(){CoreTrace.add(testId+".name");return name;}
 public boolean isRunning(){CoreTrace.add(testId+".running");return running;}
 public boolean isCategoryDisabled(){CoreTrace.add(testId+".categoryDisabled");return categoryDisabled;}
 public boolean isConstraintOrCondition(){CoreTrace.add(testId+".orMode");return orMode;}
 public boolean isDetailLoggingExcluded(){CoreTrace.add(testId+".detailExcluded");return detailExcluded;}
 public boolean canInvoke(TriggerContextInfo c){return recovered.core.MacroInvocationMethods.canInvoke(this,c);}
 public boolean canInvoke(TriggerContextInfo c,boolean f){return recovered.core.MacroInvocationMethods.canInvokeForced(this,c,f);}
 public boolean canInvoke(TriggerContextInfo c,boolean f,boolean l){return recovered.core.MacroInvocationMethods.canInvokeChecked(this,c,f,l);}

 public com.arlosoft.macrodroid.action.ShellScriptAction activeShellScriptAction;
 public int m_invokeCount,starts,terminations,outputs;public long m_invokeStart=120000,m_GUID=51,disabledTimestamp,forceEvenIfNotEnabledTimestamp;
 public static long macroDroidDisabledTimeStamp;public java.util.Set breakpoints=new java.util.HashSet();public Object debugLock=new Object();
 public boolean m_cancelFlag,isClonedInstance,engineEnabled=true;public ArrayList m_actionList=new ArrayList();public TriggerContextInfo triggerContextInfo;
 public boolean isEnabled(){CoreTrace.add(testId+".engineEnabled");return engineEnabled;}
 public void startMacro(){CoreTrace.add(testId+".start");starts++;running=true;}
 public void terminateMacro(){CoreTrace.add(testId+".terminate");terminations++;running=false;}
 public void terminateMacro(boolean all){CoreTrace.add(testId+".terminate:"+all);terminations++;running=false;}
 public ArrayList getActions(){CoreTrace.add(testId+".actions");return m_actionList;}
 public void setTriggerContextInfo(TriggerContextInfo c){CoreTrace.add(testId+".setContext:"+defpackage.EngineRuntime.id(c));triggerContextInfo=c;}
 public void i(com.arlosoft.macrodroid.action.Action a,TriggerContextInfo c,int p){CoreTrace.add(testId+".logAction:"+defpackage.EngineRuntime.id(a)+":"+p+":"+defpackage.EngineRuntime.id(c));}
 public void j(com.arlosoft.macrodroid.action.LoopAction a,String x){CoreTrace.add(testId+".logLoop:"+defpackage.EngineRuntime.id(a)+":"+x);}
 public void e(){CoreTrace.add(testId+".blockTestSummary");}public void l(com.arlosoft.macrodroid.data.ResumeMacroInfo r){CoreTrace.add(testId+".outputs:"+defpackage.EngineRuntime.id(r));outputs++;}
 public void invokeActions(List a,int p,TriggerContextInfo c,boolean f,java.util.Stack s,com.arlosoft.macrodroid.data.ResumeMacroInfo r){defpackage.EngineRuntime.dispatch(this,a,p,c,f,s,r);}
 public static class b {public long a,b,c;public boolean d;public b(int n){CoreTrace.add("loopGuard.new:"+n);a=defpackage.EngineRuntime.initialGuardStart;b=defpackage.EngineRuntime.initialGuardLast;c=defpackage.EngineRuntime.initialGuardCount;d=defpackage.EngineRuntime.initialGuardWarned;}public boolean a(Macro m,com.arlosoft.macrodroid.action.LoopAction l){return recovered.engine.LoopGuardMethods.check(this,m,l);}}

}
