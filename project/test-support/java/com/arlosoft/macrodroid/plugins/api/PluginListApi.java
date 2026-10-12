package com.arlosoft.macrodroid.plugins.api;
import defpackage.m73;
import okhttp3.MultipartBody$Part;
/** Controlled upload boundaries only. No HTTP operation occurs in host tests. */
public interface PluginListApi {
    Object uploadNonPlayStoreAppIcon(MultipartBody$Part part, m73 continuation);
    Object uploadPlayStorePlugin(String hash, UploadPluginBody body, m73 continuation);
}
