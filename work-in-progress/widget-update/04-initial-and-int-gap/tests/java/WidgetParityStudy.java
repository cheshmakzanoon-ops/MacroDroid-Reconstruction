import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** Standalone one-method entry point sharing the normal UI comparison and case code. */
public final class WidgetParityStudy {
    public static void main(String[] args)throws Exception {
        if(args.length!=3)throw new IllegalArgumentException("Expected proposed entry, original fixture, and report path");
        JsonObject entry=JsonParser.parseString(Files.readString(Paths.get(args[0]))).getAsJsonObject();
        String key=entry.get("target").getAsString()+"->"+entry.get("method").getAsString();
        if(!WidgetParityCases.KEY.equals(key))throw new IllegalArgumentException("Study entry does not identify the Widget method");
        UiParityTests.registry.put(key,entry);
        UiParityTests.original=new BytecodeOracle(Paths.get(args[1]),UiParityTests.registry.keySet());
        if(UiParityTests.original.methods.size()!=1)throw new IllegalStateException("Original one-method fixture incomplete");
        WidgetParityCases.configure(UiParityTests.original);
        WidgetParityCases.run();

        Set<Integer> visited=UiParityTests.original.executed.getOrDefault(key,Collections.emptySet());
        Set<String> edges=UiParityTests.original.branchEdges.getOrDefault(key,Collections.emptySet());
        List<Integer> unseen=new ArrayList<Integer>();List<String> missingEdges=new ArrayList<String>();
        int offset=0,total=0,possibleEdges=0;
        for(var instruction:UiParityTests.original.methods.get(key).getImplementation().getInstructions()){
            if(!visited.contains(offset))unseen.add(offset);
            if(instruction.getOpcode().name().startsWith("IF_")){
                possibleEdges+=2;
                int jump=offset+((com.android.tools.smali.dexlib2.iface.instruction.OffsetInstruction)instruction).getCodeOffset();
                for(int target:new int[]{offset+instruction.getCodeUnits(),jump})if(!edges.contains(offset+":"+target))missingEdges.add(offset+":"+target);
            }
            offset+=instruction.getCodeUnits();total++;
        }
        JsonObject coverage=new JsonObject();coverage.addProperty("instructions",total);coverage.addProperty("visited",visited.size());coverage.add("unvisitedOffsets",UiParityTests.G.toJsonTree(unseen));
        coverage.addProperty("conditionalEdges",possibleEdges);coverage.addProperty("conditionalEdgesVisited",possibleEdges-missingEdges.size());coverage.add("unvisitedConditionalEdges",UiParityTests.G.toJsonTree(missingEdges));
        boolean complete=UiParityTests.counts.keySet().equals(UiParityTests.registry.keySet())&&unseen.isEmpty()&&missingEdges.isEmpty();
        JsonObject report=new JsonObject();report.addProperty("passed",complete&&UiParityTests.mismatches==0&&UiParityTests.unsupported==0);
        report.addProperty("cases",UiParityTests.cases);report.addProperty("failedCases",UiParityTests.mismatches);report.addProperty("unsupportedExecutions",UiParityTests.unsupported);
        report.addProperty("independentExpectedResultChecks",UiParityTests.expectedChecks);report.addProperty("expectedResultFailures",UiParityTests.expectedFailures);
        report.addProperty("methodsCovered",UiParityTests.counts.size());report.add("methodKeys",UiParityTests.G.toJsonTree(UiParityTests.counts.keySet()));report.addProperty("paths",2);
        report.addProperty("androidRuntime",false);report.addProperty("rebuiltDexCompared",false);report.addProperty("registeredInActiveProject",false);
        report.add("instructionCoverage",coverage);report.addProperty("fullInstructionAndConditionalCoverage",unseen.isEmpty()&&missingEdges.isEmpty());
        report.add("failures",UiParityTests.G.toJsonTree(UiParityTests.failures));report.add("failedCaseLabels",UiParityTests.G.toJsonTree(UiParityTests.failedLabels));
        report.add("hostParentConstructorAdapters",UiParityTests.G.toJsonTree(UiParityTests.original.parentConstructorAdapters));
        report.add("hostParentConstructorAdapterCalls",UiParityTests.G.toJsonTree(UiParityTests.original.parentConstructorAdapterCalls));
        report.addProperty("constructorScope","Exact method-scoped DEX owner validation with a compile-only child reflection adapter; not ART verification");
        report.addProperty("invalidLabelDefensiveReturnUsesOneInjectedReturningBoundary",true);
        report.addProperty("scope","Bounded selected original method/JVM comparison; no widget service, rendering, coroutine scheduler, application build or Android execution");
        Files.writeString(Paths.get(args[2]),UiParityTests.G.toJson(report)+"\n");
        System.out.println("Widget cases="+UiParityTests.cases+" mismatches="+UiParityTests.mismatches+" unsupported="+UiParityTests.unsupported+" expected="+UiParityTests.expectedChecks+" coverage="+visited.size()+"/"+total+" edges="+(possibleEdges-missingEdges.size())+"/"+possibleEdges);
        if(!report.get("passed").getAsBoolean())System.exit(2);
    }
}
