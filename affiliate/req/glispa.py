import requests


class GlispaReq(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def get_all_offer(self):
        url = 'http://feed.platform.glispa.com/native-feed/%s/app' % self.api_token
        print (url)
        header = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        query = {
            'sourceid': self.api_token,
        }
        response = requests.request("GET", url, params=query)
        print (response, response.content)
        if response:
            return response.json()
        else:
            print ("error")
            return ''
            # return response.json()


if __name__ == '__main__':
    api_token = '858acb10-f8ca-4126-9f63-05c51e517f5d'  # dsp
    # api_token = 'OYSm6izb3i5w0Ll84K2g'
    glispa = GlispaReq(api_token)
    print(glispa.get_all_offer())
