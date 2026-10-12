package recovered.probe;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;

/** Exact numeric input corpus on the real original/candidate APK classes.
 * This neutral probe defines no application or Android class. Reflection builds
 * only private disposable test objects. It installs no app and schedules no alarm.
 * --inventory prints inputs/expectations only and never loads application classes.
 */
public final class DayNumericMethodProbe {
    static final String BASE = "com.arlosoft.macrodroid.variables.VariableValue";
    static final String TARGET = "com.arlosoft.macrodroid.triggers.DayTrigger";
    static final String INVENTORY_SHA256 = "e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79";
    static String name(Object[] input) { return (String) input[0]; }
    static String kind(Object[] input) { return (String) input[1]; }
    static long bits(Object[] input) { return ((Number) input[2]).longValue(); }
    static String text(Object[] input) { return (String) input[3]; }
    static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
    static String hex(byte[] bytes) {
        StringBuilder value = new StringBuilder();
        for (byte item : bytes) value.append(String.format(Locale.ROOT, "%02x", item & 255));
        return value.toString();
    }
    static String sha(byte[] bytes) {
        try { return hex(MessageDigest.getInstance("SHA-256").digest(bytes)); }
        catch (java.security.NoSuchAlgorithmException error) { throw new AssertionError(error); }
    }
    static String inputJson(Object[] input) {
        String id = name(input), category = kind(input), value = text(input);
        require(id.matches("[a-z0-9.+-]+") && category.matches("[a-z-]+"), "Unexpected literal case name");
        require(value == null || value.matches("[0-9.]*"), "Unexpected numeric-corpus text");
        return "{\"case\":\"" + id + "\",\"kind\":\"" + category
            + "\",\"rawBitsHex\":\"" + String.format(Locale.ROOT, "%016x", bits(input)) + "\""
            + (value == null ? "" : ",\"text\":\"" + value + "\"") + "}";
    }
    static String inputInventorySha256(List<Object[]> inputs) {
        StringBuilder value = new StringBuilder("[");
        for (Object[] input : inputs) {
            if (value.length() != 1) value.append(',');
            value.append(inputJson(input));
        }
        return sha(value.append(']').toString().getBytes(StandardCharsets.UTF_8));
    }
    static String rawMessage(String message) {
        if (message == null) return "null";
        StringBuilder value = new StringBuilder("utf16:");
        for (int i = 0; i < message.length(); i++)
            value.append(String.format(Locale.ROOT, "%04x", (int) message.charAt(i)));
        return value.toString();
    }

    static Integer expected(Object[] input) {
        if (kind(input).equals("null-entry")) return null;
        if (kind(input).equals("integer")) {
            BigInteger unsigned = BigInteger.valueOf(bits(input)).mod(BigInteger.ONE.shiftLeft(32));
            return (unsigned.testBit(31) ? unsigned.subtract(BigInteger.ONE.shiftLeft(32)) : unsigned).intValueExact();
        }
        if (kind(input).equals("decimal")) {
            long bits = bits(input), exponent = (bits >>> 52) & 0x7ffL, fraction = bits & 0x000fffffffffffffL;
            boolean negative = bits < 0;
            if (exponent == 0x7ffL) return fraction != 0 ? 0 : negative ? Integer.MIN_VALUE : Integer.MAX_VALUE;
            BigInteger significand = BigInteger.valueOf(fraction);
            if (exponent != 0) significand = significand.setBit(52);
            int shift = Math.toIntExact((exponent == 0 ? 1 : exponent) - 1023 - 52);
            BigInteger magnitude = shift >= 0 ? significand.shiftLeft(shift) : significand.shiftRight(-shift);
            BigInteger signed = negative ? magnitude.negate() : magnitude;
            if (signed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) return Integer.MAX_VALUE;
            if (signed.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) return Integer.MIN_VALUE;
            return signed.intValueExact();
        }
        return 0;
    }

