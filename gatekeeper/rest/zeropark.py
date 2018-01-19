import requests


class ZeroPark():
    def __init__(self, token):
        self.token = token
        self.baseUrl = 'https://panel.zeropark.com'

    def campaign_all(self, startDate, endDate):
        url = self.baseUrl + '/api/stats/campaign/all'
        headers = {
            'api-token': self.token,
        }
        query = {
            'interval': 'CUSTOM',
            'startDate': self.date_formet(startDate),
            'endDate': self.date_formet(endDate),
            'limit': 10000,
        }
        response = requests.request("GET", url, headers=headers, params=query)
        return response.json()

    # def campaign_details(self, campaignId, interval):
    #     url = self.baseUrl + '/api/stats/campaign/' + campaignId + '/details'
    #     headers = {
    #         'api-token': self.token,
    #     }
    #     query = {
    #         'interval': interval,
    #         'limit': 10000,
    #     }
    #     response = requests.request("GET", url, headers=headers, params=query)
    #     return response.text
    #     # return response.json()

    def date_formet(self, datetime):
        datetime = str(datetime)
        year = datetime[0:4]
        month = datetime[5:7]
        day = datetime[8:10]
        return str(day + '/' + month + '/' + year)


if __name__ == '__main__':
    apiKey = 'AAABWbbuJb0mnhLNrD4rT4v5pOlzyJGHSaNq8fqYFqamUf++gue16ZSprTR1qRuCkfX9i8wDueCp9TH7hERJ+Q=='
    zeropark = ZeroPark(apiKey)
    startDate = '2017-03-14'
    endDate = '2017-03-15'
    print(zeropark.campaign_all(startDate, endDate))
    # (note:return data no click,impression)


    # print(zeropark.date_formet(startDate))

    # interval='LAST_YEAR'
    # campaignId = 'c16deed0-b776-11e6-b586-0e855f2e0669'
    # print(zeropark.campaign_details(campaignId,interval))
