from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Profile-related fields
    headline = db.Column(db.String(150))
    current_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    skills = db.Column(db.Text)  # e.g., "Python,Flask,SQL"
    education = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    profile_pic = db.Column(db.String(120), default='default.jpg')

    # Timestamps
    date_joined = db.Column(db.DateTime, default=datetime.now())

    # Relationships (optional, for future features like posts, connections)
    posts = db.relationship('Post', backref='author', lazy=True)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
