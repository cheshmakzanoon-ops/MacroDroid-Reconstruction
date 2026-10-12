package recovered.ui;
import android.animation.ValueAnimator;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import com.arlosoft.macrodroid.widget.DragLinearLayout;
import defpackage.zt2;
/** Recovered event dispatch only. Original drag/animation implementations remain calls. */
public final class InteractionMethods {
    public static boolean touch(DragLinearLayout self, MotionEvent event) {
        int action = event.getActionMasked();
        zt2 state = self.e;
        switch (action) {
            case 0:
                if (!state.g) return false;
                // Preserve the original check-cast even when only testing null.
                ValueAnimator animator = (ValueAnimator) state.k;
                if (animator != null) return false;
                self.c = ((ViewGroup) self).getLayoutTransition();
                if (self.c != null) ((ViewGroup) self).setLayoutTransition(null);
                ((View) state.i).setVisibility(4);
                state.h = true;
                ((ViewGroup) self).requestDisallowInterceptTouchEvent(true);
                return true;
            case 2:
                if (!state.h || self.h == -1) return false;
                int pointer = event.findPointerIndex(self.h);
                // Cast before subtracting; do not change rounding or overflow behavior.
                int distance = (int) event.getY(pointer) - self.g;
                self.a(distance);
                return true;
            case 6:
                if (event.getPointerId(event.getActionIndex()) != self.h) return false;
                // The active pointer's release has the same cleanup as UP and CANCEL.
            case 1:
            case 3:
                self.g = -1;
                self.h = -1;
                if (state.h) {
                    self.b();
                    return true;
                }
                if (state.g) state.f();
                return true;
            default:
                return false;
        }
    }
}
