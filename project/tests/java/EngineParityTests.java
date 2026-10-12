import com.google.gson.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.*;
import com.arlosoft.macrodroid.action.*;
import com.arlosoft.macrodroid.actionblock.data.ActionBlock;
import com.arlosoft.macrodroid.common.*;
import com.arlosoft.macrodroid.constraint.Constraint;
import com.arlosoft.macrodroid.data.ResumeMacroInfo;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.*;

/** Original selected DEX -> recovered Java -> rebuilt selected DEX.
 * The dispatcher and its structural lookup/guard bodies execute, but Android service,
 * action effects, configuration, store and thread-scheduling boundaries are host doubles.
 */
public final class EngineParityTests {
 static final String MACRO="Lcom/arlosoft/macrodroid/macro/Macro;";
 static final String DISPATCH=MACRO+"->invokeActions(Ljava/util/List;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V";
 static final String GUARD="Lcom/arlosoft/macrodroid/macro/Macro$b;->a(Lcom/arlosoft/macrodroid/macro/Macro;Lcom/arlosoft/macrodroid/action/LoopAction;)Z";
 static final String SCOPES="Lcom/arlosoft/macrodroid/action/Action$a;->d(Ljava/util/List;)Ljava/util/LinkedHashMap;";
 static final String SCOPE_WRAPPER="Lcom/arlosoft/macrodroid/action/Action;->computeActionScopes(Ljava/util/List;)Ljava/util/Map;";
 static final Map<String,Map<String,Object>> mappings=new LinkedHashMap<>();static final Map<String,Method> helpers=new HashMap<>();
 static BytecodeOracle original,rebuilt;static int cases,failures,unsupported,expectedChecks;static final Map<String,Integer> counts=new TreeMap<>();static final List<Object> examples=new ArrayList<>();static final List<String> failedCaseLabels=new ArrayList<>();
 interface Factory {World make();} interface Expected {String check(World w,Object result,Throwable error);}
 static final class World {
  Object[] args;Macro root;Stack stack=new Stack();List<Macro> macros=new ArrayList<>();List<Action> actions=new ArrayList<>();Macro.b guard;Object extra;Thread notifier;volatile boolean sawWaiting;volatile String notifierFailure;
 }
 static final class FlipEnabledIf extends IfConditionAction {
  @Override public boolean isEnabled(){CoreTrace.add(testId+".enabled");boolean prior=enabled;enabled=false;return prior;}
 }
 static String nav(String method){return "Laq9;->"+method+"(ILjava/util/List;)I";}
 static <T extends Action>T action(Class<T> type,String id){try{T a=type.getDeclaredConstructor().newInstance();a.testId=id;a.system="system:"+id;return a;}catch(Exception e){throw new RuntimeException(e);}}
 static World world(Action... actions){World w=new World();Macro m=new Macro();m.testId="m";m.guid=m.m_GUID=51;m.name="macro";m.running=false;w.root=m;w.macros.add(m);w.actions.addAll(Arrays.asList(actions));m.m_actionList.addAll(Arrays.asList(actions));w.args=new Object[]{m,m.m_actionList,0,new TriggerContextInfo(),false,w.stack,null};return w;}
 static World ordinary(){return world(action(Action.class,"A0"),action(Action.class,"A1"),action(SeparatorAction.class,"S"));}
 static void reset(){Thread.interrupted();EngineRuntime.reset();CoreTrace.reset();TestClock.enabled=false;Macro.sMacroDroidEnabled=true;Macro.macroDroidDisabledTimeStamp=0;rl9.debugging=rl9.paused=rl9.threading=rl9.stopAfterPause=false;rl9.requested=-1;rl9.pauseQueries=0;rl9.generation=73;com.arlosoft.macrodroid.macro.b.k.a().macros.clear();com.arlosoft.macrodroid.macro.b.k.a().byId=com.arlosoft.macrodroid.macro.b.k.a().byName=null;Action.Companion=new Action.a();}
 static Object javaCall(String key,Object[] args)throws Throwable {try{return helpers.get(key).invoke(null,args);}catch(InvocationTargetException e){throw e.getCause();}}
 static Object call(int path,String key,Object[] args)throws Throwable{return path==0?original.invoke(key,args):path==1?javaCall(key,args):rebuilt.invoke(key,args);}
 static Object value(Object o){
  if(o==null)return null;if(o instanceof Double)return "double:"+Long.toHexString(Double.doubleToRawLongBits((Double)o));if(o instanceof Float)return "float:"+Integer.toHexString(Float.floatToRawIntBits((Float)o));
  if(o instanceof Number||o instanceof Boolean||o instanceof String)return o;
  if(o instanceof Map){List<Object> v=new ArrayList<>();for(Object e:((Map)o).entrySet()){Map.Entry entry=(Map.Entry)e;v.add(Arrays.asList(EngineRuntime.id(entry.getKey()),value(entry.getValue())));}return v;}
  if(o instanceof e6){e6 s=(e6)o;return Arrays.asList(EngineRuntime.id(s.parent),EngineRuntime.id(s.branch));}
  if(o instanceof List){List<Object> v=new ArrayList<>();for(Object e:(List)o)v.add(value(e));return v;}return EngineRuntime.id(o);
 }
 static List<String> normalizedTrace(){List<String> out=new ArrayList<>();for(String line:CoreTrace.calls){String t=line;for(String name:new String[]{"java.lang.NullPointerException","java.lang.ClassCastException"}){String prefix="Error invoking action: "+name;int at=t.indexOf(prefix);if(at>=0)t=t.substring(0,at)+prefix+":<VM-generated-message-excluded>";}out.add(t);}return out;}
 static Object snapshot(World w){
  List<Object> ms=new ArrayList<>(),as=new ArrayList<>();for(Macro m:w.macros)ms.add(Arrays.asList(m.testId,m.starts,m.terminations,m.outputs,m.m_invokeCount,m.m_cancelFlag,m.running,m.engineEnabled,EngineRuntime.id(m.activeShellScriptAction),EngineRuntime.id(m.triggerContextInfo),m.debugLock!=null&&Thread.holdsLock(m.debugLock)));
  for(Action a:w.actions){if(a==null){as.add(null);continue;}List<Object> row=new ArrayList<>(Arrays.asList(a.testId,a.executions,a.debugExecutionGeneration,a.enabled,EngineRuntime.id(a.macro),new ArrayList<>(a.engineAnswers)));if(a instanceof LoopAction){LoopAction l=(LoopAction)a;row.addAll(Arrays.asList(l.remaining,l.iterations,l.resets,l.first));if(l instanceof IterateDictionaryAction)row.add(((IterateDictionaryAction)l).dictionaryRemaining);}as.add(row);}
  TreeMap<String,String> loops=new TreeMap<>(),dictionaries=new TreeMap<>();for(Map.Entry<Macro,LoopAction> e:EngineRuntime.loops.entrySet())loops.put(e.getKey().testId,EngineRuntime.id(e.getValue()));for(Map.Entry<Macro,IterateDictionaryAction>e:EngineRuntime.dictionaries.entrySet())dictionaries.put(e.getKey().testId,EngineRuntime.id(e.getValue()));
  Object g=w.guard==null?null:Arrays.asList(w.guard.a,w.guard.b,w.guard.c,w.guard.d);
  return Arrays.asList(ms,as,String.valueOf(w.stack),g,new ArrayList<>(EngineRuntime.effects),new ArrayList<>(EngineRuntime.scheduled),loops,dictionaries,Macro.sMacroDroidEnabled,rl9.debugging,rl9.pauseQueries,EngineRuntime.nano,Thread.currentThread().isInterrupted());
 }
 static Map<String,Object> run(int path,String key,Factory factory,Expected expected){
  reset();World w=factory.make();EngineRuntime.dispatch=(m,a,p,c,f,s,r)->call(path,DISPATCH,new Object[]{m,a,p,c,f,s,r});CoreTrace.reset();Object result=null;Throwable error=null;
  try{result=call(path,key,w.args);}catch(Throwable t){error=t;}
  if(w.notifier!=null){try{w.notifier.join(3000);}catch(InterruptedException ex){Thread.currentThread().interrupt();error=ex;}if(w.notifier.isAlive()){w.notifier.interrupt();w.notifierFailure="notifier did not finish";}}

  Map<String,Object> out=new LinkedHashMap<>();out.put("value",value(result));out.put("error",error==null?null:error.getClass().getName());out.put("trace",normalizedTrace());out.put("state",snapshot(w));if(w.notifier!=null)out.put("notifierFailure",w.notifierFailure);
  if(error instanceof BytecodeOracle.Unsupported||EngineRuntime.limitExceeded){unsupported++;out.put("unsupported",error==null?"host boundary budget":error.toString());}
  if(expected!=null){expectedChecks++;try{String problem=expected.check(w,result,error);if(problem!=null)out.put("expectedFailure",problem);}catch(Throwable t){out.put("expectedFailure",t.toString());}}
  Thread.interrupted();EngineRuntime.active=false;return out;
 }
 static void check(String key,String label,Factory factory,Expected expected){cases++;counts.merge(key,1,Integer::sum);Map<String,Object>a=run(0,key,factory,expected),b=run(1,key,factory,expected),c=rebuilt==null?null:run(2,key,factory,expected);
  if(!a.equals(b)||(c!=null&&!a.equals(c))||a.containsKey("expectedFailure")||b.containsKey("expectedFailure")||(c!=null&&c.containsKey("expectedFailure"))||a.containsKey("unsupported")||b.containsKey("unsupported")||(c!=null&&c.containsKey("unsupported"))){failures++;failedCaseLabels.add(label);if(examples.size()<20)examples.add(Map.of("method",key,"case",label,"original",a,"java",b,"rebuilt",c==null?"NOT_EXECUTED":c));}
 }
 static void check(String key,String label,Factory factory){check(key,label,factory,null);}
 static Expected effect(String... ids){return(w,v,e)->e==null&&EngineRuntime.effects.equals(Arrays.asList(ids))?null:"expected effects "+Arrays.toString(ids)+", got "+EngineRuntime.effects+", error="+e;}
 static Expected completion(int starts,int terminations,String... ids){return(w,v,e)->{String problem=effect(ids).check(w,v,e);if(problem!=null)return problem;return w.root.starts==starts&&w.root.terminations==terminations?null:"start/termination counts "+w.root.starts+"/"+w.root.terminations;};}
 static List<Action> structure(int seed,int length){Random r=new Random(seed);Class<?>[] types={Action.class,IfConditionAction.class,EndIfAction.class,ElseAction.class,ElseIfConditionAction.class,ElseIfConfirmedThenAction.class,LoopAction.class,EndLoopAction.class,ActionGroupAction.class,ActionGroupEndAction.class};List<Action> out=new ArrayList<>();for(int i=0;i<length;i++){Action a=action((Class<? extends Action>)types[r.nextInt(types.length)],"A"+i);a.enabled=r.nextBoolean();out.add(a);}return out;}
 static void navigation(){
  String[] methods={"b","c","d","e","f","i","j","k"};for(String method:methods){String key=nav(method);for(int seed=0;seed<100;seed++)for(int pos:new int[]{-2,-1,0,1,3,7,16,Integer.MIN_VALUE,Integer.MAX_VALUE}){final int sd=seed,p=pos;check(key,"structure:"+seed+":"+pos,()->{World w=new World();List<Action>a=structure(sd,sd%17);w.actions.addAll(a);w.args=new Object[]{p,a};return w;});}
   for(int position:new int[]{-1,0,1,2}){final int p=position;check(key,"null-list:"+p,()->{World w=new World();w.args=new Object[]{p,null};return w;});check(key,"null-entry:"+p,()->{World w=new World();w.args=new Object[]{p,Arrays.asList(null,action(Action.class,"A"),null)};return w;});check(key,"wrong-entry:"+p,()->{World w=new World();w.args=new Object[]{p,Arrays.asList("wrong",action(Action.class,"A"),"wrong")};return w;});}
  }
  check(nav("d"),"nested-if-end",()->{World w=new World();w.args=new Object[]{0,Arrays.asList(action(IfConditionAction.class,"outer"),action(IfConditionAction.class,"inner"),action(EndIfAction.class,"innerEnd"),action(EndIfAction.class,"outerEnd"))};return w;},(w,v,e)->Objects.equals(v,3)?null:"outer ENDIF must be 3");
  check(nav("c"),"disabled-else",()->{World w=new World();ElseAction disabled=action(ElseAction.class,"disabled"),enabled=action(ElseAction.class,"enabled");disabled.enabled=false;w.args=new Object[]{0,Arrays.asList(action(IfConditionAction.class,"if"),disabled,enabled,action(EndIfAction.class,"end"))};return w;},(w,v,e)->Objects.equals(v,2)?null:"disabled ELSE must be skipped");
 }
 static void scopes(){for(String key:new String[]{SCOPES,SCOPE_WRAPPER}){
  for(int seed=0;seed<400;seed++){final int sd=seed;check(key,"scope:"+seed,()->{World w=new World();List<Action> a=structure(sd,sd%23);w.actions.addAll(a);w.args=new Object[]{a};return w;});}
  check(key,"null-list",()->{World w=new World();w.args=new Object[]{null};return w;});check(key,"null-action",()->{World w=new World();w.args=new Object[]{Arrays.asList((Object)null)};return w;});
  check(key,"same-object-twice",()->{World w=new World();Action a=action(IfConditionAction.class,"same");w.actions.add(a);w.args=new Object[]{Arrays.asList(a,a,action(EndIfAction.class,"E"),a)};return w;});
  check(key,"branch-parent-identities",()->{World w=new World();w.actions.addAll(Arrays.asList(action(IfConditionAction.class,"if"),action(Action.class,"body"),action(ElseAction.class,"else"),action(Action.class,"other"),action(EndIfAction.class,"end"),action(Action.class,"after")));w.args=new Object[]{w.actions};return w;},(w,v,e)->{Map m=(Map)v;e6 body=(e6)m.get(w.actions.get(1)),other=(e6)m.get(w.actions.get(3)),after=(e6)m.get(w.actions.get(5));return body.parent==w.actions.get(0)&&body.branch==null&&other.parent==w.actions.get(0)&&other.branch==w.actions.get(2)&&after.parent==null&&after.branch==null?null:"wrong parent/ELSE identities";});
 }}
 static Factory guard(long first,long last,long count,boolean warned,long now,boolean main,boolean interrupted){return()->{World w=world();w.guard=new Macro.b(0);w.guard.a=first;w.guard.b=last;w.guard.c=count;w.guard.d=warned;LoopAction l=action(LoopAction.class,"L");w.actions.add(l);w.args=new Object[]{w.guard,w.root,l};EngineRuntime.nano=now;EngineRuntime.mainThread=main;EngineRuntime.sleepInterrupted=interrupted;return w;};}
 static void guards(){
  long[] starts={0,1,1000000000L},elapsed={-1,0,99999999L,100000000L,3000000000L,3000000001L,60000000000L,60000000001L,61000000000L},countsV={-1,0,49,3000,3100,100000,Long.MAX_VALUE};
  for(long s:starts)for(long d:elapsed)for(long c:countsV)for(boolean warned:new boolean[]{false,true})for(boolean main:new boolean[]{false,true})check(GUARD,"guard:"+s+":"+d+":"+c+":"+warned+":"+main,guard(s,s+d,c,warned,s+d,main,false));
  check(GUARD,"100ms-preserves-window",guard(1,100,4,false,100000100,false,false),(w,v,e)->w.guard.a==1&&w.guard.c==5&&!((Boolean)v)?null:"100 ms boundary must not reset");
  check(GUARD,"100ms-plus-one-resets",guard(1,100,4,false,100000101,false,false),(w,v,e)->w.guard.a==100000101&&w.guard.c==1&&!((Boolean)v)?null:"100 ms + 1 must reset");
  check(GUARD,"three-seconds-not-throttled",guard(1,3000000001L,4,false,3000000001L,false,false),(w,v,e)->!w.guard.d&&!CoreTrace.calls.contains("thread.sleep:10")?null:"exact 3s must not throttle");
  check(GUARD,"three-seconds-plus-one-throttled",guard(1,3000000002L,4,false,3000000002L,false,false),(w,v,e)->w.guard.d&&CoreTrace.calls.contains("thread.sleep:10")?null:"3s + 1 should warn and throttle");
  check(GUARD,"sixty-seconds-not-aborted",guard(1,60000000001L,100000,false,60000000001L,true,false),(w,v,e)->Boolean.FALSE.equals(v)&&w.root.terminations==0?null:"exact 60s must not abort");
  check(GUARD,"sixty-seconds-plus-one-aborted",guard(1,60000000002L,100000,false,60000000002L,true,false),(w,v,e)->Boolean.TRUE.equals(v)&&w.root.terminations==1?null:"60s + 1 high rate must abort");
  check(GUARD,"exact-fifty-hz-not-aborted",guard(1,62000000001L,3099,false,62000000001L,true,false),(w,v,e)->Boolean.FALSE.equals(v)?null:"exact 50 Hz must not abort");
  check(GUARD,"over-fifty-hz-aborted",guard(1,62000000001L,3100,false,62000000001L,true,false),(w,v,e)->Boolean.TRUE.equals(v)?null:"above 50 Hz should abort");
  check(GUARD,"throttle-interruption-restored",guard(1,4000000001L,2,false,4000000001L,false,true),(w,v,e)->Boolean.FALSE.equals(v)&&Thread.currentThread().isInterrupted()?null:"sleep interruption must be restored");
  for(long n:new long[]{Long.MIN_VALUE,Long.MAX_VALUE})check(GUARD,"overflow:"+n,guard(n,n,Long.MAX_VALUE,true,-n,false,false));
 }
 static void basic(){
  check(DISPATCH,"empty",()->world(),completion(1,1));check(DISPATCH,"ordinary",()->ordinary(),completion(1,1,"A0","A1"));
  for(int bits=0;bits<64;bits++)for(int pos:new int[]{-1,0,1,2,3,4}){final int flags=bits,p=pos;check(DISPATCH,"gates:"+bits+":"+p,()->{World w=ordinary();w.args[2]=p;w.args[4]=(flags&1)!=0;w.root.m_cancelFlag=(flags&2)!=0;w.root.engineEnabled=(flags&4)==0;Macro.sMacroDroidEnabled=(flags&8)==0;w.root.disabledTimestamp=(flags&16)!=0?2:0;w.root.forceEvenIfNotEnabledTimestamp=1;Macro.macroDroidDisabledTimeStamp=(flags&32)!=0?2:0;return w;});}
  for(int limit:new int[]{-1,0,1,2,3,4,9})for(int pos:new int[]{0,1,3})for(int parentPosition:new int[]{-1,0}){final int l=limit,p=pos,rp=parentPosition;check(DISPATCH,"resume-range:"+l+":"+p+":"+rp,()->{World w=ordinary();ResumeMacroInfo r=new ResumeMacroInfo();r.i=l;r.b=rp;r.a=999;w.args[6]=r;w.args[2]=p;return w;});}
  check(DISPATCH,"cancel-after-first",()->{World w=ordinary();w.actions.get(0).cancelOnExecute=true;return w;},completion(1,1,"A0"));
  for(int mode=0;mode<4;mode++){final int m=mode;check(DISPATCH,"terminate-running:"+mode,()->{TerminateRunningAction a=action(TerminateRunningAction.class,"T");a.enabled=(m&1)==0;a.engineResult=(m&2)==0;return world(a,action(Action.class,"after"));});}
  for(int c:new int[]{4999,5000,5001,10000,Integer.MAX_VALUE})for(long delta:new long[]{-10000,0,999,1000,2000,100000,Long.MAX_VALUE}){final int count=c;final long elapsed=delta;check(DISPATCH,"rate:"+c+":"+delta,()->{World w=world();w.root.m_invokeCount=count;w.root.m_invokeStart=EngineRuntime.clockMillis-elapsed;return w;});}
  check(DISPATCH,"rate-limit-terminates",()->{World w=ordinary();w.root.m_invokeCount=5000;return w;},completion(1,1));
  check(DISPATCH,"null-actions",()->{World w=world();w.args[1]=null;return w;});check(DISPATCH,"null-action",()->world((Action)null));
  check(DISPATCH,"wrong-action-type",()->{World w=world();w.root.m_actionList.add("wrong");return w;});
  check(DISPATCH,"preserve-existing-owner",()->{World w=ordinary();Macro other=new Macro();other.testId="owner";w.actions.get(0).macro=other;w.macros.add(other);return w;},(w,v,e)->w.actions.get(0).macro==w.macros.get(1)?null:"non-null owner must not be replaced");
 }
 static void conditionals(){
  for(boolean truth:new boolean[]{false,true})for(boolean enabled:new boolean[]{false,true})for(int branch=0;branch<4;branch++){final boolean tr=truth,en=enabled;final int kind=branch;
   check(DISPATCH,"if:"+tr+":"+en+":"+kind,()->{IfConditionAction a=action(IfConditionAction.class,"if");a.engineResult=tr;a.enabled=en;List<Action> list=new ArrayList<>();list.add(a);list.add(action(Action.class,"then"));if(kind==1){list.add(action(ElseAction.class,"else"));list.add(action(Action.class,"other"));}else if(kind==2){ElseIfConditionAction ei=action(ElseIfConditionAction.class,"elseif");ei.engineResult=true;list.add(ei);list.add(action(Action.class,"other"));}else if(kind==3){ElseIfConfirmedThenAction ei=action(ElseIfConfirmedThenAction.class,"confirmElse");list.add(ei);list.add(action(Action.class,"other"));}list.add(action(EndIfAction.class,"end"));list.add(action(Action.class,"after"));return world(list.toArray(new Action[0]));});
  }
  check(DISPATCH,"true-if-else",()->world(action(IfConditionAction.class,"if"),action(Action.class,"then"),action(ElseAction.class,"else"),action(Action.class,"other"),action(EndIfAction.class,"end"),action(Action.class,"after")),completion(1,1,"then","after"));
  check(DISPATCH,"false-if-else",()->{IfConditionAction a=action(IfConditionAction.class,"if");a.engineResult=false;return world(a,action(Action.class,"then"),action(ElseAction.class,"else"),action(Action.class,"other"),action(EndIfAction.class,"end"),action(Action.class,"after"));},completion(1,1,"other","after"));
  for(boolean outer:new boolean[]{false,true})for(boolean inner:new boolean[]{false,true}){final boolean o=outer,i=inner;check(DISPATCH,"nested-if:"+o+":"+i,()->{IfConditionAction a=action(IfConditionAction.class,"outer"),b=action(IfConditionAction.class,"inner");a.engineResult=o;b.engineResult=i;return world(a,b,action(Action.class,"innerThen"),action(ElseAction.class,"innerElse"),action(Action.class,"innerOther"),action(EndIfAction.class,"innerEnd"),action(ElseAction.class,"outerElse"),action(Action.class,"outerOther"),action(EndIfAction.class,"outerEnd"),action(Action.class,"after"));});}
  // The original dispatcher forwards ActionGroupEndAction through the generic
  // permission/action boundary (DEX PCs 0x645 -> 0x658 -> 0x6a5), unlike other
  // EndParentAction instances. The real marker's invokeAction is a no-op; our
  // test boundary records the invocation, not an Android/user-visible effect.
  for(boolean truth:new boolean[]{false,true}){final boolean tr=truth;check(DISPATCH,"group:"+tr,()->{ActionGroupAction a=action(ActionGroupAction.class,"group");a.engineResult=tr;return world(a,action(Action.class,"body"),action(ActionGroupEndAction.class,"end"),action(Action.class,"after"));},tr?completion(1,1,"body","end","after"):completion(1,1,"after"));}
  check(DISPATCH,"group-end-boundary-preserves-conditional-stack",()->{World w=world(action(ActionGroupEndAction.class,"end"),action(Action.class,"after"));w.stack.push(99);return w;},(w,v,e)->{String p=completion(1,1,"end","after").check(w,v,e);return p!=null?p:w.stack.equals(Arrays.asList(99))?null:"group end must not pop a conditional frame";});
  check(DISPATCH,"endif-pops-conditional-stack",()->{World w=world(action(EndIfAction.class,"end"),action(Action.class,"after"));w.stack.push(99);return w;},(w,v,e)->{String p=completion(1,1,"after").check(w,v,e);return p!=null?p:w.stack.isEmpty()?null:"ENDIF must pop a conditional frame";});

  for(Class<? extends Action> cls:Arrays.asList(IfConditionAction.class,ElseAction.class,ElseIfConditionAction.class,EndIfAction.class,ActionGroupEndAction.class)){check(DISPATCH,"malformed:"+cls.getSimpleName(),()->{Action a=action(cls,"bad");a.engineResult=false;return world(a,action(Action.class,"after"));});}
  for(Object stackValue:new Object[]{0,2,-1,"wrong",null})check(DISPATCH,"preexisting-stack:"+stackValue,()->{World w=world(action(IfConditionAction.class,"if"),action(EndIfAction.class,"end"));w.stack.push(stackValue);return w;});
  check(DISPATCH,"null-stack",()->{World w=world(action(IfConditionAction.class,"if"));w.args[5]=null;return w;});
  for(boolean enabled:new boolean[]{false,true})for(boolean truth:new boolean[]{false,true}){final boolean en=enabled,tr=truth;check(DISPATCH,"confirmed-if:"+en+":"+tr,()->{IfConfirmedThenAction a=action(IfConfirmedThenAction.class,"confirm");a.enabled=en;a.engineResult=tr;return world(a,action(Action.class,"body"),action(EndIfAction.class,"end"));});}
 }
 static void additionalDispatchBoundaries(){
  check(DISPATCH,"dictionary-without-end",()->{IterateDictionaryAction a=action(IterateDictionaryAction.class,"dictionary");a.dictionaryRemaining=0;return world(a,action(Action.class,"after"));},completion(1,1));
  check(DISPATCH,"break-dictionary-clears-state",()->world(action(IterateDictionaryAction.class,"dictionary"),action(IfConditionAction.class,"if"),action(BreakFromLoopAction.class,"break"),action(EndIfAction.class,"endif"),action(EndLoopAction.class,"end"),action(Action.class,"after")),(w,v,e)->{String p=completion(2,1,"after").check(w,v,e);return p!=null?p:w.stack.empty()&&EngineRuntime.dictionaries.isEmpty()&&EngineRuntime.loops.isEmpty()?null:"dictionary break must clear both active-loop references and the IF frame";});
  check(DISPATCH,"else-without-endif",()->world(action(IfConditionAction.class,"if"),action(Action.class,"then"),action(ElseAction.class,"else"),action(Action.class,"other")),completion(1,1,"then"));
  check(DISPATCH,"else-parent-enabled-state-changes-between-reads",()->{World w=world(action(FlipEnabledIf.class,"if"),action(ElseAction.class,"else"),action(Action.class,"after"));w.args[2]=1;w.stack.push(99);return w;},(w,v,e)->{String p=completion(1,1,"after").check(w,v,e);return p!=null?p:w.stack.empty()&&!w.actions.get(0).enabled?null:"dynamic enabled-state boundary differs";});
  for(Class<? extends Action> cls:Arrays.asList(ElseIfConditionAction.class,ElseIfConfirmedThenAction.class)){
   check(DISPATCH,"false-elseif-then-else:"+cls.getSimpleName(),()->{IfConditionAction first=action(IfConditionAction.class,"if");first.engineResult=false;Action second=action(cls,"elseif");second.engineResult=false;return world(first,action(Action.class,"then"),second,action(Action.class,"middle"),action(ElseAction.class,"else"),action(Action.class,"other"),action(EndIfAction.class,"end"),action(Action.class,"after"));},completion(1,1,"other","after"));
  }
  check(DISPATCH,"debug-monitor-fault-releases-lock",()->{World w=ordinary();rl9.debugging=true;rl9.paused=true;w.root.breakpoints.add(0);EngineRuntime.fault="debug.paused";EngineRuntime.failure=new IllegalStateException("monitor-boundary-failure");return w;},(w,v,e)->{String p=completion(1,1).check(w,v,e);return p!=null?p:!Thread.holdsLock(w.root.debugLock)?null:"debug fault leaked its monitor";});
  check(DISPATCH,"debug-monitor-notify-resumes-dispatch",()->{
   World w=ordinary();rl9.debugging=true;rl9.paused=true;w.root.breakpoints.add(0);Thread target=Thread.currentThread();
   w.notifier=new Thread(()->{try{long limit=System.nanoTime()+2000000000L;while(target.getState()!=Thread.State.WAITING&&System.nanoTime()<limit)Thread.sleep(1);if(target.getState()!=Thread.State.WAITING){w.notifierFailure="dispatcher wait was not observed";return;}synchronized(w.root.debugLock){w.sawWaiting=true;rl9.paused=false;w.root.debugLock.notifyAll();}}catch(Throwable t){w.notifierFailure=t.toString();}},"dispatcher-test-notifier");
   w.notifier.setDaemon(true);w.notifier.start();return w;
  },(w,v,e)->{String p=completion(1,1,"A0","A1").check(w,v,e);return p!=null?p:w.sawWaiting&&w.notifierFailure==null&&!Thread.holdsLock(w.root.debugLock)?null:"wait/notify continuation or monitor release failed";});
 }
 static void async(){
  double[] values={Double.NaN,Double.NEGATIVE_INFINITY,Double.POSITIVE_INFINITY,-2147483649d,-1000.125,-0d,0d,0.5d,1.999d,2147483648d,Double.MAX_VALUE};
  for(int unit:new int[]{-1,0,1,2,3})for(double d:values)for(boolean alarm:new boolean[]{false,true}){final int u=unit;final double value=d;final boolean al=alarm;check(DISPATCH,"pause:"+u+":"+Long.toHexString(Double.doubleToRawLongBits(value))+":"+al,()->{PauseAction p=action(PauseAction.class,"pause");p.units=u;p.alarm=al;p.delayVariable=new MacroDroidVariable();p.delayVariable.number=value;p.engineVariables.put("delay",p.delayVariable);return world(p,action(Action.class,"after"));},(w,v,e)->e==null&&w.root.terminations==0&&EngineRuntime.effects.isEmpty()&&EngineRuntime.scheduled.size()==1?null:"pause must hand off, not complete or run next action");}
  check(DISPATCH,"fixed-pause",()->world(action(PauseAction.class,"pause")),(w,v,e)->EngineRuntime.scheduled.size()==1&&EngineRuntime.scheduled.get(0).contains(":25:false:false")&&w.root.terminations==0?null:"fixed pause duration / completion mismatch");
  for(boolean variablePresent:new boolean[]{false,true}){final boolean present=variablePresent;check(DISPATCH,"null-pause-value:"+present,()->{PauseAction p=action(PauseAction.class,"pause");p.delayVariable=new MacroDroidVariable();if(present)p.engineVariables.put("delay",p.delayVariable);return world(p);});}
  check(DISPATCH,"async-shell",()->world(action(ShellScriptAction.class,"shell"),action(Action.class,"after")),(w,v,e)->w.actions.get(0).debugExecutionGeneration==73&&w.root.terminations==0&&EngineRuntime.effects.isEmpty()?null:"async generation and handoff differ");
  for(boolean enabled:new boolean[]{false,true}){final boolean asynchronous=enabled;check(DISPATCH,"set-variable:"+enabled,()->{SetVariableAction a=action(SetVariableAction.class,"set");a.asynchronous=asynchronous;return world(a,action(Action.class,"after"));});}
  for(long target:new long[]{51,99})for(boolean others:new boolean[]{false,true}){final long t=target;final boolean o=others;check(DISPATCH,"cancel-active:"+t+":"+o,()->{CancelActiveMacroAction a=action(CancelActiveMacroAction.class,"cancel");a.target=t;a.others=o;return world(a,action(Action.class,"after"));});}
 }
 static void loops(){
  for(int type:new int[]{-1,0,1,2,3,4,5})for(boolean enabled:new boolean[]{false,true}){final int t=type;final boolean en=enabled;check(DISPATCH,"loop:"+t+":"+en,()->{LoopAction l=action(LoopAction.class,"loop");l.type=t;l.enabled=en;if(t==1)l.engineAnswers.addAll(Arrays.asList(true,true,false));if(t==2)l.engineAnswers.addAll(Arrays.asList(true,false));Action body=action(Action.class,"body");if(t==3||t<0||t>4)body.cancelAtExecution=2;return world(l,body,action(EndLoopAction.class,"end"),action(Action.class,"after"));});}
  check(DISPATCH,"counted-loop-two-iterations",()->world(action(LoopAction.class,"loop"),action(Action.class,"body"),action(EndLoopAction.class,"end"),action(Action.class,"after")),completion(1,1,"body","body","after"));
  for(int count:new int[]{0,1,2,5}){final int n=count;check(DISPATCH,"dictionary:"+n,()->{IterateDictionaryAction a=action(IterateDictionaryAction.class,"dictionary");a.dictionaryRemaining=n;return world(a,action(Action.class,"body"),action(EndLoopAction.class,"end"),action(Action.class,"after"));});}
  check(DISPATCH,"break-unwinds-and-recurses",()->world(action(LoopAction.class,"loop"),action(IfConditionAction.class,"if"),action(BreakFromLoopAction.class,"break"),action(EndIfAction.class,"endif"),action(EndLoopAction.class,"end"),action(Action.class,"after")),(w,v,e)->{String p=completion(2,1,"after").check(w,v,e);return p!=null?p:w.stack.empty()?null:"break failed to unwind IF stack";});
  check(DISPATCH,"continue-unwinds-stack",()->world(action(LoopAction.class,"loop"),action(IfConditionAction.class,"if"),action(ContinueLoopAction.class,"continue"),action(Action.class,"skipped"),action(EndIfAction.class,"endif"),action(EndLoopAction.class,"end"),action(Action.class,"after")),(w,v,e)->{String p=completion(1,1,"after").check(w,v,e);return p!=null?p:w.stack.empty()?null:"continue failed to unwind IF stack";});
  for(Class<? extends Action> cls:Arrays.asList(EndLoopAction.class,BreakFromLoopAction.class,ContinueLoopAction.class)){check(DISPATCH,"orphan-loop-marker:"+cls.getSimpleName(),()->world(action(cls,"orphan"),action(Action.class,"after")));}
  for(int type:new int[]{0,1,4}){final int t=type;check(DISPATCH,"missing-loop-end:"+t,()->{LoopAction l=action(LoopAction.class,"loop");l.type=t;l.remaining=0;l.engineResult=false;l.timedOut=true;return world(l,action(Action.class,"after"));});}
  check(DISPATCH,"loop-guard-abort",()->{World w=world(action(LoopAction.class,"loop"),action(Action.class,"body"),action(EndLoopAction.class,"end"),action(Action.class,"after"));EngineRuntime.initialGuardStart=1;EngineRuntime.initialGuardLast=60000000002L;EngineRuntime.initialGuardCount=100000;EngineRuntime.nano=60000000002L;return w;},completion(1,1,"body"));
 }
 static void jumps(){
  check(DISPATCH,"forward-goto",()->{GotoAction g=action(GotoAction.class,"goto");Action target=action(Action.class,"target");target.label="target";return world(g,action(Action.class,"skipped"),target,action(Action.class,"after"));},completion(1,1,"target","after"));
  check(DISPATCH,"missing-goto",()->world(action(GotoAction.class,"goto"),action(Action.class,"after")),completion(1,1,"after"));
  check(DISPATCH,"null-goto-label",()->{GotoAction g=action(GotoAction.class,"goto");g.destination=null;return world(g,action(Action.class,"after"));});
  check(DISPATCH,"goto-cannot-enter-if",()->{GotoAction g=action(GotoAction.class,"goto");IfConditionAction a=action(IfConditionAction.class,"if");a.engineResult=false;Action target=action(Action.class,"target");target.label="target";return world(g,a,target,action(EndIfAction.class,"end"),action(Action.class,"after"));},completion(1,1,"after"));
  check(DISPATCH,"goto-cannot-cross-else",()->{GotoAction g=action(GotoAction.class,"goto");Action target=action(Action.class,"target");target.label="target";return world(action(IfConditionAction.class,"if"),g,action(ElseAction.class,"else"),target,action(EndIfAction.class,"end"),action(Action.class,"after"));},completion(1,1,"after"));
  check(DISPATCH,"first-label-wins",()->{GotoAction g=action(GotoAction.class,"goto");Action a=action(Action.class,"first"),b=action(Action.class,"second");a.label=b.label="target";a.cancelOnExecute=true;return world(g,a,b);},completion(1,1,"first"));
 }
 static void completion(){
  for(boolean test:new boolean[]{false,true})for(boolean clone:new boolean[]{false,true})for(boolean canceled:new boolean[]{false,true}){final boolean t=test,c=clone,p=canceled;check(DISPATCH,"block-cleanup:"+t+":"+c+":"+p,()->{World w=ordinary();ActionBlock b=new ActionBlock();b.testId="block";b.guid=b.m_GUID=61;b.running=false;b.isActionBlock=true;b.testMode=t;b.isClonedInstance=c;b.parent=new Macro();b.parent.testId="parent";b.parent.m_cancelFlag=p;b.m_actionList=w.root.m_actionList;w.macros.clear();w.macros.add(b);w.macros.add(b.parent);w.root=b;w.args[0]=b;for(Action a:w.actions){Constraint constraint=new Constraint();constraint.testId=a.testId+".constraint";a.engineConstraints.add(constraint);}return w;});}
  for(int p:new int[]{-1,0,1,9})for(boolean found:new boolean[]{false,true})for(boolean threaded:new boolean[]{false,true}){final int position=p;final boolean exists=found,th=threaded;check(DISPATCH,"parent-resume:"+p+":"+found+":"+threaded,()->{World w=world();ResumeMacroInfo r=new ResumeMacroInfo();r.a=77;r.b=position;r.c=new TriggerContextInfo();w.args[6]=r;rl9.threading=th;if(exists){Macro parent=new Macro();parent.testId="parent";parent.guid=parent.m_GUID=77;parent.running=false;Action a=action(Action.class,"parentAction");parent.m_actionList.add(a);w.actions.add(a);w.macros.add(parent);com.arlosoft.macrodroid.macro.b.k.a().byId=parent;}return w;});}
  check(DISPATCH,"resume-negative-position-no-terminate",()->{World w=world();w.args[6]=new ResumeMacroInfo();return w;},(w,v,e)->e==null&&w.root.outputs==1&&w.root.terminations==0&&w.root.running?null:"negative parent position must return before termination");
 }
 static void debug(){
  for(boolean run:new boolean[]{false,true})for(boolean await:new boolean[]{false,true})for(boolean interrupted:new boolean[]{false,true}){final boolean r=run,a=await,i=interrupted;check(DISPATCH,"debug-action:"+run+":"+await+":"+interrupted,()->{World w=ordinary();rl9.debugging=true;EngineRuntime.handlerRuns=r;EngineRuntime.awaitResult=a;EngineRuntime.awaitInterrupted=i;return w;});}
  for(int requested:new int[]{-1,0,1,3,9}){final int next=requested;check(DISPATCH,"breakpoint-skip:"+next,()->{World w=ordinary();rl9.debugging=true;rl9.requested=next;w.root.breakpoints.add(0);return w;});}
  check(DISPATCH,"debug-stopped-during-pause",()->{World w=ordinary();rl9.debugging=true;rl9.stopAfterPause=true;w.root.breakpoints.add(0);return w;},completion(1,1));
  check(DISPATCH,"interrupted-debug-monitor",()->{World w=ordinary();rl9.debugging=true;rl9.paused=true;w.root.breakpoints.add(0);Thread.currentThread().interrupt();return w;},(w,v,e)->{String p=completion(1,1).check(w,v,e);return p!=null?p:Thread.currentThread().isInterrupted()&&!Thread.holdsLock(w.root.debugLock)?null:"interrupt or monitor release lost";});
  check(DISPATCH,"null-debug-monitor",()->{World w=ordinary();rl9.debugging=true;w.root.breakpoints.add(0);w.root.debugLock=null;return w;});
 }
 static void faults(){
  for(String boundary:new String[]{"m.start","loopGuard.new:0","A0.constraints:context","A0.setMacroAction","m.setContext:context","m.logAction:A0:0:context","A0.invokeWithPermission:context","m.terminate"})for(int kind=0;kind<3;kind++){final String point=boundary;final int type=kind;check(DISPATCH,"fault:"+point+":"+kind,()->{World w=ordinary();EngineRuntime.fault=point;EngineRuntime.failure=type==0?new IllegalStateException("injected engine failure"):type==1?new StackOverflowError("injected engine overflow"):new AssertionError("injected engine assertion");return w;});}
  check(DISPATCH,"start-failure-outside-catch",()->{World w=ordinary();EngineRuntime.fault="m.start";EngineRuntime.failure=new IllegalStateException("outside");return w;},(w,v,e)->e instanceof IllegalStateException&&w.root.terminations==0?null:"start failure was swallowed or completed");
  check(DISPATCH,"pause-log-failure",()->{World w=world(action(PauseAction.class,"pause"));EngineRuntime.fault="m.logAction:pause:0:context";EngineRuntime.failure=new IllegalStateException("pause failure");return w;},completion(1,1));
 }
 static Object coverage(BytecodeOracle oracle){Map<String,Object> out=new TreeMap<>();for(String key:mappings.keySet()){var m=oracle.methods.get(key);List<Integer> missing=new ArrayList<>();int pc=0,total=0;for(var i:m.getImplementation().getInstructions()){if(!oracle.executed.getOrDefault(key,Set.of()).contains(pc))missing.add(pc);total++;pc+=i.getCodeUnits();}out.put(key,Map.of("instructions",total,"visited",oracle.executed.getOrDefault(key,Set.of()).size(),"unvisitedOffsets",missing,"branchEdges",oracle.branchEdges.getOrDefault(key,Set.of()).size()));}return out;}
 static void register(Map<String,Object> m)throws Exception{String key=(String)m.get("target")+"->"+m.get("method");mappings.put(key,m);String name=(String)m.get("helper"),sig=(String)m.get("helper_method");Class<?> c=Class.forName(name.substring(1,name.length()-1).replace('/','.'));String methodName=sig.contains("(")?sig.substring(0,sig.indexOf('(')):sig;Method found=null;for(Method method:c.getDeclaredMethods())if(method.getName().equals(methodName)){if(found!=null)throw new IllegalStateException("Ambiguous helper");found=method;}if(found==null)throw new NoSuchMethodException(sig);helpers.put(key,found);}
 public static void main(String[] argv)throws Exception{
  Path root=Path.of(argv[0]);List<Map<String,Object>> rows=new Gson().fromJson(Files.readString(root.resolve("source/engine-methods.json")),List.class);for(Map<String,Object>m:rows)register(m);
  original=new BytecodeOracle(root.resolve("tests/fixtures/original-methods.dex"),mappings.keySet());
  boolean twoWay=Arrays.asList(argv).contains("--two-way");
  if(!twoWay){List<Path> dexFiles=new ArrayList<>();try(var paths=Files.walk(root.resolve("build/hybrid"))){paths.filter(p->p.toString().endsWith(".dex")).sorted().forEach(dexFiles::add);}rebuilt=new BytecodeOracle();for(Path dex:dexFiles)rebuilt.add(dex,mappings.keySet());}
  if(original.methods.size()!=mappings.size()||(!twoWay&&rebuilt.methods.size()!=mappings.size()))throw new AssertionError("Missing engine methods");
  String selection=argv.length>2?argv[2]:"all";if(selection.equals("all")||selection.equals("navigation"))navigation();if(selection.equals("all")||selection.equals("scopes"))scopes();if(selection.equals("all")||selection.equals("guards"))guards();
  if(selection.equals("all")||selection.equals("dispatch")){basic();conditionals();async();loops();jumps();completion();debug();faults();additionalDispatchBoundaries();}
  Map<String,Object> report=new LinkedHashMap<>();report.put("pass",cases>0&&failures==0&&unsupported==0&&(!selection.equals("all")||counts.keySet().equals(mappings.keySet())));report.put("paths",rebuilt==null?2:3);report.put("methodsCovered",counts.size());report.put("methodKeys",new java.util.ArrayList<>(counts.keySet()));report.put("methodsExpected",mappings.size());report.put("scope","Original selected DEX / recovered Java / rebuilt DEX, with controlled Android/action/store/clock/thread boundaries; not Android runtime");report.put("selection",selection);report.put("cases",cases);report.put("expectedChecks",expectedChecks);report.put("failures",failures);report.put("unsupportedExecutions",unsupported);report.put("methods",counts);report.put("examples",examples);report.put("failedCaseLabels",failedCaseLabels);report.put("agentTransformedClasses",TestClockAgent.changed);report.put("originalCoverage",coverage(original));report.put("rebuiltCoverage",rebuilt==null?null:coverage(rebuilt));report.put("messageExclusions",List.of("VM-generated NPE and ClassCastException text inside dispatcher error logs; exception types and ordered prefixes retained"));
  Files.writeString(Path.of(argv[1]),new GsonBuilder().serializeNulls().setPrettyPrinting().create().toJson(report)+"\n");System.out.println("Engine parity: "+cases+" cases, "+failures+" failures, "+unsupported+" unsupported, "+expectedChecks+" independent expected checks");if(!Boolean.TRUE.equals(report.get("pass")))System.exit(1);
 }
}
