#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: avazu.py
@time: 2017/3/29 下午5:35
"""
import requests

"""
username:18629

password:
23011
22433
22417
22416
"""


class AvazuReq:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_all_offer(self):
        query = {
            'uid': self.username,
            'sourceid': self.password,
            'pagesize': 9999999999999999
        }
        response = requests.request("GET", self.url, params=query)
        if (response):
            return response.json()
        return dict()


import requests


class Avazu():
    def __init__(self, api_username, api_token):
        self.api_id = api_username
        self.api_token = api_token

    def get_all_offer(self):
        url = 'http://api.c.avazutracking.net/performance/v2/getcampaigns.php'
        header = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        query = {
            'uid': self.api_id,
            # 'page': 1,
            'sourceid': self.api_token,
        }
        response = requests.request("GET", url, params=query)
        if (response):
            return response.text
        else:
            return ''
            # return response.json()


if __name__ == '__main__':
    api_id = '18629'
    api_token = '23011'  # dsp
    # api_token = '22433'# incentive traffic
    # api_token = '22417'# FB
    # api_token = '22416'# Google Adwords
    avazu = Avazu(api_id, api_token)
    print(avazu.get_all_offer())
