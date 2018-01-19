#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: base_worker.py
@time: 2017/3/30 下午1:27
"""
from affiliate.model.mysql_model import ThirdPartyOffer, OfferSyncTask, ThirdPartyAffiliateNetwork, \
    TemplateAffiliateNetwork
from affiliate.common.helper import Helper


class BaseWorker:
    def __init__(self, taskId, userId, url, username, password, token=None):
        self.taskId = taskId
        self.userId = userId
        self.url = url
        self.username = username
        self.password = password
        self.token = token
        task = OfferSyncTask.get(id=self.taskId)
        login_info = ThirdPartyAffiliateNetwork.get(id=task.thirdPartyANId)
        tan = TemplateAffiliateNetwork.get(id=login_info.trustedANId)
        self.apiOfferAutoSuffix = tan.apiOfferAutoSuffix

    def delete_old_offers(self):
        ThirdPartyOffer.delete().where(ThirdPartyOffer.taskId == self.taskId).execute()

    def start(self):
        raise NotImplementedError

    def fix_tracklink_url(self, url):
        return Helper.fix_tracklink_url(url, self.apiOfferAutoSuffix)
