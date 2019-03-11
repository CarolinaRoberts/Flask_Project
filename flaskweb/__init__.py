from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba317a60e12f823b0a9ce82ec3a24867feb31c457a94fb7e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1814178:Santiago31415@csmysql.cs.cf.ac.uk:3306/c1814178'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from flaskweb import routes