package recovered.ui;

import android.content.Context;
import android.os.Environment;
import com.arlosoft.macrodroid.action.services.BaseVideoRecordingService;
import com.arlosoft.macrodroid.action.services.a;
import defpackage.ad4;
import defpackage.at9;
import defpackage.blg;
import defpackage.d31;
import defpackage.dt9;
import defpackage.e6d;
import defpackage.jb3;
import defpackage.kjf;
import defpackage.m47;
import defpackage.qnc;
import defpackage.sz6;
import defpackage.u2f;
import defpackage.v93;
import defpackage.zp4;
import java.io.File;

/** Selected original video-monitor coroutine body; every dependency remains original. */
public final class VideoMonitorMethods {
    public static Object monitor(a self, Object result) {
        blg unit = blg.a;
        String kb = "KB";
        Object suspended = v93.COROUTINE_SUSPENDED;
        int label = self.label;
        if (label == 0) {
            u2f.P(result);
            self.label = 1;
            Object delayed = sz6.s(5000L, self);
            if (delayed == suspended) return suspended;
        } else if (label == 1) {
            u2f.P(result);
        } else if (label == 2) {
            File ignoredFile = (File) self.L$1;
            qnc ignoredFlag = (qnc) self.L$0;
            try {
                u2f.P(result);
                return unit;
            } catch (Exception failure) {
                String message = ((Throwable) failure).getMessage();
                String text = jb3.z("Error in storage monitoring: ", message);
                kjf.g(self.this$0.s, text);
            }
            self.L$0 = null;
            self.L$1 = null;
            self.label = 3;
            Object delayed = sz6.s(3000L, self);
            if (delayed == suspended) return suspended;
        } else if (label == 3) {
            u2f.P(result);
        } else {
            e6d.r("call to 'resume' before 'invoke' with coroutine");
            return null;
        }

        while (true) {
            BaseVideoRecordingService.A.getClass();
            if (!BaseVideoRecordingService.B) return unit;
            try {
                File directory = self.this$0.t;
                if (directory != null) directory = directory.getParentFile();
                if (directory == null) {
                    BaseVideoRecordingService owner = self.this$0;
                    String movies = Environment.DIRECTORY_MOVIES;
                    directory = ((Context) owner).getExternalFilesDir(movies);
                }
                boolean stop = false;
                if (directory != null) {
                    BaseVideoRecordingService storageOwner = self.this$0;
                    long available = storageOwner.c(directory);
                    long previousAvailable = storageOwner.x;
                    if (previousAvailable <= 0L || available <= previousAvailable - 104857600L) {
                        storageOwner.x = available;
                        long megabytes = available / 1048576L;
                        String text = new StringBuilder()
                                .append("Recording Video - Available storage: ")
                                .append(megabytes).append("MB").toString();
                        kjf.q(storageOwner.s, text);
                    }
                    if (available < 134217728L) {
                        long megabytes = available / 1048576L;
                        String text = new StringBuilder()
                                .append("CRITICAL: Storage space exhausted (")
                                .append(megabytes).append("MB remaining). Stopping recording.").toString();
                        kjf.g(storageOwner.s, text);
                        stop = true;
                    }
                }

                if (!stop) {
                    BaseVideoRecordingService fileOwner = self.this$0;
                    fileOwner.getClass();
                    long size;
                    try {
                        File file = fileOwner.t;
                        if (file != null) {
                            file.getClass();
                            if (file.exists()) {
                                file = fileOwner.t;
                                file.getClass();
                                size = file.length();
                            } else {
                                size = 0L;
                            }
                        } else {
                            size = fileOwner.u != null ? -1L : 0L;
                        }
                    } catch (Exception failure) {
                        String message = ((Throwable) failure).getMessage();
                        String text = jb3.z("Failed to get current video file size: ", message);
                        kjf.g(fileOwner.s, text);
                        size = 0L;
                    }

                    if (size >= 0L) {
                        long kilobytes = size / 1024L;
                        String text = new StringBuilder().append("Current file size: ")
                                .append(kilobytes).append(kb).toString();
                        kjf.q(self.this$0.s, text);
                        BaseVideoRecordingService previousOwner = self.this$0;
                        long previousSize = previousOwner.v;
                        if (previousSize > 0L) {
                            long growth = size - previousSize;
                            if (growth <= 0L) {
                                int checks = previousOwner.w + 1;
                                previousOwner.w = checks;
                                text = new StringBuilder().append("File size not growing: check ")
                                        .append(checks).append("/3").toString();
                                kjf.q(self.this$0.s, text);
                                checks = self.this$0.w;
                                if (checks >= 3) {
                                    long seconds = (long) checks * 3000L / 1000L;
                                    text = new StringBuilder().append("CRITICAL: Video file stopped growing for ")
                                            .append(seconds).append(" seconds. Storage may be full. Stopping recording.").toString();
                                    kjf.g(self.this$0.s, text);
                                    stop = true;
                                }
                            } else {
                                previousOwner.w = 0;
                                long growthKilobytes = growth / 1024L;
                                text = new StringBuilder().append("File growing normally: +")
                                        .append(growthKilobytes).append(kb).toString();
                                kjf.q(self.this$0.s, text);
                            }
                        }
                        self.this$0.v = size;
                    }
                }

                if (stop) {
                    ad4 ignoredDispatcher = zp4.a;
                    m47 dispatcher = at9.a;
                    d31 callback = new d31(self.this$0, null);
                    self.L$0 = null;
                    self.L$1 = null;
                    self.label = 2;
                    Object stopped = dt9.e0(dispatcher, callback, self);
                    if (stopped == suspended) return suspended;
                    return unit;
                }
            } catch (Exception failure) {
                String message = ((Throwable) failure).getMessage();
                String text = jb3.z("Error in storage monitoring: ", message);
                kjf.g(self.this$0.s, text);
            }
            self.L$0 = null;
            self.L$1 = null;
            self.label = 3;
            Object delayed = sz6.s(3000L, self);
            if (delayed == suspended) return suspended;
        }
    }
}
