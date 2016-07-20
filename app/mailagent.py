# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

mail_host="mail.chinaums.com"  #设置服务器
mail_user="smqiu"    #用户名
mail_pass="Rsrz1rm!"   #口令
mail_postfix="chinaums.com"  #发件箱的后缀
fromheader = Header(u"裘思明", 'utf-8')
fromheader.append("<smqiu@chinaums.com>", 'ascii')

def make_msg(msgtype,sub,content):
    msg = MIMEMultipart()
    textmsg = MIMEText(content, _subtype=msgtype, _charset='utf-8')
    msg['Subject'] = sub
    msg.attach(textmsg)
    return msg

def add_attache(msg,attache_path):
    att = MIMEText(open(attache_path, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="测试附件.txt"'
    msg.attach(att)
    return msg

def send_mail(tolist,cclist,msg):
    msg['From'] = fromheader
    tos = []
    ccs = []
    list_tomail = []
    list_ccmail = []
    for t in tolist:
        toheader = Header(t[0], 'utf-8')
        toheader.append("<" + t[1] + ">", 'ascii')
        tos.append(str(toheader))
        list_tomail.append(t[1])
    msg['To'] = ';'.join(tos)
    for c in cclist:
        ccheader = Header(t[0],'utf-8')
        ccheader.append("<" + c[1] + ">",'ascii')
        ccs.append(str(ccheader))
        list_ccmail.append(c[1])
    msg['CC'] = ';'.join(ccs)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(str(fromheader), list_tomail, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def make_to_header(tolist):
    ret = []
    for t in tolist:
        toheader = Header(t[0], 'utf-8')
        toheader.append("<" + t[1] + ">", 'ascii')
        ret.append(toheader)
    return  ret

if __name__ == '__main__':
    l = []
    #l.append([u'思明','smqiu@chinaums.com'])
    l.append([u'裘思明','qsm365@qq.com'])
    content=u"<div>各位好，</div><div>&nbsp;</div><div>福建分公司在OA上提交了孵化区资源申请，申请1台服务器部署福建代付平台。</div><div>具体需求及服务器配置见附件，请各位评估一下部署的可行性，OA流程已提交专家委员会评审，如有问题，请随时联系。</div><div>&nbsp;</div>"
    #msg = make_msg('plain',"这是一封测试邮件","中文测试")
    title=u"这是一封测试邮件"
    if not isinstance(title, unicode):
        title = unicode(title)
    msg = make_msg('html',title,content)
    msg = add_attache(msg,u'D:\\测试附件.txt')
    if send_mail(l,l,msg):
        print "发送成功"
    else:
        print "发送失败"