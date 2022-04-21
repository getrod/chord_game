import socketio

sio = socketio.Client()
sio.connect('http://localhost:3000')

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def pop_socket_handler(event):
    if '/' not in sio.handlers: return
    if event in sio.handlers['/']:
        sio.handlers['/'].pop(event)