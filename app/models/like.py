from sqlalchemy import Column, Integer, ForeignKey, orm, String

from app.models.base import Base


class ArticleLike(Base):
    __tablename__ = 'article_like'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False, default="article")
    type_id = Column(Integer, ForeignKey('article.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'type', 'type_id', 'user_id', 'status', 'create_time']


class CommentLike(Base):
    __tablename__ = 'comment_like'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False, default="comment")
    type_id = Column(Integer, ForeignKey('comment.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'type', 'type_id', 'user_id', 'status', 'create_time']


class ReplyLike(Base):
    __tablename__ = 'reply_like'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False, default="reply")
    type_id = Column(Integer, ForeignKey('reply.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'type', 'type_id', 'user_id', 'status', 'create_time']
