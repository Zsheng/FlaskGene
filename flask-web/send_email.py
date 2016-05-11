# -*- coding: UTF-8 -*-
'''
发送txt文本邮件
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

mailto_list = ['972212465@qq.com']
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "a869688975@163.com"  # 用户名
mail_pass = "123456aA"  # 口令
mail_postfix = "163.com"  # 发件箱的后缀


def send_mail(to_list, sub, content):
    me = "from张业生" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


def send_email2():
    sender = 'a869688975@163.com'
    receiver = '972212465@qq.com'
    # subject = 'python email test'
    # smtpserver = 'smtp.163.com'
    username = 'a869688975@163.com'
    password = '123456aA'

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'test'

    # 构造附件
    att = MIMEText(open('C:\\Users\\PC_yesheng.zhang\\Desktop\\python_web\\Flask_new_v3.11\\flask-web\\barcode\\145766727698z.png', 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="145766727698z.png"'
    msgRoot.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()


if __name__ == '__main__':
    info = "您的检测结果："
    if send_mail(mailto_list, "检测结果", info):
        print "发送成功"
    else:
        print "发送失败"

    # send_email2()
