from sqlalchemy import Column, Integer, String, orm, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Article(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30))
    content = Column(Text(), nullable=False)
    column_id = Column(Integer, nullable=False)
    column_name = Column(String(10))
    menu_id = Column(Integer, nullable=False)
    menu_name = Column(String(10))
    en_name = Column(String(10))
    recommend = Column(Integer, nullable=False, default=0)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'author', 'content', 'user_id', 'status',
                       'column_id', 'column_name', 'menu_id', 'menu_name', 'en_name', 'create_time', 'recommend']
