import java.nio.file.*;
import java.util.*;
import com.google.gson.*;
/** Small executable opcode fixtures checked against explicit AOSP semantics, not
 * against the reconstructed application's own Java. Never packaged in the APK. */
public final class OracleSemanticsTests {
 static BytecodeOracle oracle;static int cases;
 static Object run(String name,Object... args)throws Throwable{return oracle.invoke("Loracle/Primitives;->"+name,args);}
 static void equal(Object a,Object b){cases++;if(a instanceof Double&&b instanceof Double){if(Double.doubleToLongBits((Double)a)==Double.doubleToLongBits((Double)b))return;}else if(a instanceof Float&&b instanceof Float){if(Float.floatToIntBits((Float)a)==Float.floatToIntBits((Float)b))return;}else if(Objects.equals(a,b))return;throw new AssertionError("expected "+b+" actual "+a);}
 static int comparison(double x,double y,int nan){if(Double.isNaN(x)||Double.isNaN(y))return nan;return x>y?1:x<y?-1:0;}
 public static void main(String[] args)throws Throwable{
  Path root=Paths.get(args[0]);String[] names={"cmplFloat(FF)I","cmpgFloat(FF)I","cmplDouble(DD)I","cmpgDouble(DD)I","compareLong(JJ)I","asFloat(I)F","asDouble(I)D","arithmetic(DD)D","xor(II)I","negativeZeroFloat()F","negativeZeroDouble()D","uninitialized()I","unsupported(I)I"};Set<String> keys=new HashSet<>();for(String n:names)keys.add("Loracle/Primitives;->"+n);for(String operation:new String[]{"add","sub","mul","div"})for(String suffix:new String[]{"","2"})keys.add("Loracle/Primitives;->"+operation+"Long"+suffix+"(JJ)J");
  for(String name:new String[]{"negLong(J)J","asChar(I)C","longAsInt(J)I","doubleAsLong(D)J","subtractInt(II)I","subtractInt2(II)I"})keys.add("Loracle/Primitives;->"+name);
  oracle=new BytecodeOracle(root.resolve("build/oracle-conformance.dex"),keys);
  double[] d={Double.NEGATIVE_INFINITY,-Double.MAX_VALUE,-1.0,-0.0,0.0,Double.MIN_VALUE,Math.nextDown(1.0),1.0,Math.nextUp(1.0),Double.MAX_VALUE,Double.POSITIVE_INFINITY,Double.NaN,Double.longBitsToDouble(0xfff8000000000001L)};
  for(double x:d)for(double y:d){equal(run(names[2],x,y),comparison(x,y,-1));equal(run(names[3],x,y),comparison(x,y,1));equal(run(names[7],x,y),(((x-y)*y)/x)+x);}
  float[] f={Float.NEGATIVE_INFINITY,-Float.MAX_VALUE,-1f,-0f,0f,Float.MIN_VALUE,Math.nextDown(1f),1f,Math.nextUp(1f),Float.MAX_VALUE,Float.POSITIVE_INFINITY,Float.NaN};
  for(float x:f)for(float y:f){equal(run(names[0],x,y),comparison(x,y,-1));equal(run(names[1],x,y),comparison(x,y,1));}
  long[] l={Long.MIN_VALUE,Long.MIN_VALUE+1,-1L,0L,1L,Long.MAX_VALUE-1,Long.MAX_VALUE};for(long x:l)for(long y:l)equal(run(names[4],x,y),Long.compare(x,y));
  int[] n={Integer.MIN_VALUE,Integer.MIN_VALUE+1,-16777217,-1,0,1,16777217,Integer.MAX_VALUE};for(int x:n){equal(run(names[5],x),(float)x);equal(run(names[6],x),(double)x);for(int y:n)equal(run(names[8],x,y),x^y);}
  equal(run(names[9]),-0.0f);equal(run(names[10]),-0.0d);
  for(String name:new String[]{names[11],names[12]}){boolean rejected=false;try{if(name.equals(names[11]))run(name);else run(name,1);}catch(BytecodeOracle.Unsupported expected){rejected=true;}equal(rejected,true);}
  long[] large={Long.MIN_VALUE,Long.MIN_VALUE+1,-922337203685477580L,-4294967296L,-2,-1,0,1,2,4294967296L,922337203685477580L,Long.MAX_VALUE-1,Long.MAX_VALUE};
  for(long x:large){equal(run("negLong(J)J",x),-x);equal(run("longAsInt(J)I",x),(int)x);
   for(long y:large)for(String suffix:new String[]{"","2"}){
    equal(run("addLong"+suffix+"(JJ)J",x,y),x+y);equal(run("subLong"+suffix+"(JJ)J",x,y),x-y);equal(run("mulLong"+suffix+"(JJ)J",x,y),x*y);
    if(y==0){boolean rejected=false;try{run("divLong"+suffix+"(JJ)J",x,y);}catch(ArithmeticException expected){rejected=true;}equal(rejected,true);}else equal(run("divLong"+suffix+"(JJ)J",x,y),x/y);
   }
  }
  for(int x:new int[]{Integer.MIN_VALUE,-65537,-65536,-1,0,1,65535,65536,65537,Integer.MAX_VALUE})equal(run("asChar(I)C",x),(char)x);
  for(int x:n)for(int y:n){equal(run("subtractInt(II)I",x,y),x-y);equal(run("subtractInt2(II)I",x,y),x-y);}
  for(double x:new double[]{Double.NEGATIVE_INFINITY,-Double.MAX_VALUE,-0x1p63,-3.9,-1.1,-0.0,0.0,1.1,3.9,Math.nextDown(0x1p63),0x1p63,Double.MAX_VALUE,Double.POSITIVE_INFINITY,Double.NaN})equal(run("doubleAsLong(D)J",x),(long)x);
  JsonObject r=new JsonObject();r.addProperty("pass",true);r.addProperty("cases",cases);r.addProperty("androidRuntime",false);r.addProperty("uninitializedRegistersRejected",true);r.addProperty("unknownOpcodesRejected",true);r.addProperty("scope","Explicit primitive opcode fixtures: signed zero, NaN cmpg/cmpl, infinities, 64-bit integer comparisons, raw float bits, narrowing/widening conversions, ordered double arithmetic, long overflow/negation, truncating division and divide-by-zero exceptions.");Files.writeString(root.resolve("reports/oracle-semantics.json"),new GsonBuilder().setPrettyPrinting().create().toJson(r));System.out.println("opcode conformance cases="+cases+" passed");
 }
}
