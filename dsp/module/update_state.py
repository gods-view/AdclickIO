import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print (BASE_DIR)
sys.path.append(BASE_DIR + "/../")
from affiliate.model.mysql_model import AdCost
from affiliate.model.mysql_model import TrafficSource
from affiliate.model.mysql_model import TemplateTrafficSource, CampaignMap, TrackingCampaign
from dsp.module.mgid import Mgid
from dsp.module.popcash import PopCash
from dsp.module.popad import Popad
from dsp.module.revcontent import Revcontent
from dsp.module.zeropark import Zeropark
from dsp.module.exoclick import ExoClick


class UpdateState(object):
    def get_tasklist(self):
        while True:
            # print ("开始执行")
            visit_list = AdCost.select().where(
                AdCost.State == 1)
            # print ("查看符合条件的结果")
            # print (len(visit_list), visit_list)
            for visit in visit_list:
                # print ("遍历更新")
                # print (visit.CampaignID, type(visit.CampaignID))
                temp = int(visit.CampaignID)
                theircamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(CampaignMap.OurCampId == temp)
                # print (len(theircamplist))
                for theircampain in theircamplist:
                    # print (theircampain.TheirCampId)
                    self.update_state(visit, theircampain.TheirCampId)
                    # self.update_cost(visit)

    def update_state(self, visit, theircampid):
        # print ("查找并更新")
        result = ""
        ourcampid = visit.CampaignID
        # theircampid = visit.CampaignID
        id = visit.id
        status = visit.Status
        TrafficsourceId = visit.TrafficsourceId
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
                    newstatus = 0 if status == 1 else 1
                    result, remarks = mgid.block_campaigns(id=theircampid, whethertoblock=newstatus, reason=reason)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "PopCash.net":
                try:
                    popcash = PopCash(token)
                    # print ("popcash")
                    # print (theircampid, status)
                    if status == 1:
                        result, remarks = popcash.open_campaigns(theircampid)
                    else:
                        result, remarks = popcash.close_campaigns(theircampid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "popads.net":
                try:
                    # print ("popads.net")
                    popad = Popad(username, password, token)
                    popad.login()
                    if status == 1:
                        result, remarks = popad.play_campaigns(theircampid)
                    else:
                        result, remarks = popad.pause_campaigns(theircampid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "RevContent.com":
                try:
                    # print ("RevContent.com")
                    revcontent = Revcontent(username, password)
                    revcontent.login()
                    if status == 1:
                        result, remarks = revcontent.play_campaigns(theircampid)
                    else:
                        result, remarks = revcontent.pause_campaigns(theircampid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "ZeroPark.com":
                try:
                    # print ("ZeroPark.com")
                    zeropark = Zeropark(token)
                    # zeropark.login()
                    if status == 1:
                        result, remarks = zeropark.play_campaigns(theircampid)
                    else:
                        result, remarks = zeropark.pause_campaigns(theircampid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "ExoClick.com":
                try:
                    # print ("ExoClick.com")
                    exoclick = ExoClick(username, password, token)
                    exoclick.login()
                    if status == 1:
                        result, remarks = exoclick.play_campaigns(theircampid)
                    else:
                        result, remarks = exoclick.pause_campaigns(theircampid)
                except:
                    raise Exception('error')
            print (result)
            if result == "":
                return
            if result:
                record = str(status) + " 状态更新成功" + str(remarks)
                # print (record)
                AdCost.update(State=2, remark=record).where(AdCost.id == id).execute()
                # oldstatus = TrackingCampaign.select().where(TrackingCampaign.id == ourcampid)[0].status
                # new_status = 1 if oldstatus == 0 else 0
                TrackingCampaign.update(remark=record, status=status).where(TrackingCampaign.id == ourcampid).execute()
            else:
                # print (remarks)
                record = str(status) + " 状态更新失败" + str(remarks)
                # print (record)
                AdCost.update(State=3, remark=record).where(AdCost.id == id).execute()
                TrackingCampaign.update(remark=record).where(TrackingCampaign.id == ourcampid).execute()


update = UpdateState()
update.get_tasklist()
