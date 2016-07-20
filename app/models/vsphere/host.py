from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_by_hostid(ver,hostid):
    parameters = {}
    parameters['version'] = ver
    parameters['hostid'] = hostid
    cmd = text("select * from vsphere_host where version=:version and hostid=:hostid")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()

def get_info_by_parentid(ver,parentid):
    parameters = {}
    parameters['version'] = ver
    parameters['parentid'] = parentid
    cmd = text("select a.hostid,a.name,a.parentid,a.parent,a.cpu,a.memory,sum(case when b.vmid is not null then 1 else 0 end),sum(case when b.state='poweredOn' then b.cpu else 0 end),sum(case when b.state='poweredOn' then b.memory else 0 end) from (select * from vsphere_host where version=:version) a left join (select * from vsphere_vm where version=:version) b on a.hostid=b.hostid where a.parentid=:parentid group by a.hostid,a.name,a.parentid,a.parent,a.cpu,a.memory;")
    result = db.engine.execute(cmd, parameters)
    return result

def get_all_info(ver):
    parameters = {}
    parameters['version'] = ver
    cmd = text("select a.hostid,a.name,a.parentid,a.parent,a.cpu,a.memory,sum(case when b.vmid is not null then 1 else 0 end),sum(case when b.state='poweredOn' then b.cpu else 0 end),sum(case when b.state='poweredOn' then b.memory else 0 end) from (select * from vsphere_host where version=:version) a left join (select * from vsphere_vm where version=:version) b on a.hostid=b.hostid group by a.hostid,a.name,a.parentid,a.parent,a.cpu,a.memory;")
    result = db.engine.execute(cmd, parameters)
    return result