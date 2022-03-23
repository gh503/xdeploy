package com.huawei.authcodemanager;

import android.content.Context;
import android.os.Build;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AppUtils {
    public FileUtils stackFileUtils;
    public FileUtils securityFileUtils;
    public FileUtils smsCodeFileUtils;

    private Context context;
    private final static Pattern PATTERN_SETTINGS = Pattern.compile("USERNAME: ([\\w-]+)\n" +
            "PASSWORD: ([\\w!@#$%-_.]+)\n" +
            "TOKEN: ([\\w-_.]+)\n" +
            "HTTP_SERVER: ([\\w:/.]+)\n" +
            "PHONE: (\\d{11})\n");

    public AppUtils(Context context) {
        this.context = context;
        //内存路径：/data/data/com.huawei.authcodemanager/files
        this.securityFileUtils = new FileUtils(this.context, "security", false);
        //外存路径：/sdcard/Android/data/com.huawei.authcodemanager/files
        this.stackFileUtils = new FileUtils(this.context, "stackTrace.txt", true);
        this.smsCodeFileUtils = new FileUtils(this.context, "SMSCode.txt", true);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void logStackTrace(StackTraceElement stack[]) {
        try {
            StringBuilder content = new StringBuilder();
            content.append("\n操作发生异常:");
            for (int i = 0; i < stack.length; i++) {
                content.append("\n").append(i).append(" ").append(stack[i].getClassName()).append(": ").append(stack[i].getMethodName());
            }
            this.stackFileUtils.write(content.toString(), true);
        }
        catch (Exception exception) {
            exception.printStackTrace();
            Toast.makeText(this.context, "记录异常调用栈信息时发生异常!", Toast.LENGTH_SHORT).show();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void logInfo(String content) {
        try {
            this.smsCodeFileUtils.write(content + "\n", true);
        }
        catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public String[] readSettings() {
        try {
            String saved = this.securityFileUtils.read();
            Matcher matcher = PATTERN_SETTINGS.matcher(saved);
            if (matcher.find()) {
                return new String[]{
                        Objects.requireNonNull(matcher.group(1)).trim(), //username
                        Objects.requireNonNull(matcher.group(2)).trim(), //passwdSha256sum
                        Objects.requireNonNull(matcher.group(3)).trim(), //token
                        Objects.requireNonNull(matcher.group(4)).trim(), //httpServer
                        Objects.requireNonNull(matcher.group(5)).trim()  //PhoneNumber
                };
            }
        } catch (Exception exception) {
            logStackTrace(exception.getStackTrace());
        }
        return new String[]{};
    }
}