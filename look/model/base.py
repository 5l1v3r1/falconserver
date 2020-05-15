import json
import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base, as_declarative

@as_declarative()
class BaseModel(object):
    created = Column(DateTime, nullable=False, default=func.now())
    modified = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def get_data(self, col_list, depth=0):
        tmp_rels = {}
        for relationship in self.__mapper__.relationships.keys():
            tmp_rel_model = getattr(self, relationship)
            if tmp_rel_model:
                tmp_rels[relationship] = tmp_rel_model[0].__table__.columns.keys()
            else:
                tmp_rels[relationship] = []
        
        for relationship in self.__mapper__.relationships.keys():
            col_list.append(relationship)

        tmp = {}
        for arg in col_list:
            tmp_attr = getattr(self, arg)
            if arg in tmp_rels:
                if depth > 0:
                    tmp[arg] = [json.loads(obj.get_data(tmp_rels[arg], depth=depth-1)) for obj in tmp_attr]
                elif depth == -1:
                    tmp[arg] = [json.loads(obj.get_data(tmp_rels[arg], depth=depth)) for obj in tmp_attr]
            else:
                if type(tmp_attr) == datetime.datetime: tmp_attr = str(tmp_attr)
                tmp[arg] = tmp_attr
        return json.dumps(tmp)

    def __str__(self):
        cols = self.__table__.columns.keys()
        for relationship in self.__mapper__.relationships.keys():
            cols.append(relationship)
        return self.get_data(*tuple(cols))

Base = declarative_base(cls=BaseModel)