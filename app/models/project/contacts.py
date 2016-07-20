from sqlalchemy.sql import text
from app import db


def get_by_id(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select * from project_contacts where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def get_all():
    cmd = text("select * from project_contacts")
    result = db.engine.execute(cmd)
    return result


def find_by_departmentid(departmentid):
    parameters = {}
    parameters['departmentid'] = departmentid
    cmd = text("select * from project_contacts where departmentid=:departmentid")
    result = db.engine.execute(cmd, parameters)
    return result


def delete(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("delete from project_contacts where id=:id")
    result = db.engine.execute(cmd, parameters)


def add(name,departmentid,department,phone,email,qq):
    parameters = {}
    parameters['name'] = name
    parameters['departmentid'] = departmentid
    parameters['department'] = department
    parameters['phone'] = phone
    parameters['email'] = email
    parameters['qq'] = qq
    cmd = text("insert into project_contacts values(null,:name,:departmentid,:department,:phone,:email,:qq)")
    result = db.engine.execute(cmd, parameters)


def update(id,name,departmentid,department,phone,email,qq):
    parameters = {}
    parameters['id'] = id
    parameters['name'] = name
    parameters['departmentid'] = departmentid
    parameters['department'] = department
    parameters['phone'] = phone
    parameters['email'] = email
    parameters['qq'] = qq
    cmd = text("update project_contacts set name=:name,departmentid=:departmentid,department=:department,"
               "phone=:phone,email=:email,qq=:qq where id=:id")
    result = db.engine.execute(cmd, parameters)