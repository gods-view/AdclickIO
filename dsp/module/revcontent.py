# encoding=utf-8
import os, sys
from imp import reload

sys.path.insert(0, os.path.dirname(sys.path[0]))
# print (os.path.dirname(sys.path))
# print (sys.path)
reload(sys)
# sys.setdefaultencoding('utf8')

import time
import json
import threading
from dsp import *

from dsp.core.configure import config
from dsp.core.spider import HttpSpider
from affiliate.model.mysql_model import AdCost, CampaignMap
from affiliate.model.mysql_report import *


class Revcontent:
    def __init__(self, username, password):
        self.cost_list = {}
        # self.username = "tzula"
        # self.password = "a24dbda2249a8f8519185ec154e3927423981820"
        self.username = username
        self.password = password
        # self.token = "7c2105d2fe5ef2fea6be6656f143cfeb5b696a7b"

    def login(self):
        url = config.get('revcontent', 'tokenUrl')
        username = self.username
        password = self.password
        # username = config.get('revcontent', "username")
        # password = config.get('revcontent', "password")
        data = {'grant_type': 'client_credentials', 'client_id': username, "client_secret": password}
        # print (data)
        # print (url)
        # print (data)
        res, respond = HttpSpider().internal_post(url, data, timeout=100)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                self.headers = {
                    "Authorization": str(data["token_type"]) + " " + str(data["access_token"]),
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            except Exception as e:
                print ("error")
                return False

    # 拿到所有广告商
    def campaigns(self, table_name):
        self.tablename = table_name
        # print (config.get('popcash', 'campaignsUrl'))
        url = (config.get('revcontent', 'campaignsUrl'))
        now_time = time.strftime("%Y-%m-%d", time.localtime())
        data = {}
        # print (url)
        url += '?date_from=2017-01-01&date_to='+now_time
        # print (url)
        # print (self.headers)
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        # print url
        # print "res:",res,"respond:",respond
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print (data)
                items = data["data"]
                # print (items)
                for item in items:
                    # self.campaign_list.append(value['id'])
                    # self.analysis(value['id'])
                    createtime = int(time.time())
                    self.cost_list["CampaignID"] = item["id"]
                    self.cost_list["Cost"] = str(round(float(item["cost"]), 2))
                    self.cost_list["Createtime"] = createtime
                    self.cost_list["type"] = 1
                    # print (self.cost_list)
                    AdCost.insert(self.cost_list).execute()
                    # self.analysis(key)
                    # self.set_geotargeting(value['id'])
                    # return True
                    # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
                    data_cost = AdCost.select().where(AdCost.CampaignID == item["id"], AdCost.type == 1).order_by(
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
                        ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(CampaignMap.TheirCampId == item["id"])
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
                                print ("访问量" + str(total_visit))
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
                # return False
                # return False
                # timer = threading.Timer(300.0, self.campaigns)
                # timer.start()

    def add_widget(self, id, operate, websiteid):
        self.update_type(id, operate)
        url = config.get('revcontent', 'addwidget') % id
        # {"id": "32,35,57"}
        data = {"id": websiteid}
        try:
            res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "errors" in data.keys():
                    # print (data["message"], "fail")
                    return False, res
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def remove_widget(self, id, operate, websiteid):
        self.update_type(id, operate)
        url = config.get('revcontent', 'removewidget') % id
        data = {"id": websiteid}
        try:
            res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "errors" in data.keys():
                    # print (data["message"], "fail")
                    return False, res
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def update_type(self, id, operate):
        url = config.get('revcontent', 'updatetype') % id
        data = {"status": operate}
        res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=300, headers=self.headers)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                return True
            except Exception as e:
                print ("error")
                return False

    def get_widget(self):
        url = config.get('revcontent', 'getwidget') % id
        # data = {"campaign_ids": [2124110, 2118504]}
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                return True
            except Exception as e:
                print ("error")
                return False

    def play_campaigns(self, id):
        url = config.get('revcontent', 'palycampaignsUrl')
        data = '{"id":' + id + ', "enabled": "on"}'
        # print (data)
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "errors" in data.keys():
                    # print (data["message"], "fail")
                    return False, res
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def pause_campaigns(self, id):
        url = config.get('revcontent', 'palycampaignsUrl')
        data = '{"id":' + id + ', "enabled": "off"}'
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                if "errors" in data.keys():
                    # print (data["message"], "fail")
                    return False, res
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e


if __name__ == '__main__':
    revcontent = Revcontent()
    revcontent.login()
    # print (exoclick.headers)
    # revcontent.campaigns()
    # revcontent.update_type("include")
    # revcontent.update_type("include")

    # revcontent.add_widget(336195, "exclude")
    # revcontent.add_widget(336195, "include")
    revcontent.remove_widget(336195, "include")
    # revcontent.add_widget()
    # revcontent.get_widget()
