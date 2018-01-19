#!/usr/bin/env python
# encoding: utf-8

import os
import sys

import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import threading
import time
import traceback
import multiprocessing
from multiprocessing import cpu_count

from affiliate.common.helper import Helper
from affiliate.model.mysql_model import *
from affiliate.worker.yeahmobi import YeahmobiWork
from affiliate.worker.avazu import AvazuWork
from affiliate.worker.glispa import GlispaWork
from affiliate.worker.mobidea import MobideaWork
from affiliate.worker.clickdealer import ClickdealerWork

"""
YeahmobiWork,AvazuWork不能删除导入
"""
task_status = {'new': 0, 'running': 1, 'error': 2, 'finish': 3}


# os.getpid()
def run_task():
    print ("run_task")
    while True:
        # 获取一个任务
        task = OfferSyncTask.select().where(OfferSyncTask.status == task_status['new'],
                                            OfferSyncTask.deleted == 0).limit(1)
        # print("测试堵塞")
        if not task:  # 获取失败
            continue
        task = task[0]
        print (task.id)
        # 过滤该taskId正在运行的其他冲突项
        try:  # 尝试占用任务
            ret = OfferSyncTask.update(status=task_status['running'], executor=Helper.get_mac_address()). \
                where(OfferSyncTask.id == task.id,
                      OfferSyncTask.status == task_status['new'],
                      OfferSyncTask.deleted == 0).execute()
            # print (ret)
            if not ret:  # 没有更新成功
                print ("没有更新成功")
                # raise Exception('error')
        except Exception as e:  # 占用失败
            print (e)
            continue
        try:  # 执行任务
            with db.atomic():
                OfferSyncTask.update(startedAt=int(time.time()), status=1). \
                    where(OfferSyncTask.id == task.id,
                          OfferSyncTask.status == task_status['running'],
                          OfferSyncTask.deleted == 0).execute()
                login_info = ThirdPartyAffiliateNetwork.get(id=task.thirdPartyANId)
                tan = TemplateAffiliateNetwork.get(id=login_info.trustedANId)

                # if tan.name in ['Avazu']:
                if tan.name in ['Avazu', 'Yeahmobi', 'Mobidea', 'Clickdealer', 'Cake']:
                    globals()[tan.name + 'Work'](taskId=task.id,
                                                 userId=task.userId,
                                                 url=tan.apiUrl,
                                                 username=login_info.userName,
                                                 password=login_info.password).start()
                elif tan.name in ['Glispa']:
                    globals()[tan.name + 'Work'](taskId=task.id,
                                                 userId=task.userId,
                                                 url=tan.apiUrl,
                                                 token=login_info.token).start()
                else:
                    raise Exception('this Affiliate does not support right now')
                # 执行任务完成
                ret = OfferSyncTask.update(endedAt=int(time.time()), message='success', status=task_status['finish']). \
                    where(OfferSyncTask.id == task.id,
                          OfferSyncTask.status == task_status['running'],
                          OfferSyncTask.deleted == 0).execute()
                if not ret:
                    raise Exception('error')
        except Exception as e:  # 执行任务失败
            print(e)
            OfferSyncTask.update(status=task_status['error'], message='access error'). \
                where(OfferSyncTask.id == task.id,
                      OfferSyncTask.status == task_status['running'],
                      OfferSyncTask.deleted == 0).execute()
            with open('mylog.log', 'a') as f:
                from datetime import datetime
                f.write('%s \n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                traceback.print_exc(file=f)
                f.write('\n')
            continue


# def reset():
#     OfferSyncTask.update(status=task_status['new']).where(OfferSyncTask.status == task_status['running'],
#                                                           OfferSyncTask.deleted == 0,
#                                                           OfferSyncTask.executor == Helper.get_mac_address()).execute()


if __name__ == '__main__':
    # reset()
    run_task()
