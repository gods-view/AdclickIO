#!/usr/bin/env python
# encoding: utf-8

import redis
import json
import datetime
from affiliate.model.config_redis import redisConf
r = redis.Redis(host=redisConf['host'], port=redisConf['port'])

class Redis():
    #获取统计list列表
    def getAdStatList(self,index,stop = 500000,start = 0): 
        key = "trk.data.list"
        if (int(index) > 0):
            key = "trk.data.list"+"_"+str(index)
        print ("getAdStatList",key)
        resList = r.lrange(key,start,stop)
        return resList

    #删除统计列表
    def delAdStatList(self,index,start, stop = -1):
        key = "trk.data.list"
        if (int(index) > 0):
            key = "trk.data.list"+"_"+str(index)
        print ("delAdStatList",key)
        return r.ltrim(key,start,stop)

    #获取具体值
    def getAdStatValue(self,key):
        names = ['VisitsFlag','ClicksFlag','ConversionsFlag','UserID','CampaignID','CampaignName','FlowID','FlowName','LanderID','LanderName','OfferID','OfferName','OfferUrl','OfferCountry','AffiliateNetworkID','AffilliateNetworkName','TrafficSourceID','TrafficSourceName','Language','Model','Country','City','Region','ISP','MobileCarrier','Domain','DeviceType','Brand','OS','OSVersion','Browser','BrowserVersion','ConnectionType','Timestamp','Visits','Clicks','Conversions','Cost','Revenue','Impressions','KeysMD5','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','tsCampaignId','tsWebsiteId','ip','PostbackTimestamp','VisitTimestamp','ExternalID','ClickID','TransactionID','ConnectionType','VisitorIP','VisitorReferrer','tsCampaignName']
        try:
            res = r.hmget(key,*names)
        except Exception as e:
            res = dict()
            return res

        dataList = dict()
        num = len(names)
        for index in range(num):
            dataList[str(names[index])] = ''
            if (res[index]):
                try:
               	    dataList[str(names[index])] = bytes.decode(res[index])
                except Exception as e:
                    dataList[str(names[index])] = res[index]
        return dataList

    #设置具体值
    def setAdStatValue(self,key,value):
        names = ['VisitsFlag','ClicksFlag','ConversionsFlag']
        num = len(names)
        dataList = dict()
        for index in range(num):
            dataList[str.encode(str(names[index]))] = str.encode(str(value[str(names[index])]))
        #print ("key,redis data",dataList,"===============key==================",key) 
        r.hmset(key,dataList)
        r.expire(key, 12 * 60 * 60)
        return dataList

