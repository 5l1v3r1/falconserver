import falcon.asgi

from look.db import init_db, insert_dummy_data
from look.socket import TerminalNamespace, init_socket
from look.api import user, category, board, chapter, subchapter
from look.middleware.jsontranslator import JSONTranslator
from look.middleware.dbmanager import DBManager
from look.middleware.socketmanager import SocketManager

db_session = init_db()
# insert_dummy_data(db_session())
middleware = [
    JSONTranslator(),
    DBManager(db_session),
]

app = application = falcon.asgi.App(middleware=middleware)
socket, sio = init_socket(app)
sio.register_namespace(TerminalNamespace('/', sio))
app.add_middleware(SocketManager(sio))

class RootPage(object):
    async def on_get(self, req, res):
        res.body = "Hello, World!"

app.add_route('/', RootPage())

app.add_route('/api/user', user.Collection())
app.add_route('/api/user/{id}', user.Item())

app.add_route('/api/category', category.Collection())
app.add_route('/api/category/{id}', category.Item())

app.add_route('/api/board', board.Collection())
app.add_route('/api/board/{id}', board.Item())

app.add_route('/api/chapter', chapter.Collection())
app.add_route('/api/chapter/{id}', chapter.Item())

app.add_route('/api/subchapter', subchapter.Collection())
app.add_route('/api/subchapter/{id}', subchapter.Item())