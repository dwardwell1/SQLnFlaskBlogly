"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

dt = datetime.today().replace(microsecond=0)

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} profile pic={u.img_url}>"
    #default image
    phImage = "https://icon-library.com/images/person-image-icon/person-image-icon-7.jpg"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30))
    img_url = db.Column(db.Text, nullable=False, default=phImage)
    posts = db.relationship('Post', backref='user',cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<post id = {p.id} title = {p.title} content = {p.content} time_posted = {p.created_at} poster = {p.poster.first_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # poster = db.relationship('User', backref='user')
    tags = db.relationship('Tag', secondary='posttags', backref='post')
    

class PostTag(db.Model):
    __tablename__= 'posttags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id' ), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id' ), primary_key=True)
    

class Tag(db.Model):
    __tablename__='tags'

    def __repr__(self):
        t = self
        return f"{t.name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    
#how did adding array of tags work?