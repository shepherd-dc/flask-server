import base64
import time

from flask import g, request

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.article import Article
from app.models.base import db
from app.models.star import ArticleStar
from app.validators.forms import starForm

api = Redprint('star')

@api.route('/article/<int:aid>', methods=['GET'])
@auth.login_required
def get_article_star(aid):
    # token = request.headers.get('SN-Token')
    star = ArticleStar.query.filter(ArticleStar.type_id == aid, ArticleStar.user_id == g.user.uid).first()
    is_stared = 0

    if star:
        is_stared = 1

    return restful_json({"is_stared": is_stared})


@api.route('/articles/user', methods=['GET'])
@auth.login_required
def get_user_articles_likes():
    '''
    给定文章列表中，当前用户收藏过的文章
    :return: [{ type: 'article', type_id: int}, ...]
    '''
    list = request.values.get('list', '')
    result = []

    if list:
        list = base64.b64decode(list).decode().split(',')
        list = [int(l) for l in list]

        result = ArticleStar.query.filter(ArticleStar.type_id.in_(list), ArticleStar.user_id == g.user.uid).all()

        [like.hide('id', 'create_time', 'status', 'user_id') for like in result]

    return restful_json(result)


@api.route('/article', methods=['POST'])
@auth.login_required
def submit_star():
    form = starForm().validate_for_api()
    type_id = form.type_id.data

    with db.auto_commit():
        star = ArticleStar()
        star.type_id = type_id
        star.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        star.user_id = g.user.uid
        db.session.add(star)

        article = Article.query.get(type_id)
        article.stars += 1

    return Success()


@api.route('/article', methods=['DELETE'])
@auth.login_required
def cancel_star():
    data = request.get_json('type_id')
    type_id = data['type_id']

    with db.auto_commit():
        star = ArticleStar.query.filter(ArticleStar.type_id == type_id, ArticleStar.user_id == g.user.uid).first()
        db.session.delete(star)

        article = Article.query.get(type_id)
        article.stars -= 1

    return Success()
