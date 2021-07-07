from app import *
from flask import render_template, session
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.blueprints.login.views import login_blueprint
from flask_login import LoginManager, login_user


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(login_blueprint, url_prefix="/login")


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
    return render_template('home.html', username=username)







