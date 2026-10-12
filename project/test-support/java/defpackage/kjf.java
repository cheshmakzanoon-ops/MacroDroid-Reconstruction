package defpackage;
public class kjf {
 public static void t(long guid,String text){CoreTrace.add("log.debug:"+guid+":"+text);}
 public static void c(String text,Integer index,long guid){CoreTrace.add("log.constraint:"+index+":"+guid+":"+text);}
 public static void h(String text){CoreTrace.add("log.error:"+text);WidgetControl.hit("log.error:"+text);}
 public static void r(String text){CoreTrace.add("log.sensor:"+text);}
 public static void g(long guid,String text){if(SceneControl.active)TouchControl.hit("log.guid:"+guid+":"+text);else CoreTrace.add("log.guid:"+guid+":"+text);}
 public static void l(String text){CoreTrace.add("log.regex:"+text);}
public static void q(long g,String s){CoreTrace.add("log.info:"+g+":"+s);}public static void e(long g,String s,String x){CoreTrace.add("log.detail:"+g+":"+s+":"+x);}public static void u(String s){CoreTrace.add("log.warn:"+s);}public static void w(long g){CoreTrace.add("log.unregister:"+g);}
}
