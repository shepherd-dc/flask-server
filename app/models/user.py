from sqlalchemy import Column, Integer, String, SmallInteger, orm, or_
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed, UsernameFailed, PasswordFailed
from app.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'nickname', 'auth', 'status', 'create_time']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def verify(account, password):
        user = User.query.filter(or_(User.nickname==account, User.email==account)).first()
        if not user:
            raise UsernameFailed()
        if not user.check_password(password):
            raise PasswordFailed()

        if user.auth == 2:
            scope = 'AdminScope'
        # elif user.auth == 3:
        #     scope = 'SuperScope'
        else:
            scope = 'UserScope'
        return {
            'uid': user.id,
            'nickname': user.nickname,
            'scope': scope
        }

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
