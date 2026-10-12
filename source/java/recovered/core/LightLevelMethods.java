package recovered.core;
import com.arlosoft.macrodroid.constraint.LightLevelConstraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.kjf;
/** Strict threshold comparisons; NaN never satisfies either supported option. */
public final class LightLevelMethods {
 public static boolean evaluate(LightLevelConstraint self, TriggerContextInfo unused) {
  float threshold = self.m_lightLevel != -1 ? (float)self.m_lightLevel : self.m_lightLevelFloat;
  StringBuilder text = new StringBuilder("LightLevelConstraint: current value = ");
  text.append(LightLevelConstraint.s_lightLevel).append(", comparing to ");
  text.append(self.m_option == 0 ? "< " : "> ");
  text.append(self.m_lightLevel != -1 ? (float)self.m_lightLevel : self.m_lightLevelFloat);
  kjf.r(text.toString());
  int option = self.m_option;
  if (option == 0) return LightLevelConstraint.s_lightLevel < threshold;
  if (option == 1) return LightLevelConstraint.s_lightLevel > threshold;
  return false;
 }
}
