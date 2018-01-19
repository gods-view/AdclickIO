import datetime

import requests


class Popads():
    def __init__(self, token):
        self.token = token

    def report_advertiser(self, quick):
        url = 'https://www.popads.net/api/report_advertiser'

        query = {
            "key": self.token,
            'groups': 'campaign,datetime:day',
            'zone': 'UTC',
            'quick': quick
        }

        response = requests.request("POST", url, params=query)
        return response.json()


# if __name__ == '__main__':
#     token = '5abaf88d3b905ec8226ee45b4a5d8e43cef466f9'
#     popads = Popads(token)
#     start = datetime.date.today() + datetime.timedelta(days=-1)
#     end = datetime.date.today()
#     print(popads.report_advertiser(start, end))
