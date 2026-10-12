package android.net.wifi;
public class WifiManager {
 public int wifiState=3,apState=13;public WifiInfo info=new WifiInfo();public RuntimeException apFailure;
 public int getWifiState(){defpackage.CoreTrace.add("wifi.state");return wifiState;}
 public WifiInfo getConnectionInfo(){defpackage.CoreTrace.add("wifi.info");return info;}
 public int getWifiApState(){defpackage.CoreTrace.add("wifi.apState");if(apFailure!=null)throw apFailure;return apState;}
}
