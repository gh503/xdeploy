#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml


class FileUtils:
    """
    Process Files Class
    """

    def __init__(self, file):
        if not os.path.isfile(file) and os.system("touch " + file) != 0:
            raise Exception('%s is not a File and failed to create!' % file)
        self.file = os.path.realpath(file)
        self.file_name = os.path.basename(self.file)
        self.file_path = os.path.dirname(self.file)

    def read(self):
        with open(self.file, "r", encoding='utf-8') as handle:
            return handle.read()

    def write(self, data):
        with open(self.file, "w", encoding='utf-8') as handle:
            handle.write(data)

    def read_yaml(self):
        with open(self.file, "r", encoding='utf-8') as handle:
            return yaml.safe_load(handle.read())

    def write_yaml(self, data):
        with open(self.file, "w", encoding='utf-8') as handle:
            yaml.safe_dump(data, handle)


if __name__ == '__main__':
    f = FileUtils(__file__)
    print(__file__)
    print(f.file_name, f.file_path)
    print(f.read())
