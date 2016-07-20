# -*- coding:utf-8 -*-  

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from app.coreview import coreprofile
app.register_blueprint(coreprofile)

from app.vsphereview import vsphereprofile
app.register_blueprint(vsphereprofile)

from app.projectview import projectprofile
app.register_blueprint(projectprofile)


