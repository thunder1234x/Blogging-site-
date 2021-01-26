from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask.ext.store import Store


app=Flask(__name__)

ENV='dev'

if ENV=='dev':
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:rakesh@localhost/posts'
else:
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://utvprwurfuvkkp:27abc80aa5e45582c70624f1d92e21bb00fea8a50a96ad04b93e2d6807e583f6@ec2-54-166-114-48.compute-1.amazonaws.com:5432/d7bthrsk320b1f'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
# app.config['STORE_DOMAIN'] = 'http://127.0.0.1:5000'
# app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
# store=Store(app)

class Blog_post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author_id=db.Column(db.Integer,db.ForeignKey('user_details.id'))
    time_created=db.Column(db.DateTime,nullable=False,default=datetime.now())

    def __repr__(self):
        return 'Blog post ' +str(self.id)

class User_details(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(60),nullable=False)
    last_name=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(20),nullable=False)
    post=db.relationship('Blog_post',backref='owner' ,lazy=True)
    

    def __repr__(self):
        return self.id



if __name__ == '__main__':
   db.create_all()
    