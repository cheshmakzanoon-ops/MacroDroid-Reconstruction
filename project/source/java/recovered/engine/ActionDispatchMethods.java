package recovered.engine;
import com.arlosoft.macrodroid.action.*;
import com.arlosoft.macrodroid.actionblock.data.ActionBlock;
import com.arlosoft.macrodroid.app.MacroDroidApplication;
import com.arlosoft.macrodroid.common.MacroDroidVariable;
import com.arlosoft.macrodroid.common.SelectableItem;
import com.arlosoft.macrodroid.constraint.Constraint;
import com.arlosoft.macrodroid.data.ResumeMacroInfo;
import com.arlosoft.macrodroid.debug.events.DebugActionExecutingEvent;
import com.arlosoft.macrodroid.macro.ContinuePausedActionsHandler;
import com.arlosoft.macrodroid.macro.Macro;
import com.arlosoft.macrodroid.macro.b;
import com.arlosoft.macrodroid.triggers.TriggerContextInfo;
import defpackage.*;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Recovered dispatcher. Only this body is compiled into the original Macro class.
 * Pauses and delegated continuations return without ordinary completion. Permission
 * checks, action implementations and Android services remain original dependencies.
 * Original catch boundaries, stack operations and observable call order are retained.
 */
public final class ActionDispatchMethods {
 public static void dispatch(Macro self,List actions,int position,TriggerContextInfo context,
                             boolean force,Stack conditionalStack,ResumeMacroInfo resume){
  // Start and rate guarding are outside the original main catch region.
  self.startMacro();self.activeShellScriptAction=null;self.m_invokeCount++;
  if(self.m_invokeCount>5000){
   long seconds=Math.max(1L,(System.currentTimeMillis()-self.m_invokeStart)/1000L);
   if((long)self.m_invokeCount/seconds>5000L){
    e3g.a(MacroDroidApplication.i(),0x7f141560,0).show();
    String text=new StringBuilder().append(self.getName()).append(" macro attempting to invoke actions too rapidly. If running in a loop you should add a wait before next action to prevent rapid iteration.").toString();
    kjf.g(self.getGUID(),text);self.terminateMacro();return;
   }
  }
  Macro.b loopGuard=new Macro.b(0);
  try{
   actionLoop:
   while(position<actions.size()){
    rl9.a.getClass();
    if(rl9.m(self.m_GUID)){
     if(rl9.q(position,self.breakpoints)){
      rl9.p(position,self.m_GUID);
      synchronized(self.debugLock){
       try{while(true){rl9.a.getClass();if(!rl9.q(position,self.breakpoints)||!rl9.m(self.m_GUID)||!rl9.n())break;self.debugLock.wait();}}
       catch(InterruptedException interrupted){Thread.currentThread().interrupt();break actionLoop;}
      }
      kjf.q(self.m_GUID,new StringBuilder().append("Resumed from debug pause at action ").append(position).toString());
      if(!rl9.m(self.m_GUID))break;
      int requested=rl9.i(self.m_GUID);
      if(requested>=0&&requested>position){position=requested;continue;}
     }else cj5.a().e(new DebugActionExecutingEvent(self.m_GUID,position));
    }
    if(resume!=null&&resume.i>0&&resume.i<=position){self.terminateMacro();return;}
    if(self instanceof ActionBlock){if(((ActionBlock)self).getTopLevelParentMacro()!=null&&((ActionBlock)self).getTopLevelParentMacro().m_cancelFlag)self.m_cancelFlag=true;}
    if(self.m_cancelFlag)break;
    if(!force||self.disabledTimestamp>self.forceEvenIfNotEnabledTimestamp||Macro.macroDroidDisabledTimeStamp>self.forceEvenIfNotEnabledTimestamp){if(!Macro.sMacroDroidEnabled||!self.isEnabled())break;}
    Action action=(Action)actions.get(position);
    if(action instanceof TerminateRunningAction&&((SelectableItem)action).isEnabled()&&((SelectableItem)action).constraintsMet(self.triggerContextInfo)){self.terminateMacro(true);break;}
    if(((SelectableItem)action).getMacro()==null)action.setMacro(self);
    self.setTriggerContextInfo(context);
    boolean eligible=(action instanceof ConditionAction&&((SelectableItem)action).isEnabled())||((SelectableItem)action).constraintsMet(context);
    if(action instanceof EndIfAction||action instanceof ElseParentAction){int opening=aq9.i(actions.indexOf(action),actions);if(opening>=0)eligible=((SelectableItem)(Action)actions.get(opening)).isEnabled();}
    boolean checkResumeAfter=true;
    if(eligible){
     if(action instanceof PauseAction){
      PauseAction pause=(PauseAction)action;int milliseconds=pause.T();
      if(pause.r()!=null){MacroDroidVariable variable=((SelectableItem)pause).getVariableByName(pause.r().D());if(variable!=null){Double value=variable.G(pause.b());if(value!=null){
       if(pause.U()==2)milliseconds=(int)(value.doubleValue()*1.0d);
       else if(pause.U()==0)milliseconds=(int)(value.doubleValue()*1000.0d);
       else if(pause.U()==1)milliseconds=(int)(value.doubleValue()*1000.0d*60.0d);
      }}}
      self.i(action,self.triggerContextInfo,position);
      ContinuePausedActionsHandler.e(self,MacroDroidApplication.i(),position+1,conditionalStack,resume,context,milliseconds,force,pause.W());return;
     }
     if(action instanceof IfConditionAction||action instanceof ElseIfConditionAction||action instanceof ElseIfConfirmedThenAction||action instanceof ActionGroupAction){
      int pendingEnd=((java.util.AbstractCollection)conditionalStack).isEmpty()?0:((Integer)conditionalStack.peek()).intValue();
      if(action instanceof ElseParentAction&&pendingEnd>0){
       if(!self.isDetailLoggingExcluded()){String text=new StringBuilder().append("SKIPPING TO ENDIF (Index ").append(pendingEnd).append(")").toString();kjf.e(self.getGUID(),text,null);}
       conditionalStack.pop();position=pendingEnd;
      }else if(((SelectableItem)action).isEnabled()){
       self.i(action,self.triggerContextInfo,position);
       if(!((SelectableItem)action).constraintsMet(context,true)){
        if(action instanceof IfConditionAction)conditionalStack.push(Integer.valueOf(0));
        if(action instanceof ActionGroupAction)position=aq9.b(position,actions);
        else{
         int end=aq9.d(position,actions),elseIf=aq9.f(position,actions),otherwise=aq9.c(position,actions);
         if(elseIf>=0&&elseIf<end)position=elseIf-1;
         else if(otherwise>=0&&otherwise<end){
          self.i((Action)actions.get(otherwise),self.triggerContextInfo,otherwise);
          if(action instanceof IfConditionAction||action instanceof ElseIfConditionAction){if(!((java.util.AbstractCollection)conditionalStack).isEmpty())conditionalStack.pop();conditionalStack.push(Integer.valueOf(end));}
          position=otherwise;
         }else position=end;
         if(position==-1){sz5.e(new Exception("No corresponding end if or else for an if"));self.terminateMacro();return;}
         if(elseIf==-1&&otherwise==-1&&!((java.util.AbstractCollection)conditionalStack).isEmpty()&&((Integer)conditionalStack.peek()).intValue()==0)conditionalStack.pop();
        }
       }else if(action instanceof IfConfirmedThenAction){((IfConfirmedThenAction)action).invokeAction(context,position+1,force,conditionalStack,resume,false);return;}
       else if(action instanceof ElseIfConfirmedThenAction){((ElseIfConfirmedThenAction)action).invokeAction(context,position+1,force,conditionalStack,resume,false);return;}
       else if(!(action instanceof ActionGroupAction)){
        if(!self.isDetailLoggingExcluded()){String text=new StringBuilder().append("IF CLAUSE TRUE: ").append(((SelectableItem)action).getSystemLogEntryName(context)).toString();kjf.q(self.getGUID(),text);}
        if(!((java.util.AbstractCollection)conditionalStack).isEmpty()&&((Integer)conditionalStack.peek()).intValue()==0)conditionalStack.pop();
        conditionalStack.push(Integer.valueOf(aq9.d(position,actions)));
       }
      }
     }else if(action instanceof ud1){
      self.i(action,self.triggerContextInfo,position);action.debugExecutionGeneration=rl9.j();((ud1)action).invokeAction(context,position+1,force,conditionalStack,resume,false);return;
     }else if(action instanceof SetVariableAction&&((SetVariableAction)action).I0()){
      ((SetVariableAction)action).K0(position+1,context,force,conditionalStack,resume);self.i(action,self.triggerContextInfo,position);return;
     }else if(action instanceof CancelActiveMacroAction&&((CancelActiveMacroAction)action).U()==self.getGUID()&&!((CancelActiveMacroAction)action).T()){
      self.i(action,self.triggerContextInfo,position);self.terminateMacro();return;
     }else if(action instanceof LoopAction){
      LoopAction loop=(LoopAction)action;
      if(loop.B0()){self.i(action,self.triggerContextInfo,position);loop.I0();if(loop.A0()==4)loop.H0();}
      if(loop instanceof IterateDictionaryAction){
       IterateDictionaryAction dictionary=(IterateDictionaryAction)loop;
       if(loop.B0())((IterateDictionaryAction)loop).X0();
       if(!dictionary.Y0(context)){
        self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f140ea7));yc.c(self,dictionary);zc.c(self,loop);((IterateDictionaryAction)loop).X0();
        int end=aq9.e(position,actions);if(end==-1){sz5.e(new Exception("No corresponding end loop for a loop"));self.terminateMacro();return;}position=end;
       }else{loop.C0();if(yc.b(self)!=dictionary)yc.a(self,(IterateDictionaryAction)loop);if(zc.b(self)!=loop)zc.a(self,loop);}
      }else if(loop.A0()==1&&((SelectableItem)loop).isEnabled()){
       if(!((SelectableItem)action).constraintsMet(context)){
        self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f140ea8));zc.c(self,loop);int end=aq9.e(position,actions);if(end==-1){sz5.e(new Exception("No corresponding end loop for a loop"));self.terminateMacro();return;}position=end;
       }else{loop.C0();if(zc.b(self)!=loop)zc.a(self,loop);}
      }else if(loop.A0()==0&&((SelectableItem)loop).isEnabled()){
       if(!loop.D0()){
        self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f140ea7));loop.I0();zc.c(self,loop);int end=aq9.e(position,actions);if(end==-1){sz5.e(new Exception("No corresponding end loop for a loop"));self.terminateMacro();return;}position=end;
       }else if(zc.b(self)!=loop)zc.a(self,loop);
      }else if(loop.A0()==4&&((SelectableItem)loop).isEnabled()){
       if(loop.E0()){
        self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f14023a));zc.c(self,loop);int end=aq9.e(position,actions);if(end==-1){sz5.e(new Exception("No corresponding end loop for a loop"));self.terminateMacro();return;}position=end;
       }else{loop.C0();if(zc.b(self)!=loop)zc.a(self,loop);}
      }else if(loop.A0()==2&&((SelectableItem)loop).isEnabled()){loop.C0();if(zc.b(self)!=loop)zc.a(self,loop);}
      else if(loop.A0()==3&&((SelectableItem)loop).isEnabled()){loop.C0();if(zc.b(self)!=loop)zc.a(self,loop);}
     }else if(action instanceof EndLoopAction){
      int opening=aq9.j(position,actions);if(opening>=0){LoopAction loop=(LoopAction)actions.get(opening);if(((SelectableItem)loop).isEnabled()){
       loop.J0(false);
       if(loop.A0()==2&&!((SelectableItem)loop).constraintsMet(context)){self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f140ea8));zc.c(self,loop);}
       else{if(loopGuard.a(self,loop))return;position=opening-1;}
       checkResumeAfter=false;
      }}
     }else if(action instanceof BreakFromLoopAction){
      self.i(action,self.triggerContextInfo,position);int end=aq9.e(position,actions),opening=aq9.k(end,actions);
      if(opening>=0){
       LoopAction loop=(LoopAction)actions.get(opening);self.j(loop,((android.content.Context)MacroDroidApplication.i()).getString(0x7f14007f));Object candidate=actions.get(opening);
       if(candidate instanceof IterateDictionaryAction){yc.c(self,(IterateDictionaryAction)candidate);((IterateDictionaryAction)candidate).X0();}else((LoopAction)actions.get(opening)).I0();
       zc.c(self,loop);
       for(int scan=position+1;scan<end;scan++){if(actions.get(scan)instanceof EndIfAction){int start=aq9.i(scan,actions);if(start>=0&&((SelectableItem)(Action)actions.get(start)).isEnabled()&&start<position&&!((java.util.AbstractCollection)conditionalStack).isEmpty())conditionalStack.pop();}}
       if(end>=0){self.invokeActions(actions,end+1,context,force,conditionalStack,resume);return;}
      }
     }else if(action instanceof ContinueLoopAction){
      self.i(action,self.triggerContextInfo,position);int opening=aq9.k(position,actions);
      if(opening>=0){LoopAction loop=(LoopAction)actions.get(opening);if(loop!=null&&((SelectableItem)loop).isEnabled())loop.J0(false);int end=aq9.e(opening,actions);
       if(end>=0){for(int scan=position+1;scan<end;scan++){if(actions.get(scan)instanceof EndIfAction){int start=aq9.i(scan,actions);if(start>=0&&((SelectableItem)(Action)actions.get(start)).isEnabled()&&start<position&&!((java.util.AbstractCollection)conditionalStack).isEmpty())conditionalStack.pop();}}}
       position=opening-1;checkResumeAfter=false;
      }
     }else if(action instanceof GotoAction){
      self.i(action,self.triggerContextInfo,position);GotoAction jump=(GotoAction)action;String label=jump.W();int found=-1;
      for(int scan=0;scan<actions.size();scan++){if(label.equals(((Action)actions.get(scan)).getActionLabel())){found=scan;break;}}
      if(found>=0){Map scopes=Action.computeActionScopes(actions);e6 currentScope=(e6)scopes.get(jump);e6 destinationScope=(e6)scopes.get(actions.get(found));
       if(j$.util.Objects.equals(currentScope,destinationScope)){position=found-1;checkResumeAfter=false;}
       else kjf.t(self.m_GUID,new StringBuilder().append("Goto: label '").append(label).append("' is at a different nesting level").toString());
      }else kjf.t(self.m_GUID,new StringBuilder().append("Goto: label '").append(label).append("' not found").toString());
     }else if(action instanceof ElseAction){
      if(!((java.util.AbstractCollection)conditionalStack).isEmpty())conditionalStack.pop();int opening=aq9.i(position,actions);
      if(opening==-1){sz5.e(new Exception("No corresponding if for an else clause"));self.terminateMacro();return;}
      if(((SelectableItem)(Action)actions.get(opening)).isEnabled()){int end=aq9.d(position,actions);if(end==-1){sz5.e(new Exception("No corresponding end if for an else clause"));self.terminateMacro();return;}position=end;}
     }else if(!(action instanceof ActionGroupEndAction)&&action instanceof EndParentAction){
      if(!((java.util.AbstractCollection)conditionalStack).isEmpty())conditionalStack.pop();
     }else{
      if(action instanceof ShellScriptAction)self.activeShellScriptAction=(ShellScriptAction)action;
      if(!(action instanceof SeparatorAction)){
       self.i(action,self.triggerContextInfo,position);
       if(rl9.m(self.m_GUID)){
        CountDownLatch done=new CountDownLatch(1);android.os.Handler handler=new android.os.Handler(android.os.Looper.getMainLooper());handler.post(new h13(action,context,done,7));
        try{if(!done.await(5L,TimeUnit.MINUTES))kjf.g(self.m_GUID,"Debug mode action timed out after 5 minutes");}catch(InterruptedException interrupted){Thread.currentThread().interrupt();}
       }else action.invokeActionWithPermissionCheck(context);
      }
     }
    }
    if(checkResumeAfter&&resume!=null&&resume.i>0&&resume.i==position+1){self.terminateMacro();return;}
    position++;
   }
   if(self.isActionBlock){
    if(((ActionBlock)self).isTestMode())self.e();
    if(self.isClonedInstance){kjf.w(self.getGUID());for(Object candidate:self.getActions()){for(Object constraint:((SelectableItem)(Action)candidate).getConstraints())((Constraint)constraint).a0();}b.k.a().g((ActionBlock)self);}
   }
   if(resume!=null){
    self.l(resume);if(resume.b<0)return;
    Macro parent=b.k.a().J(resume.a);
    if(parent!=null){rl9.a.getClass();if(rl9.l())new Thread(new com.arlosoft.macrodroid.macro.a(resume,parent)).start();else parent.invokeActions(parent.m_actionList,resume.b,resume.c,resume.d,resume.e,resume.f);}
    else kjf.u(new StringBuilder().append("Could not find parent macro to resume: ").append(resume.a).toString());
   }
  }catch(StackOverflowError overflow){String text=((android.content.Context)MacroDroidApplication.i()).getString(0x7f140dc6);kjf.q(self.getGUID(),text);}
  catch(Throwable failure){String text=new StringBuilder("Error invoking action: ").append(failure).toString();kjf.g(self.getGUID(),text);}
  self.terminateMacro();
 }
}
