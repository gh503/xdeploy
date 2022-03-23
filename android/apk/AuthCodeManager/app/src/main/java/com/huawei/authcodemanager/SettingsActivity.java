package com.huawei.authcodemanager;

import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.util.Arrays;

import static android.os.SystemClock.sleep;

public class SettingsActivity extends AppCompatActivity {

    private Context context;
    private EditText idUsername;
    private EditText idPassword;
    private TextView idToken;
    private EditText idServer;
    private EditText idPhone;
    private String username;
    private String password;
    private String httpServer;
    private String token;
    private String phoneNumber;
    private AppUtils appUtils;
    private String[] savedSettings;


    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        this.context = getApplicationContext();
        this.appUtils = new AppUtils(this.context);
        this.idUsername = (EditText) findViewById(R.id.editTextUsername);
        this.idPassword = (EditText) findViewById(R.id.editTextPassword);
        this.idToken = (TextView) findViewById(R.id.textViewTokenValue);
        this.idServer = (EditText) findViewById(R.id.editTextServer);
        this.idPhone = (EditText) findViewById(R.id.editTextPhone);
        this.loadSettings();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void Test(View view) {
        this.username = this.idUsername.getText().toString().trim();
        this.password = this.idPassword.getText().toString().trim();
        this.httpServer = this.idServer.getText().toString().trim();
        this.phoneNumber = this.idPhone.getText().toString().trim();
        if (this.username.length() == 0 || this.password.length() == 0
                || this.httpServer.length() == 0 || this.phoneNumber.length() != 11) {
            String content = "请输入配置再测试!";
            Toast.makeText(this.context, content, Toast.LENGTH_SHORT).show();
        }

        Request request = new Request(this.context);
        request.getToken(this.username, this.password, this.httpServer, this.phoneNumber);
        sleep(1000); //等待子线程执行结束，刷新结果
        this.token = Request.token;
        if (!this.token.equals("")) {
            this.idToken.setText(this.token);
            String content = "测试成功!";
            Toast.makeText(this.context, content, Toast.LENGTH_SHORT).show();
            this.saveSettings();
        }
        else {
            String content = "测试失败!";
            Toast.makeText(this.context, content, Toast.LENGTH_SHORT).show();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    private void loadSettings() {

        this.savedSettings = this.appUtils.readSettings();
        if (Arrays.equals(this.savedSettings, new String[]{})) {
            return;
        }
        if (this.savedSettings.length == 5) {
            this.idUsername.setText(this.savedSettings[0]);
            this.idPassword.setText(this.savedSettings[1]);
            this.idToken.setText(this.savedSettings[2]);
            this.idServer.setText(this.savedSettings[3]);
            this.idPhone.setText(this.savedSettings[4]);
            return;
        }

        SystemInfo systemInfo = new SystemInfo(this.context);
        this.idPhone.setText(systemInfo.phoneNumber);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    private void saveSettings() {
        try {
            String content = "USERNAME: " + this.username + "\n" +
                    "PASSWORD: " + this.password + "\n" +
                    "TOKEN: " + this.token + "\n" +
                    "HTTP_SERVER: " + this.httpServer + "\n" +
                    "PHONE: " + this.phoneNumber + "\n";
            this.appUtils.securityFileUtils.write(content, false);
        } catch (Exception exception) {
            appUtils.logStackTrace(exception.getStackTrace());
        }
    }
}