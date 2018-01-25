#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,time

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
 
class SendMail:
    def sendAlert(self,title = 'Python 邮件发送测试...',subject = 'Python SMTP 邮件测试'):
        my_sender='13564726058@139.com' #发件人邮箱账号，为了后面易于维护，所以写成了变量
        my_user=['444502223@qq.com','849878006@qq.com'] #收件人邮箱账号，为了后面易于维护，所以写成了变量

        msg = MIMEText('Dashboard数据3分钟未更新，请检查','plain','utf-8')
        msg['From'] = formataddr(["发件人邮箱昵称",my_sender])  #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人邮箱昵称","admin"])  #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Dashboard数据异常" #邮件的主题，也可以说是标题
        try: 
            server=smtplib.SMTP("smtp.139.com",25) #发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender,"wudi2010")  #括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, my_user, msg.as_string())  #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  #这句是关闭连接的意思
            return True,"邮件发送成功"
        except smtplib.SMTPException:
            return False,'无法发送邮件'
