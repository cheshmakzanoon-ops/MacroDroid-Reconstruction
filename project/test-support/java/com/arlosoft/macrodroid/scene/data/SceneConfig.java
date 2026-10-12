package com.arlosoft.macrodroid.scene.data;

public class SceneConfig implements android.os.Parcelable {
    public String id, name;
    public SceneDisplayOption displayOption;
    public SceneDisplayOption[] options;
    public String[] names;
    public int optionReads, nameReads;
    public SceneConfig(String id, String name, SceneDisplayOption option) { this.id=id; this.name=name; displayOption=option; }
    public SceneDisplayOption getDisplayOption() {
        int index = optionReads++; defpackage.TouchControl.hit("scene.option:"+id+":"+index);
        return options == null ? displayOption : options[Math.min(index, options.length-1)];
    }
    public String getName() {
        int index = nameReads++; defpackage.TouchControl.hit("scene.configName:"+id+":"+index);
        return names == null ? name : names[Math.min(index, names.length-1)];
    }
 public int describeContents(){return 0;}
 public void writeToParcel(android.os.Parcel out,int flags){throw new AssertionError("Parcel encoding is outside this scene-dispatch boundary");}
}
