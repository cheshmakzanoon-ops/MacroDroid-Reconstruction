package com.arlosoft.macrodroid.action.textmanipulation;
import java.util.*; import com.arlosoft.macrodroid.macro.Macro; import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
/** Compile declarations and controlled host doubles. Never packaged into an APK. */
public class TextManipulation {
 public List<String> params=new ArrayList<>();
 public enum a { STRING, INTEGER, ENUM, STRING_OPTIONAL, BOOLEAN }
 public int getName(){return 0;}
 public String getString(int id){return com.arlosoft.macrodroid.app.MacroDroidApplication.i().getString(id);}
 public boolean getLeaveNewLines(){return false;}
 public int[] getEnumNames(int i){return new int[0];}
 public int getIntValue(int i,Macro m,TriggerContextInfo t){return Integer.parseInt(params.get(i));}
}
