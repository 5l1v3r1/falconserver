import json

from falcon import HTTP_400, HTTP_200
from falcon.uri import parse_query_string

from sqlalchemy.exc import IntegrityError

class BaseCollection(object):
    def __init__(self, model, *attrs):
        self.model = model
        if not attrs:
            attrs = model.__table__.columns.keys()
            for relationship in model.__mapper__.relationships.keys():
                attrs.append(relationship)
        if type(attrs) == tuple:
            self.attrs = list(attrs)
        else: self.attrs = attrs
        
    async def on_post(self, req, res):
        data = req.context['data']
        db_session = req.context['db_session']
        print(data)
        if data:
            try:
                tmp_attrs = {col:data[col] for col in data.keys()}
                db_session.add(self.model(**tmp_attrs))
            except TypeError:
                res.status = HTTP_400
                res.body = json.dumps({
                    "result" : "ERROR",
                    "description" : "INVALID PARAMETER",
                    "data" : "",
                })
            else:
                try:
                    db_session.commit()
                except IntegrityError:
                    db_session.rollback()
                    res.status = HTTP_400
                    res.body = json.dumps({
                        "result" : "ERROR",
                        "description" : "DUPLICATE USERNAME OR EMAIL",
                        "data" : "",
                    })
                else:
                    res.status = HTTP_200
                    res.body = json.dumps({
                        "result" : "OK",
                        "description" : "",
                        "data" : "",
                    })
    
    async def on_get(self, req, res):
        db_session = req.context['db_session']
        user_dbs = db_session.query(self.model).all()
        depth = 0

        if req.query_string:
            query = parse_query_string(req.query_string)

            if 'depth' in query:
                try:
                    depth = int(query['depth'])
                except ValueError:
                    pass

        if user_dbs:
            res.status = HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : [json.loads(row.get_data(self.attrs, depth=depth)) for row in user_dbs],
            })

class BaseItem(object):
    def __init__(self, model, *attrs):
        self.model = model
        if not attrs:
            attrs = model.__table__.columns.keys()
            for relationship in model.__mapper__.relationships.keys():
                attrs.append(relationship)
        if type(attrs) == tuple:
            self.attrs = list(attrs)

    async def on_get(self, req, res, id):
        db_session = req.context['db_session']
        user_dbs = db_session.query(self.model).filter(self.model.id == id).first()
        depth = 0

        if req.query_string:
            query = parse_query_string(req.query_string)

            if 'depth' in query:
                try:
                    depth = int(query['depth'])
                except ValueError:
                    pass

        if user_dbs:
            res.status = HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : json.loads(row.get_data(self.attrs, depth=depth)),
            })