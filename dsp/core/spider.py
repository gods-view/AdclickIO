# encoding=utf-8
import sys
from imp import reload

reload(sys)
# sys.setdefaultencoding('utf8')

import os, time
# from configure import config
from datetime import datetime as dt
import requests


# requests.adapters.DEFAULT_RETRIES = 5
# import chardet


class HttpSpider:
    headers = {
        # 'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        # 'Connection':'keep-alive',
        # 'Content-Type: application/json'
        # "Accept-Encoding":"gzip,deflate"
        # "Authorization": "Bearer 5f6f8a89a85b6bde10c69198ca9a2e8ea9f13bf8"
    }

    def __init__(self):
        pass

    def show_error(self, error_log, msg):
        if error_log is None:
            print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg)
        else:
            error_log.error(msg)

    def internal_get(self, url, timeout=5, headers=''):
        # print (headers)
        # print (type(headers["Authorization"]))
        # self.headers = timeouts
        # print (type(self.headers["Authorization"]))
        if headers == '':
            response = requests.get(url, headers=self.headers, timeout=timeout)
        else:
            response = requests.get(url, headers=headers, timeout=timeout)
        # print (response.content)
        if response:
            return response.status_code, response.text
        else:
            return response.content, None

    def internal_post(self, url, data, timeout=5, headers=''):
        # print (data, type(data))
        if headers == '':
            response = requests.post(url, data, headers=self.headers, timeout=timeout)
        else:
            response = requests.post(url, data, headers=headers, timeout=timeout)
        print (response, response.content)
        if response:
            return response.status_code, response.text
        else:
            return response.content, None

    def internal_patch(self, url, data, timeout=5):
        # print (data)
        response = requests.patch(url, data, headers=self.headers, timeout=timeout)
        # print (response, response.content)
        if response:
            return response.content, response.text
        else:
            return response.content, None

    def internal_put(self, url, data, timeout=5, headers=''):
        # print (data)
        if headers == '':
            response = requests.put(url, data, headers=self.headers, timeout=timeout)
        else:
            response = requests.put(url, data, headers=headers, timeout=timeout)
        print (response, response.content)
        if response:
            return response.status_code, response.text
        else:
            return response.content, None
