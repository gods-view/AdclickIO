#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: avazu.py
@time: 2017/3/29 下午5:41
"""
import json
import re
from affiliate.common.helper import Helper
from affiliate.req.clickdealer import ClickdealerReq
from affiliate.model.mysql_model import ThirdPartyOffer, OfferSyncTask, ThirdPartyCountryCode
import xml.etree.ElementTree as ET
from affiliate.worker.base_worker import BaseWorker


class ClickdealerWork(BaseWorker):
    def __init__(self, taskId, userId, url, username, password):
        BaseWorker.__init__(self, taskId, userId, url, username, password)

    def start(self):
        print ("ClickDealer worker")
        clickdealerreq = ClickdealerReq(url=self.url, username=self.username, password=self.password)
        raw_data = clickdealerreq.get_all_offer()
        raw_data_list = raw_data.split('</offer>')
        for c_raw_data in raw_data_list:
            #

            # re_cule = '[0-9a-zA-Z,\:\/\_\.\*\-\+!\?\$ \t\n\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+'
            item = {}
            if '<offer_id>' in c_raw_data:
                try:
                    item['offerId'] = c_raw_data.split('<offer_id>')[-1].split('</offer_id>')[0]
                except:
                    continue
            else:
                continue
            if '<status_name>' in c_raw_data:
                try:
                    item['status'] = c_raw_data.split('<status_name>')[-1].split('</status_name>')[0]
                except:
                    item['status'] = None
            if '<offer_name>' in c_raw_data:
                try:
                    item['name'] = c_raw_data.split('<offer_name>')[-1].split('</offer_name>')[0]
                except:
                    item['name'] = None
            if '<preview_link>' in c_raw_data:
                try:
                    item['previewLink'] = c_raw_data.split('<preview_link>')[-1].split('</preview_link>')[0]
                except:
                    item['previewLink'] = None

            if '<trackingLink>' in c_raw_data:
                try:
                    item['trackingLink'] = c_raw_data.split('<trackingLink>')[-1].split('</trackingLink>')[0]
                except:
                    item['trackingLink'] = None
            if '<advertiser_extended_terms>' in c_raw_data:
                try:
                    item['countryCode'] = c_raw_data.split('<advertiser_extended_terms>')[-1].split(
                        '</advertiser_extended_terms>')[0].split(': ')[1].split('\n')[0].replace('\r', '')
                except:
                    item['countryCode'] = None
                    continue
            if '<payout>' in c_raw_data:
                try:
                    item['payoutValue'] = c_raw_data.split('<payout>')[-1].split('</payout>')[0]
                except:
                    item['payoutValue'] = 0
            if '<vertical_name>' in c_raw_data:
                try:
                    item['category'] = c_raw_data.split('<vertical_name>')[-1].split('</vertical_name>')[0]
                except:
                    item['category'] = None
            item['carrier'] = None
            if '<description>' in c_raw_data:
                try:
                    item['detail'] = c_raw_data.split('<description>')[-1].split('<\description>')[0].replace('\n',
                                                                                                              ' ').replace(
                        '\r', ' ')
                except:
                    item['detail'] = None
                    # print ("ClickDealer worker", raw_data)
                    # root = ET.fromstring(raw_data)
                    # # print (root.getroot())
                    # print (root.find("offer_feed_response"))
                    # print (root.findall("offers"))
                    # for child in root:
                    #     print (child.tag, child.attrib)
                    # # print (root.tag)
                    # # print (root.findall('offers'))
                    # for offer in root.findall('offer'):
                    #     print ("打印offer")
                    #     print (offer)
                    # if 'code' in raw_data and raw_data['code'] == 0:
                    #     self.delete_old_offers()
                    #     offers = raw_data['campaigns']
                    # for item in offers:
                    #         for lp in item['lps']:
            offer_data = {}
            try:
                countryCode = Helper.fix_country(str(item.get('countryCode')))
            except Exception as e:
                countryCode = None
                key_code = {'key_code': item.get('countryCode')}
                ThirdPartyCountryCode.insert(key_code).execute()

            offer_data = {
                'sourcename': 'Clickdealer',
                'userId': self.userId,
                'taskId': self.taskId,
                'offerId': item.get('offerId'),
                'name': item.get('name'),
                'previewLink': item.get('previewLink'),
                'trackingLink': item.get('trackingLink'),
                'countryCode': countryCode,  # 这里需要转换country到三位
                'payoutValue': item.get('payoutValue'),
                'category': item.get('category'),
                'carrier': item.get('carrier'),
                'detail': item.get('detail'),
            }
            print(offer_data)
            try:
                ThirdPartyOffer.delete().where(ThirdPartyOffer.offerId == item.get('offerId')).execute()
                print(ThirdPartyOffer.insert(offer_data).execute())
            except:
                print("sdfsfsfsssf")
