from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import db

def get_new():
    cmd = text("select * from vsphere_version order by synctime desc")
    result = db.engine.execute(cmd)
    row=result.first()
    return row

def get():
    cmd = text("select * from vsphere_version order by synctime desc")
    result = db.engine.execute(cmd)
    return result