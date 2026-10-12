package defpackage;

import com.arlosoft.macrodroid.action.services.BaseVideoRecordingService;

/** The original same-owner callback constructor is an external host boundary. */
public final class d31 extends rff implements jn6 {
    public final BaseVideoRecordingService this$0;
    public final m73 completion;
    public int label;
    public d31(BaseVideoRecordingService owner, m73 completion) {
        super(2, completion);
        this.this$0 = owner; this.completion = completion;
        VideoControl.name(this, "stopCallback" + VideoControl.callbacks.size());
        VideoControl.callbacks.add(this);
        VideoControl.hit("stop.callback.new:" + VideoControl.id(this) + ":" + VideoControl.id(owner)
                + ":" + VideoControl.id(completion));
    }
}
