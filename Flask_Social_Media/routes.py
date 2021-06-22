import os
from flask import url_for, render_template, redirect, request
from flask.helpers import flash, send_from_directory
from flask_login.utils import login_required, logout_user
from Flask_Social_Media import app, db, bcrypt, csrf
from Flask_Social_Media.form import LoginForm, RegisterForm, AboutForm, EditProfile
from Flask_Social_Media.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flask_ckeditor import upload_success, upload_fail
# import phonenumbers

#--------------------------------------------Home-------------------------------------------------------------------------------------------------
@app.route('/')
@login_required
def index():
	return render_template('index.html')


#--------------------------------------------Authontication-------------------------------------------------------------------------------------------------

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


#--------------------------------------------ABOUT-------------------------------------------------------------------------------------------------

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
	form = AboutForm()
	if form.validate_on_submit():
		current_user.about=form.about.data
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('about.html', form=form)

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)

#-------------------------------------PROFILE--------------------------------------------------------------------------------------------------------

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
	form=RegisterForm()
	return render_template("profile.html", form=form)



#-------------------------------------Contacts--------------------------------------------------------------------------------------------------------

@app.route('/contacts',methods=['GET','POST'])
@login_required
def contacts():
	freinds=[]
	groups=[]
	chanals=[]
	return render_template('contacts.html',freinds=freinds,groups=groups,chanals=chanals)
