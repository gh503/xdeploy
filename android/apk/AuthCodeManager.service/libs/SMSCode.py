#!/usr/bin/env python3
r"""SMSCode class processes applications sms authentication code,
analysing the sms content and saving the result as the file under
appsms and reading the app sms code.
"""
# -*- coding: utf-8 -*-


import os
import re

from libs.FileUtils import FileUtils


class SMSCode:
    """SMS Code class"""

    # 所有键值应该以实际短信为准:
    #【爱奇艺】您的验证码是459862，转发给他人可能导致账号被盗，请勿泄漏，谨防被骗。
    #【阿里巴巴钉钉】验证码：1681，15分钟内输入有效，立即登录
    #【腾讯科技】验证码:  747021（15分钟内有效）。该验证码用于登录企业微信，请勿泄露该验证码。
    #【腾讯科技】你正在登录微信，验证码222132。转发可能导致帐号被盗。如果这不是你本人操作，回复JZ可阻止该用户登录你的微信。
    #【腾讯科技】532964（短信登录验证码），请勿转发，否则会导致QQ被盗。如不想接收此类短信，请回复TD退订。
    #【腾讯会议】验证码796230（10分钟内有效）。如非本人操作，请忽略本短信。
    #【今日头条】验证码8190，用于手机登录，5分钟内有效。验证码提供给他人可能导致帐号被盗，请勿泄露，谨防被骗。
    #【阿里巴巴钉钉】验证码：4682，15分钟内输入有效，立即登录
    #【乐逗游戏】验证码：0457，5分钟内有效。如非本人操作请忽略本短信
    #【豆瓣网】豆瓣登录验证码：8623，切勿泄露或转发他人，以防帐号被盗。如非本人操作请忽略本短信。验证码20分钟内有效。
    #【喜马拉雅】验证码:332926，10分钟内可用。请勿向任何人泄露。
    #【学习强国】验证码：1577，15分钟内输入有效，立即登录
    #【抖音】验证码8362，用于手机登录，5分钟内有效。验证码提供给他人可能导致帐号被盗，请勿泄露，谨防被骗。
    #【同花顺】(554540)为您的验证码,如非本人操作请忽略。
    #【百度帐号】验证码：698634 。您正在使用短信验证码登录功能，该验证码仅用于身份验证，请勿泄露给他人使用。
    #【拼多多】您正在登录拼多多，验证码是376401。请于5分钟内完成验证，若非本人操作，请忽略本短信。
    APP_NAME_MAPPING = {
        '【爱奇艺】': 'aiqiyi',
        '【阿里巴巴钉钉】': 'dingding',
        '【乐逗游戏】': 'ditiepaoku',
        '【豆瓣网】': 'douban',
        '【抖音】': 'douyin',
        '今日头条': 'jinritoutiao',
        '【腾讯会议】': 'tengxunhuiyi',
        '登录微信': 'weixin',
        '登录企业微信': 'qiyeweixin',
        'QQ': 'qq',
        '【同花顺】': 'tonghuashun',
        '【学习强国】': 'xuexiqiangguo',
        '【百度帐号】': 'baidu',
        '【拼多多】': 'pinduoduo',
        '【知乎】': 'zhihu',
        '【喜马拉雅】': 'ximalaya',
        '【支付宝】': 'zhifubao'
    }
    APP_CODE_PATTERN = [
        re.compile(r'(\d{8})'),
        re.compile(r'(\d{6})'),
        re.compile(r'(\d{4})[^\-\d]')
    ]
    APP_TMMIN_PATTERN = [                
        re.compile(r'\D(\d+)\s?分钟')
    ]

    @staticmethod
    def analyse(phone_num, sms_content)->tuple:
        """analyse sms content and save the code

        @param phone_num: client device ID
        @param sms_content: sms content
        @return Bool: True success; False fail
        """
        app_name = sms_code = None
        time_min = 0
        for key in SMSCode.APP_NAME_MAPPING:
            if key in sms_content:
                app_name = SMSCode.APP_NAME_MAPPING[key]
                break
        for item in SMSCode.APP_CODE_PATTERN:
            test = item.findall(sms_content)
            if len(test) != 0:
                sms_code = test[0]
                break
        for item in SMSCode.APP_TMMIN_PATTERN:
            test = item.findall(sms_content)
            if len(test) != 0:
                time_min = test[0]
                break
        if app_name is None or sms_code is None:
            return False
        file_path = os.path.join('appsms', app_name)
        os.system('mkdir -p %s' % file_path)
        code_file = FileUtils(os.path.join(file_path, phone_num))
        code_file.write(sms_code + ', ' + str(time_min) + ' minutes, ' + sms_content)
        return True

    @staticmethod
    def get_app_sms(phone_num, app_name)->str:
        """get app sms authentication code

        @param phone_num: client device ID
        @param app_name: client application name
        @return str: app sms authentication code
        """
        code_file = os.path.join('appsms', app_name, phone_num)
        if os.path.isfile(code_file):
            file_utils = FileUtils(code_file)
            return file_utils.read()
        return ''


if __name__ == '__main__':
    result = SMSCode.analyse('demo', '【学习强国】验证码：1844，15分钟内输入有效，立即登入')
    print('analyse content:', result[0], result[1])
    sms = SMSCode.get_app_sms('demo', 'xuexiqiangguo')
    print('get_app_smscode:', sms)
