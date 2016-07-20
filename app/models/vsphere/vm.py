from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_by_vmid(ver,vmid):
    parameters = {}
    parameters['version'] = ver
    parameters['vmid'] = vmid
    cmd = text("select * from vsphere_vm where version=:version and vmid=:vmid")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()

def get_parent_id(ver,vmid):
    parameters = {}
    parameters['version'] = ver
    parameters['vmid'] = vmid
    sql = "select parentid from vsphere_vm where version=:version and vmid=:vmid"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    parentid=''
    rf = result.first()
    if rf:
        parentid=rf[0]
    return parentid

def get_by_parentid(ver,parentid):
    parameters={}
    parameters['version']=ver
    parameters['parentid']=parentid
    sql="select * from vsphere_vm where version=:version and parentid=:parentid"
    cmd = text(sql)
    result = db.engine.execute(cmd,parameters)
    return result

def get_info_by_vmids(ver,vmids):
    parameters={}
    parameters['version']=ver
    sql="select c.vmname,c.vmid,c.projectname,c.projectid,d.name as zonename,d.folderid as zoneid from (select a.name as vmname,a.vmid,b.parentid as zoneid,b.name as projectname,b.folderid as projectid from (select * from vsphere_vm where version=:version) a left join (select * from vsphere_folder where version=:version) b on a.parentid=b.folderid where a.vmid in ("
    vid=0
    for vmid in vmids:
        parameters[str(vid)] = vmid
        sql = sql + ":" + str(vid) + ","
        vid = vid + 1
    sql=sql+"'')) c left join (select * from vsphere_folder where version=:version) d on c.zoneid=d.folderid"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    return result

def get_vm_by_hostid(ver,hostid):
    parameters = {}
    parameters['version']=ver
    parameters['hostid']=hostid
    sql="select * from vsphere_vm where version=:version and hostid=:hostid"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    return result

'''
def count_by_parentid(ver,parentids):
    parameters={}
    parameters['version']=ver
    sql="select count(*) from vsphere_vm where version=:version and parentid in ("
    pid=0
    for parentid in parentids:
        parameters[str(pid)]=parentid
        sql=sql+":"+str(pid)+","
        pid=pid+1
    sql=sql+"'')"
    cmd = text(sql)
    result = db.engine.execute(cmd,parameters)
    return result
'''