from pyVim import connect
import ssl
from pyVmomi import vmodl
from pyVmomi import vim
import mDB
import time
import traceback

progDB=mDB.mDB()

def getVM(ver,vm):
    vmid = vm._moId
    name = vm.name
    parentid = vm.parent._moId
    parent = vm.parent.name
    state = vm.summary.runtime.powerState
    cpu = str(vm.config.hardware.numCPU)
    memory = str(vm.config.hardware.memoryMB)
    os = vm.config.guestFullName
    committed = vm.storage.perDatastoreUsage[0].committed
    uncommitted = vm.storage.perDatastoreUsage[0].uncommitted
    datastoreid = vm.storage.perDatastoreUsage[0].datastore._moId
    datastore = vm.storage.perDatastoreUsage[0].datastore.name
    progDB.saveVM(ver, vmid, name, parentid, parent, state, cpu, memory, os, committed, uncommitted, datastoreid, datastore)
    networks = vm.network
    guest = vm.guest
    if guest is not None:
        net = guest.net
        for n in net:
            nicid = str(n.deviceConfigId)
            if n.deviceConfigId>0:
                ipaddress = ''
                if len(n.ipAddress)>0:
                    ipaddress = filterIpv4(n.ipAddress)
                if ipaddress is None:
                    ipaddress = ''
                mac = n.macAddress
                networkname = n.network
                networktype='VMNetwork'
                network=''
                for nn in networks:
                    if nn.name==networkname:
                        if str(type(nn))=='<class \'pyVmomi.VmomiSupport.vim.dvs.DistributedVirtualPortgroup\'>':
                            networktype='Nexus1000V'
                            network=nn.key
                        else:
                            network=nn._moId

                progDB.saveVMNic(ver, nicid, vmid, networktype, network, ipaddress, mac)

def getDataCenter(ver,content):
    for en in content.rootFolder.childEntity:
        mid = en._moId
        name = en.name
        progDB.saveDataCenter(ver,mid,name)
    return content.rootFolder.childEntity

def getVmFolder(ver,parent):
    parentid = parent._moId
    parentname = parent.name
    ftype = 'vmFolder'
    #print parent.childEntity
    for child in parent.childEntity:
        if str(type(child))=='<class \'pyVmomi.VmomiSupport.vim.Folder\'>':
            folderid = child._moId
            name = child.name
            progDB.saveFolder(ver,folderid, name, parentid, parentname, ftype)
            #time.sleep(1)
            try:
                getVmFolder(ver,child)
            except:
                traceback.print_exc()
        elif str(type(child))=='<class \'pyVmomi.VmomiSupport.vim.VirtualMachine\'>':
            #time.sleep(1)
            try:
                getVM(ver,child)
            except:
                traceback.print_exc()

def getHostFolder(ver,parent):
    parentid = parent._moId
    parentname = parent.name
    ftype = 'hostFolder'
    for child in parent.childEntity:
        folderid = child._moId
        name = child.name
        progDB.saveFolder(ver, folderid, name, parentid, parentname, ftype)
        for host in child.host:
            hostid=host._moId
            hostname=host.name
            cpu=str(host.hardware.cpuInfo.numCpuThreads)
            memory=str(host.hardware.memorySize/1024/1024)
            vendor=host.hardware.systemInfo.vendor
            model=host.hardware.systemInfo.model
            progDB.saveHost(ver,hostid,hostname,folderid,name,cpu,memory,vendor,model)
            for vm in host.vm:
                vmid=vm._moId
                progDB.updateVMHost(ver,vmid,hostid)

def filterIpv4(ips):
    for ip in ips:
        if len(ip)<=15:
            return ip

def getNetwork(ver,parent):
    networks=parent.network
    parentid = parent._moId
    parentname = parent.name
    for network in networks:
        networkname = network.name
        networktype = 'VMNetwork'
        if str(type(network))=='<class \'pyVmomi.VmomiSupport.vim.dvs.DistributedVirtualPortgroup\'>':
            networkid=network.key
            networktype = 'Nexus1000V'
        else:
            networkid = network._moId
        progDB.saveNetwork(ver,networkid,networkname,parentid,parentname,networktype)

def getDatastore(ver,parent):
    parentid = parent._moId
    parentname = parent.name
    datastore = parent.datastore
    for ds in datastore:
        datastoreid=ds._moId
        name=ds.name
        capacity=str(ds.summary.capacity)
        freespace=str(ds.summary.freeSpace)
        uncommitted=str(0)
        if ds.summary.uncommitted:
            uncommitted=str(ds.summary.uncommitted)
        progDB.saveDatastore(ver, datastoreid, name, parentid, parentname, capacity, freespace, uncommitted)

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    vcenterip='198.16.2.221'
    vcenterport=443
    vcenteruser='admin'
    vcenterpass='ysyw2015$8'
    try:
        si = connect.Connect(vcenterip, vcenterport, vcenteruser, vcenterpass)
        print "vCenter conneted!"
        content = si.RetrieveContent()
        ver=progDB.saveVersion()
        dcs = getDataCenter(ver,content)
        for dc in dcs:
            name = dc.vmFolder.name
            folderid = dc.vmFolder._moId
            datacenterid = dc._moId
            datacenter = dc.name
            ftype = 'vmFolder'
            progDB.saveDataCenterFolder(ver,folderid,name,datacenterid,datacenter,ftype)
            getNetwork(ver, dc)
            getVmFolder(ver,dc.vmFolder)
            getHostFolder(ver, dc.hostFolder)
            getDatastore(ver,dc)

    except:
        traceback.print_exc()
        #print("Caught vmodl fault : " + error.msg)