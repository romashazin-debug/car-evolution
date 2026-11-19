open("build.gradle", "w").write("plugins {\n    id 'com.android.application' version '8.7.2' apply false\n}\n")

open("app/build.gradle", "w").write('''plugins {
    id 'com.android.application'
}
android {
    namespace 'com.garage.carevo'
    compileSdk 35
    defaultConfig {
        applicationId "com.garage.carevo"
        minSdk 23
        targetSdk 35
        versionCode 2
        versionName "1.1"
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
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
            signingConfig signingConfigs.release
        }
    }
}
dependencies {
    implementation 'com.yandex.android:mobileads:8.6.0'
}
''')

open("app/src/main/java/com/garage/carevo/MainActivity.java", "w").write('''package com.garage.carevo;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import com.yandex.mobile.ads.common.AdError;
import com.yandex.mobile.ads.common.AdRequestConfiguration;
import com.yandex.mobile.ads.common.AdRequestError;
import com.yandex.mobile.ads.common.ImpressionData;
import com.yandex.mobile.ads.common.YandexAds;
import com.yandex.mobile.ads.rewarded.Reward;
import com.yandex.mobile.ads.rewarded.RewardedAd;
import com.yandex.mobile.ads.rewarded.RewardedAdEventListener;
import com.yandex.mobile.ads.rewarded.RewardedAdLoadListener;
import com.yandex.mobile.ads.rewarded.RewardedAdLoader;

public class MainActivity extends Activity {
    private WebView wv;
    private RewardedAd rewardedAd;
    private RewardedAdLoader loader;
    private final String AD_ID = "R-M-20450627-1";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        YandexAds.initialize(this, () -> loadAd());
        loader = new RewardedAdLoader(this);
        loader.setAdLoadListener(new RewardedAdLoadListener() {
            @Override public void onAdLoaded(RewardedAd ad) { rewardedAd = ad; }
            @Override public void onAdFailedToLoad(AdRequestError err) { rewardedAd = null; }
        });

        wv = new WebView(this);
        WebSettings s = wv.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        wv.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void showRewarded() {
                runOnUiThread(() -> {
                    if (rewardedAd != null) {
                        rewardedAd.setAdEventListener(new RewardedAdEventListener() {
                            @Override public void onAdShown() {}
                            @Override public void onAdFailedToShow(AdError e) { grantReward(); loadAd(); }
                            @Override public void onAdDismissed() { rewardedAd = null; loadAd(); }
                            @Override public void onAdClicked() {}
                            @Override public void onAdImpression(ImpressionData d) {}
                            @Override public void onRewarded(Reward r) { grantReward(); }
                        });
                        rewardedAd.show(MainActivity.this);
                    } else {
                        grantReward();
                        loadAd();
                    }
                });
            }
        }, "AndroidAds");
        wv.setWebViewClient(new WebViewClient());
        setContentView(wv);
        wv.loadUrl("file:///android_asset/index.html");
    }

    private void loadAd() {
        if (loader != null) {
            loader.loadAd(new AdRequestConfiguration.Builder(AD_ID).build());
        }
    }

    private void grantReward() {
        if (wv != null) wv.evaluateJavascript("if(typeof bst==='function')bst();", null);
    }
}
''')

html = open("app/src/main/assets/index.html", encoding="utf-8").read()
old_btn = "if(sdk)sdk.adv.showRewardedVideo({callbacks:{onRewarded:bst}});else bst()"
new_btn = "if(window.AndroidAds)window.AndroidAds.showRewarded();else if(sdk)sdk.adv.showRewardedVideo({callbacks:{onRewarded:bst}});else bst()"
open("app/src/main/assets/index.html", "w", encoding="utf-8").write(html.replace(old_btn, new_btn))
print("РЕКЛАМА ЯНДЕКСА R-M-20450627-1 ВСТРОЕНА!")
