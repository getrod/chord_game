from observer import *

MIDI_MESSAGE = 0
MIDI_NOTE = 1
MIDI_VELOCITY = 2
MIDI_MESSAGE_NOTE_ON = 144
# note to string function?

class Instrument(Listener, Provider):
    on_notes = set()

    '''When midi_provider recieves a midi message'''
    def on_callback(self, message):
        if message[MIDI_MESSAGE] == MIDI_MESSAGE_NOTE_ON:
            if message[MIDI_VELOCITY] == 0:
                self.on_notes.remove(message[MIDI_NOTE])
            else: self.on_notes.add(message[MIDI_NOTE])
        # print(self.on_notes)
        if self.on_notes:
            self.callback(self.on_notes)

    '''Update listeners (in this case, the chord interpereter)'''
    def callback(self, message):
        self.update_listeners(message)