    static List<Object[]> cases() {
        List<Object[]> out = new ArrayList<>();
        long[] integers = {0, 1, -1, 2, -2, 127, 128, 255, 256, 32767, 32768, 65535, 65536,
            2147483646L, 2147483647L, 2147483648L, 2147483649L, -2147483647L, -2147483648L,
            -2147483649L, -2147483650L, 4294967295L, 4294967296L, 4294967297L, -4294967295L,
            -4294967296L, -4294967297L, 9007199254740991L, 9007199254740992L, 9007199254740993L,
            -9007199254740991L, -9007199254740992L, -9007199254740993L, Long.MAX_VALUE, Long.MIN_VALUE};
        for (int i = 0; i < integers.length; i++) out.add(new Object[]{"integer-boundary-" + i, "integer", integers[i], null});
        for (int bit = 0; bit < 64; bit++) {
            long value = 1L << bit;
            out.add(new Object[]{"integer-bit-" + bit, "integer", value, null});
            out.add(new Object[]{"integer-complement-" + bit, "integer", ~value, null});
        }
        Random random = new Random(0x567800896700008L);
        for (int i = 0; i < 384; i++) out.add(new Object[]{"integer-seeded-" + i, "integer", random.nextLong(), null});
        double[] decimals = {0.0d, -0.0d, 0.1d, -0.1d, 0.999d, -0.999d, 1.0d, -1.0d, 1.1d, -1.1d,
            1.5d, -1.5d, 1.9d, -1.9d, 2.9d, -2.9d, 2147483646.75d, 2147483647.0d, 2147483647.75d,
            2147483648.0d, -2147483647.75d, -2147483648.0d, -2147483648.75d, 4294967296.0d,
            -4294967296.0d, 9007199254740991.0d, -9007199254740991.0d, Double.MIN_VALUE,
            -Double.MIN_VALUE, Double.MIN_NORMAL, -Double.MIN_NORMAL, Double.MAX_VALUE, -Double.MAX_VALUE,
            Double.POSITIVE_INFINITY, Double.NEGATIVE_INFINITY, Double.NaN};
        for (int i = 0; i < decimals.length; i++) out.add(new Object[]{"decimal-boundary-" + i, "decimal", Double.doubleToRawLongBits(decimals[i]), null});
        for (double pivot : new double[]{-2147483649d, -2147483648d, -2147483647d, -2d, -1d, 0d, 1d, 2d, 2147483646d, 2147483647d, 2147483648d}) {
            double value = pivot;
            for (int i = 0; i < 8; i++) {
                value = Math.nextDown(value);
                out.add(new Object[]{"decimal-next-down-" + Double.toHexString(pivot) + "-" + i, "decimal", Double.doubleToRawLongBits(value), null});
            }
            value = pivot;
            for (int i = 0; i < 8; i++) {
                value = Math.nextUp(value);
                out.add(new Object[]{"decimal-next-up-" + Double.toHexString(pivot) + "-" + i, "decimal", Double.doubleToRawLongBits(value), null});
            }
        }
        long[] special = {1L, 0x8000000000000001L, 0x000fffffffffffffL, 0x800fffffffffffffL,
            0x7ff0000000000001L, 0x7ff8000000000001L, 0x7fffffffffffffffL,
            0xfff0000000000001L, 0xfff8000000000001L, 0xffffffffffffffffL};
        for (int i = 0; i < special.length; i++) out.add(new Object[]{"decimal-special-bits-" + i, "decimal", special[i], null});
        for (int i = 0; i < 512; i++) out.add(new Object[]{"decimal-seeded-bits-" + i, "decimal", random.nextLong(), null});
        out.add(new Object[]{"null-entry", "null-entry", 0, null});
        out.add(new Object[]{"null-value", "null-value", 0, null});
        out.add(new Object[]{"string-numeric", "string", 0, "27"});
        out.add(new Object[]{"string-decimal", "string", 0, "1.9"});
        out.add(new Object[]{"string-empty", "string", 0, ""});
        out.add(new Object[]{"string-null", "string", 0, null});
        out.add(new Object[]{"boolean-false", "boolean", 0, null});
        out.add(new Object[]{"boolean-true", "boolean", 1, null});
        out.add(new Object[]{"dictionary", "dictionary", 0, null});
        out.add(new Object[]{"nested-entry", "nested-entry", 91, null});
        Set<String> names = new HashSet<String>();
        for (Object[] input : out) require(names.add(name(input)), "Duplicate case identifiers");
        require(out.size() == 1291 && inputInventorySha256(out).equals(INVENTORY_SHA256), "Numeric case inventory changed");
        return out;
    }

