#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import paramiko
import threading
import time
import termios
import select
import tty
import sys

from devicetest.common import isavailable


class SshClient:
    """paramiko二次封装. SSHClient+SFtpClient"""

    hostos = platform.system().lower()
    if hostos == 'windows':
        crlf = '\r\n'
    elif hostos == 'linux':
        crlf = '\n'
    else:
        crlf = '\r'

    def __init__(self, host, port, username, password, prompt_str='%') -> None:
        """初始化"""
        self._host, self._port, self._username, self._password, self._prompt_str = \
            host, int(port) if isinstance(port, str) else port, username, password, prompt_str
        self._ssh = paramiko.SSHClient()
        self.__connect()

    def __connect(self) -> None:
        """连接transport"""
        if not isavailable(self._host):
            raise TimeoutError("网络地址{}不可达！".format(self._host))
        # paramiko自动报异常
        self._ssh._transport = paramiko.Transport((self._host, self._port))
        self._ssh._transport.start_client()
        self._ssh._transport.auth_password(username=self._username, password=self._password)
        self._sftp = paramiko.SFTPClient.from_transport(self._ssh._transport)

    def __del__(self) -> None:
        if hasattr(self._ssh, '_transport'):
            self._ssh._transport.close()
            self._ssh._transport = None

    def reconnect(self) -> None:
        """重新连接transport"""
        if self._ssh.get_transport() is not None:
            self.__connect()

    def send(self, cmd, wait=True, timeout=5, match=None, environment=None, retry=3) -> str:
        """
        channel连接发送命令
        @param: str cmd: 待发送命令
        @param: bool wait: 等待回显
        @param: float timeout: 等待回显超时
        @param: str match: 匹配字符串
        @param: dict environment: 环境变量
        @param: int retry: 异常重试次数
        @return: 命令回显
        """
        while retry >= 0:
            try:
                channel = self._ssh._transport.open_session()
                channel.set_combine_stderr(True)
                channel.setblocking(1)  # 0 non-blocking mode; non-0 blocking mode.
                if isinstance(environment, dict):
                    channel.update_environment(environment)
                result = ''
                channel.exec_command(cmd)

                if not wait:
                    return result

                deadline = timeout + time.monotonic()
                stdout = channel.makefile('r', -1)
                while True:
                    buf = stdout.readline()
                    result += buf
                    if match is not None and match in result:
                        break
                    if stdout.channel.exit_status_ready():
                        break
                    if deadline < time.monotonic():
                        print("执行{}超时！".format(cmd))
                        break
                return result
            except Exception as message:
                print("执行命令{}过程中出现异常：{} 当前重试次数{}...".format(cmd, message, retry))
                retry -= 1
                self.reconnect()
        if retry <= 0:
            raise Exception("执行命令{}失败！请检查！".format(cmd))

    def sfget(self, remote_path, local_path) -> bool:
        """
        下载远端文件到本地
        @param: remote_path: 远端文件路径
        @param: local_path: 本地存储文件路径
        """
        if self._sftp is None:
            return False
        remote_path = remote_path.strip().replace(r'\\', '/').replace('\\', '/')
        local_path = local_path.strip().replace(r'\\', '/').replace('\\', '/')
        print("下载{}:{}到{}...".format(self._host, remote_path, local_path))
        self._sftp.get(remote_path, local_path)
        return True

    def sfput(self, local_path, remote_path) -> bool:
        """
        上传本地文件到远端
        @param: local_path: 本地文件路径
        @param: remote_path: 远端文件存储路径
        """
        if self._sftp is None:
            return False
        local_path = local_path.strip().replace(r'\\', '/').replace('\\', '/')
        remote_path = remote_path.strip().replace(r'\\', '/').replace('\\', '/')
        print("上传{}到{}:{}...".format(local_path, self._host, remote_path))
        self._sftp.put(local_path, remote_path)
        return True


