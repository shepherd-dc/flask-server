from sqlalchemy import Column, Integer, ForeignKey, orm, String

from app.models.base import Base


class ArticleStar(Base):
    __tablename__ = 'article_star'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False, default="article")
    type_id = Column(Integer, ForeignKey('article.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'type', 'type_id', 'user_id', 'status', 'create_time']
