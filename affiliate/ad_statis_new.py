#!/usr/bin/env python
# encoding: utf-8

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import time
import traceback
from affiliate.model.mysql_model import *
from affiliate.model.mysql_report import *
from affiliate.model.redis_model import *

class AdStatis():
    def __init__(self,index):
        self.RedisClass = Redis()
        self.index = index

    def doAdStatis(self):
        print ("adStatis")
        while (True):
            #try:
            self.adStatis()
            #except Exception as e:
                #pass


    #统计信息
    def adStatis(self):    
        res = self.RedisClass.getAdStatList(self.index)
        if (res == False or len(res) <= 0):
            return False
        
        statisNum = len(res)

        #分库
        num = 10
        usersList = dict()
        md5Key = dict()
        valueList = dict()
        for i in range(num):
            usersList[i] = dict()
            valueList[i] = dict()
            md5Key[i] = []

        userIdText = []
        clickIds = []
        tmpList = dict()
        Conversions = dict()

        CampaignIds = []
        FlowIds = []
        OfferIds = []
        LanderIds = []
        CountryIds = []
        TrafficSourceIds = []
        AffiliateNetworkIds = []

        CampaignMapList = dict()
        for data in res:
            key = bytes.decode(data) 
            redisData = self.RedisClass.getAdStatValue(key)
            if (isinstance(redisData['UserID'], (str))):
                continue
            userIdValue = bytes.decode(redisData['UserID'])
            userIdText.append(str(userIdValue))
            tmpList[key] = redisData
            if(len(str(redisData['Conversions'])) > 0 and int(redisData['Conversions']) > 0):
                clickId = redisData['ClickID']
                clickIds.append(clickId)
                Conversions[clickId] = redisData

            if(len(str(redisData['CampaignID'])) > 0 and int(redisData['CampaignID']) > 0):
                CampaignIds.append(int(redisData['CampaignID']))
                tsCampaignId = 0;
                print (redisData['tsCampaignId'])
                #测试代码
                try:
                    tsCampaignId = 0
                    if (len(redisData['tsCampaignId']) > 0):
                        tsCampaignId = bytes.decode(redisData['tsCampaignId'])                    
                        tsCampaignId = int(tsCampaignId)
                except Exception as e:
                    tsCampaignId = 0
                #tsCampaignId = 11
                if (tsCampaignId > 0):
                    CampaignMapList[int(redisData['CampaignID'])] = tsCampaignId
            if(len(str(redisData['FlowID'])) > 0 and int(redisData['FlowID']) > 0):
                FlowIds.append(int(redisData['FlowID']))

            if(len(str(redisData['LanderID'])) > 0 and int(redisData['LanderID']) > 0):
                LanderIds.append(int(redisData['LanderID']))

            if(len(str(redisData['OfferID'])) > 0 and int(redisData['OfferID']) > 0):
                OfferIds.append(int(redisData['OfferID']))

            if(len(str(redisData['TrafficSourceID'])) > 0 and int(redisData['TrafficSourceID']) > 0):
                TrafficSourceIds.append(int(redisData['TrafficSourceID']))

            if(len(str(redisData['AffiliateNetworkID'])) > 0 and int(redisData['AffiliateNetworkID']) > 0):
                AffiliateNetworkIds.append(int(redisData['AffiliateNetworkID']))

            if(len(str(redisData['Country'])) > 0):
                CountryIds.append(redisData['Country'])

        TrackingCampaignList = dict()
        if (len(CampaignIds) > 0):
            data = TrackingCampaign.select().where(TrackingCampaign.id << CampaignIds)
            for value in data:
                TrackingCampaignList[value.id] = value
        
        FlowList = dict()
        if (len(FlowIds) > 0):
            data = Flow.select().where(Flow.id << FlowIds)
            for value in data:
                FlowList[value.id] = value

        LanderList = dict()
        if (len(LanderIds) > 0):
            data = Lander.select().where(Lander.id << LanderIds)
            for value in data:
                LanderList[value.id] = value            

        OfferList = dict()
        if (len(OfferIds) > 0):
            data = Offer.select().where(Offer.id << OfferIds)
            for value in data:
                OfferList[value.id] = value    

        TrafficSourceList = dict()
        if (len(TrafficSourceIds) > 0):
            data = TrafficSource.select().where(TrafficSource.id << TrafficSourceIds)
            for value in data:
                TrafficSourceList[value.id] = value

        AffiliateNetworkList = dict()
        if (len(AffiliateNetworkIds) > 0):
            data = AffiliateNetwork.select().where(AffiliateNetwork.id << AffiliateNetworkIds)
            for value in data:
                AffiliateNetworkList[value.id] = value

        CountryList = dict()
        if (len(CountryIds) > 0):
            data = Country.select().where(Country.name << CountryIds)
            for value in data:
                CountryList[value.name] = value
        #print (CampaignIds,FlowIds,LanderIds,OfferIds,CountryIds)
        #print (TrackingCampaignList,FlowList,LanderList,OfferList,TrafficSourceList,AffiliateNetworkList,CountryList)
        #sys.exit()
        print("CampaignMap",CampaignMapList)
        if (len(CampaignMapList) > 0):
            insertData = []
            for key,data in CampaignMapList.items():
                value = {'OurCampId':key,\
                         'TheirCampId':data
                         }
                #print ("=======================",value)
                #CampaignMap.insert(**value).upsert(upsert=True).execute()
                insertData.append(value)
            res = CampaignMap.insert_many(insertData).upsert(upsert=True).execute()
        
        #print ("userIdText",userIdText)
        #查找用户信息
        userKeyList = dict()
        userIds = []
        resUsers = User.select().where(User.idText << userIdText)
        if(resUsers):
            for user in resUsers:
               #idText = bytes.decode(idText)
               userKeyList[user.idText] = dict()
               userKeyList[user.idText]['id'] = user.id
               userIds.append(user.id)

            #增加totalEvents
            #bonus=(Employee.bonus + (Employee.salary * .1))
            res = UserBilling.update(totalEvents=UserBilling.totalEvents + 1,billedEvents = UserBilling.billedEvents +1).where(UserBilling.expired == 0,UserBilling.userId << userIds).execute()
        #保存转化成功数据
        if (len(clickIds) > 0):
            self.saveAdConversionsStatis(clickIds,Conversions,userKeyList,TrackingCampaignList,FlowList,LanderList,OfferList,TrafficSourceList,AffiliateNetworkList,CountryList)
        
        #print ("-------------")
        #sys.exit()
        #拆分数据
        for key,data in tmpList.items():
            idText = bytes.decode(data['UserID'])
            #print ("idText",idText)
            userId = userKeyList[idText]['id']
            #print ("userId:",userId)
            modUserId = int(userId)%10
            usersList[modUserId][idText] = dict()
            usersList[modUserId][idText]['id'] = userId
            valueList[modUserId][key] = dict()
            valueList[modUserId][key] = data
            md5Key[modUserId].append(key)
        
        #print ("usersList",usersList)
        if (reportDb.is_closed()):
            reportDb.connect()
        for i in range(num):
            #print (len(valueList[i]))
            #print ("value",valueList[i],"userList",usersList[i],"md5key",md5Key[i])
            if (valueList[i]):
                self.save(eval("AdStatisLog"+str(i)),valueList[i],usersList[i],md5Key[i])
        reportDb.close()
        #清除数据
        self.RedisClass.delAdStatList(self.index,statisNum)
        return True

    #保存转换率
    def saveAdConversionsStatis(self,clickIds,Conversions,userKeyList,TrackingCampaignList,FlowList,LanderList,OfferList,TrafficSourceList,AffiliateNetworkList,CountryList):
        #clickIdsData = AdConversionsStatis.select().where(AdConversionsStatis.ClickID << clickIds)
        #clickIdsList = dict()
        #if (clickIdsData):
        #    for data in clickIdsData:
        #        clickIdsList[data.ClickID] = dict()
        #        clickIdsList[data.ClickID]['ClickID'] = data.ClickID
        #更新数据
        insertData = []
        for ClickID,data in Conversions.items():
            idText = bytes.decode(data['UserID'])
            UserID = userKeyList[idText]['id']
            CampaignName = ''
            if ('CampaignID' in data and len(str(data['CampaignID'])) > 0 and int(data['CampaignID']) in TrackingCampaignList):
                CampaignName = TrackingCampaignList[int(data['CampaignID'])].name

            FlowName = ''
            if ('FlowID' in data and len(str(data['FlowID'])) > 0 and int(data['FlowID']) in FlowList):
                FlowName = FlowList[int(data['FlowID'])].name

            LanderName = ''
            if ('LanderID' in data and len(str(data['LanderID'])) > 0 and int(data['LanderID']) in LanderList):
                LanderName = LanderList[int(data['LanderID'])].name

            OfferName = ''
            if ('OfferID' in data and len(str(data['OfferID'])) > 0 and int(data['OfferID']) in OfferList):
                OfferName = OfferList[int(data['OfferID'])].name

            TrafficSourceName = ''
            if ('TrafficSourceID' in data and len(str(data['TrafficSourceID'])) > 0 and int(data['TrafficSourceID']) in TrafficSourceList):
                TrafficSourceName = TrafficSourceList[int(data['TrafficSourceID'])].name

            AffiliateNetworkName = ''
            if ('AffiliateNetworkID' in data and len(str(data['AffiliateNetworkID'])) > 0 and int(data['AffiliateNetworkID']) in AffiliateNetworkList):
                AffiliateNetworkName = AffiliateNetworkList[int(data['AffiliateNetworkID'])].name

            CountryCode = ''
            if ('Country' in data and len(str(data['Country'])) > 0 and  str(bytes.decode(data['Country'])) in CountryList):
                CountryCode = CountryList[str(bytes.decode(data['Country']))].alpha3Code
            
            #print ("CampaignName",CampaignName,"FlowName",FlowName,"LanderName",LanderName,"OfferName",OfferName,"TrafficSourceName",TrafficSourceName,"AffiliateNetworkName",AffiliateNetworkName)
            #sys.exit()
            value = {'UserID':UserID,\
                    'PostbackTimestamp':data['PostbackTimestamp'],\
                    'VisitTimestamp':data['VisitTimestamp'],\
                    'ExternalID': data['ExternalID'],\
                    'ClickID':data['ClickID'],\
                    'TransactionID':data['TransactionID'],\
                    'Revenue':data['Revenue'],\
                    'Cost':data['Cost'],\
                    'CampaignName':CampaignName,\
                    'CampaignID':data['CampaignID'],\
                    'LanderName':LanderName,\
                    'LanderID':data['LanderID'],\
                    'OfferName':OfferName,\
                    'OfferID':data['OfferID'],\
                    'Country':data['Country'],\
                    'CountryCode':CountryCode,\
                    'TrafficSourceName':TrafficSourceName,\
                    'TrafficSourceID':data['TrafficSourceID'],\
                    'AffiliateNetworkName':AffiliateNetworkName,\
                    'AffiliateNetworkID':data['AffiliateNetworkID'],\
                    'Device':data['DeviceType'],\
                    'OS':data['OS'],\
                    'OSVersion':data['OSVersion'],\
                    'Brand':data['Brand'],\
                    'Model':data['Model'],\
                    'Browser':data['Browser'],\
                    'BrowserVersion':data['BrowserVersion'],\
                    'ISP':data['ISP'],\
                    'MobileCarrier':data['MobileCarrier'],\
                    'ConnectionType': data['ConnectionType'],\
                    'VisitorIP':data['VisitorIP'],\
                    'VisitorReferrer':data['VisitorReferrer'],\
                    'V1':data['V1'],\
                    'V2':data['V2'],\
                    'V3':data['V3'],\
                    'V4':data['V4'],\
                    'V5':data['V5'],\
                    'V6':data['V6'],\
                    'V7':data['V7'],\
                    'V8':data['V8'],\
                    'V9':data['V9'],\
                    'V10':data['V10']
                }
            insertData.append(value)

        if (len(insertData) > 0):
            res = AdConversionsStatis.insert_many(insertData).execute()

        return True    

    #执行保存
    def save(self,AdStatisLog,valueList,usersList,md5Key):
        #print("md5Key",md5Key[0])
        #查找数据库中已存在的数据
        #resAdStat = AdStatisLog.select().where(AdStatisLog.KeysMD5 << md5Key)
        #print ("resAdStat=======",resAdStat)
        resAdStatList = dict()
        #if (resAdStat):
        #    for data in resAdStat:
        #        resAdStatList[data.KeysMD5] = dict()
        #        resAdStatList[data.KeysMD5]['KeysMD5'] = data.KeysMD5

        #更新数据
        insertData = []
        for md5Key,data in valueList.items():
            UserID = 0
            #print (data['UserID'])
            UserIDText = bytes.decode(data['UserID'])
            #print(UserIDText)
            if UserIDText in usersList:
                UserID = usersList[UserIDText]['id']

            cost = 0
            if (data['Cost']):
                cost = int(float(data['Cost'])*1000000)

            Revenue = 0
            if (data['Revenue']):
                Revenue = int(float(data['Revenue']))

            #Conversions
            if (data['Conversions'] and int(data['Conversions']) >= 1):
                cost = 0
                data['Visits'] = 0
                data['Clicks'] = 0
                data['Impressions'] = 0
            elif (data['Clicks'] and int(data['Clicks']) >= 1):
                cost = 0
                data['Visits'] = 0
                data['Revenue'] = 0
                data['Impressions'] = 0

            value = {'UserID':UserID,\
                        'CampaignID':data['CampaignID'],\
                        'CampaignName':data['CampaignName'],\
                        'FlowID':data['FlowID'],\
                        'FlowName':data['FlowName'],\
                        'LanderID':data['LanderID'],\
                        'LanderName':data['LanderName'],\
                        'OfferID':data['OfferID'],\
                        'OfferName':data['OfferName'],\
                        'OfferUrl':data['OfferUrl'],\
                        'OfferCountry':data['OfferCountry'],\
                        'AffiliateNetworkID':data['AffiliateNetworkID'],\
                        'AffilliateNetworkName':data['AffilliateNetworkName'],\
                        'TrafficSourceID':data['TrafficSourceID'],\
                        'TrafficSourceName':data['TrafficSourceName'],\
                        'Language':data['Language'],\
                        'Model':data['Model'],\
                        'Country':data['Country'],\
                        'City':data['City'],\
                        'Region':data['Region'],\
                        'ISP':data['ISP'],\
                        'MobileCarrier':data['MobileCarrier'],\
                        'Domain':data['Domain'],\
                        'DeviceType':data['DeviceType'],\
                        'Brand':data['Brand'],\
                        'OS':data['OS'],\
                        'OSVersion':data['OSVersion'],\
                        'Browser':data['Browser'],\
                        'BrowserVersion':data['BrowserVersion'],\
                        'ConnectionType':data['ConnectionType'],\
                        'Timestamp':data['Timestamp'],\
                        'Visits':data['Visits'],\
                        'Clicks':data['Clicks'],\
                        'Conversions':data['Conversions'],\
                        'Cost':cost,\
                        'Revenue':Revenue,\
                        'Impressions':data['Impressions'],\
                        'KeysMD5':md5Key,\
                        'Ip':data['VisitorIP'],\
                        'V1':data['V1'],\
                        'V2':data['V2'],\
                        'V3':data['V3'],\
                        'V4':data['V4'],\
                        'V5':data['V5'],\
                        'V6':data['V6'],\
                        'V7':data['V7'],\
                        'V8':data['V8'],\
                        'V9':data['V9'],\
                        'V10':data['V10'],\
                        'tsCampaignId':data['tsCampaignId'],\
                        'tsWebsiteId':data['tsWebsiteId'],\
                        }
            insertData.append(value)

            '''
            if ( md5Key in resAdStatList):
                print ("need update",md5Key)
                AdStatisLog.update(
                        UserID=UserID,\
                        CampaignID=data['CampaignID'],\
                        CampaignName=data['CampaignName'],\
                        FlowID=data['FlowID'],\
                        FlowName=data['FlowName'],\
                        LanderID=data['LanderID'],\
                        LanderName=data['LanderName'],\
                        OfferID=data['OfferID'],\
                        OfferName=data['OfferName'],\
                        OfferUrl=data['OfferUrl'],\
                        OfferCountry=data['OfferCountry'],\
                        AffiliateNetworkID=data['AffiliateNetworkID'],\
                        AffilliateNetworkName=data['AffilliateNetworkName'],\
                        TrafficSourceID=data['TrafficSourceID'],\
                        TrafficSourceName=data['TrafficSourceName'],\
                        Language=data['Language'],\
                        Model=data['Model'],\
                        Country=data['Country'],\
                        City=data['City'],\
                        Region=data['Region'],\
                        ISP=data['ISP'],\
                        MobileCarrier=data['MobileCarrier'],\
                        Domain=data['Domain'],\
                        DeviceType=data['DeviceType'],\
                        Brand=data['Brand'],\
                        OS=data['OS'],\
                        OSVersion=data['OSVersion'],\
                        Browser=data['Browser'],\
                        BrowserVersion=data['BrowserVersion'],\
                        ConnectionType=data['ConnectionType'],\
                        Timestamp=data['Timestamp'],\
                        Visits=data['Visits'],\
                        Clicks=data['Clicks'],\
                        Conversions=data['Conversions'],\
                        Cost=cost,\
                        Revenue=Revenue,\
                        Impressions=data['Impressions'],\
                        KeysMD5=md5Key,\
                        Ip=data['VisitorIP'],\
                        V1=data['V1'],\
                        V2=data['V2'],\
                        V3=data['V3'],\
                        V4=data['V4'],\
                        V5=data['V5'],\
                        V6=data['V6'],\
                        V7=data['V7'],\
                        V8=data['V8'],\
                        V9=data['V9'],\
                        V10=data['V10'],\
                        tsCampaignId=data['tsCampaignId'],\
                        tsWebsiteId=data['tsWebsiteId']\
                    ).where(AdStatisLog.KeysMD5 == md5Key).execute()
            else:
                print ("need insert",md5Key)
                value = {'UserID':UserID,\
                        'CampaignID':data['CampaignID'],\
                        'CampaignName':data['CampaignName'],\
                        'FlowID':data['FlowID'],\
                        'FlowName':data['FlowName'],\
                        'LanderID':data['LanderID'],\
                        'LanderName':data['LanderName'],\
                        'OfferID':data['OfferID'],\
                        'OfferName':data['OfferName'],\
                        'OfferUrl':data['OfferUrl'],\
                        'OfferCountry':data['OfferCountry'],\
                        'AffiliateNetworkID':data['AffiliateNetworkID'],\
                        'AffilliateNetworkName':data['AffilliateNetworkName'],\
                        'TrafficSourceID':data['TrafficSourceID'],\
                        'TrafficSourceName':data['TrafficSourceName'],\
                        'Language':data['Language'],\
                        'Model':data['Model'],\
                        'Country':data['Country'],\
                        'City':data['City'],\
                        'Region':data['Region'],\
                        'ISP':data['ISP'],\
                        'MobileCarrier':data['MobileCarrier'],\
                        'Domain':data['Domain'],\
                        'DeviceType':data['DeviceType'],\
                        'Brand':data['Brand'],\
                        'OS':data['OS'],\
                        'OSVersion':data['OSVersion'],\
                        'Browser':data['Browser'],\
                        'BrowserVersion':data['BrowserVersion'],\
                        'ConnectionType':data['ConnectionType'],\
                        'Timestamp':data['Timestamp'],\
                        'Visits':data['Visits'],\
                        'Clicks':data['Clicks'],\
                        'Conversions':data['Conversions'],\
                        'Cost':cost,\
                        'Revenue':Revenue,\
                        'Impressions':data['Impressions'],\
                        'KeysMD5':md5Key,\
                        'Ip':data['VisitorIP'],\
                        'V1':data['V1'],\
                        'V2':data['V2'],\
                        'V3':data['V3'],\
                        'V4':data['V4'],\
                        'V5':data['V5'],\
                        'V6':data['V6'],\
                        'V7':data['V7'],\
                        'V8':data['V8'],\
                        'V9':data['V9'],\
                        'V10':data['V10'],\
                        'tsCampaignId':data['tsCampaignId'],\
                        'tsWebsiteId':data['tsWebsiteId'],\
                        }
                insertData.append(value)
            '''
        if (len(insertData) > 0):            
            AdStatisLog.insert_many(insertData).execute()

        return True
    
def main(index):    
    AdStatisClass = AdStatis(index)           
    AdStatisClass.doAdStatis()    

if __name__ == '__main__':
    index = sys.argv[1]
    try: 
        main(index)
    except Exception as e:
        #重启
        file_object = open('adStat_redis.log', 'a')
        print (traceback.print_exc())
        time = datetime.datetime.now()
        file_object.write("error time:"+str(time.strftime('%Y-%m-%d %H:%M:%S')))
        #file_object.write(traceback.print_exc())
        file_object.write("\n")
        file_object.close()
        main(index)


    
    
