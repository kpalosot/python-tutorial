'''
Database Module
'''
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    '''
    app needs to have this function so that flask-login
    can keep track of logged in users
    '''
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    '''
    User Class
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        '''
        Setting user's password to hashed password
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
        Checking to see if password provided matches stored hashed password
        '''
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    '''
    Post Class
    '''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
