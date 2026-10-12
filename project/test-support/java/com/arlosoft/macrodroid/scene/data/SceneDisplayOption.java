package com.arlosoft.macrodroid.scene.data;

public abstract class SceneDisplayOption implements android.os.Parcelable {
    public static class Overlay extends SceneDisplayOption {
        public boolean drawOverSystemApps;
        public int drawReads;
        public Overlay(boolean draw) { drawOverSystemApps=draw; }
        public boolean getDrawOverSystemApps() {
            defpackage.TouchControl.hit("scene.overlayDraw:"+(drawReads++)); return drawOverSystemApps;
        }
    }
    public static class Dialog extends SceneDisplayOption {}
    public static class FullScreen extends SceneDisplayOption {}
 public int describeContents(){return 0;}
 public void writeToParcel(android.os.Parcel out,int flags){throw new AssertionError("Parcel encoding is outside this scene-dispatch boundary");}
}
