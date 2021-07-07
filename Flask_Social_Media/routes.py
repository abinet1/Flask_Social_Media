import os
import random
from datetime import datetime
from flask import url_for, render_template, redirect, request, abort
from flask.helpers import flash, send_from_directory
from flask_login.utils import login_required, logout_user
from Flask_Social_Media import app, db, bcrypt, csrf
from Flask_Social_Media.form import LoginForm, RegisterForm, AboutForm, PostForm, ProfileForm, CommentForm, ReplayForm
from Flask_Social_Media.models import PostLike, User, Post, Comment
from flask_login import login_user, logout_user, current_user, login_required
from flask_ckeditor import upload_success, upload_fail
#--------------------------------------------Home-------------------------------------------------------------------------------------------------

@app.route('/')
@login_required
def index():
	posts = Post.query.all()
	posts_you_follow=[]
	posts_for_you=[]
	my_post=[]
	form = PostForm()
	for post in posts:
		if(current_user.is_followed(post.auther)):
			posts_you_follow.append(post)
		elif (current_user == post.auther):
			my_post.append(post)
		elif not(current_user.is_followed(post.auther)):
			posts_for_you.append(post)
	if form.validate_on_submit():
		pst=Post(title=form.title.data,context=form.context.data,article=form.article.data)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', posts_you_follow=posts_you_follow, posts_for_you=posts_for_you, my_post=my_post, form=form)



#--------------------------------------------Friends-------------------------------------------------------------------------------------------------

@app.route('/friends', methods=['GET','POST'])
@login_required
def friends():
	requests=current_user.requests.all()
	find_freinds=current_user.find_friend()
	random.shuffle(find_freinds)
	return render_template('friends.html',friends=find_freinds,requests=requests)

@app.route('/friends/confirm/<int:user_id>',methods=['GET','POST'])
@login_required
def confirm_User(user_id):
	u2 = User.query.filter_by(id=user_id).first()
	current_user.confirm(u2)
	db.session.commit()
	return redirect(url_for('friends'))

@app.route('/friends/delete/<int:user_id>',methods=['GET','POST'])
@login_required
def delete_request(user_id):
	try:
		u2 = User.query.filter_by(id=user_id).first()
		resultetion=current_user.delete_request(u2)
		db.session.commit()
		return redirect(url_for('friends'))
	except:
		return redirect(url_for('friends'))

@app.route('/friends/add/<int:user_id>',methods=['GET','POST'])
@login_required
def add_friends(user_id):
	try:
		u2 = User.query.filter_by(id=user_id).first()
		resultetion=current_user.send_request(u2)
		db.session.commit()
		return redirect(url_for('friends'))
	except:
		return redirect(url_for('friends'))

@app.route('/friends/follow/<int:user_id>',methods=['GET','POST'])
@login_required
def follow(user_id):
	current_user.follow_user(User.query.get(user_id))
	return redirect( url_for('friends'))


#-------------------------------------------- Profile like and Comment ----------------------------------------------------------------------------------------------


#-------------------------------------------- Posts --------------------------------------------------------------------------------------------------------

@app.route("/addpost",methods=['GET','POST'])
@login_required
def add_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title = form.title.data, context = form.context.data, article = form.article.data, catagory=form.catagory.data, auther = current_user)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('addpost.html',form=form)


@app.route('/post/edit<int:post_id>', methods=['GET','POST'])
@login_required
def edit_post(post_id):
	form = PostForm()
	post=Post.query.get(post_id)
	if request.method =="GET":
		form.title.data = post.title
		form.context.data = post.context
		form.article.data = post.article
		form.image.data = post.image
	if request.method =="POST":
		post.title = form.title.data
		post.context = form.context.data
		post.article = form.article.data
		post.lastupdate = datetime.utcnow()
		db.session.commit()
		return redirect(url_for("index"))

	return render_template("edit_post.html", form=form)

@app.route('/post/delete<int:post_id>',methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	print(post)
	if post.auther != current_user:
		abort(403)
	else:
		db.session.delete(post)
		db.session.commit()

	return redirect(url_for("index"))

@app.route('/post/<int:post_id>',methods=["GET","POST"])
@login_required
def view_post(post_id):
	post = Post.query.get_or_404(post_id)
	commentform=CommentForm()
	comments=Comment.query.filter_by(post_comment=post)
	replayform=ReplayForm()
	if commentform.validate_on_submit():
		comment1=Comment(user_comment=current_user, post_comment=post, contant=commentform.contant.data)
		db.session.add(comment1)
		db.session.commit()
		return render_template("view_post.html", post=post, commentform=commentform, comments=comments, replayform=replayform)
		
	# if replayform.validate_on_submit():
	# 	replay1=Comment(user_comment=current_user, post_comment=post, contant=commentform.contant.data)
	# 	db.session.add(replay1)
	# 	db.session.commit()
	# 	comment_.add_replay(replay1)
	# 	db.session.commit()
		# return render_template("view_post.html", post=post, commentform=commentform, comments=comments, replayform=replayform)

	return render_template("view_post.html", post=post, commentform=commentform, comments=comments, replayform=replayform)

@app.route('/post/<int:post_id>/like',methods=["GET","POST"])
@login_required
def post_like(post_id):
	post_liker=Post.query.get_or_404(post_id)
	post_liked = PostLike.query.filter_by(user_like=current_user,post_like=post_liker).first()
	
	if not(post_liked):
		like = PostLike(post_like=post_liker,user_like=current_user)
		db.session.add(like)
		db.session.commit()
	elif post_liked:
		db.session.delete(post_liked)
		db.session.commit()
	return redirect(url_for("view_post", post_id=post_id))

#------------------------------------------- Chats ------------------------------------------------------------------------------------------------


#------------------------------------------- Authontication ------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		try:
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
		except:
			print("user don'r exsist")
			return redirect(url_for("login"))
	
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

#------------------------------------------- ABOUT ------------------------------------------------------------------------------------------------

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
	form=ProfileForm()
	if request.method == "GET":
		form.first_name.data=current_user.first_name
		form.mid_name.data=current_user.mid_name
		form.last_name.data=current_user.last_name
		form.gender.data=current_user.gender
		form.phone_number.data=current_user.phone_number
		form.address.data=current_user.address
		form.birth_day.data=current_user.birth_day

	if request.method=="POST":
		current_user.first_name=form.first_name.data
		current_user.mid_name=form.mid_name.data
		current_user.last_name=form.last_name.data
		current_user.gender=form.gender.data
		current_user.phone_number=form.phone_number.data
		current_user.address=form.address.data
		current_user.birth_day=form.birth_day.data
		db.session.commit()
		return redirect(url_for("profile"))

	return render_template("profile.html", form=form)


