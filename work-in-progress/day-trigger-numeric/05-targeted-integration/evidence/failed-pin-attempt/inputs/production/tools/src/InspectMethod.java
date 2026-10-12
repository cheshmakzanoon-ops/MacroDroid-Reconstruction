import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;
/** Instruction-offset listing for comparing a recovered method with the original DEX. */
public final class InspectMethod {
    public static void main(String[] args) throws Exception {
        if (args.length != 3) throw new IllegalArgumentException("DEX owner->signature OUTPUT.json");
        var dex = DexFileFactory.loadDexFile(args[0], Opcodes.forApi(23));
        Method found = null;
        for (ClassDef c : dex.getClasses()) for (Method m : c.getMethods()) {
            String key = c.getType() + "->" + m.getName() + "(" + String.join("", m.getParameterTypes()) + ")" + m.getReturnType();
            if (key.equals(args[1])) found = m;
        }
        if (found == null || found.getImplementation() == null) throw new IllegalArgumentException("Method not found or no body");
        List<Object> rows = new ArrayList<>();
        int pc = 0;
        for (Instruction i : found.getImplementation().getInstructions()) {
            Map<String,Object> r = new LinkedHashMap<>();
            r.put("pc", pc); r.put("hex", "0x" + Integer.toHexString(pc)); r.put("opcode", i.getOpcode().name);
            List<Integer> registers = new ArrayList<>();
            if (i instanceof RegisterRangeInstruction x) for (int k = 0; k < x.getRegisterCount(); k++) registers.add(x.getStartRegister()+k);
            else if (i instanceof FiveRegisterInstruction x) {
                int[] values = {x.getRegisterC(), x.getRegisterD(), x.getRegisterE(), x.getRegisterF(), x.getRegisterG()};
                for (int k=0; k<x.getRegisterCount(); k++) registers.add(values[k]);
            } else if (i instanceof ThreeRegisterInstruction x) registers.addAll(List.of(x.getRegisterA(),x.getRegisterB(),x.getRegisterC()));
            else if (i instanceof TwoRegisterInstruction x) registers.addAll(List.of(x.getRegisterA(),x.getRegisterB()));
            else if (i instanceof OneRegisterInstruction x) registers.add(x.getRegisterA());
            r.put("registers",registers);
            if (i instanceof WideLiteralInstruction x) r.put("literal",x.getWideLiteral());
            if (i instanceof OffsetInstruction x) r.put("branchTarget",pc+x.getCodeOffset());
            if (i instanceof ReferenceInstruction x) r.put("reference",x.getReference().toString());
            rows.add(r); pc += i.getCodeUnits();
        }
        List<Object> handlers=new ArrayList<>();
        for (var t: found.getImplementation().getTryBlocks()) for (var h:t.getExceptionHandlers()) {
            Map<String,Object> r=new LinkedHashMap<>();r.put("start",t.getStartCodeAddress());r.put("end",t.getStartCodeAddress()+t.getCodeUnitCount());r.put("type",h.getExceptionType());r.put("handler",h.getHandlerCodeAddress());handlers.add(r);
        }
        Map<String,Object> result=new LinkedHashMap<>();result.put("method",args[1]);result.put("registerCount",found.getImplementation().getRegisterCount());result.put("instructions",rows);result.put("handlers",handlers);
        Files.writeString(Path.of(args[2]),new GsonBuilder().serializeNulls().setPrettyPrinting().create().toJson(result));
    }
}
