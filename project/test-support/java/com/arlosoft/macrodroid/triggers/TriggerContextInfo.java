package com.arlosoft.macrodroid.triggers;
public class TriggerContextInfo implements android.os.Parcelable {
 public String id="trigger-info";
 public Trigger trigger;
 public Trigger getTrigger(){defpackage.CoreTrace.add("triggerContext.getTrigger");return trigger;}
 public int describeContents(){return 0;}
 public void writeToParcel(android.os.Parcel out,int flags){throw new AssertionError("Parcel encoding is outside this scene-dispatch boundary");}
}
