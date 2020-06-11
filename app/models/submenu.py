from sqlalchemy import Column, Integer, String, ForeignKey, orm, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    menu_name = Column(String(50))
    path = Column(String(50), nullable=False)
    pic = Column(String(512), nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    description = Column(Text(), nullable=False)
    official_doc = Column(String(100), nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'path', 'pic', 'menu_name', 'menu_id', 'description', 'official_doc', 'status', 'create_time']
