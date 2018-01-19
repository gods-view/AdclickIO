# encoding=utf-8
import sys
import time
from datetime import datetime
from datetime import timedelta

#时间管理类
class DateManager:
    @classmethod
    def strtoint(cls, time_str, time_format='%Y-%m-%d %H:%M:%S'):
        tp = time.strptime(time_str, time_format)
        return int(time.mktime(tp))
    @classmethod
    def inttostr(cls, time_int, is_local=True, time_format='%Y-%m-%d %H:%M:%S'):
        if is_local:
            dt = datetime.fromtimestamp(time_int)
        else:
            dt = datetime.utcfromtimestamp(time_int)
        return dt.strftime(time_format)
    
    @classmethod
    def dtdeltatostr(cls, dt, hours=0, days=0, minutes=0, time_format='%Y-%m-%d %H:%M:%S'):
        return (dt+timedelta(hours=hours,days=days,minutes=minutes)).strftime(time_format)
    
    @classmethod
    def formatTimeStr(cls, time_str, time_format='%Y-%m-%dT%H:%M:%S+00:00', dest_format='%Y-%m-%d %H:%M:%S'):
        dt = datetime.strptime(time_str, time_format)
        return dt.strftime(dest_format)
    
    @classmethod
    def strtodt(cls, time_str, time_format='%Y-%m-%dT%H:%M:%S+00:00'):
        return datetime.strptime(time_str, time_format)
    
    @classmethod
    def strdeltatodt(cls, time_str, hours=0, days=0, time_format='%Y-%m-%dT%H:%M:%S+00:00'):
        return datetime.strptime(time_str, time_format) + timedelta(hours=hours, days=days)
    
    @classmethod
    def strdeltatoint(cls, time_str, hours=0, days=0, time_format='%Y-%m-%dT%H:%M:%S+00:00'):
        return  int(time.mktime( (datetime.strptime(time_str, time_format) + timedelta(hours=hours, days=days)).timetuple()))
    
    @classmethod
    def dtdeltatoint(cls, dt, hours=0, days=0):
        return int(time.mktime((dt+timedelta(hours=hours, days=days)).timetuple()))
    
    @classmethod
    def strdeltatostr(cls, time_str, hours=0, days=0, time_format='%Y-%m-%dT%H:%M:%S+00:00', dest_time_format='%Y-%m-%d %H:%M:%S'):
        return  (datetime.strptime(time_str, time_format) + timedelta(hours=hours, days=days)).strftime(dest_time_format)

    @classmethod
    #获取指定的某天是某个月中的第几周
    #周一作为一周的开始
    def getWeekOfMonth(cls, year, month, day):
        end = int(datetime(year, month, day).strftime("%W"))
        begin = int(datetime(year, month, 1).strftime("%W"))
        return end - begin + 1
 
    
 