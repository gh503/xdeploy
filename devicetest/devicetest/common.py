#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import platform


def isavailable(ip) -> bool:
    """测试目标IP是否可达"""
    hostos = platform.system().lower()
    if hostos == 'windows':
        return subprocess.call(['ping', '-n', '1', ip], stdout=subprocess.DEVNULL) == 0
    elif hostos == 'linux':
        return subprocess.call(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL) == 0
    else:
        print("当前未支持{}!".format(hostos))
        return True
