#!/usr/bin/env python
# encoding: utf-8

import os,time
import subprocess
import sys,copy
import gevent
from gevent.event import Event
import gc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import time
import traceback
from affiliate.model.config import mysql, mysql_report
from affiliate.model.mysql_model import *
from affiliate.model.mysql_report import *
from affiliate.model.redis_model import *


class AdStatis():
    def __init__(self,index):
        self.RedisClass = Redis()
        self.index = index
        self.adStatisList = dict()

    def doAdStatis(self):
        print ("adStatis")
        while (True):
            #try:
            self.adStatisList = dict()
            self.adStatis()
            #sys.exit()
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
            valueList[i] = []
            md5Key[i] = []

        userIdText = []
        clickIds = []
        resAdStat = []
        CampaignIds = []
        FlowIds = []
        OfferIds = []
        LanderIds = []
        CountryIds = []
        TrafficSourceIds = []
        AffiliateNetworkIds = []

        getOfferIdsByFlow = []

        userEventNum = dict()
        Conversions = dict()

        CampaignMapList = dict()
        for data in res:
            key = bytes.decode(data)
            redisData = self.RedisClass.getAdStatValue(key)
            #print ("redisData",redisData)
            if (isinstance(redisData['UserID'], (str,int)) == False or len(str(redisData['UserID'])) <= 0):
                print ("error",redisData['UserID'])
                continue
            userIdValue = redisData['UserID']
            userIdText.append(str(userIdValue))

            #统计次数
            if (userIdValue not in userEventNum):
                userEventNum[userIdValue] = 0
            userEventNum[userIdValue] += 1

            redisData['KeysMD5'] = key
            print ("success",redisData['UserID'],key)
            self.adStatisList[key] = redisData
            resAdStat.append(redisData)
            #if (redisData['Conversions']):
                #print ("data======",redisData['Conversions'])
            #tmpList[key] = redisData
            if(len(str(redisData['Conversions'])) > 0 and int(redisData['Conversions']) > 0):
                clickId = redisData['ClickID']
                clickIds.append(clickId)
                Conversions[clickId] = redisData
                print ("Conversions success",key,clickId)

            if(len(str(redisData['CampaignID'])) > 0 and int(redisData['CampaignID']) > 0):
                CampaignIds.append(int(redisData['CampaignID']))
                tsCampaignId = redisData['tsCampaignId']
                tsCampaignName = redisData['tsCampaignName']
                if (int(redisData['CampaignID']) not in CampaignMapList):
                    CampaignMapList[int(redisData['CampaignID'])] = dict()
                    CampaignMapList[int(redisData['CampaignID'])]['id'] = ''
                    CampaignMapList[int(redisData['CampaignID'])]['name'] = ''

                if (len(str(tsCampaignId)) > 0):
                    CampaignMapList[int(redisData['CampaignID'])]['id'] = tsCampaignId

                if (len(str(tsCampaignName)) > 0):
                    CampaignMapList[int(redisData['CampaignID'])]['name'] = tsCampaignName

            if(len(str(redisData['FlowID'])) > 0 and int(redisData['FlowID']) > 0):
                FlowIds.append(int(redisData['FlowID']))

            if(len(str(redisData['LanderID'])) > 0 and int(redisData['LanderID']) > 0):
                LanderIds.append(int(redisData['LanderID']))

            if(len(str(redisData['OfferID'])) > 0 and int(redisData['OfferID']) > 0):
                OfferIds.append(int(redisData['OfferID']))
            else:
                #OfferIds为空的时候，需要根据flow的配比设置offerId
                getOfferIdsByFlow.append(int(redisData['FlowID']))

            if(len(str(redisData['TrafficSourceID'])) > 0 and int(redisData['TrafficSourceID']) > 0):
                TrafficSourceIds.append(int(redisData['TrafficSourceID']))

            if(len(str(redisData['AffiliateNetworkID'])) > 0 and int(redisData['AffiliateNetworkID']) > 0):
                AffiliateNetworkIds.append(int(redisData['AffiliateNetworkID']))

            if(len(str(redisData['Country'])) > 0):
                CountryIds.append(redisData['Country'])

        #处理offerId为空的(nodejs搬过来的)
        if (len(getOfferIdsByFlow) > 0):
            sql = "SELECT  f.`id` AS flowId,p.`id` AS parentId, l.`id`,l.`name`,p2.`weight` ,f.`userId`\
                FROM Flow f \
                INNER JOIN `Rule2Flow` f2 ON f2.`flowId` = f.`id`\
                INNER JOIN `Rule` r ON r.`id` = f2.`ruleId` \
                INNER JOIN `Path2Rule` r2 ON r2.`ruleId`= r.`id`\
                INNER JOIN `Path` p ON p.`id` = r2.`pathId`\
                INNER JOIN `Offer2Path` p2 ON p2.`pathId` = p.`id` \
                INNER JOIN `Offer` l ON l.`id`= p2.`offerId`\
                WHERE  f2.`deleted`= 0 AND r.`deleted` = 0 \
                AND r2.`deleted`= 0 AND p.`deleted` = 0  \
                AND p2.`deleted` = 0 AND l.`deleted` = 0 \
                AND f.`id` in (%s) AND p2.`weight` > 0 ORDER BY p2.`order` ASC" %(','.join(getOfferIdsByFlow))

            print ("sql----------",sql)
            getOfferIdsList = TrackingCampaign.execute_sql(sql)
            print("getOfferIdsList:",getOfferIdsList)

        sys.exit()
        '''
        SELECT  f.`id` AS flowId,p.`id` AS parentId, l.`id`,l.`name`,p2.`weight` ,f.`userId`
        FROM Flow f 
        INNER JOIN `Rule2Flow` f2 ON f2.`flowId` = f.`id`
        INNER JOIN `Rule` r ON r.`id` = f2.`ruleId` 
        INNER JOIN `Path2Rule` r2 ON r2.`ruleId`= r.`id`
        INNER JOIN `Path` p ON p.`id` = r2.`pathId`
        INNER JOIN `Offer2Path` p2 ON p2.`pathId` = p.`id` 
        INNER JOIN `Offer` l ON l.`id`= p2.`offerId`
        WHERE  f2.`deleted`= 0 AND r.`deleted` = 0 
        AND r2.`deleted`= 0 AND p.`deleted` = 0  
        AND p2.`deleted` = 0 AND l.`deleted` = 0 
        AND f.`id` = 1180 AND f.`userId`= 14 AND p2.`weight` > 0 ORDER BY p2.`order` ASC;

        根据offer取AffiliateNetworkId
        '''

        TrackingCampaignList = dict()
        if (len(CampaignIds) > 0):
            CampaignIds =  list(set(CampaignIds))
            data = TrackingCampaign.select().where(TrackingCampaign.id << CampaignIds)
            #print ("TrackingCampaign data",data,"CampaignIds:",CampaignIds,"list",CampaignMapList)
            for value in data:
                if (int(value.id) not in CampaignMapList.keys()):
                    print("CampaignMapList id error",value.id,"keys:",CampaignMapList.keys(),"list:",CampaignMapList,"ids:",CampaignIds)
                    continue
                TrackingCampaignList[value.id] = value
                
                #更新TrackingCampaign 表 tsCampaignName 字段
                TheirCampNameList = []
                TheirCampName = CampaignMapList[value.id]['name']
                if (value.TheirCampName):
                    TheirCampNameList = value.TheirCampName.split(",")

                if (len(str(TheirCampName)) > 0 and TheirCampName not in TheirCampNameList):
                    TheirCampNameList.append(TheirCampName)

                    updateTsCampaignName = ','.join(TheirCampNameList)
                    res = TrackingCampaign.update(TheirCampName = updateTsCampaignName).where(TrackingCampaign.id == value.id).execute() 
                else:
                   print("update id error:",value.id,"TheirCampName:",TheirCampName,"TheirCampNameList:",TheirCampNameList)
        #print("CampaignIds",CampaignIds)
        #sys.exit()
        FlowList = dict()
        if (len(FlowIds) > 0):
            FlowIds =  list(set(FlowIds))
            data = Flow.select().where(Flow.id << FlowIds)
            for value in data:
                FlowList[value.id] = value

        LanderList = dict()
        if (len(LanderIds) > 0):
            LanderIds =  list(set(LanderIds))
            data = Lander.select().where(Lander.id << LanderIds)
            for value in data:
                LanderList[value.id] = value            

        OfferList = dict()
        if (len(OfferIds) > 0):
            OfferIds =  list(set(OfferIds))
            data = Offer.select().where(Offer.id << OfferIds)
            for value in data:
                OfferList[value.id] = value    

        TrafficSourceList = dict()
        if (len(TrafficSourceIds) > 0):
            TrafficSourceIds =  list(set(TrafficSourceIds))
            data = TrafficSource.select().where(TrafficSource.id << TrafficSourceIds)
            for value in data:
                TrafficSourceList[value.id] = value

        AffiliateNetworkList = dict()
        if (len(AffiliateNetworkIds) > 0):
            AffiliateNetworkIds =  list(set(AffiliateNetworkIds))
            data = AffiliateNetwork.select().where(AffiliateNetwork.id << AffiliateNetworkIds)
            for value in data:
                AffiliateNetworkList[value.id] = value

        CountryList = dict()
        if (len(CountryIds) > 0):
            CountryIds =  list(set(CountryIds))
            data = Country.select().where(Country.name << CountryIds)
            for value in data:
                CountryList[value.name] = value

        if (len(CampaignMapList) > 0):
            insertData = []
            for key,data in CampaignMapList.items():
                if (len(str(data['id'])) > 0):
                    value = {'OurCampId':key,\
                             'TheirCampId':data['id']
                             }
                    #print ("CampaignMapList =======================",value)
                    insertData.append(value)
            res = CampaignMap.insert_many(insertData).upsert(upsert=True).execute()
        
        #print ("userIdText",userIdText)
        #查找用户信息
        userKeyList = dict()
        userIdText =  list(set(userIdText))
        resUsers = User.select().where(User.idText << userIdText)
        if(resUsers):
            userIds = []
            for user in resUsers:
               #idText = bytes.decode(idText)
               userKeyList[user.idText] = dict()
               userKeyList[user.idText]['id'] = user.id
               userIds.append(user.id)

               eventNum = userEventNum[user.idText]
               #增加totalEvents,billedEvents
               res = UserBilling.update(totalEvents=UserBilling.totalEvents + eventNum,billedEvents = UserBilling.billedEvents + eventNum).where(UserBilling.expired == 0,UserBilling.userId == user.id).execute()
            
        #保存转化成功数据
        #print ("clickIds",clickIds)
        if (len(clickIds) > 0):
            self.saveAdConversionsStatis(clickIds,Conversions,userKeyList,TrackingCampaignList,FlowList,LanderList,OfferList,TrafficSourceList,AffiliateNetworkList,CountryList)
        
        #print ("-------------")
        #sys.exit()
        #拆分数据
        for index in range(len(resAdStat)):
            idText = resAdStat[index]['UserID']
            #print ("idText",idText)
            userId = userKeyList[idText]['id']
            print ("userId:",userId)
            modUserId = int(userId)%10
            usersList[modUserId][idText] = dict()
            usersList[modUserId][idText]['id'] = userId
            #offer为空的根据比例给一个
            valueList[modUserId].append(resAdStat[index])
            md5Key[modUserId].append(key)
        
        #print ("usersList",usersList)
        geventList = []
        for i in range(num):            
            geventList.append(gevent.spawn(self.save,"adstatis_new_"+str(i),valueList[i],usersList[i],md5Key[i],OfferList))
            #print (len(valueList[i]))
            #print ("value",valueList[i],"userList",usersList[i],"md5key",md5Key[i])
            #if (valueList[i] and len(valueList[i]) > 0):
            #    res = self.save("adstatis_new_"+str(i),valueList[i],usersList[i],md5Key[i],OfferList)
        #sys.exit()
        gevent.joinall(geventList)
        #清除数据
        self.RedisClass.delAdStatList(self.index,statisNum)
        return True

    #保存转换率
    def saveAdConversionsStatis(self,clickIds,Conversions,userKeyList,TrackingCampaignList,FlowList,LanderList,OfferList,TrafficSourceList,AffiliateNetworkList,CountryList):
        print ("saveAdConversionsStatis")
        clickIdsData = AdConversionsStatis.select().where(AdConversionsStatis.ClickID << clickIds)
        clickIdsList = dict()
        if (clickIdsData):
            for data in clickIdsData:
                clickIdsList[data.ClickID] = dict()
                clickIdsList[data.ClickID]['ClickID'] = data.ClickID

        #更新数据
        insertData = []
        for ClickID,data in Conversions.items():
            if (ClickID in clickIdsList.keys()):
                continue

            idText = data['UserID']
            UserID = userKeyList[idText]['id']
            CampaignName = ''
            if ('CampaignID' in data.keys() and len(str(data['CampaignID'])) > 0 and int(data['CampaignID']) in TrackingCampaignList):
                CampaignName = TrackingCampaignList[int(data['CampaignID'])].name

            FlowName = ''
            if ('FlowID' in data.keys() and len(str(data['FlowID'])) > 0 and int(data['FlowID']) in FlowList):
                FlowName = FlowList[int(data['FlowID'])].name

            LanderName = ''
            if ('LanderID' in data.keys() and len(str(data['LanderID'])) > 0 and int(data['LanderID']) in LanderList):
                LanderName = LanderList[int(data['LanderID'])].name

            OfferName = ''
            if ('OfferID' in data.keys() and len(str(data['OfferID'])) > 0 and int(data['OfferID']) in OfferList):
                OfferName = OfferList[int(data['OfferID'])].name

            TrafficSourceName = ''
            if ('TrafficSourceID' in data.keys() and len(str(data['TrafficSourceID'])) > 0 and int(data['TrafficSourceID']) in TrafficSourceList):
                TrafficSourceName = TrafficSourceList[int(data['TrafficSourceID'])].name

            AffiliateNetworkName = ''
            if ('AffiliateNetworkID' in data.keys() and len(str(data['AffiliateNetworkID'])) > 0 and int(data['AffiliateNetworkID']) in AffiliateNetworkList):
                AffiliateNetworkName = AffiliateNetworkList[int(data['AffiliateNetworkID'])].name

            CountryCode = ''
            if ('Country' in data.keys() and len(str(data['Country'])) > 0 and  str(data['Country']) in CountryList):
                CountryCode = CountryList[str(data['Country'])].alpha3Code
            
            #payoutMode 等于Manual 取 payoutValue
            if (int(data['OfferID']) in OfferList and int(OfferList[int(data['OfferID'])].payoutMode) == 1):
                data['Revenue'] = int(OfferList[int(data['OfferID'])].payoutValue * 1000000)

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
    def save(self,table,valueList,usersList,md5Key,OfferList):
        print ("save")
        resAdStatList = dict()

        #更新数据
        fileName = "/tmp/"+table
        #print ("table",table)        
        f=open(fileName+'.tbl','w')
        stringData = ''
        print ("valueList",len(valueList))
        num = len(valueList)
        for index in range(num):
            md5Key = valueList[index]['KeysMD5']
            data = copy.deepcopy(self.adStatisList[md5Key])#self.RedisClass.getAdStatValue(md5Key)
            #data['KeysMD5'] = md5Key
            UserID = 0
            #print ("data================================",data,"________________")
            #print ("________________",md5Key,data)
            UserIDText = data['UserID']
            #print(UserIDText)
            if UserIDText in usersList:
                UserID = usersList[UserIDText]['id']

            cost = 0
            Revenue = 0            
            #print (md5Key,"Visits",data['Visits'],"VisitsFlag",data['VisitsFlag'],'Conversions',data['Conversions'],'ConversionsFlag',data['ConversionsFlag'],'Clicks',data['Clicks'],"ClicksFlag",data['ClicksFlag'])
            if (data['Visits'] and str(data['VisitsFlag']) != '1'):
                data['Clicks'] = 0
                data['Revenue'] = 0
                data['VisitsFlag'] = 1
                data['Conversions'] = 0
                self.adStatisList[md5Key]['VisitsFlag'] = 1
                if (data['Cost']):
                    cost = int(float(data['Cost'])*1000000)
            elif (data['Conversions'] and int(data['Conversions']) >= 1 and str(data['ConversionsFlag']) != '1'):
                data['Visits'] = 0
                data['Clicks'] = 0
                data['Impressions'] = 0
                data['ConversionsFlag'] = 1
                self.adStatisList[md5Key]['ConversionsFlag'] = 1
                if (data['Revenue']):
                    Revenue = int(float(data['Revenue']))
                
                #print(OfferList[int(data['OfferID'])])
                #payoutMode 等于Manual 取 payoutValue
                if (int(data['OfferID']) in OfferList and int(OfferList[int(data['OfferID'])].payoutMode) == 1):
                    Revenue = int(OfferList[int(data['OfferID'])].payoutValue * 1000000)
                #print('OfferID',data['OfferID'])
                #sys.exit()

            elif (data['Clicks'] and int(data['Clicks']) >= 1):
                data['Visits'] = 0
                data['Revenue'] = 0
                data['Impressions'] = 0
                #data['ClicksFlag'] = 1
                data['Conversions'] = 0
                #self.adStatisList[md5Key]['ClicksFlag'] = 1
            else:
                continue
            #print("Revenue",data['Revenue'])
            self.RedisClass.setAdStatValue(md5Key,self.adStatisList[md5Key])

            stringData += str(UserID)+"|"+\
                str(data['CampaignID'])+"|"+\
                str(data['CampaignName'])+"|"+\
                str(data['FlowID'])+"|"+\
                str(data['FlowName'])+"|"+\
                str(data['LanderID'])+"|"+\
                str(data['LanderName'])+"|"+\
                str(data['OfferID'])+"|"+\
                str(data['OfferName'])+"|"+\
                str(data['OfferUrl'])+"|"+\
                str(data['OfferCountry'])+"|"+\
                str(data['AffiliateNetworkID'])+"|"+\
                str(data['AffilliateNetworkName'])+"|"+\
                str(data['TrafficSourceID'])+"|"+\
                str(data['TrafficSourceName'])+"|"+\
                str(data['Language'])+"|"+\
                str(data['Model'])+"|"+\
                str(data['Country'])+"|"+\
                str(data['City'])+"|"+\
                str(data['Region'])+"|"+\
                str(data['ISP'])+"|"+\
                str(data['MobileCarrier'])+"|"+\
                str(data['Domain'])+"|"+\
                str(data['DeviceType'])+"|"+\
                str(data['Brand'])+"|"+\
                str(data['OS'])+"|"+\
                str(data['OSVersion'])+"|"+\
                str(data['Browser'])+"|"+\
                str(data['BrowserVersion'])+"|"+\
                str(data['ConnectionType'])+"|"+\
                str(data['Timestamp'])+"|"+\
                str(data['Visits'])+"|"+\
                str(data['Clicks'])+"|"+\
                str(data['Conversions'])+"|"+\
                str(cost)+"|"+\
                str(Revenue)+"|"+\
                str(data['Impressions'])+"|"+\
                str(md5Key)+"|"+\
                str(data['VisitorIP'])+"|"+\
                str(data['V1'])+"|"+\
                str(data['V2'])+"|"+\
                str(data['V3'])+"|"+\
                str(data['V4'])+"|"+\
                str(data['V5'])+"|"+\
                str(data['V6'])+"|"+\
                str(data['V7'])+"|"+\
                str(data['V8'])+"|"+\
                str(data['V9'])+"|"+\
                str(data['V10'])+"|"+\
                str(data['tsCampaignId'])+"|"+\
                str(data['tsWebsiteId'])+"|"+\
                "|"+\
                "|"+\
                str(data['ClickID'])
            stringData += '\n'
        f.write(stringData)
        f.close()
        #print ("stringData===============",stringData)
        #sys.exit()
        if (len(stringData) <= 0):
            return False
        
        #清空字段
        stringData = ''
        #command = "mysqlimport -h ec2-18-220-153-39.us-east-2.compute.amazonaws.com -udev -p'55Te$ydFq' --fields-terminated-by='|' -f AdClickTool  adstatis_new_4 --local  /tmp/adstatis_new_4.tbl"  
        command = "mysqlimport -h "+mysql_report['host']+" -u"+mysql_report['user']+" -p'"+mysql_report['passwd']+"' --fields-terminated-by='|'  -f  "+mysql_report['name']+"  --use-threads=10  --local  /tmp/"+table+".tbl"
        print ("command",command)
        try:
            return_code = subprocess.call(command, shell=True)
            print ("return_code:",return_code)
            gc.collect()
            return True
        except Exception as e:
            print (traceback.print_exc())
            gc.collect() 
            return False
        

def main(index):  
    print ("AutoRes is starting")
    print ("Respawning")
    try:
        AdStatisClass = AdStatis(index)           
        AdStatisClass.doAdStatis()
    except Exception as e:
        print (traceback.print_exc())
        #main(index)
    finally:
        print ('success')

if __name__ == "__main__": 
    index = sys.argv[1] 
    main(index)
