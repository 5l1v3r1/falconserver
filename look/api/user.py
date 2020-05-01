import json
from falcon import HTTP_400, HTTP_200

from sqlalchemy.exc import IntegrityError

from look.model.user import User as UserModel

class Collection(object):
    async def on_post(self, req, res):
        user_data = req.context['data']
        session = req.context['db_session']
        print(user_data)
        if user_data and ("email" in user_data) and ("name" in user_data) and ("password" in user_data):
            session.add(UserModel(email=user_data['email'], name=user_data['name'], password=user_data['password']))

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                res.status = HTTP_400
                res.body = json.dumps({
                    "result" : "ERROR",
                    "description" : "DUPLICATE EMAIL",
                    "data" : "",
                })
            else:
                res.status = HTTP_200
                res.body = json.dumps({
                    "result" : "OK",
                    "description" : "",
                    "data" : "",
                })
        else:
            res.status = HTTP_400
            res.body = json.dumps({
                "result" : "ERROR",
                "description" : "INVALID PARAMETER",
                "data" : "",
            })
    
    async def on_get(self, req, res):
        session = req.context['db_session']
        user_dbs = session.query(UserModel).all()
        if user_dbs:
            res.status = HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : [json.loads(str(row)) for row in user_dbs],
            })

class Item(object):
    async def on_get(self, req, res, id):
        session = req.context['db_session']
        user_dbs = session.query(UserModel).filter(UserModel.id == id).first()
        if user_dbs:
            res.status = HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : json.loads(str(user_dbs)),
            })