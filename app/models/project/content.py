from sqlalchemy.sql import text
from app import db


def get_by_id(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select * from project_content where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def get_all():
    cmd = text("select * from project_content where state!='del'")
    result = db.engine.execute(cmd)
    return result


def delete(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("update project_content set state='del' where id=:id")
    result = db.engine.execute(cmd,parameters)
    return result


def add(name,departmentid,department,managerid,manager,projecttype,amount,endat):
    parameters = {}
    parameters['name'] = name
    parameters['departmentid'] = departmentid
    parameters['department'] = department
    parameters['managerid'] = managerid
    parameters['manager'] = manager
    parameters['type'] = projecttype
    parameters['amount'] = amount
    parameters['endat'] = endat
    cmd = text("insert into project_content values(null,:name,:departmentid,:department,"
               ":managerid,:manager,:type,:amount,'new',now(),:endat,null,null,null,null,"
               "null,null,null,null)")
    db.engine.execute(cmd, parameters)


def update(projectid,name, departmentid, department, managerid, manager, projecttype, amount, endat):
    parameters = {}
    parameters['id'] = projectid
    parameters['name'] = name
    parameters['departmentid'] = departmentid
    parameters['department'] = department
    parameters['managerid'] = managerid
    parameters['manager'] = manager
    parameters['type'] = projecttype
    parameters['amount'] = amount
    parameters['endat'] = endat
    cmd = text("update project_content set name=:name,departmentid=:departmentid,department=:department,"
               "managerid=:managerid,manager=:manager,type=:type,amount=:amount,endat=:endat "
               "where id=:id")
    db.engine.execute(cmd, parameters)


def check_precheck(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select precheck,zone from project_content where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def commit_precheck(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("update project_content set precheckat=now(),state='check' where id=:id")
    db.engine.execute(cmd, parameters)


def commit_approval(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("update project_content set approvalat=now(),state='approvaled' where id=:id")
    db.engine.execute(cmd, parameters)


def update_precheck(id,zone,prechecktext):
    parameters = {}
    parameters['id'] = id
    parameters['zone'] = zone
    parameters['precheck'] = prechecktext
    cmd = text("update project_content set zone=:zone,precheck=:precheck where id=:id")
    db.engine.execute(cmd, parameters)
