package recovered.engine;
import com.arlosoft.macrodroid.action.*;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import defpackage.e6;
import defpackage.xj2;
/** Parent and ELSE-branch identities, rather than merely numeric nesting depth. */
public final class ActionScopeMethods {
 public static Map compute(List actions){Action.Companion.getClass();return Action.a.d(actions);}
 public static LinkedHashMap scopes(List actions){
  actions.getClass();LinkedHashMap result=new LinkedHashMap();ArrayList parents=new ArrayList();ArrayList branches=new ArrayList();branches.add(null);
  for(Object candidate:actions){Action action=(Action)candidate;
   if(action instanceof EndParentAction){
    if(!parents.isEmpty()){parents.remove(parents.size()-1);branches.remove(branches.size()-1);}
    ((Map)result).put(action,new e6((ParentAction)xj2.L0(parents),(ElseParentAction)xj2.L0(branches)));
   }else if(action instanceof ElseParentAction){
    branches.set(branches.size()-1,action);
    ((Map)result).put(action,new e6((ParentAction)xj2.L0(parents),(ElseParentAction)action));
   }else{
    ((Map)result).put(action,new e6((ParentAction)xj2.L0(parents),(ElseParentAction)xj2.L0(branches)));
    if(action instanceof ParentAction){parents.add(action);branches.add(null);}
   }
  }
  return result;
 }
}
