import os

os.makedirs("app/src/main/res/values", exist_ok=True)
os.makedirs("app/src/main/res/drawable", exist_ok=True)
os.makedirs("app/src/main/java/com/garage/carevo", exist_ok=True)

lt, gt = chr(60), chr(62)

strings = f'{lt}?xml version="1.0" encoding="utf-8"?{gt}\n{lt}resources{gt}\n    {lt}string name="app_name"{gt}Эволюция Тачек{lt}/string{gt}\n{lt}/resources{gt}\n'
open("app/src/main/res/values/strings.xml", "w", encoding="utf-8").write(strings)

manifest = f'''{lt}?xml version="1.0" encoding="utf-8"?{gt}
{lt}manifest xmlns:android="http://android.com"{gt}
    {lt}uses-permission android:name="android.permission.INTERNET" /{gt}
    {lt}application
        android:allowBackup="true"
        android:icon="@drawable/icon"
        android:label="@string/app_name"
        android:usesCleartextTraffic="true"{gt}
        {lt}activity
            android:name="com.garage.carevo.MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"{gt}
            {lt}intent-filter{gt}
                {lt}action android:name="android.intent.action.MAIN" /{gt}
                {lt}category android:name="android.intent.category.LAUNCHER" /{gt}
            {lt}/intent-filter{gt}
        {lt}/activity{gt}
    {lt}/application{gt}
{lt}/manifest{gt}
'''
open("app/src/main/AndroidManifest.xml", "w", encoding="utf-8").write(manifest)

java_code = '''package com.garage.carevo;
import android.app.Activity;
import android.os.Bundle;
import android.view.Window;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        WebView wv = new WebView(this);
        WebSettings s = wv.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        wv.setWebViewClient(new WebViewClient());
        setContentView(wv);
        wv.loadUrl("file:///android_asset/index.html");
    }
}
'''
open("app/src/main/java/com/garage/carevo/MainActivity.java", "w", encoding="utf-8").write(java_code)

build_gradle = '''plugins {
    id 'com.android.application'
}
android {
    namespace 'com.garage.carevo'
    compileSdk 34
    defaultConfig {
        applicationId "com.garage.carevo"
        minSdk 23
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    lint {
        checkReleaseBuilds false
        abortOnError false
    }
    signingConfigs {
        release {
            storeFile file("../release.jks")
            storePassword "123456"
            keyAlias "mykey"
            keyPassword "123456"
        }
    }
    buildTypes {
        release {
            minifyEnabled false
            shrinkResources false
            signingConfig signingConfigs.release
        }
    }
}
'''
open("app/build.gradle", "w", encoding="utf-8").write(build_gradle)
print("ВСЕ ФАЙЛЫ ПЕРЕСОБРАНЫ БЕЗ ОШИБОК!")
