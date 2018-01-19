#!/usr/bin/env python
# encoding: utf-8
import logging
import peewee

from affiliate.common.helper import Helper
from affiliate.req.yeahmobi import YeahmobiReq
from affiliate.model.mysql_model import ThirdPartyOffer
from affiliate.worker.base_worker import BaseWorker


class YeahmobiWork(BaseWorker):
    def __init__(self, taskId, userId, url, username, password):
        BaseWorker.__init__(self, taskId, userId, url, username, password)

    def start(self):
        yeahmobi_req = YeahmobiReq(url=self.url, username=self.username, password=self.password)
        flag, pages, first_data = yeahmobi_req.get_pages()
        print (flag, pages)
        if flag == 'success':
            self.delete_old_offers()
            for i in range(pages):
                current_page = i + 1
                if current_page == 1:
                    offers = first_data
                else:
                    offers = yeahmobi_req.get_offer_by_page(current_page)
                    if offers['flag'] != 'success':
                        raise Exception('access yeahmobi failed')
                    offers = offers['data']['data']

                for k, v in dict(offers).items():
                    # print (v['countries'])
                    offer_data = {
                        'sourcename': 'Yeahmobi',
                        'userId': self.userId,
                        'taskId': self.taskId,
                        'offerId': k,
                        'name': v['name'],
                        'previewLink': v['preview_url'],
                        'trackingLink': v['tracklink'],
                        'countryCode': Helper.fix_country(v['countries']),  # 这里需要转换country到三位
                        'payoutValue': float(v['payout']),
                        'category': v['category'],
                        'carrier': v['carriers'],
                        'platform': v['platform'],
                        'detail': v,
                    }
                    ThirdPartyOffer.delete().where(ThirdPartyOffer.offerId == k).execute()
                    ThirdPartyOffer.insert(offer_data).execute()
        else:
            raise Exception('access yeahmobi failed')
            # pass
