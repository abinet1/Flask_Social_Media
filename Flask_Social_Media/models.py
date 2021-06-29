from enum import unique
from sqlalchemy.orm import undefer
from Flask_Social_Media import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

requests = db.Table('requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('reciver_id', db.Integer, db.ForeignKey('user.id'))
)

friends = db.Table('friends',
    db.Column('first_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('second_id', db.Integer, db.ForeignKey('user.id'))
)

class Post(db.Model):
    title = db.Column(db.String(120), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    article = db.Column(db.Text, nullable=False, unique=False)
    postdate = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.now.utc)
    lastupdate = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.now.utc)

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

    def __repr__(self):
        return f"User('{self.id}','{self.first_name}','{self.last_name}','{self.phone_number}','{self.user_name}')"



