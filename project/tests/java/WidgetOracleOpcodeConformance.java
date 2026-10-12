import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Independent truth-table checks of the original Widget high-bit operation. */
public final class WidgetOracleOpcodeConformance {
    static int expected(int left, int right) {
        long x = Integer.toUnsignedLong(left), y = Integer.toUnsignedLong(right), place = 1, result = 0;
        for (int bit = 0; bit < 32; bit++) {
            if ((x / place) % 2 == 1 && (y / place) % 2 == 1) result += place;
            place *= 2;
        }
        return (int) result;
    }
    static void require(boolean ok, String label) { if (!ok) throw new AssertionError(label); }
    public static void main(String[] args) throws Throwable {
        Set<String> keys = Set.of("LWidgetBitwiseProbe;->ordinary(II)I", "LWidgetBitwiseProbe;->leftAlias(II)I", "LWidgetBitwiseProbe;->rightAlias(II)I", "LWidgetBitwiseProbe;->highBit(I)I");
        BytecodeOracle oracle = new BytecodeOracle(Paths.get(args[0]), keys);
        int[] values = {0, 1, -1, 2, -2, Integer.MIN_VALUE, Integer.MAX_VALUE, 0x80000001, 0x7ffffffe, 0x55555555, 0xaaaaaaaa, 0x01010101, 0x80808080, 0x0000ffff, 0xffff0000, 0x00ff00ff, 0xff00ff00, 0x40000000, 0xc0000000, 0x12345678, 0x87654321, 0x00000100};
        int cases = 0;
        for (String method : new String[]{"ordinary", "leftAlias", "rightAlias"}) {
            String key = "LWidgetBitwiseProbe;->" + method + "(II)I";
            for (int left : values) for (int right : values) {
                require(((Integer) oracle.invoke(key, left, right)) == expected(left, right), method + " boundary " + left + ":" + right);
                cases++;
            }
            for (int first = 0; first < 32; first++) for (int second = 0; second < 32; second++) {
                int left = (int) (1L << first), right = (int) (1L << second);
                require(((Integer) oracle.invoke(key, left, right)) == (first == second ? left : 0), method + " bit truth table " + first + ":" + second);
                cases++;
            }
        }
        for (int value : values) {
            require(((Integer) oracle.invoke("LWidgetBitwiseProbe;->highBit(I)I", value)) == (value < 0 ? Integer.MIN_VALUE : 0), "continuation high bit " + value);
            cases++;
        }
        require(oracle.parentConstructorAdapters.isEmpty() && oracle.parentConstructorAdapterCalls.isEmpty(), "numeric operation used constructor adapters");
        JsonObject report = new JsonObject(); report.addProperty("passed", true); report.addProperty("cases", cases);
        report.addProperty("androidRuntime", false); report.addProperty("threeRegisterAndInt", true);
        report.addProperty("leftAndRightDestinationAliases", true); report.addProperty("all32BitTruthTablePairs", true);
        report.addProperty("signedContinuationHighBit", true); report.addProperty("expectedValuesUseIndependentPerBitArithmetic", true);
        report.addProperty("scope", "Explicit synthetic AND_INT numeric semantics; no application or ART execution");
        Files.writeString(Paths.get(args[1]), new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        System.out.println("Widget bitwise oracle conformance passed=" + cases);
    }
}
