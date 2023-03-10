from . import db
from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash
from .models import Users, Posts, Replies
from datetime import timedelta, datetime
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash 


views = Blueprint("views",  __name__)

@views.route('/')
def home():
    return render_template("openmind.html")


@views.route('/register',  methods=['GET', 'POST'] )
def register():
    if request.method == "POST":
        name= request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        username_exists = Users.query.filter_by(username = username).first()
        email_exists = Users.query.filter_by(email = email).first()
        if password1 != password2:
            flash("Passwords don't match!")
        elif username_exists or email_exists:
            flash('username or email already exists!')
        elif len(password1) < 6 or len(username) <6:
            flash("Username or password must contain more than 6 characters")
        else:
            new_user = Users(name = name, username = username, email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['loggedin'] = True
            flash('sign up sucessful', 'info')
            return redirect(url_for('views.home'))


    return render_template("register.html")

@views.route('/login',  methods=["GET", "POST"] )
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        permanentsesh =request.form.get('permanentsession')
        user = Users.query.filter_by(username=username).first() #Users is database with all the users
       #the line above will create a new child in the class User
       #stores as first because usernames are unique and will always be the first option
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=user.email)
                print('Logged in')
                if permanentsesh:
                    session.permanent = True
                else:
                    session.permanent = False
                session['loggedin'] = True
                session['email'] = user.email
                flash('Log in sucessful', 'info ')
                return redirect(url_for('views.home')) 
            else:
                print('Wrong Password')
        else:
            print('Username does not exist')

    return render_template("login.html")

@views.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get('content')
        poster = current_user.id
        post = Posts(title=title, content=content, poster_id=poster)

        db.session.add(post)
        db.session.commit()

        flash('Event created sucessfully')
        print('post sucessful')

        return redirect(url_for('views.posts'))

    return render_template("create.html")

@views.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_added)
    return render_template("posts.html", posts=posts)


@views.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    replies = Replies.query.filter_by(replyposts=id).all()
    
    
    return render_template('post.html', post=post, replies=replies)
    

@views.route("/post/<int:id>/reply", methods=["GET", "POST"])
def reply(id):
    if request.method == "POST":
        content = request.form.get("content")
        post=Posts.query.filter_by(id=id).first()
        reply = Replies(text=content, replier=current_user.id, replyposts=post.id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('views.post', id=id))

    return render_template("reply.html")


