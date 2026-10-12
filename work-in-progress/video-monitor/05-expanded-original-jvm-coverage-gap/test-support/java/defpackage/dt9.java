package defpackage;
public abstract class dt9 {
    public static Object e0(i93 dispatcher, jn6 callback, m73 continuation) {
        int index = VideoControl.dispatchReads++;
        VideoControl.dispatches.add(new VideoControl.DispatchCall(dispatcher, callback, continuation));
        VideoControl.hit("stop.dispatch:" + VideoControl.id(dispatcher) + ":" + VideoControl.id(callback)
                + ":" + VideoControl.id(continuation));
        return VideoControl.result(VideoControl.dispatchResults, index, blg.a);
    }
}
