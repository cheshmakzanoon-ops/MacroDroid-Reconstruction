import java.nio.file.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import com.google.gson.*;
/** Bounded host instruction conformance, not ART validation or Android execution. */
public final class EngineOracleConformance {
 static int cases;static BytecodeOracle oracle;
 static Object run(String n,Object...v)throws Throwable{return oracle.invoke("Loracle/EnginePrimitives;->"+n,v);}
 static void check(boolean b,String what){cases++;if(!b)throw new AssertionError(what);}
 static void expect(Class<?> kind,String n,Object...v)throws Throwable{try{run(n,v);throw new AssertionError("expected "+kind.getName());}catch(Throwable t){check(kind.isInstance(t),n+" got "+t);}}
 public static void main(String[] args)throws Throwable{
  Path root=Paths.get(args[0]);defpackage.EngineRuntime.active=false;
  Set<String> names=Set.of("longAsDouble(J)D","doubleAsInt(D)I","underLock(Ljava/lang/Object;)Z","nestedLocks(Ljava/lang/Object;Ljava/lang/Object;)I","throwInside(Ljava/lang/Object;Ljava/lang/Throwable;)V","interruptedWait(Ljava/lang/Object;)Z","timedWait(Ljava/lang/Object;)Z","advancedExitPc(Ljava/lang/Object;)Z","crossedLocks(Ljava/lang/Object;Ljava/lang/Object;)V","missingExit(Ljava/lang/Object;)V");
  Set<String> keys=new HashSet<>();for(String n:names)keys.add("Loracle/EnginePrimitives;->"+n);oracle=new BytecodeOracle(root.resolve("build/engine-opcodes.dex"),keys);
  long[] longs={Long.MIN_VALUE,Long.MIN_VALUE+1,-9007199254740993L,-1,0,1,9007199254740993L,Long.MAX_VALUE-1,Long.MAX_VALUE};
  for(long v:longs)check(Double.doubleToRawLongBits((Double)run("longAsDouble(J)D",v))==Double.doubleToRawLongBits((double)v),"long/double boundary");
  double[] doubles={Double.NaN,Double.NEGATIVE_INFINITY,Double.POSITIVE_INFINITY,-Double.MAX_VALUE,Double.MAX_VALUE,-2147483649d,-2147483648d,2147483647d,2147483648d,-1.9,-0d,0d,1.9,Double.MIN_VALUE};
  for(double v:doubles)check((Integer)run("doubleAsInt(D)I",v)==(int)v,"double/int boundary");
  Random random=new Random(884012);
  for(int i=0;i<2048;i++){long l=random.nextLong();double d=Double.longBitsToDouble(random.nextLong());check(Double.doubleToRawLongBits((Double)run("longAsDouble(J)D",l))==Double.doubleToRawLongBits((double)l),"generated long/double");check((Integer)run("doubleAsInt(D)I",d)==(int)d,"generated double/int");}
  Object first=new Object(),second=new Object();
  check((Boolean)run("underLock(Ljava/lang/Object;)Z",first),"monitor owned inside");check(!Thread.holdsLock(first),"monitor released after return");
  check((Integer)run("nestedLocks(Ljava/lang/Object;Ljava/lang/Object;)I",first,second)==2,"nested locks held");check(!Thread.holdsLock(first)&&!Thread.holdsLock(second),"nested release");
  check((Integer)run("nestedLocks(Ljava/lang/Object;Ljava/lang/Object;)I",first,first)==2,"reentrant locks held");check(!Thread.holdsLock(first),"reentrant release");
  synchronized(first){check((Boolean)run("underLock(Ljava/lang/Object;)Z",first),"caller monitor nesting");check(Thread.holdsLock(first),"caller retains ownership");}
  expect(NullPointerException.class,"underLock(Ljava/lang/Object;)Z",(Object)null);
  for(Throwable t:new Throwable[]{new IllegalArgumentException("fixture"),new AssertionError("fixture"),new StackOverflowError("fixture")}){expect(t.getClass(),"throwInside(Ljava/lang/Object;Ljava/lang/Throwable;)V",first,t);check(!Thread.holdsLock(first),"release after "+t.getClass());}
  Thread.currentThread().interrupt();try{check((Boolean)run("interruptedWait(Ljava/lang/Object;)Z",first),"wait interrupted");check(Thread.currentThread().isInterrupted(),"interrupt restored");}finally{Thread.interrupted();}check(!Thread.holdsLock(first),"interrupted monitor released");
  AtomicBoolean notified=new AtomicBoolean();Thread notifier=new Thread(()->{try{Thread.sleep(20);}catch(InterruptedException e){Thread.currentThread().interrupt();}synchronized(first){notified.set(true);first.notifyAll();}},"oracle-notifier");
  notifier.start();try{check((Boolean)run("timedWait(Ljava/lang/Object;)Z",first),"wait reacquires monitor");}finally{notifier.join(2000);}check(notified.get()&&!notifier.isAlive(),"notifier completed");check(!Thread.holdsLock(first),"notified monitor released");
  check((Boolean)run("advancedExitPc(Ljava/lang/Object;)Z",first),"monitor-exit exception PC advances");
  expect(BytecodeOracle.Unsupported.class,"crossedLocks(Ljava/lang/Object;Ljava/lang/Object;)V",first,second);check(!Thread.holdsLock(first)&&!Thread.holdsLock(second),"crossed locks fail closed without monitor leak");
  expect(BytecodeOracle.Unsupported.class,"missingExit(Ljava/lang/Object;)V",first);check(!Thread.holdsLock(first),"missing exit fails closed without monitor leak");
  Map<String,Object> r=new LinkedHashMap<>();r.put("pass",true);r.put("cases",cases);r.put("androidRuntime",false);r.put("scope","Explicit numeric conversions and lexical JVM monitor ownership, reentrancy, exceptions, interrupt restoration, wait/notify and fail-closed unsupported monitor structure. Synthetic invalid sequences do not assert ART-verifier acceptance.");
  Files.writeString(root.resolve("reports/engine-oracle-semantics.json"),new GsonBuilder().setPrettyPrinting().create().toJson(r));System.out.println("Engine instruction conformance cases="+cases+" passed");
 }
}
