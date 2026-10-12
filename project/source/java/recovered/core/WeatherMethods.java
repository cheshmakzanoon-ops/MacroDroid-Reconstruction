package recovered.core;
import com.arlosoft.macrodroid.triggers.WeatherTrigger;
import com.arlosoft.macrodroid.data.b;
import defpackage.cah;
import java.util.HashSet;
/** Recovered threshold-crossing logic and the original weather-code groups. */
public final class WeatherMethods {
 public static int category(int code) {
  if (code >= 200 && code <= 232) return 3;
  if (code >= 300 && code <= 531) return 2;
  if (code >= 600 && code <= 622) return 4;
  if (code >= 800 && code <= 801) return 0;
  if (code >= 802 && code <= 804) return 1;
  return -1;
 }
 public static double temperature(cah self, boolean celsius) {
  double value = self.a - 273.15;
  if (celsius) return value;
  // Preserve each IEEE-754 rounding step; do not replace this with value * 1.8.
  return ((value * 9.0) / 5.0) + 32.0;
 }
 public static boolean crosses(WeatherTrigger self, b previous, b current) {
  switch (self.m_option) {
   case 0: {
    boolean below = self.m_tempBelow;
    cah reading = current.b;
    if (below) {
     if (!(reading.a(self.m_tempCelcius) <= (double)self.m_temperature)) return false;
     return previous == null || previous.b.a(self.m_tempCelcius) > (double)self.m_temperature;
    }
    if (!(reading.a(self.m_tempCelcius) >= (double)self.m_temperature)) return false;
    return previous == null || previous.b.a(self.m_tempCelcius) < (double)self.m_temperature;
   }
   case 1: {
    double threshold = (double)self.m_windSpeedValue;
    int mph = self.m_windSpeedValueMph;
    if (mph > 0) threshold = ((double)mph) / 2.23694;
    boolean above = self.m_windSpeedAbove;
    cah reading = current.c;
    if (above) return reading.a >= threshold && (previous == null || previous.c.a < threshold);
    return reading.a <= threshold && (previous == null || previous.c.a > threshold);
   }
   case 2: {
    boolean above = self.m_humidityAbove;
    int humidity = current.e;
    int threshold = self.m_humidityValue;
    if (above) return humidity >= threshold && (previous == null || previous.e < threshold);
    return humidity <= threshold && (previous == null || previous.e > threshold);
   }
   case 3: {
    HashSet<Integer> before = new HashSet<Integer>();
    HashSet<Integer> after = new HashSet<Integer>();
    if (previous != null) for (Object item : previous.a) before.add(Integer.valueOf(WeatherTrigger.x0(((b.a)item).a)));
    for (Object item : current.a) after.add(Integer.valueOf(WeatherTrigger.x0(((b.a)item).a)));
    return !before.contains(Integer.valueOf(self.m_weatherCondition)) && after.contains(Integer.valueOf(self.m_weatherCondition));
   }
   case 5: return previous == null || current.f != previous.f;
   default: return true;
  }
 }
}
