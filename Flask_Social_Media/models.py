from enum import unique
from Flask_Social_Media import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

requests = db.Table('requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('reciver_id', db.Integer, db.ForeignKey('user.id')),
    # db.Column(db.DateTime,nullable=False, unique=False, default=datetime.now.utc)
)

friends = db.Table('friends',
    db.Column('first_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('second_id', db.Integer, db.ForeignKey('user.id')),
    # db.Column(db.DateTime,nullable=False, unique=False, default=datetime.now.utc)
)

follows = db.Table('follows',
    db.Column('first_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('second_id', db.Integer, db.ForeignKey('user.id')),
)

comments = db.Table('comments',
    db.Column('first_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('second_id', db.Integer, db.ForeignKey('comment.id')),
)

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
    posts = db.relationship('Post',backref="auther", lazy=True)
    comment = db.relationship('Comment',backref="user_comment", lazy=True)
    like = db.relationship('PostLike',backref="user_like", lazy=True)
    user_name = db.Column(db.String(30), nullable=False, unique=False)
    password = db.Column(db.String(60), nullable=False, unique=False)
    requested = db.relationship('User', 
                                secondary=requests, 
                                primaryjoin=(requests.c.sender_id == id), 
                                secondaryjoin=(requests.c.reciver_id == id), 
                                backref=db.backref('requests', lazy='dynamic'), 
                                lazy='dynamic')
    
    friendz = db.relationship('User',
                                secondary=friends,
                                primaryjoin=(friends.c.first_id==id),
                                secondaryjoin=(friends.c.second_id==id),
                                backref=db.backref('friend',lazy='dynamic'),
                                lazy='dynamic')

    followed = db.relationship('User',
                                secondary=follows,
                                primaryjoin=(follows.c.first_id==id),
                                secondaryjoin=(follows.c.second_id==id),
                                backref=db.backref('follows',lazy='dynamic'),
                                lazy='dynamic')
    
    def send_request(self, user):
        if not ( self.is_requested(user) or user.is_requested(self)):
            self.requested.append(user)
            return self
        elif user.is_requested(self):
            return "this user alredy send you request"
        else:
            return "error: unknoun"

    def cancel_request(self, user):
        if (self.is_requested(user) and (not(self.is_friends(user)))):
            self.requested.remove(user)
            return self
        elif (self.is_friends(user)):
            return "Already friends"
        
    def delete_request(self, user):
        if user.is_requested(self):
            user.requested.remove(self)
            return user
        else:
            return "you can't delete you can cancel though."

    def find_friend(self):
        users=User.query.all()
        friendss=self.friendz.all()
        friend=self.friend.all()
        requested=self.requested.all()
        requestted=self.requests.all()
        responce=[]
        for user in users:
            if not ((user in friendss) or (user in friend) or (user in requested) or (user in requestted) or (self == user)):
                responce.append(user)
        return responce

    def is_requested(self, user):
        return self.requested.filter(requests.c.reciver_id == user.id).count() > 0
    
    def confirm(self, user):
        if user.is_requested(self):
            self.friendz.append(user)
            user.requested.remove(self)
            return self
    
    def is_friends(self, user):
        if self.friendz.filter(friends.c.second_id == user.id).count() or user.friendz.filter(friends.c.second_id == self.id).count():
            return True
        else:
            return False

    def follow_User(self, user):
        if not (self.is_followed(user)):
            self.followed.append(user)
            return self
        elif self.is_followed(user):
            self.followed.remove(user)

    def is_followed(self, user):
        return self.followed.filter(follows.c.second_id == user.id).count() > 0

    def __repr__(self):
        return f"User('{self.id}','{self.first_name}','{self.last_name}','{self.phone_number}','{self.user_name}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    commented = db.relationship('Comment',
                                secondary=comments,
                                primaryjoin=(comments.c.first_id==id),
                                secondaryjoin=(comments.c.second_id==id),
                                backref=db.backref('comments',lazy='dynamic'),
                                lazy='dynamic')
    date = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.utcnow)
    contant = db.Column(db.Text, nullable=False, unique=False)
    
    def add_replay(self, replay):
        self.commented.append(replay)

    def all_replays(self):
       return self.commented.all()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=False)
    context = db.Column(db.Text, nullable=False, unique=False)
    article = db.Column(db.Text, nullable=False, unique=False)
    catagory = db.Column(db.String(10), nullable=False, unique=False, default="For All")
    image = db.Column(db.String(255), unique=False, default="picture1.jpg")
    postdate = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
    lastupdate = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
    comment = db.relationship('Comment',backref="post_comment", lazy=True)
    like = db.relationship('PostLike',backref="post_like", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    
    
    def __repr__(self):
        return f"post id('{self.id}','{self.title}','{self.postdate}','{self.lastupdate}','{self.user_id}','{self.auther.user_name}')"

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    