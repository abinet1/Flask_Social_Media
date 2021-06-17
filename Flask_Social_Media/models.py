from Flask_Social_Media import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(25), nullable=False, unique=False)
	mid_name = db.Column(db.String(25), nullable=False, unique=False)
	last_name = db.Column(db.String(25), nullable=False, unique=False)
	gender = db.Column(db.String(1), nullable=False, unique=False)
	phone_number = db.Column(db.String(15), nullable=True, unique=True)
	email = db.Column(db.String(125), nullable=False, unique=True)
	address = db.Column(db.String(125), nullable=False, unique=False)
	profile_picture = db.Column(db.String(125), nullable=False, unique=False, default="profile_picture.jpg")
	bio = db.Column(db.Text, nullable=True, unique=False)
	birth_day = db.Column(db.DateTime, nullable=False)
	about = db.Column(db.Text, nullable=True, unique=False)
	user_name = db.Column(db.String(30), nullable=False, unique=False)
	password = db.Column(db.String(60), nullable=False, unique=False)

	def __repr__(self):
		return f"User('{self.id}','{self.first_name}','{self.last_name}','{self.phone_number}','{self.user_name}')"