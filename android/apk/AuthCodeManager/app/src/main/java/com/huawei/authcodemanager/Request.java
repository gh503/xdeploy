package com.huawei.authcodemanager;

import android.content.Context;
import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.security.MessageDigest;


public class Request {

    public static String token = "";
    public static boolean postResult = false;
    private static int postCode;
    private static JSONObject message;

    private Context context;
    private AppUtils appUtils;

    public Request(Context context) {
        this.context = context;
        this.appUtils = new AppUtils(this.context);
    }

    public void getToken(String username, String password, String httpServer, String phoneNumber) {
        new Thread() {
            @RequiresApi(api = Build.VERSION_CODES.KITKAT)
            @Override
            public void run() {
                try {
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put("username", username);
                    jsonObject.put("password", getSha256sum(password));
                    jsonObject.put("phoneNumber", phoneNumber);
                    jsonObject.put("operate", "get");
                    jsonObject.put("msg", "client device authentication");
                    String content = String.valueOf(jsonObject);
                    postRequest(httpServer, "/token", content);
                    if (postCode == 200 && (int) message.get("status") == 200) {
                        token = message.get("token").toString();
                    }
                }
                catch (JSONException jsonException) {
                    appUtils.logStackTrace(jsonException.getStackTrace());
                }
                catch (Exception exception) {
                    exception.printStackTrace();
                    appUtils.logStackTrace(exception.getStackTrace());
                }
            }
        }.start();
    }

    public void postSms(String pToken, String httpServer, String phoneNumber, String sms) {
        new Thread() {
            @RequiresApi(api = Build.VERSION_CODES.KITKAT)
            @Override
            public void run() {
                try {
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put("token", pToken);
                    jsonObject.put("phoneNumber", phoneNumber);
                    jsonObject.put("sms", sms);
                    jsonObject.put("msg", "new sms received");
                    String content = String.valueOf(jsonObject);
                    postRequest(httpServer, "/sms/new", content);
                    if (postCode == 200 && (int) message.get("status") == 200) {
                        postResult = true;
                    }
                    else {
                        postResult = false; //避免上次结果残留
                    }
                    Log.e("get post result", String.valueOf(postResult));
                }
                catch (JSONException jsonException) {
                    appUtils.logStackTrace(jsonException.getStackTrace());
                }
                catch (Exception exception) {
                    appUtils.logStackTrace(exception.getStackTrace());
                }
            }
        }.start();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    private void postRequest(String httpServer, String route, String content) {
        HttpURLConnection httpURLConnection;
        OutputStream outputStream = null;
        try {
            URL httpUrl = new URL(httpServer + route);
            httpURLConnection = (HttpURLConnection) httpUrl.openConnection();
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Content-Type", "application/json");
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setDoInput(true);
            outputStream = httpURLConnection.getOutputStream();
            outputStream.write(content.getBytes());
            outputStream.flush();
            postCode = httpURLConnection.getResponseCode();
            InputStream inputStream = httpURLConnection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            StringBuilder stringBuilder = new StringBuilder();
            while((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line);
            }
            message = new JSONObject(String.valueOf(stringBuilder));
        } catch (MalformedURLException malformedURLException) {
            malformedURLException.printStackTrace();
            this.appUtils.logStackTrace(malformedURLException.getStackTrace());
        } catch (ProtocolException protocolException) {
            protocolException.printStackTrace();
            this.appUtils.logStackTrace(protocolException.getStackTrace());
        } catch (ConnectException connectException) {
            connectException.printStackTrace();
            this.appUtils.logStackTrace(connectException.getStackTrace());
        } catch (IOException ioException) {
            ioException.printStackTrace();
            this.appUtils.logStackTrace(ioException.getStackTrace());
        } catch (JSONException jsonException) {
            jsonException.printStackTrace();
            this.appUtils.logStackTrace(jsonException.getStackTrace());
        } catch (Exception exception) {
            exception.printStackTrace();
            this.appUtils.logStackTrace(exception.getStackTrace());
        }
        finally {
            try {
                outputStream.close();
            }
            catch (Exception exception) {
                return;
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    private static String getSha256sum(String string) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        StringBuilder result = new StringBuilder();
        for (byte b : md.digest(string.getBytes())) {
            result.append(String.format("%02x", b));
        }
        return result.toString();
    }
}