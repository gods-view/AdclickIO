#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: t.py
@time: 2017/3/30 下午4:43
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# -*- coding:utf-8 -*-
from multiprocessing import Process,Pool
from ad_statis_new import doAdStatis
from reset import reset
from single_task import run_task
import os,time

def run_proc(name):        ##定义一个函数用于进程调用
    print ("=================",name,'python %s' % BASE_DIR+'affiliate/'+name+'.py')
    eval(name)()

if __name__ =='__main__': #执行主进程
    reset()
    task = ['run_task','doAdStatis']
    #print ('Run the main process (%s).' % (os.getpid()),len(task))
    mainStart = time.time() #记录主进程开始的时间
    p = Pool(len(task))           #开辟进程池
    for i in range(len(task)):                                 #开辟14个进程
        p.apply_async(run_proc,args=(task[i],))#每个进程都调用run_proc函数，
                                                        #args表示给该函数传递的参数。

    print ('Waiting for all subprocesses done ...')
    p.close() #关闭进程池
    p.join()  #等待开辟的所有进程执行完后，主进程才继续往下执行
    print ('All subprocesses done')
    #mainEnd = time.time()  #记录主进程结束时间
    #print ('All process ran %0.2f seconds.' % (mainEnd-mainStart))  #主进程执行时间
