from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base, as_declarative

@as_declarative()
class BaseModel(object):
    created = Column(DateTime, nullable=False, default=func.now())
    modified = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

Base = declarative_base(cls=BaseModel)