#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: reset.py
@time: 2017/3/31 下午4:03
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

task_status = {'new': 0, 'running': 1, 'error': 2, 'finish': 3}


def reset():
    print ("reset")
    from affiliate.model.mysql_model import OfferSyncTask
    from affiliate.common.helper import Helper
    OfferSyncTask.update(status=task_status['new']).where(OfferSyncTask.status == task_status['running'],
                                                          OfferSyncTask.deleted == 0,
                                                          OfferSyncTask.executor == Helper.get_mac_address()).execute()


if __name__ == '__main__':
    reset()
