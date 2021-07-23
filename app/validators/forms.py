from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.des import PyDES3
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='账号不能为空'), length(
        min=2, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    # account = StringField(validators=[
    #     Email(message='邮箱格式不正确')
    # ])
    secret = StringField(validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9_*&$#@=]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        email = PyDES3().decrypt(value.data)
        if User.query.filter_by(email=email).first():
            raise ValidationError(message='邮箱已注册')

    def validate_nickname(self, value):
        nickname = PyDES3().decrypt(value.data)
        if User.query.filter_by(nickname=nickname).first():
            raise ValidationError(message='昵称已注册')


class EmailForm(BaseForm):
    # email = StringField(validators=[
    #     Email(message='邮箱格式不正确')
    # ])
    email = StringField(validators=[DataRequired(message='邮箱不能为空')])


class NicknameForm(BaseForm):
    nickname = StringField(validators=[DataRequired()])


class BookSearchForm(BaseForm):
    q = StringField(validators=[DataRequired()])


class TokenForm(BaseForm):
    token = StringField(validators=[DataRequired()])


class LoginForm(BaseForm):
    account = StringField(validators=[DataRequired()])
    secret = StringField(validators=[DataRequired()])


class MenuForm(BaseForm):
    menu_name = StringField(validators=[DataRequired()])
    en_name = StringField(validators=[DataRequired()])


class SubmenuForm(BaseForm):
    id = IntegerField()
    name_zh = StringField(validators=[DataRequired()])
    name_en = StringField(validators=[DataRequired()])
    path = StringField(validators=[DataRequired()])
    pic = StringField(validators=[DataRequired()])
    menu_id = IntegerField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    official_doc = StringField(validators=[DataRequired()])
    status = IntegerField(validators=[DataRequired()])


class ArticleForm(BaseForm):
    id = IntegerField()
    title = StringField(validators=[DataRequired()])
    author = StringField()
    create_time = StringField()
    content = StringField(validators=[DataRequired()])
    column_id = IntegerField(validators=[DataRequired()])
    user_id = IntegerField()
    recommend = IntegerField()
    status = IntegerField()


class UserForm(BaseForm):
    id = IntegerField()
    auth = IntegerField(validators=[DataRequired()])
    nickname = StringField(validators=[DataRequired()])
    email = StringField(validators=[
        DataRequired(),
        # Email(message='邮箱格式不正确')
    ])
    password = StringField(validators=[DataRequired()])
    create_time = StringField()
    status = IntegerField()


class UploadForm(BaseForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()


class CommentForm(BaseForm):
    id = IntegerField()
    from_uid = IntegerField()
    content = StringField(validators=[DataRequired()])
    topic_id = IntegerField(validators=[DataRequired()])
    topic_type = StringField()


class ReplyForm(BaseForm):
    id = IntegerField()
    to_uid = IntegerField(validators=[DataRequired()])
    to_name = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    comment_id = IntegerField()
    topic_id = IntegerField(validators=[DataRequired()])
    topic_type = StringField()
    reply_id = IntegerField()
    reply_type = StringField(validators=[DataRequired()])
