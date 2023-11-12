from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
from . import login_manager

from app import db

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()        
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)         
    
    def __repr__(self):
        return '<User %r>' % self.username  

class AnonymousUser(AnonymousUserMixin):
    
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    