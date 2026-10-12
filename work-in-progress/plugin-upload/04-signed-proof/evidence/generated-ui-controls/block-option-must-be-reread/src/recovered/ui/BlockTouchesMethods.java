package recovered.ui;

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
import defpackage.kjf;
import defpackage.ku1;

/** Recovered service selection and Intent construction; original services remain dependencies. */
public final class BlockTouchesMethods {
    public static void invoke(BlockTouchesAction self, TriggerContextInfo info) {
        int option = self.option;
        if (option == 0 || option == 2) {
            Trigger trigger = info == null ? null : info.getTrigger();
            boolean rejected = trigger instanceof DeviceUnlockedTrigger;
            if (!rejected) {
                // Each original lookup can observe a different trigger or throw.
                trigger = info == null ? null : info.getTrigger();
                if (trigger instanceof ScreenOnOffTrigger) {
                    trigger = info.getTrigger();
                    trigger.getClass();
                    rejected = ((ScreenOnOffTrigger) trigger).n0();
                }
            }
            if (rejected) {
                String message = SelectableItem.getString(0x7f14007a);
                message.getClass();
                kjf.u(message);
                return;
            }
        }

        BlockTouchesService.a overlayCompanion = BlockTouchesService.i;
        overlayCompanion.getClass();
        boolean blocking = BlockTouchesService.j;
        if (!blocking) {
            MacroDroidAccessibilityServiceJellyBean.a accessibilityCompanion =
                MacroDroidAccessibilityServiceJellyBean.u;
            accessibilityCompanion.getClass();
            blocking = MacroDroidAccessibilityServiceJellyBean.v;
        }

        Context stopContext = ((SelectableItem) self).getContext();
        Intent stop = new Intent(((SelectableItem) self).getContext(), BlockTouchesService.class);
        stopContext.stopService(stop);

        // The toggle decision uses the saved state, but rereads the option after stopService.
        option = option;
        if (option != 0 && (option != 2 || blocking)) {
            MacroDroidAccessibilityServiceJellyBean.a companion =
                MacroDroidAccessibilityServiceJellyBean.u;
            Context context = ((SelectableItem) self).getContext();
            context.getClass();
            companion.getClass();
            MacroDroidAccessibilityServiceJellyBean.a.b(context);
            return;
        }

        int color = com.arlosoft.macrodroid.variables.a.e(
            ((SelectableItem) self).getMacro(), self.bgColorVariable, self.bgColor, info);
        if (self.useAccessibilityService) {
            MacroDroidAccessibilityServiceJellyBean.a companion =
                MacroDroidAccessibilityServiceJellyBean.u;
            Context context = ((SelectableItem) self).getContext();
            context.getClass();
            if (!self.showBlockedArea) color = -1;
            companion.getClass();
            try {
                Intent start = new Intent(context, MacroDroidAccessibilityServiceJellyBean.class);
                start.setAction("com.arlosoft.macrodroid.triggers.services.BLOCK_SCREEN_TOUCHES");
                start.putExtra("blocking_color", color);
                context.startService(start);
            } catch (Exception error) {
                // Only accessibility Intent creation/configuration/start is inside this handler.
                ku1.A("Could not capture screen at this time: ", error);
            }
            return;
        }

        MacroDroidAccessibilityServiceJellyBean.a companion =
            MacroDroidAccessibilityServiceJellyBean.u;
        Context unblockContext = ((SelectableItem) self).getContext();
        unblockContext.getClass();
        companion.getClass();
        MacroDroidAccessibilityServiceJellyBean.a.b(unblockContext);

        Context context = ((SelectableItem) self).getContext();
        context.getClass();
        float x = self.xPosition;
        float y = self.yPosition;
        float width = self.width;
        float height = self.height;
        if (!self.showBlockedArea) color = -1;
        Intent start = new Intent(context, BlockTouchesService.class);
        start.putExtra("x", x);
        start.putExtra("y", y);
        start.putExtra("width", width);
        start.putExtra("height", height);
        start.putExtra("blocking_color", color);
        context.startService(start);
    }
}
