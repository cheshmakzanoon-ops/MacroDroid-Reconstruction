package android.view;
import android.animation.LayoutTransition;
public class ViewGroup extends View {
    public LayoutTransition transition; public boolean disallow;
    public String failAt;
    public LayoutTransition getLayoutTransition() { defpackage.UiTrace.add("layout.get"); if("get".equals(failAt))throw new IllegalStateException("fixture get"); return transition; }
    public void setLayoutTransition(LayoutTransition value) { defpackage.UiTrace.add("layout.set:"+(value==null)); if("set".equals(failAt))throw new IllegalStateException("fixture set"); transition=value; }
    public void requestDisallowInterceptTouchEvent(boolean value) { defpackage.UiTrace.add("layout.disallow:"+value); if("disallow".equals(failAt))throw new IllegalStateException("fixture disallow"); disallow=value; }
}
