#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: mobidea.py
@time: 2017/4/11 下午2:58
"""
import urllib

import requests

from affiliate.req.base_req import BaseReq


class MobideaReq(BaseReq):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_all_offer(self):

        """
        
        :return: flag,msg,result_string
        """
        params = {'login': self.username,
                  'password': self.password,
                  'currency': 'USD',
                  'tags': 'status,category,payouts,url',
                  }
        url = self.url + '?%s' % urllib.parse.urlencode(params, safe=',')
        response = requests.request("GET", url)
        print (response.text)
        self.log(url, '', response.text)
        # print (response.status_code, response.text)
        if response.status_code == 401:
            return False, 'login or password error', ''
        elif response.status_code != 200:
            return False, 'unknown error', ''
        return True, 'success', response.text
