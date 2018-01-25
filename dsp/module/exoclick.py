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


class ExoClick:
    def __init__(self, username, password, token):
        self.cost_list = {}
        self.headers = {"test": "test"}
        self.username = username
        self.password = password
        self.token = token
        # self.username = "ChuckChuck"
        # self.password = "Ihave4cars$"
        # self.token = "7c2105d2fe5ef2fea6be6656f143cfeb5b696a7b"

    def login(self):
        url = config.get('exoclick', 'loginUrl')
        # username = config.get('exoclick', "username")
        # password = config.get('exoclick', "password")
        data = {'username': self.username, "password": self.password, "api_token": self.token}
        # print (data)
        res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=10)
        # print (respond)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                self.token = data['token']
                # print (self.token, data["type"])
                self.headers = {
                    "Authorization": str(data["type"]) + " " + str(data["token"])
                    # "Authorization": data['type'] + " " + data['token']
                }
                # print (self.headers)
                return True
            except Exception as e:
                print("error")
                return False
        return False

    # 拿到所有广告商
    def campaigns(self, table_name):
        self.tablename = table_name
        # print (config.get('popcash', 'campaignsUrl'))
        url = (config.get('exoclick', 'campaignsUrl'))
        print (url)
        # print (self.headers)
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        # print url
        # print "res:",res,"respond:",respond
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print (data)
                items = data["result"]
                # print (items)
                for key, value in items.items():
                    # self.campaign_list.append(value['id'])
                    # self.analysis(value['id'])
                    # print (key)
                    self.analysis(key)
                    # self.set_geotargeting(value['id'])
                    # return True
            except Exception as e:
                print (e)
                print("error")
                # return False
        # return False
        timer = threading.Timer(300.0, self.campaigns)
        timer.start()

    # 根据广告id拉取广告内容
    def analysis(self, id):
        # print(id)
        url = config.get('exoclick', 'qualityAnalysisUrl') % (id, "totals")
        # print "analysis url", url
        res, respond = HttpSpider().internal_get(url, timeout=300, headers=self.headers)
        if respond:
            data = json.loads(respond.encode())
            # print (data)
            try:
                createtime = int(time.time())
                data = json.loads(respond)
                # print (data["result"])
                items = data["result"]
                for item in items:
                    # print (type(item["idcampaign"]), type(id))
                    # print (item["idcampaign"], item["cost"])
                    # print (item)
                    if item["idcampaign"] == int(id):
                        self.cost_list["CampaignID"] = item["idcampaign"]
                        self.cost_list["Cost"] = str(float('%.2f' % item["cost"]))
                        self.cost_list["Createtime"] = createtime
                        self.cost_list["type"] = 1
                        # print (self.cost_list)
                        AdCost.insert(self.cost_list).execute()
                # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
                data_cost = AdCost.select().where(AdCost.CampaignID == str(id), AdCost.type == 1).order_by(
                    AdCost.Createtime.desc()).limit(2)
                # for data in data_cost:
                #     print (data.CampaignID, data.Cost)
                if len(data_cost) >= 2:
                    max_createtime = data_cost[1].Createtime
                    new_max_createtime = data_cost[0].Createtime
                    OldCost = data_cost[1].Cost
                    NewCost = data_cost[0].Cost
                    print (float(OldCost), float(NewCost))
                    # 算出与15分钟之前的cost的差值
                    temp_cost = float(NewCost) - float(OldCost)
                    ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
                        CampaignMap.TheirCampId == str(id))
                    # print (len(ourcamplist))
                    if len(ourcamplist) > 0:
                        for ourcamp in ourcamplist:
                            ourcampid = ourcamp.OurCampId
                            # print (ourcampid)
                            # 拿到该时间段内的访问量
                            # visit_list = self.tablename.select().where(
                            #     self.tablename.CampaignID == 150489,
                            #     self.tablename.Timestamp.between(1512127713263, 1512127719302))
                            visit_list = self.tablename.select().where(
                                self.tablename.CampaignID == ourcampid,
                                self.tablename.Timestamp.between(max_createtime * 1000, new_max_createtime * 1000)
                            )
                            # print (visit_list)
                            # print (len(visit_list))
                            total_visit = 0
                            avg_cost = 0.0
                            # 算出访问量的总和
                            if len(visit_list) > 0:
                                for visit in visit_list:
                                    total_visit += int(visit.Visits)
                                print ("访问量" + str(total_visit))
                            # 若访问量大于0，计算cost的平均值
                            if total_visit > 0:
                                avg_cost = temp_cost / total_visit
                                print ("平均花费为：%s" % avg_cost)
                                # 将该时间段内的Campaign更新
                                self.tablename.update(Cost=avg_cost * 1000000).where(
                                    self.tablename.CampaignID == ourcampid,
                                    self.tablename.Timestamp.between(
                                        max_createtime * 1000,
                                        new_max_createtime * 1000)).execute()
                                # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
                                #                                  self.tablename.Timestamp.between(
                                #                                      1512127713263, 1512127719302)).execute()
                            # 如果访问量等于0，则将总的花费放到一个visit中
                            else:
                                print ("总花费" + str(temp_cost))
                                self.tablename.update(Cost=temp_cost * 1000000).where(
                                    self.tablename.CampaignID == ourcampid,
                                    self.tablename.Timestamp.between(
                                        max_createtime * 1000,
                                        new_max_createtime * 1000)).execute()
                                # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
                                #                                   self.tablename.Timestamp.between(
                                #                                       1512127713263, 1512127719302)).execute()
                else:
                    pass
                    # return True
            except Exception as e:
                print (e)
                print ("error")
                # return False

    def update_zone(self, campaignid, targeting_type, domains):
        url = config.get('exoclick', 'updateZone') % (campaignid, targeting_type)
        print (url)
        # data = {"targeting_type": targeting_type, "body_collection_strings_array": [domains]}
        data = domains
        # print (data)
        try:
            res, respond = HttpSpider().internal_put(url, json.dumps(data), timeout=300, headers=self.headers)
            if respond:

                data = json.loads(respond)
                if data[0] == "Campaign successfully updated.":
                    # print (data[0])
                    return True, res
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def play_campaigns(self, id):
        url = config.get('exoclick', 'palycampaignsUrl')
        data = {"campaign_ids": [id]}
        # print ("请求头", self.headers)
        try:
            res, respond = HttpSpider().internal_put(url, json.dumps(data), timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                # print (data)
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
        url = config.get('exoclick', 'pausecampaignsUrl')
        data = {"campaign_ids": [id]}
        try:
            res, respond = HttpSpider().internal_put(url, json.dumps(data), timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                # print (type(data), data)
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
    print ("执行")
    exoclick = ExoClick("ChuckChuck", "Ihave4cars$", "7c2105d2fe5ef2fea6be6656f143cfeb5b696a7b")
    exoclick.login()
    # print (exoclick.headers)
    # exoclick.campaigns()
    exoclick.update_zone(2145550, "blocked", "javdoe.com")
    # exoclick.update_zone(2145550, "targeted", "javdoe.com")
    # exoclick.pause_campaigns(21829620)
