from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin





post_identifier = db.Table('post_identifier',
                           db.Column('post_id', db.Integer,
                                     db.ForeignKey('category.id')),
                           db.Column('category_id', db.Integer,
                                     db.ForeignKey('post.id'))
                           )

                           
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    categories = db.relationship('Category', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}\
                ({self.id}, {self.name}, {self.username})'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}\
                ({self.id}, {self.title[:32]}, {self.date})'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship("Post", secondary=post_identifier)

    def __repr__(self):
        return f'{self.__class__.__name__}\
                ({self.id}, {self.title[:32]})'
