import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Read-only instruction/exception-table and actual pinned JRT class inventory. */
public final class VideoHandlerInventory {
    static String signature(MethodReference method){return method.getName()+"("+String.join("",method.getParameterTypes())+")"+method.getReturnType();}
    static String reference(Reference value){
        if(value instanceof MethodReference method)return method.getDefiningClass()+"->"+signature(method);
        if(value instanceof FieldReference field)return field.getDefiningClass()+"->"+field.getName()+":"+field.getType();
        if(value instanceof TypeReference type)return type.getType();
        if(value instanceof StringReference text)return text.getString();
        return value.toString();
    }
    public static void main(String[] args)throws Exception {
        if(args.length!=2)throw new IllegalArgumentException("Expected original method fixture and output directory");
        Path out=Path.of(args[1]);
        var dex=DexFileFactory.loadDexFile(Path.of(args[0]).toFile(),Opcodes.forApi(23));
        Method selected=null;
        for(ClassDef type:dex.getClasses())for(Method method:type.getMethods()){
            if((type.getType()+"->"+signature(method)).equals("Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;")){
                if(selected!=null)throw new IllegalArgumentException("Duplicate selected body");selected=method;
            }
        }
        if(selected==null)throw new IllegalArgumentException("Missing selected body");
        JsonArray instructions=new JsonArray(),regions=new JsonArray();int offset=0;
        for(Instruction instruction:selected.getImplementation().getInstructions()){
            JsonObject row=new JsonObject();row.addProperty("offset",offset);row.addProperty("opcode",instruction.getOpcode().name());row.addProperty("units",instruction.getCodeUnits());
            if(instruction instanceof OneRegisterInstruction registers)row.addProperty("A",registers.getRegisterA());
            if(instruction instanceof TwoRegisterInstruction registers)row.addProperty("B",registers.getRegisterB());
            if(instruction instanceof ThreeRegisterInstruction registers)row.addProperty("C",registers.getRegisterC());
            if(instruction instanceof FiveRegisterInstruction registers){row.add("invokeRegisters",new Gson().toJsonTree(Arrays.asList(registers.getRegisterC(),registers.getRegisterD(),registers.getRegisterE(),registers.getRegisterF(),registers.getRegisterG()).subList(0,registers.getRegisterCount())));}
            if(instruction instanceof RegisterRangeInstruction registers){row.addProperty("firstRegister",registers.getStartRegister());row.addProperty("registerCount",registers.getRegisterCount());}
            if(instruction instanceof WideLiteralInstruction literal)row.addProperty("literal",literal.getWideLiteral());
            if(instruction instanceof ReferenceInstruction referred)row.addProperty("reference",reference(referred.getReference()));
            if(instruction instanceof OffsetInstruction branch)row.addProperty("target",offset+branch.getCodeOffset());
            instructions.add(row);offset+=instruction.getCodeUnits();
        }
        for(TryBlock<? extends ExceptionHandler> block:selected.getImplementation().getTryBlocks()){
            JsonObject row=new JsonObject();row.addProperty("start",block.getStartCodeAddress());row.addProperty("end",block.getStartCodeAddress()+block.getCodeUnitCount());JsonArray handlers=new JsonArray();
            for(ExceptionHandler handler:block.getExceptionHandlers()){JsonObject target=new JsonObject();target.addProperty("type",handler.getExceptionType());target.addProperty("offset",handler.getHandlerCodeAddress());handlers.add(target);}row.add("handlers",handlers);regions.add(row);
        }
        JsonObject report=new JsonObject();report.addProperty("scope","Metadata only; no selected app method is executed and no original coverage credit is added");report.add("instructions",instructions);report.add("exceptionRegions",regions);
        Files.writeString(out.resolve("original-instructions.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(report)+"\n");
        Path classes=out.resolve("jrt-classfiles");Files.createDirectory(classes);
        for(String name:List.of("java.lang.StringBuilder","java.lang.AbstractStringBuilder","java.lang.StringUTF16","java.lang.Object")){
            Class<?> type=Class.forName(name,false,null);String shortName=name.substring(name.lastIndexOf('.')+1);
            try(var input=type.getResourceAsStream(shortName+".class")){
                if(input==null)throw new IllegalArgumentException("Missing JRT class resource");Files.write(classes.resolve(shortName+".class"),input.readAllBytes());
            }
        }
        System.out.println("Original instruction rows="+instructions.size()+"; exception regions="+regions.size()+"; actual JRT class files=4; app executions=0");
    }
}
