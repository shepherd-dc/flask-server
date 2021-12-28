import datetime
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()

User = namedtuple('User', ['uid', 'nickname', 'avatar', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(account, password=''):
    user_info = verify_auth_token(account)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)

    uid = data['uid']
    nickname = data['nickname']
    avatar = data['avatar']
    ac_type = data['type']
    scope = data['scope']

    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()

    return User(uid, nickname, avatar, ac_type, scope)


def decode_token_uid(token):
    """解密令牌信息"""
    info = verify_auth_token(token)
    return info.uid
