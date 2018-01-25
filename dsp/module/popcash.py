# encoding=utf-8
'''
mid登陆
write by alex
create on 2017-10-29
'''
import os, sys
from imp import reload

sys.path.insert(0, os.path.dirname(sys.path[0]))
reload(sys)
# sys.setdefaultencoding('utf8')

import time, datetime
import json
import threading
from dsp.core.configure import config
from dsp.core.spider import HttpSpider
from affiliate.model.mysql_model import AdCost, CampaignMap
from affiliate.model.mysql_report import *


class PopCash:
    def __init__(self, apikey=''):
        self.cost_list = {}
        self.apikey = apikey
        # "f0dd541062cffe022fed-1494250040-285e83f0c5e58506b1f0122554"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    # 拿到所有广告商
    def campaigns(self, table_name):
        self.tablename = table_name
        # print (config.get('popcash', 'campaignsUrl'))
        url = config.get('popcash', 'campaignsUrl') % self.apikey
        # print (url)
        res, respond = HttpSpider().internal_get(url, timeout=300)
        # print url
        # print "res:",res,"respond:",respond
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                items = data["campaigns"]
                # print (items["items"])
                for item in items["items"]:
                    # self.campaign_list.append(value['id'])
                    # print (item["id"], item["name"])
                    self.get_report(item["id"])

            except Exception as e:
                print (e)
                print("error")

    # 根据广告id拉取广告内容
    # def get_report(self, id):
    #     url = config.get('popcash', 'qualityAnalysisUrl') % self.apikey
    #     now_time = time.strftime("%m/%d/%Y", time.localtime())
    #     # oneDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
    #     # yesterday_time = oneDayAgo.strftime("%m/%d/%Y")
    #     # print "analysis url", url
    #     # print (yesterday_time, now_time)"campaign": 104443,
    #
    #     data = '{"startDate": "' + now_time + '","endDate": "' + now_time + '","campaign": ' + str(
    #         id) + ',"reportType": 0}'
    #     # data = '{"startDate": "11/12/2016", "endDate": "12/18/2017", "reportType": 3}'
    #     # print (data)
    #     res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
    #     # res, respond = HttpSpider().internal_post(url, data, timeout=300)
    #     # print (respond)
    #     if respond:
    #         data = json.loads(respond.encode())
    #         try:
    #             data = json.loads(respond)
    #             if len(data["report"]) > 0:
    #                 cost = data["report"][0]["ssp"]
    #                 createtime = int(time.time())
    #                 self.cost_list["CampaignID"] = id
    #                 self.cost_list["Cost"] = str(round(float(cost), 8))
    #                 self.cost_list["Createtime"] = createtime
    #                 self.cost_list["type"] = 1
    #                 print (self.cost_list)
    #                 AdCost.insert(self.cost_list).execute()
    #                 # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
    #                 data_cost = AdCost.select().where(AdCost.CampaignID == str(id), AdCost.type == 1).order_by(
    #                     AdCost.Createtime.desc()).limit(2)
    #                 if len(data_cost) >= 2:
    #                     print (len(data_cost))
    #                     max_createtime = data_cost[1].Createtime * 1000
    #                     new_max_createtime = data_cost[0].Createtime * 1000
    #                     OldCost = data_cost[1].Cost
    #                     NewCost = data_cost[0].Cost
    #                     print (float(OldCost), float(NewCost))
    #                     # 算出与15分钟之前的cost的差值
    #                     temp_cost = float(NewCost) - float(OldCost)
    #                     ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(CampaignMap.TheirCampId == str(id))
    #                     print (len(ourcamplist))
    #                     if len(ourcamplist) > 0:
    #                         for ourcamp in ourcamplist:
    #                             ourcampid = ourcamp.OurCampId
    #                             print (ourcampid)
    #                             # for data in data_cost:
    #                             #     print (data.CampaignID, data.Cost)
    #                             # 拿到该时间段内的访问量
    #                             # visit_list = self.tablename.select().where(
    #                             #     self.tablename.CampaignID == 150489,
    #                             #     self.tablename.Timestamp.between(1512127713263, 1512127719302))
    #                             total_visit = 0
    #                             avg_cost = 0.0
    #                             total_visit_obj = self.tablename.select(fn.Count(self.tablename.Visits)).where(
    #                                 self.tablename.CampaignID == ourcampid,
    #                                 self.tablename.Timestamp.between(max_createtime, new_max_createtime)
    #                             )
    #                             total_visit = total_visit_obj[0].Visits
    #                             # visit_list = self.tablename.select().where(
    #                             #     self.tablename.CampaignID == ourcampid,
    #                             #     self.tablename.Timestamp.between(max_createtime, new_max_createtime)
    #                             # )
    #                             # print (max_createtime, new_max_createtime)
    #                             # print (visit_list)
    #                             # print (len(visit_list))
    #                             # 算出访问量的总和
    #                             # if len(visit_list) > 0:
    #                             #     for visit in visit_list:
    #                             #         total_visit += int(visit.Visits)
    #                             print ("访问量" + str(total_visit))
    #                             # 若访问量大于0，计算cost的平均值
    #                             if total_visit > 0:
    #                                 avg_cost = temp_cost / total_visit
    #                                 print ("平均花费为：%s" % avg_cost)
    #                                 # 将该时间段内的Campaign更新
    #                                 self.tablename.update(Cost=avg_cost * 1000000).where(
    #                                     self.tablename.CampaignID == ourcampid,
    #                                     self.tablename.Timestamp.between(
    #                                         max_createtime,
    #                                         new_max_createtime)).execute()
    #                                 # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
    #                                 #                                  self.tablename.Timestamp.between(
    #                                 #                                      1512127713263, 1512127719302)).execute()
    #                             # 如果访问量等于0，则将总的花费放到每个visit中
    #                             else:
    #                                 print ("总花费" + str(temp_cost))
    #                                 self.tablename.update(Cost=temp_cost * 1000000).where(
    #                                     self.tablename.CampaignID == ourcampid,
    #                                     self.tablename.Timestamp.between(
    #                                         max_createtime,
    #                                         new_max_createtime)).execute()
    #                                 # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
    #                                 #                                   self.tablename.Timestamp.between(
    #                                 #                                       1512127713263, 1512127719302)).execute()
    #         except Exception as e:
    #             print (e)
    #             print ("error")
    def get_report(self, table_name):
        self.tablename = table_name
        url = config.get('popcash', 'qualityAnalysisUrl') % self.apikey
        now_time = time.strftime("%m/%d/%Y", time.localtime())
        # print "analysis url", url
        # print (now_time)
        data = '{"startDate": "11/30/2017","endDate": "' + now_time + '","reportType": 3}'
        # print (data)
        res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
        # res, respond = HttpSpider().internal_post(url, data, timeout=300)
        # print (respond)
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print (data["token"])
                self.detail_report(data["token"])
            except Exception as e:
                print (e)
                print ("error")

    def detail_report(self, token):
        url = config.get('popcash', 'detailreport') % self.apikey
        now_time = time.strftime("%m/%d/%Y", time.localtime())
        # print "analysis url", url
        # print (now_time)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {"token": token}
        # print (data)
        res, respond = HttpSpider().internal_post(url, json.dumps(data), timeout=300, headers=self.headers)
        data = json.loads(respond)
        # print (data["report"])
        for item in data["report"]:
            createtime = int(time.time())
            self.cost_list["CampaignID"] = item[0]
            self.cost_list["Cost"] = str(round(float(item[2]), 8))
            self.cost_list["Createtime"] = createtime
            self.cost_list["type"] = 1
            # print (self.cost_list)
            AdCost.insert(self.cost_list).execute()
            # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
            data_cost = AdCost.select().where(AdCost.CampaignID == item[0], AdCost.type == 1).order_by(
                AdCost.Createtime.desc()).limit(2)
            if len(data_cost) >= 2:
                print (len(data_cost))
                max_createtime = data_cost[1].Createtime * 1000
                new_max_createtime = data_cost[0].Createtime * 1000
                OldCost = data_cost[1].Cost
                NewCost = data_cost[0].Cost
                print (float(OldCost), float(NewCost))
                # 算出与15分钟之前的cost的差值
                temp_cost = float(NewCost) - float(OldCost)
                ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
                    CampaignMap.TheirCampId == item[0])
                # print (len(ourcamplist))
                if len(ourcamplist) > 0:
                    for ourcamp in ourcamplist:
                        ourcampid = ourcamp.OurCampId
                        # print (ourcampid)
                        # for data in data_cost:
                        #     print (data.CampaignID, data.Cost)
                        # 拿到该时间段内的访问量
                        # visit_list = self.tablename.select().where(
                        #     self.tablename.CampaignID == 150489,
                        #     self.tablename.Timestamp.between(1512127713263, 1512127719302))
                        total_visit = 0
                        avg_cost = 0.0
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
                            self.tablename.update(Cost=avg_cost * 1000000).where(self.tablename.CampaignID == ourcampid,
                                                                                 self.tablename.Timestamp.between(
                                                                                     max_createtime,
                                                                                     new_max_createtime)).execute()
                            # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
                            #                                  self.tablename.Timestamp.between(
                            #                                      1512127713263, 1512127719302)).execute()
                        # 如果访问量等于0，则将总的花费放到每个visit中
                        else:
                            print ("总花费" + str(temp_cost))
                            self.tablename.update(Cost=temp_cost * 1000000).where(
                                self.tablename.CampaignID == ourcampid,
                                self.tablename.Timestamp.between(
                                    max_createtime,
                                    new_max_createtime)).execute()
                            # self.tablename.update(Cost=0).where(self.tablename.CampaignID == 150489,
                            #                                   self.tablename.Timestamp.between(
                            #                                       1512127713263, 1512127719302)).execute()

    def close_campaigns(self, id):
        url = config.get('popcash', 'blockcampaignsUrl') % (id, self.apikey)
        data = {"status": 3}
        # print (url)
        try:
            res, respond = HttpSpider().internal_put(url, json.dumps(data), timeout=300, headers=self.headers)
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

    def open_campaigns(self, id):
        url = config.get('popcash', 'blockcampaignsUrl') % (id, self.apikey)
        data = {"status": 1}
        # print (url)
        try:
            res, respond = HttpSpider().internal_put(url, json.dumps(data), timeout=300, headers=self.headers)
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

    def website_switch(self, campaignid, operate, websiteid):
        url = config.get('popcash', 'switchWebsiteUrl') % (campaignid, self.apikey)
        # url = config.get('popcash', 'switchWebsiteUrl') % self.apikey
        print (url)
        data = '{"append": true,"siteTargeting":' + str(operate) + ',"websitesIds":[' + websiteid + ']}'
        # data = '{"append": true,"siteTargeting":' + str(operate) + ',"websitesIds":[170663,318227]}'
        # res, respond = HttpSpider().internal_post(url, data, timeout=300)
        print (data)
        try:
            res, respond = HttpSpider().internal_post(url, data, timeout=300, headers=self.headers)
            if respond:
                data = json.loads(respond)
                print (data)
                if "websites" in data.keys():
                    # if int(websiteid) in data["websites"]:
                    # print ("success")
                    return True, res
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e


