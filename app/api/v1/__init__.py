from flask import Blueprint
from app.api.v1 import user, client, token, article, upload, menu, comment, like, star


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    # user.api.register(bp_v1, url_prefix = '/user')
    # if url_prefix is None: url_prefix = '/' + Redprint().name
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    article.api.register(bp_v1)
    upload.api.register(bp_v1)
    menu.api.register(bp_v1)
    comment.api.register(bp_v1)
    like.api.register(bp_v1)
    star.api.register(bp_v1)

    return bp_v1
