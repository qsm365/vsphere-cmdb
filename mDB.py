import MySQLdb
import logging

db_host='127.0.0.1'
db_user='vsphere'
db_passwd='vsphere'
db_name='vsphere'
db_port=3306
db_charset='utf8'

logger = logging.getLogger('mDB')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
logger.addHandler(ch)

class mDB:
    def __init__(self):
        self.sql=''
    
    def saveVersion(self):
        self.sql='insert into vsphere_version(synctime) values(now())'
        version_id = str(self.DMLSql())
        return version_id
    
    def saveDataCenter(self,ver,mid,name):
        self.sql='insert into vsphere_datacenter(version,id,name) values ("'+ver+'","'+mid+'","'+name+'")'
        self.DMLSql()
    
    def saveDataCenterFolder(self,ver,folderid,name,datacenterid,datacenter,ftype):
        self.sql='insert into vsphere_datacenter_folder(version,folderid,name,datacenterid,datacenter,type) values ("'+ver+'","'+folderid+'","'+name+'","'+datacenterid+'","'+datacenter+'","'+ftype+'")'
        self.DMLSql()
    
    def saveFolder(self,ver,folderid,name,parentid,parent,ftype):
        self.sql='insert into vsphere_folder(version,folderid,name,parentid,parent,type) values ("'+ver+'","'+folderid+'","'+name+'","'+parentid+'","'+parent+'","'+ftype+'")'
        self.DMLSql()
    
    def saveVM(self,ver,vmid,name,parentid,parent,state,cpu,memory,os):
        self.sql='insert into vsphere_vm(version,vmid,name,parentid,parent,state,cpu,memory,os) values ("'+ver+'","'+vmid+'","'+name+'","'+parentid+'","'+parent+'","'+state+'","'+cpu+'","'+memory+'","'+os+'")'
        self.DMLSql()
    
    def saveVMNic(self,ver,nicid,vmid,networktype,network,ipaddress,mac):
        self.sql='insert into vsphere_vmnic(version,nicid,vmid,network,ipaddress,mac,networktype) values ("'+ver+'","'+nicid+'","'+vmid+'","'+network+'","'+ipaddress+'","'+mac+'","'+networktype+'")'
        self.DMLSql()

    def saveNetwork(self,ver,networkid,name,parentid,parent,networktype):
        self.sql='insert into vsphere_network(version,networkid,name,parentid,parent,networktype) values ("'+ver+'","'+networkid+'","'+name+'","'+parentid+'","'+parent+'","'+networktype+'")'
        self.DMLSql()

    def saveHost(self,ver,hostid,name,parentid,parent,cpu,memory,vendor,model):
        self.sql='insert into vsphere_host(version,hostid,name,parentid,parent,cpu,memory,vendor,model) values ("'+ver+'","'+hostid+'","'+name+'","'+parentid+'","'+parent+'","'+cpu+'","'+memory+'","'+vendor+'","'+model+'")'
        self.DMLSql()

    def saveDatastore(self,ver,datastoreid,name,parentid,parent,capacity,freespace,uncommitted):
        self.sql='insert into vsphere_datastore(version,datastoreid,name,parentid,parent,capacity,freespace,uncommitted) values ("'+ver+'","'+datastoreid+'","'+name+'","'+parentid+'","'+parent+'","'+capacity+'","'+freespace+'","'+uncommitted+'")'
        self.DMLSql()

    def updateVMHost(self,ver,vmid,hostid):
        self.sql='update vsphere_vm set hostid="'+hostid+'" where version="'+ver+'" and vmid="'+vmid+'"'
        self.DMLSql()

    def DMLSql(self):
        try:
            if(len(self.sql)<500):
                logging.debug(self.sql)
            else:
                logging.debug(self.sql[0:499])
            conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name,port=db_port,charset='utf8')
            cur=conn.cursor()
            ares=cur.execute(self.sql)
            logging.debug("Mysql DMLOps "+str(ares))
            insert_id = conn.insert_id()
            cur.close()
            conn.commit()
            conn.close()
            return insert_id
        except MySQLdb.Error,e:
            print e
            logging.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
