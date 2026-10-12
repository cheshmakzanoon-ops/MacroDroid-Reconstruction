package recovered.environment;
import defpackage.yih;
import defpackage.kjf;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

/** Recovered wildcard/regular-expression pipeline. Locale-sensitive lowercase,
 * find versus matches, escaping order, and PatternSyntaxException handling are retained.
 */
public final class MatchingMethods {
    public static String containsPattern(String text, boolean ignoreCase) {
        if (ignoreCase) text = text.toLowerCase();
        return "(?s)".concat(".*").concat(yih.a.matcher(text).replaceAll("\\\\$0")
                .replace("*", ".*").replace("..*", ".*").replace("?", ".").concat(".*"));
    }
    public static String contains(String text, boolean regex, boolean ignoreCase) {
        if (text.isEmpty()) return "";
        return regex ? "(?s)".concat(text) : yih.a(text, ignoreCase);
    }
    public static String full(String text, boolean regex, boolean ignoreCase) {
        if (text.isEmpty()) return "";
        if (regex) return "(?s)".concat(text);
        if (text.isEmpty()) return "";
        if (ignoreCase) text = text.toLowerCase();
        return "(?s)".concat(yih.a.matcher(text).replaceAll("\\\\$0")
                .replace("*", ".*").replace("..*", ".*").replace("?", "."));
    }
    public static boolean matches(String text, String pattern, boolean regex, boolean ignoreCase) {
        if (regex) {
            try {
                return Pattern.compile(pattern).matcher(text).find();
            } catch (PatternSyntaxException failure) {
                kjf.l("Error with regex, you may need to escape a special character (for example if matching the + character then you should write \\+) : " + failure);
                return false;
            }
        }
        if (ignoreCase) text = text.toLowerCase();
        try {
            return text.matches(pattern);
        } catch (PatternSyntaxException failure) {
            kjf.l("Error with regex, you may need to escape a special character (for example if matching the + character then you should write \\+) : " + failure);
            return false;
        }
    }
}
