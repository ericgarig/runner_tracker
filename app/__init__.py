from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models