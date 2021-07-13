from app import *
from flask import render_template, session, flash, request, redirect, url_for
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager, login_user
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.login.views import login_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.payment.views import payment_blueprint 
from models.images import Image
from models.user import User
from peewee import prefetch 
from .util.payment import *
from instagram_web.util.google_oauth import oauth
from models.follow import Follow

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(payment_blueprint, url_prefix = "/payment")

oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        if user:
            username = user.username
        else:
            username = None
    return render_template('500.html', username = username), 500


@app.errorhandler(404)
def page_not_found(e):
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        if user:
            username = user.username
    else:
        username = None
    return render_template('404.html', username = username), 404


@app.errorhandler(401)
def unauthorized_entry(e):
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        if user:
            username = user.username
    else:
        username = None
    return render_template('401.html', username = username), 401



@app.route("/")
def home():
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        if user:
            idols = User.select().join(Follow, on = Follow.idol_id == User.id).where(Follow.follower_id == user.id, Follow.approved == "1")
    
    else:
        user = None 
        idols = []

    users = User.select()
    images = Image.select().order_by(Image.date_posted.desc())
    users_with_images = prefetch(images, users)

    return render_template('home.html', user = user, users_with_images = users_with_images, idols = idols)


@app.route("/searchbar", methods = ["POST"])

def site_search():
    
    if session.get('user_id'):
        user = User.get_or_none(User.id == session["user_id"])
        username = user.username
    
    else:
        user = None 
        username = None

    show_username = request.form['site-search']
    show_user = User.get_or_none(User.username == show_username)
        
    if show_user:
        show_profilepic = show_user.image_path
        show_description = show_user.description
        show_privacy = show_user.privacy 
        images = Image.select().where(Image.user_id == show_user.id).order_by(Image.date_posted.desc())
        approval_record = Follow.get_or_none(Follow.follower == user, Follow.idol == show_user)
        show_idols = User.select().join(Follow, on = Follow.idol_id == User.id).where(Follow.follower_id == show_user.id, Follow.approved == "1")
        length_si = show_idols.count()
            
        return redirect(url_for('users.show', username = username, show_profilepic = show_profilepic, 
        show_username = show_username, show_description = show_description, images = images, 
        show_idols = show_idols,  length_si = length_si, show_privacy = show_privacy))
        
    else: 
        flash("Username not found")
        return redirect('/')









