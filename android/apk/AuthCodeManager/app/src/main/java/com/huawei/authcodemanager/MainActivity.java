package com.huawei.authcodemanager;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;


public class MainActivity extends AppCompatActivity {

    private AppUtils appUtils;
    private SMSContentObserver smsContentObserver = null;

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //申请存储卡读写权限
        int permissionSDWrite = ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.WRITE_EXTERNAL_STORAGE);
        int permissionSDRead = ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.READ_EXTERNAL_STORAGE);
        int permissionPhoneNumber = ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.READ_PHONE_NUMBERS);
        int permissionPhoneState = ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.READ_PHONE_STATE);
        int permissionSMS = ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.READ_SMS);
        if(permissionSDWrite != PackageManager.PERMISSION_GRANTED
                || permissionSDRead != PackageManager.PERMISSION_GRANTED
                || permissionPhoneNumber != PackageManager.PERMISSION_GRANTED
                || permissionPhoneState != PackageManager.PERMISSION_GRANTED
                || permissionSMS != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "正在请求权限", Toast.LENGTH_SHORT).show();
            //申请权限，特征码自定义为1，可在回调时进行相关判断
            ActivityCompat.requestPermissions(MainActivity.this,
                    new String[]{ Manifest.permission.WRITE_EXTERNAL_STORAGE,
                            Manifest.permission.READ_EXTERNAL_STORAGE,
                            Manifest.permission.READ_PHONE_NUMBERS,
                            Manifest.permission.READ_PHONE_STATE,
                            Manifest.permission.READ_SMS},
                    1);
        }
        appUtils = new AppUtils(this.getApplicationContext());
    }

    public void RunService(View view) {
        if (this.smsContentObserver != null) {
            Toast.makeText(this.getApplicationContext(), "服务已经运行", Toast.LENGTH_SHORT).show();
        }
        else {
            this.smsContentObserver = new SMSContentObserver(view.getContext(), new Handler());
            getContentResolver().registerContentObserver(this.smsContentObserver.sms_uri,
                    true,
                    this.smsContentObserver);
            Toast.makeText(this.getApplicationContext(), "运行服务", Toast.LENGTH_SHORT).show();
        }
    }

    //TODO
    public void ReadLogs(View view) {
        Toast.makeText(this.getApplicationContext(), "读取日志", Toast.LENGTH_SHORT).show();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void ClearLogs(View view) {
        Toast.makeText(this.getApplicationContext(), "清除日志", Toast.LENGTH_SHORT).show();
        try {
            this.appUtils.smsCodeFileUtils.clear();
        }
        catch (Exception exception) {
            this.appUtils.logStackTrace(exception.getStackTrace());
        }
    }

    public void StopService(View view) {
        if (this.smsContentObserver != null) {
            getContentResolver().unregisterContentObserver(this.smsContentObserver);
            this.smsContentObserver = null;
            Toast.makeText(this.getApplicationContext(), "停止服务", Toast.LENGTH_SHORT).show();
        }
        else {
            Toast.makeText(this.getApplicationContext(), "服务未运行", Toast.LENGTH_SHORT).show();
        }
    }

    public void SetLanguage(View view) {
        LanguageUtils.settingLanguage(MainActivity.this, LanguageUtils.getInstance());
        MainActivity.this.recreate();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void Settings(View view) {
        Intent intent = new Intent(MainActivity.this, SettingsActivity.class);
        startActivity(intent);
        //高版本不finish()程序会异常退出, 导致需要重新进入app操作
        finish();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        if (requestCode == 1) {
            if (grantResults.length <= 0 || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                String content = "获取SD卡读写权限失败，请在设置中重新设定权限!";
                Toast.makeText(this.getApplicationContext(), content, Toast.LENGTH_SHORT).show();
            }
            finish();
        }
        else {
            super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}