package com.arlosoft.macrodroid.scene.data;

public class SceneDescription implements android.os.Parcelable {
    public String id;
    public SceneConfig sceneConfig;
    public SceneConfig[] configs;
    public int configReads;
    public SceneDescription(String id, SceneConfig config) { this.id = id; this.sceneConfig = config; }
    public SceneConfig getSceneConfig() {
        int index = configReads++; defpackage.TouchControl.hit("scene.config:"+id+":"+index);
        return configs == null ? sceneConfig : configs[Math.min(index, configs.length-1)];
    }
 public int describeContents(){return 0;}
 public void writeToParcel(android.os.Parcel out,int flags){throw new AssertionError("Parcel encoding is outside this scene-dispatch boundary");}
}
