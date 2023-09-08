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
class User(db.Model, UserMixin):
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
    title = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    Nom = db.Column(db.String(200), unique=True, nullable=False)
    # image = db.Column(db.String(150), nullable=False, default='no-image.jpg')
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, title, body, Nom, date_pub):
    self.title=title
    self.body=body
    self.Nom=Nom
    self.date_pub=date_pub

with app.app_context():
    db.create_all()    

# Index
@app.route('/')
def index():
    return render_template('index.html')


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

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        flash("Suppression Effectuée","delete")
        return redirect(url_for("users"))

    return render_template("admin/users/delete.html", user=user) 
 
@app.route("/user/<int:id>/update", methods=["GET", "POST"])
def user_update(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        user.username=request.form['username']
        user.email=request.form['email']
        db.session.commit()
        flash('Modification Effectuée','update')
        return redirect(url_for("users"))
    return render_template("admin/users/edit.html", user=user)     

# Dashboard admin
@app.route('/dashboardadmin')
def AdminDashboard():
    return render_template('DashboardAdmin.html')


# admin login
@app.route('/admin/')
def adminIndex():
    return render_template('admin/index.html',title='Admin Login')

# user login
@app.route('/user/')
def userIndex():
    return render_template('user/index.html',title='User Login')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if session['username']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

# users
@app.route('/users')
def users():
    users= User.query.order_by(User.id)
    return render_template('admin/users/users.html',users=users)
    

# posts
@app.route('/posts')
def posts():
    posts= Post.query.order_by(Post.date_pub)
    return render_template('posts/posts.html',posts=posts)    

@app.route('/addpost',methods=["GET","POST"])
def addpost():
    if request.method== "POST":
        title = request.form['titre']
        Nom=request.form['auteur']
        body = request.form['contenu']
        # image = request.form['image']
        new_post=Post(title=title,body=body,Nom=Nom)
        db.session.add(new_post)
        db.session.commit()
        return url_for('posts')
    return render_template('posts/createpost.html', titre='création des articles')


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/NiceAdmin')
def NiceAdmin():
    return render_template('NiceAdmin/index.html')

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__=='__main__':
    # with app.app_context():
    #     db.create_all()
    
    app.run(debug=True, port=3000)




    