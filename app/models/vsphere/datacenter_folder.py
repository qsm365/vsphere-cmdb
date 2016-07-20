from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get(ver,datacenterid):
    parameters={}
    parameters['version']=ver
    parameters['datacenterid']=datacenterid
    cmd = text("select * from vsphere_datacenter_folder where version=:version and datacenterid=:datacenterid")
    result = db.engine.execute(cmd,parameters)
    return result