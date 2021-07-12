
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models import * 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.user import User 
import re
from flask_login import login_user, login_required
from instagram_web.util.helpers import upload_file_to_s3
from app import *
from models.images import Image
from peewee import prefetch 
from instagram_web.util.payment import gateway


payment_blueprint = Blueprint('payment',
                            __name__,
                            template_folder='templates')


@payment_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    token = gateway.client_token.generate()
    print(token)
    user_id = session['user_id'] 
    user = User.get_or_none(User.id == user_id)
    username = user.username

    return render_template('/payment/new.html', token = token, username=username)


@payment_blueprint.route('/create', methods=['POST'])
@login_required
def create():
    nonce = request.form["nonce"]
    gateway.transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    flash ("Thank you for your generous donation!")
    return redirect(url_for('payment.new'))
