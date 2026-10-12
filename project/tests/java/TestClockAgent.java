import java.lang.instrument.*;
import java.security.ProtectionDomain;
import java.util.*;
import org.objectweb.asm.*;
/** Freezes the recovered-host Calendar boundary, matching the instruction oracle.
 * Only test JVM loaded recovered/* bytecode is transformed. Not an Android agent.
 */
public final class TestClockAgent {
 public static final Set<String> changed=Collections.synchronizedSet(new TreeSet<>());
 public static void premain(String args,Instrumentation instrumentation){
  defpackage.TestClock.agentInstalled=true;
  instrumentation.addTransformer(new ClassFileTransformer(){
   @Override public byte[] transform(ClassLoader loader,String name,Class<?> type,ProtectionDomain domain,byte[] data){
    if(name==null || !name.startsWith("recovered/"))return null;
    final int[] sites={0};ClassReader reader=new ClassReader(data);ClassWriter writer=new ClassWriter(0);
    reader.accept(new ClassVisitor(Opcodes.ASM9,writer){
     @Override public MethodVisitor visitMethod(int access,String n,String d,String s,String[] ex){
      return new MethodVisitor(Opcodes.ASM9,super.visitMethod(access,n,d,s,ex)){
       @Override public void visitMethodInsn(int opcode,String owner,String method,String desc,boolean itf){
        if(opcode==Opcodes.INVOKESTATIC && owner.equals("java/util/Calendar") && method.equals("getInstance") && desc.equals("()Ljava/util/Calendar;")){
         sites[0]++;super.visitMethodInsn(opcode,"defpackage/TestClock","calendar",desc,false);
        }else if(name.startsWith("recovered/engine/") && opcode==Opcodes.INVOKESTATIC && owner.equals("java/lang/System") && method.equals("currentTimeMillis") && desc.equals("()J")){
         sites[0]++;super.visitMethodInsn(Opcodes.INVOKESTATIC,"defpackage/EngineRuntime","now",desc,false);
        }else if(name.startsWith("recovered/engine/") && opcode==Opcodes.INVOKESTATIC && owner.equals("java/lang/System") && method.equals("nanoTime") && desc.equals("()J")){
         sites[0]++;super.visitMethodInsn(Opcodes.INVOKESTATIC,"defpackage/EngineRuntime","nanoTime",desc,false);
        }else if(name.startsWith("recovered/engine/") && opcode==Opcodes.INVOKESTATIC && owner.equals("java/lang/Thread") && method.equals("sleep") && desc.equals("(J)V")){
         sites[0]++;super.visitMethodInsn(Opcodes.INVOKESTATIC,"defpackage/EngineRuntime","sleep",desc,false);
        }else if(name.startsWith("recovered/engine/") && opcode==Opcodes.INVOKEVIRTUAL && owner.equals("java/util/concurrent/CountDownLatch") && method.equals("await") && desc.equals("(JLjava/util/concurrent/TimeUnit;)Z")){
         sites[0]++;super.visitMethodInsn(Opcodes.INVOKESTATIC,"defpackage/EngineRuntime","await","(Ljava/util/concurrent/CountDownLatch;JLjava/util/concurrent/TimeUnit;)Z",false);
        }else if(name.startsWith("recovered/engine/") && opcode==Opcodes.INVOKEVIRTUAL && owner.equals("java/lang/Thread") && method.equals("start") && desc.equals("()V")){
         sites[0]++;super.visitMethodInsn(Opcodes.INVOKESTATIC,"defpackage/EngineRuntime","start","(Ljava/lang/Thread;)V",false);
        }else super.visitMethodInsn(opcode,owner,method,desc,itf);
       }
      };
     }
    },0);
    if(sites[0]==0)return null;changed.add(name+":"+sites[0]);return writer.toByteArray();
   }
  });
 }
}
