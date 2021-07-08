from models import * 
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app import *
from flask_login import login_user, LoginManager, logout_user, login_required

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new')
@login_required
def new():
    user = User.get_or_none(User.id == session['user_id'])
    if user:
        username = user.username
    else:
        username = None 

    return render_template('/images/new.html', username = username)


@images_blueprint.route('/')
@login_required
def create():
    
    user = User.select().where(User.id == session['user_id'])
        
    if user: 
        username = user.username
        story_image = request.form["story_image"]
        story_description = request.form["story_description"]

        if (story_image == "") or (story_description == ""):
            flash("Please attach a file and fill in the description box.")
            return redirect('/new')
            
        else:
            story_image.filename = secure_filename(story_image.filename)
            image_path = upload_file_to_s3(file, app.config["S3_BUCKET"])
            new_image = Image(image_path = image_path, user_id = user.id, description = story_description)
                
            if new_image.save():
                flash("Story uploaded successfully!")
                return redirect(url_for('images.new', username = username))

            else:
                flash("Story upload unsuccessful. Please try again.")
                return redirect(url_for('images.new', username = usermame))

    return redirect('/new')


@images_blueprint.route('/<id>/edit')
def edit():
    pass


@images_blueprint.route('/<id>')
def update():
    pass


@images_blueprint.route('/<id>')
def show():
    pass


@images_blueprint.route('/')
def index():
    pass


@images_blueprint.route('/<id>/delete')
def destroy():
    pass


    