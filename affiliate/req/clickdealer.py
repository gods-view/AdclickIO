import urllib

import requests

from affiliate.req.base_req import BaseReq


class ClickdealerReq(BaseReq):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_all_offer(self):
        params = {'api_key': self.password,
                  'affiliate_id': self.username,
                  'start_date': '01/01/2010+00:00:00',
                  'end_date': '07/01/2018+01:00:00',
                  'sub_affiliate': '',
                  'start_at_row': 1,
                  'row_limit': 0,
                  'sort_field': 'site_offer_id',
                  'sort_descending': 'FALSE',
                  'event_type': 'all',
                  'campaign_name': '',
                  'media_type_category_id': '',
                  'vertical_category_id': '',
                  'vertical_id': '',
                  'offer_status_id': '',
                  'tag_id': ''
                  }
        url = self.url + '?%s' % urllib.parse.urlencode(params, safe='/+:')
        response = requests.request("GET", url)
        self.log(url, '', response.text)
        return response.text
