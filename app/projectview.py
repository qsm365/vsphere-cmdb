# -*- coding:utf-8 -*-

from flask import request,Blueprint,render_template,session,redirect,url_for,send_file,jsonify,make_response
from . import app
import projectbusiness,mailagent
import os
from urllib import quote
import HTMLParser

html_parser = HTMLParser.HTMLParser()

projectprofile = Blueprint('projectprofile', __name__)


@app.route('/project/test', methods = ['GET', 'POST'])
def projecttest():
    return "OK",200


@app.route('/project/file/upload', methods=['GET', 'POST', 'DELETE'])
def project_file_upload():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method=='GET':
        projectid = request.args.get('projectid')
        projectname = request.args.get('projectname')
        return render_template('project/project_file_upload.html', title='Upload File',projectid=projectid,
                               projectname=projectname)
    elif request.method=='POST':
        projectid = request.form.get('projectid')
        projectname = request.form.get('projectname')
        filetype = request.form.get('filetype')
        f = request.files['file']
        ret = projectbusiness.upload_attachment(projectid,projectname,f,filetype)
        fileid = ret['fileid']
        filename = ret['filename']
        addtime = ret['addtime']
        return render_template('project/project_file_uploaded.html', title='File Uploaded',fileid=fileid,
                               filename=filename,filetype=filetype,addtime=addtime)
    elif request.method=='DELETE':
        fileid = request.args.get('fileid')
        if projectbusiness.del_attachment(fileid):
            return "ok",200
        else:
            return "not found",404


@app.route('/project/file/download',methods=['GET'])
def project_file_download():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        fileid = request.args.get('fileid')
        if fileid:
            fileinfo = projectbusiness.get_attachment(fileid)
            response = make_response(send_file(os.path.join(app.config['ATTACHMENTPATH'],str(fileid))))
            realfilename = fileinfo[3].encode("utf-8")
            realfilenameurlencode = quote(realfilename)
            response.headers["Content-Disposition"] = "attachment; filename="+realfilenameurlencode+";"
            return response


@app.route('/project/mail/send',methods = ['GET','POST'])
def project_mail_send():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        fromer = mailagent.fromheader
        tolist = []
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        tolist.append([u'思明', 'smqiu@chinaums.com'])
        toer = mailagent.make_to_header(tolist)
        subject = u"这是一封测试邮件"
        content = u"<div>各位好，</div><div>&nbsp;</div><div>福建分公司在OA上提交了孵化区资源申请，申请1台服务器部署福建代付平台。</div><div>具体需求及服务器配置见附件，请各位评估一下部署的可行性，OA流程已提交专家委员会评审，如有问题，请随时联系。</div><div>&nbsp;</div>"
        return render_template('project/project_mail_send.html', title='Send Mail', fromer = fromer, toer = toer,
                               subject = subject, content = content)
    elif request.method == 'POST':
        return "ok",200


@app.route('/project/contacts/edit',methods = ['GET','POST','DELETE'])
def project_contacts_edit():
    if not session.get('username'):
        return redirect(url_for('login'))
    contactsid = request.args.get('id')
    if contactsid:
        if request.method == 'GET':
            department_list = projectbusiness.get_all_department()
            contactsinfo = projectbusiness.get_contacts(contactsid)
            return render_template('project/project_contacts_edit.html', title='Edit Contacts',
                                   department_list=department_list, contactsinfo=contactsinfo)
        if request.method == 'POST':
            name = request.form.get('name')
            departmentid = request.form.get('departmentid')
            email = request.form.get('email')
            phone = request.form.get('phone')
            qq = request.form.get('qq')
            projectbusiness.edit_contacts(contactsid,name,departmentid,email,phone,qq)
            return "ok",200
        if request.method == 'DELETE':
            projectbusiness.del_contacts(contactsid)
            return "ok",200
    return redirect(url_for('project_contacts_list'))


@app.route('/project/department/edit',methods = ['GET','POST','DELETE'])
def project_department_edit():
    if not session.get('username'):
        return redirect(url_for('login'))
    departmentid = request.args.get('id')
    if departmentid:
        if request.method == 'GET':
            contacts_list = projectbusiness.get_all_contacts().fetchall()
            departmentinfo = projectbusiness.get_department(departmentid)
            return render_template('project/project_department_edit.html', title='Edit Department',
                                   contacts_list=contacts_list, departmentinfo=departmentinfo)
        elif request.method == 'POST':
            departmentname=request.form.get('name')
            leader1=request.form.get('leader1')
            leader2=request.form.get('leader2')
            projectbusiness.edit_department(departmentid,departmentname,leader1,leader2)
            return "ok",200
        elif request.method == 'DELETE':
            projectbusiness.del_department(departmentid)
            return "ok",200
    return redirect(url_for('project_department_list'))


@app.route('/project/add',methods = ['GET','POST'])
def project_add():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        department_list = projectbusiness.get_all_department()
        return render_template('project/project_content_add.html', title='Add Project',
                               department_list=department_list)
    elif request.method == 'POST':
        name = request.form.get('name')
        departmentid = request.form.get('departmentid')
        managerid = request.form.get('managerid')
        projecttype = request.form.get('projecttype')
        amount = request.form.get('amount')
        enddate = request.form.get('enddate')
        if enddate:
            projectbusiness.add_content(name, departmentid, managerid, projecttype, amount, enddate)
        else:
            projectbusiness.add_content(name, departmentid, managerid, projecttype, amount, None)
        return 'ok', 200


