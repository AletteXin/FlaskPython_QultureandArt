from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import * 
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User 
import re
from app import *
from flask_login import login_user, LoginManager, logout_user, login_required

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
        login_user(user)
        return redirect(url_for('users.show', username = username))

    else: 
        flash("Invalid username and/or password. Please enter your details again.")
        return redirect('/login')


@login_blueprint.route('/<username>/logout', methods=["POST"])
def destroy(username):
    
    user = User.get_or_none(User.username == username)
    session['user_id'] = None
    logout_user()
    return redirect (url_for('home'))