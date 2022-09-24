from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import * 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.user import User 
import re
from flask_login import login_user, login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3
from app import *
from models.images import Image
from peewee import prefetch 
from models.follow import Follow
from models.likes import Likes


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
#     query = User.delete().where(User.username == 'stephaniechiu')
    query_ = User.delete_by_id(9)
    query_.execute()
    return render_template('/users/new.html')


@users_blueprint.route('/create-new', methods=['POST'])
def create():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    reenter_password = request.form['reenter_password']
    email = request.form['email']
    # birth_date = request.form['birth_date']

    if password != reenter_password:
        flash("Passwords do not match. Please reenter details.")

    new_user = User(name = name, username=username, password = password, email = email)

    if new_user.save():
        user = User.get_or_none(User.name == username)
        session['user_id'] = user.id
        login_user(user)
        return redirect(url_for('users.show', show_user = user, show_username = username))
    
    else:
        return redirect('/users/new')
    

@users_blueprint.route('/profile/<show_username>', methods=["GET"])
@login_required
def show(show_username):
    
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
    else:
        user = None 
    
    show_user = User.get_or_none(User.username == show_username)

    if show_user:
        show_username = show_user.username
        images = Image.select().where(Image.user_id == show_user.id).order_by(Image.date_posted.desc())
        approval_record = Follow.get_or_none(Follow.follower == user, Follow.idol == show_user)
        show_idols = User.select().join(Follow, on = Follow.idol_id == User.id).where(Follow.follower_id == show_user.id, Follow.approved == "1")
        length_si = show_idols.count()
        user_liked = Image.select().join(Likes, on = Likes.liker_id == user.id).where(Likes.image_id == Image.id)


        return render_template('/users/profile.html', show_user = show_user, approval_record = approval_record, images = images, 
        show_idols = show_idols,  length_si = length_si, user_liked = user_liked)

        
    else:
        return redirect (url_for('login.new'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return redirect('/users/new')


@users_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    # user = User.get_or_none(User.id == session['user_id'])
    # if not user:
    #     user = None 
    return render_template("/users/edit.html", show_user = current_user )


@users_blueprint.route('/update/<field>', methods=['POST'])
@login_required
def update(field):
    # if session.get('user_id'):
    #     user = User.get_or_none(User.id == session['user_id'])
    if current_user:
        new_info = request.form[field]
            
        if field == "email":
            email_existing = User.get_or_none(User.email == new_info)
            if email_existing:
                flash("There is an existing account associated with this email.")
                return redirect (url_for('users.edit'))
            
        if field == "username":
            existing_username = User.get_or_none(User.username == new_info)
            if existing_username:
                flash("Sadly, this username has been taken. Please choose another.")
                return redirect (url_for('users.edit'))
            
        if field == "password":
            reenter_password = request.form['reenter_password']

            if new_info != reenter_password:
                flash("Passwords do not match. Please reenter details.")
                return redirect (url_for('users.edit'))

        if field == "privacy":
            if new_info == "Public":
                new_info = "1"
            else:
                new_info = "0"

        setattr(current_user, field, new_info)
        current_user.save()

        flash("Your info has been updated.")
    else:
        flash("An error occured, please try again.")
    return redirect (url_for('users.edit'))

    # else:
    #     flash("An error occured, please try again.")
    #     return redirect (url_for('users.edit'))


@users_blueprint.route('/upload')
@login_required
def upload():
    # user = User.get_or_none(User.id == session['user_id'])
    # if not user:
    #     user = None 

    return render_template ("/users/upload.html")


@users_blueprint.route('/upload/profilepic/', methods=['POST'])
@login_required
def newpic():
    
    user = User.get_or_none(User.id == session['user_id'])
    
    if not user:
        user = None 
    
    else:
        print(request.files["profilepic"])

        if "profilepic" not in request.files:
            flash ("No profilepic key in request.files.")
            return redirect(url_for('users.upload'))

        file = request.files["profilepic"]

        if file.filename == "":
            flash("Please attach a file.")
            return redirect(url_for('users.upload'))

        file.filename = secure_filename(file.filename)
        print(file.filename)
        image_path = upload_file_to_s3(file, app.config["S3_BUCKET"])

        print(image_path)

        user.image_path = image_path 

        if user.save():
            flash("Image uploaded successfully!")
            return redirect(url_for('users.upload'))
        else:
            flash("Image upload unsuccessful. Please try again.")
            return redirect(url_for('users.upload'))
    
    return redirect(url_for('users.upload'))



@users_blueprint.route('/<show_username>/follow')
@login_required
def follow(show_username):
    
    user = User.get_or_none(User.id == session['user_id'])
    follower = user
    idol = User.get_or_none(User.username == show_username)
    privacy = idol.privacy
    approval_record = Follow.select().where(Follow.follower == follower, Follow.idol == idol)

    if approval_record:
        record_to_delete = Follow.get_or_none(Follow.follower == follower, Follow.idol == idol)
        record_to_delete.delete_instance()
        already_following = False
        flash(f"You are no longer following {show_username}")
        return redirect(url_for('users.show', user = user, show_user = idol, show_username = show_username,
        already_following = already_following, approval_record = approval_record))
    
    elif Follow.create(idol = idol, follower = user, approved = privacy):
        flash(f"Congratulations! You are now following {show_username}")
        already_following = True 
        return redirect(url_for('users.show', user = user, show_user = idol, show_username = show_username,
        already_following = already_following, approval_record = approval_record))

    else:
        return redirect('/404.html')


@users_blueprint.route('/approve')
@login_required
def approve():
    user = User.get_or_none(User.id == session['user_id'])
    user_followers = User.select().join(Follow, on = Follow.follower_id == User.id).where(Follow.idol_id == user.id, Follow.approved == "1")
    requests = Follow.select().where(Follow.idol_id == user.id, Follow.approved == "0")
    length_sf = user_followers.count()

    return render_template ("/users/approve.html", requests = requests, user_followers = user_followers, length_sf = length_sf)


@users_blueprint.route('/approve_done/<follow_id>', methods = ["POST"])
@login_required
def approve_done(follow_id):
    user = User.get_or_none(User.id == session['user_id'])
    record = Follow.get_or_none(Follow.id == follow_id)
    decision = request.form['decision']

    if decision == "Yes":
        record.approved = "1"
        record.save()
        # setattr(record, "approved", "1")
        # record.save()
    
    else: 
        record.delete_instance()
    
    requests = Follow.select().where(Follow.idol_id == user.id, Follow.approved == "0")
    user_followers = User.select().join(Follow, on = Follow.follower_id == User.id).where(Follow.idol_id == user.id, Follow.approved == "1")
    length_sf = user_followers.count()
    
    return render_template ("/users/approve.html", requests = requests, user_followers = user_followers, length_sf = length_sf)


    


