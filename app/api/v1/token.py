import base64
import time

import datetime

from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from app.libs.des import PyDES3
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import TokenInvalid
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm

api = Redprint('token')


@api.route('', methods=['POST'])
def grant_token():
    form = ClientForm().validate_for_api()
    account = PyDES3().decrypt(form.account.data)
    secret = PyDES3().decrypt(form.secret.data)
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = promise[form.type.data](account, secret)
    ac_type = form.type.data
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity, ac_type, expiration)
    t = {
        'token': token.decode('ascii'),
        'nickname': account,
        'avatar': identity['avatar']
    }
    return restful_json(t), 201


@api.route('/code', methods=['GET'])
def grant_public_key():
    key = PyDES3.des_key
    return restful_json(key)

@api.route('/code/key', methods=['GET'])
def grant_base64_key():
    key = PyDES3.des_key
    base64_key = base64.b64encode(key.encode()).decode()
    return restful_json(base64_key)

@api.route('/decode', methods=['POST'])
def decode_data():
    params = request.get_json()
    data = params['data']
    decode_data = PyDES3().decrypt(data)
    return restful_json({
        "raw": data,
        "decode": decode_data
    })


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise TokenInvalid(msg='token is expired', error_code=1003)
    except BadSignature:
        raise TokenInvalid(msg='token is invalid', error_code=1002)

    r = {
        # 'uid': data[0]['uid'],
        'nickname': PyDES3().encrypt(data[0]['nickname']),
        'avatar': PyDES3().encrypt(data[0]['avatar']),
        'scope': PyDES3().encrypt(data[0]['scope']),
        'create_at': PyDES3().encrypt(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[1]['iat']))),
        'expire_in': PyDES3().encrypt(datetime.datetime.utcfromtimestamp(data[1]['exp']).strftime('%Y-%m-%d %H:%M:%S'))
    }
    return restful_json(r)


def generate_auth_token(identity, ac_type, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    uid = identity['uid']
    nickname = identity['nickname']
    avatar = identity['avatar']
    scope = identity['scope']
    return s.dumps({
        'uid': uid,
        'nickname': nickname,
        'avatar': avatar,
        'scope': scope,
        'type': ac_type.value
    })
