import socketio

sio = socketio.Client()
sio.connect('http://localhost:3000')

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError