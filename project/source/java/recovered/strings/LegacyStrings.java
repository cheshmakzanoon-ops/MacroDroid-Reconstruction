package recovered.strings;
/** Algorithms reconstructed from vdg.h0/u0 and q77.B in the supplied DEX. */
public final class LegacyStrings {
    private LegacyStrings() {}
    public static String decodeEscapedNewlines(String input) {
        input.getClass();
        StringBuilder out = new StringBuilder(input.length());
        int i = 0;
        while (i < input.length()) {
            // Two backslashes followed by n mean a literal backslash-n, not a line feed.
            if (i + 3 <= input.length() && input.charAt(i) == '\\'
                    && input.charAt(i + 1) == '\\' && input.charAt(i + 2) == 'n') {
                out.append("\\n");
                i += 3;
            } else if (i + 2 <= input.length() && input.charAt(i) == '\\'
                    && input.charAt(i + 1) == 'n') {
                out.append('\n');
                i += 2;
            } else {
                out.append(input.charAt(i));
                i++;
            }
        }
        return out.toString();
    }
    public static String removeDirectionMarks(String input) {
        input.getClass();
        return new defpackage.aqc("[\\u200E\\u202A\\u202C]").g(input, "");
    }
    public static String appendSuffix(String a, String b, StringBuilder builder) {
        builder.append(a);
        builder.append(b);
        return builder.toString();
    }
}
