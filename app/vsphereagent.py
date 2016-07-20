# -*- coding:utf-8 -*-
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
from . import app
import datetime
import pytz

ssl._create_default_https_context = ssl._create_unverified_context
vcenterip=app.config['VCENTERIP']
vcenterport=app.config['VCENTERPORT']
vcenteruser=app.config['VCENTERUSER']
vcenterpass=app.config['VCENTERPASS']

def get_brief_performance(moid,histlevel,perftype):
    perfResults = query_performance(moid, histlevel, perftype)
    if perfResults:
        metric = perfResults[0]
        # print metric
        sampletime = []
        starttime = str(metric.sampleInfo[0].timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')))[0:19]
        endtime = str(metric.sampleInfo[-1].timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')))[0:19]
        ret = {}
        ret['moid'] = moid
        ret['starttime'] = starttime
        ret['endtime'] = endtime
        for val in metric.value:
            if val.id.counterId == 2:
                ret['cpuavg'] = round(sum(val.value) / float(len(val.value))/100.0,2)
                ret['cpumax'] = max(val.value)/100.0
            elif val.id.counterId == 125:
                ret['disk1avg'] = round(sum(val.value) / float(len(val.value)),2)
                ret['disk1max'] = max(val.value)
            elif val.id.counterId == 133:
                ret['disk2avg'] = round(sum(val.value) / float(len(val.value)),2)
                ret['disk2max'] = max(val.value)
            elif val.id.counterId == 24:
                ret['memavg'] = round(sum(val.value) / float(len(val.value))/100.0,2)
                ret['memmax'] = max(val.value)/100.0
            elif val.id.counterId == 143:
                ret['netavg'] = round(sum(val.value) / float(len(val.value)),2)
                ret['netmax'] = max(val.value)
        return ret

def get_performance(moid,histlevel,perftype):
    perfResults = query_performance(moid, histlevel, perftype)
    if perfResults:
        metric = perfResults[0]
        # print metric
        sampletime = []
        for msi in metric.sampleInfo:
            localtime = str(msi.timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')))[0:19]
            sampletime.append(localtime)
        cpuval = []
        disk1val = []
        disk2val = []
        memval = []
        netval = []
        for val in metric.value:
            if val.id.counterId == 2:
                # cpu usage
                for v in val.value:
                    # if v>0:
                    cpuval.append(v / 100.0)
            elif val.id.counterId == 125:
                # disk usage
                for v in val.value:
                    # if v > 0:
                    disk1val.append(v)
            elif val.id.counterId == 133:
                # disk latency
                for v in val.value:
                    # if v > 0:
                    disk2val.append(v)
            elif val.id.counterId == 24:
                # memory usage
                for v in val.value:
                    # if v > 0:
                    memval.append(v / 100.0)
            elif val.id.counterId == 143:
                # net usage
                for v in val.value:
                    # if v > 0:
                    netval.append(v)
        ret = {}
        ret['sampletime'] = sampletime
        ret['cpuval'] = cpuval
        ret['disk1val'] = disk1val
        ret['disk2val'] = disk2val
        ret['memval'] = memval
        ret['netval'] = netval
        return ret

def query_performance(moid,histlevel,perftype):
    try:
        si = connect.Connect(vcenterip, vcenterport, vcenteruser, vcenterpass)
        content = si.RetrieveContent()
        perfManager = content.perfManager
        micpu = vim.PerformanceManager.MetricId(counterId=2, instance="")
        midisk1 = vim.PerformanceManager.MetricId(counterId=125, instance="")
        midisk2 = vim.PerformanceManager.MetricId(counterId=133, instance="")
        mimem = vim.PerformanceManager.MetricId(counterId=24, instance="")
        minet = vim.PerformanceManager.MetricId(counterId=143, instance="")
        #startTime = datetime.datetime.strptime(str(datetime.date.today() - datetime.timedelta(days=1)), '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Shanghai')).astimezone(pytz.utc)
        #endTime = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Shanghai')).astimezone(pytz.utc)
        endTime = datetime.datetime.now()-datetime.timedelta(minutes=10)
        intervalId = 20
        if histlevel=='day':
            intervalId = 300
        elif histlevel=='week':
            intervalId = 1800
        elif histlevel=='month':
            intervalId = 7200
        else:
            intervalId = 20
            endTime = None

        if perftype=='vm':
            vm = vim.VirtualMachine(moid)
            query = vim.PerformanceManager.QuerySpec(intervalId=intervalId, entity=vm,
                                                     metricId=[micpu, midisk1, midisk2, mimem, minet], endTime=endTime)
        elif perftype=='host':
            host = vim.HostSystem(moid)
            query = vim.PerformanceManager.QuerySpec(intervalId=intervalId, entity=host,
                                                     metricId=[micpu, midisk1, midisk2, mimem, minet],endTime=endTime)
        perfResults = perfManager.QueryPerf(querySpec=[query])
        return perfResults
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)