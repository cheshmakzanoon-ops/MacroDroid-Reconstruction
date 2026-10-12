package recovered.engine;
import com.arlosoft.macrodroid.action.*;
import com.arlosoft.macrodroid.common.SelectableItem;
import java.util.List;
/** Original structural traversal rules, including disabled ELSE and active-loop handling. */
public final class ActionNavigationMethods {
 public static int groupEnd(int position,List actions){int depth=1;for(position++;position<actions.size();position++){Action a=(Action)actions.get(position);if(a instanceof ActionGroupAction)depth++;else if(a instanceof ActionGroupEndAction && --depth==0)return position;}return -1;}
 public static int otherwise(int position,List actions){int depth=1;position++;while(position<actions.size()&&depth>0){Action a=(Action)actions.get(position);if(a instanceof IfConditionAction)depth++;else if(a instanceof EndIfAction)depth--;else if(((SelectableItem)a).isEnabled()&&a instanceof ElseAction&&depth==1)return position;position++;}return -1;}
 public static int conditionalEnd(int position,List actions){int depth=1;for(position++;position<actions.size();position++){Action a=(Action)actions.get(position);if(a instanceof IfConditionAction)depth++;else if(a instanceof EndIfAction&&--depth==0)return position;}return -1;}
 public static int loopEnd(int position,List actions){int depth=1;for(position++;position<actions.size();position++){Action a=(Action)actions.get(position);if(a instanceof LoopAction)depth++;else if(a instanceof EndLoopAction&&--depth==0)return position;}return -1;}
 public static int elseIf(int position,List actions){int depth=1;for(position++;position<actions.size();position++){Action a=(Action)actions.get(position);if(a instanceof IfConditionAction)depth++;else if(a instanceof EndIfAction){if(--depth==0)return -1;}else if(((SelectableItem)a).isEnabled()&&(a instanceof ElseIfConditionAction||a instanceof ElseIfConfirmedThenAction)&&depth==1)return position;}return -1;}
 public static int conditionalStart(int position,List actions){int depth=1;for(position--;position>=0;position--){Action a=(Action)actions.get(position);if(a instanceof EndIfAction)depth++;else if(a instanceof IfConditionAction&&--depth==0)return position;}return -1;}
 public static int loopStart(int position,List actions){int depth=1;for(position--;position>=0;position--){Action a=(Action)actions.get(position);if(a instanceof EndLoopAction)depth++;else if(a instanceof LoopAction&&--depth==0)return position;}return -1;}
 public static int activeLoopStart(int position,List actions){int depth=1;for(position--;position>=0;position--){Action a=(Action)actions.get(position);if(a instanceof EndLoopAction&&((SelectableItem)a).isEnabled()){int start=defpackage.aq9.j(position,actions);if(start!=-1&&((SelectableItem)(Action)actions.get(start)).isEnabled())depth++;}else if(a instanceof LoopAction&&((SelectableItem)a).isEnabled()){if(--depth==0)return position;}}return -1;}
}
