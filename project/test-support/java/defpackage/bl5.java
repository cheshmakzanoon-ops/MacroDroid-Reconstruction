package defpackage;
public class bl5 {
    public static String t(String first, String middle, String last) {
        TouchControl.hit("scene.message:"+first+":"+middle+":"+last);
        return new StringBuilder(first).append(middle).append(last).toString();
    }
}
