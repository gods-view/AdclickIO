#!/usr/bin/env python
# encoding: utf-8
import requests
from affiliate.common.encryption import Encryption


class YeahmobiReq:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = Encryption.md5(password)

    def get_offer_by_page(self, page):
        """
        按页码获取offer
        :param page: 页码
        :return: raw_data 原始返回值
        """
        query = {'api_id': self.username,
                 'api_token': self.password,
                 'limit': 100,  # Limit the number of items returned per page. No more than 100 items. Default to 30
                 'page': page,  # Page by the limit of items returned. Defaults to page 1
                 }
        response = requests.request("GET", self.url, params=query)
        print (response, response.content, page)
        return response.json()

    def get_pages(self):
        """
        获取page的数量
        :return: flag,totalpage,first_data
        """
        query = {'api_id': self.username,
                 'api_token': self.password,
                 'limit': 100,
                 'page': 1
                 }
        response = requests.request("GET", self.url, params=query)
        # print (response, response.content)
        raw_data = response.json()
        if raw_data['flag'] == 'success':
            return 'success', raw_data['data']['totalpage'], raw_data['data']['data']
        else:
            return 'fail', 0, ''
