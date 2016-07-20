from sqlalchemy.sql import text
from app import db


def get_by_id(id):
    parameters = {}
    parameters['id'] = id
    cmd = text("select * from project_mail where id=:id")
    result = db.engine.execute(cmd, parameters)
    if result:
        return result.first()


def get_all():
    cmd = text("select * from project_mail where state!='del'")
    result = db.engine.execute(cmd)
    return result


def create(projectid,projectname,mailtype,m):
    parameters = {}
    parameters['projectid'] = str(projectid)
    parameters['project'] = projectname
    parameters['type'] = str(mailtype)
    parameters['state'] = 'new'
    parameters['title'] = m['title']
    parameters['from'] = m['from']
    parameters['to'] = ','.join(m['to'])
    parameters['cc'] = ','.join(m['cc'])
    parameters['attachment'] = ','.join(m['attachment'])
    parameters['content'] = m['content']
    cmd = text("insert into project_mail values(null,:projectid,:project,:type,:state,"
               "now(),null,:title,:from,:to,:cc,:attachment,:content)")
    db.engine.execute(cmd, parameters)