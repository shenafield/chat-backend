import eventlet
import socketio
import string

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


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
