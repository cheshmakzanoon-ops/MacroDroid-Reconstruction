package defpackage;
public final class xj2 {public static java.util.List c1(Iterable input,int n){if(n<0)throw new IllegalArgumentException();java.util.ArrayList out=new java.util.ArrayList();for(Object value:input){if(n--==0)break;out.add(value);}return out;}public static Object L0(java.util.List a){return a.isEmpty()?null:a.get(a.size()-1);}
}
