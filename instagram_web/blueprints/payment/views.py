
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


@payment_blueprint.route('/new/<id>', methods=['GET'])
@login_required
def new(id):
    token = gateway.client_token.generate()
    print(token)

    return render_template('/payment/new.html', token = token, id = id)


@payment_blueprint.route('/create/<id>', methods=['POST'])
@login_required
def create(id):
    nonce = request.form["nonce"]
    amount = int(request.form["amount"])
    gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    image_donated = Image.get_or_none(Image.id == id)
    existing_donation = image_donated.donation
    new_donation = existing_donation + amount 
    image_donated.donation = new_donation 
    image_donated.save()

    flash ("Thank you for your generous contribution!")
    return redirect(url_for('payment.new', id = id))
