import time

from flask import request, g

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.base import db
from app.models.comment import Comment
from app.models.reply import Reply
from app.validators.forms import CommentForm

api = Redprint('comment')

@api.route('', methods=['GET'])
def comment_list():
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    order = int(request.args.get('order', 0))

    comments = Comment.query

    if order and order == 1:
        comments = comments.order_by(Comment.create_time.asc())
    else:
        comments = comments.order_by(Comment.create_time.desc())

    total = comments.count()
    comments = comments.limit(page_size).offset((page_index - 1) * page_size).all()

    data = {
        "total": total,
        "data": comments
    }
    return restful_json(data)


@api.route('/<int:aid>', methods=['GET'])
def get_comments(aid):
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    order = int(request.args.get('order', 0))

    comments = Comment.query.filter_by(topic_id=aid)

    if order and order == 1:
        comments = comments.order_by(Comment.create_time.asc())
    else:
        comments = comments.order_by(Comment.create_time.desc())

    total = comments.count()
    comments = comments.limit(page_size).offset((page_index - 1) * page_size).all()

    data = {
        "total": total,
        "data": comments
    }
    return restful_json(data)


@api.route('/reply', methods=['GET'])
def reply_list():
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    order = int(request.args.get('order', 0))

    replies = Reply.query

    if order and order == 1:
        replies = replies.order_by(Reply.create_time.asc())
    else:
        replies = replies.order_by(Reply.create_time.desc())

    total = replies.count()
    replies = replies.limit(page_size).offset((page_index - 1) * page_size).all()

    data = {
        "total": total,
        "data": replies
    }
    return restful_json(data)


@api.route('/submit', methods=['POST'])
@auth.login_required
def publish_article():
    form = CommentForm().validate_for_api()

    with db.auto_commit():
        comment = Comment()
        comment.topic_id = form.topic_id.data
        comment.content = form.content.data
        comment.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        comment.from_uid = g.user.uid
        comment.from_name = g.user.nickname
        db.session.add(comment)

    return Success()
