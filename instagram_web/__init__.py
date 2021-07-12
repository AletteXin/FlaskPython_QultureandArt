from app import *
from flask import render_template, session
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
            username = user.username
    else:
        username = None

    users = User.select()
    images = Image.select().order_by(Image.date_posted.desc())
    users_with_images = prefetch(images, users)
    return render_template('home.html', username=username, users_with_images=users_with_images)


    # users = User.select()
    # images = Image.select().order_by(Image.date_posted.desc())
    # users_with_images = prefetch(users, images)
    # return render_template('home.html', username=username, users_with_images=users_with_images)









