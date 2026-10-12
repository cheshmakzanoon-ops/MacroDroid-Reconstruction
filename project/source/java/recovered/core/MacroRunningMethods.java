package recovered.core;
import android.content.Context;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.MacroRunningConstraint;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.macro.b;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.sr9;
import defpackage.yih;
import defpackage.vq9;
import defpackage.kjf;
/** Preserve first name match, self-macro sentinel, ID/name fallback, and errors. */
public final class MacroRunningMethods {
 public static boolean evaluate(MacroRunningConstraint self, TriggerContextInfo context) {
  if (self.textToMatch != null) {
   Context androidContext = ((SelectableItem)self).getContext();
   androidContext.getClass();
   String input = self.textToMatch;
   Macro owner = ((SelectableItem)self).getMacro();
   String expanded = sr9.l(androidContext, owner, context, input);
   String pattern = self.matchOption == 0 ? yih.b(expanded, false, false) : yih.c(expanded, false, false);
   Macro found = null;
   for (Object candidate : b.k.a().w(true)) {
    Macro macro = (Macro) candidate;
    if (yih.d(macro.getName(), pattern, false, false)) { found = macro; break; }
   }
   if (self.option == 0) return found != null && found.isRunning();
   return found == null || !found.isRunning();
  }
  if (self.macroId == -1L) {
   // Both branches retain the original explicit null check before isRunning().
   if (self.option == 0) {
    Macro macro = ((SelectableItem)self).getMacro();
    macro.getClass();
    return macro.isRunning();
   }
   Macro macro = ((SelectableItem)self).getMacro();
   macro.getClass();
   return !macro.isRunning();
  }
  vq9 provider = b.k;
  Macro macro = provider.a().J(self.macroId);
  if (macro != null) return self.option == 0 ? macro.isRunning() : !macro.isRunning();
  macro = provider.a().L(self.macroName);
  if (macro != null) return self.option == 0 ? macro.isRunning() : !macro.isRunning();
  long missingId = self.macroId;
  String missingName = self.macroName;
  StringBuilder text = new StringBuilder("Macro Running constraint could not find macro with id: ");
  text.append(missingId).append(" and name: ").append(missingName);
  kjf.h(text.toString());
  return false;
 }
}
