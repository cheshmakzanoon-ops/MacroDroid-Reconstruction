package com.arlosoft.macrodroid.app; public class MacroDroidApplication extends android.content.Context { private static final MacroDroidApplication INSTANCE=new MacroDroidApplication(); public static MacroDroidApplication i(){return INSTANCE;}  public android.content.res.Resources getResources(){return super.getResources();}
}
