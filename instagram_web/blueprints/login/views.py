from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import * 
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User 
import re
from app import *
from flask_login import login_user, LoginManager, logout_user, login_required
from models.images import Image
from instagram_web.util.google_oauth import oauth
import random 
import string 


login_blueprint = Blueprint('login',
                            __name__,
                            template_folder='templates')


@login_blueprint.route('/')
def new():
    return render_template('login/new.html')


@login_blueprint.route('/login-create', methods=["POST"])
def create():
    username = request.form['username']
    password = request.form['password']

    user = User.get_or_none(User.username == username)
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        images = Image.select().where(Image.user_id == user.id)
        login_user(user)
        return redirect(url_for('users.show', user = user, show_user = user, show_username = username, images = images))

    else: 
        flash("Invalid username and/or password. Please enter your details again.")
        return redirect('/login')


@login_blueprint.route('/<username>/logout', methods=["POST"])
def destroy(username):
    
    user = User.get_or_none(User.username == username)
    session['user_id'] = None
    # User.get_or_none(User.email == 'alettengxinling@gmail.com').delete_instance()
    logout_user()
    return redirect (url_for('home'))


@login_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('login.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@login_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    google_info = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
    email = google_info['email']

    user = User.get_or_none(User.email == email)
    if user: 
        user = User.get_or_none(User.email == email)
        session['user_id'] = user.id
        login_user(user)

        return redirect(url_for('home', user = user, show_user = user))
    
    else:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(10))
        new_user = User(name = email, username = email, password = password, email = email)

        if new_user.save():
            user = User.get_or_none(User.email == email)
            session['user_id'] = user.id
            login_user(user)
            
            flash("Please update your password and choose a username before proceeding onto other pages.")
            return redirect(url_for('users.edit', user = user, show_user = user))
        
        else:
            return redirect('/users/new')

