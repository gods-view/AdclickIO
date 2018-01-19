#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: base_req.py
@time: 2017/4/11 上午10:55
"""
import urllib

import logging


class BaseReq:
    def log(self, url, params, response_text):
        if params:
            url = url + '?%s' % urllib.parse.urlencode(params)
        logging.info('url=%s' % url)
        logging.info('response=%s' % response_text)
