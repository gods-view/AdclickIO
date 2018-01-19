#!/usr/bin/env python
# encoding: utf-8
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print (BASE_DIR)
sys.path.append(BASE_DIR + "/../")
from affiliate.model.mysql_report import *
from affiliate.model.mysql_model import AdCost, TrafficSource, TemplateTrafficSource, CampaignMap, TrackingCampaign
from dsp.module.mgid import Mgid
from dsp.module.popcash import PopCash
from dsp.module.popad import Popad
from dsp.module.revcontent import Revcontent
from dsp.module.zeropark import Zeropark
from dsp.module.exoclick import ExoClick


class UpdateCost(object):
    def get_object(self):
        while True:
            if reportDb.is_closed():
                # print ("连接关闭")
                reportDb.connect()
            res = AdStatisLog4.select(AdStatisLog4.CampaignID).limit(1)
            # print ("AdStatisLog4", len(res))
            update_list = AdCost.select().where(
                AdCost.updatecost == 1
            )
            # print ("update_list", len(update_list))
            if len(update_list) > 0:
                for item in update_list:
                    id = item.id
                    CampaignID = int(item.CampaignID)
                    cost = float(item.Cost)
                    begintime = int(item.begintime) * 1000
                    endtime = int(item.endtime) * 1000
                    userid = int(item.userid)
                    # print (userid, type(userid))
                    self.update_cost(id, userid, CampaignID, begintime, endtime, cost)
            # print ("success")
            update_bidlist = AdCost.select().where(
                AdCost.updatebid == 1
            )
            if len(update_bidlist) > 0:
                for item in update_bidlist:
                    # print ("遍历更新")
                    # print (bid.CampaignID, type(bid.CampaignID))
                    temp = int(item.CampaignID)
                    theircamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
                        CampaignMap.OurCampId == temp)
                    # print (len(theircamplist))
                    for theircampain in theircamplist:
                        # print (theircampain.TheirCampId)
                        # print (temp, item.bid, item.updatebid)
                        self.update_bid(item, theircampain.TheirCampId)
                        # self.update_cost(visit)

    def update_cost(self, id, userid, CampaignID, begintime, endtime, cost):
        table_name = eval("AdStatisLog" + str(userid % 10))
        # 拿到该时间段内的访问量
        # visit_list = AdStatisLog4.select().where(
        #     AdStatisLog4.tsCampaignId == 150489,
        #     AdStatisLog4.Timestamp.between(1512127713263, 1512127719302))        
        # print ("update_cost", table_name, CampaignID, begintime, endtime)
        try:
            if reportDb.is_closed():
                print ("连接关闭")
                reportDb.connect()
            total_visit = 0
            total_visit_obj = table_name.select(fn.Count(table_name.Visits)).where(
                table_name.CampaignID == CampaignID, table_name.Timestamp.between(begintime, endtime)
            )
            # print (total_visit_obj, "total_visit_obj")
            total_visit = total_visit_obj[0].Visits
            # reportDb.close()
            avg_cost = 0.0
            # 算出访问量的总和
            if total_visit > 0:
                print("访问量" + str(total_visit))
                # 若访问量大于0，计算cost的平均值
                avg_cost = float(cost) / total_visit
                print("平均花费为：%s" % avg_cost)
                # 将该时间段内的Campaign更新
                # print (table_name, CampaignID)
                if reportDb.is_closed():
                    reportDb.connect()
                update_result = table_name.update(Cost=avg_cost * 1000000).where(
                    table_name.CampaignID == CampaignID,
                    table_name.Timestamp.between(begintime, endtime), (table_name.Visits != 0)).execute()
                print (update_result)
                # reportDb.close()
                # table_name.update(Cost=0).where(table_name.tsCampaignId == 150489,
                #                                  table_name.Timestamp.between(
                #                                      1512127713263, 1512127719302)).execute()
                AdCost.update(updatecost=2, remark="cost更新成功").where(AdCost.id == id).execute()
            else:
                AdCost.update(updatecost=3, remark="该段时间无访问").where(AdCost.id == id).execute()
        except Exception as e:
            print(e)
            AdCost.update(updatecost=3, remark="cost更新失败").where(AdCost.id == id).execute()
            print ("exit")
            sys.exit()

    def update_bid(self, item, theircampid):
        # print ("查找并更新")
        result = ""
        ourcampid = item.CampaignID
        id = item.id
        bid = item.bid
        TrafficsourceId = item.TrafficsourceId
        # print (TrafficsourceId, ourcampid)
        trafficsourcelist = TrafficSource.select().where(TrafficSource.id == TrafficsourceId,
                                                         TrafficSource.integrations == 1)
        if len(trafficsourcelist) > 0:
            trafficsource = trafficsourcelist[0]
            # print (len(trafficsource))
            username = trafficsource.account
            password = trafficsource.password
            token = trafficsource.token
            # print (username, password, token)
            # print (trafficsource.name, trafficsource.trafficTemplateId)
            TemplateTraffic = TemplateTrafficSource.select().where(
                TemplateTrafficSource.id == trafficsource.trafficTemplateId)[0]
            # print (TemplateTraffic.name, theircampid)
            if TemplateTraffic.name == "MGID.com":
                try:
                    reason = "it not worth"
                    token = trafficsource.token
                    # username = "adobest@adobest.com"
                    # password = "Ihave4cars"
                    mgid = Mgid(token)
                    mgid.login(username, password)
                except:
                    raise Exception('error')
            # elif TemplateTraffic.name == "PopCash.net":
            #     try:
            #         popcash = PopCash(token)
            #         print ("popcash")
            #
            #     except:
            #         raise Exception('error')
            # elif TemplateTraffic.name == "popads.net":
            #     try:
            #         print ("popads.net")
            #         popad = Popad(username, password, token)
            #         popad.login()
            #
            #     except:
            #         raise Exception('error')
            # elif TemplateTraffic.name == "RevContent.com":
            #     try:
            #         print ("RevContent.com")
            #         revcontent = Revcontent(username, password)
            #         revcontent.login()
            #
            #     except:
            #         raise Exception('error')
            elif TemplateTraffic.name == "ZeroPark.com":
                try:
                    # print ("ZeroPark.com")
                    zeropark = Zeropark(token)
                    result, remarks = zeropark.updatebid(theircampid, bid)
                except:
                    raise Exception('error')
            # elif TemplateTraffic.name == "ExoClick.com":
            #     try:
            #         print ("ExoClick.com")
            #         exoclick = ExoClick(username, password, token)
            #         exoclick.login()
            #
            #     except:
            #         raise Exception('error')
            print (result)
            if result == "":
                return
            if result:
                record = "bid更新成功" + str(remarks)
                # print (record)
                AdCost.update(updatebid=2, remark=record).where(AdCost.id == id).execute()
            else:
                # print (remarks)
                record = "bid更新失败" + remarks.decode()
                print (record)
                AdCost.update(updatebid=3, remark=record).where(AdCost.id == id).execute()


if __name__ == '__main__':
    update_cost = UpdateCost()
    update_cost.get_object()
