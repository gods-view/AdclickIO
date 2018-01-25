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

import time
import json
import threading
from dsp.core.configure import config
from dsp.core.spider import HttpSpider
from affiliate.model.mysql_model import AdCost, AdStatisLog, CampaignMap
from affiliate.model.mysql_report import *


class Mgid:
    def __init__(self, token=''):
        self.token = token
        self.idAuth = ''
        self.campaign_list = []
        self.teaser_list = []
        self.widget_uid_list = {}
        self.cost_list = {}

    def login(self, username='', password=''):
        url = config.get('mgid', 'tokenUrl')
        # username = config.get('mgid', "username")
        # password = config.get('mgid', "password")
        data = {'email': username, "password": password}
        # print (data)
        res, respond = HttpSpider().internal_post(url, data, timeout=10)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                self.token = data['token']
                self.idAuth = data['idAuth']
                # print (self.token)
                return True
            except Exception as e:
                print("error")
                return False
        return False

    # 拿到所有广告商
    def campaigns(self, table_name):
        self.tablename = table_name
        # print (config.get('mgid', 'campaignsUrl'))
        url = (config.get('mgid', 'campaignsUrl') % self.idAuth)
        url = url + "?token=" + str(self.token) + "&Fields=['name','id','status','widgetsFilterUid']"
        res, respond = HttpSpider().internal_get(url, timeout=300)
        # print url
        # print "res:",res,"respond:",respond
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print data
                for index, value in data.items():
                    # self.campaign_list.append(value['id'])
                    self.analysis(value['id'])
                    # print (value['id'])
                    # self.set_geotargeting(value['id'])
                return True
            except Exception as e:
                print (e)
                print("error")
                return False
        return False

    # 根据广告id拉取广告内容
    def analysis(self, id):
        url = config.get('mgid', 'qualityAnalysisUrl') % (id, self.token)
        # print "analysis url", url
        res, respond = HttpSpider().internal_get(url, timeout=300)
        if respond:
            data = json.loads(respond.encode())
            try:
                data = json.loads(respond)
                for key, items in data.items():
                    # 拿到CampaignID这层的数据
                    key = key
                    sum_websiteId = 0.0
                    createtime = int(time.time())
                    # print items
                    for keys, item in items.items():
                        # print item
                        if item:
                            # 如果CampaignID中包含WebsiteId，则遍历取得每个WebsiteId的数据
                            for uid, values in item.items():
                                if len(values["sources"]) != 0:
                                    # print (values["sources"])
                                    for widget, widgetval in values["sources"].items():
                                        sum_websiteId += widgetval["spent"]
                                # 若无子集，则直接拿出cost
                                else:
                                    sum_websiteId += values["spent"]
                        else:
                            pass
                        self.cost_list["CampaignID"] = key
                        self.cost_list["Cost"] = str(float('%.2f' % sum_websiteId))
                        self.cost_list["Createtime"] = createtime
                        self.cost_list["type"] = 1
                        # print (self.cost_list)
                        AdCost.insert(self.cost_list).execute()
                        # print ("插入成功")
                # print (key)
                # 从数据库中拿Createtime最大的两条数据，即为当前数据与15分钟之前的数据
                data_cost = AdCost.select().where(AdCost.CampaignID == key, AdCost.type == 1).order_by(
                        AdCost.Createtime.desc()).limit(2)
                if len(data_cost) >= 2:
                    max_createtime = data_cost[1].Createtime * 1000
                    new_max_createtime = data_cost[0].Createtime * 1000
                    OldCost = data_cost[1].Cost
                    NewCost = data_cost[0].Cost
                    # print (float(OldCost), float(NewCost), NewCost, OldCost)
                    # 算出与15分钟之前的cost的差值
                    temp_cost = float(NewCost) - float(OldCost)
                    ourcamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
                        CampaignMap.TheirCampId == key)
                    # print (len(ourcamplist))
                    if len(ourcamplist) > 0:
                        for ourcamp in ourcamplist:
                            ourcampid = ourcamp.OurCampId
                            # print (ourcampid)
                            # 拿到该时间段内的访问量
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
                                self.tablename.update(Cost=avg_cost * 1000000).where(
                                    self.tablename.CampaignID == ourcampid,
                                    self.tablename.Timestamp.between(
                                        max_createtime,
                                        new_max_createtime)).execute()
                                # self.tablename.update(Cost=2 * 1000000).where(self.tablename.CampaignID == 119,
                                #                                               self.tablename.Timestamp.between(
                                #                                                   1512482109442,
                                #                                                   1512453342117)).execute()
                            # 如果访问量等于0，则将总的花费放到一个visit中
                            else:
                                print ("总花费" + str(temp_cost))
                                print (self.tablename.update(Cost=temp_cost * 1000000).where(
                                    self.tablename.CampaignID == ourcampid,
                                    self.tablename.Timestamp.between(max_createtime,
                                                                     new_max_createtime)).execute())
                else:
                    pass
                return True
            except Exception as e:
                print (e)
                print ("error")
                return False

    def block_campaigns(self, id, whethertoblock, reason):
        url = config.get('mgid', 'BlockOrUnblockUrl') % (self.idAuth, id, self.token)
        if whethertoblock == 0:
            # print ("打开")
            data = {'whetherToBlockByClient': whethertoblock}
        else:
            # print ("关闭，原因:%s" % reason)
            data = {'whetherToBlockByClient': whethertoblock, "blockByClientReason": reason}
        # print (data)
        try:
            res, respond = HttpSpider().internal_patch(url, data, timeout=300)
            if respond:
                datas = json.loads(respond)
                if "errors" in datas.keys():
                    # print ("fail")
                    return False, res
                return True, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    # page=24
    def block_widgets(self, id, websiteid):
        url = config.get('mgid', 'blockwidgetsUrl') % (self.idAuth, id, self.token)
        # data = {'widgetsfilterUid': ['off', 'only', 56930494]}
        print (url)
        # "widgetsFilterUid=include,only,5582974"
        # widgetsFilterUid = include,except, 5495607
        data = [('widgetsFilterUid', 'include,except,' + websiteid), ]
        # data = {'widgetsfilterUid': {'editing_method': 'include', 'filter_type': 'only', 'uid1': 5582974}}
        # print (data)
        try:
            res, respond = HttpSpider().internal_patch(url, data, timeout=300)
            if respond:
                data = json.loads(respond)
                # print (type(data["id"]))
                if "id" in data.keys():
                    if data["id"] == int(id):
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def play_widgets(self, id, websiteid):
        url = config.get('mgid', 'blockwidgetsUrl') % (self.idAuth, id, self.token)
        # data = {'widgetsfilterUid': ['off', 'only', 56930494]}
        print (url)
        # "widgetsFilterUid=include,only,5582974"
        # widgetsFilterUid = include,except, 5495607
        data = [('widgetsFilterUid', 'exclude,except,' + websiteid), ]
        # data = {'widgetsfilterUid': {'editing_method': 'include', 'filter_type': 'only', 'uid1': 5582974}}
        # print (data)
        try:
            res, respond = HttpSpider().internal_patch(url, data, timeout=300)
            if respond:
                data = json.loads(respond)
                # print (type(data["id"]))
                if "id" in data.keys():
                    if data["id"] == int(id):
                        # print ("success")
                        return True, res
                # print (data)
                return False, res
            else:
                return False, res
        except Exception as e:
            print ("error")
            return False, e

    def get_teaserlist(self, campaign_id):
        url = config.get('mgid', 'getclientteaserUrl') % (self.idAuth)
        url = url + "?token=" + str(self.token) + "&Fields=['title','url']&campaign=" + campaign_id + "&limit=400"
        res, respond = HttpSpider().internal_get(url, timeout=300)
        # print url
        # print "res:",res,"respond:",respond
        if respond:
            data = json.loads(respond)
            try:
                data = json.loads(respond)
                # print (data)
                for index, value in data.items():
                    self.teaser_list.append(value['id'])
                    # self.set_geotargeting(value['id'])
                return True
            except Exception as e:
                print (e)
                print ("error")
                return False
        return False

    def set_coefficient(self, id, qualityFactor):
        url = config.get('mgid', 'setcoefficientUrl') % (id, self.token)
        # url += ":_coeff_"
        print (url)
        # [('widgetsFilterUid', 'exclude,except,5495607'), ]
        # data = [(5597263, 2.0), ]
        # data = '{(5597263, 2.0), }'
        data = '{"5597263": 2.0}'
        # data = {"5597263": 2.0}
        # {5597263: 2.0}
        res, respond = HttpSpider().internal_patch(url, data, timeout=300)
        if respond:
            try:
                data = json.loads(respond)
                # print (data)
                return True
            except Exception as e:
                print (e)
                print ("error")
                return False

    def block_teaser(self, id, whetherToBlockByClient):
        url = config.get('mgid', 'blockteaserUrl') % (self.idAuth, id, self.token)
        # if whetherToBlockByClient == 0:
        #     print "打开"
        #     data = {'whetherToBlockByClient': whetherToBlockByClient}
        # else:
        #     print "关闭"
        data = {'whetherToBlockByClient': whetherToBlockByClient}
        # print (data)
        res, respond = HttpSpider().internal_patch(url, data, timeout=300)
        if respond:
            try:
                data = json.loads(respond)
                # print(data)
                return True
            except Exception as e:
                print ("error")
                return False


if __name__ == '__main__':
    mgid = Mgid()
    mgid.login("adobest@adobest.com", "Ihave4cars")
    # mgid.campaigns()
    # print mgid.campaign_list
    # print int(time.time())
    # print (mgid.cost_list)
    # mgid.block_campaigns('474931', 1, 'HOLIDAYS')
    # mgid.block_campaigns('474931', 0)
    # mgid.set_coefficient('475493', {"5597263": 2.0})
    # mgid.get_teaserlist('471122')
    # print mgid.teaser_list
    # mgid.block_teaser('2400883', 0)
    # mgid.set_geotargeting()
    # mgid.block_widgets('468950', "5505504,5543809")
    mgid.play_widgets('468950', "5505504,5543809")
