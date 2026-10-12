package com.arlosoft.macrodroid.widget;
public class DragLinearLayout extends android.widget.LinearLayout {
    public android.animation.LayoutTransition c; public defpackage.zt2 e = new defpackage.zt2(); public int g,h;
    public Integer distance; public int finishes; public RuntimeException movementFailure,finishFailure;
    public void a(int value) { defpackage.UiTrace.add("drag.move:"+value); if(movementFailure!=null)throw movementFailure; distance=value; }
    public void b() { defpackage.UiTrace.add("drag.finish"); if(finishFailure!=null)throw finishFailure; finishes++; }
}
