package j$.util.concurrent;

/** Host-only desugared map boundary backed by the JVM concurrent map. */
public class ConcurrentHashMap extends java.util.concurrent.ConcurrentHashMap<Object,Object> {
    @Override public Object get(Object key) {
        defpackage.TouchControl.hit("scene.map.get:"+defpackage.SceneControl.id(key)); return super.get(key);
    }
}
