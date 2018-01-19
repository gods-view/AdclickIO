#!/usr/bin/env python
# encoding: utf-8
import json

from affiliate.common.helper import Helper
from affiliate.req.glispa import GlispaReq
from affiliate.model.mysql_model import ThirdPartyOffer, OfferSyncTask
from affiliate.worker.base_worker import BaseWorker


class GlispaWork(BaseWorker):
    def __init__(self, taskId=0, userId=12, url='', username='', password='', token=''):
        BaseWorker.__init__(self, taskId, userId, url, username, password, token=token)

    def start(self):
        print ("GlispaWork worker")
        glispa_req = GlispaReq(api_token=self.token)
        raw_data = glispa_req.get_all_offer()
        print (raw_data)
        if 'status' in raw_data:
            # for item, key in raw_data.items():
            #     print (key)
            offers = raw_data["data"]
            print (offers)
            for item in offers:
                # print (item["campaign_id"], item["name"], item["payout_amount"], item["category"])
                # for lp in item['lps']:
                offer_data = {
                    'sourcename': 'Glispa',
                    'userId': self.userId,
                    'taskId': self.taskId,
                    'offerId': item['campaign_id'],
                    'name': item['name'],
                    'previewLink': item['preload_click_url'],
                    # 'trackingLink': item['trackinglink'],
                    'countryCode': Helper.fix_country(item['countries']),  # 这里需要转换country到三位
                    'payoutValue': float(item['payout_amount']),
                    'category': item['category'],
                    'carrier': item['mobile_devices_included'],
                    'detail': json.dumps(item),
                }
                ThirdPartyOffer.delete().where(ThirdPartyOffer.offerId == item['campaign_id']).execute()
                ThirdPartyOffer.insert(offer_data).execute()
            print (offer_data)
        else:
            raise Exception('access glispa failed')


if __name__ == '__main__':
    glispa = GlispaWork(token="858acb10-f8ca-4126-9f63-05c51e517f5d")
    glispa.start()
