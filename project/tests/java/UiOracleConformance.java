import java.nio.file.*;
import java.util.*;
import com.google.gson.*;
/** Bounded AOSP float-to-int conversion checks; no ART execution. */
public final class UiOracleConformance {
    static int cases;
    static void one(BytecodeOracle oracle, float value, int expected)throws Throwable {
        Object actual=oracle.invoke("LUiNumericProbe;->narrow(F)I",value);
        cases++;if(!Integer.valueOf(expected).equals(actual))throw new AssertionError(Integer.toHexString(Float.floatToRawIntBits(value))+":"+actual+" != "+expected);
        for(int anchor:new int[]{Integer.MIN_VALUE,-1,0,1,Integer.MAX_VALUE}){
            int result=expected-anchor;actual=oracle.invoke("LUiNumericProbe;->delta(FI)I",value,anchor);
            cases++;if(!Integer.valueOf(result).equals(actual))throw new AssertionError("cast/subtract ordering");
        }
    }
    public static void main(String[] args)throws Throwable {
        Path root=Paths.get(args[0]);BytecodeOracle oracle=new BytecodeOracle(root.resolve("build/ui-opcodes.dex"),Set.of("LUiNumericProbe;->narrow(F)I","LUiNumericProbe;->delta(FI)I"));
        float[] values={Float.NaN,Float.POSITIVE_INFINITY,Float.NEGATIVE_INFINITY,0f,-0f,Float.MIN_VALUE,-Float.MIN_VALUE,0.99f,-0.99f,1.99f,-1.99f,2147483648f,-2147483648f,2147483520f,-2147483520f,Float.MAX_VALUE,-Float.MAX_VALUE};
        int[] expected={0,Integer.MAX_VALUE,Integer.MIN_VALUE,0,0,0,0,0,0,1,-1,Integer.MAX_VALUE,Integer.MIN_VALUE,2147483520,-2147483520,Integer.MAX_VALUE,Integer.MIN_VALUE};
        for(int i=0;i<values.length;i++)one(oracle,values[i],expected[i]);
        for(int bits:new int[]{0x7f800001,0x7fc00001,0xff800001,0xffc00001})one(oracle,Float.intBitsToFloat(bits),0);
        Random random=new Random(923411);for(int i=0;i<1024;i++){
            float value=Float.intBitsToFloat(random.nextInt());
            // Reference is a independently specified saturating/truncating rule.
            int result=Float.isNaN(value)?0:value>=2147483648d?Integer.MAX_VALUE:value<=-2147483648d?Integer.MIN_VALUE:(int)(value<0?Math.ceil((double)value):Math.floor((double)value));
            one(oracle,value,result);
        }
        JsonObject r=new JsonObject();r.addProperty("passed",true);r.addProperty("cases",cases);r.addProperty("fixedExpectedValues",21);r.addProperty("androidRuntime",false);r.addProperty("specification","https://source.android.com/docs/core/runtime/dalvik-bytecode");
        Files.writeString(root.resolve("reports/ui-oracle-semantics.json"),new GsonBuilder().setPrettyPrinting().create().toJson(r));System.out.println(r);
    }
}
