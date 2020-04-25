import json

from sqlalchemy import Column, Integer, String

from look.model.base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def __str__(self):
        return json.dumps({
            "id" : self.id,
            "email" : self.email,
            "name" : self.name,
            "password" : self.password,
        })