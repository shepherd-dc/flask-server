from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = -1


class UsernameFailed(APIException):
    code = 202
    msg = '用户不存在'
    error_code = 1002


class PasswordFailed(APIException):
    code = 202
    msg = '密码错误'
    error_code = 1003


class LoginFailed(APIException):
    code = 202
    msg = '用户名或密码错误'
    error_code = 1003


class ServerException(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006
    description = (
    )


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'


class FileSizeLimit(APIException):
    code = 413
    error_code = 2002
    msg = '附件大小不能超过12M'





