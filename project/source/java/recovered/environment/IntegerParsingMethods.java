package recovered.environment;
import defpackage.bz9;
import defpackage.j68;

/** The original negative-accumulation parser, including Unicode Character.digit
 * behavior, overflow guards, optional sign and no whitespace trimming.
 */
public final class IntegerParsingMethods {
    public static Long parseLong(String text) {
        text.getClass();
        bz9.k(10);
        int length = text.length();
        if (length == 0) return null;
        int offset = 0;
        char first = text.charAt(0);
        long limit = -9223372036854775807L;
        boolean negative;
        if (j68.h(first, 48) < 0) {
            negative = true;
            if (length == 1) return null;
            if (first == '+') {
                negative = false;
                offset = 1;
            } else {
                if (first != '-') return null;
                limit = Long.MIN_VALUE;
                offset = 1;
            }
        } else {
            negative = false;
        }
        long value = 0L;
        long multiplyLimit = -256204778801521550L;
        while (offset < length) {
            int digit = Character.digit((int) text.charAt(offset), 10);
            if (digit < 0) return null;
            if (value < multiplyLimit) {
                if (multiplyLimit != -256204778801521550L) return null;
                multiplyLimit = limit / 10;
                if (value < multiplyLimit) return null;
            }
            long multiplied = value * 10;
            long digitValue = digit;
            if (multiplied < limit + digitValue) return null;
            value = multiplied - digitValue;
            offset++;
        }
        return Long.valueOf(negative ? value : -value);
    }
}
