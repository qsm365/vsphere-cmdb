# -*- coding:utf-8 -*-
from app.models.vsphere import folder, version, host, network, vm, vmnic, datacenter,datastore

def get_new_verion():
    vers = version.get_new()
    if vers:
        return vers

def get_all_datacenters(ver):
    dcs = datacenter.get_all(ver);
    return dcs

def get_dcinfo_by_dcid(ver,dcid):
    dcinfo = datacenter.get_info_by_dcid(ver, dcid)
    return dcinfo

def get_folder(ver,vmfid):
    folders = folder.get_by_folderid(ver, vmfid)
    if folders:
        return folders.first()

def get_child_folder_conut(ver,vmfid):
    count = folder.count_by_parentid(ver, vmfid)
    c = count.first()
    if c:
        return c[0]
    return -1

def get_child_folder(ver,vmfid):
    folders = folder.get_by_parentid(ver, vmfid)
    return folders

def get_child_vm(ver,vmfid):
    vms = vm.get_by_parentid(ver, vmfid)
    return vms


def get_vm_detail_from_vmid(ver,vmid):
    projectid= vm.get_parent_id(ver, vmid)
    zoneid= folder.get_parent_id(ver, projectid)
    zoneinfo = folder.get_by_folderid(ver, zoneid).first()
    projectinfo = folder.get_by_folderid(ver, projectid).first()

    if not zoneinfo:
        zoneinfo=projectinfo
        projectinfo=None
    vminfo = vm.get_by_vmid(ver, vmid)
    vmnicinfo = vmnic.get_by_vmid(ver, vmid).fetchall()
    hostid = vminfo[9]
    hostinfo = host.get_by_hostid(ver, hostid)
    info={}
    info['zone'] = zoneinfo
    info['project'] = projectinfo
    info['vm'] = vminfo
    info['vmnic'] = vmnicinfo
    info['host'] = hostinfo
    return info

def get_brief_vminfo_from_vmid(ver,vmid):
    vminfo = vm.get_by_vmid(ver, vmid)
    return vminfo

def get_vminfo_from_vmids(ver,vmids):
    vminfo = vm.get_info_by_vmids(ver, vmids)
    return vminfo

def get_all_networkinfos(ver):
    return network.get_all_info(ver).fetchall()

def get_networkinfo_by_networkid(ver,networkid):
    networkinfo = network.get_by_networkid(ver, networkid).first()
    if networkinfo:
        ipinfos = vmnic.get_info_by_networkid(ver, networkid)
        fullnetwork=[]
        re={}
        subnet='0.0.0'
        for i in range(1,256):
            fullnetwork.append([i])
        unknownnetwork = []
        re['known']=0
        for ipinfo in ipinfos:
            if ipinfo[0]:
                re['known'] = re['known']+1
                ip = ipinfo[0]
                if subnet=='0.0.0':
                    subnet = ip[0:ip.rfind('.')]
                i = int(ip[ip.rfind('.')+1:])
                ii=ipinfo.values()
                ii[0] = i
                fullnetwork[i-1]=ii
            else:
                unknownnetwork.append(ipinfo)
        re['list']=fullnetwork
        re['unknown']=unknownnetwork
        re['info']=networkinfo
        re['subnet']=subnet
        return re

def get_project_map(ver,dcid):
    dcmap = datacenter.get_project_map_by_dcid(ver, dcid)
    return dcmap

def get_vm_map(ver,dcid):
    dcmap = datacenter.get_vm_map_by_dcid(ver, dcid)
    return dcmap

def get_host_list_by_domainid(ver,domainid):
    if domainid:
        hostinfo = host.get_info_by_parentid(ver, domainid).fetchall()
    else:
        hostinfo = host.get_all_info(ver).fetchall()
    return hostinfo

def get_host_detail_by_hostid(ver,hostid):
    hostinfo = host.get_by_hostid(ver, hostid)
    hostvm = vm.get_vm_by_hostid(ver, hostid).fetchall()
    re = {}
    re['hostinfo'] = hostinfo
    re['hostvm'] = hostvm
    return re

def get_brief_hostinfo_from_hostid(ver,hostid):
    hostinfo = host.get_by_hostid(ver, hostid)
    return hostinfo

def get_all_datastoreinfo(ver):
    info = datastore.get_all_info(ver).fetchall()
    #过滤内部存储
    re = []
    for i in info:
        if i[2][0:9]!='datastore':
            re.append(i)
    return re