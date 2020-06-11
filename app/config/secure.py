from datetime import timedelta

import os

DEBUG = True
SECRET_KEY = os.urandom(24)
TOKEN_EXPIRATION = 7 * 24 * 3600
REMEMBER_COOKIE_DURATION = timedelta(days=7)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

UPLOAD_IMAGE_FOLDER = '/uploads/images'
UPLOAD_FILE_FOLDER = '/uploads/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'cymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'shepherdnet'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'\
    .format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
