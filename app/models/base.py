import time
from contextlib import contextmanager
from datetime import datetime

from flask import flash
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Integer, SmallInteger, Column, String

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, msg='操作成功'):
        try:
            yield
            self.session.commit()
            flash(msg)
        except Exception as e:
            self.session.rollback()
            raise e


class MyQuery(BaseQuery):
    def filter_by(self, **kwargs):
        # if 'status' not in kwargs.keys():
        #     kwargs['status'] = 1
        return super(MyQuery, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=MyQuery)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', String(50))
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
