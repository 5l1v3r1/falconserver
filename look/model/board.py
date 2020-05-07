import json

from sqlalchemy import Column, Integer, String

from look.model.base import Base

class Board(Base):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)

    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __str__(self):
        return json.dumps({
            "id" : self.id,
            "name" : self.name,
            "category" : self.category,
        })