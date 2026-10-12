package com.arlosoft.macrodroid.events;

public class ClearSceneByExactNameEvent {
    public final String sceneName;
    public ClearSceneByExactNameEvent(String name) {
        defpackage.TouchControl.hit("scene.event.new:"+name); name.getClass();
        sceneName=name; defpackage.SceneControl.name(this,"event"+defpackage.SceneControl.createdEvents.size());
        defpackage.SceneControl.createdEvents.add(this);
    }
}
