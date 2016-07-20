from sqlalchemy.sql import text
from app import db

def get_vmnic_by_network(ver,network):
    parameters = {}
    parameters['version'] = ver
    parameters['network'] = network
    cmd = text("select * from vsphere_vmnic where version=:version and network=:network")
    result = db.engine.execute(cmd, parameters)
    return result

def get_by_vmid(ver,vmid):
    parameters = {}
    parameters['version'] = ver
    parameters['vmid'] = vmid
    cmd = text("select * from vsphere_vmnic where version=:version and vmid=:vmid")
    result = db.engine.execute(cmd, parameters)
    return result

def count_by_networkid(ver,network):
    parameters = {}
    parameters['version'] = ver
    parameters['network'] = network
    cmd = text("select count(*) from vsphere_vmnic where version=:version and network=:network")
    result = db.engine.execute(cmd, parameters)
    return result

def get_info_by_networkid(ver,networkid):
    parameters = {}
    parameters['version'] = ver
    parameters['networkid'] = networkid
    sql = "select c.ipaddress,c.vmname,c.vmid,c.projectname,c.projectid,d.name as zonename,d.folderid as zoneid from (select a.ipaddress,a.name as vmname,a.vmid,b.parentid as zoneid,b.name as projectname,b.folderid as projectid from (select v1.ipaddress,v2.vmid,v2.name,v2.parentid from (select * from vsphere_vmnic where version=:version) v1 left join (select * from vsphere_vm where version=:version) v2 on v1.vmid=v2.vmid where v1.network=:networkid ) a left join (select * from vsphere_folder where version=:version) b on a.parentid=b.folderid) c left join (select * from vsphere_folder where version=:version) d on c.zoneid=d.folderid"
    cmd = text(sql)
    result = db.engine.execute(cmd, parameters)
    return result