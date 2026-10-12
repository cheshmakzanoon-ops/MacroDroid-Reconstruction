package com.arlosoft.macrodroid.constraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
public class WifiConstraint extends Constraint {
 public java.util.ArrayList m_SSIDList=new java.util.ArrayList();public String m_SSID;public int m_wifiState;
 @Override public boolean X(TriggerContextInfo c){return recovered.environment.WifiMethods.evaluate(this,c);}
}
