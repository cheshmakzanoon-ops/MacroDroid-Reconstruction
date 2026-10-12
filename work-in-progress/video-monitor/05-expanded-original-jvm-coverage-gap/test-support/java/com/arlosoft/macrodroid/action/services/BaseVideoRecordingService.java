package com.arlosoft.macrodroid.action.services;

import android.os.ParcelFileDescriptor;
import androidx.lifecycle.LifecycleService;
import defpackage.VideoControl;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

/** Host-only field facade and controlled free-space call; omitted from all APKs. */
public class BaseVideoRecordingService extends LifecycleService {
    public static BaseVideoRecordingService$a A = new BaseVideoRecordingService$a();
    public static volatile boolean B;
    public long s, v, x;
    public int w;
    public File t;
    public ParcelFileDescriptor u;
    public long available = 268435456L;
    public int availableReads;
    public final List<Object> availableResults = new ArrayList<Object>();
    public long c(File directory) {
        int index = availableReads++;
        VideoControl.hit("storage.available:" + VideoControl.id(this) + ":" + VideoControl.id(directory));
        return ((Number) VideoControl.result(availableResults, index, available)).longValue();
    }
}
