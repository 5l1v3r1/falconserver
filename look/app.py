import falcon.asgi

from look.session import init_session
from look.socket import TerminalNamespace, init_socket
from look.api import user
from look.api.compile import Compile
from look.middleware.jsontranslator import JSONTranslator
from look.middleware.sessionmanager import SessionManager
from look.middleware.socketmanager import SocketManager

middleware = [
    JSONTranslator(),
    SessionManager(init_session()),
]

app = application = falcon.asgi.App(middleware=middleware)
socket, sio = init_socket(app)
sio.register_namespace(TerminalNamespace('/', sio))
app.add_middleware(SocketManager(sio))

class Test(object):
    async def on_get(self, req, res):
        res.body = "Hello, World!"

app.add_route('/', Test())
app.add_route('/api/user', user.Collection())
app.add_route('/api/user/{id}', user.Item())

app.add_route('/api/compile/{lang}', Compile())