package android.content;
/** Host-only Android service boundary. Its classes are excluded from every APK. */
public class Context {
 public String testContextId="context";
 public ContentResolver resolver=new ContentResolver();
 public Object wifiService=new android.net.wifi.WifiManager();
 public boolean nullApplicationContext; public RuntimeException serviceFailure;
 public java.io.File videoExternalFilesDir;
 public int videoDirectoryReads;
 public final java.util.List<Object> videoDirectoryResults=new java.util.ArrayList<Object>();
 public java.io.File getExternalFilesDir(String type){
  int index=videoDirectoryReads++;
  defpackage.VideoControl.hit("context.externalFiles:"+defpackage.VideoControl.id(this)+":"+type);
  return (java.io.File)defpackage.VideoControl.result(videoDirectoryResults,index,videoExternalFilesDir);
 }
 public String getString(int id){return "resource:"+id;}
 public Context getApplicationContext(){defpackage.CoreTrace.add("context.application");return nullApplicationContext?null:this;}
 public Object getSystemService(String name){defpackage.CoreTrace.add("context.service:"+name);if(serviceFailure!=null)throw serviceFailure;return wifiService;}
 public ContentResolver getContentResolver(){defpackage.CoreTrace.add("context.resolver");return resolver;}
public android.content.res.Resources getResources(){defpackage.CoreTrace.add("context.resources");return new android.content.res.Resources();}
 public boolean stopService(Intent intent){
  defpackage.TouchControl.hit("service.stop:"+testContextId+":"+intent.id);
  defpackage.TouchControl.stops.add(intent);com.arlosoft.macrodroid.action.services.BlockTouchesService.j=false;
  return defpackage.TouchControl.stopResult;
 }
 public ComponentName startService(Intent intent){
  defpackage.TouchControl.hit("service.start:"+testContextId+":"+intent.id);
  defpackage.TouchControl.starts.add(intent);
  if(!defpackage.SceneControl.active) {
   if(intent.target==com.arlosoft.macrodroid.action.services.BlockTouchesService.class)com.arlosoft.macrodroid.action.services.BlockTouchesService.j=true;
   else com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean.v=true;
  }
  return defpackage.TouchControl.startReturnsNull?null:new ComponentName();
 }
 public void startActivity(Intent intent) {
  defpackage.TouchControl.hit("activity.start:"+testContextId+":"+intent.id);
  defpackage.SceneControl.activityStarts.add(intent);
 }
}
