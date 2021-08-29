import json
import time

import requests
from flask import request, g, url_for
from sqlalchemy.orm import aliased

from app.libs.error_code import Success, ParameterException
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.base import db
from app.models.comment import Comment
from app.models.reply import Reply
from app.validators.forms import CommentForm, ReplyForm

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


@api.route('/list/<int:aid>', methods=['GET'])
def get_comments_list(aid):
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


@api.route('/detail/<int:cid>', methods=['GET'])
def get_comment(cid):
    comment = Comment.query.filter_by(id=cid).first_or_404()
    return restful_json(comment)


@api.route('/reply/detail/<int:rid>', methods=['GET'])
def get_reply(rid):
    reply = Reply.query.filter_by(id=rid).first_or_404()
    return restful_json(reply)


@api.route('/reply/list/<int:rid>', methods=['GET'])
def reply_list(rid):
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    order = int(request.args.get('order', 0))

    replies = Reply.query.filter_by(reply_id=rid)

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


@api.route('/replies/<int:aid>', methods=['GET'])
def replies_list(aid):
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    order = int(request.args.get('order', 0))

    reply2 = aliased(Reply) # 同步别名作为从表

    replies = Reply.query.join(reply2, Reply.reply_id == reply2.id).filter_by(topic_id=aid)

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
def submit_comment():
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


@api.route('/reply/submit', methods=['POST'])
@auth.login_required
def submit_reply():
    form = ReplyForm().validate_for_api()
    reply_type = form.reply_type.data
    reply_id = form.reply_id.data

    with db.auto_commit():
        reply = Reply()
        reply.content = form.content.data
        reply.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        reply.to_uid = form.to_uid.data
        reply.to_name = form.to_name.data
        reply.from_uid = g.user.uid
        reply.from_name = g.user.nickname
        reply.comment_id = form.comment_id.data
        reply.topic_id = form.topic_id.data
        reply.topic_type = form.topic_type.data
        reply.reply_type = reply_type
        if reply_type == 'reply':
            if reply_id:
                reply.reply_id = form.reply_id.data
            else:
                return ParameterException(msg='reply_id is required')
        elif reply_type != 'comment':
            return ParameterException(msg='reply_type is invalid')

        db.session.add(reply)

    return Success()
