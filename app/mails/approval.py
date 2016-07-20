# -*- coding:utf-8 -*-

def build(projectname,department,projecttype,amount,attachments):
    ret = {}
    ret['title']=department+u'“'+projectname+u'”云平台资源申请，请各位评审'
    ret['from'] = '1'
    to = []
    to.append('1')
    ret['to'] = to
    cc = []
    cc.append('1')
    ret['cc'] = cc
    atts = []
    for att in attachments:
        atts.append(str(att.id))
    ret['attachment'] = atts
    if str(projecttype)=='1':
        ret['content'] = u'<div>各位好，</div><div>&nbsp;</div><div>' + department + u'在OA上提交了孵化区资源申请，申请' + \
                         str(amount) + u'台服务器部署' + projectname + u'。</div><div>具体需求及服务器配置见附件，请各位评估一下部署的可行性，OA流程已提交专家委员会评审，如有问题，请随时联系。</div><div>&nbsp;</div>'
    elif str(projecttype)=='2':
        ret['content'] = u''
    return ret