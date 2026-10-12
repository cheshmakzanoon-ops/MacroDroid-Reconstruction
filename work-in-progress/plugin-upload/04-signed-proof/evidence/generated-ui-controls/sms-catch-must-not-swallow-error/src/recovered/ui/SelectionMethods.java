package recovered.ui;
import android.text.TextUtils;
import android.content.Context;
import android.provider.ContactsContract;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.triggers.IncomingSMSTrigger;
import defpackage.htg;
/** Original selection/validation behavior, including its narrow exception boundaries. */
public final class SelectionMethods {
    public static boolean isSoundToken(String text) {
        if (TextUtils.isEmpty(text)) return false;
        if (text.equals("[Stop Existing Sound]")) return true;
        try {
            if (text.equals(SelectableItem.getString(0x7f140298))) return true;
        } catch (Exception ignored) {
            // Only this resource lookup/equality region was guarded in the original.
        }
        return text.startsWith("[") && text.endsWith("]");
    }
    public static boolean validSms(IncomingSMSTrigger self) {
        int option = self.m_option;
        if (option < 0) option = 0;
        if (option == 0) {
            if (self.m_smsFrom == null && self.m_smsFromList.size() == 0) return false;
            if (self.m_smsFrom != null && self.m_smsFrom.b().equals("Select_Contact")) return false;
            return true;
        }
        if (option != 1) return true;
        if (self.m_groupIdList.size() != 1) return self.m_groupIdList.size() != 0;
        // These operations intentionally precede the provider-read catch region.
        Context context = self.getContext();
        String id = (String) self.m_groupIdList.get(0);
        java.util.List ignoredInitialization = htg.a;
        boolean valid = false;
        try {
            valid = context.getContentResolver().query(
                ContactsContract.Groups.CONTENT_SUMMARY_URI, null,
                new StringBuilder("_id = '").append(id).append("'").toString(),
                null, null).getCount() > 0;
        } catch (Throwable ignored) {
            // Preserve the uploaded implementation; do not widen this to Throwable.
        }
        self.lastValidCheck = valid;
        return valid;
    }
}
