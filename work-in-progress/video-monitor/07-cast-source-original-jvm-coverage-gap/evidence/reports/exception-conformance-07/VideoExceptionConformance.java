import com.google.gson.*;
import defpackage.*;
import java.nio.file.*;
import java.util.*;

/** Host observation controls only; does not execute any original or recovered app body. */
public final class VideoExceptionConformance {
    static final String STRING_FILE="class java.lang.String cannot be cast to class java.io.File (java.lang.String and java.io.File are in module java.base of loader 'bootstrap')";
    static final String STRING_FLAG="class java.lang.String cannot be cast to class defpackage.qnc (java.lang.String is in module java.base of loader 'bootstrap'; defpackage.qnc is in unnamed module of loader 'app')";
    static final String FILE_FLAG="class defpackage.VideoFile cannot be cast to class defpackage.qnc (defpackage.VideoFile and defpackage.qnc are in unnamed module of loader 'app')";
    static final String FLAG_FILE="class defpackage.qnc cannot be cast to class java.io.File (defpackage.qnc is in unnamed module of loader 'app'; java.io.File is in module java.base of loader 'bootstrap')";
    static final List<JsonObject> results=new ArrayList<JsonObject>();
    static void check(String label,boolean passed){JsonObject row=new JsonObject();row.addProperty("label",label);row.addProperty("passed",passed);results.add(row);if(!passed)throw new AssertionError(label);}
    static void reject(String label,String path,String text){boolean refused=false;try{VideoParityCases.generatedCastSource(path,text);}catch(IllegalStateException expected){refused=true;}check(label,refused);}
    public static void main(String[] args)throws Exception{
        if(args.length!=1)throw new IllegalArgumentException("Expected fresh report path");
        JsonObject report=new JsonObject();
        try{
            for(String path:new String[]{"original","rebuilt"})for(String source:new String[]{"java.lang.String","defpackage.qnc","defpackage.VideoFile"})check("exact-"+path+":"+source,source.equals(VideoParityCases.generatedCastSource(path,source)));
            for(String[] row:new String[][]{{STRING_FILE,"java.lang.String"},{STRING_FLAG,"java.lang.String"},{FILE_FLAG,"defpackage.VideoFile"},{FLAG_FILE,"defpackage.qnc"}})check("exact-java:"+row[0],row[1].equals(VideoParityCases.generatedCastSource("java",row[0])));
            check("distinct-source-type-order-remains-visible",!VideoParityCases.generatedCastSource("original","defpackage.qnc").equals(VideoParityCases.generatedCastSource("java",FILE_FLAG)));
            check("altered-source-type-remains-a-mismatch",!VideoParityCases.generatedCastSource("java",FLAG_FILE).equals(VideoParityCases.generatedCastSource("java",FILE_FLAG)));
            check("same-source-type-targets-explicitly-not-distinguished",VideoParityCases.generatedCastSource("java",STRING_FILE).equals(VideoParityCases.generatedCastSource("java",STRING_FLAG)));
            reject("altered-target","java",FLAG_FILE.replace("to class java.io.File","to class java.lang.Number"));
            reject("impossible-same-source-target","java",FLAG_FILE.replace("to class java.io.File","to class defpackage.qnc"));
            reject("altered-source","java",FLAG_FILE.replace("class defpackage.qnc cannot","class java.lang.Integer cannot"));
            reject("changed-loader","java",FILE_FLAG.replace("loader 'app'","loader 'other'"));
            reject("extra-newline","java",STRING_FILE+"\n");
            reject("extra-space","java",STRING_FILE+" ");
            reject("wrong-path","unexpected",STRING_FILE);
            reject("unexpected-java-message","java","unrecognized generated wording");
            reject("null-java-message","java",null);
            reject("oracle-form-as-java","java","java.lang.String");
            reject("java-form-as-oracle","original",STRING_FILE);
            reject("unexpected-oracle-source","original","java.lang.Integer");
            reject("null-oracle-message","original",null);
            String[] forms={"java.lang.String","defpackage.qnc","defpackage.VideoFile",STRING_FILE,STRING_FLAG,FILE_FLAG,FLAG_FILE};
            for(int kind=0;kind<2;kind++)for(int source=0;source<3;source++)for(int index=0;index<forms.length;index++){
                VideoControl.reset();VideoParityCases.generatedEscapedMessages.clear();
                VideoParityCases.Fixture f=new VideoParityCases.Fixture(1,0);String text=forms[index];
                Throwable error=kind==0?new ClassCastException(text):new NullPointerException(text);
                if(source==0)f.error(error);else if(source==1)VideoControl.failure=error;else VideoControl.failures.put(0,error);
                VideoControl.escaped=error;JsonObject actual=new JsonObject();VideoParityCases.executionPath="java";
                VideoParityCases.observe(f.args(),actual);JsonObject state=actual.getAsJsonObject("videoState");
                check("external-lookalike:"+kind+":"+source+":"+index,state.get("escapedExternalIdentity").getAsBoolean()
                    &&!state.get("vmGeneratedEscapedMessageExcluded").getAsBoolean()
                    &&state.get("exceptionMessage").getAsString().equals(text)&&!state.has("castSourceClass")
                    &&VideoParityCases.generatedEscapedMessages.isEmpty());
            }
            report.addProperty("passed",true);
        }catch(Throwable error){report.addProperty("passed",false);report.addProperty("failure",error.toString());throw error;}
        finally{
            report.addProperty("controls",results.size());report.add("results",new Gson().toJsonTree(results));
            report.addProperty("appMethodExecutions",0);report.addProperty("originalCoverageCreditAdded",0);
            report.addProperty("scope","Exact message-form and observation controls only. Original oracle unchanged; no app body or Android execution.");
            Files.writeString(Paths.get(args[0]),new GsonBuilder().setPrettyPrinting().create().toJson(report)+"\n");
            System.out.println("Video exception observation controls="+results.size()+" passed="+report.get("passed"));
        }
    }
}
