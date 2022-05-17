from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy="dynamic")
    likes = db.relationship('Like', backref='user', lazy="dynamic")
    comments = db.relationship('Comment', backref='author', lazy="dynamic")
        
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    category= db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    pitch= db.Column(db.Text)
    link= db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('Like', backref='post', lazy="dynamic")
    comments = db.relationship('Comment', backref='post', lazy="dynamic")

    def getcomments(self):
        a = []

        for comment in self.comments:
        
            print(comment)
            a.append(comment)
        return a

    def __repr__(self):
        return f"Post('{self.category}', '{self.date_posted},{self.getcomments()}')"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    text= db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def  __init__ (self, text,post_id):
        self.text = text
        self.post_id = post_id

    def __repr__(self):
        return f"Comment('{self.text}', '{self.date_posted}')"

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key = True)
    author= db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Like('{self.author}', '{self.date_posted}')"




    


         

