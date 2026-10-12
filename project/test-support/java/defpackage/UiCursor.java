package defpackage;
public class UiCursor implements android.database.Cursor {
    public int count,closed; public Throwable failure;
    public int getCount() {UiTrace.add("cursor.count");UiTrace.raise(failure);return count;}
    public void close() {UiTrace.add("cursor.close");closed++;}
}
