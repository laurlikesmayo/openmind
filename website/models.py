from . import db
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime

#puts all the users information into the database
class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    name= db.Column("name", db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    posts = db.relationship('Posts', backref='poster')
    replier = db.relationship("Replies", backref='replier')

class Posts(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text(1000))#not a string but text cuz it a lot bigger
    #author = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship("Replies", backref='replyto')

class Replies(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    replyto = db.Column(db.Integer, db.ForeignKey("posts.id"))
    text = db.Column(db.Text(1000))
    replier=db.Column(db.Integer, db.ForeignKey("users.id"))
