from sqlalchemy.sql import text
from app import db


def get_by_id(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select * from project_department where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def get_all():
    cmd = text("select * from project_department")
    result = db.engine.execute(cmd)
    return result


def delete(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("delete from project_department where id=:id")
    result = db.engine.execute(cmd, parameters)

def add(name):
    parameters = {}
    parameters['name'] = name
    cmd = text("insert into project_department values(null,:name,null,null)")
    result = db.engine.execute(cmd, parameters)


def update(id,name,leader1,leader2):
    parameters = {}
    parameters['id'] = id
    parameters['name'] = name
    parameters['leader1'] = leader1
    parameters['leader2'] = leader2
    cmd = text("update project_department set name=:name,leaderid1=:leader1,leaderid2=:leader2 where id=:id")
    result = db.engine.execute(cmd,parameters)