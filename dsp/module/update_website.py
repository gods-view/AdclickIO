import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print (BASE_DIR)
sys.path.append(BASE_DIR + "/../")
from affiliate.model.mysql_model import WebsiteId
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
        filter_list = ['#', '[', ']', '{', '}', '%', '@']
        while True:
            # task_list = WebsiteId.select().where(
            #     WebsiteId.state == 0)
            # # print (len(task_list), task_list)
            # for task in task_list:
            #     # print ("遍历更新")
            #     # print (task.campaignId, task.web_site_id, task.TrafficSourceId)
            #     theircamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
            #         CampaignMap.OurCampId == task.campaignId)
            #     for theircampain in theircamplist:
            #         # print (task.campaignId)
            #         self.update_state(task, theircampain.TheirCampId)
            #         # self.update_cost(task)
            task_list = WebsiteId.select().where(WebsiteId.state == 0).group_by(WebsiteId.campaignId, WebsiteId.status,
                                                                                WebsiteId.TrafficSourceId)

            for task in task_list:
                # print ("遍历更新")
                # website_list = []
                website_list = ""
                id_list = []
                websites = WebsiteId.select().where(WebsiteId.status == task.status,
                                                    WebsiteId.campaignId == task.campaignId,
                                                    WebsiteId.TrafficSourceId == task.TrafficSourceId,
                                                    WebsiteId.state == 0)
                for website in websites:
                    # website_list.append(website.web_site_id.replace("\r", ""))
                    temp_list = []
                    [temp_list.append(websiteid) for item in filter_list if websiteid.find(item) > -1]
                    if len(temp_list) > 0 or websiteid.lower() == 'unknown':
                        continue
                    website_list += website.web_site_id.replace("\r", "") + ","
                    id_list.append(website.id)
                # print (task.campaignId, task.web_site_id, task.TrafficSourceId)
                theircamplist = CampaignMap.select(CampaignMap.OurCampId, CampaignMap.TheirCampId).where(
                    CampaignMap.OurCampId == task.campaignId)
                print (website_list[:-1])
                for theircampain in theircamplist:
                    # print (task.campaignId)
                    self.update_state(task, theircampain.TheirCampId, website_list[:-1], id_list)

    def update_state(self, task, theircampid, website_list, id_list):
        # print ("查找并更新")
        result = ""
        ourcampid = task.campaignId
        # theircampid = task.CampaignID
        id = id_list
        status = task.status
        TrafficsourceId = task.TrafficSourceId
        # websiteid = task.web_site_id.replace("\r", "")
        websiteid = website_list
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
            # print (theircampid, websiteid)
            if TemplateTraffic.name == "MGID.com":
                try:
                    # print ("MGID.com")
                    token = trafficsource.token
                    mgid = Mgid(token)
                    mgid.login(username, password)
                    if status == 1:
                        result, remarks = mgid.play_widgets(theircampid, websiteid)
                    else:
                        result, remarks = mgid.block_widgets(theircampid, websiteid)
                        # print (status)
                        # print (theircampid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "PopCash.net":
                try:
                    # print ("begin")
                    # print ("PopCash.net")
                    popcash = PopCash(token)
                    # print ("popcash")
                    # print (theircampid, status)
                    operate = 2 if status == 1 else 1
                    result, remarks = popcash.website_switch(theircampid, operate, websiteid)
                except:
                    raise Exception('error')
            # elif TemplateTraffic.name == "popads.net":
            #     try:
            #         popad = Popad(username, password, token)
            #         popad.login()
            #         if status == 1:
            #             result, remarks = popad.play_campaigns(theircampid)
            #         else:
            #             result, remarks = popad.pause_campaigns(theircampid)
            #     except:
            #         raise Exception('error')
            elif TemplateTraffic.name == "RevContent.com":
                try:
                    # print ("RevContent.com")
                    revcontent = Revcontent(username, password)
                    revcontent.login()
                    if status == 1:
                        result, remarks = revcontent.add_widget(theircampid, "include", websiteid)
                    else:
                        result, remarks = revcontent.remove_widget(theircampid, "exclude", websiteid)
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "ZeroPark.com":
                try:
                    # print ("ZeroPark.com")
                    zeropark = Zeropark(token)
                    # zeropark.login()
                    if status == 1:
                        result, remarks = zeropark.resume_targets(theircampid, websiteid.split(','))
                    else:
                        result, remarks = zeropark.pause_targets(theircampid, websiteid.split(','))
                except:
                    raise Exception('error')
            elif TemplateTraffic.name == "ExoClick.com":
                try:
                    # print ("ExoClick.com")
                    exoclick = ExoClick(username, password, token)
                    exoclick.login()
                    if status == 1:
                        result, remarks = exoclick.update_zone(theircampid, "targeted", websiteid.split(','))
                    else:
                        result, remarks = exoclick.update_zone(theircampid, "blocked", websiteid.split(','))
                except:
                    raise Exception('error')
            # print (result)
            if result == "":
                return
            if result:
                record = str(status) + " 状态更新成功" + str(remarks)
                # print (record)
                WebsiteId.update(state=2, remark=record, status=status).where(WebsiteId.id << id).execute()
            else:
                # print (remarks)
                if status == 1:
                    record = str(status) + " 状态更新失败" + str(remarks)
                    WebsiteId.update(state=3, remark=record, status=0).where(WebsiteId.id << id).execute()
                else:
                    record = str(status) + " 状态更新失败" + str(remarks)
                    WebsiteId.update(state=3, remark=record, status=1).where(WebsiteId.id << id).execute()


if __name__ == '__main__':
    # print ('123,234'.split(','))
    update = UpdateState()
    update.get_tasklist()
