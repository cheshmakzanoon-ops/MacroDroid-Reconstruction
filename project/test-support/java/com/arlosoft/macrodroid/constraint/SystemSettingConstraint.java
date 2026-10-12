package com.arlosoft.macrodroid.constraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
public class SystemSettingConstraint extends Constraint {
 public static int TABLE_OPTION_SYSTEM=0,TABLE_OPTION_SECURE=1,TABLE_OPTION_GLOBAL=2;
 public String settingString="fixture",valueString="0";public int valueType,tableOption,equalityCheckOption;public boolean regexEnabled;
 @Override public boolean X(TriggerContextInfo c){return recovered.environment.SystemSettingMethods.evaluate(this,c);}
 public boolean r0(long value,TriggerContextInfo c){return recovered.environment.SystemSettingMethods.compareInteger(this,value,c);}
 public boolean t0(String value,TriggerContextInfo c){return recovered.environment.SystemSettingMethods.compareText(this,value,c);}
}
