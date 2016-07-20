from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_all(ver):
    parameters={}
    parameters['version']=ver
    sql="select * from vsphere_network where version=:version"
    cmd = text(sql)
    result = db.engine.execute(cmd,parameters)
    return result

def get_all_info(ver):
    parameters = {}
    parameters['version'] = ver
    sql = "select a.networkid,a.name,a.networktype,count(*) as count from (select * from vsphere_network where version=:version) a left join (select * from vsphere_vmnic where version=:version) b on a.networkid=b.network group by a.networkid,name,networktype"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    return result

def get_by_networkid(ver,folderid):
    parameters = {}
    parameters['version'] = ver
    parameters['folderid'] = folderid
    cmd = text("select * from vsphere_network where version=:version and networkid=:folderid")
    result = db.engine.execute(cmd, parameters)
    return result