from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# password hashing
bcrypt = Bcrypt(app)

# manage logins
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# SQL
app.config.from_object('config')
db = SQLAlchemy(app)


# now load the app. Done last to avoid self-referencing
from app import views, models