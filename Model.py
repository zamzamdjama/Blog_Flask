# from flask import *
# from flask_sqlalchemy import SQLAlchemy
# db=SQLAlchemy()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# db.init_app(app)
# class User(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     username=db.Column(db.String)
#     email=db.Column(db.String)
#     password=db.Column(db.String, unique=False, nullable=False)
# with app.app_context():
#     db.create_all()


from flask import *
from datetime import datetime  
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
from flask_login import *
from flask_migrate import Migrate


# app= Flask(__name__) 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/blog'


# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# session(app)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'users'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql=MySQL(app)

# db=SQLAlchemy(app)
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
    comments = db.Column(db.Integer,default=0)

def __init__(self, title, body, Nom, image, date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.date_pub=date_pub
    self.image=image

with app.app_context():
    db.create_all()    
    
    
class Postpublie(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    #person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(150))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, title, body, Nom,image ,date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.image=image
    self.date_pub=date_pub

with app.app_context():
    db.create_all()   
    
class PostAttent(db.Model):
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

# table comments

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref('posts',lazy=True,
    passive_deletes=True))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)




# Index
@app.route('/')
def index():
    posts= Post.query.order_by(Post.id.desc()).limit(2) 
    return render_template('index.html',posts=posts)


# Register
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method== "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user=User(username=username,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    return render_template('register.html')

# Login
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        email = request.form['email']
        password = request.form['password']
        user=User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['username']=user.username
            session['email']=user.email
            session['password']=user.password

            return redirect('/addpost')
        else:
            flash("Votre email ou votre mot de passe est incorrect, Veuiilez réessayez")
            return render_template('login.html')   
        
    return render_template('login.html')

# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.id)).scalars()
#     return render_template("user/list.html", users=users)

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)
    session.pop('user.email',None)
    session.pop('user.username',None)
    userDelete=db.session.delete(user)
    db.session.commit()
    

    if   not userDelete:
        return redirect(url_for('GestionUser'))
        

    return render_template("NiceAdmin/tables-data.html") 
 
# @app.route("/user/<int:id>/update", methods=["GET", "POST"])
# def user_update(id):
#     user = db.get_or_404(User, id)

#     if request.method == "POST":
#         user.username=request.form['username']
#         user.email=request.form['email']
#         db.session.commit()
#         flash('Modification Effectuée','update')
#         return redirect(url_for("users"))
#     return render_template("/user/edit.html", user=user)     

# Dashboard admin
@app.route('/dashboardadmin')
def AdminDashboard():
    return render_template('DashboardAdmin.html')



@app.route('/navpost')
def navpost():
       if session['username']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('navpost.html',user=user)


# Logout
@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)
    return redirect('/')



@app.route('/base')
def base():
    return render_template('base.html')    


# Add post
@app.route('/addpost',methods=["GET","POST"])
def addpost():
    if request.method== "POST":
        title = request.form['titre']
        Nom=request.form['auteur']
        body = request.form['contenu']
        image = request.form['image']
        
        # image = request.form['image']
        new_post=PostAttent(title=title,body=body,Nom=Nom, image=image)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    
    user = User.query.filter_by(email=session['email']).first()
    return render_template('createpost.html', titre='création des articles',user=user)

# posts
@app.route('/posts')
def posts():
    posts= Postpublie.query.all()
     
    return render_template('posts.html',posts=posts)    

# Latest_articles
@app.route('/Latest_articles')
def Latest_articles():
    
    posts= Post.query.order_by(Post.id.desc()).limit(2) 

    return render_template('Latest_articles.html',posts=posts)


@app.route('/NiceAdmin')
def NiceAdmin():
    nombreBlogAttent=PostAttent.query.count()
    nombreBlogRejeter=PostRejeter.query.count()
    nombreBlogPublier=Postpublie.query.count()
    dernierBlog=db.session.query(Postpublie).order_by(Postpublie.id.desc()).limit(1).all()
    users=db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template('NiceAdmin/index.html', nombreBlogAttent=nombreBlogAttent, nombreBlogRejeter=nombreBlogRejeter, nombreBlogPublier=nombreBlogPublier,dernierBlog=dernierBlog,users=users )



