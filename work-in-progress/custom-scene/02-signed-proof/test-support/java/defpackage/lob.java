package defpackage; public class lob {public static void v(android.content.Context c,String permission,String name){CoreTrace.add("permission.prompt:"+permission+":"+name);}
 public static boolean a(android.content.Context context){SceneControl.permissionReads++;TouchControl.hit("scene.permission:"+SceneControl.id(context));return SceneControl.overlayPermission;}
 public static void w(android.content.Context context,String name,String detail,int mode){TouchControl.hit("scene.permissionWarning:"+SceneControl.id(context)+":"+name+":"+detail+":"+mode);SceneControl.permissionWarnings++;}
}
