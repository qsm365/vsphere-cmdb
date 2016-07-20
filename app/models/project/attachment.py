from sqlalchemy.sql import text
from app import db


def get_by_id(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select * from project_attachment where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def get_all():
    cmd = text("select * from project_attachment")
    result = db.engine.execute(cmd)
    return result


def get_by_projectid(projectid):
    parameters = {}
    parameters['projectid'] = projectid
    cmd = text("select * from project_attachment where projectid=:projectid")
    result = db.engine.execute(cmd, parameters)
    return result


def check_by_projectid(projectid):
    parameters = {}
    parameters['projectid'] = projectid
    cmd = text("select sum(case when type='1' then 1 else 0 end) t1,sum(case when type='2' then 1 else 0 end) t2 from project_attachment where projectid=:projectid")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def delete(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("delete from project_attachment where id=:id")
    result = db.engine.execute(cmd,parameters)
    return result


def add(projectid,projectname,filename,filetype):
    parameters = {}
    parameters['projectid'] = projectid
    parameters['projectname'] = projectname
    parameters['filename'] = filename
    parameters['filetype'] = filetype
    cmd = text("insert into project_attachment values(null,:projectid,:projectname,:filename,"
               "now(),:filetype)")
    result = db.engine.execute(cmd, parameters)
    return result