@app.route("/user/<int:id>/update")
def user_update(id, userName='', Email=''):
    user = db.get_or_404(User, id)

    
    user.username=userName
    user.email=Email
       
 
       
    
    db.session.commit()
    flash('Modification Effectuée','update')
        
        
    return user
















@app.route('/users-profile/<int:id>/update', methods=["GET", "POST"])
def usersProfileModifier(id):
    users=db.session.execute(db.select(User).order_by(User.id)).scalars()


    if request.method == "POST" :
       
        user=user_update(id,request.form['username'], request.form['email'])
        return redirect(url_for("GestionUser"))
   
    return render_template('NiceAdmin/users-profile.html',users=users, id=id)








@app.route("/user/<int:id>/update-pass")
def user_updatepass(id,  newpass=""):
    user = db.get_or_404(User, id)

   
        
    user.password= newpass
       
    
    db.session.commit()
    flash('Modification Effectuée','update')
        
        
    return user



@app.route('/users-profile/<int:id>/update-password', methods=["GET", "POST"])
def passwordProfileModifier(id):
    users=db.session.execute(db.select(User).order_by(User.id)).scalars()


    if request.method == "POST":
       
        user=user_updatepass(id,request.form['newpassword'])
        return redirect(url_for("GestionUser"))
   
    return render_template('NiceAdmin/users-profile.html',users=users, id=id)





@app.route('/users-profile')
def usersProfile():
    return render_template('NiceAdmin/users-profile.html')

@app.route('/utilisateur')
def GestionUser():
    users=db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template('NiceAdmin/tables-data.html', users=users)











# blog




@app.route('/Blog-attent')
def BlogAttent():
    BlogAttent= PostAttent.query.order_by(PostAttent.date_pub)
    return render_template('NiceAdmin/BlogAttend.html', BlogAttent=BlogAttent)




# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)
@app.route('/Blog-publier/<int:id>/Ajout')
def BlogPublierAjout(id):
    Blog = db.get_or_404(PostAttent, id)
    newBlog=Postpublie(title=Blog.title,body=Blog.body,Nom=Blog.Nom, image=Blog.image)
    blogdelete=db.get_or_404(PostAttent, id)
    db.session.delete(blogdelete)
    db.session.add(newBlog)
    db.session.commit()
    if newBlog:
       return redirect(url_for('BlogPublier'))
  
    return render_template('NiceAdmin/BlogPublier.html')

@app.route('/Blog-publier')
def BlogPublier():

    BlogPublie=db.session.execute(db.select(Postpublie).order_by(Postpublie.id)).scalars()

    return render_template('NiceAdmin/BlogPublier.html',BlogPublie=BlogPublie )




@app.route('/Blog-rejeter')
def BlogRejeter():
    BlogRejeter=db.session.execute(db.select(PostRejeter).order_by(PostRejeter.id)).scalars()
    return render_template('NiceAdmin/BlogRejeter.html',BlogRejeter=BlogRejeter)


@app.route('/Blog-rejeter/<int:id>/delete')
def BlogrejeterAjout(id):
    Blog = db.get_or_404(PostAttent, id)
    newBlog=PostRejeter(title=Blog.title,body=Blog.body,Nom=Blog.Nom, image=Blog.image)
    blogdelete=db.get_or_404(PostAttent, id)
    db.session.delete(blogdelete)
    db.session.add(newBlog)
    db.session.commit()
    if newBlog:
       return redirect(url_for('BlogRejeter'))
   
    return render_template('NiceAdmin/BlogRejeter.html')




@app.route('/Blog-rejeter/<int:id>/deleteDef')
def BlogrejeterAjoutDef(id):
    Blog = db.get_or_404(PostRejeter, id)
   
    BlogSupp=db.session.delete(Blog)
   
    db.session.commit()
    
    if BlogSupp:
       return redirect(url_for('BlogRejeter'))
   
    return render_template('NiceAdmin/BlogRejeter.html')

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404








if __name__=='__main__':
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=3000)




    