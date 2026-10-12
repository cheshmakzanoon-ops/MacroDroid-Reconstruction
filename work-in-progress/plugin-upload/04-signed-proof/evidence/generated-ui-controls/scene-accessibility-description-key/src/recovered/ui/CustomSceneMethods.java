package recovered.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import com.arlosoft.macrodroid.action.CustomSceneAction;
import com.arlosoft.macrodroid.actionblock.data.ActionBlock;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.data.ResumeMacroInfo;
import com.arlosoft.macrodroid.events.ClearSceneByExactNameEvent;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.scene.data.SceneDescription;
import com.arlosoft.macrodroid.scene.data.SceneDisplayOption;
import com.arlosoft.macrodroid.scene.display.SceneBaseActivity;
import com.arlosoft.macrodroid.scene.display.SceneDialogActivity;
import com.arlosoft.macrodroid.scene.display.SceneDisplayActivity;
import com.arlosoft.macrodroid.scene.display.SceneOverlayDisplayService;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import com.arlosoft.macrodroid.triggers.services.MacroDroidAccessibilityServiceJellyBean;
import defpackage.aj5;
import defpackage.bl5;
import defpackage.cj5;
import defpackage.eld;
import defpackage.j68;
import defpackage.kjf;
import defpackage.ku1;
import defpackage.lob;
import java.util.Stack;

