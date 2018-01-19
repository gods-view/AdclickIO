import datetime
import json

import requests


class ExoClick():
    def __init__(self, api_token):
        self.api_token = api_token
        self.baseUrl = 'https://api.exoclick.com/v1'

        url = self.baseUrl + '/login'
        query = {
            'api_token': self.api_token,
        }
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        response = requests.request(
            "POST", url, data=json.dumps(query), headers=headers)
        resp = response.json()
        self.Authorization = resp['type'] + ' ' + resp['token']

    def campaign_list(self):
        url = "https://api.exoclick.com/v1/campaigns"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.Authorization,
        }
        query = {
            'limit': 10000,
            'count': True
        }
        response = requests.request("GET", url, headers=headers, params=query)

        return response.json()
        # return response.text

    def statistics(self, campaign_id, quick):
        url = self.baseUrl + "/statistics/advertiser/date"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.Authorization,
        }
        query = {
            'campaignid': campaign_id,
            'date-from': quick,
            'date-to': datetime.date.today(),
            'limit': 10000,
            'count': True,
        }
        response = requests.request("GET", url, headers=headers, params=query)

        return response.json()
        # return response.text


# if __name__ == '__main__':
#     quick = '2015-01-01'
#     # quick=datetime.date.today() + datetime.timedelta(days=-1)
#     api_token = "b76374416f5db01c5ddeeef59f2aa42756d3b58e"
#     exoclick = ExoClick(api_token)
#     # print(exoclick.campaign_list())
#     print(exoclick.statistics(1735635, quick))
