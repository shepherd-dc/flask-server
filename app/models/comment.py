from sqlalchemy import Column, Integer, String, Text, ForeignKey, orm
from sqlalchemy.orm import relationship

from app.models.base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey('article.id'))
    topic_type = Column(String(10))
    content = Column(Text(), nullable=False)
    user = relationship('User')
    from_uid = Column(Integer, ForeignKey('user.id'))
    from_name = Column(String(30))
    replies = relationship('Reply', backref='comment')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'topic_id', 'topic_type', 'content', 'from_name', 'from_uid', 'replies', 'create_time']