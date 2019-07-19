#encoding=utf-8
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

from Config.ProjectVar import *

#发送邮件函数
def send_mail(attachement_file_path):

    #创建带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["hhq8286","286542822@qq.com"])
    message['To'] = ''.join(receivers)
    subject = "自动化测试报告"
    message['Subject'] = Header(subject,'utf-8')

    #邮件正文
    message.attach(MIMEText('最新执行的自动化测试报告，请参阅附件内容！', 'plain', 'utf-8'))

    #构造附件1，传送测试结果
    att = MIMEBase("application",'octet-stream')
    att.set_payload(open(attachement_file_path,"rb").read())
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "接口测试报告.html"))
    encoders.encode_base64(att)
    message.attach(att)
    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender,receivers,message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("发送邮件异常",e)

if __name__ == '__main__':
    print(mail_host)
    send_mail(test_data_file)


