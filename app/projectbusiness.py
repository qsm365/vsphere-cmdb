# -*- coding:utf-8 -*-
from app.models.project import contacts,department,content,attachment,mail
from . import app
import os
import datetime
from mails import approval

attachmentpath=app.config['ATTACHMENTPATH']


def get_all_contacts():
    return contacts.get_all()


def get_all_department():
    return department.get_all()


def get_all_content():
    return content.get_all()


def get_all_mail():
    return mail.get_all()


def get_content(id):
    return content.get_by_id(id)


def get_department(id):
    return department.get_by_id(id)


def get_contacts(id):
    return contacts.get_by_id(id)


def del_content(id):
    content.delete(id)


def del_department(id):
    department.delete(id)


def del_contacts(id):
    contacts.delete(id)


def add_contacts(name,departmentid,email,phone,qq):
    dep = department.get_by_id(departmentid)
    if dep:
        try:
            contacts.add(name,departmentid,dep[1],phone,email,qq)
        except Exception, e:
            print e


def add_department(name):
    try:
        department.add(name)
    except Exception, e:
        print e


def add_content(name,departmentid,managerid,projecttype,amount,endat):
    dep = department.get_by_id(departmentid)
    mgr = contacts.get_by_id(managerid)
    try:
        content.add(name,departmentid,dep[1],managerid,mgr[1],projecttype,amount,endat)
    except Exception, e:
        print e


def edit_content(projectid,name,departmentid,managerid,projecttype,amount,endat):
    dep = department.get_by_id(departmentid)
    mgr = contacts.get_by_id(managerid)
    try:
        content.update(projectid,name, departmentid, dep[1], managerid, mgr[1], projecttype, amount, endat)
    except Exception, e:
        print e


def check_precheck(projectid):
    try:
        c1 = content.check_precheck(projectid)
        if c1:
            if not c1.precheck or not c1.zone:
                return "noprecheck"
        c2 = attachment.check_by_projectid(projectid)
        if c2:
            if c2.t1==0 or c2.t2==0:
                return "noattach"
        return "ok"
    except Exception, e:
        print e


def commit_content_precheck(projectid):
    #try:
        content.commit_precheck(projectid)
        p = content.get_by_id(projectid)
        atts = attachment.get_by_projectid(projectid)
        approvalmail = approval.build(p.name,p.department,p.type,p.amount,atts)
        print approvalmail
        mail.create(p.id,p.name,'1',approvalmail)
        return str(datetime.datetime.now())[0:10]
    #except Exception, e:
    #    print e


def edit_content_precheck(projectid,zone,text):
    try:
        content.update_precheck(projectid,zone,text)
    except Exception, e:
        print e


def edit_department(id,name,leader1,leader2):
    try:
        department.update(id,name,leader1,leader2)
    except Exception, e:
        print e


def edit_contacts(id,name,departmentid,email,phone,qq):
    dep = department.get_by_id(departmentid)
    if dep:
        try:
            contacts.update(id,name, departmentid, dep[1], phone, email, qq)
        except:
            print "edit_contacts error"


def find_contacts_by_departmentid(departmentid):
    contacts_list = contacts.find_by_departmentid(departmentid)
    ret=[]
    for c in contacts_list:
        cont={}
        cont['contacts_id']=c[0]
        cont['contacts_name']=c[1]
        ret.append(cont)
    return ret


def upload_attachment(projectid,projectname,file,filetype):
    try:
        filename = file.filename
        re = attachment.add(projectid,projectname,filename,filetype)
        fileid = re.lastrowid
        file.save(os.path.join(attachmentpath,str(fileid)))
        ret = {}
        ret['fileid'] = fileid
        ret['filename'] = filename
        ret['addtime'] = str(datetime.datetime.now())[0:19]
        return ret
    except Exception,e:
        print e


def del_attachment(fileid):
    try:
        print os.path.join(attachmentpath,str(fileid))
        os.remove(os.path.join(attachmentpath,str(fileid)))
        attachment.delete(fileid)
        return True
    except Exception, e:
        print e


def get_attachmentlist_by_projectid(projectid):
    return attachment.get_by_projectid(projectid)


def get_attachment(fileid):
    ret = attachment.get_by_id(fileid)
    return ret