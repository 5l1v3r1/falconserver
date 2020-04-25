import json
import falcon

from sqlalchemy.exc import IntegrityError

from look.model.user import User as UserModel

class Collection(object):
    def on_post(self, req, res):
        user_data = req.context['data']
        session = req.context['db_session']
        print(user_data)
        if user_data and ("email" in user_data) and ("name" in user_data) and ("password" in user_data):
            session.add(UserModel(email=user_data['email'], name=user_data['name'], password=user_data['password']))

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                res.status = falcon.HTTP_400
                res.body = json.dumps({
                    "result" : "ERROR",
                    "description" : "DUPLICATE EMAIL",
                    "data" : "",
                })
            else:
                res.status = falcon.HTTP_200
                res.body = json.dumps({
                    "result" : "OK",
                    "description" : "",
                    "data" : "",
                })
        else:
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                "result" : "ERROR",
                "description" : "INVALID PARAMETER",
                "data" : "",
            })
    
    def on_get(self, req, res):
        session = req.context['db_session']
        user_dbs = session.query(UserModel).all()
        if user_dbs:
            res.status = falcon.HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : [json.loads(str(row)) for row in user_dbs],
            })

class Item(object):
    def on_get(self, req, res, id):
        session = req.context['db_session']
        user_dbs = session.query(UserModel).filter(UserModel.id == id).first()
        if user_dbs:
            res.status = falcon.HTTP_200
            res.body = json.dumps({
                'result' : 'OK',
                'description' : '',
                'data' : json.loads(str(user_dbs)),
            })