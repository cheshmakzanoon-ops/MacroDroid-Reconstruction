package android.content;
/** Host-only Android service boundary. Its classes are excluded from every APK. */
public class Context {
 public String testContextId="context";
 public ContentResolver resolver=new ContentResolver();
 public Object wifiService=new android.net.wifi.WifiManager();
 public boolean nullApplicationContext; public RuntimeException serviceFailure;
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
  if(intent.target==com.arlosoft.macrodroid.action.services.BlockTouchesService.class)com.arlosoft.macrodroid.action.services.BlockTouchesService.j=true;
  else com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean.v=true;
  return defpackage.TouchControl.startReturnsNull?null:new ComponentName();
 }
}
