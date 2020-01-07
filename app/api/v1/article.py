import time

from flask import request, g

from app.libs.error_code import Success, DeleteSuccess, ParameterException
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.article import Article
from app.models.base import db
from app.models.user import User
from app.validators.forms import ArticleForm

api = Redprint('article')


@api.route('', methods=['GET'])
def article_list():
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 10))
    title = request.args.get('title', None)
    order = int(request.args.get('order', 0))

    articles = Article.query

    if title:
        articles = articles.filter(Article.title.like('%' + title + '%'))

    if order and order == 1:
        articles = articles.order_by(Article.create_time.asc())
    else:
        articles = articles.order_by(Article.create_time.desc())


    total = articles.count()
    articles = articles.limit(page_size).offset((page_index - 1) * page_size).all()

    data = {
        "total": total,
        "data": articles
    }
    return restful_json(data)


@api.route('/<int:aid>', methods=['GET'])
def get_article(aid):
    article = Article.query.filter_by(id=aid).first_or_404()
    return restful_json(article)


@api.route('/publish', methods=['POST'])
# @auth.login_required
def publish_article():
    form = ArticleForm().validate_for_api()

    # user_id = form.user_id.data

    create_time = form.create_time.data


    with db.auto_commit():
        article = Article()
        article.title = form.title.data
        article.author = form.author.data
        article.content = form.content.data
        article.status = form.status.data

        # if user_id:
        #     article.user_id =user_id
        # else:
        #     article.user_id = g.user.uid

        if create_time:
            article.create_time = create_time
        else:
            article.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        db.session.add(article)
    return Success()


@api.route('/edit', methods=['PUT'])
# @auth.login_required
def edit_article():
    form = ArticleForm().validate_for_api()
    # data = request.get_json()
    # id = data['id']
    id = int(form.id.data)

    with db.auto_commit():
        article = Article.query.get(id)
        article.title = form.title.data
        article.author = form.author.data
        article.content = form.content.data
    return Success()


@api.route('/delete', methods=['POST', 'DELETE'])
# @auth.login_required
def delete_article():
    data = request.get_json('id')
    article = Article.query.filter_by(id=data['id']).first_or_404()

    if request.method == 'POST':
        with db.auto_commit():
            article.status = 0

    if request.method == 'DELETE':
        with db.auto_commit():
            db.session.delete(article)

    return DeleteSuccess()
