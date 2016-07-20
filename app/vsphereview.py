# -*- coding:utf-8 -*-  

from flask import request,Blueprint,render_template,session,redirect,url_for,jsonify
from . import app
import vspherebusiness
import vsphereagent

vsphereprofile = Blueprint('vsphereprofile', __name__)

@app.route('/test', methods = ['GET', 'POST'])
def test():
    if not session.get('username'):
        return redirect(url_for('login'))
    moid = request.args.get('moid')
    histlevel = request.args.get('histlevel')
    perftype = request.args.get('type')
    if moid and histlevel and perftype:
        perfinfo = vsphereagent.get_brief_performance(moid, histlevel, perftype)
        return jsonify(perfinfo)
    else:
        return 'bad request',401

@app.route('/vsphere/datastore/list')
def vsphere_datastore_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    datastoreinfo = vspherebusiness.get_all_datastoreinfo(ver)
    return render_template('vsphere/vsphere_datastore_list.html', title='VSpher Datastore List', version=version,
                           datastoreinfo=datastoreinfo)

@app.route('/vsphere/performance/json',methods=['GET'])
def vsphere_performance_json():
    if not session.get('username'):
        return redirect(url_for('login'))
    moid = request.args.get('moid')
    histlevel = request.args.get('histlevel')
    perftype = request.args.get('type')
    if moid and histlevel and perftype:
        perfinfo = vsphereagent.get_brief_performance(moid, histlevel, perftype)
        return jsonify(perfinfo)
    else:
        return 'bad request', 401

@app.route('/vsphere/performance/detail',methods=['GET'])
def vsphere_performance_detail():
    if not session.get('username'):
        return redirect(url_for('login'))
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    if not request.args.get('type'):
        return redirect(url_for('vsphere_vm_home'))
    if not request.args.get('moid'):
        return redirect(url_for('vsphere_vm_home'))
    moid = request.args.get('moid')
    perftype = request.args.get('type')
    histlevel = request.args.get('histlevel')
    if histlevel == 'day':
        histlevelstr = u'近一日'
    elif histlevel == 'week':
        histlevelstr = u'近一周'
    elif histlevel == 'month':
        histlevelstr = u'近一月'
    else:
        histlevelstr = u'准实时'
    if perftype=='vm':
        info = vspherebusiness.get_brief_vminfo_from_vmid(ver, moid)
        ret = vsphereagent.get_performance(moid, histlevel, 'vm')
    elif perftype=='host':
        info = vspherebusiness.get_brief_hostinfo_from_hostid(ver, moid)
        ret = vsphereagent.get_performance(moid, histlevel, 'host')
    if ret:
        sampletime = ret['sampletime']
        cpuval = ret['cpuval']
        disk1val = ret['disk1val']
        disk2val = ret['disk2val']
        memval = ret['memval']
        netval = ret['netval']
        slen = len(sampletime)
        return render_template('vsphere/vsphere_performance_detail.html', title='VSpher VM Performance', sampletime=sampletime,
                               cpuval=cpuval, disk1val=disk1val, disk2val=disk2val, memval=memval, netval=netval,
                               slen=slen, info=info, histlevelstr=histlevelstr, moid=moid, perftype=perftype)
    else:
        return redirect(url_for('vsphere/vsphere_vm_home'))