if __name__ == '__main__':
    popcash = PopCash()
    # mgid.login()
    # popcash.campaigns()
    # popcash.open_campaigns('829')
    # popcash.close_campaigns('1037600')
    # popcash.website_switch(156592, 2, "['170888', '359792', '90704', '5262', '15473', '285536', '400590', '380250', '377025', '312717', '9715', '347266', '111848', '127291', '127292', '27257', '376933', '236497', '377312', '49660', '95643', '373914', '61439', '90702', '90700', '216507', '58054', '72300', '389528', '403643', '52198', '401657', '95642', '221521', '86209', '118109', '381379', '44807', '30256', '41812', '401662', '354824', '231725', '0', '370872', '287692', '24794', '11374', '326817', '402903', '282289', '403425', '376588', '256223', '388541', '404109', '108560', '117986', '120356', '106522', '55445', '334959', '143301', '105968', '372525', '335029', '332204', '60611', '333030', '365623', '86020', '124002', '400503', '51842', '294405', '403827', '247234', '49372', '398733', '123204', '50670', '223489', '367248', '208223', '209723', '86215', '318228', '372324', '388088', '332207', '386682', '333761', '121879', '159231', '108771', '71964', '369367', '322867', '76240', '52199', '90698', '34097', '394048', '51623', '138719', '379413', '400348', '361085', '117294', '86214', '366809', '205616', '38189', '2260', '166983', '94064', '170663', '236840', '86212', '214405']")
