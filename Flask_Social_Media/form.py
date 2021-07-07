from datetime import MAXYEAR
from flask.helpers import flash
from wtforms.fields.core import BooleanField, FormField, IntegerField, SelectField
from wtforms.fields.simple import SubmitField, TextAreaField 
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.fields.html5 import DateField, TelField
from Flask_Social_Media import db, bcrypt
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField
from Flask_Social_Media.models import User

class RegisterForm(FlaskForm):
	first_name = StringField("First Name", validators=[DataRequired(), Length(max=25)])
	mid_name = StringField("Midle Name", validators=[Length(max=25)])
	last_name = StringField("Last Name", validators=[DataRequired(), Length(max=25)])
	gender = SelectField("Gender",choices=[("M","Male"),("F","Female")], validators=[DataRequired()])
	phone_number = StringField("Phone Number", validators=[DataRequired(), Length(max=15)])
	email = StringField("Email", validators=[Email(), DataRequired(), Length(min=3, max=125)])
	address = StringField("Address", validators=[DataRequired(), Length(min=3, max=125)])
	bio = CKEditorField("Bio", validators=[DataRequired()])
	birth_day = DateField("Birth day", validators=[DataRequired()])
	user_name = StringField("User name", validators=[DataRequired(), Length(min=3,max=30)])
	password = StringField("Password", validators=[DataRequired()])
	confirm_password = StringField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Sign up")
	def validate_user_name(self, user_name):
		user = User.query.filter_by(user_name = user_name.data).first()
		if user:
			raise ValidationError(f"This user name is alredy been used by other user please try an other one.")

	def validate_phone_number(self, phone_number):
		user = User.query.filter_by(phone_number = phone_number.data).first()
		if user:
			raise ValidationError(f"This Phone number is alredy been used by other user please try an other one.")
	
	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError(f"This Email is alredy been used by other user please try an other one.")

class LoginForm(FlaskForm):
	email = StringField("Email/Phone Numbet", validators=[DataRequired(), Length(min=3, max=125)])
	password = StringField("Password", validators=[DataRequired()])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Login")

class AboutForm(FlaskForm):
	about = CKEditorField('About my self', validators=[DataRequired()])
	submit = SubmitField('Update')

# class EditProfile(FlaskForm):
# 	first_name = StringField("First Name", validators=[Length(max=25), DataRequired()])
# 	mid_name = StringField("Midle Name", validators=[Length(max=25), DataRequired()])
# 	last_name = StringField("Last Name", validators=[Length(max=25), DataRequired()])
# 	gender = SelectField("Gender",choices=[("M","Male"),("F","Female")], validators=[DataRequired()])
# 	phone_number = StringField("Phone Number", validators=[Length(max=15), DataRequired()])
# 	address = StringField("Address", validators=[Length(min=3, max=125), DataRequired()])
# 	birth_day = DateField("Birth day", validators=[DataRequired()])
# 	password = StringField("Password", validators=[DataRequired()])
# 	submit = SubmitField("Update")
	
class PostForm(FlaskForm):
	title = StringField("Title", validators=[Length(max=120)])
	context = TextAreaField("Context", validators=[Length(max=120,min=3)])
	article = CKEditorField("Article", validators=[])
	image = StringField('Images', validators=[])
	catagory = StringField('Images', validators=[])
	submit = SubmitField('Post')


class ProfileForm(FlaskForm):
	first_name = StringField("First Name", validators=[Length(max=25)])
	mid_name = StringField("Midle Name", validators=[Length(max=25)])
	last_name = StringField("Last Name", validators=[Length(max=25)])
	gender = SelectField("Gender",choices=[("M","Male"),("F","Female")], validators=[])
	phone_number = StringField("Phone Number", validators=[Length(max=15)])
	email = StringField("Email", validators=[Email(), Length(min=3, max=125)])
	address = StringField("Address", validators=[Length(min=3, max=125)])
	bio = CKEditorField("Bio", validators=[])
	birth_day = DateField("Birth day", validators=[])
	user_name = StringField("User name", validators=[Length(min=3,max=30)])
	password = StringField("Password", validators=[])
	submit = SubmitField("Update Profile")


class CommentForm(FlaskForm):
	contant = TextAreaField("Comment", validators=[DataRequired()])
	submit = SubmitField("Comment")

class ReplayForm(FlaskForm):
	comment = IntegerField("Comment id", validators=[DataRequired()])
	contant = TextAreaField("Comment", validators=[DataRequired()])
	submit = SubmitField("Replay")

    