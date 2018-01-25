# encoding=utf-8
import os, sys
from imp import reload

sys.path.insert(0, os.path.dirname(sys.path[0]))
# print (os.path.dirname(sys.path))
# print (sys.path)
reload(sys)
# sys.path.insert(0, os.path.dirname(sys.path[0]))
# reload(sys)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
# print (BASE_DIR)
# sys.setdefaultencoding('utf8')

import time
import json
import threading
from dsp import *

from dsp.core.configure import config
from dsp.core.spider import HttpSpider
from affiliate.model.mysql_model import AdCost, CampaignMap
from affiliate.model.mysql_report import *


class Zeropark:
    def __init__(self, token):
        self.cost_list = {}
        # self.username = username
        # self.password = password
        # self.token = token
        # self.headers = {
        #     "api-token": "AAABWbbuJb0mnhLNrD4rT4v5pOlzyJGHSaNq8fqYFqamUf++gue16ZSprTR1qRuCkfX9i8wDueCp9TH7hERJ+Q=="
        # }
        self.headers = {
            "api-token": token
        }

    # 拿到所有广告商
    def campaigns(self, table_name):
        self.tablename = table_name
        url = config.get('zeropark', 'campaignsUrl') + "interval=THIS_YEAR"
        # print (url)
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print (data["elements"])
                for item in data["elements"]:
                    # print (item)
                    createtime = int(time.time())
                    # print (item["details"]["id"], item["details"]["name"], item["stats"]["spent"])
                    id = str(item["details"]["id"])
                    self.cost_list["CampaignID"] = id
                    self.cost_list["Cost"] = str(float('%.2f' % item["stats"]["spent"]))
                    self.cost_list["Createtime"] = createtime
                    self.cost_list["type"] = 1
                    # print (self.cost_list)
                    AdCost.insert(self.cost_list).execute()
                    # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
                    data_cost = AdCost.select().where(AdCost.CampaignID == id, AdCost.type == 1).order_by(
                        AdCost.Createtime.desc()).limit(2)
                    # for data in data_cost:
                    #     print (data.CampaignID, data.Cost)
                    if len(data_cost) >= 2:
                        max_createtime = data_cost[1].Createtime * 1000
                        new_max_createtime = data_cost[0].Createtime * 1000
                        OldCost = data_cost[1].Cost
                        NewCost = data_cost[0].Cost
                        print (float(OldCost), float(NewCost))
                        # 算出与15分钟之前的cost的差值
                        temp_cost = float(NewCost) - float(OldCost)
                        ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(CampaignMap.TheirCampId == id)
                        # print (len(ourcamplist))
                        if len(ourcamplist) > 0:
                            for ourcamp in ourcamplist:
                                ourcampid = ourcamp.OurCampId
                                # print (ourcampid)
                                # 拿到该时间段内的访问量
                                # visit_list = self.tablename.select().where(
                                #     self.tablename.tsCampaignId == 150489,
                                #     self.tablename.Timestamp.between(1512127713263, 1512127719302))
                                total_visit = 0
                                avg_cost = 0.0
                                # print (self.tablename)
                                total_visit_obj = self.tablename.select(fn.Count(self.tablename.Visits)).where(
                                    self.tablename.CampaignID == ourcampid,
                                    self.tablename.Timestamp.between(max_createtime, new_max_createtime)
                                )
                                total_visit = total_visit_obj[0].Visits
                                # visit_list = self.tablename.select().where(
                                #     self.tablename.CampaignID == ourcampid,
                                #     self.tablename.Timestamp.between(max_createtime, new_max_createtime)
                                # )
                                # print (max_createtime, new_max_createtime)
                                # print (visit_list)
                                # print (len(visit_list))
                                # 算出访问量的总和
                                # if len(visit_list) > 0:
                                #     for visit in visit_list:
                                #         total_visit += int(visit.Visits)
                                # print ("访问量" + str(total_visit))
                                # 若访问量大于0，计算cost的平均值
                                if total_visit > 0:
                                    avg_cost = temp_cost / total_visit
                                    print ("平均花费为：%s" % avg_cost)
                                    # 将该时间段内的Campaign更新
                                    self.tablename.update(Cost=avg_cost*1000000).where(self.tablename.CampaignID == ourcampid,
                                                                             self.tablename.Timestamp.between(
                                                                                 max_createtime,
                                                                                 new_max_createtime)).execute()
                                    # self.tablename.update(Cost=0).where(self.tablename.tsCampaignId == 150489,
                                    #                                  self.tablename.Timestamp.between(
                                    #                                      1512127713263, 1512127719302)).execute()
                                # 如果访问量等于0，则将总的花费放到每个visit中
                                else:
                                    print ("总花费" + str(temp_cost))
                                    self.tablename.update(Cost=temp_cost*1000000).where(self.tablename.CampaignID == ourcampid,
                                                                              self.tablename.Timestamp.between(
                                                                                  max_createtime,
                                                                                  new_max_createtime)).execute()
                                    # self.tablename.update(Cost=0).where(self.tablename.tsCampaignId == 150489,
                                    #                                   self.tablename.Timestamp.between(
                                    #                                       1512127713263, 1512127719302)).execute()
                    else:
                        pass
            except Exception as e:
                print (e)
                print("error")

    # def getbid(self, campaignid):
    #     url = config.get('zeropark', 'getbidUrl') % campaignid
    #     print (url)
    #     res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
    #     if respond:
    #         try:
    #             data = json.loads(respond)
    #             print (data)
    #             print (data["value"])
    #
    #         except Exception as e:
    #             print (e)
    #             print("error")

    def updatebid(self, campaignid, bid):
        url = config.get('zeropark', 'updatebidUrl') % campaignid
        # print (url)
        data = {"bid": bid}
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:

                data = json.loads(respond)
                # print (data)
                # print (data["value"])
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def resume_target(self, id, target_name):
        url = config.get('zeropark', 'resumetarget') % id
        data = {"hash": target_name}
        # print (data)
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"]["state"] == "ACTIVE":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def pause_target(self, id, target_name):
        url = config.get('zeropark', 'pausetarget') % id
        data = {"hash": target_name}
        # print (data)
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"]["state"] == "ACTIVE":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def resume_targets(self, id, target_name):
        url = config.get('zeropark', 'resumetargets') % id
        data = {"hash": target_name}
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"]["state"] == "PAUSED":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def pause_targets(self, id, target_name):
        url = config.get('zeropark', 'pausetargets') % id
        data = {"hash": target_name}
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"]["state"] == "PAUSED":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def get_target(self, id):
        url = config.get('zeropark', 'gettarget') % id + "interval=THIS_YEAR"
        # print (url)
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        if respond:
            try:
                data = json.loads(respond)
                # print (data["elements"])
                for item in data["elements"]:
                    print (item["target"], item["state"]["state"])
                return True
            except Exception as e:
                print ("error")
                return False

    def play_campaigns(self, id):
        url = config.get('zeropark', 'resumecampaigns') % id
        data = {}
        # print (url)
        # res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=300)
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"] == "ACTIVE":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def pause_campaigns(self, id):
        url = config.get('zeropark', 'pausecampaigns') % id
        # print (url)
        data = {}
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "state" in data.keys():
                    if data["state"] == "PAUSED":
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e


