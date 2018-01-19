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

from affiliate.common.helper import Helper
from affiliate.req.avazu import AvazuReq
from affiliate.model.mysql_model import ThirdPartyOffer, OfferSyncTask
from affiliate.worker.base_worker import BaseWorker


class AvazuWork(BaseWorker):
    def __init__(self, taskId, userId, url, username, password):
        BaseWorker.__init__(self, taskId, userId, url, username, password)

    def start(self):
        print ("AvazuWork worker")
        avazu_req = AvazuReq(url=self.url, username=self.username, password=self.password)
        raw_data = avazu_req.get_all_offer()
        # print "AvazuWork worker",raw_data
        if 'code' in raw_data and raw_data['code'] == 0:
            self.delete_old_offers()
            offers = raw_data['campaigns']
            for item in offers:
                for lp in item['lps']:
                    offer_data = {
                        'sourcename': 'Avazu',
                        'userId': self.userId,
                        'taskId': self.taskId,
                        'offerId': item['cpnid'],
                        'name': item['cpnname'],
                        'previewLink': lp['previewlink'],
                        'trackingLink': lp['trackinglink'],
                        'countryCode': Helper.fix_country(str(lp['country'])),  # 这里需要转换country到三位
                        'payoutValue': float(lp['payout']),
                        'category': item['category'],
                        'carrier': item['carrier'],
                        'detail': json.dumps(item),
                    }
                    ThirdPartyOffer.delete().where(ThirdPartyOffer.offerId == item['cpnid']).execute()
                    # st = ThirdPartyOffer.get(offerId=item['cpnid'])
                    # st.delete_instance()
                    ThirdPartyOffer.insert(offer_data).execute()
        else:
            raise Exception('access avazu failed')
