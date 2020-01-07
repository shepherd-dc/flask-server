from .app import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    register_blueprints(app)
    register_plugins(app)

    return app


def register_blueprints(app):
    # from app.api.v1.user import user
    # from app.api.v1.book import book
    # app.register_blueprint(user)
    # app.register_blueprint(book)
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugins(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
