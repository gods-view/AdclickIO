import requests


class TrafficJunky():
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.baseUrl = 'http://api.trafficjunky.com'

    def campaign_list(self):
        url = self.baseUrl + '/api/campaigns.json'
        querystring = {
            "api_key": self.apiKey,
        }
        response = requests.request("GET", url, params=querystring)
        return response.json()

    def campaigns_stats(self, campaign_id, startdate, enddate):
        url = self.baseUrl + '/api/campaigns/stats.json'
        querystring = {
            "api_key": self.apiKey,
            "timestamp": True,
            'startDate': self.date_formet(startdate),
            'endDate': self.date_formet(enddate),
            'campaignId': campaign_id,
        }
        response = requests.request("GET", url, params=querystring)
        return response.json()

    def date_formet(self, datetime):
        datetime = str(datetime)
        year = datetime[0:4]
        month = datetime[5:7]
        day = datetime[8:10]
        return str(day + '/' + month + '/' + year)


# if __name__ == '__main__':
#     campaign_id = 1001144791
#     apiKey = 'TJ5881c996e35cd2.62299992'
#     startdate = datetime.date.today() + datetime.timedelta(days=-1)
#     enddate = time.strftime(str(datetime.date.today()))
#     trafficjunky = TrafficJunky(apiKey)
#     # print(trafficjunky.campaign_list())
#     print(trafficjunky.campaigns_stats(1001144791, startdate, enddate))
