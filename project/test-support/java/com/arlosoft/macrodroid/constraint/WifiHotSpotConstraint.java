package com.arlosoft.macrodroid.constraint;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
public class WifiHotSpotConstraint extends Constraint {
 public boolean m_checkConnections,m_enabled;public int m_comparisonValue,m_connectedCount;
 public static int connected;public static RuntimeException connectedFailure;
 public static int l0(){defpackage.CoreTrace.add("hotspot.clients");if(connectedFailure!=null)throw connectedFailure;return connected;}
 @Override public boolean X(TriggerContextInfo c){return recovered.environment.WifiMethods.hotspot(this,c);}
}
