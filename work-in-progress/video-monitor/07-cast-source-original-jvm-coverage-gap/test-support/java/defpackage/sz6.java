package defpackage;
public abstract class sz6 {
    public static Object s(long milliseconds, m73 continuation) {
        int index = VideoControl.delayReads++;
        VideoControl.delays.add(new VideoControl.DelayCall(milliseconds, continuation));
        VideoControl.hit("delay:" + milliseconds + ":" + VideoControl.id(continuation));
        return VideoControl.result(VideoControl.delayResults, index, v93.COROUTINE_SUSPENDED);
    }
}
