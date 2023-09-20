from flask import *
from datetime import datetime  
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
from flask_login import *
from flask_migrate import Migrate




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/blog'

db = SQLAlchemy()
migrate=Migrate(app, db)
db.init_app(app)
app.secret_key='this_is_my_secret_key'

# Create table User
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), unique=True)
    
    password= db.Column(db.String(100))
    

    def __init__(self, email, password, username):
        self.username=username
        self.email=email
       
        self.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
with app.app_context():
    db.create_all()   

# Create table Post

class Post(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(150))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

def __init__(self, title, body, Nom, image, date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.date_pub=date_pub
    self.image=image

with app.app_context():
    db.create_all()    
    


# Create table Postpublie

class Postpublie(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    #person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(150))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # comments = db.Column(db.Integer,default=0)


def __init__(self, title, body, Nom,image ,date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.image=image
    self.date_pub=date_pub

with app.app_context():
    db.create_all()   



# create table comments
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('postpublie.id', ondelete='CASCADE'), nullable=False)
    post = db.relationship('Postpublie', backref=db.backref('posts',lazy=True))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, name, email, message,post_id, date_pub):
    self.name=name
    self.email=email
    self.message=message
    self.post_id=post_id
    self.date_pub=date_pub

with app.app_context():
    db.create_all()   

    
class PostAttent(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
   
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    
    image = db.Column(db.String(150))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, title, body, Nom,image, date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.image=image
    self.date_pub=date_pub

with app.app_context():
    db.create_all() 
    
class PostRejeter(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    #person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    
    image = db.Column(db.String(150))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, title, body, Nom,image, date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.image=image
    self.date_pub=date_pub

with app.app_context():
    db.create_all()   


