package com.huawei.authcodemanager;

import android.content.Context;
import android.telephony.TelephonyManager;

import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class SystemInfo {
    public String phoneNumber;
    public int simState;

    private Context context;
    private final static Pattern patternPhoneNumber = Pattern.compile("\\d{11}");

    public SystemInfo(Context context) {
        this.context = context;
        TelephonyManager tm = (TelephonyManager) this.context.getSystemService(Context.TELEPHONY_SERVICE);
        this.simState = tm.getSimState();
        Matcher result = patternPhoneNumber.matcher(tm.getLine1Number());
        if (result.find()) {
            this.phoneNumber = result.group(0);
        }
    }
}
