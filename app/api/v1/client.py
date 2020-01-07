import time

from flask import request, session, jsonify
from flask_login import login_user
from sqlalchemy import or_

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success, LoginFailed
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.models.base import db
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm, LoginForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()

    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    with db.auto_commit():
        user = User()
        user.nickname = form.nickname.data
        user.email = form.account.data
        user.password = form.secret.data
        user.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db.session.add(user)


@api.route('/login', methods=['POST'])
def login():
    form = LoginForm().validate_for_api()
    user = User.query.filter(or_(User.nickname==form.account.data, User.email==form.account.data)).first()
    if user and user.check_password(form.secret.data):
        # login_user(user, remember=True)
        # session.permanent = True
        return restful_json(user)
    else:
        return LoginFailed()

