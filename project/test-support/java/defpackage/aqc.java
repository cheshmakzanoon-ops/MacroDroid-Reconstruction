package defpackage; import java.util.regex.Pattern; public class aqc { private final Pattern pattern; public aqc(String s){pattern=Pattern.compile(s);} public String g(String text,String replacement){return pattern.matcher(text).replaceAll(replacement);}  public java.util.List h(int limit,CharSequence text){return java.util.Arrays.asList(pattern.split(text,limit==0?-1:limit));}
}
