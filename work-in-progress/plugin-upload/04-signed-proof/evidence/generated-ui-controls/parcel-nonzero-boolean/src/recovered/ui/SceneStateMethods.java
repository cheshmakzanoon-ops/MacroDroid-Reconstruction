package recovered.ui;
import android.os.Parcel;
import com.arlosoft.macrodroid.scene.components.SceneTextConfig;
import com.arlosoft.macrodroid.scene.data.*;
/** Original 21-field Parcel protocol, without adding defaults or changing read order. */
public final class SceneStateMethods {
    public static Object read(SceneTextConfig.a self, Parcel parcel) {
        parcel.getClass();
        return new SceneTextConfig(
            parcel.readString(),
            parcel.readInt(),
            (SceneVariableData) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            parcel.readString(),
            parcel.readInt() == 1,
            parcel.readInt() != 0,
            (SceneAlignment) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            parcel.readInt() != 0,
            parcel.readInt() != 0,
            (SceneVariableData) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            (SceneVariableData) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            parcel.readInt() != 0,
            parcel.readString(),
            parcel.readInt() != 0,
            parcel.readString(),
            parcel.readInt() != 0,
            parcel.readString(),
            (ButtonClickConfig) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            parcel.readInt() != 0,
            (SceneVariableData) parcel.readParcelable(SceneTextConfig.class.getClassLoader()),
            (SceneVariableUpdateValue) parcel.readParcelable(SceneTextConfig.class.getClassLoader()));
    }
    public static void write(SceneTextConfig self, Parcel parcel, int flags) {
        parcel.getClass();
        parcel.writeString(self.text);
        parcel.writeInt(self.textColor);
        parcel.writeParcelable(self.textColorVariable, flags);
        parcel.writeString(self.textSize);
        parcel.writeInt(self.isBold ? 1 : 0);
        parcel.writeInt(self.isItalic ? 1 : 0);
        parcel.writeParcelable(self.textAlignment, flags);
        parcel.writeInt(self.enableSelection ? 1 : 0);
        parcel.writeInt(self.htmlFormatting ? 1 : 0);
        parcel.writeParcelable(self.visibilityVariable, flags);
        parcel.writeParcelable(self.enabledVariable, flags);
        parcel.writeInt(self.maxLinesEnabled ? 1 : 0);
        parcel.writeString(self.maxLines);
        parcel.writeInt(self.autoSizeText ? 1 : 0);
        parcel.writeString(self.fontFamily);
        parcel.writeInt(self.enableAutoRefresh ? 1 : 0);
        parcel.writeString(self.padding);
        parcel.writeParcelable(self.buttonClickConfig, flags);
        parcel.writeInt(self.closeSceneOnPress ? 1 : 0);
        parcel.writeParcelable(self.variableToUpdate, flags);
        parcel.writeParcelable(self.variableUpdateValue, flags);
    }
}