    static Class<?> ownedType(String name, ClassLoader expected) throws Exception {
        Class<?> value = Class.forName(name);
        require(value.getName().equals(name) && value.getClassLoader() == expected,
                "Application type is not from the same actual APK classpath: " + name);
        return value;
    }
    static Object entry(Object[] input, Class<?> valueType, Class<?> entryType,
                        Class<?> integerType, Class<?> decimalType, Class<?> stringType,
                        Class<?> booleanType, Class<?> dictionaryType) throws Exception {
        if (kind(input).equals("null-entry")) return null;
        Object value;
        String category = kind(input);
        if (category.equals("integer")) {
            value = integerType.getConstructor(long.class, List.class).newInstance(bits(input), null);
            long observed = ((Long) integerType.getMethod("getIntValue").invoke(value)).longValue();
            require(observed == bits(input), "Integer input bits changed: " + name(input));
        } else if (category.equals("decimal")) {
            value = decimalType.getConstructor(double.class, List.class)
                .newInstance(Double.longBitsToDouble(bits(input)), null);
            double observed = ((Double) decimalType.getMethod("getDecimalValue").invoke(value)).doubleValue();
            require(Double.doubleToRawLongBits(observed) == bits(input), "Decimal input bits changed: " + name(input));
        } else if (category.equals("string")) {
            value = stringType.getConstructor(String.class, List.class)
                .newInstance(text(input) == null ? "" : text(input), null);
            if (text(input) == null) {
                // The host corpus includes an otherwise invalid null text field.
                // Set it only in this new disposable object, then read it back.
                Field field = stringType.getDeclaredField("textValue");
                field.setAccessible(true);
                field.set(value, null);
                require(field.get(value) == null, "Explicit null-text fixture was not constructed");
            }
        } else if (category.equals("boolean")) {
            value = booleanType.getConstructor(boolean.class, List.class).newInstance(bits(input) != 0, null);
        } else if (category.equals("dictionary")) {
            value = dictionaryType.getConstructor(List.class, boolean.class, List.class)
                .newInstance(new ArrayList<Object>(), false, null);
        } else if (category.equals("nested-entry")) {
            Object nested = integerType.getConstructor(long.class, List.class).newInstance(bits(input), null);
            value = entryType.getConstructor(String.class, valueType, List.class).newInstance("nested", nested, null);
        } else if (category.equals("null-value")) {
            value = integerType.getConstructor(long.class, List.class).newInstance(0L, null);
        } else throw new IllegalArgumentException(category);
        Constructor<?> constructor = entryType.getConstructor(String.class, valueType, List.class);
        Object result = constructor.newInstance("numeric", value, null);
        if (category.equals("null-value")) {
            // The real constructor rejects null. This deliberately injected
            // heap state tests the already declared null-contained-value case.
            Field field = entryType.getDeclaredField("variable");
            field.setAccessible(true);
            field.set(result, null);
            value = null;
        }
        require(entryType.getMethod("getVariable").invoke(result) == value,
                "Exact contained input identity differs: " + name(input));
        return result;
    }
    public static void main(String[] args) throws Exception {
        List<Object[]> inputs = cases();
        if (args.length == 1 && args[0].equals("--inventory")) {
            System.out.println("DAY_NUMERIC_INPUTS_BEGIN\tcases=1291\tsha256=" + INVENTORY_SHA256);
            for (Object[] input : inputs)
                System.out.println(inputJson(input) + "\t" + (expected(input) == null
                    ? "exception:java.lang.NullPointerException" : "value:" + expected(input)));
            System.out.println("DAY_NUMERIC_INPUTS_END\tcases=1291\tandroid_executed=false");
            return;
        }
        require(args.length == 0, "No runtime argument or case selection is allowed");
        Class<?> target = Class.forName(TARGET);
        ClassLoader loader = target.getClassLoader();
        require(loader != null, "Application class must not be a bootstrap substitute");
        Class<?> valueType = ownedType(BASE, loader), entryType = ownedType(BASE + "$DictionaryEntry", loader),
            integerType = ownedType(BASE + "$IntegerValue", loader), decimalType = ownedType(BASE + "$DecimalValue", loader),
            stringType = ownedType(BASE + "$StringValue", loader), booleanType = ownedType(BASE + "$BooleanValue", loader),
            dictionaryType = ownedType(BASE + "$Dictionary", loader);
        Method method = target.getDeclaredMethod("r0", entryType);
        require(method.getDeclaringClass() == target && Modifier.isStatic(method.getModifiers())
                && Modifier.isPublic(method.getModifiers()) && method.getReturnType() == int.class,
                "The exact public static r0(DictionaryEntry):int method is required");
        System.out.println("DAY_NUMERIC_ART_BEGIN\tcases=1291\tsha256=" + INVENTORY_SHA256);
        int index = 0;
        for (Object[] input : inputs) {
            Object argument = entry(input, valueType, entryType, integerType, decimalType, stringType, booleanType, dictionaryType);
            String prefix = "DAY_NUMERIC_ART_CASE\t" + index + "\t" + name(input) + "\t" + kind(input)
                + "\t" + String.format(Locale.ROOT, "%016x", bits(input));
            try {
                Object observed = method.invoke(null, argument);
                require(observed instanceof Integer && expected(input) != null
                        && expected(input).equals(observed), "Numeric value mismatch: " + name(input));
                System.out.println(prefix + "\tvalue\t" + observed);
            } catch (InvocationTargetException wrapper) {
                Throwable cause = wrapper.getCause();
                require(kind(input).equals("null-entry") && cause != null
                        && cause.getClass() == NullPointerException.class,
                        "Unexpected target exception: " + name(input) + " " + cause);
                System.out.println(prefix + "\texception\t" + cause.getClass().getName() + "\t" + rawMessage(cause.getMessage()));
            }
            index++;
        }
        require(index == 1291, "Incomplete input corpus");
        System.out.println("DAY_NUMERIC_ART_END\tcases=1291\tpassed=true");
    }
}
