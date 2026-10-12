package android.provider;
import android.content.ContentResolver;
public final class Settings {
 public static class SettingNotFoundException extends Exception {public SettingNotFoundException(String name){super(name);}}
 public static final class System {
  public static int getInt(ContentResolver r,String name) throws SettingNotFoundException {r.read("System","Int",name);return r.integer;}
  public static long getLong(ContentResolver r,String name) throws SettingNotFoundException {r.read("System","Long",name);return r.longValue;}
  public static float getFloat(ContentResolver r,String name) throws SettingNotFoundException {r.read("System","Float",name);return r.floating;}
  public static String getString(ContentResolver r,String name) throws SettingNotFoundException {r.read("System","String",name);return r.text;}
 }
 public static final class Secure {
  public static int getInt(ContentResolver r,String name) throws SettingNotFoundException {r.read("Secure","Int",name);return r.integer;}
  public static long getLong(ContentResolver r,String name) throws SettingNotFoundException {r.read("Secure","Long",name);return r.longValue;}
  public static float getFloat(ContentResolver r,String name) throws SettingNotFoundException {r.read("Secure","Float",name);return r.floating;}
  public static String getString(ContentResolver r,String name) throws SettingNotFoundException {r.read("Secure","String",name);return r.text;}
 }
 public static final class Global {
  public static int getInt(ContentResolver r,String name) throws SettingNotFoundException {r.read("Global","Int",name);return r.integer;}
  public static long getLong(ContentResolver r,String name) throws SettingNotFoundException {r.read("Global","Long",name);return r.longValue;}
  public static float getFloat(ContentResolver r,String name) throws SettingNotFoundException {r.read("Global","Float",name);return r.floating;}
  public static String getString(ContentResolver r,String name) throws SettingNotFoundException {r.read("Global","String",name);return r.text;}
 }
}
