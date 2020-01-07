from sqlalchemy import Column, Integer, String, orm, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Article(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    author = Column(String(30))
    content = Column(Text(), nullable=False)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'author', 'content', 'user_id', 'status', 'create_time']
