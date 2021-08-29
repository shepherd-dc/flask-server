from sqlalchemy import Column, Integer, ForeignKey, String, Text, orm
from sqlalchemy.orm import relationship

from app.models.base import Base


class Reply(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer)
    topic_type = Column(String(10))
    comment_id = Column(Integer, ForeignKey('comment.id'))
    reply_id = Column(Integer)
    reply_type = Column(String(10))
    content = Column(Text(), nullable=False)
    user = relationship('User')
    from_uid = Column(Integer, ForeignKey('user.id'))
    from_name = Column(String(30))
    to_uid = Column(Integer, nullable=False)
    to_name = Column(String(30))
    likes = Column(Integer, nullable=False, default=0)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'topic_id', 'topic_type', 'comment_id', 'reply_id', 'reply_type', 'content',
                       'from_name', 'from_uid', 'to_uid', 'to_name', 'create_time', 'likes']
