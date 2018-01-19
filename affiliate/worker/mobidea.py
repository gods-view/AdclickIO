#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: mobidea.py
@time: 2017/4/11 下午4:22
"""
import json

from affiliate.model.mysql_model import ThirdPartyOffer
from affiliate.req.mobidea import MobideaReq
from affiliate.worker.base_worker import BaseWorker
import xml.etree.ElementTree as ET

from affiliate.common.helper import Helper


class MobideaWork(BaseWorker):
    def __init__(self, taskId, userId, url, username, password):
        BaseWorker.__init__(self, taskId, userId, url, username, password)

    def start(self):
        print (self.username, self.password)
        mobidea_req = MobideaReq(url=self.url, username=self.username, password=self.password)
        flag, msg, result = mobidea_req.get_all_offer()
        # print (result, flag, "测试输出")
        if flag:
            self.delete_old_offers()
            root = ET.fromstring(result)
            # print(result)
            url = ''
            # print (root)
            for offer in root.findall('offer'):
                # print(offer)
                name = offer.find('name').text
                status = offer.find('status').text
                category = offer.find('category').text
                if offer.find('url') is not None:
                    url = offer.find('url').text
                print(url)
                items = offer.find('payouts').find('items').findall('item')
                countryCode, carrier, platform = [], [], []
                payouts_info = []
                for item in items:
                    country = Helper.fix_country_str(item.get('country'))
                    currency = item.get('currency')
                    operator = item.get('operator')  # carrier
                    os = item.get('os')
                    countryCode.append(country)
                    carrier.append(operator)
                    platform.append(os)
                    payoutValue = item.text
                    payouts_info.append({'country': country,
                                         'currency': currency,
                                         'operator': operator,
                                         'os': os,
                                         'payoutValue': payoutValue})

                detail = {'name': name,
                          'status': status,
                          'category': category,
                          'url': url,
                          'payouts': payouts_info}

                offer_data = {
                    'sourcename': 'Mobidea',
                    'userId': self.userId,
                    'taskId': self.taskId,
                    'status': 1 if status == 'active' else 2,
                    'offerId': name.split('-')[0].strip(),
                    'name': name,
                    'trackingLink': self.fix_tracklink_url(url),
                    'countryCode': ','.join(list(set(countryCode))),  # 这里需要转换country到三位
                    'payoutValue': float(payoutValue),
                    'category': category,
                    'carrier': json.dumps(list(set(carrier))),
                    'platform': json.dumps(list(set(platform))),
                    'detail': json.dumps(detail),
                }
                ThirdPartyOffer.delete().where(ThirdPartyOffer.offerId == name.split('-')[0].strip()).execute()
                ThirdPartyOffer.insert(offer_data).execute()
        else:
            raise Exception(msg)
