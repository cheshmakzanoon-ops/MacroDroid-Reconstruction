package recovered.engine;
import com.arlosoft.macrodroid.action.LoopAction;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.macro.Macro;
import android.os.Looper;
import defpackage.e3g;
import defpackage.kjf;
import defpackage.zc;
/** Original 100 ms reset, 3 s throttle and 60 s / 50 Hz abort thresholds. */
public final class LoopGuardMethods {
 public static boolean check(Macro.b self,Macro macro,LoopAction loop){
  long now=System.nanoTime();long started=self.a;
  if(started==0L || now-self.b>100000000L){self.a=now;self.c=0L;started=now;}
  self.b=now;long count=self.c+1L;self.c=count;long elapsed=now-started;
  if(elapsed>60000000000L&&(double)count*1.0E9/(double)elapsed>50.0d){
   MacroDroidApplication application=MacroDroidApplication.i();
   int initializationRead=e3g.b;
   CharSequence text=application.getResources().getText(0x7f141560);
   e3g.b(application,text,0).show();
   String message=new StringBuilder().append(macro.getName()).append(" loop ran with no wait/delay for too long - aborting macro. Add a 'Wait Before Next Action' inside the loop to prevent rapid iteration.").toString();
   kjf.g(macro.getGUID(),message);zc.c(macro,loop);macro.terminateMacro();return true;
  }
  if(elapsed>3000000000L){
   if(!self.d){self.d=true;String message=new StringBuilder().append(macro.getName()).append(" loop is running with no wait/delay - throttling to keep the device responsive. Add a 'Wait Before Next Action' inside the loop.").toString();kjf.t(macro.getGUID(),message);}
   if(Looper.myLooper()!=Looper.getMainLooper()){try{Thread.sleep(10L);return false;}catch(InterruptedException interrupted){Thread.currentThread().interrupt();}}
  }
  return false;
 }
}
