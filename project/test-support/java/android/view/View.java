package android.view;
public class View {
    public int visibility; public RuntimeException visibilityFailure;
    public void setVisibility(int value) { defpackage.UiTrace.add("view.visibility:"+value); if(visibilityFailure!=null)throw visibilityFailure; visibility=value; }
}