@app.route('/project/department/add', methods=['GET', 'POST'])
def project_department_add():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('project/project_department_add.html', title='Add Department')
    elif request.method == 'POST':
        department_name = request.form.get('name')
        projectbusiness.add_department(department_name)
        return 'ok',200


@app.route('/project/contacts/add', methods = ['GET','POST'])
def project_contacts_add():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        department_list = projectbusiness.get_all_department()
        return render_template('project/project_contacts_add.html', title='Add Contacts',
                               department_list=department_list)
    elif request.method == 'POST':
        name = request.form.get('name')
        departmentid = request.form.get('departmentid')
        email = request.form.get('email')
        phone = request.form.get('phone')
        qq = request.form.get('qq')
        projectbusiness.add_contacts(name,departmentid,email,phone,qq)
        return 'ok',200


@app.route('/project/',methods=['GET'])
def project_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    content_list = projectbusiness.get_all_content()
    return render_template('project/project_content_list.html', title='Project List',
                           content_list=content_list)


@app.route('/project/mail',methods=['GET'])
def project_mail_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    mail_list = projectbusiness.get_all_mail()
    return render_template('project/project_mail_list.html', title='Mail List',
                           mail_list=mail_list)

@app.route('/project/department', methods=['GET'])
def project_department_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    departmentlist = projectbusiness.get_all_department()
    return render_template('project/project_department_list.html', title='Department List',
                           departmentlist=departmentlist)


@app.route('/project/contacts', methods=['GET'])
def project_contacts_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    contactslist = projectbusiness.get_all_contacts()
    return render_template('project/project_contacts_list.html', title='Contacts List', contactslist=contactslist)


@app.route('/project/edit',methods=['GET','POST'])
def project_edit():
    if not session.get('username'):
        return redirect(url_for('login'))
    projectid = request.args.get('id')
    if projectid:
        if request.method == 'GET':
            content = projectbusiness.get_content(projectid)
            department_list = projectbusiness.get_all_department()
            return render_template('project/project_content_edit.html', title='Add Project',
                           department_list=department_list,content=content)
        elif request.method == 'POST':
            name = request.form.get('name')
            departmentid = request.form.get('departmentid')
            managerid = request.form.get('managerid')
            projecttype = request.form.get('projecttype')
            amount = request.form.get('amount')
            enddate = request.form.get('enddate')
            if enddate:
                projectbusiness.edit_content(projectid, name, departmentid, managerid, projecttype, amount, enddate)
            else:
                projectbusiness.edit_content(projectid, name, departmentid, managerid, projecttype, amount, None)
            return 'ok', 200
    return redirect(url_for('project_list'))

@app.route('/project/detail', methods=['GET','DELETE','POST'])
def project_detail():
    if not session.get('username'):
        return redirect(url_for('login'))
    projectid = request.args.get('id')
    if projectid:
        if request.method=='GET':
            content = projectbusiness.get_content(projectid)
            attachments = projectbusiness.get_attachmentlist_by_projectid(projectid).fetchall()
            return render_template('project/project_content_detail.html', title='Project Detail',
                                   content=content,attachments=attachments)
        elif request.method=='DELETE':
            projectbusiness.del_content(projectid)
            return 'ok',200
        elif request.method=='POST':
            operation = request.form.get('operation')
            if operation:
                if operation=='commitprecheck':
                    c = projectbusiness.check_precheck(projectid)
                    if c!='ok':
                        return c, 500
                    else:
                        ret = projectbusiness.commit_content_precheck(projectid)
                        return ret,200
                elif operation=='editprecheck':
                    zone = request.form.get('zone')
                    text = request.form.get('text')
                    projectbusiness.edit_content_precheck(projectid, zone, text)
                    return 'ok', 200
            else:
                return "bad request",401
    return redirect(url_for('project_list'))


@app.route('/project/contacts/json', methods=['POST'])
def project_find_contacts_json():
    if not session.get('username'):
        return redirect(url_for('login'))
    departmentid = request.form.get('departmentid')
    contacts_list = projectbusiness.find_contacts_by_departmentid(departmentid)
    return jsonify({'contacts_list': contacts_list})


@app.template_filter('filetype')
def filetype_filter(s):
    if str(s)=='1':
        return u'资源申请表'
    elif str(s)=='2':
        return u'资源清单'
    else:
        return '-'


@app.template_filter('zoneinfo')
def zoneinfo_filter(s):
    if str(s)=='1':
        return u'上海创新区'
    elif str(s)=='2':
        return u'上海孵化区'
    elif str(s)=='3':
        return u'上海测试区'
    elif str(s)=='4':
        return u'武汉区'
    else:
        return '-'


@app.template_filter('htmlparser')
def html_parser_filter(s):
    return html_parser.unescape(s)


@app.template_filter('stateinfo')
def stateinfo_filter(s):
    if s == 'new':
        return u'初审中'
    elif s == 'check':
        return u'审核中'
    else:
        return '-'


@app.template_filter('projecttypeinfo')
def projecttypeinfo(s):
    if str(s) == '1':
        return u'新建资源'
    elif str(s) == '2':
        return u'扩容资源'
    else:
        return '-'