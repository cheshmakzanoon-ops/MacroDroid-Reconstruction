package recovered.actions;

import android.content.Context;
import android.content.Intent;
import com.arlosoft.macrodroid.action.BlockTouchesAction;
import com.arlosoft.macrodroid.action.services.BlockTouchesService;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.triggers.DeviceUnlockedTrigger;
import com.arlosoft.macrodroid.triggers.ScreenOnOffTrigger;
import com.arlosoft.macrodroid.triggers.Trigger;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean;

/** Recovered from the pinned original invokeAction DEX body, not its failed decompilation. */
public final class BlockTouchesMethods {
    private BlockTouchesMethods() {}

    public static void invoke(BlockTouchesAction self, TriggerContextInfo info) {
        int option = self.option;
        if (option == 0 || option == 2) {
            Trigger first = info == null ? null : info.getTrigger();
            boolean prohibited = first instanceof DeviceUnlockedTrigger;
            if (!prohibited) {
                Trigger second = info == null ? null : info.getTrigger();
                if (second instanceof ScreenOnOffTrigger) {
                    Trigger third = info.getTrigger();
                    third.getClass();
                    prohibited = ((ScreenOnOffTrigger) third).n0();
                }
            }
            if (prohibited) {
                String message = SelectableItem.getString(0x7f14007a);
                message.getClass();
                defpackage.kjf.u(message);
                return;
            }
        }

        BlockTouchesService.i.getClass();
        boolean blocking = BlockTouchesService.j;
        if (!blocking) {
            MacroDroidAccessibilityServiceJellyBean.u.getClass();
            blocking = MacroDroidAccessibilityServiceJellyBean.v;
        }
        Context stopContext = self.getContext();
        Intent stop = new Intent(self.getContext(), BlockTouchesService.class);
        stopContext.stopService(stop);

        // The original re-reads option after stopService; callbacks can mutate it.
        option = self.option;
        if (option != 0 && (option != 2 || blocking)) {
            MacroDroidAccessibilityServiceJellyBean.a companion = MacroDroidAccessibilityServiceJellyBean.u;
            Context context = self.getContext();
            context.getClass();
            companion.getClass();
            MacroDroidAccessibilityServiceJellyBean.a.b(context);
            return;
        }
        int resolvedColor = com.arlosoft.macrodroid.variables.a.e(
            self.getMacro(), self.bgColorVariable, self.bgColor, info);
        if (self.useAccessibilityService) {
            MacroDroidAccessibilityServiceJellyBean.a companion = MacroDroidAccessibilityServiceJellyBean.u;
            Context context = self.getContext();
            context.getClass();
            int color = self.showBlockedArea ? resolvedColor : -1;
            companion.getClass();
            // Only this service-start region catches Exception, not Error.
            try {
                Intent intent = new Intent(context, MacroDroidAccessibilityServiceJellyBean.class);
                intent.setAction("com.arlosoft.macrodroid.triggers.services.BLOCK_SCREEN_TOUCHES");
                intent.putExtra("blocking_color", color);
                context.startService(intent);
            } catch (Exception failure) {
                defpackage.ku1.A("Could not capture screen at this time: ", failure);
            }
            return;
        }
        MacroDroidAccessibilityServiceJellyBean.a companion = MacroDroidAccessibilityServiceJellyBean.u;
        Context context = self.getContext();
        context.getClass();
        companion.getClass();
        MacroDroidAccessibilityServiceJellyBean.a.b(context);
        context = self.getContext();
        context.getClass();
        float x = self.xPosition;
        float y = self.yPosition;
        float width = self.width;
        float height = self.height;
        int color = self.showBlockedArea ? resolvedColor : -1;
        Intent intent = new Intent(context, BlockTouchesService.class);
        intent.putExtra("x", x);
        intent.putExtra("y", y);
        intent.putExtra("width", width);
        intent.putExtra("height", height);
        intent.putExtra("blocking_color", color);
        context.startService(intent);
    }
}
