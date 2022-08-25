import eventlet
import socketio
import string
import os
from pathlib import Path


def mimetyped(path):
    types = {
        "html": "text/html",
        "txt": "text/plain",
        "js": "application/javascript",
        "css": "text/css",
    }
    return {
        "content_type": types.get(path.split(".")[-1], "text/plain"),
        "filename": path,
    }


paths = [
    os.path.join(*path.parts[1:])
    for path in Path("chat-frontend").rglob("*")
    if ".git" not in path.parts
]
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(
    sio,
    static_files={**{
        "/" + path: mimetyped(os.path.join("chat-frontend", path)) for path in paths
    }, **{
        "/": mimetyped("chat-frontend/index.html"),
    }},
)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.on("message")
def message(sid, data):
    print("message ", data)
    if not data["content"]:
        return
    if not data["author"]:
        return
    if len(data["author"]) > 25:
        sio.emit("error", "invalid userename", room=sid)
        return
    for character in data["author"]:
        if character not in string.ascii_letters + string.digits + "_-":
            sio.emit("error", "invalid userename", room=sid)
            return
    if len(data["content"]) > 2000:
        sio.emit("error", "message too large", room=sid)
        return
    sio.emit("message", {"content": data["content"], "author": data["author"]})


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
