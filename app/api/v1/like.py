import time

from flask import g, request

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.article import Article
from app.models.base import db
from app.models.comment import Comment
from app.models.like import ArticleLike, CommentLike, ReplyLike
from app.models.reply import Reply
from app.validators.forms import LikeForm

api = Redprint('like')

@api.route('/article/<int:aid>', methods=['GET'])
@auth.login_required
def get_article_like(aid):
    # token = request.headers.get('SN-Token')
    like = ArticleLike.query.filter(ArticleLike.type_id == aid, ArticleLike.user_id == g.user.uid).first()
    is_liked = 0

    if like:
        is_liked = 1

    return restful_json({"is_liked": is_liked})


@api.route('/article', methods=['POST'])
@auth.login_required
def submit_article_like():
    form = LikeForm().validate_for_api()
    type_id = form.type_id.data

    with db.auto_commit():
        like = ArticleLike()
        like.type_id = type_id
        like.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        like.user_id = g.user.uid
        db.session.add(like)

    with db.auto_commit():
        article = Article.query.get(type_id)
        article.likes += 1

    return Success()


@api.route('/comment/<int:cid>', methods=['GET'])
@auth.login_required
def get_comment_like(cid):
    like = CommentLike.query.filter(CommentLike.type_id == cid, CommentLike.user_id == g.user.uid).first()
    is_liked = 0

    if like:
        is_liked = 1

    return restful_json({"is_liked": is_liked})


@api.route('/comment', methods=['POST'])
@auth.login_required
def submit_comment_like():
    form = LikeForm().validate_for_api()
    type_id = form.type_id.data

    with db.auto_commit():
        like = CommentLike()
        like.type_id = type_id
        like.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        like.user_id = g.user.uid
        db.session.add(like)

    with db.auto_commit():
        comment = Comment.query.get(type_id)
        comment.likes += 1

    return Success()


@api.route('/reply/<int:rid>', methods=['GET'])
@auth.login_required
def get_reply_like(rid):
    like = ReplyLike.query.filter(ReplyLike.type_id == rid, ReplyLike.user_id == g.user.uid).first()
    is_liked = 0

    if like:
        is_liked = 1

    return restful_json({"is_liked": is_liked})


@api.route('/reply', methods=['POST'])
@auth.login_required
def submit_reply_like():
    form = LikeForm().validate_for_api()
    type_id = form.type_id.data

    with db.auto_commit():
        like = ReplyLike()
        like.type_id = type_id
        like.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        like.user_id = g.user.uid
        db.session.add(like)

    with db.auto_commit():
        reply = Reply.query.get(type_id)
        reply.likes += 1

    return Success()
