import subprocess
import socketio
import pty
import select
import os
import sys
import signal

signal.signal(signal.SIGCHLD, lambda signum, bt: os.waitpid(-1, os.WNOHANG))

class TerminalNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace, sio):
        super().__init__(namespace)
        self.sio = sio

    async def on_connect(self, sid, environ):
        print('hi')
        print('session', await self.sio.get_session(sid))
        await self.sio.emit('test', {'data': 'hi'}, room=sid)

    async def on_disconnect(self, sid):
        session = await self.sio.get_session(sid)
        os.write(session['fd'], "exit\n".encode())
        os.kill(session['child_pid'], signal.SIGKILL)

    async def on_test(self, sid, data):
        data['proc'].stdin.write(data['data'])

    async def on_create_terminal(self, sid):
        session = await self.sio.get_session(sid)

        if session:
            return

        (child_pid, fd) = pty.fork()

        if child_pid == 0:
            subprocess.run("bash")
        else:
            print("opening a new session")

            await self.sio.save_session(sid, {"fd":fd, "child_pid":child_pid})

            print("connect: child pid is", child_pid)

            self.sio.start_background_task(
                target=self.read_and_forward_pty_output, session_id=sid
            )
            
            print("connect: task started")

    async def on_client_input(self, sid, data):
        session = await self.sio.get_session(sid)
        
        if session:
            file_desc = session["fd"]

            if file_desc:
                os.write(file_desc, f"{data['input']}\n".encode())
            
            if data["input"] == "exit":
                await self.sio.disconnect(sid)
                        
    async def read_and_forward_pty_output(self, session_id):
        max_read_bytes = 1024 * 2

        while True:
            try:
                session = await self.sio.get_session(session_id)
            except KeyError:
                return

            await self.sio.sleep(0.01)

            if session:
                file_desc = session["fd"]

                if file_desc:
                    timeout_sec = 0.1
                    (data_ready, _, _) = select.select([file_desc], [], [], timeout_sec)
                    if data_ready:
                        try:
                            output = os.read(file_desc, max_read_bytes).decode()

                            if len(output) > 3 or output == r"\b":
                                await self.sio.emit(
                                    "client_output",
                                    {
                                        "output": output,
                                        "ssid": session_id,
                                    },
                                    room=session_id,
                                )
                        except OSError:
                            await self.sio.disconnect(session_id)
                            sys.exit(0)

def init_socket(app):
    sio = socketio.AsyncServer(async_mode='asgi')
    socket = socketio.ASGIApp(sio, app)

    return (socket, sio)