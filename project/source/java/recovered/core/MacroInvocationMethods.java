package recovered.core;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.Constraint;
import com.arlosoft.macrodroid.triggers.Trigger;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.action.WaitUntilTriggerAction;
import defpackage.rl9;
import defpackage.kjf;
/** Recovered from the original three canInvoke overloads. No policy is bypassed.
 * Disabled constraints are assigned their macro but not evaluated. No enabled
 * constraints means success even in OR mode. Logging order/wording is preserved.
 */
public final class MacroInvocationMethods {
 public static boolean canInvoke(Macro self, TriggerContextInfo context) {
  if (context != null) {
   WaitUntilTriggerAction pending = self.actionWaitingForTriggerActive;
   if (pending != null) {
    java.util.ArrayList triggers = pending.D0();
    if (triggers.contains(context.getTrigger())) return true;
   }
  }
  return self.canInvoke(context, false);
 }
 public static boolean canInvokeForced(Macro self, TriggerContextInfo context, boolean force) {
  return self.canInvoke(context, force, true);
 }
 public static boolean canInvokeChecked(Macro self, TriggerContextInfo context, boolean force, boolean log) {
  if (self.isActionBlock) return true;
  rl9 debugger = rl9.a;
  long debugGuid = self.getGUID();
  debugger.getClass();
  if (rl9.m(debugGuid)) {
   StringBuilder text = new StringBuilder();
   text.append(((SelectableItem)context.getTrigger()).getConfiguredName());
   text.append(" - skipping invocation (macro is currently being debugged): ");
   text.append(self.getName());
   String message = text.toString();
   long guid = self.getGUID();
   kjf.t(guid, message);
   return false;
  }
  if (!force && !Macro.sMacroDroidEnabled) return false;
  if (self.isCategoryDisabled()) return false;
  Trigger trigger = context == null ? null : context.getTrigger();
  if (self.m_constraintList.size() <= 0) return true;
  if (self.isConstraintOrCondition()) {
   int enabled = 0;
   boolean passed = false;
   String firstFailure = "";
   for (Object candidate : self.m_constraintList) {
    Constraint constraint = (Constraint) candidate;
    SelectableItem item = constraint;
    item.setMacro(self);
    if (!item.isEnabled()) continue;
    enabled++;
    if (constraint.X(context)) { passed = true; break; }
    if (firstFailure.isEmpty()) firstFailure = item.getConfiguredName();
   }
   if (!passed && !self.isDetailLoggingExcluded() && enabled > 0) {
    if (trigger != null) {
     if (self.m_constraintList.size() > 1) {
      for (Object candidate : self.m_constraintList) {
       if (((SelectableItem)(Constraint)candidate).isLoggingDisabled()) return false;
      }
      if (log) {
       StringBuilder text = new StringBuilder();
       text.append(((SelectableItem)trigger).getConfiguredName());
       text.append(" did not fire because no constraints were true (");
       text.append(firstFailure).append(")");
       kjf.c(text.toString(), Integer.valueOf(self.m_triggerList.indexOf(trigger)+1), self.getGUID());
      }
     } else if (self.m_constraintList.size() == 1) {
      if (!((SelectableItem)(Constraint)self.m_constraintList.get(0)).isLoggingDisabled() && log) {
       StringBuilder text = new StringBuilder();
       text.append(((SelectableItem)trigger).getConfiguredName());
       text.append(" did not fire because constraint failed: ");
       text.append(((SelectableItem)(Constraint)self.m_constraintList.get(0)).getConfiguredName());
       text.append(" (").append(self.getName()).append(")");
       kjf.c(text.toString(), Integer.valueOf(self.m_triggerList.indexOf(trigger)+1), self.getGUID());
      }
     }
    } else if (log) {
     StringBuilder text = new StringBuilder();
     text.append(self.getName()).append(" did not fire because no constraints were true (");
     text.append(firstFailure).append(")");
     kjf.c(text.toString(), Integer.valueOf(self.m_triggerList.indexOf(trigger)+1), self.getGUID());
    }
   }
   return enabled == 0 || passed;
  }
  int enabled = 0;
  for (Object candidate : self.m_constraintList) {
   Constraint constraint = (Constraint)candidate;
   SelectableItem item = constraint;
   item.setMacro(self);
   if (!item.isEnabled()) continue;
   enabled++;
   if (constraint.X(context)) continue;
   if (!self.isDetailLoggingExcluded() && enabled > 0) {
    if (trigger != null) {
     if (!item.isLoggingDisabled() && log) {
      StringBuilder text = new StringBuilder();
      text.append(((SelectableItem)trigger).getSystemLogEntryName(context));
      text.append(" did not fire because constraint failed: ");
      text.append(item.getSystemLogEntryName(context));
      text.append(" (").append(self.getName()).append(")");
      kjf.c(text.toString(), Integer.valueOf(self.m_triggerList.indexOf(trigger)+1), self.getGUID());
     }
    } else if (!item.isLoggingDisabled() && log) {
     StringBuilder text = new StringBuilder();
     text.append(self.getName()).append(" did not invoke because constraint failed: ");
     text.append(item.getSystemLogEntryName(context));
     text.append(" (").append(self.getName()).append(")");
     kjf.c(text.toString(), Integer.valueOf(self.m_triggerList.indexOf(trigger)+1), self.getGUID());
    }
   }
   return false;
  }
  return true;
 }
}
