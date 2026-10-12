package com.arlosoft.macrodroid.action;import defpackage.*;
public class LoopAction extends ParentAction {
 public int type,remaining=2,iterations,resets,maxIterations=2;public boolean first=true,timedOut;
 public int A0(){CoreTrace.add(testId+".loopType");return type;}public boolean B0(){CoreTrace.add(testId+".loopFirst");return first;}
 public void C0(){CoreTrace.add(testId+".loopIncrement");iterations++;}public boolean D0(){CoreTrace.add(testId+".loopRemaining:"+remaining);return remaining-->0;}
 public boolean E0(){CoreTrace.add(testId+".loopTimedOut");return timedOut||iterations>=maxIterations;}
 public void H0(){CoreTrace.add(testId+".loopStartTimer");}public void I0(){CoreTrace.add(testId+".loopReset");resets++;}public void J0(boolean v){CoreTrace.add(testId+".loopSetFirst:"+v);first=v;}
}
