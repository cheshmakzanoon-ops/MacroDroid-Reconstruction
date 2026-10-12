import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.instruction.formats.ArrayPayload;
import com.android.tools.smali.dexlib2.iface.reference.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;

/** Strict, bounded instruction interpreter for the selected methods, NOT ART/Android.
 * Reference and primitive registers are distinct. Unsupported instructions fail closed.
 * External calls use the controlled JVM classpath; Android/app boundaries are test doubles.
 */
public final class BytecodeOracle {
 static final class Ref { Object value; Ref(Object value){this.value=value;} }
 static final class Bits {long value;Bits(long v){value=v;} }
 static final class Pending {Class<?> type;Pending(Class<?> t){type=t;} }
 static final class Unsupported extends Error {Unsupported(String s){super(s);} }
 final Map<String,com.android.tools.smali.dexlib2.iface.Method> methods=new HashMap<>();
 final Map<String,Set<Integer>> executed = new TreeMap<>();
 final Map<String,Set<String>> branchEdges = new TreeMap<>();
 static final Object UNDEFINED = new Object();
 int depth;
 static String sig(MethodReference m){return m.getName()+"("+String.join("",m.getParameterTypes())+")"+m.getReturnType();}
 static String key(MethodReference m){return m.getDefiningClass()+"->"+sig(m);}
 BytecodeOracle(Path file,Set<String> selected) throws Exception { add(file,selected); }
 BytecodeOracle(){}
 void add(Path file,Set<String> selected) throws Exception {
  var dex=DexFileFactory.loadDexFile(file.toFile(),Opcodes.forApi(23));
  for(ClassDef c:dex.getClasses())for(var m:c.getMethods())if(selected.contains(key(m)))methods.put(key(m),m);
 }
 static boolean reference(String type){return type.startsWith("L")||type.startsWith("[");}
 static String descriptor(Class<?> c){if(c.isArray())return c.getName().replace('.','/');if(!c.isPrimitive()){String n=c.getName();if(n.startsWith("defpackage."))n=n.substring(11);return "L"+n.replace('.','/')+";";}return Map.of(void.class,"V",boolean.class,"Z",byte.class,"B",short.class,"S",char.class,"C",int.class,"I",long.class,"J",float.class,"F",double.class,"D").get(c);}
 static Class<?> type(String d) throws ClassNotFoundException {
  switch(d){case "V":return void.class;case "Z":return boolean.class;case "B":return byte.class;case "S":return short.class;case "C":return char.class;case "I":return int.class;case "J":return long.class;case "F":return float.class;case "D":return double.class;}
  if(d.startsWith("["))return Array.newInstance(type(d.substring(1)),0).getClass();
  String n=d.substring(1,d.length()-1).replace('/','.');if(!n.contains("."))n="defpackage."+n;
  return Class.forName(n);
 }
 static Object ref(Object v){if(v instanceof Ref)return ((Ref)v).value;if(v==null)return null;if(v instanceof Number&&((Number)v).longValue()==0)return null;throw new Unsupported("Reference register contains primitive "+v);}
 static int integer(Object v){if(v==null)return 0;if(v instanceof Boolean)return (Boolean)v?1:0;if(v instanceof Character)return (Character)v;if(v instanceof Bits)return (int)((Bits)v).value;if(v instanceof Number)return ((Number)v).intValue();throw new Unsupported("Integer register contains reference");}
 static float floating(Object v){return (Float)argument(v,"F");}
 static double doubleValue(Object v){return (Double)argument(v,"D");}
 static long longValue(Object v){return (Long)argument(v,"J");}
 static int fpCompare(double x,double y,boolean greaterOnNaN){
  if(Double.isNaN(x)||Double.isNaN(y))return greaterOnNaN?1:-1;
  return x>y?1:x<y?-1:0;
 }
 static Object wrap(Object v,String d){return reference(d)?new Ref(v):v;}
 static Object argument(Object v,String d){
  if(reference(d))return ref(v);
  switch(d){case "Z":return integer(v)!=0;case "B":return (byte)integer(v);case "S":return (short)integer(v);case "C":return (char)integer(v);case "I":return integer(v);case "J":return v instanceof Bits?((Bits)v).value:((Number)v).longValue();case "F":return v instanceof Float?v:Float.intBitsToFloat(integer(v));case "D":return v instanceof Bits?Double.longBitsToDouble(((Bits)v).value):((Number)v).doubleValue();case "V":return null;default:throw new Unsupported(d);}
 }
 static boolean zero(Object v){if(v instanceof Ref)return ((Ref)v).value==null;return v==null||integer(v)==0;}
 static boolean equal(Object a,Object b){if(a instanceof Ref||b instanceof Ref)return ref(a)==ref(b);return integer(a)==integer(b);}
 static int a(Instruction i){return ((OneRegisterInstruction)i).getRegisterA();}
 static int b(Instruction i){return ((TwoRegisterInstruction)i).getRegisterB();}
 static int c(Instruction i){return ((ThreeRegisterInstruction)i).getRegisterC();}
 static int offset(Instruction i){return ((OffsetInstruction)i).getCodeOffset();}
 static int[] regs(Instruction i){int n=((VariableRegisterInstruction)i).getRegisterCount();int[] out=new int[n];if(i instanceof RegisterRangeInstruction){int start=((RegisterRangeInstruction)i).getStartRegister();for(int k=0;k<n;k++)out[k]=start+k;}else{var v=(FiveRegisterInstruction)i;int[] values={v.getRegisterC(),v.getRegisterD(),v.getRegisterE(),v.getRegisterF(),v.getRegisterG()};System.arraycopy(values,0,out,0,n);}return out;}
 static java.lang.reflect.Field field(Class<?> owner,String name) throws Exception {for(Class<?> t=owner;t!=null;t=t.getSuperclass())try{java.lang.reflect.Field f=t.getDeclaredField(name);f.setAccessible(true);return f;}catch(NoSuchFieldException e){}throw new NoSuchFieldException(owner.getName()+"."+name);}
 static java.lang.reflect.Method method(Class<?> owner,String name,Class<?>[] params) throws Exception {try{return owner.getMethod(name,params);}catch(NoSuchMethodException e){for(Class<?> t=owner;t!=null;t=t.getSuperclass())try{var m=t.getDeclaredMethod(name,params);m.setAccessible(true);return m;}catch(NoSuchMethodException ignore){}throw e;}}
 Object invoke(String key,Object... args) throws Throwable {
  var m=methods.get(key);if(m==null)throw new Unsupported("Unselected method: "+key);
  if(++depth>48)throw new Unsupported("Recursion limit");try{return execute(m,args);}finally{depth--;}
 }
 Object call(MethodReference target,String op,Object[] args) throws Throwable {
  boolean stat=op.startsWith("INVOKE_STATIC");String chosen=key(target);
  if(defpackage.EngineRuntime.active){
   if(chosen.equals("Ljava/lang/System;->currentTimeMillis()J"))return defpackage.EngineRuntime.now();
   if(chosen.equals("Ljava/lang/System;->nanoTime()J"))return defpackage.EngineRuntime.nanoTime();
   if(chosen.equals("Ljava/lang/Thread;->sleep(J)V")){defpackage.EngineRuntime.sleep((Long)args[0]);return null;}
   if(chosen.equals("Ljava/util/concurrent/CountDownLatch;->await(JLjava/util/concurrent/TimeUnit;)Z"))return defpackage.EngineRuntime.await((java.util.concurrent.CountDownLatch)args[0],(Long)args[1],(java.util.concurrent.TimeUnit)args[2]);
   if(chosen.equals("Ljava/lang/Thread;->start()V")){defpackage.EngineRuntime.start((Thread)args[0]);return null;}
  }
  if(chosen.equals("Ljava/util/Calendar;->getInstance()Ljava/util/Calendar;") && defpackage.TestClock.enabled) return defpackage.TestClock.calendar();
  if(!stat&&!op.startsWith("INVOKE_SUPER")&&args[0]!=null){
   for(Class<?> t=args[0].getClass();t!=null;t=t.getSuperclass()){
    String candidate=descriptor(t)+"->"+sig(target);if(methods.containsKey(candidate)){chosen=candidate;break;}
   }
  }
  if(methods.containsKey(chosen))return invoke(chosen,args);
  Class<?> owner=type(target.getDefiningClass());Class<?>[] pts=new Class<?>[target.getParameterTypes().size()];for(int k=0;k<pts.length;k++)pts[k]=type(target.getParameterTypes().get(k).toString());
  try{return method(owner,target.getName(),pts).invoke(stat?null:args[0],stat?args:Arrays.copyOfRange(args,1,args.length));}
  catch(InvocationTargetException e){throw e.getCause();}
 }
 static final class Frame {
  final com.android.tools.smali.dexlib2.iface.Method method;final MethodImplementation implementation;final Object[] registers;final Map<Integer,Instruction> instructions;
  Object result,returned;Throwable thrown;int pc,steps;boolean done;
  Frame(com.android.tools.smali.dexlib2.iface.Method m,MethodImplementation i,Object[] r,Map<Integer,Instruction> c){method=m;implementation=i;registers=r;instructions=c;}
 }
 static final class Escaped extends Exception {final Throwable error;Escaped(Throwable t){super(null,null,false,false);error=t;}}
 Object execute(com.android.tools.smali.dexlib2.iface.Method m,Object[] args) throws Throwable {
  MethodImplementation impl=m.getImplementation();if(impl==null)throw new Unsupported("No implementation: "+key(m));
  Object[] r=new Object[impl.getRegisterCount()];Arrays.fill(r,UNDEFINED);boolean stat=(m.getAccessFlags()&8)!=0;List<String> pars=new ArrayList<>();if(!stat)pars.add(m.getDefiningClass());for(CharSequence t:m.getParameterTypes())pars.add(t.toString());
  if(pars.size()!=args.length)throw new Unsupported("Argument arity "+key(m));int words=0;for(String t:pars)words+=(t.equals("J")||t.equals("D"))?2:1;int start=r.length-words;
  for(int k=0;k<args.length;k++){r[start]=wrap(args[k],pars.get(k));start+=(pars.get(k).equals("J")||pars.get(k).equals("D"))?2:1;}
  Map<Integer,Instruction> code=new HashMap<>();int cursor=0;for(Instruction i:impl.getInstructions()){code.put(cursor,i);cursor+=i.getCodeUnits();}
  Frame frame=new Frame(m,impl,r,code);
  try{runFrame(frame,null);}catch(Escaped escaped){throw escaped.error;}
  if(!frame.done)throw new Unsupported("Method left frame without return "+key(m));return frame.returned;
 }
 void runFrame(Frame frame,Object heldMonitor)throws Throwable {
  var m=frame.method;var impl=frame.implementation;Object[] r=frame.registers;var code=frame.instructions;
  while(true){
   int pc=frame.pc;if(++frame.steps>2000000)throw new Unsupported("Instruction budget exceeded "+key(m));Instruction i=code.get(pc);if(i==null)throw new Unsupported("Invalid pc "+pc+" in "+key(m));String op=i.getOpcode().name();int next=pc+i.getCodeUnits();
   executed.computeIfAbsent(key(m),k->new TreeSet<>()).add(pc);
   try {
    switch(op){
     case "NOP":break;
     case "MONITOR_ENTER":{Object lock=ref(r[a(i)]);if(lock==null)throw new NullPointerException();frame.pc=next;
      synchronized(lock){try{runFrame(frame,lock);}catch(Unsupported e){throw e;}catch(Escaped e){throw e;}catch(Throwable e){throw new Escaped(e);}}
      if(frame.done)throw new Unsupported("Returned through unbalanced monitor");next=frame.pc;break;}
     case "MONITOR_EXIT":{Object lock=ref(r[a(i)]);if(lock==null)throw new NullPointerException();if(!Thread.holdsLock(lock))throw new IllegalMonitorStateException();if(heldMonitor!=lock)throw new Unsupported("Crossed or unbalanced monitor exits");frame.pc=next;return;}
     case "CONST_4":case "CONST_16":case "CONST":case "CONST_HIGH16":r[a(i)]=((NarrowLiteralInstruction)i).getNarrowLiteral();break;
     case "CONST_WIDE_16":case "CONST_WIDE_32":case "CONST_WIDE":case "CONST_WIDE_HIGH16":r[a(i)]=new Bits(((WideLiteralInstruction)i).getWideLiteral());break;
     case "CONST_STRING":case "CONST_STRING_JUMBO":r[a(i)]=new Ref(((StringReference)((ReferenceInstruction)i).getReference()).getString());break;
     case "FLOAT_TO_INT":r[a(i)]=(int)floating(r[b(i)]);break;
     case "CONST_CLASS":r[a(i)]=new Ref(type(((TypeReference)((ReferenceInstruction)i).getReference()).getType()));break;
     case "MOVE":case "MOVE_FROM16":case "MOVE_16":case "MOVE_OBJECT":case "MOVE_OBJECT_FROM16":case "MOVE_OBJECT_16":case "MOVE_WIDE":case "MOVE_WIDE_FROM16":case "MOVE_WIDE_16":r[a(i)]=r[b(i)];break;
     case "MOVE_RESULT":case "MOVE_RESULT_OBJECT":case "MOVE_RESULT_WIDE":r[a(i)]=frame.result;break;
     case "MOVE_EXCEPTION":r[a(i)]=new Ref(frame.thrown);break;
     case "RETURN_VOID":if(heldMonitor!=null)throw new Unsupported("Return before monitor exit");frame.done=true;frame.returned=null;return;
     case "RETURN":case "RETURN_WIDE":case "RETURN_OBJECT":if(heldMonitor!=null)throw new Unsupported("Return before monitor exit");frame.done=true;frame.returned=argument(r[a(i)],m.getReturnType());return;
     case "GOTO":case "GOTO_16":case "GOTO_32":next=pc+offset(i);break;
     case "IF_EQZ":if(zero(r[a(i)]))next=pc+offset(i);break;
     case "IF_NEZ":if(!zero(r[a(i)]))next=pc+offset(i);break;
     case "IF_EQ":if(equal(r[a(i)],r[b(i)]))next=pc+offset(i);break;
     case "IF_NE":if(!equal(r[a(i)],r[b(i)]))next=pc+offset(i);break;
     case "IF_LT":if(integer(r[a(i)])<integer(r[b(i)]))next=pc+offset(i);break;
     case "IF_LE":if(integer(r[a(i)])<=integer(r[b(i)]))next=pc+offset(i);break;
     case "IF_GT":if(integer(r[a(i)])>integer(r[b(i)]))next=pc+offset(i);break;
     case "IF_GE":if(integer(r[a(i)])>=integer(r[b(i)]))next=pc+offset(i);break;
     case "IF_LTZ":if(integer(r[a(i)])<0)next=pc+offset(i);break;
     case "IF_LEZ":if(integer(r[a(i)])<=0)next=pc+offset(i);break;
     case "IF_GTZ":if(integer(r[a(i)])>0)next=pc+offset(i);break;
     case "IF_GEZ":if(integer(r[a(i)])>=0)next=pc+offset(i);break;
     case "ADD_INT_LIT8":case "ADD_INT_LIT16":r[a(i)]=integer(r[b(i)])+((NarrowLiteralInstruction)i).getNarrowLiteral();break;
     case "AND_INT_LIT8":case "AND_INT_LIT16":r[a(i)]=integer(r[b(i)])&((NarrowLiteralInstruction)i).getNarrowLiteral();break;
     case "OR_INT_LIT8":case "OR_INT_LIT16":r[a(i)]=integer(r[b(i)])|((NarrowLiteralInstruction)i).getNarrowLiteral();break;
     case "ADD_INT_2ADDR":r[a(i)]=integer(r[a(i)])+integer(r[b(i)]);break;
     case "AND_INT_2ADDR":r[a(i)]=integer(r[a(i)])&integer(r[b(i)]);break;
     case "OR_INT_2ADDR":r[a(i)]=integer(r[a(i)])|integer(r[b(i)]);break;
     case "SHR_INT_2ADDR":r[a(i)]=integer(r[a(i)])>>(integer(r[b(i)])&31);break;
     case "ADD_INT":r[a(i)]=integer(r[b(i)])+integer(r[c(i)]);break;
     case "SUB_INT":r[a(i)]=integer(r[b(i)])-integer(r[c(i)]);break;
     case "SUB_INT_2ADDR":r[a(i)]=integer(r[a(i)])-integer(r[b(i)]);break;
     case "MUL_LONG":r[a(i)]=longValue(r[b(i)])*longValue(r[c(i)]);break;
     case "MUL_LONG_2ADDR":r[a(i)]=longValue(r[a(i)])*longValue(r[b(i)]);break;
     case "DIV_LONG":r[a(i)]=longValue(r[b(i)])/longValue(r[c(i)]);break;
     case "DIV_LONG_2ADDR":r[a(i)]=longValue(r[a(i)])/longValue(r[b(i)]);break;
     case "SUB_LONG":r[a(i)]=longValue(r[b(i)])-longValue(r[c(i)]);break;
     case "SUB_LONG_2ADDR":r[a(i)]=longValue(r[a(i)])-longValue(r[b(i)]);break;
     case "ADD_LONG":r[a(i)]=longValue(r[b(i)])+longValue(r[c(i)]);break;
     case "ADD_LONG_2ADDR":r[a(i)]=longValue(r[a(i)])+longValue(r[b(i)]);break;
     case "NEG_LONG":r[a(i)]=-longValue(r[b(i)]);break;
     case "INT_TO_CHAR":r[a(i)]=(int)(char)integer(r[b(i)]);break;
     case "LONG_TO_INT":r[a(i)]=(int)longValue(r[b(i)]);break;
     case "DOUBLE_TO_INT":r[a(i)]=(int)doubleValue(r[b(i)]);break;
     case "LONG_TO_DOUBLE":r[a(i)]=(double)longValue(r[b(i)]);break;
     case "DOUBLE_TO_LONG":r[a(i)]=(long)doubleValue(r[b(i)]);break;
     case "INT_TO_LONG":r[a(i)]=(long)integer(r[b(i)]);break;
     case "INT_TO_FLOAT":r[a(i)]=(float)integer(r[b(i)]);break;
     case "INT_TO_DOUBLE":r[a(i)]=(double)integer(r[b(i)]);break;
     case "CMP_LONG":r[a(i)]=Long.compare(longValue(r[b(i)]),longValue(r[c(i)]));break;
     case "CMPL_FLOAT":case "CMPG_FLOAT":r[a(i)]=fpCompare(floating(r[b(i)]),floating(r[c(i)]),op.equals("CMPG_FLOAT"));break;
     case "CMPL_DOUBLE":case "CMPG_DOUBLE":r[a(i)]=fpCompare(doubleValue(r[b(i)]),doubleValue(r[c(i)]),op.equals("CMPG_DOUBLE"));break;
     case "ADD_DOUBLE_2ADDR":r[a(i)]=doubleValue(r[a(i)])+doubleValue(r[b(i)]);break;
     case "SUB_DOUBLE_2ADDR":r[a(i)]=doubleValue(r[a(i)])-doubleValue(r[b(i)]);break;
     case "MUL_DOUBLE_2ADDR":r[a(i)]=doubleValue(r[a(i)])*doubleValue(r[b(i)]);break;
     case "DIV_DOUBLE_2ADDR":r[a(i)]=doubleValue(r[a(i)])/doubleValue(r[b(i)]);break;
     case "ADD_DOUBLE":r[a(i)]=doubleValue(r[b(i)])+doubleValue(r[c(i)]);break;
     case "SUB_DOUBLE":r[a(i)]=doubleValue(r[b(i)])-doubleValue(r[c(i)]);break;
     case "MUL_DOUBLE":r[a(i)]=doubleValue(r[b(i)])*doubleValue(r[c(i)]);break;
     case "DIV_DOUBLE":r[a(i)]=doubleValue(r[b(i)])/doubleValue(r[c(i)]);break;
     case "XOR_INT_2ADDR":r[a(i)]=integer(r[a(i)])^integer(r[b(i)]);break;
     case "XOR_INT_LIT8":case "XOR_INT_LIT16":r[a(i)]=integer(r[b(i)])^((NarrowLiteralInstruction)i).getNarrowLiteral();break;
     case "CHECK_CAST":{Class<?> t=type(((TypeReference)((ReferenceInstruction)i).getReference()).getType());Object o=ref(r[a(i)]);if(o!=null&&!t.isInstance(o))throw new ClassCastException(o.getClass().getName());break;}
     case "INSTANCE_OF":{Class<?> t=type(((TypeReference)((ReferenceInstruction)i).getReference()).getType());r[a(i)]=t.isInstance(ref(r[b(i)]))?1:0;break;}
     case "NEW_INSTANCE":r[a(i)]=new Ref(new Pending(type(((TypeReference)((ReferenceInstruction)i).getReference()).getType())));break;
     case "NEW_ARRAY":{String d=((TypeReference)((ReferenceInstruction)i).getReference()).getType();r[a(i)]=new Ref(Array.newInstance(type(d.substring(1)),integer(r[b(i)])));break;}
     case "ARRAY_LENGTH":r[a(i)]=Array.getLength(ref(r[b(i)]));break;
     case "AGET":case "AGET_OBJECT":case "AGET_WIDE":case "AGET_BOOLEAN":case "AGET_BYTE":case "AGET_CHAR":case "AGET_SHORT":{Object array=ref(r[b(i)]);Object v=Array.get(array,integer(r[c(i)]));r[a(i)]=wrap(v,descriptor(array.getClass().getComponentType()));break;}
     case "APUT":case "APUT_OBJECT":case "APUT_WIDE":case "APUT_BOOLEAN":case "APUT_BYTE":case "APUT_CHAR":case "APUT_SHORT":{Object array=ref(r[b(i)]);Array.set(array,integer(r[c(i)]),argument(r[a(i)],descriptor(array.getClass().getComponentType())));break;}
     case "FILLED_NEW_ARRAY":case "FILLED_NEW_ARRAY_RANGE":{String d=((TypeReference)((ReferenceInstruction)i).getReference()).getType();int[] rs=regs(i);Object array=Array.newInstance(type(d.substring(1)),rs.length);for(int k=0;k<rs.length;k++)Array.set(array,k,argument(r[rs[k]],d.substring(1)));frame.result=new Ref(array);break;}
     case "FILL_ARRAY_DATA":{Object array=ref(r[a(i)]);ArrayPayload data=(ArrayPayload)code.get(pc+offset(i));int k=0;String d=descriptor(array.getClass().getComponentType());for(Number n:data.getArrayElements())Array.set(array,k++,argument(n,d));break;}
     case "PACKED_SWITCH":case "SPARSE_SWITCH":{SwitchPayload data=(SwitchPayload)code.get(pc+offset(i));for(SwitchElement e:data.getSwitchElements())if(e.getKey()==integer(r[a(i)])){next=pc+e.getOffset();break;}break;}
     case "IGET_OBJECT":case "IGET":case "IGET_WIDE":case "IGET_BOOLEAN":case "IGET_BYTE":case "IGET_CHAR":case "IGET_SHORT":{FieldReference f=(FieldReference)((ReferenceInstruction)i).getReference();r[a(i)]=wrap(field(type(f.getDefiningClass()),f.getName()).get(ref(r[b(i)])),f.getType());break;}
     case "IPUT_OBJECT":case "IPUT":case "IPUT_WIDE":case "IPUT_BOOLEAN":case "IPUT_BYTE":case "IPUT_CHAR":case "IPUT_SHORT":{FieldReference f=(FieldReference)((ReferenceInstruction)i).getReference();field(type(f.getDefiningClass()),f.getName()).set(ref(r[b(i)]),argument(r[a(i)],f.getType()));break;}
     case "SGET_OBJECT":case "SGET":case "SGET_WIDE":case "SGET_BOOLEAN":{FieldReference f=(FieldReference)((ReferenceInstruction)i).getReference();r[a(i)]=wrap(field(type(f.getDefiningClass()),f.getName()).get(null),f.getType());break;}
     case "THROW":throw (Throwable)ref(r[a(i)]);
     default:
      if(op.startsWith("INVOKE_")){
       MethodReference target=(MethodReference)((ReferenceInstruction)i).getReference();int[] rs=regs(i);boolean isStatic=op.startsWith("INVOKE_STATIC");List<Object> arguments=new ArrayList<>();int k=0;
       if(!isStatic)arguments.add(ref(r[rs[k++]]));
       for(CharSequence pt:target.getParameterTypes()){String d=pt.toString();arguments.add(argument(r[rs[k]],d));k+=d.equals("J")||d.equals("D")?2:1;}
       if(target.getName().equals("<init>")){
        Object pending=arguments.get(0);if(!(pending instanceof Pending))throw new Unsupported("Constructor receiver already initialized");Class<?>[] pts=new Class<?>[target.getParameterTypes().size()];for(int q=0;q<pts.length;q++)pts[q]=type(target.getParameterTypes().get(q).toString());Object initialized;
        try{var constructor=((Pending)pending).type.getDeclaredConstructor(pts);constructor.setAccessible(true);initialized=constructor.newInstance(arguments.subList(1,arguments.size()).toArray());}catch(InvocationTargetException e){throw e.getCause();}
        for(Object cell:r)if(cell instanceof Ref&&((Ref)cell).value==pending)((Ref)cell).value=initialized;frame.result=null;
       }else{Object value=call(target,op,arguments.toArray());frame.result=wrap(value,target.getReturnType());}
      }else throw new Unsupported("Unsupported opcode "+op+" in "+key(m));
    }
   }catch(Escaped escaped){throw escaped;}catch(Unsupported error){throw error;}catch(Throwable error){
    int catchPc=op.equals("MONITOR_EXIT")?next:pc;int handler=-1;for(var t:impl.getTryBlocks())if(catchPc>=t.getStartCodeAddress()&&catchPc<t.getStartCodeAddress()+t.getCodeUnitCount())for(var h:t.getExceptionHandlers())if(h.getExceptionType()==null||type(h.getExceptionType()).isInstance(error)){handler=h.getHandlerCodeAddress();break;}
    if(handler<0)throw error;frame.thrown=error;next=handler;
   }
   if(op.startsWith("IF_")||op.equals("PACKED_SWITCH")||op.equals("SPARSE_SWITCH"))branchEdges.computeIfAbsent(key(m),k->new TreeSet<>()).add(pc+":"+next);
   frame.pc=next;
  }
 }
}
