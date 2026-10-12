package com.arlosoft.macrodroid.scene.components;
import com.arlosoft.macrodroid.scene.data.*;
/** Constructor/fields are host boundaries; no compiled stub enters the app APK. */
public class SceneTextConfig implements android.os.Parcelable {
 public String text;
 public int textColor;
 public SceneVariableData textColorVariable;
 public String textSize;
 public boolean isBold;
 public boolean isItalic;
 public SceneAlignment textAlignment;
 public boolean enableSelection;
 public boolean htmlFormatting;
 public SceneVariableData visibilityVariable;
 public SceneVariableData enabledVariable;
 public boolean maxLinesEnabled;
 public String maxLines;
 public boolean autoSizeText;
 public String fontFamily;
 public boolean enableAutoRefresh;
 public String padding;
 public ButtonClickConfig buttonClickConfig;
 public boolean closeSceneOnPress;
 public SceneVariableData variableToUpdate;
 public SceneVariableUpdateValue variableUpdateValue;
 public SceneTextConfig(String text, int textColor, SceneVariableData textColorVariable, String textSize, boolean isBold, boolean isItalic, SceneAlignment textAlignment, boolean enableSelection, boolean htmlFormatting, SceneVariableData visibilityVariable, SceneVariableData enabledVariable, boolean maxLinesEnabled, String maxLines, boolean autoSizeText, String fontFamily, boolean enableAutoRefresh, String padding, ButtonClickConfig buttonClickConfig, boolean closeSceneOnPress, SceneVariableData variableToUpdate, SceneVariableUpdateValue variableUpdateValue) {
  text.getClass(); textSize.getClass();
  this.text=text;
  this.textColor=textColor;
  this.textColorVariable=textColorVariable;
  this.textSize=textSize;
  this.isBold=isBold;
  this.isItalic=isItalic;
  this.textAlignment=textAlignment;
  this.enableSelection=enableSelection;
  this.htmlFormatting=htmlFormatting;
  this.visibilityVariable=visibilityVariable;
  this.enabledVariable=enabledVariable;
  this.maxLinesEnabled=maxLinesEnabled;
  this.maxLines=maxLines;
  this.autoSizeText=autoSizeText;
  this.fontFamily=fontFamily;
  this.enableAutoRefresh=enableAutoRefresh;
  this.padding=padding;
  this.buttonClickConfig=buttonClickConfig;
  this.closeSceneOnPress=closeSceneOnPress;
  this.variableToUpdate=variableToUpdate;
  this.variableUpdateValue=variableUpdateValue;
 }
 public int describeContents(){return 0;} public void writeToParcel(android.os.Parcel out,int flags){throw new UnsupportedOperationException("fixture body");}
 public static class a implements android.os.Parcelable.Creator<SceneTextConfig> {
  public SceneTextConfig createFromParcel(android.os.Parcel in){throw new UnsupportedOperationException("fixture body");}
  public SceneTextConfig[] newArray(int n){return new SceneTextConfig[n];}
 }
}