@app.route('/vsphere/host/detail',methods=['GET'])
def vsphere_host_detail():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not request.args.get('hostid'):
        return redirect(url_for('vsphere_host_list'))
    hostid = request.args.get('hostid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    host = vspherebusiness.get_host_detail_by_hostid(ver, hostid)
    hostinfo = host['hostinfo']
    hostvms = host['hostvm']
    allocated_cpu=0
    allocated_mem=0
    for h in hostvms:
        if h[5]=='poweredOn':
            allocated_cpu = allocated_cpu + int(h[6])
            allocated_mem = allocated_mem + int(h[7])
    return render_template('vsphere/vsphere_host_detail.html', title='VSpher Host', version=version, hostinfo=hostinfo,
                           hostvms=hostvms, allocated_cpu=allocated_cpu, allocated_mem=allocated_mem)

@app.route('/vsphere/host/list',methods=['GET'])
def vsphere_host_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    domainid = request.args.get('domainid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    hostinfo = vspherebusiness.get_host_list_by_domainid(ver, domainid)
    return render_template('vsphere/vsphere_host_list.html', title='VSpher Host List', version=version,
                           hostinfo=hostinfo)

@app.route('/vsphere/vm/map',methods=['GET'])
def vsphere_vm_map():
    if not session.get('username'):
        return redirect(url_for('login'))
    dcid = request.args.get('dcid', 'datacenter-2')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    dcmap = vspherebusiness.get_vm_map(ver, dcid)
    return render_template('vsphere/vsphere_vm_map.html', title='VSpher VM Map', version=version, dcmap=dcmap)

@app.route('/vsphere/project/map',methods=['GET'])
def vsphere_project_map():
    if not session.get('username'):
        return redirect(url_for('login'))
    dcid = request.args.get('dcid', 'datacenter-2')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    dcmap = vspherebusiness.get_project_map(ver, dcid)
    return render_template('vsphere/vsphere_project_map.html', title='VSpher Project Map', version=version, dcmap=dcmap)

@app.route('/vsphere/vm/detail',methods = ['GET'])
def vsphere_vm_detail():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not request.args.get('vmid'):
        return redirect(url_for('vsphere_vm_home'))
    vmid = request.args.get('vmid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    info = vspherebusiness.get_vm_detail_from_vmid(ver, vmid)
    zoneinfo = info['zone']
    projectinfo = info['project']
    vminfo = info['vm']
    vmnicinfo = info['vmnic']
    hostinfo = info['host']
    return render_template('vsphere/vsphere_vm_detail.html', title='VSpher VM',version=version,zoneinfo=zoneinfo,projectinfo=projectinfo,
                           vminfo=vminfo,vmnicinfo=vmnicinfo,hostinfo=hostinfo)

@app.route('/vsphere/network',methods = ['GET'])
def vsphere_network_home():
    if not session.get('username'):
        return redirect(url_for('login'))
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    networks = vspherebusiness.get_all_networkinfos(ver)
    return render_template('vsphere/vsphere_network_home.html', title='VSpher Network', version=version, networks=networks)

@app.route('/vsphere/network/list',methods = ['GET'])
def vsphere_network_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not request.args.get('networkid'):
        return redirect(url_for('vsphere_network_home'))
    networkid = request.args.get('networkid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    network = vspherebusiness.get_networkinfo_by_networkid(ver, networkid)
    networkinfo = network.pop('info')
    networklist = network.pop('list')
    networkunknown = network.pop('unknown')
    networksubnet = network.pop('subnet')
    networkknown = network.pop('known')
    return render_template('vsphere/vsphere_network_list.html', title='VSpher Network List', version=version, networkinfo=networkinfo,
                           list=networklist, networkunknown=networkunknown, networksubnet=networksubnet,
                           networkknown=networkknown)

@app.route('/vsphere/vm/list',methods = ['GET'])
def vsphere_vm_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not request.args.get('vmfid'):
        return redirect(url_for('vsphere_vm_home'))
    vmfid=request.args.get('vmfid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    folder = vspherebusiness.get_folder(ver, vmfid)
    vms = vspherebusiness.get_child_vm(ver, vmfid).fetchall()
    c_vm = len(vms)
    return render_template('vsphere/vsphere_vm_list.html', title='VSpher VM List',version=version,folder=folder,vms=vms,c_vm=c_vm)

@app.route('/vsphere/vm/project/list',methods = ['GET'])
def vsphere_project_list():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not request.args.get('vmfid'):
        return redirect(url_for('vsphere_vm_home'))
    vmfid=request.args.get('vmfid')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    folder = vspherebusiness.get_folder(ver, vmfid)
    folders = vspherebusiness.get_child_folder(ver, vmfid).fetchall()
    vms = vspherebusiness.get_child_vm(ver, vmfid).fetchall()
    c_vms = len(vms)
    c_vm = c_vms
    for f in folders:
        c_vm = c_vm + f[2]
    return render_template('vsphere/vsphere_project_list.html', title='VSpher Project List',version=version,folder=folder,
                           folders=folders,c_vm=c_vm,c_vms=c_vms,vmfid=vmfid)

@app.route('/vsphere/vm', methods = ['GET'])
def vsphere_vm_home():
    if not session.get('username'):
        return redirect(url_for('login'))
    dcid = request.args.get('dcid','datacenter-2')
    version = vspherebusiness.get_new_verion()
    ver = version[0]
    dcs = vspherebusiness.get_all_datacenters(ver)
    dcinfo = vspherebusiness.get_dcinfo_by_dcid(ver, dcid)
    return render_template('vsphere/vsphere_vm_home.html', title='VSpher VM Home', version=version, dcs=dcs,dcinfo=dcinfo )

@app.template_filter('adjustnum_k')
def adjustnum_filter(s):
    if s<1000:
        return str(s)+' K'
    elif s<1000000:
        return str(round(s/1024.0,2))+' M'
    elif s<1000000000:
        return str(round(s/1024.0/1024.0,2))+' G'
    else:
        return str(round(s / 1024.0 / 1024.0/ 1024.0, 2)) + ' T'

@app.template_filter('adjustnum')
def adjustnum_filter(s):
    s = s/1024;
    if s<1024:
        return str(s)+' K'
    elif s<1048576:
        return str(round(s/1024.0,2))+' M'
    elif s<1073741824:
        return str(round(s/1024.0/1024.0,2))+' G'
    else:
        return str(round(s / 1024.0 / 1024.0/ 1024.0, 2)) + ' T'

@app.template_filter('percentage')
def percentage_filter(s):
    return str(round(s*100,2)) + ' %'