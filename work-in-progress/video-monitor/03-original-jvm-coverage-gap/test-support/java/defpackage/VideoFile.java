package defpackage;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/** Overrides the three observed File operations; never asks the host filesystem. */
public final class VideoFile extends File {
    public File parent;
    public boolean present = true;
    public long lengthValue;
    public int parentReads, existsReads, lengthReads;
    public final List<Object> parentResults = new ArrayList<Object>();
    public final List<Object> existsResults = new ArrayList<Object>();
    public final List<Object> lengthResults = new ArrayList<Object>();
    public VideoFile(String name) {
        super("controlled-video-" + name);
        VideoControl.name(this, name); VideoControl.files.add(this);
    }
    @Override public File getParentFile() {
        int index = parentReads++;
        VideoControl.hit("file.parent:" + VideoControl.id(this));
        return (File) VideoControl.result(parentResults, index, parent);
    }
    @Override public boolean exists() {
        int index = existsReads++;
        VideoControl.hit("file.exists:" + VideoControl.id(this));
        return (Boolean) VideoControl.result(existsResults, index, present);
    }
    @Override public long length() {
        int index = lengthReads++;
        VideoControl.hit("file.length:" + VideoControl.id(this));
        return ((Number) VideoControl.result(lengthResults, index, lengthValue)).longValue();
    }
}
