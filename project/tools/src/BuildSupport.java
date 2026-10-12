import com.android.apksig.*;
import java.io.*;
import java.nio.file.*;
import java.security.*;
import java.security.cert.X509Certificate;
import java.util.*;
/** Signing only. Uses a public development certificate; no identity/integrity bypass. */
public final class BuildSupport {
 public static void main(String[] args) throws Exception {
  if(args.length<2) throw new IllegalArgumentException("sign input.apk output.apk key.p12 | verify file.apk");
  if("sign".equals(args[0])) {
   if(args.length!=4) throw new IllegalArgumentException("sign input.apk output.apk key.p12");
   KeyStore ks=KeyStore.getInstance("PKCS12");
   try(InputStream in=Files.newInputStream(Paths.get(args[3]))){ks.load(in,"android".toCharArray());}
   PrivateKey key=(PrivateKey)ks.getKey("reconstruction","android".toCharArray());
   List<X509Certificate> certificates=new ArrayList<>();
   for(java.security.cert.Certificate c:ks.getCertificateChain("reconstruction")) certificates.add((X509Certificate)c);
   ApkSigner.SignerConfig signer=new ApkSigner.SignerConfig.Builder("RECONSTRUCTION",key,certificates).build();
   new ApkSigner.Builder(Collections.singletonList(signer)).setInputApk(new File(args[1]))
    .setOutputApk(new File(args[2])).setMinSdkVersion(23).setV1SigningEnabled(true)
    .setV2SigningEnabled(true).setV3SigningEnabled(true).setV4SigningEnabled(false)
    .setOtherSignersSignaturesPreserved(false).setAlignmentPreserved(true)
    .setLibraryPageAlignmentBytes(16384).setCreatedBy("MacroDroid source reconstruction v5")
    .build().sign();
   System.out.println("Signed with the shared DEVELOPMENT key; not the publisher identity.");
  } else if("verify".equals(args[0])) {
   ApkVerifier.Result result=new ApkVerifier.Builder(new File(args[1]))
    .setMinCheckedPlatformVersion(23).setMaxCheckedPlatformVersion(36).build().verify();
   System.out.println("verified="+result.isVerified()+" v1="+result.isVerifiedUsingV1Scheme()+" v2="+result.isVerifiedUsingV2Scheme()+" v3="+result.isVerifiedUsingV3Scheme());
   for(var e:result.getAllErrors()) System.out.println("ERROR: "+e);
   for(var w:result.getWarnings()) System.out.println("WARNING: "+w);
   for(X509Certificate c:result.getSignerCertificates()) System.out.println("certificate_sha256="+HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(c.getEncoded())));
   if(!result.isVerified()) throw new SecurityException("APK verification failed");
  } else throw new IllegalArgumentException("Unknown command: "+args[0]);
 }
}
