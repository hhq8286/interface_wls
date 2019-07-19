# -*- coding : utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import  traceback
import os

class Mail(object):

    def __init__(self,mail_host,mail_user,mail_passwd,sender):
        '''
        :param mail_host: 邮件服务器
        :param mail_user: 发件邮箱的用户名
        :param mail_passwd: 发件邮箱的授权码
        :param sender: 发件箱地址
        '''
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_passwd = mail_passwd
        self.sender = sender

    def send_mail(self,receivers,subject,send_content,attachment_file_path):
        """

        :param receivers:收件人列表,可以同时发送多人，此处传入的是一个列表
        :param subject:邮件主题
        :param send_content:邮件内容
        :param attachment_file_path: 需要发送的附件路径
        :return:
        """
        #创建一个带附件的实例
        message = MIMEMultipart()
        #设置发件人别名
        message["From"] = Header(self.sender,"utf-8")
        #设置收件人别名
        message["To"] = Header("myself")
        #设置邮件主题
        message["Subject"] = Header(subject,"utf-8")

        #设置邮件正文
        message.attach(MIMEText(send_content,"plain","utf-8"))

        #构造发送的附件
        #需要以二进制读模式打开,非文本文件用MIMEApplication
        #文本文件用MIMEText
        # att = MIMEText(open('1.txt', 'rb').read(), 'base64', 'utf-8')
        att = MIMEApplication(open(attachment_file_path,"rb").read())
        #指定发送附件的文件名称
        file_name = os.path.split(attachment_file_path)[1]
        att.add_header('Content-Disposition','attachment',filename=file_name)

        #设置附件
        message.attach(att)
        # 开始发送邮件
        try:
            #创建SMTP实例
            smtpObj = smtplib.SMTP()
            #连接邮件服务器，此处为qq邮件服务器
            #25为SMTP端口号
            smtpObj.connect(self.mail_host,25)
            #登录邮件服务器
            smtpObj.login(self.mail_user,self.mail_passwd)
            #发送邮件
            smtpObj.sendmail(self.sender,receivers,message.as_string())
            print("邮件发送成功！")
        except smtplib.SMTPException as e:
            traceback.print_exc()
            print("发送邮件出错")
            raise e

if __name__ == "__main__":
    mail = Mail("smtp.qq.com","286542822@qq.com","dsssmsrpvbuecaac","286542822@qq.com")
    receivers = ["hhq8286@163.com","286542822@qq.com"]
    mail.send_mail(receivers,"自动化测试结果","自动化测试结果","e:\\1.txt")
