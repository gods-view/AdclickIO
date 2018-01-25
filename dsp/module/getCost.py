#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print (BASE_DIR)
sys.path.append(BASE_DIR + "/../")
from affiliate.model.mysql_report import AdStatisLog0, AdStatisLog1, AdStatisLog2, AdStatisLog3, AdStatisLog4, \
    AdStatisLog5, AdStatisLog6, AdStatisLog7, AdStatisLog8, AdStatisLog9
from affiliate.model.mysql_model import TrafficSource, AdCost, CampaignMap, TemplateTrafficSource
from dsp.module.mgid import Mgid
from dsp.module.popcash import PopCash
from dsp.module.popad import Popad
from dsp.module.revcontent import Revcontent
from dsp.module.zeropark import Zeropark
from dsp.module.exoclick import ExoClick


class GetCost(object):
    def get_object(self):
        # while True:
        getdata_list = TrafficSource.select().where(
            TrafficSource.integrations == 1
        )
        token, account, password = '', '', ''
        for item in getdata_list:
            name = item.name
            userid = item.userid
            if item.token:
                token = item.token
            if item.account:
                account = item.account
            if item.password:
                password = item.password
            templateId = item.trafficTemplateId
            # print (userid, name, token, account, password, templateId)
            self.get_data(userid, name, token, account, password, templateId)
        # timer = threading.Timer(900.0, self.get_object)
        # timer.start()

    def get_data(self, userid, name, token, account, password, templateId):
        # 拿到该流量源对应的模板
        TemplateTraffic = TemplateTrafficSource.select().where(
            TemplateTrafficSource.id == templateId)[0]
        table_name = eval("AdStatisLog" + str(userid % 10))
        print (table_name)
        # print (table_name, TemplateTraffic.name)
        # 根据流量源名称调用不同的api
        if TemplateTraffic.name == "MGID.com":
            try:
                print ("mgid")
                mgid = Mgid(token)
                result = mgid.login(account, password)
                if result:
                    mgid.campaigns(table_name)
            except:
                raise Exception('error')
        elif TemplateTraffic.name == "PopCash.net":
            try:
                print ("popcash")
                popcash = PopCash(token)
                popcash.get_report(table_name)
            except:
                raise Exception('error')
        elif TemplateTraffic.name == "popads.net":
            try:
                print ("popads")
                popad = Popad(account, password, token)
                popad.campaigns(table_name)
            except:
                raise Exception('error')
        elif TemplateTraffic.name == "RevContent.com":
            try:
                print ("RevContent")
                revcontent = Revcontent(account, password)
                revcontent.login()
                revcontent.campaigns(table_name)
            except:
                raise Exception('error')
        elif TemplateTraffic.name == "ZeroPark.com":
            try:
                print ("ZeroPark")
                zeropark = Zeropark(token)
                zeropark.campaigns(table_name)
            except:
                raise Exception('error')
        elif TemplateTraffic.name == "ExoClick.com":
            try:
                print ("ExoClick")
                exoclick = ExoClick(account, password, token)
                exoclick.login()
                exoclick.campaigns(table_name)
            except:
                raise Exception('error')


if __name__ == '__main__':
    update_cost = GetCost()
    update_cost.get_object()
