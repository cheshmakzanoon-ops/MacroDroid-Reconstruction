package recovered.ui;

import android.content.Context;
import com.arlosoft.macrodroid.widget.custom.WidgetUpdateManager;
import com.arlosoft.macrodroid.widget.custom.b;
import defpackage.*;
import java.util.Iterator;
import java.util.List;

/** Editable recovery of WidgetUpdateManager.m; validation is tracked separately.
 * The DEX integration must restore the pinned Lzhh allocation's Lrff constructor
 * owner. Compile-only constructors and test boundaries never enter the APK.
 */
public final class WidgetUpdateMethods {
    private WidgetUpdateMethods() {}

    @SuppressWarnings({"rawtypes", "unused"})
    public static Object update(WidgetUpdateManager self, Context context,
                                List widgetIds, o73 completion) {
        b state;
        if (completion instanceof b) {
            b existing = (b) completion;
            int oldLabel = existing.label;
            if ((oldLabel & Integer.MIN_VALUE) != 0) {
                existing.label = oldLabel - Integer.MIN_VALUE;
                state = existing;
            } else {
                state = new b(self, completion);
            }
        } else {
            state = new b(self, completion);
        }

        Object result = state.result;
        Object suspended = v93.COROUTINE_SUSPENDED;
        int label = state.label;
        int savedIndex = 0;
        int widgetId = 0;
        int savedPhase = 0;
        Iterator iterator;
        wx6 manager;
        hn9 renderer;
        gy6 identifier = null;
        boolean afterFirstSuspension = false;

        if (label == 2) {
            widgetId = state.I$1;
            savedIndex = state.I$0;
            gy6 discardedIdentifier = (gy6) state.L$7;
            iterator = (Iterator) state.L$5;
            Iterable discardedIterable = (Iterable) state.L$4;
            renderer = (hn9) state.L$3;
            manager = (wx6) state.L$2;
            List discardedList = (List) state.L$1;
            context = (Context) state.L$0;
            try {
                u2f.P(result);
            } catch (Exception failure) {
                String message = ((Throwable) failure).getMessage();
                kjf.h(new StringBuilder("Failed to update custom widget instance ")
                    .append(widgetId).append(": ").append(message).toString());
            }
        } else if (label == 1) {
            savedPhase = state.I$2;
            widgetId = state.I$1;
            savedIndex = state.I$0;
            identifier = (gy6) state.L$7;
            iterator = (Iterator) state.L$5;
            Iterable discardedIterable = (Iterable) state.L$4;
            renderer = (hn9) state.L$3;
            manager = (wx6) state.L$2;
            List discardedList = (List) state.L$1;
            context = (Context) state.L$0;
            try {
                u2f.P(result);
                afterFirstSuspension = true;
            } catch (Exception failure) {
                String message = ((Throwable) failure).getMessage();
                kjf.h(new StringBuilder("Failed to update custom widget instance ")
                    .append(widgetId).append(": ").append(message).toString());
            }
        } else if (label == 0) {
            u2f.P(result);
            if (widgetIds.isEmpty()) {
                return blg.a;
            }
            self.a(context);
            manager = new wx6(context);
            renderer = new hn9();
            iterator = ((Iterable) widgetIds).iterator();
        } else {
            e6d.r("call to 'resume' before 'invoke' with coroutine");
            return null;
        }

        while (true) {
            if (!afterFirstSuspension) {
                if (!iterator.hasNext()) {
                    return blg.a;
                }
                try { widgetId = ((Number) iterator.next()).intValue(); }
                catch (Exception ignored) { return blg.a; }
                try {
                    if (manager.b.getAppWidgetInfo(widgetId) == null) {
                        throw new IllegalArgumentException("Invalid AppWidget ID.");
                    }
                    identifier = new mh0(widgetId);
                    zhh factory = new zhh(2, null);
                    state.L$0 = context;
                    state.L$1 = null;
                    state.L$2 = manager;
                    state.L$3 = renderer;
                    state.L$4 = null;
                    state.L$5 = iterator;
                    state.L$6 = null;
                    state.L$7 = identifier;
                    state.I$0 = savedIndex;
                    state.I$1 = widgetId;
                    state.I$2 = 0;
                    state.label = 1;
                    Object first = rjb.M(context, identifier, factory, state);
                    if (first == suspended) {
                        return suspended;
                    }
                    savedPhase = 0;
                } catch (Exception failure) {
                    String message = ((Throwable) failure).getMessage();
                    kjf.h(new StringBuilder("Failed to update custom widget instance ")
                        .append(widgetId).append(": ").append(message).toString());
                    continue;
                }
            }
            afterFirstSuspension = false;
            try {
                state.L$0 = context;
                state.L$1 = null;
                state.L$2 = manager;
                state.L$3 = renderer;
                state.L$4 = null;
                state.L$5 = iterator;
                state.L$6 = null;
                state.L$7 = null;
                state.I$0 = savedIndex;
                state.I$1 = widgetId;
                state.I$2 = savedPhase;
                state.label = 2;
                Object second = ((rx6) renderer).d(context, identifier, state);
                if (second == suspended) {
                    return suspended;
                }
            } catch (Exception failure) {
                String message = ((Throwable) failure).getMessage();
                kjf.h(new StringBuilder("Failed to update custom widget instance ")
                    .append(widgetId).append(": ").append(message).toString());
            }
        }
    }
}
