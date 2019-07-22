#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: test.py
@time: 2019-07-20 21:47
@discription: 
"""
import hashlib
import os


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