class Terminal(object):
    """
    交互性终端。
        仅支持下发命令;
        不能获取命令回显;
        支持with操作;
        拷机测试，反复执行命令场景;
    """

    def __init__(self, sshclient) -> None:
        """初始化
        @param sshclient: SshClient 类实例
        """
        self.client = sshclient

    def __enter__(self):
        """with进入新建终端，返回self"""
        self.channel, self.oldtty = self.__terminal()
        return self

    def __exit__(self, Type, value, traceback):
        """with退出关闭终端"""
        self.__close_terminal()

    def __del__(self):
        """关闭通道"""
        self.channel.close()

    def __terminal(self) -> None:
        """创建交互式操作终端"""
        print("entering terminal...")
        channel = self.client._ssh._transport.open_session()
        channel.set_combine_stderr(True)
        channel.setblocking(False)
        channel.get_pty()
        channel = self.client._ssh.invoke_shell()
        oldtty = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)

        def read():
            while True:
                if channel.get_transport() is None:
                    return
                readlist, _, _ = select.select([sys.stdin,], [], [])
                # 检测并发送用户输入命令
                if sys.stdin in readlist:
                    input_char = sys.stdin.read(1)
                    channel.sendall(input_char)

        def write():
            while True:
                if channel.get_transport() is None:
                    return
                readlist, _, _ = select.select([channel,], [], [])
                # 检测到通道收到服务器返回结果
                if channel in readlist:
                    result = channel.recv(1024)
                    if len(result) == 0:
                        return
                    sys.stdout.write(result.decode(encoding='utf-8', errors='ignore'))
                    sys.stdout.flush()

        threading.Thread(target=read, name='read', daemon=True).start()
        threading.Thread(target=write, name='write', daemon=True).start()
        time.sleep(1)
        return (channel, oldtty)

    def __close_terminal(self) -> None:
        """关闭终端，恢复终端设置"""
        time.sleep(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldtty)

    def send(self, cmd) -> None:
        """终端执行命令"""
        for c in cmd:
            self.channel.send(c)
        self.channel.send(SshClient.crlf)

class ROTerminal(object):
    """
    只读性终端。
        不支持手工输入命令;
        支持返回命令执行结果;
        支持with操作;
    TODO:交互性终端使用死循环会导致终端挂死
    """

    def __init__(self, sshclient) -> None:
        """初始化
        @param sshclient: SshClient 类实例
        """
        self.client = sshclient

    def __enter__(self):
        """with进入新建终端，返回self"""
        self.channel, self.oldtty = self.__terminal()
        return self

    def __exit__(self, Type, value, traceback):
        """with退出关闭终端"""
        self.__close_terminal()

    def __del__(self):
        """关闭通道"""
        self.channel.close()

    def __terminal(self) -> None:
        """创建只读终端"""
        channel = self.client._ssh._transport.open_session()
        channel.set_combine_stderr(True)
        channel.setblocking(False)
        channel.get_pty()
        channel = self.client._ssh.invoke_shell()
        oldtty = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)

        while True:
            buf = channel.recv(256).decode(encoding='utf-8', errors='ignore')
            sys.stdout.write(buf)
            sys.stdout.flush()
            if self.client._prompt_str in buf:
                break

        time.sleep(1)
        return (channel, oldtty)

    def __close_terminal(self) -> None:
        """关闭终端，恢复终端设置"""
        time.sleep(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldtty)

    def send(self, cmd, match=None) -> None:
        """终端执行命令"""
        for c in cmd:
            self.channel.send(c)
        self.channel.sendall(SshClient.crlf)

        result = ''
        begin_index, end_index, begin_flag, end_str = 0, -1, False,\
            self.client._prompt_str if match is None else match
        while True:
            buf = self.channel.recv(256).decode(encoding='utf-8', errors='ignore')
            result += buf
            sys.stdout.write(buf)
            sys.stdout.flush()
            if cmd in result:
                begin_flag = True
                begin_index = result.find(cmd) + len(cmd) + len(SshClient.crlf)
            if begin_flag and end_str in result[begin_index:]:
                end_index = result.find(end_str, begin_index) + 1
                result = result[begin_index:end_index]
                break
        return result


if __name__ == '__main__':
    ssh = SshClient('localhost', '22', 'demo', '1234', '%')

    res = ssh.send('lscpu && sleep 4', timeout=1, match='VT-x')
    print(res)
    ssh.send('cd /home')
    res = ssh.send('echo $SSH_CLIENT, $TEST_VAR, $PWD,', environment=dict(TEST_VAR='/data/code'))
    print(res)

    with Terminal(ssh) as terminal:
        terminal.send('pwd')
        terminal.send('lsblk')
        terminal.send('cat /proc/cpuinfo')

    with ROTerminal(ssh) as terminal:
        terminal.send('pwd')
        terminal.send('lsblk')
        terminal.send('cat /proc/cpuinfo')
