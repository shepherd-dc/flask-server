from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy.orm import relationship

from app.models.base import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)
    submenu = relationship('Submenu', backref='menu')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'menu_name', 'en_name', 'status', 'submenu']


