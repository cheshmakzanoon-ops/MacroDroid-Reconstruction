package android.content;
/** Host-only controllable Settings provider; not Android's provider implementation. */
public class ContentResolver {
 public int integer; public long longValue; public float floating; public String text;
 public String failure, failureTable, failureKind;
 public void read(String table,String kind,String name) throws android.provider.Settings.SettingNotFoundException {
  defpackage.CoreTrace.add("settings.read:"+table+":"+kind+":"+name);
  if(failure==null || (failureTable!=null&&!failureTable.equals(table)) || (failureKind!=null&&!failureKind.equals(kind)))return;
  if(failure.equals("missing"))throw new android.provider.Settings.SettingNotFoundException(name);
  if(failure.equals("security"))throw new SecurityException("fixture denied");
  if(failure.equals("illegal"))throw new IllegalStateException("fixture provider");
 }

 public android.database.Cursor queryCursor = new defpackage.UiCursor(); public Throwable queryFailure;
 public android.database.Cursor query(android.net.Uri uri,String[] projection,String selection,String[] arguments,String sort) {
  defpackage.UiTrace.add("query:"+uri+":"+java.util.Arrays.toString(projection)+":"+selection+":"+java.util.Arrays.toString(arguments)+":"+sort);
  defpackage.UiTrace.raise(queryFailure); return queryCursor;
 }
}
