import subprocess
import socketio

sio = socketio.Server()

class Compile_Python(object):
    def on_get(self, req, res):
        proc = subprocess.Popen(
            ['python3', '-c', 'import time; print(input());'],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        out, err = proc.communicate(input().encode("utf-8"))

        res.body = out.decode('utf-8')