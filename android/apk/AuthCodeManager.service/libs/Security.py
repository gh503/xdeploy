#!/usr/bin/env python3
r"""
Security class is designed for client authentication.
Client sends data with token sha256sum instead username
and password or raw token to server.
"""
# -*- coding: utf-8 -*-


import os
import time

from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES

from libs.FileUtils import FileUtils
from libs.RandomToken import RandomToken


class Security:
    """process client authentication"""

    @staticmethod
    def auth_user(username, password, phone_num, operate)->tuple:
        """client authentication

        @param  username: client username
        @param  password: client password
        @param  phone_num: client phoneNumber
        @param  operate: token operation: get for saved token; update for new token
        @return tuple: True success; False fail
        """
        file_sec = FileUtils(os.path.join('.', 'security'))
        security = file_sec.read_yaml()
        if username in security.keys() and \
                password == security[username]['passwdSha256sum']:
            if operate == 'get':
                file_token = FileUtils(os.path.join('.', 'client', phone_num))
                token = file_token.read()
                result = (True, token)
            elif operate == 'update':
                random_token = RandomToken()
                random_key = random_token.generate_random_key()
                result = (True, random_token.generate_token(random_key, phone_num))
            else:
                result = (False, '')
        else:
            result = (False, '')
        return result

    @staticmethod
    def auth_token(client_token, phone_num)->bool:
        """check client token

        @param  client_token: client token
        @param  phone_num: client phone number
        @return str: Pass return client data; Fail return ''
        """
        file_utils = FileUtils(os.path.join('client', phone_num))
        if client_token == file_utils.read():
            return True
        else:
            return False

    @staticmethod
    def encrypt(data, secret_key)->str:
        """encrpt data"""
        cipher = AES.new(secret_key.encode('utf-8'),
                         AES.MODE_CBC,
                         Security.__get_timestamp().encode('utf-8'))
        result = cipher.encrypt(Security.__padding(data.encode('utf-8')))
        return Security.__padding(b2a_hex(result))

    @staticmethod
    def decrypt(data, secret_key)->str:
        """decrypt data"""
        cipher = AES.new(secret_key.encode('utf-8'),
                         AES.MODE_CBC,
                         Security.__get_timestamp().encode('utf-8'))
        result = cipher.decrypt(a2b_hex(data))
        return Security.__un_padding(result)

    @staticmethod
    def __padding(encrpt_data)->str:
        """data encrypted add bits"""
        return encrpt_data + \
               (16 - len(encrpt_data) % 16) * chr(16 - len(encrpt_data) % 16).encode('utf-8')

    @staticmethod
    def __un_padding(decrypt_data)->str:
        """data decrypted remove bits"""
        return decrypt_data[0:-(decrypt_data[-1])].decode('utf-8')

    @staticmethod
    def __get_timestamp()->str:
        return str(int(time.time() * 1000)).rjust(16, '0')
