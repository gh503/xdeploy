#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='devicetest',
    version='0.1',
    author='arobot123',
    author_email='angus_robot@163.com',
    packages=find_packages(),
    requires=['paramiko']
)
