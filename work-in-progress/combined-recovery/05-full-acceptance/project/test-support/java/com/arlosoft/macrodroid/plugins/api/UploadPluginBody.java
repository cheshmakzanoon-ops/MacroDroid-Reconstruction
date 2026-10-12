package com.arlosoft.macrodroid.plugins.api;
import defpackage.PluginControl;
/** Constructor boundary with the preserved null checks and field-assignment order. */
public final class UploadPluginBody {
    public int userId;
    public String name, developerName, description, packageName, downloadLink, iconUrl, website, language;
    public UploadPluginBody(int userId, String name, String developerName, String description,
            String packageName, String downloadLink, String iconUrl, String website, String language) {
        PluginControl.constructed(this, "uploadBody", new Object[]{userId, name, developerName,
                description, packageName, downloadLink, iconUrl, website, language});
        name.getClass(); developerName.getClass(); description.getClass();
        packageName.getClass(); downloadLink.getClass(); website.getClass(); language.getClass();
        this.userId = userId; this.name = name; this.developerName = developerName;
        this.description = description; this.packageName = packageName;
        this.downloadLink = downloadLink; this.iconUrl = iconUrl;
        this.website = website; this.language = language;
    }
}
