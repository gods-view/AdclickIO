#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: encryption.py
@time: 2017/3/28 下午10:16
"""
import hashlib


class Encryption:
    def __init__(self):
        pass

    @classmethod
    def md5(cls, src):
        src = src.encode(encoding='gb2312')
        m2 = hashlib.md5()
        m2.update(src)
        return m2.hexdigest()
