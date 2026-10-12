package retrofit2;
import defpackage.PluginControl;
/** Controlled status-code boundary; no Retrofit or HTTP operation is performed. */
public class HttpException extends RuntimeException {
    public int[] codes;
    public int reads;
    public HttpException(String message, int... values) { super(message); codes = values; }
    public final int a() {
        int index = reads++;
        PluginControl.hit("http.code:" + PluginControl.id(this) + ":" + index);
        return codes[Math.min(index, codes.length - 1)];
    }
}
