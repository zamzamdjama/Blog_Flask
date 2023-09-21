from base import *



# Register
@app.route('/register',methods=["GET","POST"])
def register():
    user=""
    if request.method== "POST":
        user=User.query.filter_by(email=request.form['email'], username=request.form['username'])
        try:
            
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            new_user=User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            flash("cette utilisateur existe deja, Veuiilez réessayez")
            return render_template('register.html')   
    
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
 
  

# Logout
@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)
    return redirect('/')




# ---------------  Routes  ----------------------------


# index
@app.route('/')
def index():
    posts= Postpublie.query.order_by(Postpublie.id.desc()).limit(10) 
    #  posts = Postpublie.query.order_by(Postpublie.id.desc()).all()
    comments = Comments.query.order_by(Comments.id.desc()).all()
  
    Nbcomment=Comments.query.count()

    return render_template('home.html',titre='Djib Blogger - Home', posts=posts, comments=comments, Nbcomment=Nbcomment)


# about
@app.route('/about')
def about():
    posts= Postpublie.query.order_by(Postpublie.id.desc()).limit(3) 
    return render_template('about.html',titre='Djib Blogger - About', posts=posts)




# contact
@app.route('/contact',methods=["GET","POST"])
def contact():
    if request.method== "POST":
        name = request.form['name']
        email=request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        contact=Contact(name=name,email=email,subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        return redirect('/contact')

    return render_template('contact.html',titre='Djib Blogger - Contact')




@app.route('/contacts')
def contacts():
   
   contacts = Contact.query.order_by(Contact.id.desc()).all()
   
   return render_template('NiceAdmin/contacts.html',titre='Djib Blogger - contacts', contacts=contacts)




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
    return render_template('createpost.html', titre="Djib Blogger - création des articles", user=user)


# posts
@app.route('/posts')
def posts():
  
    posts = Postpublie.query.order_by(Postpublie.id.desc()).all()
    comments = Comments.query.order_by(Comments.id.desc()).all()
    
    
  
    Nbcomment=Comments.query.count()
    
    

    return render_template('posts.html',title='Djib Blogger - Articles', posts=posts, comments=comments, Nbcomment=Nbcomment)    


@app.route('/posts/<int:post_id>',methods=["GET","POST"])
def comments(post_id):
    
    # post=Postpublie.query.get_or_404(post_id)
    # posts = Postpublie.query.order_by(Postpublie.id.desc()).all()
    # comments = Comments.query.filter_by(post_id=Postpublie.id).all()
    
   
    try:

        if request.method == "POST":
            name = request.form.get('nom')
            email=request.form.get('email')
            message = request.form.get('message')
            post_id=post_id
            comment=Comments(name=name,email=email,message=message, post_id=post_id)
            db.session.add(comment)
            # Nbcomment=Comments.query.filter_by(post_id=post.id).count()
            # post.comments += 1
            db.session.commit()
           
            return redirect('/posts')
    except:
        pass
    return render_template('comments.html')  




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

@app.route('/Blog-rejeter/<int:id>/delete')
def BlogrejeterAjoutP(id):
    Blog = db.get_or_404(PostAttent, id)
    newBlog=PostRejeter(title=Blog.title,body=Blog.body,Nom=Blog.Nom, image=Blog.image)
    blogdelete=db.get_or_404(PostAttent, id)
    db.session.delete(blogdelete)
    db.session.add(newBlog)
    db.session.commit()
    if newBlog:
       return redirect(url_for('BlogRejeter'))
   
    return render_template('NiceAdmin/BlogRejeter.html')

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




    