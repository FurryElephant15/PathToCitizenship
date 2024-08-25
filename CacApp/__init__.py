from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

fcp = Flask(__name__)
db = SQLAlchemy()
fcp.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
fcp.config['SECRET_KEY'] = 'password'

db.init_app(fcp)
migrate = Migrate(fcp, db)
login = LoginManager(fcp)
from CacApp.routes import *
from CacApp.models import * 