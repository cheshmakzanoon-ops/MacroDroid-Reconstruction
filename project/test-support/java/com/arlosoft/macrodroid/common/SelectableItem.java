package com.arlosoft.macrodroid.common;
import android.content.Context;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.CoreTrace;
public class SelectableItem {
 public String testId="item", configured="configured", system="system";
 public boolean enabled=true, loggingDisabled;
 public Macro macro;
 public Context context = new Context();
 public String getConfiguredName(){CoreTrace.add(testId+".configured");return configured;}
 public String getSystemLogEntryName(TriggerContextInfo c){CoreTrace.add(testId+".system");return system;}
 public void setMacro(Macro m){CoreTrace.add(testId+".setMacro");macro=m;}
 public boolean isEnabled(){CoreTrace.add(testId+".enabled");return enabled;}
 public boolean isLoggingDisabled(){CoreTrace.add(testId+".loggingDisabled");return loggingDisabled;}
 public Context getContext(){CoreTrace.add(testId+".context");return context;}
 public Macro getMacro(){CoreTrace.add(testId+".macro");return macro;}
 public Long macroGuid=42L;
 public java.util.Map<String,String> expansions=new java.util.HashMap<String,String>();
 public String expansionFailureInput;public RuntimeException expansionFailure;
 public Long getMacroGuid(){CoreTrace.add(testId+".macroGuid");return macroGuid;}
 public String applyMagicText(String text,TriggerContextInfo info){CoreTrace.add(testId+".magic:"+text);if(expansionFailure!=null&&java.util.Objects.equals(expansionFailureInput,text))throw expansionFailure;return expansions.containsKey(text)?expansions.get(text):text;}

 public java.util.ArrayList engineConstraints=new java.util.ArrayList();public boolean engineResult=true;
 public java.util.ArrayDeque<Boolean> engineAnswers=new java.util.ArrayDeque<Boolean>();
 public java.util.Map<String,MacroDroidVariable> engineVariables=new java.util.HashMap<String,MacroDroidVariable>();
 public boolean constraintsMet(TriggerContextInfo c){CoreTrace.add(testId+".constraints:"+defpackage.EngineRuntime.id(c));return engineAnswers.isEmpty()?engineResult:engineAnswers.removeFirst();}
 public boolean constraintsMet(TriggerContextInfo c,boolean d){CoreTrace.add(testId+".constraintsDetailed:"+d+":"+defpackage.EngineRuntime.id(c));return engineAnswers.isEmpty()?engineResult:engineAnswers.removeFirst();}
 public java.util.List getConstraints(){CoreTrace.add(testId+".constraintsList");return engineConstraints;}
 public MacroDroidVariable getVariableByName(String n){CoreTrace.add(testId+".variable:"+n);return engineVariables.get(n);}


 public static String getString(int id) { defpackage.UiTrace.add("resource:"+id); defpackage.UiTrace.raise(defpackage.UiTrace.resourceFailure); return defpackage.UiTrace.resource; }
}
