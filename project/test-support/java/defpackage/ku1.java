package defpackage;
public class ku1 {
    public static void A(String prefix,Exception error) {
        TouchControl.loggedFailure=error;TouchControl.loggedPrefix=prefix;TouchControl.logCalls++;
        TouchControl.hit("log.capture:"+prefix+":"+error.getClass().getName()+":"+error.getMessage());
    }
}
