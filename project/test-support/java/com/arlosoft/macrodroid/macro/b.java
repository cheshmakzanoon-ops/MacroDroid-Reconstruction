package com.arlosoft.macrodroid.macro;
import java.util.*;
import defpackage.CoreTrace;
public class b {
 public static defpackage.vq9 k=new defpackage.vq9();
 public ArrayList<Macro> macros=new ArrayList<Macro>();
 public Macro byId,byName;
 public ArrayList w(boolean include){CoreTrace.add("store.list:"+include);return macros;}
 public Macro J(long id){CoreTrace.add("store.id:"+id);return byId;}
 public Macro L(String name){CoreTrace.add("store.name:"+name);return byName;}
public void g(com.arlosoft.macrodroid.actionblock.data.ActionBlock block){CoreTrace.add("store.remove:"+block.testId);}
}
