from pyVim import connect
import ssl
from pyVmomi import vmodl
from pyVmomi import vim
import mDB
import time

progDB=mDB.mDB()

def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    
    #print("Name       : ", summary.config.name)
    #print("Parent Name: ",parent.name)
    #print("Template   : ", summary.config.template)
    #print("Path       : ", summary.config.vmPathName)
    #print("Guest      : ", summary.config.guestFullName)
    #print("Instance UUID : ", summary.config.instanceUuid)
    #print("Bios UUID     : ", summary.config.uuid)
    #annotation = summary.config.annotation
    #if annotation:
    #    print("Annotation : ", annotation)
    
    #if summary.runtime.question is not None:
    #    print("Question  : ", summary.runtime.question.text)
    print("")

def getVM(ver,vm):
    vmid = vm._moId
    name = vm.name
    parentid = vm.parent._moId
    parent = vm.parent.name
    state = vm.summary.runtime.powerState
    cpu = str(vm.config.hardware.numCPU)
    memory = str(vm.config.hardware.memoryMB)
    os = vm.config.guestFullName
    progDB.saveVM(ver, vmid, name, parentid, parent, state, cpu, memory, os)
    
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
                network = n.network
                progDB.saveVMNic(ver, nicid, vmid, network, ipaddress, mac)
    

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
            time.sleep(1)
            getVmFolder(ver,child)
        elif str(type(child))=='<class \'pyVmomi.VmomiSupport.vim.VirtualMachine\'>':
            time.sleep(1)
            getVM(ver,child)

def filterIpv4(ips):
    for ip in ips:
        if len(ip)<=15:
            return ip

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        si = connect.Connect("198.16.2.221", 443, "admin", "ysyw2015$8")
        content = si.RetrieveContent()
        #container = content.rootFolder
        #viewType = [vim.VirtualMachine]
        #recursive = True
        #containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
        #children = containerView.view
        #iii=0
        #for child in children:
        #    iii=iii+1
        #    print_vm_info(child)
        #    if iii>3:
        #        break
        
        ver=progDB.saveVersion()
        dcs = getDataCenter(ver,content)
        for dc in dcs:
            getVmFolder(ver,dc.vmFolder)
            
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)