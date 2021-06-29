import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '275a2480f58a41dc98bd4f302335af51'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_WIDTH'] = 600
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)

from Flask_Social_Media import routes
