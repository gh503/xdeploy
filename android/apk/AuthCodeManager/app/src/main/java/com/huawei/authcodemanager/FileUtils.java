package com.huawei.authcodemanager;

import android.content.Context;
import android.os.Build;

import androidx.annotation.RequiresApi;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;


public class FileUtils {

    private Context context;
    //操作文件对象
    private String objFileName;
    private File objFile;
    //文件存储位置标记
    private boolean externalFlag;

    //应用在内部存储中的files路径
    private static String internalFilesPath;
    //应用在外部存储中的files路径
    private static String externalFilePath;

    public FileUtils(Context context, String fileName, boolean externalFlag) {
        this.context = context;
        this.objFileName = fileName;
        this.externalFlag = externalFlag;
        internalFilesPath = this.context.getFilesDir().getAbsolutePath();
        externalFilePath = this.context.getExternalFilesDir("").getAbsolutePath();
        if (this.externalFlag) {
            this.objFile = new File(externalFilePath, this.objFileName);
        }
        else {
            this.objFile = new File(internalFilesPath, this.objFileName);
        }
        try {
            this.createDir(internalFilesPath);
            this.createDir(externalFilePath);
            this.createFile(this.objFile);
        }
        catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void write(String content, boolean append) throws Exception {
        try {
            FileOutputStream handle = new FileOutputStream(this.objFile, append);
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(handle, StandardCharsets.UTF_8);
            outputStreamWriter.append(content);
            outputStreamWriter.close();
        }
        catch (Exception exception) {
            throw new Exception(exception);
        }
    }

    public void clear() throws Exception {
        try {
            FileWriter fileWriter = new FileWriter(this.objFile);
            fileWriter.write("");
            fileWriter.flush();
            fileWriter.close();
        }
        catch (Exception exception) {
            throw new Exception(exception);
        }
    }

    public String read() throws Exception {
        try {
            FileInputStream handle = new FileInputStream(this.objFile);
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            byte[] buffer = new byte[256];
            int len = 0;
            while ((len = handle.read(buffer)) != -1) {
                byteArrayOutputStream.write(buffer, 0, len);
            }
            byte[] data = byteArrayOutputStream.toByteArray();
            String content = new String(data);
            handle.close();
            byteArrayOutputStream.close();
            return content;
        }
        catch (Exception exception) {
            throw new Exception(exception);
        }
    }

    private void createFile(File dstFile) throws Exception {
        try {
            if (!dstFile.exists()) {
                dstFile.createNewFile();
            }
        }
        catch (Exception exception) {
            throw new Exception(exception);
        }
    }

    private void createDir(String dstDir) throws Exception {
        try {
            File dir = new File(dstDir);
            if (!dir.exists()) {
                dir.mkdirs();
            }
        }
        catch (Exception exception) {
            throw new Exception(exception);
        }
    }
}