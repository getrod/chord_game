import my_socket
import observer
import chord_rules
import random
import time
import json
from validator2 import Validator, chordMatch

namespace = '\\random_chord_game'
default_settings = {
    'key-filter': list(map(lambda note: note.name, chord_rules.note_names)),
    'chord-type-filter': list(map(lambda chord_type: chord_type['name'], chord_rules.chord_types)),
    'voice-filter': list(set(map(lambda voice_rule: voice_rule['name'], chord_rules.voice_rules))),
    'use-voice': False
}

class RandomChordGame(observer.Listener):
    def __init__(self):
        self.settings = dict(default_settings)
        self.validator = Validator(compare_func=chordMatch, use_voice=self.settings['use-voice'])
        self.register_socket_handlers()

    
    def register_socket_handlers(self):
        my_socket.pop_socket_handler('get question')
        my_socket.pop_socket_handler('get settings')
        my_socket.pop_socket_handler('get default settings')
        my_socket.pop_socket_handler('change settings')
        @my_socket.sio.on('get question')

        def on_get_question(data):
            # generate and send the next question
            question = self.get_random_chord()
            self.validator.set_question_chord(question)
            my_socket.sio.emit('question', json.dumps(question, default=my_socket.set_default))

        @my_socket.sio.on('get settings')
        def on_get_settings(data):
            # send settings
            my_socket.sio.emit('settings', self.settings)

        @my_socket.sio.on('get default settings')
        def on_get_default_settings(data):
            self.register_socket_handlers()
            # send default settings
            my_socket.sio.emit('default settings', default_settings)

        @my_socket.sio.on('change settings')
        def on_change_settings(settings):
            print("settings from server: " + str(settings))
            # change the settings of this game
            self.settings['key-filter'] = settings['key-filter'] 
            self.settings['chord-type-filter'] = settings['chord-type-filter']
            self.settings['voice-filter'] = settings['voice-filter']
            self.settings['use-voice'] = settings['use-voice']
            self.validator.use_voice = self.settings['use-voice']
    
    def get_random_chord(self):
        key = random.choice(self.settings['key-filter'])
        chord_type = random.choice(self.settings['chord-type-filter'])
        # get the chord type object
        chord_type = list(filter(lambda chord_type_: chord_type_['name'] == chord_type, chord_rules.chord_types))[0]
        voice_rule = random.choice(self.settings['voice-filter'])

        if self.settings['use-voice']:
            # get size of chord formula
            size = len(chord_type['formula'])
            # make an array of voices with that size (ie. 3 for trias)
            filtered_voices = list(filter(lambda voice: voice['name'] == voice_rule and len(voice['voice']) == size, chord_rules.voice_rules))

            if len(filtered_voices) == 0:
                voice_rule = None
            else:
                # out of that filtered voice array, randomly choose a voice
                voice_rule = random.choice(filtered_voices)
        else: voice_rule = None
        notes = chord_rules.numbersToNotes(key, chord_type['formula'])
        return chord_rules.Chord(key=key, notes=notes, type=chord_type, voice=voice_rule)

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