package recovered.core;
import com.arlosoft.macrodroid.variables.s0;
import com.arlosoft.macrodroid.events.ShowActionBlockTestSummaryEvent;
import defpackage.j68;
/** Preserve identity shortcuts and original null-sensitive vs null-safe fields. */
public final class ValueEqualityMethods {
 public static boolean variable(s0 self, Object other) {
  if (self == other) return true;
  if (!(other instanceof s0)) return false;
  s0 value = (s0)other;
  if (!self.a.equals(value.a)) return false;
  if (!((Object)self.b).equals(value.b)) return false;
  return self.c == value.c;
 }
 public static boolean summary(ShowActionBlockTestSummaryEvent self, Object other) {
  if (self == other) return true;
  if (!(other instanceof ShowActionBlockTestSummaryEvent)) return false;
  ShowActionBlockTestSummaryEvent value = (ShowActionBlockTestSummaryEvent)other;
  if (self.a != value.a) return false;
  if (!j68.d(self.b, value.b)) return false;
  return j68.d(self.c, value.c);
 }
}
