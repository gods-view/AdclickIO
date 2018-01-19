from affiliate.common.helper import Helper
from affiliate.model.mysql_model import ThirdPartyOffer
from affiliate.worker.base_worker import BaseWorker
from dsp.module.mgid import Mgid


class YeahmobiWork(BaseWorker):
    def __init__(self, taskId, userId, url, username, password):
        BaseWorker.__init__(taskId, userId, url, username, password)

    def start(self):
        yeahmobi_req = Mgid()
        flag, pages, first_data = yeahmobi_req.get_pages()
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
                    offer_data = {
                        'userId': self.userId,
                        'taskId': self.taskId,
                        'offerId': k,
                        'name': v['name'],
                        'previewLink': v['preview_url'],
                        'trackingLink': v['tracklink'],
                        'countryCode': Helper.fix_country(str(v['countries'])),  # 这里需要转换country到三位
                        'payoutValue': float(v['payout']),
                        'category': v['category'],
                        'carrier': v['carriers'],
                        'platform': v['platform'],
                        'detail': v,
                    }
                    ThirdPartyOffer.insert(offer_data).execute()
        else:
            raise Exception('access yeahmobi failed')
