package recovered.environment;

import defpackage.n7b;
import defpackage.g94;
import defpackage.srh;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.Calendar;
import java.util.TimeZone;

/** Recovered solar-hour calculations, not a replacement astronomical model.
 * Four-decimal HALF_EVEN rounding, BigDecimal(double) construction, arithmetic
 * order, daylight adjustment, and the original out-of-range behavior are retained.
 */
public final class SolarMethods {
    public static BigDecimal round(BigDecimal value) {
        return value.setScale(4, RoundingMode.HALF_EVEN);
    }
    public static BigDecimal radians(BigDecimal degrees) {
        return n7b.M(degrees.multiply(BigDecimal.valueOf(0.017453292519943295d)));
    }
    public static Calendar toCalendar(BigDecimal hour, Calendar base) {
        if (hour == null) return null;
        Calendar result = (Calendar) base.clone();
        BigDecimal minutes = BigDecimal.ZERO;
        if (hour.compareTo(minutes) == -1) {
            hour = hour.add(BigDecimal.valueOf(24.0d));
            result.add(11, -24);
        }
        String[] parts = hour.toPlainString().split("\\.");
        int hours = Integer.parseInt(parts[0]);
        BigDecimal roundedMinutes = new BigDecimal("0." + parts[1])
                .multiply(BigDecimal.valueOf(60L)).setScale(0, RoundingMode.HALF_EVEN);
        if (roundedMinutes.intValue() == 60) {
            hours++;
        } else {
            minutes = roundedMinutes;
        }
        if (hours == 24) hours = 0;
        result.set(11, hours);
        result.set(12, minutes.intValue());
        result.set(13, 0);
        result.set(14, 0);
        result.setTimeZone(base.getTimeZone());
        return result;
    }

    public static BigDecimal hour(n7b self, srh zenith, Calendar day, boolean sunrise) {
        g94 coordinates = (g94) self.b;
        TimeZone zone = (TimeZone) self.c;
        day.setTimeZone(zone);
        BigDecimal approximateHour = BigDecimal.valueOf(sunrise ? 6L : 18L);
        BigDecimal longitude = (BigDecimal) coordinates.c;
        RoundingMode rounding = RoundingMode.HALF_EVEN;
        BigDecimal time = n7b.M(new BigDecimal(day.get(6)).add(approximateHour
                .subtract(longitude.divide(BigDecimal.valueOf(15L), 4, rounding))
                .divide(BigDecimal.valueOf(24L), 4, rounding)));
        BigDecimal anomaly = n7b.M(n7b.M(new BigDecimal("0.9856").multiply(time))
                .subtract(new BigDecimal("3.289")));
        BigDecimal sinAnomaly = new BigDecimal(Math.sin(n7b.z(anomaly).doubleValue()));
        BigDecimal sinDoubleAnomaly = new BigDecimal(Math.sin(n7b.M(n7b.z(anomaly)
                .multiply(BigDecimal.valueOf(2L))).doubleValue()));
        BigDecimal trueLongitude = anomaly.add(n7b.M(sinAnomaly.multiply(new BigDecimal("1.916"))))
                .add(n7b.M(sinDoubleAnomaly.multiply(new BigDecimal("0.020")))
                        .add(new BigDecimal("282.634")));
        if (trueLongitude.doubleValue() > 360.0d) {
            trueLongitude = trueLongitude.subtract(BigDecimal.valueOf(360L));
        }
        trueLongitude = n7b.M(trueLongitude);
        BigDecimal sinDeclination = n7b.M(BigDecimal.valueOf(Math.sin(n7b.z(trueLongitude).doubleValue()))
                .multiply(new BigDecimal("0.39782")));
        BigDecimal cosDeclination = n7b.M(BigDecimal.valueOf(Math.cos(
                BigDecimal.valueOf(Math.asin(sinDeclination.doubleValue())).doubleValue())));
        BigDecimal zenithCosine = BigDecimal.valueOf(Math.cos(n7b.z(zenith.a).doubleValue()));
        BigDecimal latitude = (BigDecimal) coordinates.b;
        BigDecimal cosHour = n7b.M(zenithCosine.subtract(sinDeclination
                .multiply(BigDecimal.valueOf(Math.sin(n7b.z(latitude).doubleValue()))))
                .divide(cosDeclination.multiply(BigDecimal.valueOf(Math.cos(n7b.z(latitude).doubleValue()))),
                        4, rounding));
        if (cosHour.doubleValue() < -1.0d || cosHour.doubleValue() > 1.0d) return null;
        BigDecimal hourAngle = n7b.M(n7b.M(BigDecimal.valueOf(Math.acos(cosHour.doubleValue())))
                .multiply(new BigDecimal(57.29577951308232d)));
        if (sunrise) hourAngle = BigDecimal.valueOf(360L).subtract(hourAngle);
        BigDecimal hourAngleHours = hourAngle.divide(BigDecimal.valueOf(15L), 4, rounding);
        BigDecimal rightAscension = n7b.M(n7b.M(new BigDecimal(Math.atan(n7b.z(n7b.M(n7b.M(
                new BigDecimal(Math.tan(n7b.z(trueLongitude).doubleValue()))
                        .multiply(new BigDecimal(57.29577951308232d)))
                .multiply(new BigDecimal("0.91764")))).doubleValue()))
                .multiply(new BigDecimal(57.29577951308232d))));
        if (rightAscension.doubleValue() < 0.0d) {
            rightAscension = rightAscension.add(BigDecimal.valueOf(360L));
        } else if (rightAscension.doubleValue() > 360.0d) {
            rightAscension = rightAscension.subtract(BigDecimal.valueOf(360L));
        }
        BigDecimal quadrant = BigDecimal.valueOf(90L);
        BigDecimal localTime = hourAngleHours.add(rightAscension.add(trueLongitude
                .divide(quadrant, 0, RoundingMode.FLOOR).multiply(quadrant)
                .subtract(rightAscension.divide(quadrant, 0, RoundingMode.FLOOR).multiply(quadrant)))
                .divide(BigDecimal.valueOf(15L), 4, rounding))
                .subtract(time.multiply(new BigDecimal("0.06571"))).subtract(new BigDecimal("6.622"));
        if (localTime.doubleValue() < 0.0d) {
            localTime = localTime.add(BigDecimal.valueOf(24L));
        } else if (localTime.doubleValue() > 24.0d) {
            localTime = localTime.subtract(BigDecimal.valueOf(24L));
        }
        BigDecimal result = n7b.M(localTime)
                .subtract(((BigDecimal) coordinates.c).divide(BigDecimal.valueOf(15L), 4, rounding))
                .add(new BigDecimal(day.get(15)).divide(new BigDecimal(3600000), new MathContext(2)));
        if (zone.inDaylightTime(day.getTime())) result = result.add(BigDecimal.ONE);
        return result.doubleValue() > 24.0d ? result.subtract(BigDecimal.valueOf(24L)) : result;
    }
}
