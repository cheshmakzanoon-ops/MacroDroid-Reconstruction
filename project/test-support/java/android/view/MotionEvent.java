package android.view;
public class MotionEvent {
    public int action, actionIndex; public int[] ids = {7}; public float[] ys = {10.5f};
    public int getActionMasked() { defpackage.UiTrace.add("event.action"); return action; }
    public int getActionIndex() { defpackage.UiTrace.add("event.actionIndex"); return actionIndex; }
    public int getPointerId(int index) { defpackage.UiTrace.add("event.pointerId:"+index); return ids[index]; }
    public int findPointerIndex(int id) { defpackage.UiTrace.add("event.find:"+id); for(int i=0;i<ids.length;i++)if(ids[i]==id)return i;return -1; }
    public float getY(int index) { defpackage.UiTrace.add("event.y:"+index); return ys[index]; }
}
