#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: file_gen.py
@time: 2019-07-19 09:55
@discription: 
"""

import os, sys

# coding=gbk

import hashlib
import os
import time


def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def create_file(size):
    file_name = str(time.time()) + '.temp'
    with open(file_name, 'wb') as f:
        f.write(os.urandom(size))

    return file_name


def main():
    file_size = 0
    unit = 'MB'
    size = 1

    print("Generating file with size " + str(size) + unit)

    if unit == 'KB':
        file_size = size * 1024
    if unit == 'MB':
        file_size = size * 1024 * 1024
    if unit == 'GB':
        file_size = size * 1024 * 1024 * 1024

    file_name = create_file(file_size)

    file_md5 = get_file_md5(file_name)
    os.rename(file_name, file_md5 + '.dat')

    print('Generating file : '+ file_md5 + '.dat finish. ')

if __name__ == '__main__':
    main()
