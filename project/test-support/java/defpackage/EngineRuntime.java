package defpackage;
import java.util.*;import java.util.concurrent.*;
import com.arlosoft.macrodroid.action.*;import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;import com.arlosoft.macrodroid.data.ResumeMacroInfo;
/** Explicit host-only service/clock boundaries. These classes never enter an APK. */
public final class EngineRuntime {
 public static boolean active,limitExceeded;public static long clockMillis=120000,nano=1000000000L,nanoStep;
 public static String fault;public static int faultOccurrence=1,faultSeen;public static Throwable failure;
 public static boolean handlerRuns=true,awaitResult=true,awaitInterrupted,sleepInterrupted,mainThread;
 public static long initialGuardStart,initialGuardLast,initialGuardCount;public static boolean initialGuardWarned;
 public static final List<String> effects=new ArrayList<String>(),scheduled=new ArrayList<String>();
 public static final Map<Macro,LoopAction> loops=new IdentityHashMap<Macro,LoopAction>();
 public static final Map<Macro,IterateDictionaryAction> dictionaries=new IdentityHashMap<Macro,IterateDictionaryAction>();
 public interface Dispatch {void run(Macro m,List a,int p,TriggerContextInfo c,boolean f,Stack t,ResumeMacroInfo r)throws Throwable;}
 public static Dispatch dispatch;
 public static void reset(){active=true;limitExceeded=false;clockMillis=120000;nano=1000000000L;nanoStep=0;fault=null;faultOccurrence=1;faultSeen=0;failure=null;handlerRuns=true;awaitResult=true;awaitInterrupted=false;sleepInterrupted=false;mainThread=false;initialGuardStart=initialGuardLast=initialGuardCount=0;initialGuardWarned=false;effects.clear();scheduled.clear();loops.clear();dictionaries.clear();dispatch=null;}
 public static void onCall(String k){if(!active)return;if(CoreTrace.calls.size()>15000){limitExceeded=true;throw new IllegalStateException("host boundary budget");}if(fault!=null&&k.equals(fault)&&++faultSeen==faultOccurrence&&failure!=null)EngineRuntime.<RuntimeException>raise(failure);}
 @SuppressWarnings("unchecked")public static <E extends Throwable>void raise(Throwable t)throws E{throw(E)t;}
 public static String id(Object o){if(o==null)return"null";if(o instanceof Macro)return((Macro)o).testId;if(o instanceof com.arlosoft.macrodroid.common.SelectableItem)return((com.arlosoft.macrodroid.common.SelectableItem)o).testId;if(o instanceof TriggerContextInfo)return"context";if(o instanceof ResumeMacroInfo)return"resume:"+((ResumeMacroInfo)o).i;return o.getClass().getName();}
 public static long now(){CoreTrace.add("clock.millis");return clockMillis;}
 public static long nanoTime(){CoreTrace.add("clock.nanos");long v=nano;nano+=nanoStep;return v;}
 public static void sleep(long ms)throws InterruptedException{CoreTrace.add("thread.sleep:"+ms);if(sleepInterrupted||Thread.interrupted())throw new InterruptedException("host sleep interrupted");}
 public static boolean await(CountDownLatch l,long n,TimeUnit u)throws InterruptedException{CoreTrace.add("debug.await:"+n+":"+u+":"+l.getCount());if(awaitInterrupted||Thread.interrupted())throw new InterruptedException("host await interrupted");return awaitResult;}
 public static void start(Thread t){CoreTrace.add("thread.start");scheduled.add("parent-continuation");t.run();}
 public static void dispatch(Macro m,List a,int p,TriggerContextInfo c,boolean f,Stack t,ResumeMacroInfo x){if(dispatch==null)throw new IllegalStateException("Missing host dispatcher");try{dispatch.run(m,a,p,c,f,t,x);}catch(Throwable e){EngineRuntime.<RuntimeException>raise(e);}}
}
