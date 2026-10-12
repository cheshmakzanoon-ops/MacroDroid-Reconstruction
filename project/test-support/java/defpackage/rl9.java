package defpackage;
public class rl9 {public static rl9 a=new rl9();public static boolean debugging;
 public static boolean m(long guid){CoreTrace.add("debug.check:"+guid);return debugging;}
 public static boolean paused,threading,stopAfterPause;public static int requested=-1,pauseQueries;public static long generation=73;
 public static boolean q(int p,java.util.Set s){CoreTrace.add("debug.breakpoint:"+p);boolean found=s.contains(Integer.valueOf(p));if(stopAfterPause&&++pauseQueries>1){debugging=false;return false;}return found;}
 public static void p(int p,long g){CoreTrace.add("debug.pause:"+p+":"+g);}public static boolean n(){CoreTrace.add("debug.paused");return paused;}
 public static int i(long g){CoreTrace.add("debug.requested:"+g);return requested;}public static long j(){CoreTrace.add("debug.generation");return generation;}public static boolean l(){CoreTrace.add("debug.threading");return threading;}

}
