import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** One selected method, sharing the normal comparison and case infrastructure. */
public final class VideoParityStudy {
    public static void main(String[] args)throws Exception {
        if(args.length!=3)throw new IllegalArgumentException("Expected proposed entry, original fixture and report path");
        JsonObject entry=JsonParser.parseString(Files.readString(Paths.get(args[0]))).getAsJsonObject();
        String key=entry.get("target").getAsString()+"->"+entry.get("method").getAsString();
        if(!VideoParityCases.KEY.equals(key)||entry.has("constructor_owner_mappings"))throw new IllegalArgumentException("Unexpected video study entry");
        UiParityTests.registry.put(key,entry);
        UiParityTests.original=new BytecodeOracle(Paths.get(args[1]),UiParityTests.registry.keySet());
        if(UiParityTests.original.methods.size()!=1)throw new IllegalStateException("Exact original one-method fixture required");
        VideoParityCases.run();
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
        boolean noAdapter=UiParityTests.original.parentConstructorAdapters.isEmpty()&&UiParityTests.original.parentConstructorAdapterCalls.isEmpty();
        JsonObject report=new JsonObject();report.addProperty("passed",complete&&noAdapter&&UiParityTests.mismatches==0&&UiParityTests.unsupported==0&&UiParityTests.expectedFailures==0);
        report.addProperty("cases",UiParityTests.cases);report.addProperty("failedCases",UiParityTests.mismatches);report.addProperty("unsupportedExecutions",UiParityTests.unsupported);
        report.addProperty("independentExpectedResultChecks",UiParityTests.expectedChecks);report.addProperty("expectedResultFailures",UiParityTests.expectedFailures);
        report.addProperty("originalOnlyBoundaryDiscoveryExecutions",VideoParityCases.discoveryExecutions);
        report.addProperty("methodsCovered",UiParityTests.counts.size());report.add("methodKeys",UiParityTests.G.toJsonTree(UiParityTests.counts.keySet()));report.addProperty("paths",2);
        report.addProperty("androidRuntime",false);report.addProperty("rebuiltDexCompared",false);report.addProperty("registeredInActiveProject",false);
        report.add("instructionCoverage",coverage);report.addProperty("fullInstructionAndConditionalCoverage",unseen.isEmpty()&&missingEdges.isEmpty());
        report.add("failures",UiParityTests.G.toJsonTree(UiParityTests.failures));report.add("failedCaseLabels",UiParityTests.G.toJsonTree(UiParityTests.failedLabels));
        report.add("hostParentConstructorAdapters",UiParityTests.G.toJsonTree(UiParityTests.original.parentConstructorAdapters));
        report.add("hostParentConstructorAdapterCalls",UiParityTests.G.toJsonTree(UiParityTests.original.parentConstructorAdapterCalls));
        report.addProperty("noConstructorOwnerAdapterUsed",noAdapter);
        report.addProperty("invalidLabelDefensiveReturnUsesOneInjectedReturningBoundary",true);
        report.add("generatedEscapedMessageExclusions",UiParityTests.G.toJsonTree(VideoParityCases.generatedEscapedMessages));
        report.addProperty("exceptionMessageScope","Only VM-generated escaped cast/null wording is excluded with raw messages retained. Injected and external exception identities/messages and all logged text remain exact.");
        report.addProperty("scope","Bounded selected original method/JVM comparison with controlled File/storage/logging/coroutine boundaries; no filesystem operation, scheduler, Android service, APK build or Android execution");
        Files.writeString(Paths.get(args[2]),UiParityTests.G.toJson(report)+"\n");
        System.out.println("Video cases="+UiParityTests.cases+" mismatches="+UiParityTests.mismatches+" unsupported="+UiParityTests.unsupported+" expected="+UiParityTests.expectedChecks+" coverage="+visited.size()+"/"+total+" edges="+(possibleEdges-missingEdges.size())+"/"+possibleEdges);
        if(!report.get("passed").getAsBoolean())System.exit(2);
    }
}
