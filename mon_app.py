# from flask import *
# from flask_sqlalchemy import SQLAlchemy
# db=SQLAlchemy(app)
# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')

# def profile(username):
#     return f"Profil de l'utilisateur{username}"
# def login():
#     if request.method=='POST':
#         return 'connexion reussie'
#     else:
#         return render_template('login.html')
# class User(db.Model):
#     id=db.Column    



# if __name__=='__main__':
#     app.run(debug=True, port=3000)