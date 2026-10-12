package defpackage;
public class yih {
 public static final java.util.regex.Pattern a=java.util.regex.Pattern.compile("[{}()\\[\\].+^$\\\\|]");
 public static String a(String text,boolean lower){return recovered.environment.MatchingMethods.containsPattern(text,lower);}
 public static String b(String text,boolean regex,boolean lower){if(EnvironmentControl.recoveredMatching)return recovered.environment.MatchingMethods.contains(text,regex,lower);CoreTrace.add("match.contains:"+text);return "contains:"+text;}
 public static String c(String text,boolean regex,boolean lower){if(EnvironmentControl.recoveredMatching)return recovered.environment.MatchingMethods.full(text,regex,lower);CoreTrace.add("match.full:"+text);return "full:"+text;}
 public static boolean d(String name,String pattern,boolean regex,boolean lower){if(EnvironmentControl.recoveredMatching)return recovered.environment.MatchingMethods.matches(name,pattern,regex,lower);CoreTrace.add("match.test:"+name+":"+pattern);return name!=null&&(pattern.startsWith("contains:")?name.contains(pattern.substring(9)):name.equals(pattern.substring(5)));}
}
