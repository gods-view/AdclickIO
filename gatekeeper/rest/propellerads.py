import requests


class PropellerAds():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def campaign_list(self,startdate,enddate):
        url = 'http://report.propellerads.com/'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        querystring = {
            'action': 'getStats',
            'key': self.apiKey,
            'params[group_by]': 'campaign_id',
            'params[stat_columns][]': ['show', 'click', 'convers', 'convrate', 'cpm', 'ctr', 'profit'],
            # cost=(show/1000)*cpm
            'date_range': 'custom',
            'date_start': startdate,
            'date_end': enddate,
        }

        response = requests.request("POST", url, headers=headers, params=querystring)
        # return response.text
        return response.json()



# if __name__ == '__main__':
#     apiKey = 'c1517f8f1cb8cad17555addc2eb72227569323e2'
#     propellerads = PropellerAds(apiKey)
#     quick=datetime.date.today() + datetime.timedelta(days=-190)
#     print(propellerads.campaign_list(quick))