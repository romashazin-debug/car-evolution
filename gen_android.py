open("settings.gradle", "w").write('rootProject.name = "CarEvolution"\ninclude ":app"\n')
open("build.gradle", "w").write('buildscript { repositories { google(); mavenCentral() } dependencies { classpath "com.android.tools.build:gradle:8.2.2" } }\nallprojects { repositories { google(); mavenCentral() } }\n')
open("gradle.properties", "w").write('android.useAndroidX=true\norg.gradle.jvmargs=-Xmx1536m\n')

open("app/build.gradle", "w").write('''apply plugin: 'com.android.application'
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
    buildTypes { release { minifyEnabled false } }
}
dependencies { implementation 'androidx.appcompat:appcompat:1.6.1' }
''')

open("app/src/main/AndroidManifest.xml", "w").write('''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://android.com">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:label="Эволюция Тачек" android:icon="@drawable/icon" android:theme="@style/Theme.AppCompat.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true" android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''')

open("app/src/main/java/com/garage/carevo/MainActivity.java", "w").write('''package com.garage.carevo;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
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
''')

open(".github/workflows/build.yml", "w").write('''name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }
      - uses: gradle/actions/setup-gradle@v3
        with: { gradle-version: '8.5' }
      - name: Generate Keystore and Build Signed APK
        run: |
          keytool -genkey -v -keystore release.jks -alias mykey -keyalg RSA -keysize 2048 -validity 10000 -storepass 123456 -keypass 123456 -dname "CN=GarageDev,O=Dev,C=RU"
          gradle assembleRelease
          $ANDROID_HOME/build-tools/34.0.0/zipalign -v -p 4 app/build/outputs/apk/release/app-release-unsigned.apk app-aligned.apk
          $ANDROID_HOME/build-tools/34.0.0/apksigner sign --ks release.jks --ks-pass pass:123456 --out CarEvolution-release.apk app-aligned.apk
      - uses: actions/upload-artifact@v4
        with:
          name: CarEvolution-APK
          path: |
            CarEvolution-release.apk
            release.jks
''')
print("ПРОЕКТ ANDROID СГЕНЕРИРОВАН!")
