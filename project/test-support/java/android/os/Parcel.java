package android.os;
import java.util.*;
/** Typed token stream for host tests; NOT Android's binary Parcel implementation. */
public class Parcel {
    public List<String> written;
    public final List<Object> tokens = new ArrayList<Object>();
    public final List<String> operations = new ArrayList<String>();
    public int position, failAt = -1;
    public RuntimeException failure = new IllegalStateException("fixture parcel failure");
    public void writeStringList(List<String> value) { written=value==null?null:new ArrayList<String>(value); }
    public void readStringList(List<String> value) { if(written!=null)value.addAll(written); }
    private void operation(String name) {
        operations.add(name);
        if (operations.size()-1 == failAt) throw failure;
    }
    public String readString() { operation("readString"); return (String)tokens.get(position++); }
    public int readInt() { operation("readInt"); return (Integer)tokens.get(position++); }
    public Parcelable readParcelable(ClassLoader loader) { operation("readParcelable:"+(loader==Parcel.class.getClassLoader())); return (Parcelable)tokens.get(position++); }
    public void writeString(String value) { operation("writeString"); tokens.add(value); }
    public void writeInt(int value) { operation("writeInt"); tokens.add(value); }
    public void writeParcelable(Parcelable value, int flags) { operation("writeParcelable:"+flags); tokens.add(value); }
}
