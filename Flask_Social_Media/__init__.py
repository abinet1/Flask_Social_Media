from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor




app = Flask(__name__)

app.config['SECRET_KEY'] = '275a2480f58a41dc98bd4f302335af51'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)

from Flask_Social_Media import routes