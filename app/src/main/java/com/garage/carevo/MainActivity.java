package com.garage.carevo;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import com.yandex.mobile.ads.common.AdError;
import com.yandex.mobile.ads.common.AdRequest;
import com.yandex.mobile.ads.common.AdRequestError;
import com.yandex.mobile.ads.common.ImpressionData;
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
        loader = new RewardedAdLoader(this);
        loader.setAdLoadListener(new RewardedAdLoadListener() {
            @Override
            public void onAdLoaded(RewardedAd ad) {
                rewardedAd = ad;
            }
            @Override
            public void onAdFailedToLoad(AdRequestError err) {
                rewardedAd = null;
            }
        });
        loadAd();

        wv = new WebView(this);
        WebSettings s = wv.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        wv.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void showRewarded() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
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
            loader.loadAd(new AdRequest.Builder(AD_ID).build());
        }
    }

    private void grantReward() {
        if (wv != null) {
            wv.evaluateJavascript("if(typeof bst==='function')bst();", null);
        }
    }
}
