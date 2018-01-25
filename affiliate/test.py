#!/usr/bin/env python
# encoding: utf-8
import os
import sys,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from model.mysql_report import *
from common.mail import SendMail
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
import gc

class testClass:
    def doTest(self):
        num = 10
        totalRecoders = 0
        errNum = 0
        print ("start")
        Timestamp = int(time.time()) * 1000 - 3 * 60 * 60
        for i in range(num):
            reportDb.connect()             
            log = eval("AdStatisLog0")
            res = log.select(log.id).where(log.Timestamp > Timestamp).count()
            totalRecoders += 0#int(res)
            log = None
            print(res)
            gc.collect() 
            reportDb.close()
            errNum += 1

        if (errNum) >= 100:
            res = log.select(log.rid).where(log.Timestamp > Timestamp).count()

        #if (totalRecoders <= 0):
            
            #res,msg = SendMail().sendAlert()
            #print(res,msg)

        print("uuuuuuuuuuuu",totalRecoders)

def main():    
    while True:
        testClass().doTest()
        time.sleep(1)
        #break

if __name__ == "__main__": 
    reportDb.close()
    main()
