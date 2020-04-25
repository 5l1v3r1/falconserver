import falcon

from look.session import init_session
from look.api import user
from look.middleware.jsontranslator import JSONTranslator
from look.middleware.sessionmanager import SessionManager

middleware = [
    JSONTranslator(),
    SessionManager(init_session())
]

api = application = falcon.API(middleware=middleware)

class Test(object):
    def on_get(self, req, res):
        res.body = "Hello, World!"

api.add_route('/', Test())
api.add_route('/api/user', user.Collection())
api.add_route('/api/user/{id}', user.Item())