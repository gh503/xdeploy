package com.huawei.authcodemanager;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.database.ContentObserver;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static android.os.SystemClock.sleep;

public class SMSContentObserver extends ContentObserver {

    public final Uri sms_uri = Uri.parse("content://sms/inbox");
    private final String[] sms_line = {"_id", "date", "body", "read"};
    private final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    private final Pattern pattern = Pattern.compile("验证码");

    private Context context;
    private AppUtils appUtils;

    public SMSContentObserver(Context context, Handler handler) {
        super(handler);
        this.context = context;
        this.appUtils = new AppUtils(this.context);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    public void onChange(boolean selfChange) {
        String[] saveSettings = this.appUtils.readSettings();
        String token = saveSettings[2];
        String httpServer = saveSettings[3];
        String phoneNumber = saveSettings[4];

        long date;
        Request request;
        Matcher matcher;
        String content, strDate, body, read, type, id;
        ContentValues contentValues = new ContentValues();;
        contentValues.put("read", 1);

        super.onChange(selfChange);
        ContentResolver contentResolver = this.context.getContentResolver();
        Cursor cursor = contentResolver.query(
                sms_uri, //路径
                sms_line, //列名
                null, //条件
                null, //条件参数
                "date desc" //排序，默认升序ASC
        );

        if (cursor.moveToFirst()) {
            do {
                id   = cursor.getString(cursor.getColumnIndex("_id"));
                date = cursor.getLong(cursor.getColumnIndex("date"));
                strDate = dateFormat.format(new Date(date));
                body = cursor.getString(cursor.getColumnIndex("body"));
                read = cursor.getString(cursor.getColumnIndex("read"));
                Log.e("new-sms-" + id, "read:" + read);
                if (read.equals("0")) {//未读收件短信
                    content = "(" + strDate + ") " + body;
                    matcher = pattern.matcher(content);
                    if (matcher.find()) {
                        Log.e("new-sms-" + id, body);
                        request = new Request(this.context);
                        request.postSms(token, httpServer, phoneNumber, content);
                        sleep(1000); //等待子线程执行结束，刷新结果
                        if (Request.postResult) {
                            contentResolver.update(
                                    sms_uri,
                                    contentValues,
                                    "_id=" + id,
                                    null
                            );
                            this.appUtils.logInfo(content);
                            Toast.makeText(this.context, "短信发送成功:" + content, Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(this.context, "短信发送失败:" + content, Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            } while(cursor.moveToNext());
            if (!cursor.isClosed()) {
                cursor.close();
            }
        }
    }
}