import imp
from my_socket import *
from chord_rules import *
from observer import *
import json

class ChordQuestion(Provider, Listener):
    def __init__(self):
        # listen to get question event
        super().__init__()

        @sio.on('get question')
        def on_message(data):
            print('I got a question for the question class!')
            questionChord = getRandomChord(True)
            self.update_listeners(('q', questionChord)) # revc by validator
            sio.emit('on question', json.dumps(questionChord, default=set_default),)
    
    def on_callback(self, score):
        # handle logic to deal with the score returned
        pass
    