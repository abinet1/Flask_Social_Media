from flask import Flask, url_for, render_template, redirect
from flask.helpers import flash
from flask_login.utils import logout_user
from wtforms.validators import Email
from Flask_Social_Media import app, db, bcrypt
from Flask_Social_Media.form import LoginForm, RegisterForm
from Flask_Social_Media.models import User
from flask_login import login_user, logout_user, current_user
import phonenumbers

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember_me.data)
				return redirect(url_for("index"))
		else:
			user = User.query.filter_by(phone_number=form.email.data ).first()
			if user:
				if bcrypt.check_password_hash(user.password, form.password.data):
					login_user(user, remember=form.remember_me.data)
					return redirect(url_for("index"))
			else:
				flash(f'wrong Email/Phone Number')
				print('wrong Email/Phone Number')
			
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
		
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(first_name = form.first_name.data, mid_name = form.mid_name.data, last_name = form.last_name.data, 
			gender = form.gender.data, phone_number = form.phone_number.data, email = form.email.data, address = form.address.data, 
			birth_day = form.birth_day.data, bio = form.bio.data, user_name = form.user_name.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template('signup.html', form=form)

@app.route('/logout')
def log_out():
	logout_user()
	return redirect(url_for('login'))
	
