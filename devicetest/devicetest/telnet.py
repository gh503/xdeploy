#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib
import time

from devicetest.common import isavailable


class TelnetClient:
    """telnetlib二次封装"""

    crlf = '\r\n'

    def __init__(self, host, port, username, password, prompt_str='%') -> None:
        port = str(port) if isinstance(port, int) else port
        self._host, self._port, self._username, self._password, self._prompt_str = \
            host, port, username, password, prompt_str
        self._telnet = telnetlib.Telnet()
        self._connected = False
        self.__connect()

    def __connect(self) -> None:
        """连接会话"""
        if isavailable(self._host):
            raise TimeoutError('网络地址{}不可达！'.format(self._host))
        self._telnet.open(self._host, self._port)
        self._telnet.read_until(b'login:', timeout=5)
        self._telnet.write(bytes('{}{}'.format(self._username, TelnetClient.crlf), encoding='utf-8'))
        self._telnet.read_until(b'assword:', timeout=5)
        self._telnet.write(bytes('{}{}'.format(self._password, TelnetClient.crlf), encoding='utf-8'))
        time.sleep(2)
        buf = self._telnet.read_very_eager().decode(encoding='utf-8', errors='ignore')
        if self._prompt_str in buf:
            print('登入{}成功！'.format(self._host))
        else:
            raise ValueError("登入{}失败！请检查账号密码是否正确！".format(self._host))
        self._connected = True

    def __del__(self) -> None:
        self._telnet.write(bytes('exit{}'.format(TelnetClient.crlf)))

    def reconnect(self) -> None:
        if not self._connected:
            self.__connect()

    def send(self, cmd, timeout=30, wait=True, match=None, retry=3) -> str:
        if not self._connected:
            self.__connect()
        begin_index, end_index, begin_flag, end_str = None, None, False,\
            match if match is not None else self._prompt_str
        result = ''
        deadline = timeout + time.monotonic()
        while retry >= 0:
            try:
                self._telnet.write(bytes('{}{}'.format(cmd, TelnetClient.crlf)))
                if not wait:
                    return ""
                buf = self._telnet.read_very_eager().decode(encoding='utf-8', errors='ignore')
                result += buf
                if not begin_flag and cmd in result:
                    begin_flag = True
                    begin_index = result.find(cmd) + len(cmd) + len(TelnetClient.crlf)
                if begin_flag and end_str in result[begin_index:]:
                    end_index = result.find(end_str, begin_index)
                if begin_index is not None and end_index is not None:
                    result = result[begin_index:end_index]
                    break
                if deadline <= time.monotonic():
                    print("执行命令{}超时！".format(cmd))
                    break
            except Exception as message:
                print("执行命令{}过程中出现异常:{}！当前重试次数{}...".format(cmd, message, retry))
                retry -= 1
                self.reconnect()
        if retry <= 0:
            raise Exception("执行命令{}失败！".format(cmd))
        return result


if __name__ == '__main__':
    pass
