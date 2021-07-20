from models import * 
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app import *
from flask_login import login_user, LoginManager, logout_user, login_required
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
from models.images import Image
from peewee import prefetch 
from models.likes import Likes


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new')
@login_required
def new():
    user = User.get_or_none(User.id == session['user_id'])
    if not user:
        
        user = None 

    return render_template('/images/new.html', user = user)


@images_blueprint.route('/', methods = ["POST"])
@login_required
def create():
    
    user = User.get_or_none(User.id == session['user_id'])

    story_image = request.files['story_image']
    story_description = request.form['story_description']
    story_title = request.form['story_title']

    if (story_image == "") or (story_description == "") or (story_title == ""):
        flash("Please complete all fields.")
        return redirect('/new')
            
    else:
        story_image.filename = secure_filename(story_image.filename)
        image_path = upload_file_to_s3(story_image, app.config["S3_BUCKET"])
        new_image = Image(image_url = image_path, user_id = user.id, description = story_description, title = story_title)
        
                
        if new_image.save():
            flash("Story uploaded successfully!")
            return redirect(url_for('images.new', user = user))

        else:
            flash("Story upload unsuccessful. Please try again.")
            return redirect(url_for('images.new', user = user))

    return redirect('/new')


@images_blueprint.route('/<id>/edit')
@login_required
def edit(id):
    story_to_edit = Image.get_or_none(Image.id == id)

    if story_to_edit.user_id == session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])

        return render_template ('/images/edit.html', id = id,  story_to_edit = story_to_edit, user = user)

    else: 
        return redirect('/401.html')

@images_blueprint.route('/update/<id>/', methods = ["POST"])
@login_required
def update(id):
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        username = user.username
        image_to_edit = Image.get_or_none(Image.id == id)
    
    if user.id == image_to_edit.user_id:
        
        story_title = image_to_edit.title
        story_description = image_to_edit.description
        story_image_url = image_to_edit.image_url
        new_title = request.form['new_title']
        new_description = request.form['new_description']
        file = request.files["new_image"]

        if file.filename == "":
            image_path = story_image_url
        else:
            file.filename = secure_filename(file.filename)
            image_path = upload_file_to_s3(file, app.config["S3_BUCKET"])
        
        if new_description == "":
            new_description = story_description 
        if new_title == "":
            new_title = story_title

        setattr(image_to_edit, 'title', new_title)
        setattr(image_to_edit, 'description', new_description)
        setattr(image_to_edit, 'image_url', image_path)

        if image_to_edit.save():
            flash("Post successfully updated.")
            return redirect(url_for('images.edit', id = id))

    else:
        return redirect('/404.html')


@images_blueprint.route('/<id>')
def show():
    pass


@images_blueprint.route('/')
def index():
    pass


@images_blueprint.route('/<id>/delete')
@login_required
def destroy(id):

    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
    else:
        return redirect('/404.html')

    image_to_delete = Image.get_or_none(Image.id == id)
    image_user_id = image_to_delete.user_id

    if user.id == image_user_id:
        
        images = Image.select().where(Image.user_id == user.id)
        image_to_delete.delete_instance()
        flash ("Post deleted successfully!")
        return redirect(url_for('users.show', user = user, show_user = user, show_username = user.username, images = images))

    else:
        return redirect('/404.html')


@images_blueprint.route('/<id>/like')
@login_required
def like(id):
    
    user = User.get_or_none(User.id == session['user_id'])
    liker = user
    image = Image.get_or_none(Image.id == id)
    like_record = Likes.select().where(Likes.liker == liker, Likes.image == image)
    show_user = User.get_or_none(User.id == image.user_id)
    show_username = show_user.username


    if like_record:
        record_to_delete = Likes.get_or_none(Likes.liker == liker, Likes.image == image)
        record_to_delete.delete_instance()
        image_likes = Likes.select().where(Likes.image == id)
        length_likes = image_likes.count()
        image.likes = length_likes 
        image.save()
        # return redirect(url_for('users.show', user = user, show_user = show_user, 
        # show_username = show_username, length_likes = length_likes))
        return redirect(request.referrer)
    
    elif Likes.create(liker = liker, image = image):
        image_likes = Likes.select().where(Likes.image == id)
        length_likes = image_likes.count()
        image.likes = length_likes 
        image.save()
        # return redirect(url_for('users.show', user = user, show_user = show_user, 
        # show_username = show_username, length_likes = length_likes))
        return redirect(request.referrer)

    else:
        return redirect('/404.html')


    