/** Recovered scene dispatch body; the original display components remain dependencies. */
public final class CustomSceneMethods {
    public static void display(CustomSceneAction self, int nextActionIndex,
            TriggerContextInfo info, boolean isTest, Stack skipEndifIndex,
            ResumeMacroInfo resume) {
        if (((SelectableItem) self).getMacro() instanceof ActionBlock) {
            Macro macro = ((SelectableItem) self).getMacro();
            macro.getClass();
            ((ActionBlock) macro).setDisplayingScene(true);
        }

        SceneDescription description = self.sceneDescription;
        if (description == null) {
            j68.h0("sceneDescription");
            throw null;
        }
        if (description.getSceneConfig().getDisplayOption() instanceof SceneDisplayOption.Overlay) {
            description = self.sceneDescription;
            if (description == null) {
                j68.h0("sceneDescription");
                throw null;
            }
            SceneDisplayOption option = description.getSceneConfig().getDisplayOption();
            option.getClass();
            if (((SceneDisplayOption.Overlay) option).getDrawOverSystemApps()) {
                MacroDroidAccessibilityServiceJellyBean.a companion =
                    MacroDroidAccessibilityServiceJellyBean.u;
                Context context = ((SelectableItem) self).getContext();
                context.getClass();
                description = self.sceneDescription;
                if (description == null) {
                    j68.h0("sceneDescription");
                    throw null;
                }
                Long boxedGuid = ((SelectableItem) self).getMacroGuid();
                boxedGuid.getClass();
                long guid = boxedGuid.longValue();
                long itemId = ((SelectableItem) self).getSIGUID();
                companion.getClass();
                skipEndifIndex.getClass();
                try {
                    Intent intent = new Intent(context, MacroDroidAccessibilityServiceJellyBean.class);
                    intent.setAction("com.arlosoft.macrodroid.triggers.services.SHOW_SCENE_OVERLAY");
                    intent.putExtra("sceneDescription", description);
                    intent.putExtra("MacroGuid", guid);
                    intent.putExtra("SelectableItemId", itemId);
                    intent.putExtra("TriggerContextInfo", info);
                    intent.putExtra("SkipEndifIndex", skipEndifIndex);
                    intent.putExtra("IsTest", isTest);
                    intent.putExtra("resume_macro_info", resume);
                    intent.putExtra("NextActionIndex", nextActionIndex);
                    intent.putExtra("force_not_enabled", false);
                    context.startService(intent);
                } catch (Exception error) {
                    ku1.A("Could not show scene overlay: ", error);
                }
                return;
            }

            SceneOverlayDisplayService.a companion = SceneOverlayDisplayService.d;
            Context context = ((SelectableItem) self).getContext();
            context.getClass();
            description = self.sceneDescription;
            if (description == null) {
                j68.h0("sceneDescription");
                throw null;
            }
            Long boxedGuid = ((SelectableItem) self).getMacroGuid();
            boxedGuid.getClass();
            long guid = boxedGuid.longValue();
            long itemId = ((SelectableItem) self).getSIGUID();
            companion.getClass();
            skipEndifIndex.getClass();
            Intent intent = new Intent(context, SceneOverlayDisplayService.class);
            intent.putExtra("sceneDescription", description);
            intent.putExtra("MacroGuid", guid);
            intent.putExtra("SelectableItemId", itemId);
            intent.putExtra("TriggerContextInfo", info);
            intent.putExtra("SkipEndifIndex", skipEndifIndex);
            intent.putExtra("IsTest", isTest);
            intent.putExtra("resume_macro_info", resume);
            intent.putExtra("NextActionIndex", nextActionIndex);
            intent.putExtra("force_not_enabled", false);
            context.startService(intent);
            return;
        }

        MacroDroidApplication.a applicationCompanion = MacroDroidApplication.E;
        applicationCompanion.getClass();
        MacroDroidApplication application = MacroDroidApplication.F;
        application.getClass();
        if (!application.u && !lob.a(((SelectableItem) self).getContext())) {
            description = self.sceneDescription;
            if (description == null) {
                j68.h0("sceneDescription");
                throw null;
            }
            String name = description.getSceneConfig().getName();
            String message = bl5.t("Scene '", name,
                "' cannot be displayed while MacroDroid is in the background without the 'Display over other apps' permission");
            Long boxedGuid = ((SelectableItem) self).getMacroGuid();
            boxedGuid.getClass();
            kjf.g(boxedGuid.longValue(), message);
            Context context = ((SelectableItem) self).getContext();
            String actionName = ((SelectableItem) self).getName();
            lob.w(context, actionName, null, 2);
            // The original warning deliberately falls through to scene dispatch.
        }

        description = self.sceneDescription;
        if (description == null) {
            j68.h0("sceneDescription");
            throw null;
        }
        if (description.getSceneConfig().getDisplayOption() instanceof SceneDisplayOption.Dialog) {
            SceneDialogActivity.a companion = SceneDialogActivity.R;
            Context context = ((SelectableItem) self).getContext();
            context.getClass();
            Long boxedGuid = ((SelectableItem) self).getMacroGuid();
            boxedGuid.getClass();
            long guid = boxedGuid.longValue();
            long itemId = ((SelectableItem) self).getSIGUID();
            description = self.sceneDescription;
            if (description == null) {
                j68.h0("sceneDescription");
                throw null;
            }
            companion.getClass();
            skipEndifIndex.getClass();
            String name = description.getSceneConfig().getName();
            SceneDisplayActivity.a displayCompanion = SceneDisplayActivity.P;
            displayCompanion.getClass();
            SceneDisplayActivity existing = (SceneDisplayActivity) SceneDisplayActivity.Q.get(name);
            if (existing != null && !((Activity) existing).isFinishing() && !((Activity) existing).isDestroyed()) {
                eld update = new eld(existing, info, guid, itemId, skipEndifIndex,
                    isTest, resume, nextActionIndex, 0);
                ((Activity) existing).runOnUiThread(update);
                return;
            }

            Intent intent = new Intent(context, SceneDialogActivity.class);
            SceneBaseActivity.a baseCompanion = SceneBaseActivity.D;
            baseCompanion.getClass();
            String descriptionKey = SceneBaseActivity.E;
            intent.putExtra(descriptionKey, description);
            intent.putExtra("TriggerContextInfo", info);
            intent.putExtra("MacroGuid", guid);
            intent.putExtra("SelectableItemId", itemId);
            intent.putExtra("SkipEndifIndex", skipEndifIndex);
            intent.putExtra("resume_macro_info", resume);
            intent.putExtra("NextActionIndex", nextActionIndex);
            intent.putExtra("IsTest", isTest);
            intent.putExtra("force_not_enabled", false);
            intent.addFlags(0x18000000);
            aj5 bus = cj5.a();
            ClearSceneByExactNameEvent clear = new ClearSceneByExactNameEvent(description.getSceneConfig().getName());
            bus.e(clear);
            context.startActivity(intent);
            return;
        }

        SceneDisplayActivity.a companion = SceneDisplayActivity.P;
        Context context = ((SelectableItem) self).getContext();
        context.getClass();
        Long boxedGuid = ((SelectableItem) self).getMacroGuid();
        boxedGuid.getClass();
        long guid = boxedGuid.longValue();
        long itemId = ((SelectableItem) self).getSIGUID();
        description = self.sceneDescription;
        if (description == null) {
            j68.h0("sceneDescription");
            throw null;
        }
        companion.getClass();
        skipEndifIndex.getClass();
        String name = description.getSceneConfig().getName();
        SceneDisplayActivity existing = (SceneDisplayActivity) SceneDisplayActivity.Q.get(name);
        if (existing != null && !((Activity) existing).isFinishing() && !((Activity) existing).isDestroyed()) {
            eld update = new eld(existing, info, guid, itemId, skipEndifIndex,
                isTest, resume, nextActionIndex, 1);
            ((Activity) existing).runOnUiThread(update);
            return;
        }

        Intent intent = new Intent(context, SceneDisplayActivity.class);
        SceneBaseActivity.a baseCompanion = SceneBaseActivity.D;
        baseCompanion.getClass();
        String descriptionKey = SceneBaseActivity.E;
        intent.putExtra(descriptionKey, description);
        intent.putExtra("TriggerContextInfo", info);
        intent.putExtra("MacroGuid", guid);
        intent.putExtra("SelectableItemId", itemId);
        intent.putExtra("SkipEndifIndex", skipEndifIndex);
        intent.putExtra("resume_macro_info", resume);
        intent.putExtra("NextActionIndex", nextActionIndex);
        intent.putExtra("IsTest", isTest);
        intent.putExtra("force_not_enabled", false);
        intent.addFlags(0x18000000);
        aj5 bus = cj5.a();
        ClearSceneByExactNameEvent clear = new ClearSceneByExactNameEvent(description.getSceneConfig().getName());
        bus.e(clear);
        context.startActivity(intent);
    }
}
