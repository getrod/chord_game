
import my_socket
import chord_rules
import observer
import random
import json
import time
from validator2 import Validator, chordMatch


default_settings = {
    'key-filter': list(map(lambda note: note.name, chord_rules.note_names)),
    'chord-number-filter': list(map(lambda chord_number: chord_number['number'], chord_rules.chord_numbers))
}

class ChordNumberGame(observer.Listener):
    def __init__(self):
        self.settings = dict(default_settings)
        self.validator = Validator(compare_func=chordMatch)
        self.register_socket_handlers()
        
        
    def register_socket_handlers(self):
        my_socket.pop_socket_handler('get question')
        my_socket.pop_socket_handler('get settings')
        my_socket.pop_socket_handler('get default settings')
        my_socket.pop_socket_handler('change settings')

        @my_socket.sio.on('get question')
        def on_get_question(data):
            # generate and send the next question
            key, chord_number, question = self.get_random_chord()
            self.validator.set_question_chord(question)
            my_socket.sio.emit('question', {'key': key, 'chord_number': chord_number})

        @my_socket.sio.on('get settings')
        def on_get_settings(data):
            my_socket.sio.emit('settings', self.settings)

        @my_socket.sio.on('get default settings')
        def on_get_default_settings(data):
            self.register_socket_handlers()
            # send default settings
            my_socket.sio.emit('default settings', default_settings)
            pass

        @my_socket.sio.on('change settings')
        def on_change_settings(settings):
            print('settings from server: ' + str(settings))
            # change the settings of this game
            self.settings['key-filter'] = settings['key-filter'] 
            self.settings['chord-number-filter'] = settings['chord-number-filter'] 
            
    
    def get_random_chord(self):
        key = random.choice(self.settings['key-filter'])
        chord_number = random.choice(self.settings['chord-number-filter'])
        chord = chord_rules.findChordFromChordNumber(key, chord_number)
        return key, chord_number, chord
    
    # listen to chord messages
    def on_callback(self, chords):
        for chord in chords:
            print('game chord: ' + str(chord))
            # send chord to validator
            score = self.validator.validate(chord)
            print('score chord: ' + str(score))
            if score:
                my_socket.sio.emit('score', json.dumps(score, default=my_socket.set_default))
                time.sleep(1)
                my_socket.sio.emit('get question')
                break


'''
Game {
    namespace: 'test'
    setting: {...}
}
'''