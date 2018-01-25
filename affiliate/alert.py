#!/usr/bin/env python
# encoding: utf-8
import os
import sys,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from model.mysql_report import *
from common.mail import SendMail

def main():
    num = 10
    totalRecoders = 0
    Timestamp = int(time.time()) * 1000 - 3 * 60 * 1000
    for i in range(num):
        log = eval("AdStatisLog"+str(i))
        res = log.select().where(log.Timestamp > Timestamp).count()
        totalRecoders += int(res)
    print("totalRecoders:",totalRecoders)
    if (totalRecoders <= 0):
        res,msg = SendMail().sendAlert()
        print(res,msg)

if __name__ == "__main__": 
    main()
