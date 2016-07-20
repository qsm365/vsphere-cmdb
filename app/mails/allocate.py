# -*- coding:utf-8 -*-
from .. import projectview

def build(projectname,department,projecttype,amount,attachment,zone):
    ret = {}
    ret['title']=u'云平台资源申请审批通过，资源创建通知'
    ret['from'] = 1
    to = []
    to.append(1)
    ret['to'] = to
    cc = []
    cc.append(1)
    ret['cc'] = cc
    ret['attachment'] = attachment
    if str(projecttype)=='1':
        datacenter = ''
        if str(zone)=='4':
            datacenter = u'武汉运行中心'
        else:
            datacenter = u'上海运行中心'
        ret['content'] = u"<div>各位好，</div><div>"+department+projectname+"申请审批通过，评审结果：<span style='background:yellow;mso-highlight:yellow'>在"+projectview.zoneinfo_filter(zone)+"部署</span>；</div><div>请"+datacenter+"同事按附件配置云平台环境；</div><div>相关变更后续提交OA运维变更流程；</div><div>如有问题，请随时联系。</div>"
    elif str(projecttype)=='2':
        ret['content'] = u''
    return ret