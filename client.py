import requests
from observer import Listener
import json
from my_socket import *

class ChordClient(Listener):
    def __init__(self, chord_interpreter):
        chord_interpreter.subscribe(self)

    def on_callback(self, message):
        print(message)
        sio.emit('on question', json.dumps(message, default=set_default))
        # requests.post('http://127.0.0.1:5000/chord', json=json.dumps(message, default=set_default))
