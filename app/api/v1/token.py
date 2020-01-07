import time

import datetime
from flask import current_app, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = promise[form.type.data](form.account.data, form.secret.data)

    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'], identity['nickname'], form.type.data, identity['scope'], expiration)
    t = {
        'token': token.decode('ascii')
    }
    return restful_json(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'uid': data[0]['uid'],
        'nickname': data[0]['nickname'],
        'scope': data[0]['scope'],
        'create_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[1]['iat'])),
        'expire_in': datetime.datetime.utcfromtimestamp(data[1]['exp']).strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(r)


def generate_auth_token(uid, nickname, ac_type, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'nickname': nickname,
        'type': ac_type.value,
        'scope': scope
    })
