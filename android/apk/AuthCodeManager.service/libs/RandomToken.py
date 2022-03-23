#!/usr/bin/env python3
r"""
RandomToken class is designed for generate token transferred between
client and server. Token generates from base_str with fixed length
specified with var random_length. And the random token shall not be
timeout util server update the token.
"""
# -*- coding: utf-8 -*-


import os
import random
from itsdangerous import JSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from libs.FileUtils import FileUtils


class RandomToken:
    """Generate Random Token Class"""

    @staticmethod
    def generate_random_key(length=16)->str:
        """generate fix length random key"""
        base_str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%'
        random_str = ''
        base_max_index = len(base_str) - 1
        for i in range(length):
            random_str += base_str[random.randint(0, base_max_index)]
        return random_str

    @staticmethod
    def generate_token(random_key, phone_num)->str:
        """generate random token"""
        serializer = Serializer(random_key)
        file_utils = FileUtils(os.path.join('client', phone_num))
        random_token = str(serializer.dumps({ 'phoneNumber': phone_num}), encoding='utf-8')
        file_utils.write(random_token)
        print(random_token)
        return random_token

    @staticmethod
    def check_token(random_key, client_token):
        """check client token"""
        serializer = Serializer(random_key)
        try:
            return serializer.loads(client_token)
        except SignatureExpired:
            return 'SignatureExpired'
        except BadSignature:
            return 'BadSignature'


if __name__ == '__main__':
    rand_key = RandomToken.generate_random_key()
    print(rand_key)
    token = RandomToken.generate_token(rand_key, 'demo')
    print(token)
    data = RandomToken.check_token(rand_key, token)
    print(data)
