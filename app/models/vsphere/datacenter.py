from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_all(ver):
    parameters={}
    parameters['version']=ver
    cmd = text("select * from vsphere_datacenter where version=:version")
    result = db.engine.execute(cmd,parameters)
    return result

def get_project_map_by_dcid(ver,dcid):
    parameters={}
    parameters['version']=ver
    parameters['dcid']=dcid
    cmd = text("select e.name as datacentername,e.zonename,e.zoneid,f.name as projectname,f.folderid as projectid from (select c.*,d.name as zonename,d.folderid as zoneid from (select a.name,a.id as datacenterid,b.folderid as vmfolderid from (select * from vsphere_datacenter where version=:version) a left join (select * from vsphere_datacenter_folder where version=:version) b on a.id=b.datacenterid where a.id=:dcid) c left join (select * from vsphere_folder where version=:version) d on vmfolderid=d.parentid) e left join (select * from vsphere_folder where version=:version) f on e.zoneid=f.parentid")
    result = db.engine.execute(cmd, parameters)
    return result

def get_vm_map_by_dcid(ver,dcid):
    parameters = {}
    parameters['version'] = ver
    parameters['dcid'] = dcid
    cmd = text("select g.*,h.name,h.vmid from (select e.name as datacentername,e.zonename,e.zoneid,f.name as projectname,f.folderid as projectid from (select c.*,d.name as zonename,d.folderid as zoneid from (select a.name,a.id as datacenterid,b.folderid as vmfolderid from (select * from vsphere_datacenter where version=:version) a left join (select * from vsphere_datacenter_folder where version=:version) b on a.id=b.datacenterid where a.id=:dcid) c left join (select * from vsphere_folder where version=:version) d on vmfolderid=d.parentid) e left join (select * from vsphere_folder where version=:version) f on e.zoneid=f.parentid) g left join (select * from vsphere_vm where version=:version) h on g.projectid=h.parentid")
    result = db.engine.execute(cmd, parameters)
    return result

def get_info_by_dcid(ver,dcid):
    parameters = {}
    parameters['version'] = ver
    parameters['dcid'] = dcid
    cmd = text("select e.name,e.zonename,e.zoneid,count(*) from (select c.*,d.name as zonename,d.folderid as zoneid from (select a.name,a.id as datacenterid,b.folderid as vmfolderid from (select * from vsphere_datacenter where version=:version) a left join (select * from vsphere_datacenter_folder where version=:version) b on a.id=b.datacenterid where a.id=:dcid) c left join (select *  from vsphere_folder where version=:version) d on vmfolderid=d.parentid) e join (select * from vsphere_folder where version=:version) f on e.zoneid=f.parentid group by e.name,e.zonename,e.zoneid")
    result = db.engine.execute(cmd, parameters)
    return result