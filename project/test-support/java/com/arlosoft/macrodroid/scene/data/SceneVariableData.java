package com.arlosoft.macrodroid.scene.data;
/** Controlled nested Parcelable; original nested implementations are not claimed tested. */
public class SceneVariableData implements android.os.Parcelable {
 public String id; public SceneVariableData() {} public SceneVariableData(String id) { this.id=id; }
 public int describeContents(){return 0;} public void writeToParcel(android.os.Parcel out,int flags){throw new UnsupportedOperationException("nested fixture");}
}
