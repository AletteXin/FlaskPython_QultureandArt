from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import * 
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User 
import re

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('/users/new.html')


@users_blueprint.route('/create-new', methods=['POST'])
def create():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    reenter_password = request.form['reenter_password']
    email = request.form['email']
    birth_date = request.form['birth_date']

    if password != reenter_password:
        flash("Passwords do not match. Please reenter details.")

    new_user = User(name = name, username=username, password = password, email = email, birth_date = birth_date)

    if new_user.save():
        user = User.get_or_none(User.username == username)
        session['user_id'] = user.id
        flash("You have signed up successfully! Here is your profile page. Explore around!")
        return redirect(url_for('users.show', username = username))
    
    else:
        return redirect('/users/new')
    

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    
    if session.get('user_id'):
        user = User.get_or_none(User.id == session['user_id'])
        if user:
            username = user.username
        else:
            username = None 
        return render_template("/users/profile.html", username = username)

    else:
        return redirect (url_for('login.new'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
