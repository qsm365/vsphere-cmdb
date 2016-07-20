from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_by_datastoreid(ver,datastoreid):
    parameters = {}
    parameters['version'] = ver
    parameters['datastoreid'] = datastoreid
    cmd = text("select * from vsphere_datastore where version=:version and datastoreid=:datastoreid")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()

def get_all_info(ver):
    parameters = {}
    parameters['version'] = ver
    cmd = text("select * from vsphere_datastore where version=:version")
    result = db.engine.execute(cmd, parameters)
    return result