if __name__ == '__main__':
    print ("begin")
    zeropark = Zeropark("AAABWbbuJb0mnhLNrD4rT4v5pOlzyJGHSaNq8fqYFqamUf++gue16ZSprTR1qRuCkfX9i8wDueCp9TH7hERJ+Q==")
    print ("开始执行")
    # popad.login()
    # print (exoclick.headers)
    # zeropark.campaigns()
    # zeropark.updatebid("ebd0f9c0-b239-11e6-a9c8-0e0b03568723", 0.0001)
    # zeropark.campaigns()
    # zeropark.get_target("cb3862c0-a26b-11e7-86a7-0e06c6fba698")
    # zeropark.pause_target("ebd0f9c0-b239-11e6-a9c8-0e0b03568723", "uniform-fey-91bLaBX5")
    # zeropark.resume_target("ebd0f9c0-b239-11e6-a9c8-0e0b03568723", "uniform-fey-91bLaBX5")
    # zeropark.resume_targets("cb3862c0-a26b-11e7-86a7-0e06c6fba698", ["yankee-pus-ig4rn8fR", "whiskey-gey-4x1KVHrY"])
    zeropark.pause_targets("cb3862c0-a26b-11e7-86a7-0e06c6fba698", ["uniform-fey-91bLaBX5", "whiskey-gey-4x1KVHrY"])
    # zeropark.play_campaigns("cb3862c0-a26b-11e7-86a7-0e06c6fba698")
    # zeropark.pause_campaigns("cb3862c0-a26b-11e7-86a7-0e06c6fba698")
