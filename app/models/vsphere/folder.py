from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_parent_id(ver,folderid):
    parameters = {}
    parameters['version'] = ver
    parameters['folderid'] = folderid
    sql = "select parentid from vsphere_folder where version=:version and folderid=:folderid"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    parentid=''
    rf = result.first()
    if rf:
        parentid=rf[0]
    return parentid

def get_by_folderid(ver,folderid):
    parameters = {}
    parameters['version'] = ver
    parameters['folderid'] = folderid
    cmd = text("select * from vsphere_folder where version=:version and folderid=:folderid")
    result = db.engine.execute(cmd, parameters)
    return result

def get_by_parentid(ver,parentid):
    parameters={}
    parameters['version']=ver
    parameters['parentid']=parentid
    cmd = text("select a.folderid,a.name,count(*) from (select * from vsphere_folder where version=:version) a left join (select * from vsphere_vm where version=:version) b on b.parentid=a.folderid where a.parentid=:parentid group by a.folderid,a.name")
    result = db.engine.execute(cmd,parameters)
    return result

def count_by_parentid(ver,parentid):
    parameters = {}
    parameters['version'] = ver
    parameters['parentid'] = parentid
    cmd = text("select count(*) from vsphere_folder where version=:version and parentid=:parentid")
    result = db.engine.execute(cmd, parameters)
    return result